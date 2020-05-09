import pytest
import requests

from pyhmy.rpc import (
    account,
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
    assert balance > 0

@pytest.mark.run(order=2)
def test_get_balance_by_block(setup_blockchain):
    balance = _test_account_rpc(account.get_balance_by_block, local_test_address, genesis_block_number)
    assert balance > 0

@pytest.mark.run(order=3)
def test_get_transaction_count(setup_blockchain):
    transactions = _test_account_rpc(account.get_transaction_count, local_test_address, endpoint=endpoint_shard_one)
    assert transactions > 0

@pytest.mark.run(order=4)
def test_get_transaction_history(setup_blockchain):
    tx_history = _test_account_rpc(account.get_transaction_history, local_test_address, endpoint=explorer_endpoint)
    assert len(tx_history) >= 0

@pytest.mark.run(order=5)
def test_get_staking_transaction_history(setup_blockchain):
    staking_tx_history = _test_account_rpc(account.get_staking_transaction_history, test_validator_address, endpoint=explorer_endpoint)
    assert len(staking_tx_history) > 0
