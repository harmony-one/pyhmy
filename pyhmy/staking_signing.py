"""
Sign Harmony staking transactions
"""

import math

from decimal import Decimal

from functools import partial
from toolz import (
    pipe,
    dissoc,
    merge,
    identity,
)

from hexbytes import HexBytes

import rlp

from eth_account.datastructures import SignedTransaction

from eth_account._utils.signing import sign_transaction_hash

from eth_account._utils.legacy_transactions import chain_id_to_v

from eth_utils.curried import (
    hexstr_if_str,
    to_bytes,
    keccak,
    apply_formatters_to_dict,
    to_int,
    apply_formatters_to_sequence,
    apply_formatter_to_array,
)

from .constants import PRECISION, MAX_DECIMAL

from .signing import sanitize_transaction

from .staking_structures import (
    FORMATTERS,
    Directive,
    CreateValidator,
    EditValidator,
    DelegateOrUndelegate,
    CollectRewards,
)

from .util import convert_one_to_hex


# https://github.com/harmony-one/sdk/blob/99a827782fabcd5f91f025af0d8de228956d42b4/packages/harmony-staking/src/stakingTransaction.ts#L335
def _convert_staking_percentage_to_number(
    value,
):
    """Convert from staking percentage to integer For example, 0.1 becomes
    1000000000000000000. Since Python floats are problematic with precision,
    this function is used as a workaround.

    Parameters
    ---------
    value: :obj:`str` or :obj:`Decimal`
        the value to convert

    Returns
    -------
    int, converted as above

    Raises
    ------
    AssertionError, if data types are not as expected
    ValueError, if the input type is not supported
    """
    assert isinstance(value, (str, Decimal)), "Only strings or decimals are supported"
    if isinstance(value, Decimal):
        value = str(value)
    value1 = value
    if value[0] == "-":
        raise ValueError("Negative numbers are not accepted")
    if value[0] == "+":
        value1 = value[1:]
    if len(value1) == 0:
        raise ValueError("StakingDecimal string is empty")
    spaced = value1.split(" ")
    if len(spaced) > 1:
        raise ValueError("Bad decimal string")
    splitted = value1.split(".")
    combined_str = splitted[0]
    if len(splitted) == 2:
        length = len(splitted[1])
        if length == 0 or len(combined_str) == 0:
            raise ValueError("Bad StakingDecimal length")
        if splitted[1][0] == "-":
            raise ValueError("Bad StakingDecimal string")
        combined_str += splitted[1]
    elif len(splitted) > 2:
        raise ValueError("Too many periods to be a StakingDecimal string")
    if length > PRECISION:
        raise ValueError(
            "Too much precision, must be less than {PRECISION}"
        )
    zeroes_to_add = PRECISION - length
    combined_str += (
        "0" * zeroes_to_add
    )  # This will not have any periods, so it is effectively a large integer
    val = int(combined_str)
    assert val <= MAX_DECIMAL, "Staking percentage is too large"
    return val


def _get_account_and_transaction(transaction_dict, private_key):
    """Create account from private key and sanitize the transaction
    Sanitization involves removal of 'from' key And conversion of chainId key
    from str to int (if present)

    Parameters
    ----------
    transaction_dict: :obj:`dict`
        See sign_staking_transaction
    private_key: obj:`str`
        Private key for the account

    Returns
    -------
    a tuple containing account :obj:`eth_account.Account`
        and sanitize_transaction :obj:`dict`

    Raises
    ------
    AssertionError, if chainId is not present in util.chain_id_to_int
    TypeError, if the value of 'from' key is not the same as account address
    """
    account, sanitized_transaction = sanitize_transaction(
        transaction_dict, private_key
    )  # remove from, convert chain id (if present) to integer
    sanitized_transaction["directive"] = sanitized_transaction[
        "directive"
    ].value  # convert to value, like in TypeScript
    return account, sanitized_transaction

# pylint: disable=too-many-locals,protected-access,invalid-name
def _sign_transaction_generic(account, sanitized_transaction, parent_serializer):
    """Sign a generic staking transaction, given the serializer base class and
    account.

    Paramters
    ---------
    account: :obj:`eth_account.Account`, the account to use for signing
    sanitized_transaction: :obj:`dict`, The sanitized transaction (chainId checks and no from key)
    parent_serializer: :obj: The serializer class from staking_structures

    Returns
    -------
    SignedTransaction object, which can be posted to the chain by using
        blockchain.send_raw_transaction

    Raises
    ------
    Assertion / KeyError, if certain keys are missing from the dict
    rlp.exceptions.ObjectSerializationError, if data types are not as expected
    """
    # obtain the serializers
    if sanitized_transaction.get("chainId", 0) == 0:
        unsigned_serializer, signed_serializer = (
            parent_serializer.Unsigned(),
            parent_serializer.Signed(),
        )  # unsigned, signed
    else:
        unsigned_serializer, signed_serializer = (
            parent_serializer.SignedChainId(),
            parent_serializer.SignedChainId(),
        )  # since chain_id_to_v adds v/r/s, unsigned is not used here
    # fill the transaction
    # https://github.com/ethereum/eth-account/blob/00e7b10005c5fa7090086fcef37a76296c524e17/eth_account/_utils/transactions.py#L39
    filled_transaction = pipe(
        sanitized_transaction,
        dict,
        partial(merge, {"chainId": None}),
        chain_id_to_v,  # will move chain id to v and add v/r/s
        apply_formatters_to_dict(FORMATTERS),
    )
    # get the unsigned transaction
    for field, _ in unsigned_serializer._meta.fields:
        assert field in filled_transaction, f"Could not find {field} in transaction"
    unsigned_transaction = unsigned_serializer.from_dict(
        {f: filled_transaction[f] for f, _ in unsigned_serializer._meta.fields}
    )  # drop extras silently
    # sign the unsigned transaction
    if "v" in unsigned_transaction.as_dict():
        chain_id = unsigned_transaction.v
    else:
        chain_id = None
    transaction_hash = unsigned_transaction.hash()
    (v, r, s) = sign_transaction_hash(account._key_obj, transaction_hash, chain_id)
    chain_naive_transaction = dissoc(
        unsigned_transaction.as_dict(), "v", "r", "s"
    )  # remove extra v/r/s added by chain_id_to_v
    # serialize it
    # https://github.com/harmony-one/sdk/blob/99a827782fabcd5f91f025af0d8de228956d42b4/packages/harmony-staking/src/stakingTransaction.ts#L207
    signed_transaction = signed_serializer(
        v=v
        + (
            8 if chain_id is None else 0
        ),
        r=r,
        s=s,  # in the below statement, remove everything not expected by signed_serializer
        **{
            f: chain_naive_transaction[f]
            for f, _ in signed_serializer._meta.fields
            if f not in "vrs"
        },
    )
    # encode it
    encoded_transaction = rlp.encode(signed_transaction)
    # hash it
    signed_transaction_hash = keccak(encoded_transaction)
    # return is
    return SignedTransaction(
        rawTransaction=HexBytes(encoded_transaction),
        hash=HexBytes(signed_transaction_hash),
        r=r,
        s=s,
        v=v,
    )


def _sign_delegate_or_undelegate(transaction_dict, private_key):
    """Sign a delegate or undelegate transaction See sign_staking_transaction
    for details."""
    # preliminary steps
    if transaction_dict["directive"] not in [Directive.Delegate, Directive.Undelegate]:
        raise TypeError(
            "Only Delegate or Undelegate are supported by _sign_delegate_or_undelegate"
        )
    # first common step
    account, sanitized_transaction = _get_account_and_transaction(
        transaction_dict, private_key
    )
    # encode the stakeMsg
    sanitized_transaction["stakeMsg"] = apply_formatters_to_sequence(
        [hexstr_if_str(to_bytes), hexstr_if_str(to_bytes), hexstr_if_str(to_int)],
        [
            convert_one_to_hex(sanitized_transaction.pop("delegatorAddress")),
            convert_one_to_hex(sanitized_transaction.pop("validatorAddress")),
            sanitized_transaction.pop("amount"),
        ],
    )
    return _sign_transaction_generic(
        account, sanitized_transaction, DelegateOrUndelegate
    )


def _sign_collect_rewards(transaction_dict, private_key):
    """Sign a collect rewards transaction See sign_staking_transaction for
    details."""
    # preliminary steps
    if transaction_dict["directive"] != Directive.CollectRewards:
        raise TypeError("Only CollectRewards is supported by _sign_collect_rewards")
    # first common step
    account, sanitized_transaction = _get_account_and_transaction(
        transaction_dict, private_key
    )
    # encode the stakeMsg
    sanitized_transaction["stakeMsg"] = [
        hexstr_if_str(to_bytes)(
            convert_one_to_hex(sanitized_transaction.pop("delegatorAddress"))
        )
    ]
    return _sign_transaction_generic(account, sanitized_transaction, CollectRewards)


def _sign_create_validator(transaction_dict, private_key):
    """Sign a create validator transaction See sign_staking_transaction for
    details."""
    # preliminary steps
    if transaction_dict["directive"] != Directive.CreateValidator:
        raise TypeError(
            "Only CreateValidator is supported by _sign_create_or_edit_validator"
        )
    # first common step
    account, sanitized_transaction = _get_account_and_transaction(
        transaction_dict, private_key
    )
    # encode the stakeMsg
    description = [
        sanitized_transaction.pop("name"),
        sanitized_transaction.pop("identity"),
        sanitized_transaction.pop("website"),
        sanitized_transaction.pop("security-contact"),
        sanitized_transaction.pop("details"),
    ]
    commission = apply_formatter_to_array(
        hexstr_if_str(to_int),  # formatter
        [
            _convert_staking_percentage_to_number(sanitized_transaction.pop("rate")),
            _convert_staking_percentage_to_number(
                sanitized_transaction.pop("max-rate")
            ),
            _convert_staking_percentage_to_number(
                sanitized_transaction.pop("max-change-rate")
            ),
        ],
    )
    commission = [[element] for element in commission]
    bls_keys = apply_formatter_to_array(
        hexstr_if_str(to_bytes),  # formatter
        sanitized_transaction.pop("bls-public-keys"),
    )
    bls_key_sigs = apply_formatter_to_array(
        hexstr_if_str(to_bytes), sanitized_transaction.pop("bls-key-sigs")  # formatter
    )
    sanitized_transaction["stakeMsg"] = apply_formatters_to_sequence(
        [
            hexstr_if_str(to_bytes),  # address
            identity,  # description
            identity,  # commission rates
            hexstr_if_str(
                to_int
            ),  # min self delegation (in ONE), decimals are silently dropped
            hexstr_if_str(
                to_int
            ),  # max total delegation (in ONE), decimals are silently dropped
            identity,  # bls public keys
            identity,  # bls key sigs
            hexstr_if_str(
                to_int
            ),  # amount (the Hexlify in the SDK drops the decimals, which is what we will do too)
        ],
        [
            convert_one_to_hex(sanitized_transaction.pop("validatorAddress")),
            description,
            commission,
            math.floor(
                sanitized_transaction.pop("min-self-delegation")
            ),  # Decimal floors it correctly
            math.floor(sanitized_transaction.pop("max-total-delegation")),
            bls_keys,
            bls_key_sigs,
            math.floor(sanitized_transaction.pop("amount")),
        ],
    )
    return _sign_transaction_generic(account, sanitized_transaction, CreateValidator)


def _sign_edit_validator(transaction_dict, private_key):
    """Sign an edit validator transaction See sign_staking_transaction for
    details."""
    # preliminary steps
    if transaction_dict["directive"] != Directive.EditValidator:
        raise TypeError(
            "Only EditValidator is supported by _sign_create_or_edit_validator"
        )
    # first common step
    account, sanitized_transaction = _get_account_and_transaction(
        transaction_dict, private_key
    )
    # encode the stakeMsg
    description = [
        sanitized_transaction.pop("name"),
        sanitized_transaction.pop("identity"),
        sanitized_transaction.pop("website"),
        sanitized_transaction.pop("security-contact"),
        sanitized_transaction.pop("details"),
    ]
    sanitized_transaction["stakeMsg"] = apply_formatters_to_sequence(
        [
            hexstr_if_str(to_bytes),  # address
            identity,  # description
            identity,  # new rate (it's in a list so can't do hexstr_if_str)
            hexstr_if_str(
                to_int
            ),  # min self delegation (in ONE), decimals are silently dropped
            hexstr_if_str(
                to_int
            ),  # max total delegation (in ONE), decimals are silently dropped
            hexstr_if_str(to_bytes),  # key to remove
            hexstr_if_str(to_bytes),  # key to add
            hexstr_if_str(to_bytes),  # key to add sig
        ],
        [
            convert_one_to_hex(sanitized_transaction.pop("validatorAddress")),
            description,
            [_convert_staking_percentage_to_number(sanitized_transaction.pop("rate"))],
            math.floor(
                sanitized_transaction.pop("min-self-delegation")
            ),  # Decimal floors it correctly
            math.floor(sanitized_transaction.pop("max-total-delegation")),
            sanitized_transaction.pop("bls-key-to-remove"),
            sanitized_transaction.pop("bls-key-to-add"),
            sanitized_transaction.pop("bls-key-to-add-sig"),
        ],
    )
    return _sign_transaction_generic(account, sanitized_transaction, EditValidator)


def sign_staking_transaction(transaction_dict, private_key):
    """Sign a supplied transaction_dict with the private_key.

    Parameters
    ----------
    transaction_dict: :obj:`dict`, a dictionary with the following keys
        directive :obj:`staking_structures.Directive`, type of transaction
        nonce: :obj:`int`, nonce of transaction
        gasPrice: :obj:`int`, gas price for the transaction
        gasLimit: :obj:`int`, gas limit for the transaction
        chainId: :obj:`int`, chain id for the transaction, optional
            see util.chain_id_to_int for options
        The following keys depend on the directive:
        CollectRewards:
            delegatorAddress: :obj:`str`, Address of the delegator
        Delegate/Undelegate:
            delegatorAddress: :obj:`str`, Address of the delegator
            validatorAddress: :obj:`str`, Address of the validator
            amount: :obj:`int`, Amount to (un)delegate in ATTO
        CreateValidator:
            validatorAddress: :obj:`str`, Address of the validator
            name: ;obj:`str`, Name of the validator
            identity: :obj:`str`, Identity of the validator, must be unique
            website: :obj:`str`, Website of the validator
            security-contact: :obj:`str`, Security contact
            details: :obj:`str` Validator details
            rate: :obj:'Decimal' or :obj:`str` Staking commission rate
            max-rate: :obj:'Decimal' or :obj:`str` Maximum staking commission rate
            max-change-rate: :obj:'Decimal' or :obj:`str` Maximum change in
                    staking commission rate per epoch
            bls-public-keys: :obj:`list` List of strings of BLS public keys
            min-self-delegation: :obj:`int` or :obj:`Decimal` Validator min
                self delegation in ATTO
            max-total-delegation: :obj:`int` or :obj:`Decimal` Validator max
                total delegation in ATTO
        EditValidator:
            validatorAddress: :obj:`str`, Address of the validator
            name: ;obj:`str`, Name of the validator
            identity: :obj:`str`, Identity of the validator, must be unique
            website: :obj:`str`, Website of the validator
            security-contact: :obj:`str`, Security contact
            details: :obj:`str` Validator details
            rate: :obj:'Decimal' or :obj:`str` Staking commission rate
            min-self-delegation: :obj:`int` or :obj:`Decimal` Validator min
                self delegation in ATTO
            max-total-delegation: :obj:`int` or :obj:`Decimal` Validator max
                total delegation in ATTO
            bls-key-to-remove: :obj:`str` BLS Public key to remove
            bls-key-to-add: :obj:`str` BLS Public key to add
    private_key: :obj:`str`, the private key to sign the transaction with

    Raises
    ------
    AssertionError, if inputs are not as expected
    KeyError, if inputs are missing
    ValueError, if specifically staking rates are malformed
    rlp.exceptions.ObjectSerializationError, if input data types are not as expected

    Returns
    -------
    SignedTransaction object, the hash of which can be used to send the transaction
        using transaction.send_raw_transaction

    API Reference
    -------------
    https://github.com/harmony-one/sdk/blob/99a827782fabcd5f91f025af0d8de228956d42b4/packages/harmony-staking/src/stakingTransaction.ts
    """
    assert isinstance(
        transaction_dict, dict
    ), "Only dictionaries are supported"  # OrderedDict is a subclass
    # chain_id missing => results in rlp decoding error for GasLimit
    assert "chainId" in transaction_dict, "chainId missing"
    assert "directive" in transaction_dict, "Staking transaction type not specified"
    assert isinstance(
        transaction_dict["directive"], Directive
    ), "Unknown staking transaction type"
    if transaction_dict["directive"] == Directive.CollectRewards:
        return _sign_collect_rewards(transaction_dict, private_key)
    if transaction_dict["directive"] == Directive.Delegate:
        return _sign_delegate_or_undelegate(transaction_dict, private_key)
    if transaction_dict["directive"] == Directive.Undelegate:
        return _sign_delegate_or_undelegate(transaction_dict, private_key)
    if transaction_dict["directive"] == Directive.CreateValidator:
        return _sign_create_validator(transaction_dict, private_key)
    if transaction_dict["directive"] == Directive.EditValidator:
        return _sign_edit_validator(transaction_dict, private_key)
    raise ValueError('Unknown staking transaction type')
