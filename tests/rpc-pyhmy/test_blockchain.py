import pytest
import requests

from pyhmy.rpc import (
    blockchain,
    exceptions
)


test_epoch_number = 0
genesis_block_number = 0
test_block_number = 1
test_block_hash = None

def _test_blockchain_rpc(fn, *args, **kwargs):
    if not callable(fn):
        pytest.fail(f'Invalid function: {fn}')

    try:
        response = fn(*args, **kwargs)
    except Exception as e:
        if isinstance(e, exceptions.RPCError) and 'does not exist/is not available' in str(e):
            pytest.skip(f'{str(e)}')
        pytest.fail(f'Unexpected error: {e.__class__} {e}')
    return response

@pytest.mark.run(order=1)
def test_get_node_metadata(setup_blockchain):
    _test_blockchain_rpc(blockchain.get_node_metadata)

@pytest.mark.run(order=2)
def test_get_sharding_structure(setup_blockchain):
    _test_blockchain_rpc(blockchain.get_sharding_structure)

@pytest.mark.run(order=3)
def test_get_leader_address(setup_blockchain):
    _test_blockchain_rpc(blockchain.get_leader_address)

@pytest.mark.run(order=4)
def test_get_block_number(setup_blockchain):
    _test_blockchain_rpc(blockchain.get_block_number)

@pytest.mark.run(order=5)
def test_get_current_epoch(setup_blockchain):
    _test_blockchain_rpc(blockchain.get_current_epoch)

@pytest.mark.run(order=6)
def tset_get_gas_price(setup_blockchain):
    _test_blockchain_rpc(blockchain.get_gas_price)

@pytest.mark.run(order=7)
def test_get_num_peers(setup_blockchain):
    _test_blockchain_rpc(blockchain.get_num_peers)

@pytest.mark.run(order=8)
def test_get_latest_header(setup_blockchain):
    _test_blockchain_rpc(blockchain.get_latest_header)

@pytest.mark.run(order=9)
def test_get_latest_headers(setup_blockchain):
    _test_blockchain_rpc(blockchain.get_latest_headers)

@pytest.mark.run(order=10)
def test_get_block_by_number(setup_blockchain):
    global test_block_hash
    block = _test_blockchain_rpc(blockchain.get_block_by_number, test_block_number)
    test_block_hash = block['hash']

@pytest.mark.run(order=11)
def test_get_block_by_hash(setup_blockchain):
    if not test_block_hash:
        pytest.skip('Failed to get reference block hash')
    _test_blockchain_rpc(blockchain.get_block_by_hash, test_block_hash)

@pytest.mark.run(order=12)
def test_get_block_transaction_count_by_number(setup_blockchain):
    _test_blockchain_rpc(blockchain.get_block_transaction_count_by_number, test_block_number)

@pytest.mark.run(order=13)
def test_get_block_transaction_count_by_hash(setup_blockchain):
    if not test_block_hash:
        pytest.skip('Failed to get reference block hash')
    _test_blockchain_rpc(blockchain.get_block_transaction_count_by_hash, test_block_hash)

@pytest.mark.run(order=14)
def test_get_blocks(setup_blockchain):
    _test_blockchain_rpc(blockchain.get_blocks, genesis_block_number, test_block_number)

@pytest.mark.run(order=15)
def test_get_block_signers(setup_blockchain):
    _test_blockchain_rpc(blockchain.get_block_signers, test_block_number)

@pytest.mark.run(order=16)
def test_get_validators(setup_blockchain):
    _test_blockchain_rpc(blockchain.get_validators, test_epoch_number)
