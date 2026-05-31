"""Mock-based unit tests for contract module."""
from unittest.mock import patch

import pytest

from pyhmy import contract
from pyhmy.exceptions import InvalidRPCReplyError
from pyhmy.rpc.exceptions import RPCError


MOCK_ENDPOINT = "https://api.s0.b.hmny.io"


def _make_rpc_response(result):
    return {"jsonrpc": "2.0", "id": 1, "result": result}


@patch("pyhmy.contract.rpc_request")
def test_call(mock_rpc):
    mock_rpc.return_value = _make_rpc_response("0x0000000000000000000000000000000000000000000000000000000000000042")
    result = contract.call(
        "0xcontract", "latest", data="0x1234", endpoint=MOCK_ENDPOINT
    )
    assert result.startswith("0x")


@patch("pyhmy.contract.rpc_request")
def test_estimate_gas(mock_rpc):
    mock_rpc.return_value = _make_rpc_response("0x5208")
    result = contract.estimate_gas(
        "0xcontract", data="0x", endpoint=MOCK_ENDPOINT
    )
    assert result == 21000


@patch("pyhmy.contract.rpc_request")
def test_get_code(mock_rpc):
    mock_rpc.return_value = _make_rpc_response("0x60806040")
    result = contract.get_code(
        "0xcontract", "latest", endpoint=MOCK_ENDPOINT
    )
    assert result == "0x60806040"


@patch("pyhmy.contract.rpc_request")
def test_get_code_empty(mock_rpc):
    mock_rpc.return_value = _make_rpc_response("0x")
    result = contract.get_code(
        "0xcontract", "latest", endpoint=MOCK_ENDPOINT
    )
    assert result == "0x"


@patch("pyhmy.contract.rpc_request")
def test_get_storage_at(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        "0x0000000000000000000000000000000000000000000000000000000000000001"
    )
    result = contract.get_storage_at(
        "0xcontract", "0x0", "latest", endpoint=MOCK_ENDPOINT
    )
    assert result.endswith("0001")


@patch("pyhmy.contract.get_transaction_receipt")
def test_get_contract_address_from_hash(mock_receipt):
    mock_receipt.return_value = {"contractAddress": "0xnewcontract"}
    result = contract.get_contract_address_from_hash(
        "0xtxhash", endpoint=MOCK_ENDPOINT
    )
    assert result == "0xnewcontract"


@patch("pyhmy.contract.get_transaction_receipt")
def test_get_contract_address_no_contract(mock_receipt):
    mock_receipt.return_value = {}
    with pytest.raises(ValueError):
        contract.get_contract_address_from_hash(
            "0xtxhash", endpoint=MOCK_ENDPOINT
        )


@patch("pyhmy.contract.rpc_request")
def test_get_logs(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        [
            {
                "address": "0xcontract",
                "topics": ["0xtopic1"],
                "data": "0xdata",
                "blockNumber": "0x64",
                "blockHash": "0xblockhash",
                "transactionHash": "0xtxhash",
                "logIndex": "0x0",
                "removed": False,
            }
        ]
    )
    result = contract.get_logs(
        from_block="0x0",
        to_block="0x64",
        address="0xcontract",
        endpoint=MOCK_ENDPOINT,
    )
    assert len(result) == 1
    assert result[0]["address"] == "0xcontract"


@patch("pyhmy.contract.rpc_request")
def test_new_filter(mock_rpc):
    mock_rpc.return_value = _make_rpc_response("0xfilterid123")
    result = contract.new_filter(
        address="0xcontract", endpoint=MOCK_ENDPOINT
    )
    assert result == "0xfilterid123"


@patch("pyhmy.contract.rpc_request")
def test_new_block_filter(mock_rpc):
    mock_rpc.return_value = _make_rpc_response("0xfilterid456")
    result = contract.new_block_filter(endpoint=MOCK_ENDPOINT)
    assert result == "0xfilterid456"


@patch("pyhmy.contract.rpc_request")
def test_get_filter_changes(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        [
            {
                "address": "0xcontract",
                "topics": ["0xtopic"],
                "data": "0x",
                "blockNumber": "0x65",
            }
        ]
    )
    result = contract.get_filter_changes(
        "0xfilterid", endpoint=MOCK_ENDPOINT
    )
    assert len(result) == 1


@patch("pyhmy.contract.rpc_request")
def test_uninstall_filter(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(True)
    result = contract.uninstall_filter(
        "0xfilterid", endpoint=MOCK_ENDPOINT
    )
    assert result is True


@patch("pyhmy.contract.rpc_request")
def test_get_logs_with_block_hash(mock_rpc):
    mock_rpc.return_value = _make_rpc_response([])
    result = contract.get_logs(
        block_hash="0xblockhash", endpoint=MOCK_ENDPOINT
    )
    assert isinstance(result, list)


@patch("pyhmy.contract.rpc_request")
def test_get_logs_with_topics(mock_rpc):
    mock_rpc.return_value = _make_rpc_response([])
    result = contract.get_logs(
        from_block="0x0",
        to_block="0x64",
        address="0xcontract",
        topics=[["0xtopic1", "0xtopic2"]],
        endpoint=MOCK_ENDPOINT,
    )
    assert isinstance(result, list)


@patch("pyhmy.contract.rpc_request")
def test_call_rpc_error(mock_rpc):
    mock_rpc.side_effect = RPCError(
        "hmyv2_call", MOCK_ENDPOINT, "execution reverted"
    )
    with pytest.raises(RPCError):
        contract.call("0xaddr", "latest", endpoint=MOCK_ENDPOINT)


def test_encode_abi_function_no_abi():
    abi = [{"name": "getValue", "type": "function", "inputs": []}]
    encoded = contract.encode_abi_function(abi, "getValue")
    assert encoded.startswith("0x")


def test_encode_abi_function_not_found():
    with pytest.raises(ValueError):
        contract.encode_abi_function([], "nonexistent")


def test_encode_abi_function_with_args():
    abi = [
        {"name": "balanceOf", "type": "function", "inputs": [
            {"name": "owner", "type": "address"}
        ]}
    ]
    encoded = contract.encode_abi_function(
        abi, "balanceOf",
        args=["one18t4yj4fuutj83uwqckkvxp9gfa0568uc48ggj7"]
    )
    assert encoded.startswith("0x")
    assert len(encoded) > 10
