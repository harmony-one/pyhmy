import pytest
import requests
import sys

sys.path.append("../../")
from pyhmy import (
    account
)

from pyhmy.rpc import (
    exceptions
)


explorer_endpoint = 'http://localhost:9599'
endpoint_shard_one = 'http://localhost:9501'
local_test_address = 'one1zksj3evekayy90xt4psrz8h6j2v3hla4qwz4ur'
test_validator_address = 'one18tvf56zqjkjnak686lwutcp5mqfnvee35xjnhc'
genesis_block_number = 0
test_block_number = 1

def _test_account_rpc(fn, *args, **kwargs):
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
def test_get_balance(setup_blockchain):
    balance = _test_account_rpc(account.get_balance, local_test_address)
    assert isinstance(balance, int)
    assert balance > 0

@pytest.mark.run(order=2)
def test_get_balance_by_block(setup_blockchain):
    balance = _test_account_rpc(account.get_balance_by_block, local_test_address, genesis_block_number)
    assert isinstance(balance, int)
    assert balance > 0

@pytest.mark.run(order=3)
def test_get_true_nonce(setup_blockchain):
    true_nonce = _test_account_rpc(account.get_account_nonce, local_test_address, true_nonce=True, endpoint=endpoint_shard_one)
    assert isinstance(true_nonce, int)
    assert true_nonce > 0

@pytest.mark.run(order=4)
def test_get_pending_nonce(setup_blockchain):
    pending_nonce = _test_account_rpc(account.get_account_nonce, local_test_address, endpoint=endpoint_shard_one)
    assert isinstance(pending_nonce, int)
    assert pending_nonce > 0

@pytest.mark.run(order=5)
def test_get_transaction_history(setup_blockchain):
    tx_history = _test_account_rpc(account.get_transaction_history, local_test_address, endpoint=explorer_endpoint)
    assert isinstance(tx_history, list)
    assert len(tx_history) >= 0

@pytest.mark.run(order=6)
def test_get_staking_transaction_history(setup_blockchain):
    staking_tx_history = _test_account_rpc(account.get_staking_transaction_history, test_validator_address, endpoint=explorer_endpoint)
    assert isinstance(staking_tx_history, list)
    assert len(staking_tx_history) > 0

@pytest.mark.run(order=7)
def test_get_balance_on_all_shards(setup_blockchain):
    balances = _test_account_rpc(account.get_balance_on_all_shards, local_test_address)
    assert isinstance(balances, list)
    assert len(balances) == 2

@pytest.mark.run(order=8)
def test_get_total_balance(setup_blockchain):
    total_balance = _test_account_rpc(account.get_total_balance, local_test_address)
    assert isinstance(total_balance, int)
    assert total_balance > 0

@pytest.mark.run(order=9)
def test_is_valid_address():
    assert account.is_valid_address('one1zksj3evekayy90xt4psrz8h6j2v3hla4qwz4ur')
    assert not account.is_valid_address('one1wje75aedczmj4dwjs0812xcg7vx0dy231cajk0')

@pytest.mark.run(order=10)
def test_get_staking_transaction_count():
    staking_tx_count = _test_account_rpc(account.get_staking_transaction_count, test_validator_address, endpoint=explorer_endpoint)
    assert isinstance(staking_tx_count, int)
    assert staking_tx_count > 0

@pytest.mark.run(order=11)
def test_get_transaction_count():
    tx_count = _test_account_rpc(account.get_transaction_count, test_validator_address, endpoint=explorer_endpoint)
    assert isinstance(tx_count, int)
    assert tx_count > 0
    
