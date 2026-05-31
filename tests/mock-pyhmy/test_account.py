"""Mock-based unit tests for account module."""
from unittest.mock import patch

import pytest

from pyhmy import account
from pyhmy.rpc.exceptions import RPCError


MOCK_ENDPOINT = "https://api.s0.b.hmny.io"
TEST_ADDR = "one18t4yj4fuutj83uwqckkvxp9gfa0568uc48ggj7"


def _make_rpc_response(result):
    return {"jsonrpc": "2.0", "id": 1, "result": result}


@patch("pyhmy.account.rpc_request")
def test_get_balance(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(1000000000000000000)
    result = account.get_balance(TEST_ADDR, endpoint=MOCK_ENDPOINT)
    assert result == 1000000000000000000


@patch("pyhmy.account.rpc_request")
def test_get_balance_by_block(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(500000000000000000)
    result = account.get_balance_by_block(
        TEST_ADDR, 0, endpoint=MOCK_ENDPOINT
    )
    assert result == 500000000000000000


@patch("pyhmy.account.rpc_request")
def test_get_account_nonce(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(42)
    result = account.get_account_nonce(
        TEST_ADDR, "latest", endpoint=MOCK_ENDPOINT
    )
    assert result == 42


@patch("pyhmy.account.rpc_request")
def test_get_nonce(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(42)
    result = account.get_nonce(TEST_ADDR, endpoint=MOCK_ENDPOINT)
    assert result == 42


@patch("pyhmy.account.rpc_request")
def test_get_transaction_count(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(10)
    result = account.get_transaction_count(
        TEST_ADDR, "latest", endpoint=MOCK_ENDPOINT
    )
    assert result == 10


@patch("pyhmy.account.rpc_request")
def test_get_transactions_count(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(25)
    result = account.get_transactions_count(
        TEST_ADDR, "ALL", endpoint=MOCK_ENDPOINT
    )
    assert result == 25


@patch("pyhmy.account.rpc_request")
def test_get_transactions_count_sent(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(15)
    result = account.get_transactions_count(
        TEST_ADDR, "SENT", endpoint=MOCK_ENDPOINT
    )
    assert result == 15


@patch("pyhmy.account.rpc_request")
def test_get_transactions_count_received(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(10)
    result = account.get_transactions_count(
        TEST_ADDR, "RECEIVED", endpoint=MOCK_ENDPOINT
    )
    assert result == 10


@patch("pyhmy.account.rpc_request")
def test_get_staking_transactions_count(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(5)
    result = account.get_staking_transactions_count(
        TEST_ADDR, "ALL", endpoint=MOCK_ENDPOINT
    )
    assert result == 5


@patch("pyhmy.account.rpc_request")
def test_get_transaction_history(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "transactions": [
                {"hash": "0xtx1", "from": TEST_ADDR, "nonce": 0},
                {"hash": "0xtx2", "from": TEST_ADDR, "nonce": 1},
            ]
        }
    )
    result = account.get_transaction_history(
        TEST_ADDR, page=0, page_size=100, endpoint=MOCK_ENDPOINT
    )
    assert len(result) == 2
    assert result[0]["nonce"] == 0


@patch("pyhmy.account.rpc_request")
def test_get_transaction_history_empty(mock_rpc):
    mock_rpc.return_value = _make_rpc_response({"transactions": []})
    result = account.get_transaction_history(
        TEST_ADDR, page=0, page_size=10, endpoint=MOCK_ENDPOINT
    )
    assert len(result) == 0


@patch("pyhmy.account.rpc_request")
def test_get_staking_transaction_history(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "staking_transactions": [
                {
                    "hash": "0xstx1",
                    "type": "Delegate",
                    "from": TEST_ADDR,
                }
            ]
        }
    )
    result = account.get_staking_transaction_history(
        TEST_ADDR, page=0, page_size=100, endpoint=MOCK_ENDPOINT
    )
    assert len(result) == 1
    assert result[0]["type"] == "Delegate"


@patch("pyhmy.account.get_sharding_structure")
@patch("pyhmy.account.get_balance")
def test_get_balance_on_all_shards(mock_get_balance, mock_sharding):
    mock_sharding.return_value = [
        {"shardID": 0, "http": "http://localhost:9500"},
        {"shardID": 1, "http": "http://localhost:9501"},
    ]
    mock_get_balance.side_effect = [100, 200]
    result = account.get_balance_on_all_shards(TEST_ADDR)
    assert len(result) == 2
    assert result[0] == {"shard": 0, "balance": 100}
    assert result[1] == {"shard": 1, "balance": 200}


@patch("pyhmy.account.get_sharding_structure")
@patch("pyhmy.account.get_balance")
def test_get_total_balance(mock_get_balance, mock_sharding):
    mock_sharding.return_value = [
        {"shardID": 0, "http": "http://localhost:9500"},
        {"shardID": 1, "http": "http://localhost:9501"},
    ]
    mock_get_balance.side_effect = [100, 200]
    result = account.get_total_balance(TEST_ADDR)
    assert result == 300


@patch("pyhmy.account.rpc_request")
def test_rpc_error(mock_rpc):
    mock_rpc.side_effect = RPCError(
        "hmyv2_getBalance", MOCK_ENDPOINT, "timeout"
    )
    with pytest.raises(RPCError):
        account.get_balance(TEST_ADDR, endpoint=MOCK_ENDPOINT)


def test_is_valid_address():
    assert account.is_valid_address(
        "one1zksj3evekayy90xt4psrz8h6j2v3hla4qwz4ur"
    )
    assert not account.is_valid_address("invalid")
    assert not account.is_valid_address("0x1234")
