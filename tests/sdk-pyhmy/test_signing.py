from pyhmy import (
    signing
)

"""
Test signature source (node.js)
import { Transaction, RLPSign, TxStatus } from '@harmony-js/transaction';
import { HttpProvider, Messenger } from '@harmony-js/network';
import { ChainType, ChainID } from '@harmony-js/utils';

const provider = new HttpProvider('http://localhost:9500');
let privateKey = '4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48'
let hmyMessenger = new Messenger(provider, ChainType.Ethereum, ChainID.Default);

let transaction: Transaction = new Transaction(
        {
          gasLimit: 100,
          gasPrice: 1,
          to: "one1z3u3d9expexf5u03sjzvn7vhkvywtye9nqmmlu",
          value: 5,
          nonce: 2,
        },
        hmyMessenger,
        TxStatus.INTIALIZED,
      );
console.log('Unsigned transaction')
let payload = transaction.txPayload
console.log(payload)
let signed = RLPSign(transaction, privateKey);
console.log( 'Signed transaction' )
console.log(signed)
"""
def test_eth_transaction():
    transaction_dict = {
        'nonce': 2,
        'gasPrice': 1,
        'gas': 100,             # signing.py uses Ether, which by default calls it gas
        'to': '0x14791697260e4c9a71f18484c9f997b308e59325',
        'value': 5,
    }
    signed_tx = signing.sign_transaction(transaction_dict, '4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48')
    assert signed_tx.rawTransaction.hex() == '0xf85d0201649414791697260e4c9a71f18484c9f997b308e5932505801ca0b364f4296bfd3231889d1b9ac94c68abbcb8ee6a6c7a5fa412ac82b5b7b0d5d1a02233864842ab28ee4f99c207940a867b0f8534ca362836190792816b48dde3b1'

"""
Test signature source (node.js)
import { Transaction, RLPSign, TxStatus } from '@harmony-js/transaction';
import { HttpProvider, Messenger } from '@harmony-js/network';
import { ChainType, ChainID } from '@harmony-js/utils';

const provider = new HttpProvider('http://localhost:9500');
let privateKey = '4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48'
let hmyMessenger = new Messenger(provider, ChainType.Harmony, ChainID.HmyMainnet);

let transaction: Transaction = new Transaction(
        {
          gasLimit: 100,
          gasPrice: 1,
          to: "one1z3u3d9expexf5u03sjzvn7vhkvywtye9nqmmlu",
          value: 5,
          nonce: 2,
          shardID: 0,
          toShardID: 1
        },
        hmyMessenger,
        TxStatus.INTIALIZED,
      );
console.log('Unsigned transaction')
let payload = transaction.txPayload
console.log(payload)
let signed = RLPSign(transaction, privateKey);
console.log( 'Signed transaction' )
console.log(signed)
"""
def test_hmy_transaction():
    transaction_dict = {
        'nonce': 2,
        'gasPrice': 1,
        'gas': 100,             # signing.py uses Ether, which by default calls it gas
        'to': '0x14791697260e4c9a71f18484c9f997b308e59325',
        'value': 5,
        'shardID': 0,
        'toShardID': 1,
        'chainId': 'HmyMainnet'
    }
    signed_tx = signing.sign_transaction(transaction_dict, '4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48')
    assert signed_tx.rawTransaction.hex() == '0xf85f02016480019414791697260e4c9a71f18484c9f997b308e59325058026a02a203357ca6d7cdec981ad3d3692ad2c9e24536a9b6e7b486ce2f94f28c7563ea010d38cd0312a153af0aa7d8cd986040c36118bba373cb94e3e86fd4aedce904d'
