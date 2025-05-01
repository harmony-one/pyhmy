import pytest
import requests

from pyhmy import account

from pyhmy.rpc import exceptions

explorer_endpoint = "http://localhost:9620"
endpoint_shard_one = "http://localhost:9622"
local_test_address = "one155jp2y76nazx8uw5sa94fr0m4s5aj8e5xm6fu3"
test_validator_address = local_test_address
genesis_block_number = 0
test_block_number = 1
fake_shard = "http://example.com"


def _test_account_rpc( fn, *args, **kwargs ):
    if not callable( fn ):
        pytest.fail( f"Invalid function: {fn}" )

    try:
        response = fn( *args, **kwargs )
    except Exception as e:
        if isinstance( e,
                       exceptions.RPCError
                      ) and "does not exist/is not available" in str( e ):
            pytest.skip( f"{str(e)}" )
        pytest.fail( f"Unexpected error: {e.__class__} {e}" )
    return response


def test_get_balance( setup_blockchain ):
    balance = _test_account_rpc( account.get_balance, local_test_address )
    assert isinstance( balance, int )
    assert balance > 0


def test_get_balance_by_block( setup_blockchain ):
    balance = _test_account_rpc(
        account.get_balance_by_block,
        local_test_address,
        genesis_block_number
    )
    assert isinstance( balance, int )
    assert balance > 0


def test_get_account_nonce( setup_blockchain ):
    true_nonce = _test_account_rpc(
        account.get_account_nonce,
        local_test_address,
        test_block_number,
        endpoint = endpoint_shard_one,
    )
    assert isinstance( true_nonce, int )


def test_get_transaction_history( setup_blockchain ):
    tx_history = _test_account_rpc(
        account.get_transaction_history,
        local_test_address,
        endpoint = explorer_endpoint
    )
    assert isinstance( tx_history, list )
    assert len( tx_history ) >= 0


def test_get_staking_transaction_history( setup_blockchain ):
    staking_tx_history = _test_account_rpc(
        account.get_staking_transaction_history,
        test_validator_address,
        endpoint = explorer_endpoint,
    )
    assert isinstance( staking_tx_history, list )
    assert len( staking_tx_history ) > 0


def test_get_balance_on_all_shards( setup_blockchain ):
    balances = _test_account_rpc(
        account.get_balance_on_all_shards,
        local_test_address
    )
    assert isinstance( balances, list )
    assert len( balances ) == 2


def test_get_total_balance( setup_blockchain ):
    total_balance = _test_account_rpc(
        account.get_total_balance,
        local_test_address
    )
    assert isinstance( total_balance, int )
    assert total_balance > 0


def test_is_valid_address():
    assert account.is_valid_address(
        "one1zksj3evekayy90xt4psrz8h6j2v3hla4qwz4ur"
    )
    assert not account.is_valid_address(
        "one1wje75aedczmj4dwjs0812xcg7vx0dy231cajk0"
    )


def test_get_transaction_count( setup_blockchain ):
    tx_count = _test_account_rpc(
        account.get_transaction_count,
        local_test_address,
        "latest",
        explorer_endpoint
    )
    assert isinstance( tx_count, int )
    assert tx_count > 0


def test_get_transactions_count( setup_blockchain ):
    tx_count = _test_account_rpc(
        account.get_transactions_count,
        local_test_address,
        "ALL",
        explorer_endpoint
    )


def test_get_staking_transactions_count( setup_blockchain ):
    tx_count = _test_account_rpc(
        account.get_staking_transactions_count,
        local_test_address,
        "ALL",
        explorer_endpoint,
    )
    assert isinstance( tx_count, int )


def test_errors():
    with pytest.raises( exceptions.RPCError ):
        account.get_balance( "", fake_shard )
    with pytest.raises( exceptions.RPCError ):
        account.get_balance_by_block( "", 1, fake_shard )
    with pytest.raises( exceptions.RPCError ):
        account.get_account_nonce( "", 1, fake_shard )
    with pytest.raises( exceptions.RPCError ):
        account.get_transaction_count( "", 1, fake_shard )
    with pytest.raises( exceptions.RPCError ):
        account.get_transactions_count( "", 1, fake_shard )
    with pytest.raises( exceptions.RPCError ):
        account.get_transactions_count( "", "ALL", fake_shard )
    with pytest.raises( exceptions.RPCError ):
        account.get_transaction_history( "", endpoint = fake_shard )
    with pytest.raises( exceptions.RPCError ):
        account.get_staking_transaction_history( "", endpoint = fake_shard )
    with pytest.raises( exceptions.RPCError ):
        account.get_balance_on_all_shards( "", endpoint = fake_shard )
    with pytest.raises( exceptions.RPCError ):
        account.get_total_balance( "", endpoint = fake_shard )
