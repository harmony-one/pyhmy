from pyhmy import staking_signing, staking_structures

from pyhmy.numbers import convert_one_to_atto

# other transactions (create/edit validator) are in test_validator.py
# test_delegate is the same as test_undelegate (except the directive) so it has been omitted
# staking transactions without a chain id have been omitted as well, since the node does not accept them anyway
"""
let stakingTx
let stakeMsg3: CollectRewards = new CollectRewards(
  'one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9'
)
stakingTx = new StakingTransaction(
  Directive.DirectiveCollectRewards,
  stakeMsg3,
  2,    // nonce
  numberToHex(new Unit('1').asOne().toWei()),    // gasPrice
  100,  // gasLimit
  null,    // chainId
);
const signed = stakingTx.rlpSign('4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48')
console.log( 'Signed transaction' )
console.log(signed)
"""
# def test_collect_rewards_no_chain_id():
#     transaction_dict = {
#         'directive': staking_structures.Directive.CollectRewards,
#         'delegatorAddress': 'one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9',
#         'nonce': 2,
#         'gasPrice': int(convert_one_to_atto(1)),
#         'gasLimit': 100,
#     }
#     signed_tx = staking_signing.sign_staking_transaction(transaction_dict, '4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48')
#     assert signed_tx.rawTransaction.hex() == '0xf85a04d594ebcd16e8c1d8f493ba04e99a56474122d81a9c5823a0490e4ceb747563ba40da3e0db8a65133cf6f6ae4c48a24866cd6aa1f0d6c2414a06dbd51a67b35b5685e7b7420cba26e63b0e7d3c696fc6cb69d48e54fcad280e9'
"""
let stakingTx
let stakeMsg3: CollectRewards = new CollectRewards(
  'one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9'
)
stakingTx = new StakingTransaction(
  Directive.DirectiveCollectRewards,
  stakeMsg3,
  2,    // nonce
  numberToHex(new Unit('1').asOne().toWei()),    // gasPrice
  100,  // gasLimit
  1,    // chainId
);
const signed = stakingTx.rlpSign('4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48')
console.log( 'Signed transaction' )
console.log(signed)
"""


def test_collect_rewards_chain_id():
    transaction_dict = {
        "directive": staking_structures.Directive.CollectRewards,
        "delegatorAddress": "one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9",
        "nonce": 2,
        "gasPrice": int(convert_one_to_atto(1)),
        "gasLimit": 100,
        "chainId": 1,  # with chainId for coverage
    }
    signed_tx = staking_signing.sign_staking_transaction(
        transaction_dict,
        "4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48",
    )
    assert (
        signed_tx.rawTransaction.hex() ==
        "0xf86504d594ebcd16e8c1d8f493ba04e99a56474122d81a9c5802880de0b6b3a76400006425a055d6c3c0d8e7a1e75152db361a2ed47f5ab54f6f19b0d8e549953dbdf13ba647a076e1367dfca38eae3bd0e8da296335acabbaeb87dc17e47ebe4942db29334099"
    )


"""
let stakingTx
let stakeMsg4: Delegate = new Delegate(
  'one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9',
  'one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9',
  5
)
stakingTx = new StakingTransaction(
  Directive.DirectiveDelegate,
  stakeMsg4,
  2,    // nonce
  numberToHex(new Unit('1').asOne().toWei()),    // gasPrice
  100,  // gasLimit
  2,    // chainId
);
const signed = stakingTx.rlpSign('4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48')
console.log( 'Signed transaction' )
console.log(signed)
"""


def test_delegate():
    transaction_dict = {
        "directive": staking_structures.Directive.Delegate,
        "delegatorAddress": "one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9",
        "validatorAddress": "one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9",
        "amount": 5,
        "nonce": 2,
        "gasPrice": int( convert_one_to_atto( 1 ) ),
        "gasLimit": 100,
        "chainId": 2,
    }
    signed_tx = staking_signing.sign_staking_transaction(
        transaction_dict,
        "4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48",
    )
    assert (
        signed_tx.rawTransaction.hex() ==
        "0xf87b02eb94ebcd16e8c1d8f493ba04e99a56474122d81a9c5894ebcd16e8c1d8f493ba04e99a56474122d81a9c580502880de0b6b3a76400006428a0c856fd483a989ca4db4b5257f6996729527828fb21ec13cc65f0bffe6c015ab1a05e9d3c92742e8cb7450bebdfb7ad277ccbfc9fa0719db0b12a715a0a173cadd6"
    )
