import pytest
import requests
import sys

sys.path.append("../../")

from pyhmy import (
    blockchain
)

from pyhmy.rpc import (
    exceptions
)


test_epoch_number = 0
genesis_block_number = 0
test_block_number = 1
test_block_hash = None
test_block_number_start = 10
test_block_number_end = 20

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
    metadata = _test_blockchain_rpc(blockchain.get_node_metadata)
    assert isinstance(metadata, dict)

@pytest.mark.run(order=2)
def test_get_sharding_structure(setup_blockchain):
    sharding_structure = _test_blockchain_rpc(blockchain.get_sharding_structure)
    assert isinstance(sharding_structure, list)
    assert len(sharding_structure) > 0

@pytest.mark.run(order=3)
def test_get_leader_address(setup_blockchain):
    leader = _test_blockchain_rpc(blockchain.get_leader_address)
    assert isinstance(leader, str)
    assert 'one1' in leader

@pytest.mark.run(order=4)
def test_get_block_number(setup_blockchain):
    current_block_number = _test_blockchain_rpc(blockchain.get_block_number)
    assert isinstance(current_block_number, int)

@pytest.mark.run(order=5)
def test_get_current_epoch(setup_blockchain):
    current_epoch = _test_blockchain_rpc(blockchain.get_current_epoch)
    assert isinstance(current_epoch, int)

@pytest.mark.run(order=6)
def tset_get_gas_price(setup_blockchain):
    gas = _test_blockchain_rpc(blockchain.get_gas_price)
    assert isinstance(gas, int)

@pytest.mark.run(order=7)
def test_get_num_peers(setup_blockchain):
    peers = _test_blockchain_rpc(blockchain.get_num_peers)
    assert isinstance(peers, int)

@pytest.mark.run(order=8)
def test_get_latest_header(setup_blockchain):
    header = _test_blockchain_rpc(blockchain.get_latest_header)
    assert isinstance(header, dict)

@pytest.mark.run(order=9)
def test_get_latest_headers(setup_blockchain):
    header_pair = _test_blockchain_rpc(blockchain.get_latest_headers)
    assert isinstance(header_pair, dict)

@pytest.mark.run(order=10)
def test_get_block_by_number(setup_blockchain):
    global test_block_hash
    block = _test_blockchain_rpc(blockchain.get_block_by_number, test_block_number)
    assert isinstance(block, dict)
    assert 'hash' in block.keys()
    test_block_hash = block['hash']

@pytest.mark.run(order=11)
def test_get_block_by_hash(setup_blockchain):
    if not test_block_hash:
        pytest.skip('Failed to get reference block hash')
    block = _test_blockchain_rpc(blockchain.get_block_by_hash, test_block_hash)
    assert isinstance(block, dict)

@pytest.mark.run(order=12)
def test_get_block_transaction_count_by_number(setup_blockchain):
    tx_count = _test_blockchain_rpc(blockchain.get_block_transaction_count_by_number, test_block_number)
    assert isinstance(tx_count, int)

@pytest.mark.run(order=13)
def test_get_block_transaction_count_by_hash(setup_blockchain):
    if not test_block_hash:
        pytest.skip('Failed to get reference block hash')
    tx_count = _test_blockchain_rpc(blockchain.get_block_transaction_count_by_hash, test_block_hash)
    assert isinstance(tx_count, int)

@pytest.mark.run(order=14)
def test_get_blocks(setup_blockchain):
    blocks = _test_blockchain_rpc(blockchain.get_blocks, genesis_block_number, test_block_number)
    assert isinstance(blocks, list)
    assert len(blocks) == (test_block_number - genesis_block_number + 1)

@pytest.mark.run(order=15)
def test_get_block_signers(setup_blockchain):
    block_signers = _test_blockchain_rpc(blockchain.get_block_signers, test_block_number_start,test_block_number_end)
    assert isinstance(block_signers, list)
    assert len(block_signers) > 0

@pytest.mark.run(order=16)
def test_get_validators(setup_blockchain):
    validators = _test_blockchain_rpc(blockchain.get_validators, test_epoch_number)
    assert isinstance(validators, dict)
    assert 'validators' in validators.keys()
    assert len(validators['validators']) > 0

@pytest.mark.run(order=17)
def test_get_shard(setup_blockchain):
    shard = _test_blockchain_rpc(blockchain.get_shard)
    assert isinstance(shard, int)
    assert shard == 0

@pytest.mark.run(order=18)
def test_get_staking_epoch(setup_blockchain):
    staking_epoch = _test_blockchain_rpc(blockchain.get_staking_epoch)
    assert isinstance(staking_epoch, int)

@pytest.mark.run(order=19)
def test_get_prestaking_epoch(setup_blockchain):
    prestaking_epoch = _test_blockchain_rpc(blockchain.get_prestaking_epoch)
    assert isinstance(prestaking_epoch, int)

@pytest.mark.run(order=20)
def test_get_bad_blocks(setup_blockchain):
    # TODO: Remove skip when RPC is fixed
    pytest.skip("Known error with hmy_getCurrentBadBlocks")
    bad_blocks = _test_blockchain_rpc(blockchain.get_bad_blocks)
    assert isinstance(bad_blocks, list)

@pytest.mark.run(order=21)
def test_get_validator_keys(setup_blockchain):
    keys = _test_blockchain_rpc(blockchain.get_validator_keys, test_epoch_number)
    assert isinstance(keys, list)
    assert len(keys) > 0

@pytest.mark.run(order=22)
def test_get_block_signer_keys(setup_blockchain):
    keys = _test_blockchain_rpc(blockchain.get_block_signer_keys, test_block_number)
    assert isinstance(keys, list)
    assert len(keys) > 0

@pytest.mark.run(order=23)
def test_get_circulate_supply(setup_blockchain):
    supply = _test_blockchain_rpc(blockchain.get_circulate_supply)
    assert isinstance(supply, int)
    assert supply > 0
