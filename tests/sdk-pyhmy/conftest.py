import json
import time

import pytest
import requests

test_validator_address = 'one18tvf56zqjkjnak686lwutcp5mqfnvee35xjnhc'
transfer_raw_transaction = '0xf86f80843b9aca008252080180943ad89a684095a53edb47d7ddc5e034d8133667318a152d02c7e14af68000008027a0ec6c8ad0f70b3c826fa77574c6815a8f73936fafb7b2701a7082ad7d278c95a9a0429f9f166b1c1d385a4ec8f8b86604c26e427c2b0a1c85d9cf4ec6bbd0719508'
tx_hash = '0x1fa20537ea97f162279743139197ecf0eac863278ac1c8ada9a6be5d1e31e633'
create_validator_raw_transaction = '0xf9015680f90105943ad89a684095a53edb47d7ddc5e034d813366731d984746573748474657374847465737484746573748474657374ddc988016345785d8a0000c9880c7d713b49da0000c887b1a2bc2ec500008a022385a827e8155000008b084595161401484a000000f1b0282554f2478661b4844a05a9deb1837aac83931029cb282872f0dcd7239297c499c02ea8da8746d2f08ca2b037e89891f862b86003557e18435c201ecc10b1664d1aea5b4ec59dbfe237233b953dbd9021b86bc9770e116ed3c413fe0334d89562568a10e133d828611f29fee8cdab9719919bbcc1f1bf812c73b9ccd0f89b4f0b9ca7e27e66d58bbb06fcf51c295b1d076cfc878a0228f16f86157860000080843b9aca008351220027a018385211a150ca032c3526cef0aba6a75f99a18cb73f547f67bab746be0c7a64a028be921002c6eb949b3932afd010dfe1de2459ec7fe84403b9d9d8892394a78c'
staking_tx_hash = '0x57ec011aabdeb078a4816502224022f291fa8b07c82bbae8476f514a1d71c730'
contract_tx_hash = '0xa13414dd152173395c69a11e79dea31bf029660f747a42a53744181d05571e70'
contract_raw_transaction = '0xf9025080843b9aca008366916c80808080b901fc608060405234801561001057600080fd5b50336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555061019c806100606000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c8063445df0ac146100465780638da5cb5b14610064578063fdacd576146100ae575b600080fd5b61004e6100dc565b6040518082815260200191505060405180910390f35b61006c6100e2565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6100da600480360360208110156100c457600080fd5b8101908080359060200190929190505050610107565b005b60015481565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141561016457806001819055505b5056fea265627a7a723158209b80813a158b44af65aee232b44c0ac06472c48f4abbe298852a39f0ff34a9f264736f6c6343000510003227a03a3ad2b7c2934a8325fc04d04daad740d337bb1f589482bbb1d091e1be804d29a00c46772871866a34f254e6197a526bebc2067f75edc53c488b31d84e07c3c685'

endpoint = 'http://localhost:9500'
endpoint_shard_one = 'http://localhost:9501'
timeout = 30
headers = {
    'Content-Type': 'application/json'
}

@pytest.fixture(scope="session", autouse=True)
def setup_blockchain():

    metadata = _check_connection()
    _check_staking_epoch(metadata)

    tx_data = _check_funding_transaction()

    if not tx_data['result']:
        _send_funding_transaction()
        time.sleep(20)  # Sleep to let cross shard transaction finalize

        tx_data = _check_funding_transaction()
        if 'error' in tx_data:
            pytest.skip(f"Error in hmyv2_getTransactionByHash reply: {tx_data['error']}", allow_module_level=True)
        if not tx_data['result']:
            pytest.skip(f"Funding transaction failed: {tx_hash}", allow_module_level=True)


    stx_data = _check_staking_transaction()

    if not stx_data['result']:
        _send_staking_transaction()
        time.sleep(30)  # Sleep to let transaction finalize

        stx_data = _check_staking_transaction()
        if 'error' in stx_data:
            pytest.skip(f"Error in hmyv2_getStakingTransactionByHash reply: {stx_data['error']}", allow_module_level=True)
        if not stx_data['result']:
            pytest.skip(f"Staking transaction failed: {staking_tx_hash}", allow_module_level=True)

    contract_data = _check_contract_transaction()

    if not contract_data['result']:
        _send_contract_transaction()
        times.sleep(30)

        contract_data = _check_contract_transaction()
        if 'error' in contract_data:
            pytest.skip(f"Error in hmyv2_getStakingTransactionByHash reply: {contract_data['error']}", allow_module_level=True)
        if not contract_data['result']:
            pytest.skip(f"Staking transaction failed: {contract_tx_hash}", allow_module_level=True)

    # TODO: Build data object to return data instead of hard coded values in the test files
    try:
        return int(stx_data['result']['blockNumber'])
    except (TypeError, KeyError) as e:
        pytest.skip(f"Unexpected reply for hmyv2_getStakingTransactionByHash: {stx_data['result']}", allow_module_level=True)


def _check_connection():
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": 'hmyv2_getNodeMetadata',
            "params": []
        }
        response = requests.request('POST', endpoint, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
        metadata = json.loads(response.content)
        if 'error' in metadata:
            pytest.skip(f"Error in hmyv2_getNodeMetadata reply: {metadata['error']}", allow_module_level=True)
        if 'chain-config' not in metadata['result']:
            pytest.skip("Chain config not found in hmyv2_getNodeMetadata reply", allow_module_level=True)
        return metadata
    except Exception as e:
        pytest.skip('Can not connect to local blockchain or bad hmyv2_getNodeMetadata reply', allow_module_level=True)

def _check_staking_epoch(metadata):
    latest_header = None
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": 'hmyv2_latestHeader',
            "params": []
        }
        response = requests.request('POST', endpoint, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
        latest_header = json.loads(response.content)
        if 'error' in latest_header:
            pytest.skip(f"Error in hmyv2_latestHeader reply: {latest_header['error']}", allow_module_level=True)
    except Exception as e:
        pytest.skip('Failed to get hmyv2_latestHeader reply', allow_module_level=True)

    if metadata and latest_header:
        staking_epoch = metadata['result']['chain-config']['staking-epoch']
        current_epoch = latest_header['result']['epoch']
        if staking_epoch > current_epoch:
            pytest.skip(f'Not staking epoch: current {current_epoch}, staking {staking_epoch}', allow_module_level=True)

def _send_funding_transaction():
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": 'hmyv2_sendRawTransaction',
            "params": [transfer_raw_transaction]
        }
        response = requests.request('POST', endpoint_shard_one, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
        tx = json.loads(response.content)
        if 'error' in tx:
            pytest.skip(f"Error in hmyv2_sendRawTransaction reply: {tx['error']}", allow_module_level=True)
    except Exception as e:
        pytest.skip('Failed to get hmyv2_sendRawTransaction reply', allow_module_level=True)

def _check_funding_transaction():
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": 'hmyv2_getTransactionByHash',
            "params": [tx_hash]
        }
        response = requests.request('POST', endpoint_shard_one, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
        tx_data = json.loads(response.content)
        return tx_data
    except Exception as e:
        pytest.skip('Failed to get hmyv2_getTransactionByHash reply', allow_module_level=True)

def _check_contract_transaction():
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": 'hmyv2_getTransactionByHash',
            "params": [contract_tx_hash]
        }
        response = requests.request('POST', endpoint, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
        tx_data = json.loads(response.content)
        return tx_data
    except Exception as e:
        pytest.skip('Failed to get hmyv2_getTransactionByHash reply', allow_module_level=True)

def _send_contract_transaction():
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": 'hmyv2_sendRawTransaction',
            "params": [contract_raw_transaction]
        }
        response = requests.request('POST', endpoint, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
        tx_data = json.loads(response.content)
        if 'error' in staking_tx:
            pytest.skip(f"Error in hmyv2_sendRawTransaction reply: {tx_data['error']}", allow_module_level=True)
    except Exception as e:
        pytest.skip('Failed to get hmyv2_sendRawTransaction reply', allow_module_level=True)

def _send_staking_transaction():
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": 'hmyv2_sendRawStakingTransaction',
            "params": [create_validator_raw_transaction]
        }
        response = requests.request('POST', endpoint, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
        staking_tx = json.loads(response.content)
        if 'error' in staking_tx:
            pytest.skip(f"Error in hmyv2_sendRawStakingTransaction reply: {staking_tx['error']}", allow_module_level=True)
    except Exception as e:
        pytest.skip('Failed to get hmyv2_sendRawStakingTransaction reply', allow_module_level=True)

def _check_staking_transaction():
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": 'hmyv2_getStakingTransactionByHash',
            "params": [staking_tx_hash]
        }
        response = requests.request('POST', endpoint, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
        stx_data = json.loads(response.content)
        return stx_data
    except Exception as e:
        pytest.skip('Failed to get hmyv2_getStakingTransactionByHash reply', allow_module_level=True)
