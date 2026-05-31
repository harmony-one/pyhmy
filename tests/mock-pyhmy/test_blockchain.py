"""Mock-based unit tests for blockchain module (no localnet required)."""
from unittest.mock import patch, MagicMock

import pytest

from pyhmy import blockchain
from pyhmy.rpc.exceptions import RPCError
from pyhmy.exceptions import InvalidRPCReplyError


MOCK_ENDPOINT = "https://api.s0.b.hmny.io"


def _make_rpc_response(result):
    return {"jsonrpc": "2.0", "id": 1, "result": result}


def _make_rpc_error(msg="not found"):
    return {"jsonrpc": "2.0", "id": 1, "error": {"code": -32000, "message": msg}}


@patch("pyhmy.blockchain.rpc_request")
def test_chain_id(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(2)
    result = blockchain.chain_id(endpoint=MOCK_ENDPOINT)
    assert result == 2
    mock_rpc.assert_called_once()


@patch("pyhmy.blockchain.rpc_request")
def test_get_node_metadata(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "blskey": ["abc"],
            "version": "Harmony-v1.2.3",
            "network": "testnet",
            "chain-config": {"chain-id": 2, "staking-epoch": 1, "prestaking-epoch": 0},
            "is-leader": True,
            "shard-id": 0,
            "current-epoch": 10,
            "blocks-per-epoch": 16384,
            "role": "Validator",
            "dns-zone": "t.hmny.io",
            "is-archival": False,
        }
    )
    result = blockchain.get_node_metadata(endpoint=MOCK_ENDPOINT)
    assert isinstance(result, dict)
    assert result["shard-id"] == 0
    assert result["network"] == "testnet"


@patch("pyhmy.blockchain.rpc_request")
def test_get_sharding_structure(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        [
            {"shardID": 0, "current": True, "http": "http://0", "wss": "wss://0"},
            {"shardID": 1, "current": False, "http": "http://1", "wss": "wss://1"},
        ]
    )
    result = blockchain.get_sharding_structure(endpoint=MOCK_ENDPOINT)
    assert len(result) == 2
    assert result[0]["shardID"] == 0


@patch("pyhmy.blockchain.rpc_request")
def test_get_block_number(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(12345)
    result = blockchain.get_block_number(endpoint=MOCK_ENDPOINT)
    assert result == 12345


@patch("pyhmy.blockchain.rpc_request")
def test_get_block_by_number(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "hash": "0xabc",
            "number": 100,
            "epoch": 5,
            "viewID": 100,
            "timestamp": 1600000000,
            "transactions": ["0xtx1", "0xtx2"],
        }
    )
    result = blockchain.get_block_by_number(100, endpoint=MOCK_ENDPOINT)
    assert result["number"] == 100
    assert result["hash"] == "0xabc"


@patch("pyhmy.blockchain.rpc_request")
def test_get_block_by_hash(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {"hash": "0xdef", "number": 200}
    )
    result = blockchain.get_block_by_hash("0xdef", endpoint=MOCK_ENDPOINT)
    assert result["hash"] == "0xdef"


@patch("pyhmy.blockchain.rpc_request")
def test_get_latest_header(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "blockHash": "0xabc",
            "blockNumber": 1000,
            "shardID": 0,
            "leader": "one1leader",
            "viewID": 1000,
            "epoch": 50,
        }
    )
    result = blockchain.get_latest_header(endpoint=MOCK_ENDPOINT)
    assert result["blockNumber"] == 1000
    assert result["shardID"] == 0


@patch("pyhmy.blockchain.rpc_request")
def test_get_current_epoch(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(100)
    result = blockchain.get_current_epoch(endpoint=MOCK_ENDPOINT)
    assert result == 100


@patch("pyhmy.blockchain.rpc_request")
def test_get_gas_price(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(1000000000)
    result = blockchain.get_gas_price(endpoint=MOCK_ENDPOINT)
    assert result == 1000000000


@patch("pyhmy.blockchain.rpc_request")
def test_in_sync(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(True)
    result = blockchain.in_sync(endpoint=MOCK_ENDPOINT)
    assert result is True


@patch("pyhmy.blockchain.rpc_request")
def test_get_num_peers(mock_rpc):
    mock_rpc.return_value = _make_rpc_response("0x5")
    result = blockchain.get_num_peers(endpoint=MOCK_ENDPOINT)
    assert result == 5


@patch("pyhmy.blockchain.rpc_request")
def test_get_version(mock_rpc):
    mock_rpc.return_value = _make_rpc_response("0x1")
    result = blockchain.get_version(endpoint=MOCK_ENDPOINT)
    assert result == 1


@patch("pyhmy.blockchain.rpc_request")
def test_get_circulating_supply(mock_rpc):
    mock_rpc.return_value = _make_rpc_response("1234567890.123456")
    result = blockchain.get_circulating_supply(endpoint=MOCK_ENDPOINT)
    assert result == "1234567890.123456"


@patch("pyhmy.blockchain.rpc_request")
def test_get_total_supply(mock_rpc):
    mock_rpc.return_value = _make_rpc_response("13170000000")
    result = blockchain.get_total_supply(endpoint=MOCK_ENDPOINT)
    assert result == "13170000000"


@patch("pyhmy.blockchain.rpc_request")
def test_get_leader_address(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        "one1leader00000000000000000000000000000000"
    )
    result = blockchain.get_leader_address(endpoint=MOCK_ENDPOINT)
    assert result.startswith("one1")


@patch("pyhmy.blockchain.rpc_request")
def test_get_shard(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {"result": {"shard-id": 0}}
    )
    mock_rpc.return_value = _make_rpc_response({"shard-id": 0})
    result = blockchain.get_shard(endpoint=MOCK_ENDPOINT)
    assert result == 0


@patch("pyhmy.blockchain.rpc_request")
def test_get_bad_blocks(mock_rpc):
    mock_rpc.return_value = _make_rpc_response([])
    result = blockchain.get_bad_blocks(endpoint=MOCK_ENDPOINT)
    assert result == []


@patch("pyhmy.blockchain.rpc_request")
def test_get_peer_info(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {"peerid": "PeerID", "connected-peers": [], "blocked-peers": []}
    )
    result = blockchain.get_peer_info(endpoint=MOCK_ENDPOINT)
    assert result["peerid"] == "PeerID"


@patch("pyhmy.blockchain.rpc_request")
def test_protocol_version(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(635)
    result = blockchain.protocol_version(endpoint=MOCK_ENDPOINT)
    assert result == 635


@patch("pyhmy.blockchain.rpc_request")
def test_is_last_block(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(False)
    result = blockchain.is_last_block(0, endpoint=MOCK_ENDPOINT)
    assert result is False


@patch("pyhmy.blockchain.rpc_request")
def test_epoch_last_block(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(16383)
    result = blockchain.epoch_last_block(5, endpoint=MOCK_ENDPOINT)
    assert result == 16383


@patch("pyhmy.blockchain.rpc_request")
def test_get_last_cross_links(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        [{"hash": "0xabc", "block-number": 100, "shard-id": 1}]
    )
    result = blockchain.get_last_cross_links(endpoint=MOCK_ENDPOINT)
    assert isinstance(result, list)


@patch("pyhmy.blockchain.rpc_request")
def test_get_blocks_range(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        [{"number": 0, "hash": "0x0"}, {"number": 1, "hash": "0x1"}]
    )
    result = blockchain.get_blocks(0, 1, endpoint=MOCK_ENDPOINT)
    assert len(result) == 2


@patch("pyhmy.blockchain.rpc_request")
def test_get_block_signers(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        ["one1signer1", "one1signer2"]
    )
    result = blockchain.get_block_signers(1, endpoint=MOCK_ENDPOINT)
    assert len(result) == 2


@patch("pyhmy.blockchain.rpc_request")
def test_get_block_signers_keys(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        ["0xblskey1", "0xblskey2"]
    )
    result = blockchain.get_block_signers_keys(1, endpoint=MOCK_ENDPOINT)
    assert len(result) == 2


@patch("pyhmy.blockchain.rpc_request")
def test_is_block_signer(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(True)
    result = blockchain.is_block_signer(1, "one1addr", endpoint=MOCK_ENDPOINT)
    assert result is True


@patch("pyhmy.blockchain.rpc_request")
def test_get_signed_blocks(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(42)
    result = blockchain.get_signed_blocks(
        "one1addr", endpoint=MOCK_ENDPOINT
    )
    assert result == 42


@patch("pyhmy.blockchain.rpc_request")
def test_get_validators(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "shardID": 0,
            "validators": [
                {"address": "one1v1", "balance": 1000},
                {"address": "one1v2", "balance": 2000},
            ],
        }
    )
    result = blockchain.get_validators(10, endpoint=MOCK_ENDPOINT)
    assert len(result["validators"]) == 2


@patch("pyhmy.blockchain.rpc_request")
def test_get_validator_keys(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        ["0xkey1", "0xkey2", "0xkey3"]
    )
    result = blockchain.get_validator_keys(10, endpoint=MOCK_ENDPOINT)
    assert len(result) == 3


@patch("pyhmy.blockchain.rpc_request")
def test_beacon_in_sync(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(True)
    result = blockchain.beacon_in_sync(endpoint=MOCK_ENDPOINT)
    assert result is True


@patch("pyhmy.blockchain.rpc_request")
def test_get_header_by_number(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {"blockHash": "0xabc", "blockNumber": 50}
    )
    result = blockchain.get_header_by_number(50, endpoint=MOCK_ENDPOINT)
    assert result["blockNumber"] == 50


@patch("pyhmy.blockchain.rpc_request")
def test_get_latest_chain_headers(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "beacon-chain-header": {"number": 500, "hash": "0xbeacon"},
            "shard-chain-header": {"number": 500, "hash": "0xshard"},
        }
    )
    result = blockchain.get_latest_chain_headers(endpoint=MOCK_ENDPOINT)
    assert "beacon-chain-header" in result
    assert "shard-chain-header" in result


@patch("pyhmy.blockchain.rpc_request")
def test_get_block_transaction_count_by_number(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(10)
    result = blockchain.get_block_transaction_count_by_number(
        100, endpoint=MOCK_ENDPOINT
    )
    assert result == 10


@patch("pyhmy.blockchain.rpc_request")
def test_get_block_staking_transaction_count_by_number(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(3)
    result = blockchain.get_block_staking_transaction_count_by_number(
        100, endpoint=MOCK_ENDPOINT
    )
    assert result == 3


@patch("pyhmy.blockchain.rpc_request")
def test_get_staking_epoch(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {"chain-config": {"staking-epoch": 3}}
    )
    result = blockchain.get_staking_epoch(endpoint=MOCK_ENDPOINT)
    assert result == 3


@patch("pyhmy.blockchain.rpc_request")
def test_get_prestaking_epoch(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {"chain-config": {"prestaking-epoch": 2}}
    )
    result = blockchain.get_prestaking_epoch(endpoint=MOCK_ENDPOINT)
    assert result == 2


@patch("pyhmy.blockchain.rpc_request")
def test_rpc_error_raises(mock_rpc):
    mock_rpc.side_effect = RPCError(
        "hmyv2_chainId", MOCK_ENDPOINT, "method not found"
    )
    with pytest.raises(RPCError):
        blockchain.chain_id(endpoint=MOCK_ENDPOINT)


@patch("pyhmy.blockchain.rpc_request")
def test_none_result_raises(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(None)
    with pytest.raises(InvalidRPCReplyError):
        blockchain.get_block_number(endpoint=MOCK_ENDPOINT)
