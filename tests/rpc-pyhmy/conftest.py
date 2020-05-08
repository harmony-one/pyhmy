import json
import time

import pytest
import requests

test_validator_address = 'one18tvf56zqjkjnak686lwutcp5mqfnvee35xjnhc'
transfer_raw_transaction = '0xf86f80843b9aca008252088080943ad89a684095a53edb47d7ddc5e034d8133667318a152d02c7e14af68000008028a0e453ffec54139efccb6b689df723f12b969710fbf1438abc1dcf5618e1c3b0d5a0595543cffcc8e41549bfc74900e6c7317ed1e667cfa71e07da1d8a663d363823'
tx_hash = '0xfe6af62e5037d2e33412a5837e5753ebed2e4f9ab7da988bd7aa35d17ae4283f'
create_validator_raw_transaction = '0xf9015680f90105943ad89a684095a53edb47d7ddc5e034d813366731d984746573748474657374847465737484746573748474657374ddc988016345785d8a0000c9880c7d713b49da0000c887b1a2bc2ec500008a022385a827e8155000008b084595161401484a000000f1b0282554f2478661b4844a05a9deb1837aac83931029cb282872f0dcd7239297c499c02ea8da8746d2f08ca2b037e89891f862b86003557e18435c201ecc10b1664d1aea5b4ec59dbfe237233b953dbd9021b86bc9770e116ed3c413fe0334d89562568a10e133d828611f29fee8cdab9719919bbcc1f1bf812c73b9ccd0f89b4f0b9ca7e27e66d58bbb06fcf51c295b1d076cfc878a0228f16f86157860000080843b9aca008351220027a018385211a150ca032c3526cef0aba6a75f99a18cb73f547f67bab746be0c7a64a028be921002c6eb949b3932afd010dfe1de2459ec7fe84403b9d9d8892394a78c'
staking_tx_hash = '0x57ec011aabdeb078a4816502224022f291fa8b07c82bbae8476f514a1d71c730'

@pytest.fixture(scope="session", autouse=True)
def setup_blockchain():
    endpoint = 'http://localhost:9500'
    timeout = 30
    headers = {
        'Content-Type': 'application/json'
    }

    metadata = None
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": 'hmy_getNodeMetadata',
            "params": []
        }
        response = requests.request('POST', endpoint, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
        metadata = json.loads(response.content)
        if 'error' in metadata:
            pytest.skip(f"Error in hmy_getNodeMetadata reply: {metadata['error']}", allow_module_level=True)
        if 'chain-config' not in metadata['result']:
            pytest.skip("Chain config not found in hmy_getNodeMetadata reply", allow_module_level=True)
    except Exception as e:
        pytest.skip('Can not connect to local blockchain or bad hmy_getNodeMetadata reply', allow_module_level=True)

    latest_header = None
    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": 'hmy_latestHeader',
            "params": []
        }
        response = requests.request('POST', endpoint, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
        latest_header = json.loads(response.content)
        if 'error' in latest_header:
            pytest.skip(f"Error in hmy_latestHeader reply: {latest_header['error']}", allow_module_level=True)
    except Exception as e:
        pytest.skip('Failed to get hmy_latestHeader reply', allow_module_level=True)

    if metadata and latest_header:
        staking_epoch = metadata['result']['chain-config']['staking-epoch']
        current_epoch = latest_header['result']['epoch']
        if staking_epoch > current_epoch:
            pytest.skip('Not staking epoch: current {current_epoch}, staking {staking_epoch}', allow_module_level=True)

    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": 'hmy_sendRawTransaction',
            "params": [transfer_raw_transaction]
        }
        response = requests.request('POST', endpoint, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
        tx = json.loads(response.content)
        if 'error' in tx:
            pytest.skip(f"Error in hmy_sendRawTransaction reply: {tx['error']}", allow_module_level=True)
    except Exception as e:
        pytest.skip('Failed to get hmy_sendRawTransaction reply', allow_module_level=True)

    time.sleep(15)  # Sleep to let transaction finalize

    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": 'hmy_getTransactionByHash',
            "params": [tx_hash]
        }
        response = requests.request('POST', endpoint, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
        tx_data = json.loads(response.content)
        if 'error' in tx_data:
            pytest.skip(f"Error in hmy_getTransactionByHash reply: {tx_data['error']}", allow_module_level=True)
        if not tx_data['result']:
            pytest.skip(f"Funding transaction failed: {tx_hash}", allow_module_level=True)
    except Exception as e:
        pytest.skip('Failed to get hmy_getTransactionByHash reply', allow_module_level=True)

    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": 'hmy_sendRawStakingTransaction',
            "params": [create_validator_raw_transaction]
        }
        response = requests.request('POST', endpoint, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
        staking_tx = json.loads(response.content)
        if 'error' in staking_tx:
            pytest.skip(f"Error in hmy_sendRawStakingTransaction reply: {staking_tx['error']}", allow_module_level=True)
    except Exception as e:
        pytest.skip('Failed to get hmy_sendRawStakingTransaction reply', allow_module_level=True)

    time.sleep(30)  # Sleep to let transaction finalize

    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": 'hmy_getStakingTransactionByHash',
            "params": [staking_tx_hash]
        }
        response = requests.request('POST', endpoint, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
        tx_data = json.loads(response.content)
        if 'error' in tx_data:
            pytest.skip(f"Error in hmy_getStakingTransactionByHash reply: {tx_data['error']}", allow_module_level=True)
        if not tx_data['result']:
            pytest.skip(f"Staking transaction failed: {staking_tx_hash}", allow_module_level=True)
    except Exception as e:
        pytest.skip('Failed to get hmy_getStakingTransactionByHash reply', allow_module_level=True)
