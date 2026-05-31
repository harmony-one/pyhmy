"""Mock-based unit tests for transaction module."""
from unittest.mock import patch

import pytest

from pyhmy import transaction
from pyhmy.exceptions import InvalidRPCReplyError, TxConfirmationTimedoutError
from pyhmy.rpc.exceptions import RPCError


MOCK_ENDPOINT = "https://api.s0.b.hmny.io"


def _make_rpc_response(result):
    return {"jsonrpc": "2.0", "id": 1, "result": result}


def _make_tx_dict(block_hash="0xabc", block_number=100):
    return {
        "blockHash": block_hash,
        "blockNumber": block_number,
        "from": "one1from",
        "to": "one1to",
        "gas": 21000,
        "gasPrice": 1000000000,
        "hash": "0xtxhash",
        "nonce": 5,
        "shardID": 0,
        "toShardID": 0,
        "timestamp": 1600000000,
        "transactionIndex": 0,
        "value": 1000000000000000000,
        "r": "0xr",
        "s": "0xs",
        "v": "0x27",
    }


@patch("pyhmy.transaction.rpc_request")
def test_get_pending_transactions(mock_rpc):
    mock_rpc.return_value = _make_rpc_response([_make_tx_dict()])
    result = transaction.get_pending_transactions(endpoint=MOCK_ENDPOINT)
    assert isinstance(result, list)
    assert len(result) == 1


@patch("pyhmy.transaction.rpc_request")
def test_get_transaction_by_hash(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(_make_tx_dict())
    result = transaction.get_transaction_by_hash(
        "0xtxhash", endpoint=MOCK_ENDPOINT
    )
    assert result["hash"] == "0xtxhash"
    assert result["blockNumber"] == 100


@patch("pyhmy.transaction.rpc_request")
def test_get_transaction_by_hash_not_found(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(None)
    result = transaction.get_transaction_by_hash(
        "0xnonexistent", endpoint=MOCK_ENDPOINT
    )
    assert result is None


@patch("pyhmy.transaction.rpc_request")
def test_get_transaction_receipt(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "blockHash": "0xabc",
            "blockNumber": 100,
            "contractAddress": None,
            "cumulativeGasUsed": 21000,
            "from": "one1from",
            "gasUsed": 21000,
            "status": 1,
            "to": "one1to",
            "transactionHash": "0xtxhash",
            "transactionIndex": 0,
            "logs": [],
        }
    )
    result = transaction.get_transaction_receipt(
        "0xtxhash", endpoint=MOCK_ENDPOINT
    )
    assert result["status"] == 1
    assert result["transactionHash"] == "0xtxhash"


@patch("pyhmy.transaction.rpc_request")
def test_get_transaction_by_block_hash_and_index(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(_make_tx_dict())
    result = transaction.get_transaction_by_block_hash_and_index(
        "0xblockhash", 0, endpoint=MOCK_ENDPOINT
    )
    assert result["hash"] == "0xtxhash"


@patch("pyhmy.transaction.rpc_request")
def test_get_transaction_by_block_number_and_index(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(_make_tx_dict())
    result = transaction.get_transaction_by_block_number_and_index(
        100, 0, endpoint=MOCK_ENDPOINT
    )
    assert result["transactionIndex"] == 0


@patch("pyhmy.transaction.rpc_request")
def test_get_pending_cx_receipts(mock_rpc):
    mock_rpc.return_value = _make_rpc_response([])
    result = transaction.get_pending_cx_receipts(endpoint=MOCK_ENDPOINT)
    assert isinstance(result, list)


@patch("pyhmy.transaction.rpc_request")
def test_get_cx_receipt_by_hash(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "blockHash": "0xabc",
            "blockNumber": 100,
            "hash": "0xcxhash",
            "from": "one1from",
            "to": "one1to",
            "shardID": 0,
            "toShardID": 1,
            "value": 1000,
        }
    )
    result = transaction.get_cx_receipt_by_hash(
        "0xcxhash", endpoint=MOCK_ENDPOINT
    )
    assert result["hash"] == "0xcxhash"


@patch("pyhmy.transaction.rpc_request")
def test_resend_cx_receipt(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(True)
    result = transaction.resend_cx_receipt(
        "0xcxhash", endpoint=MOCK_ENDPOINT
    )
    assert result is True


@patch("pyhmy.transaction.rpc_request")
def test_get_staking_transaction_by_hash(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "blockHash": "0xabc",
            "blockNumber": 100,
            "from": "one1from",
            "hash": "0xstxhash",
            "type": "CollectRewards",
            "nonce": 3,
            "gas": 50000,
            "gasPrice": 1,
        }
    )
    result = transaction.get_staking_transaction_by_hash(
        "0xstxhash", endpoint=MOCK_ENDPOINT
    )
    assert result["type"] == "CollectRewards"


@patch("pyhmy.transaction.rpc_request")
def test_get_staking_transaction_by_block_hash_and_index(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {"hash": "0xstxhash", "type": "Delegate"}
    )
    result = transaction.get_staking_transaction_by_block_hash_and_index(
        "0xblockhash", 0, endpoint=MOCK_ENDPOINT
    )
    assert result["hash"] == "0xstxhash"


@patch("pyhmy.transaction.rpc_request")
def test_get_pool_stats(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {"executable-count": 5, "non-executable-count": 2}
    )
    result = transaction.get_pool_stats(endpoint=MOCK_ENDPOINT)
    assert result["executable-count"] == 5


@patch("pyhmy.transaction.rpc_request")
def test_get_pending_staking_transactions(mock_rpc):
    mock_rpc.return_value = _make_rpc_response([])
    result = transaction.get_pending_staking_transactions(
        endpoint=MOCK_ENDPOINT
    )
    assert isinstance(result, list)


@patch("pyhmy.transaction.rpc_request")
def test_get_transaction_error_sink(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        [
            {
                "tx-hash-id": "0xbadhash",
                "time-at-rejection": 1600000000,
                "error-message": "insufficient funds",
            }
        ]
    )
    result = transaction.get_transaction_error_sink(endpoint=MOCK_ENDPOINT)
    assert len(result) == 1
    assert result[0]["error-message"] == "insufficient funds"


@patch("pyhmy.transaction.rpc_request")
def test_get_staking_transaction_error_sink(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        [
            {
                "tx-hash-id": "0xbadstx",
                "time-at-rejection": 1600000000,
                "error-message": "unknown validator",
                "directive-kind": "CreateValidator",
            }
        ]
    )
    result = transaction.get_staking_transaction_error_sink(
        endpoint=MOCK_ENDPOINT
    )
    assert len(result) == 1


@patch("pyhmy.transaction.send_raw_transaction")
@patch("pyhmy.transaction.get_transaction_by_hash")
def test_send_and_confirm_raw_transaction(mock_get_tx, mock_send_raw):
    mock_send_raw.return_value = "0xtxhash"
    mock_get_tx.return_value = _make_tx_dict(
        block_hash="0x12345", block_number=200
    )
    result = transaction.send_and_confirm_raw_transaction(
        "0xsignedtx", endpoint=MOCK_ENDPOINT, timeout=10
    )
    assert result["hash"] == "0xtxhash"
    assert result["blockNumber"] == 200


@patch("pyhmy.transaction.send_raw_transaction")
@patch("pyhmy.transaction.get_transaction_by_hash")
def test_send_and_confirm_times_out(mock_get_tx, mock_send_raw):
    mock_send_raw.return_value = "0xtxhash"
    mock_get_tx.return_value = _make_tx_dict(
        block_hash="0x0000000000000000000000000000000000000000000000000000000000000000",
        block_number=None,
    )
    with pytest.raises(TxConfirmationTimedoutError):
        transaction.send_and_confirm_raw_transaction(
            "0xsignedtx", endpoint=MOCK_ENDPOINT, timeout=1
        )


@patch("pyhmy.transaction.rpc_request")
def test_get_staking_transaction_by_block_number_and_index(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {"hash": "0xstxhash", "type": "Undelegate"}
    )
    result = transaction.get_staking_transaction_by_block_number_and_index(
        100, 0, endpoint=MOCK_ENDPOINT
    )
    assert result["hash"] == "0xstxhash"
