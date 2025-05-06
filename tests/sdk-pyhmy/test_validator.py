import pytest
from decimal import Decimal

from pyhmy import validator

from pyhmy.numbers import convert_one_to_atto

from pyhmy.exceptions import InvalidValidatorError

test_epoch_number = 0
genesis_block_number = 0
test_block_number = 1
test_validator_object = None
test_validator_loaded = False


def test_instantiate_validator( setup_blockchain ):
    global test_validator_object
    test_validator_object = validator.Validator(
        "one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9"
    )
    assert isinstance( test_validator_object, validator.Validator )


def test_load_validator( setup_blockchain ):
    if not test_validator_object:
        pytest.fail( "Validator not instantiated yet" )
    info = {
        "name": "Alice",
        "identity": "alice",
        "website": "alice.harmony.one",
        "details": "Don't mess with me!!!",
        "security-contact": "Bob",
        "min-self-delegation": convert_one_to_atto( 10000 ),
        "amount": convert_one_to_atto( 10001 ),
        "max-rate": "0.9",
        "max-change-rate": "0.05",
        "rate": "0.01",
        "bls-public-keys": [
            "0x30b2c38b1316da91e068ac3bd8751c0901ef6c02a1d58bc712104918302c6ed03d5894671d0c816dad2b4d303320f202"
        ],
        "bls-key-sigs": [
            "0x68f800b6adf657b674903e04708060912b893b7c7b500788808247550ab3e186e56a44ebf3ca488f8ed1a42f6cef3a04bd5d2b2b7eb5a767848d3135b362e668ce6bba42c7b9d5666d8e3a83be707b5708e722c58939fe9b07c170f3b7062414"
        ],
        "max-total-delegation": convert_one_to_atto( 40000 ),
    }
    test_validator_object.load( info )
    global test_validator_loaded
    test_validator_loaded = True


"""
TypeScript signature source (is outdated because the JS SDK has not been updated for SlotKeySigs)
For now I have checked that the below transaction to localnet works
---
const description: Description = new Description('Alice', 'alice', 'alice.harmony.one', 'Bob', "Don't mess with me!!!")
const commissionRates: CommissionRate = new CommissionRate(new Decimal('0.01'), new Decimal('0.9'), new Decimal('0.05'))
const stakeMsg: CreateValidator = new CreateValidator(
        'one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9',
        description,
        commissionRates,
        numberToHex(new Unit('10000').asOne().toWei()),    // minSelfDelegation
        numberToHex(new Unit('40000').asOne().toWei()),    // maxTotalDelegation
        [ '0xb9486167ab9087ab818dc4ce026edb5bf216863364c32e42df2af03c5ced1ad181e7d12f0e6dd5307a73b62247608611' ],
        numberToHex(new Unit('10001').asOne().toWei())    // amount
  )
const stakingTx: StakingTransaction = new StakingTransaction(
  Directive.DirectiveCreateValidator,
  stakeMsg,
  2,    // nonce
  numberToHex(new Unit('1').asOne().toWei()),    // gasPrice
  100,      // gasLimit
  null,     // chainId
);
const signed = stakingTx.rlpSign('4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48')
console.log( 'Signed transaction' )
console.log(signed)
"""


def test_create_validator_sign( setup_blockchain ):
    if not ( test_validator_object or test_validator_loaded ):
        pytest.fail( "Validator not instantiated yet" )
    signed_hash = test_validator_object.sign_create_validator_transaction(
        2,
        int( convert_one_to_atto( 1 ) ),
        100,
        "4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48",
        2,
    ).raw_transaction.to_0x_hex()
    assert (
        signed_hash ==
        "0xf9017580f9012394ebcd16e8c1d8f493ba04e99a56474122d81a9c58f83885416c69636585616c69636591616c6963652e6861726d6f6e792e6f6e6583426f6295446f6e2774206d6573732077697468206d65212121dcc8872386f26fc10000c9880c7d713b49da0000c887b1a2bc2ec500008a021e19e0c9bab24000008a0878678326eac9000000f1b030b2c38b1316da91e068ac3bd8751c0901ef6c02a1d58bc712104918302c6ed03d5894671d0c816dad2b4d303320f202f862b86068f800b6adf657b674903e04708060912b893b7c7b500788808247550ab3e186e56a44ebf3ca488f8ed1a42f6cef3a04bd5d2b2b7eb5a767848d3135b362e668ce6bba42c7b9d5666d8e3a83be707b5708e722c58939fe9b07c170f3b70624148a021e27c1806e59a4000002880de0b6b3a76400006428a0c6c7e62f02331df0afd4699ec514a2fc4548c920d77ad74d98caeec8c924c09aa02b27b999a724b1d341d6bbb0e877611d0047542cb7e380f9a6a272d204b450cd"
    )


"""
Signature matched from TypeScript (is outdated because the JS SDK has not been updated for SlotKeyToAddSig)
For now I have checked that the below transaction to localnet works
---
import {
  CreateValidator,
  EditValidator,
  Delegate,
  Undelegate,
  CollectRewards,
  Directive,
  Description,
  CommissionRate,
  Decimal,
  StakingTransaction,
} from '@harmony-js/staking'
const { numberToHex, Unit } = require('@harmony-js/utils');

const description: Description = new Description('Alice', 'alice', 'alice.harmony.one', 'Bob', "Don't mess with me!!!")
const commissionRates: CommissionRate = new CommissionRate(new Decimal('0.01'), new Decimal('0.9'), new Decimal('0.05'))
const stakeMsg: EditValidator = new EditValidator(
        'one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9',
        description,
        new Decimal('0.06'),
        numberToHex(new Unit('10000').asOne().toWei()),    // minSelfDelegation
        numberToHex(new Unit('40000').asOne().toWei()),    // maxTotalDelegation
        '0xb9486167ab9087ab818dc4ce026edb5bf216863364c32e42df2af03c5ced1ad181e7d12f0e6dd5307a73b62247608611', // remove key
        '0xb9486167ab9087ab818dc4ce026edb5bf216863364c32e42df2af03c5ced1ad181e7d12f0e6dd5307a73b62247608612'  // add key
  )
const stakingTx: StakingTransaction = new StakingTransaction(
  Directive.DirectiveEditValidator,
  stakeMsg,
  2,    // nonce
  numberToHex(new Unit('1').asOne().toWei()),    // gasPrice
  100,  // gasLimit
  2,    // chainId
);
const signed = stakingTx.rlpSign('4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48')
console.log( 'Signed transaction' )
console.log(signed)
"""


def test_edit_validator_sign( setup_blockchain ):
    if not ( test_validator_object or test_validator_loaded ):
        pytest.fail( "Validator not instantiated yet" )
    signed_hash = test_validator_object.sign_edit_validator_transaction(
        2,
        int(convert_one_to_atto(1)),
        100,
        "0.06",
        "0xb9486167ab9087ab818dc4ce026edb5bf216863364c32e42df2af03c5ced1ad181e7d12f0e6dd5307a73b62247608612",  # remove key
        "0xb9486167ab9087ab818dc4ce026edb5bf216863364c32e42df2af03c5ced1ad181e7d12f0e6dd5307a73b62247608611",  # add key
        "0x68f800b6adf657b674903e04708060912b893b7c7b500788808247550ab3e186e56a44ebf3ca488f8ed1a42f6cef3a04bd5d2b2b7eb5a767848d3135b362e668ce6bba42c7b9d5666d8e3a83be707b5708e722c58939fe9b07c170f3b7062414",  # add key sig
        "4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48",
        2,
    ).raw_transaction.to_0x_hex()
    assert (
        signed_hash ==
        "0xf9018401f9013294ebcd16e8c1d8f493ba04e99a56474122d81a9c58f83885416c69636585616c69636591616c6963652e6861726d6f6e792e6f6e6583426f6295446f6e2774206d6573732077697468206d65212121c887d529ae9e8600008a021e19e0c9bab24000008a0878678326eac9000000b0b9486167ab9087ab818dc4ce026edb5bf216863364c32e42df2af03c5ced1ad181e7d12f0e6dd5307a73b62247608612b0b9486167ab9087ab818dc4ce026edb5bf216863364c32e42df2af03c5ced1ad181e7d12f0e6dd5307a73b62247608611b86068f800b6adf657b674903e04708060912b893b7c7b500788808247550ab3e186e56a44ebf3ca488f8ed1a42f6cef3a04bd5d2b2b7eb5a767848d3135b362e668ce6bba42c7b9d5666d8e3a83be707b5708e722c58939fe9b07c170f3b706241402880de0b6b3a76400006427a0ecdae4a29d051f4f83dd54004858fbf0f7820e169b8e1846245835ceb686ee12a04b2336eb5830e30720137b2de539518fd5655467fef140ab31fde881a19f256a"
    )


def test_invalid_validator( setup_blockchain ):
    if not ( test_validator_object or test_validator_loaded ):
        pytest.fail( "Validator not instantiated yet" )
    with pytest.raises( InvalidValidatorError ):
        info = {
            "name": "Alice",
        }
        test_validator_object.load( info )
    with pytest.raises( InvalidValidatorError ):
        test_validator_object.set_name( "a" * 141 )
    with pytest.raises( InvalidValidatorError ):
        test_validator_object.set_identity( "a" * 141 )
    with pytest.raises( InvalidValidatorError ):
        test_validator_object.set_website( "a" * 141 )
    with pytest.raises( InvalidValidatorError ):
        test_validator_object.set_security_contact( "a" * 141 )
    with pytest.raises( InvalidValidatorError ):
        test_validator_object.set_details( "a" * 281 )
    with pytest.raises( InvalidValidatorError ):
        test_validator_object.set_min_self_delegation( 1 )
    with pytest.raises( InvalidValidatorError ):
        test_validator_object.set_max_total_delegation( 1 )
    with pytest.raises( InvalidValidatorError ):
        test_validator_object.set_amount( 1 )
    with pytest.raises( InvalidValidatorError ):
        test_validator_object.set_max_rate( "2.0" )
    with pytest.raises( InvalidValidatorError ):
        test_validator_object.set_max_change_rate( "-2.0" )
    with pytest.raises( InvalidValidatorError ):
        test_validator_object.set_rate( "-2.0" )


def test_validator_getters( setup_blockchain ):
    if not ( test_validator_object or test_validator_loaded ):
        pytest.fail( "Validator not instantiated yet" )
    assert (
        test_validator_object.get_address() ==
        "one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9"
    )
    assert test_validator_object.add_bls_key( "5" )
    assert test_validator_object.remove_bls_key( "5" )
    assert test_validator_object.get_name() == "Alice"
    assert test_validator_object.get_identity() == "alice"
    assert test_validator_object.get_website() == "alice.harmony.one"
    assert test_validator_object.get_security_contact() == "Bob"
    assert test_validator_object.get_details() == "Don't mess with me!!!"
    assert isinstance(
        test_validator_object.get_min_self_delegation(),
        Decimal
    )
    assert isinstance(
        test_validator_object.get_max_total_delegation(),
        Decimal
    )
    assert isinstance( test_validator_object.get_amount(), Decimal )
    assert isinstance( test_validator_object.get_max_rate(), Decimal )
    assert isinstance( test_validator_object.get_max_change_rate(), Decimal )
    assert isinstance( test_validator_object.get_rate(), Decimal )
    assert len( test_validator_object.get_bls_keys() ) > 0


def test_validator_load_from_blockchain( setup_blockchain ):
    test_validator_object2 = validator.Validator(
        "one155jp2y76nazx8uw5sa94fr0m4s5aj8e5xm6fu3"
    )
    test_validator_object2.load_from_blockchain()
