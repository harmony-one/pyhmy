"""Mock-based unit tests for staking module."""
from unittest.mock import patch

import pytest

from pyhmy import staking
from pyhmy.rpc.exceptions import RPCError


MOCK_ENDPOINT = "https://api.s0.b.hmny.io"
TEST_VAL = "one1xjanr7lgulc0fqyc8dmfp6jfwuje2d94xfnzyd"
TEST_DEL = "one1y2624lg0mpkxkcttaj0c85pp8pfmh2tt5zhdte"


def _make_rpc_response(result):
    return {"jsonrpc": "2.0", "id": 1, "result": result}


@patch("pyhmy.staking.rpc_request")
def test_get_all_validator_addresses(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        [TEST_VAL, "one1othervalidator"]
    )
    result = staking.get_all_validator_addresses(endpoint=MOCK_ENDPOINT)
    assert len(result) == 2
    assert TEST_VAL in result


@patch("pyhmy.staking.rpc_request")
def test_get_validator_information(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "validator": {
                "address": TEST_VAL,
                "name": "TestValidator",
                "identity": "test",
                "rate": "0.1",
                "min-self-delegation": 10000000000000000000000,
                "max-total-delegation": 40000000000000000000000,
            },
            "total-delegation": 25000000000000000000000,
            "currently-in-committee": True,
            "active-status": "active",
            "epos-status": "currently elected",
            "lifetime": {
                "reward-accumulated": 1000000000000000000,
                "blocks": {"to-sign": 1000, "signed": 950},
                "apr": "0.12",
            },
        }
    )
    result = staking.get_validator_information(
        TEST_VAL, endpoint=MOCK_ENDPOINT
    )
    assert result["validator"]["name"] == "TestValidator"
    assert result["active-status"] == "active"
    assert result["currently-in-committee"] is True


@patch("pyhmy.staking.rpc_request")
def test_get_elected_validator_addresses(mock_rpc):
    mock_rpc.return_value = _make_rpc_response([TEST_VAL])
    result = staking.get_elected_validator_addresses(endpoint=MOCK_ENDPOINT)
    assert len(result) > 0


@patch("pyhmy.staking.rpc_request")
def test_get_validators(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "shardID": 0,
            "validators": [{"address": TEST_VAL, "balance": 1000000000000000000}],
        }
    )
    result = staking.get_validators(100, endpoint=MOCK_ENDPOINT)
    assert result["shardID"] == 0


@patch("pyhmy.staking.rpc_request")
def test_get_validator_keys(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        ["0xblskey1", "0xblskey2"]
    )
    result = staking.get_validator_keys(100, endpoint=MOCK_ENDPOINT)
    assert len(result) == 2


@patch("pyhmy.staking.rpc_request")
def test_get_validator_information_by_block_number(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "validator": {"name": "Test", "address": TEST_VAL},
            "total-delegation": 10000,
        }
    )
    result = staking.get_validator_information_by_block_number(
        TEST_VAL, 1000, endpoint=MOCK_ENDPOINT
    )
    assert result["validator"]["name"] == "Test"


@patch("pyhmy.staking.rpc_request")
def test_get_all_validator_information(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        [
            {"validator": {"address": TEST_VAL}},
            {"validator": {"address": "one1other"}},
        ]
    )
    result = staking.get_all_validator_information(
        page=0, endpoint=MOCK_ENDPOINT
    )
    assert len(result) == 2


@patch("pyhmy.staking.rpc_request")
def test_get_validator_self_delegation(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(5000000000000000000000)
    result = staking.get_validator_self_delegation(
        TEST_VAL, endpoint=MOCK_ENDPOINT
    )
    assert result > 0


@patch("pyhmy.staking.rpc_request")
def test_get_validator_total_delegation(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(10000000000000000000000)
    result = staking.get_validator_total_delegation(
        TEST_VAL, endpoint=MOCK_ENDPOINT
    )
    assert result > 0


@patch("pyhmy.staking.rpc_request")
def test_get_all_delegation_information(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        [
            [
                {
                    "delegator_address": TEST_DEL,
                    "validator_address": TEST_VAL,
                    "amount": 1000000000000000000,
                    "reward": 0,
                }
            ]
        ]
    )
    result = staking.get_all_delegation_information(
        page=0, endpoint=MOCK_ENDPOINT
    )
    assert len(result) == 1


@patch("pyhmy.staking.rpc_request")
def test_get_delegations_by_delegator(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        [
            {
                "validator_address": TEST_VAL,
                "delegator_address": TEST_DEL,
                "amount": 500000000000000000,
                "reward": 1000000000000000,
                "Undelegations": [],
            }
        ]
    )
    result = staking.get_delegations_by_delegator(
        TEST_DEL, endpoint=MOCK_ENDPOINT
    )
    assert len(result) == 1
    assert result[0]["amount"] == 500000000000000000


@patch("pyhmy.staking.rpc_request")
def test_get_delegations_by_validator(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        [
            {
                "validator_address": TEST_VAL,
                "delegator_address": TEST_DEL,
                "amount": 1000000000000000000,
            }
        ]
    )
    result = staking.get_delegations_by_validator(
        TEST_VAL, endpoint=MOCK_ENDPOINT
    )
    assert len(result) == 1


@patch("pyhmy.staking.rpc_request")
def test_get_delegation_by_delegator_and_validator(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "validator_address": TEST_VAL,
            "delegator_address": TEST_DEL,
            "amount": 500000000000000000,
        }
    )
    result = staking.get_delegation_by_delegator_and_validator(
        TEST_DEL, TEST_VAL, endpoint=MOCK_ENDPOINT
    )
    assert result["amount"] == 500000000000000000


@patch("pyhmy.staking.rpc_request")
def test_get_available_redelegation_balance(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(0)
    result = staking.get_available_redelegation_balance(
        TEST_DEL, endpoint=MOCK_ENDPOINT
    )
    assert result == 0


@patch("pyhmy.staking.rpc_request")
def test_get_current_utility_metrics(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "AccumulatorSnapshot": 1000000,
            "CurrentStakedPercentage": "45.5",
            "Deviation": "1.2",
            "Adjustment": "0.5",
        }
    )
    result = staking.get_current_utility_metrics(endpoint=MOCK_ENDPOINT)
    assert "CurrentStakedPercentage" in result


@patch("pyhmy.staking.rpc_request")
def test_get_staking_network_info(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "total-supply": "13170000000",
            "circulating-supply": "12000000000",
            "epoch-last-block": 16383,
            "total-staking": 5000000000000000000000000,
            "median-raw-stake": 10000000000000000000000,
        }
    )
    result = staking.get_staking_network_info(endpoint=MOCK_ENDPOINT)
    assert result["total-staking"] > 0


@patch("pyhmy.staking.rpc_request")
def test_get_super_committees(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "current": {"epoch": 100, "epos-median-stake": "50000"},
            "previous": {"epoch": 99, "epos-median-stake": "49000"},
        }
    )
    result = staking.get_super_committees(endpoint=MOCK_ENDPOINT)
    assert "current" in result
    assert "previous" in result


@patch("pyhmy.staking.rpc_request")
def test_get_total_staking(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(1000000000000000000000000)
    result = staking.get_total_staking(endpoint=MOCK_ENDPOINT)
    assert isinstance(result, int)
    assert result > 0


@patch("pyhmy.staking.rpc_request")
def test_get_raw_median_stake_snapshot(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        {
            "epos-median-stake": "50000000000000000000000",
            "max-external-slots": 80,
            "epos-slot-winners": [],
            "epos-slot-candidates": [],
        }
    )
    result = staking.get_raw_median_stake_snapshot(endpoint=MOCK_ENDPOINT)
    assert result["max-external-slots"] == 80


@patch("pyhmy.staking.rpc_request")
def test_get_delegations_by_delegator_by_block_number(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        [
            {
                "validator_address": TEST_VAL,
                "delegator_address": TEST_DEL,
                "amount": 1000000000000000000,
            }
        ]
    )
    result = staking.get_delegations_by_delegator_by_block_number(
        TEST_DEL, "latest", endpoint=MOCK_ENDPOINT
    )
    assert len(result) == 1


@patch("pyhmy.staking.rpc_request")
def test_get_all_validator_information_by_block_number(mock_rpc):
    mock_rpc.return_value = _make_rpc_response(
        [{"validator": {"address": TEST_VAL}}]
    )
    result = staking.get_all_validator_information_by_block_number(
        "latest", page=0, endpoint=MOCK_ENDPOINT
    )
    assert len(result) == 1


@patch("pyhmy.staking.rpc_request")
def test_rpc_error(mock_rpc):
    mock_rpc.side_effect = RPCError(
        "hmyv2_getAllValidatorAddresses", MOCK_ENDPOINT, "error"
    )
    with pytest.raises(RPCError):
        staking.get_all_validator_addresses(endpoint=MOCK_ENDPOINT)
