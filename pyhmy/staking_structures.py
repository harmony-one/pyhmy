from enum import Enum, auto

from rlp.sedes import big_endian_int, Binary, CountableList, List, Text

from eth_rlp import HashableRLP

from eth_utils.curried import (
    to_int,
    hexstr_if_str,
)


class StakingSettings:
    PRECISION = 18
    MAX_DECIMAL = 1000000000000000000


class Directive(
    Enum
):  # https://github.com/harmony-one/sdk/blob/99a827782fabcd5f91f025af0d8de228956d42b4/packages/harmony-staking/src/stakingTransaction.ts#L120
    def _generate_next_value_(name, start, count, last_values):
        return count

    CreateValidator = auto()
    EditValidator = auto()
    Delegate = auto()
    Undelegate = auto()
    CollectRewards = auto()


FORMATTERS = {
    "directive": hexstr_if_str(
        to_int
    ),  # delegatorAddress is already formatted before the call
    "nonce": hexstr_if_str(to_int),
    "gasPrice": hexstr_if_str(to_int),
    "gasLimit": hexstr_if_str(to_int),
    "chainId": hexstr_if_str(to_int),
}


class CollectRewards:
    @staticmethod
    def UnsignedChainId():
        class UnsignedChainId(HashableRLP):
            fields = (
                ("directive", big_endian_int),
                ("stakeMsg", CountableList(Binary.fixed_length(20, allow_empty=True))),
                ("nonce", big_endian_int),
                ("gasPrice", big_endian_int),
                ("gasLimit", big_endian_int),
                ("chainId", big_endian_int),
            )

        return UnsignedChainId

    @staticmethod
    def SignedChainId():
        class SignedChainId(HashableRLP):
            fields = CollectRewards.UnsignedChainId()._meta.fields[
                :-1
            ] + (  # drop chainId
                ("v", big_endian_int),
                ("r", big_endian_int),
                ("s", big_endian_int),
            )

        return SignedChainId

    @staticmethod
    def Unsigned():
        class Unsigned(HashableRLP):
            fields = CollectRewards.UnsignedChainId()._meta.fields[:-1]  # drop chainId

        return Unsigned

    @staticmethod
    def Signed():
        class Signed(HashableRLP):
            fields = CollectRewards.Unsigned()._meta.fields[
                :-3
            ] + (  # drop last 3 for raw.pop()
                ("v", big_endian_int),
                ("r", big_endian_int),
                ("s", big_endian_int),
            )

        return Signed


class DelegateOrUndelegate:
    @staticmethod
    def UnsignedChainId():
        class UnsignedChainId(HashableRLP):
            fields = (
                ("directive", big_endian_int),
                (
                    "stakeMsg",
                    List(
                        [
                            Binary.fixed_length(20, allow_empty=True),
                            Binary.fixed_length(20, allow_empty=True),
                            big_endian_int,
                        ],
                        True,
                    ),
                ),
                ("nonce", big_endian_int),
                ("gasPrice", big_endian_int),
                ("gasLimit", big_endian_int),
                ("chainId", big_endian_int),
            )

        return UnsignedChainId

    @staticmethod
    def SignedChainId():
        class SignedChainId(HashableRLP):
            fields = DelegateOrUndelegate.UnsignedChainId()._meta.fields[
                :-1
            ] + (  # drop chainId
                ("v", big_endian_int),
                ("r", big_endian_int),
                ("s", big_endian_int),
            )

        return SignedChainId

    @staticmethod
    def Unsigned():
        class Unsigned(HashableRLP):
            fields = DelegateOrUndelegate.UnsignedChainId()._meta.fields[
                :-1
            ]  # drop chainId

        return Unsigned

    @staticmethod
    def Signed():
        class Signed(HashableRLP):
            fields = DelegateOrUndelegate.Unsigned()._meta.fields[
                :-3
            ] + (  # drop last 3 for raw.pop()
                ("v", big_endian_int),
                ("r", big_endian_int),
                ("s", big_endian_int),
            )

        return Signed


class CreateValidator:
    @staticmethod
    def UnsignedChainId():
        class UnsignedChainId(HashableRLP):
            fields = (
                ("directive", big_endian_int),
                (
                    "stakeMsg",
                    List(
                        [  # list with the following members
                            Binary.fixed_length(
                                20, allow_empty=True
                            ),  # validatorAddress
                            List(
                                [Text()] * 5, True
                            ),  # description is Text of 5 elements
                            List(
                                [List([big_endian_int], True)] * 3, True
                            ),  # commission rate is made up of 3 integers in an array [ [int1], [int2], [int3] ]
                            big_endian_int,  # min self delegation
                            big_endian_int,  # max total delegation
                            CountableList(
                                Binary.fixed_length(48, allow_empty=True)
                            ),  # bls-public-keys array of unspecified length, each key of 48
                            CountableList(
                                Binary.fixed_length(96, allow_empty=True)
                            ),  # bls-key-sigs array of unspecified length, each sig of 96
                            big_endian_int,  # amount
                        ],
                        True,
                    ),
                ),  # strictly these number of elements
                ("nonce", big_endian_int),
                ("gasPrice", big_endian_int),
                ("gasLimit", big_endian_int),
                ("chainId", big_endian_int),
            )

        return UnsignedChainId

    @staticmethod
    def SignedChainId():
        class SignedChainId(HashableRLP):
            fields = CreateValidator.UnsignedChainId()._meta.fields[
                :-1
            ] + (  # drop chainId
                ("v", big_endian_int),
                ("r", big_endian_int),
                ("s", big_endian_int),
            )

        return SignedChainId

    @staticmethod
    def Unsigned():
        class Unsigned(HashableRLP):
            fields = CreateValidator.UnsignedChainId()._meta.fields[:-1]  # drop chainId

        return Unsigned

    @staticmethod
    def Signed():
        class Signed(HashableRLP):
            fields = CreateValidator.Unsigned()._meta.fields[
                :-3
            ] + (  # drop last 3 for raw.pop()
                ("v", big_endian_int),
                ("r", big_endian_int),
                ("s", big_endian_int),
            )

        return Signed


class EditValidator:
    @staticmethod
    def UnsignedChainId():
        class UnsignedChainId(HashableRLP):
            fields = (
                ("directive", big_endian_int),
                (
                    "stakeMsg",
                    List(
                        [  # list with the following members
                            Binary.fixed_length(
                                20, allow_empty=True
                            ),  # validatorAddress
                            List(
                                [Text()] * 5, True
                            ),  # description is Text of 5 elements
                            List([big_endian_int], True),  # new rate is in a list
                            big_endian_int,  # min self delegation
                            big_endian_int,  # max total delegation
                            Binary.fixed_length(
                                48, allow_empty=True
                            ),  # slot key to remove
                            Binary.fixed_length(
                                48, allow_empty=True
                            ),  # slot key to add
                        ],
                        True,
                    ),
                ),  # strictly these number of elements
                ("nonce", big_endian_int),
                ("gasPrice", big_endian_int),
                ("gasLimit", big_endian_int),
                ("chainId", big_endian_int),
            )

        return UnsignedChainId

    @staticmethod
    def SignedChainId():
        class SignedChainId(HashableRLP):
            fields = EditValidator.UnsignedChainId()._meta.fields[
                :-1
            ] + (  # drop chainId
                ("v", big_endian_int),
                ("r", big_endian_int),
                ("s", big_endian_int),
            )

        return SignedChainId

    @staticmethod
    def Unsigned():
        class Unsigned(HashableRLP):
            fields = EditValidator.UnsignedChainId()._meta.fields[:-1]  # drop chainId

        return Unsigned

    @staticmethod
    def Signed():
        class Signed(HashableRLP):
            fields = EditValidator.Unsigned()._meta.fields[
                :-3
            ] + (  # drop last 3 for raw.pop()
                ("v", big_endian_int),
                ("r", big_endian_int),
                ("s", big_endian_int),
            )

        return Signed
