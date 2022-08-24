"""
Sign Harmony or Ethereum transactions
Harmony staking transaction signing is not covered by this module
"""

# pylint: disable=protected-access, no-member

from functools import partial
from toolz import dissoc, pipe, merge

import rlp

from eth_utils.curried import keccak, to_int, hexstr_if_str, apply_formatters_to_dict

from rlp.sedes import big_endian_int, Binary, binary

from eth_rlp import HashableRLP

from hexbytes import HexBytes

from eth_account import Account
from eth_account.datastructures import SignedTransaction
from eth_account._utils.legacy_transactions import (
    Transaction as SignedEthereumTxData,
    UnsignedTransaction as UnsignedEthereumTxData,
    LEGACY_TRANSACTION_FORMATTERS as ETHEREUM_FORMATTERS,
    TRANSACTION_DEFAULTS,
    chain_id_to_v,
)
from eth_account._utils.signing import sign_transaction_hash

from .util import chain_id_to_int, convert_one_to_hex

HARMONY_FORMATTERS = dict(
    ETHEREUM_FORMATTERS,
    shardID=hexstr_if_str(to_int),  # additional fields for Harmony transaction
    toShardID=hexstr_if_str(to_int),  # which may be cross shard
)


class UnsignedHarmonyTxData( HashableRLP ):
    """
    Unsigned Harmony transaction data
    Includes `shardID` and `toShardID`
    as the difference against Eth
    """
    fields = (
        ( "nonce",
          big_endian_int ),
        ( "gasPrice",
          big_endian_int ),
        ( "gas",
          big_endian_int ),
        ( "shardID",
          big_endian_int ),
        ( "toShardID",
          big_endian_int ),
        ( "to",
          Binary.fixed_length( 20,
                               allow_empty = True ) ),
        ( "value",
          big_endian_int ),
        ( "data",
          binary ),
    )


class SignedHarmonyTxData( HashableRLP ):
    """
    Signed Harmony transaction data
    Includes `shardID` and `toShardID`
    as the difference against Eth
    """
    fields = UnsignedHarmonyTxData._meta.fields + (
        ("v", big_endian_int),  # Recovery value + 27
        ("r", big_endian_int),  # First 32 bytes
        ("s", big_endian_int),  # Next  32 bytes
    )


# https://github.com/ethereum/eth-account/blob/00e7b10005c5fa7090086fcef37a76296c524e17/eth_account/_utils/transactions.py#L55
def encode_transaction( unsigned_transaction, vrs ):
    """serialize and encode an unsigned transaction with v,r,s."""
    ( v, r, s ) = vrs  # pylint: disable=invalid-name
    chain_naive_transaction = dissoc(
        unsigned_transaction.as_dict(),
        "v",
        "r",
        "s"
    )
    if isinstance(
        unsigned_transaction,
        ( UnsignedHarmonyTxData,
          SignedHarmonyTxData )
    ):
        serializer = SignedHarmonyTxData
    else:
        serializer = SignedEthereumTxData
    signed_transaction = serializer(
        v = v,
        r = r,
        s = s,
        **chain_naive_transaction
    )
    return rlp.encode( signed_transaction )


def serialize_transaction( filled_transaction ):
    """serialize a signed/unsigned transaction."""
    if "v" in filled_transaction:
        if "shardID" in filled_transaction:
            serializer = SignedHarmonyTxData
        else:
            serializer = SignedEthereumTxData
    else:
        if "shardID" in filled_transaction:
            serializer = UnsignedHarmonyTxData
        else:
            serializer = UnsignedEthereumTxData
    for field, _ in serializer._meta.fields:
        assert field in filled_transaction, f"Could not find {field} in transaction"
    return serializer.from_dict(
        {
            field: filled_transaction[ field ]
            for field,
            _ in serializer._meta.fields
        }
    )


# https://github.com/ethereum/eth-account/blob/00e7b10005c5fa7090086fcef37a76296c524e17/eth_account/account.py#L650
def sanitize_transaction( transaction_dict, private_key ):
    """remove the originating address from the dict and convert chainId to
    int."""
    account = Account.from_key( # pylint: disable=no-value-for-parameter
        private_key
    )
    sanitized_transaction = transaction_dict.copy(
    )  # do not alter the original dictionary
    if "from" in sanitized_transaction:
        sanitized_transaction[ "from" ] = convert_one_to_hex(
            transaction_dict[ "from" ]
        )
        if sanitized_transaction[ "from" ] == account.address:
            sanitized_transaction = dissoc( sanitized_transaction, "from" )
        else:
            raise TypeError(
                "from field must match key's {account.address}, "
                "but it was {sanitized_transaction['from']}"
            )
    if "chainId" in sanitized_transaction:
        sanitized_transaction[ "chainId" ] = chain_id_to_int(
            sanitized_transaction[ "chainId" ]
        )
    return account, sanitized_transaction


def sign_transaction( transaction_dict, private_key ) -> SignedTransaction:
    """Sign a (non-staking) transaction dictionary with the specified private
    key.

    Parameters
    ----------
    transaction_dict: :obj:`dict` with the following keys
        nonce: :obj:`int` Transaction nonce
        gasPrice: :obj:`int` Transaction gas price in Atto
        gas: :obj:`int` Gas limit in Atto
        to: :obj:`str` Destination address
        value: :obj:`int` Amount to be transferred in Atto
        data: :obj:`str` Transaction data, used for smart contracts
        from: :obj:`str` From address, optional (if passed, must match the
                    public key address generated from private_key)
        chainId: :obj:`int` One of util.chainIds.keys(), optional
            If you want to replay your transaction across networks, do not pass it
        shardID: :obj:`int` Originating shard ID, optional (needed for cx shard transaction)
        toShardID: :obj:`int` Destination shard ID, optional (needed for cx shard transaction)
        r:  :obj:`int` First 32 bytes of the signature, optional
        s:  :obj:`int` Next  32 bytes of the signature, optional
        v:  :obj:`int` Recovery value, optional
    private_key: :obj:`str` The private key

    Returns
    -------
    A SignedTransaction object, which is a named tuple
        rawTransaction: :obj:`str` Hex bytes of the raw transaction
        hash: :obj:`str` Hex bytes of the transaction hash
        r:  :obj:`int` First 32 bytes of the signature
        s:  :obj:`int` Next  32 bytes of the signature
        v:  :obj:`int` Recovery value

    Raises
    ------
    TypeError, if the from address specified is not the same
        one as derived from the the private key
    AssertionError, if the fields for the transaction are missing,
        or if the chainId supplied is not a string,
        or if the chainId is not a key in util.py

    API Reference
    -------------
    https://readthedocs.org/projects/eth-account/downloads/pdf/stable/
    """
    account, sanitized_transaction = sanitize_transaction(transaction_dict, private_key)
    if "to" in sanitized_transaction and sanitized_transaction[ "to"
                                                               ] is not None:
        sanitized_transaction[ "to" ] = convert_one_to_hex(
            sanitized_transaction[ "to" ]
        )
    # https://github.com/ethereum/eth-account/blob/00e7b10005c5fa7090086fcef37a76296c524e17/eth_account/_utils/transactions.py#L39
    filled_transaction = pipe(
        sanitized_transaction,
        dict,
        partial( merge,
                 TRANSACTION_DEFAULTS ),
        chain_id_to_v,
        apply_formatters_to_dict( HARMONY_FORMATTERS ),
    )
    unsigned_transaction = serialize_transaction( filled_transaction )
    transaction_hash = unsigned_transaction.hash()

    # https://github.com/ethereum/eth-account/blob/00e7b10005c5fa7090086fcef37a76296c524e17/eth_account/_utils/signing.py#L26
    if isinstance(
        unsigned_transaction,
        ( UnsignedEthereumTxData,
          UnsignedHarmonyTxData )
    ):
        chain_id = None
    else:
        chain_id = unsigned_transaction.v
    ( v, # pylint: disable=invalid-name
      r, # pylint: disable=invalid-name
      s ) = sign_transaction_hash( # pylint: disable=invalid-name
          account._key_obj,
          transaction_hash,
          chain_id
      )
    encoded_transaction = encode_transaction(
        unsigned_transaction,
        vrs = ( v,
                r,
                s )
    )
    signed_transaction_hash = keccak( encoded_transaction )
    return SignedTransaction(
        rawTransaction = HexBytes( encoded_transaction ),
        hash = HexBytes( signed_transaction_hash ),
        r = r,
        s = s,
        v = v,
    )
