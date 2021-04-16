import rlp
from eth_typing import HexStr
from eth_utils.curried import keccak, to_int, hexstr_if_str, apply_formatters_to_dict
from rlp.sedes import Binary, big_endian_int, binary
from eth_account import Account
from eth_rlp import HashableRLP
from hexbytes import HexBytes
from eth_account._utils.signing import sign_transaction_hash
from eth_account._utils.transactions import (
    Transaction as EthTxData,
    UnsignedTransaction as UnsignedEthTxData,
    TRANSACTION_FORMATTERS as ETHTX_FORMATTERS,
    TRANSACTION_DEFAULTS,
    chain_id_to_v,
    encode_transaction
)
from cytoolz import dissoc, pipe, merge, partial
from eth_account.datastructures import SignedTransaction


HMYTX_FORMATTERS = dict(
    ETHTX_FORMATTERS,
    shardID=hexstr_if_str(to_int),
    toShardID=hexstr_if_str(to_int),
)


class HmyTxData(HashableRLP):
    fields = [
        ("nonce", big_endian_int),
        ("gasPrice", big_endian_int),
        ("gas", big_endian_int),
        ("shardID", big_endian_int),
        ("toShardID", big_endian_int),
        ("to", Binary.fixed_length(20, allow_empty=True)),
        ("value", big_endian_int),
        ("data", binary),
        ("v", big_endian_int),
        ("r", big_endian_int),
        ("s", big_endian_int),
    ]


class UnsignedHmyTxData(HashableRLP):
    fields = []
    for field, sedes in HmyTxData._meta.fields:
        if field not in "vrs":
            fields.append((field, sedes))


def encode_transaction(unsigned_transaction, vrs):
    (v, r, s) = vrs
    chain_naive_transaction = dissoc(
        unsigned_transaction.as_dict(), 'v', 'r', 's')
    if isinstance(
            unsigned_transaction,
            UnsignedHmyTxData) or isinstance(
            unsigned_transaction,
            HmyTxData):
        serializer = HmyTxData
    else:
        serializer = EthTxData
    signed_transaction = serializer(v=v, r=r, s=s, **chain_naive_transaction)
    return rlp.encode(signed_transaction)


class HmyAccount(object):

    def sign_transaction(self, transaction_dict, private_key):
        account = Account.from_key(private_key)
        # allow from field, *only* if it matches the private key
        if 'from' in transaction_dict:
            if transaction_dict['from'] == account.address:
                sanitized_transaction = dissoc(transaction_dict, 'from')
            else:
                raise TypeError(
                    "from field must match key's %s, but it was %s" %
                    (account.address, transaction_dict['from'], ))
        else:
            sanitized_transaction = transaction_dict

        filled_transaction = pipe(
            transaction_dict,
            dict,
            partial(merge, TRANSACTION_DEFAULTS),
            chain_id_to_v,
            apply_formatters_to_dict(HMYTX_FORMATTERS)
        )

        if 'v' in filled_transaction:
            if 'shardID' in transaction_dict:
                serializer = HmyTxData
            else:
                serializer = EthTxData
        else:
            if 'shardID' in transaction_dict:
                serializer = UnsignedHmyTxData
            else:
                serializer = UnsignedEthTxData

        unsigned_transaction = serializer.from_dict(
            {f: filled_transaction[f] for f, s in serializer._meta.fields})
        transaction_hash = unsigned_transaction.hash()

        if 'v' not in filled_transaction:
            chain_id = None
        else:
            chain_id = unsigned_transaction.v

        (v, r, s) = sign_transaction_hash(
            account._key_obj, transaction_hash, chain_id)

        encoded_transaction = encode_transaction(
            unsigned_transaction, vrs=(v, r, s))

        signed_txhash = HexBytes(keccak(encoded_transaction))

        return SignedTransaction(
            rawTransaction=HexBytes(encoded_transaction),
            hash=HexBytes(signed_txhash),
            r=r,
            s=s,
            v=v,
        )
