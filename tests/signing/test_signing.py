from pyhmy.signing.account import HmyAccount


def test_sign_eth_tx():
    eth_tx_dict = {
        'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
        'value': 1000000000,
        'gas': 2000000,
        'gasPrice': 234567897654321,
        'nonce': 0,
        'chainId': 1
    }

    k = "0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318"
    h = HmyAccount()

    output = h.sign_transaction(eth_tx_dict, k)

    assert output.rawTransaction.hex() == '0xf86a8086d55698372431831e848094f0109fc8df283027b6285cc889f5aa624eac1f55843b9aca008025a009ebb6ca057a0535d6186462bc0b465b561c94a295bdb0621fc19208ab149a9ca0440ffd775ce91a833ab410777204d5341a6f9fa91216a6f3ee2c051fea6a0428'


def test_sign_hmy_tx():
    hmy_tx_dict = {'gas': '0x5208',
                   'gasPrice': '0x3b9aca00',
                   'nonce': '0x1',
                   'shardID': 0,
                   'to': '0x52789f18a342da8023cc401e5d2b14a6b710fba9',
                   'toShardID': 1,
                   'value': '0x16345785d8a0000',
                   'chainId': 2
                   }

    k = "3eb5b377f122b98d7cacf99e0363c14ab6333c9ded189cf6ce3923e1a9b04588"
    h = HmyAccount()

    output = h.sign_transaction(hmy_tx_dict, k)

    assert output.rawTransaction.hex() == "0xf86d01843b9aca0082520880019452789f18a342da8023cc401e5d2b14a6b710fba988016345785d8a00008028a01095f775386e0e3203446179a7a62e5ce1e765c200b5d885f6bb5b141155bd4da0651350a31e1797035cbf878e4c26069e9895845071d01308573532512cca5820"
