import json
import time
import random

import pytest
import requests

# private keys
# 1f84c95ac16e6a50f08d44c7bde7aff8742212fda6e4321fde48bf83bef266dc / one155jp2y76nazx8uw5sa94fr0m4s5aj8e5xm6fu3 (genesis)
# 3c86ac59f6b038f584be1c08fced78d7c71bb55d5655f81714f3cddc82144c65 / one1ru3p8ff0wsyl7ncsx3vwd5szuze64qz60upg37 (transferred 503)

endpoint = "http://localhost:9620"
timeout = 30
headers = {
    "Content-Type": "application/json"
}
txs = [
    # same shard 503 ONE transfer from one155jp2y76nazx8uw5sa94fr0m4s5aj8e5xm6fu3 to one1ru3p8ff0wsyl7ncsx3vwd5szuze64qz60upg37 (0 nonce)
    "0xf86f8085174876e8008252088080941f2213a52f7409ff4f103458e6d202e0b3aa805a891b4486fafde57c00008027a0d7c0b20207dcc9dde376822dc3f5625eac6f59a7526111695cdba3e29553ca17a05d4ca9a421ae16f89cbf6848186eaea7a800da732446dff9952e7c1e91d414e3",
    # contract creation by one1ru3p8ff0wsyl7ncsx3vwd5szuze64qz60upg37 (0 nonce)
    "0xf8e88085174876e800830186a080808080b8946080604052348015600f57600080fd5b50607780601d6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80634936cd3614602d575b600080fd5b604080516001815290519081900360200190f3fea2646970667358221220fa3fa0e8d0267831a59f4dd5edf39a513d07e98461cb06660ad28d4beda744cd64736f6c634300080f003327a08bf26ee0120c296b17af507f62606abdb5c5f09a65642c3d30b349b8bfbb3d69a03ec7be51c615bcbf2f1d63f6eaa56cf8d7be81671717f90239619830a81ebc9f",
    # cross shard transfer by one1ru3p8ff0wsyl7ncsx3vwd5szuze64qz60upg37 (1 nonce)
    "0xf86b0185174876e800825208800194c9c6d47ee5f2e3e08d7367ad1a1373ba9dd1724185174876e8008027a02501c517220e9499f14e97c20b0a88cd3b7ba80637bba43ed295422e69a3f300a079b8e1213c9506184aed6ac2eb0b2cb00594c3f9fcdd6c088937ce17fe47107c",
]
stxs = [
    # creation of one155jp2y76nazx8uw5sa94fr0m4s5aj8e5xm6fu3 as validator (1 nonce)
    "0xf9017c80f9012994a5241513da9f4463f1d4874b548dfbac29d91f34f83d85416c69636585616c69636591616c6963652e6861726d6f6e792e6f6e6583426f629a41726520796f75206576656e2072656164696e6720746869733fddc988016345785d8a0000c9880c7d713b49da0000c887b1a2bc2ec500008a021e19e0c9bab24000008a152d02c7e14af6800000f1b0a20e70089664a874b00251c5e85d35a73871531306f3af43e02138339d294e6bb9c4eb82162199c6a852afeaa8d68712f862b860ef2c49a2f31fbbd23c21bc176eaf05cd0bebe6832033075d81fea7cff6f9bc1ab42f3b6895c5493fe645d8379d2eaa1413de55a9d3ce412a4f747cb57d52cc4da4754bfb2583ec9a41fe5dd48287f964f276336699959a5fcef3391dc24df00d8a021e19e0c9bab24000000185174876e8008403473bc028a08c1146305eaef981aa24c2f17c8519664d10c99ee42acedbc258749930d31a7ca031dadf114ee6ab9bd09933208094c65037b66c796bcfc57a70158106b37357b0",
    # delegation by one1ru3p8ff0wsyl7ncsx3vwd5szuze64qz60upg37 to one155jp2y76nazx8uw5sa94fr0m4s5aj8e5xm6fu3 (2 nonce)
    "0xf88302f4941f2213a52f7409ff4f103458e6d202e0b3aa805a94a5241513da9f4463f1d4874b548dfbac29d91f3489056bc75e2d631000000285174876e80082c35028a02c5e953062dcdfa2de9723639b63bab45705eb6dfbfe7f44536ed266c3c7ca20a0742964e646338e7431874f70715565d99c01c762324355c69db34a9ed9de81d7",
]
tx_hashes = [
    "0xc26be5776aa57438bccf196671a2d34f3f22c9c983c0f844c62b2fb90403aa43",
    "0xa605852dd2fa39ed42e101c17aaca9d344d352ba9b24b14b9af94ec9cb58b31f",
    "0xf73ba634cb96fc0e3e2c9d3b4c91379e223741be4a5aa56e6d6caf49c1ae75cf",
]
stx_hashes = [
    "0x400e9831d358f5daccd153cad5bf53650a0d413bd8682ec0ffad55367d162968",
    "0xc8177ace2049d9f4eb4a45fd6bd6b16f693573d036322c36774cc00d05a3e24f",
]
assert len( txs ) == len( tx_hashes ), "Mismatch in tx and tx_hash count"
assert len( stxs ) == len( stx_hashes ), "Mismatch in stx and stx_hash count"


@pytest.fixture( scope = "session", autouse = True )
def setup_blockchain():
    # return

    metadata = _check_connection()
    _check_staking_epoch( metadata )

    for i in range( len( txs ) ):
        tx = txs[ i ]
        tx_hash = tx_hashes[ i ]
        _send_transaction( tx, endpoint )
        if not _wait_for_transaction_confirmed( tx_hash, endpoint ):
            pytest.fail(
                "Could not confirm initial transaction #{} on chain"
                .format( i )
            )

    for i in range( len( stxs ) ):
        stx = stxs[ i ]
        stx_hash = stx_hashes[ i ]
        _send_staking_transaction( stx, endpoint )
        if not _wait_for_staking_transaction_confirmed( stx_hash, endpoint ):
            pytest.fail(
                "Could not confirm initial staking transaction #{} on chain"
                .format( i )
            )


def _check_connection():
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": "hmyv2_getNodeMetadata",
            "params": [],
        }
        response = requests.request(
            "POST",
            endpoint,
            headers = headers,
            data = json.dumps( payload ),
            timeout = timeout,
            allow_redirects = True,
        )
        metadata = json.loads( response.content )
        if "error" in metadata:
            pytest.fail(
                f"Error in hmyv2_getNodeMetadata reply: {metadata['error']}"
            )
        if "chain-config" not in metadata[ "result" ]:
            pytest.fail(
                "Chain config not found in hmyv2_getNodeMetadata reply"
            )
        return metadata
    except Exception as e:
        pytest.fail(
            "Can not connect to local blockchain or bad hmyv2_getNodeMetadata reply"
        )


def _check_staking_epoch( metadata ):
    latest_header = None
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": "hmyv2_latestHeader",
            "params": [],
        }
        response = requests.request(
            "POST",
            endpoint,
            headers = headers,
            data = json.dumps( payload ),
            timeout = timeout,
            allow_redirects = True,
        )
        latest_header = json.loads( response.content )
        if "error" in latest_header:
            pytest.fail(
                f"Error in hmyv2_latestHeader reply: {latest_header['error']}"
            )
    except Exception as e:
        pytest.fail(
            "Failed to get hmyv2_latestHeader reply"
        )

    if metadata and latest_header:
        staking_epoch = metadata[ "result" ][ "chain-config" ][ "staking-epoch"
                                                               ]
        current_epoch = latest_header[ "result" ][ "epoch" ]
        if staking_epoch > current_epoch:
            pytest.fail(
                f"Not staking epoch: current {current_epoch}, staking {staking_epoch}"
            )


def _send_transaction( raw_tx, endpoint ):
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": "hmyv2_sendRawTransaction",
            "params": [ raw_tx ],
        }
        response = requests.request(
            "POST",
            endpoint,
            headers = headers,
            data = json.dumps( payload ),
            timeout = timeout,
            allow_redirects = True,
        )
        tx = json.loads( response.content )
        if "error" in tx:
            pytest.fail(
                f"Error in hmyv2_sendRawTransaction reply: {tx['error']}"
            )
    except Exception as e:
        pytest.fail(
            "Failed to get hmyv2_sendRawTransaction reply"
        )


def _check_transaction( tx_hash, endpoint ):
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": "hmyv2_getTransactionByHash",
            "params": [ tx_hash ],
        }
        response = requests.request(
            "POST",
            endpoint,
            headers = headers,
            data = json.dumps( payload ),
            timeout = timeout,
            allow_redirects = True,
        )
        tx_data = json.loads( response.content )
        return tx_data
    except Exception as e:
        pytest.fail(
            "Failed to get hmyv2_getTransactionByHash reply"
        )


def _wait_for_transaction_confirmed( tx_hash, endpoint, timeout = 30 ):
    start_time = time.time()
    while ( time.time() - start_time ) <= timeout:
        tx_data = _check_transaction( tx_hash, endpoint )
        if tx_data is not None:
            block_hash = tx_data[ "result" ].get( "blockHash", "0x00" )
            unique_chars = "".join( set( list( block_hash[ 2 : ] ) ) )
            if unique_chars != "0":
                return True
        time.sleep( random.uniform( 0.2, 0.5 ) )
    return False


def _send_staking_transaction( raw_tx, endpoint = endpoint ):
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": "hmyv2_sendRawStakingTransaction",
            "params": [ raw_tx ],
        }
        response = requests.request(
            "POST",
            endpoint,
            headers = headers,
            data = json.dumps( payload ),
            timeout = timeout,
            allow_redirects = True,
        )
        staking_tx = json.loads( response.content )
        if "error" in staking_tx:
            pytest.fail(
                f"Error in hmyv2_sendRawStakingTransaction reply: {staking_tx['error']}"
            )
    except Exception as e:
        pytest.fail(
            "Failed to get hmyv2_sendRawStakingTransaction reply"
        )


def _check_staking_transaction( stx_hash, endpoint = endpoint ):
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": "hmyv2_getStakingTransactionByHash",
            "params": [ stx_hash ],
        }
        response = requests.request(
            "POST",
            endpoint,
            headers = headers,
            data = json.dumps( payload ),
            timeout = timeout,
            allow_redirects = True,
        )
        stx_data = json.loads( response.content )
        return stx_data
    except Exception as e:
        pytest.fail(
            "Failed to get hmyv2_getStakingTransactionByHash reply"
        )


def _wait_for_staking_transaction_confirmed( tx_hash, endpoint, timeout = 30 ):
    answer = False
    start_time = time.time()
    while ( time.time() - start_time ) <= timeout:
        tx_data = _check_staking_transaction( tx_hash, endpoint )
        if tx_data is not None:
            block_hash = tx_data[ "result" ].get( "blockHash", "0x00" )
            unique_chars = "".join( set( list( block_hash[ 2 : ] ) ) )
            if unique_chars != "0":
                answer = True
        time.sleep( random.uniform( 0.2, 0.5 ) )
    return answer
