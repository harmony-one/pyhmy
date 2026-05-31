"""Mock-based unit tests for util and account modules."""
import datetime
from unittest.mock import patch

import pytest

from pyhmy import util
from pyhmy.rpc.exceptions import RPCError


@patch("pyhmy.util.get_latest_header")
def test_is_active_shard_true(mock_header):
    now = datetime.datetime.now(datetime.UTC)
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S.0 +0000 UTC")
    mock_header.return_value = {"timestamp": timestamp}
    result = util.is_active_shard(
        "https://api.s0.b.hmny.io", delay_tolerance=3600
    )
    assert result is True


@patch("pyhmy.util.get_latest_header")
def test_is_active_shard_rpc_error(mock_header):
    mock_header.side_effect = RPCError(
        "hmyv2_latestHeader", "endpoint", "error"
    )
    result = util.is_active_shard("https://api.s0.b.hmny.io")
    assert result is False


def test_chain_id_to_int_string():
    assert util.chain_id_to_int("HmyMainnet") == 1
    assert util.chain_id_to_int("HmyTestnet") == 2
    assert util.chain_id_to_int("HmyLocal") == 2
    assert util.chain_id_to_int("HmyPangaea") == 3


def test_chain_id_to_int_numeric():
    assert util.chain_id_to_int(1) == 1
    assert util.chain_id_to_int(1666600000) == 1666600000


def test_chain_id_to_int_invalid():
    with pytest.raises(AssertionError):
        util.chain_id_to_int("UnknownChain")
    with pytest.raises(TypeError):
        util.chain_id_to_int([])


def test_convert_one_to_hex():
    addr = "one155jp2y76nazx8uw5sa94fr0m4s5aj8e5xm6fu3"
    hex_addr = util.convert_one_to_hex(addr)
    assert hex_addr.startswith("0x")
    assert len(hex_addr) == 42


def test_convert_hex_to_one():
    hex_addr = "0xA5241513DA9F4463F1d4874b548dFBAC29D91f34"
    one_addr = util.convert_hex_to_one(hex_addr)
    assert one_addr.startswith("one1")


def test_roundtrip_address():
    original = "one155jp2y76nazx8uw5sa94fr0m4s5aj8e5xm6fu3"
    hex_addr = util.convert_one_to_hex(original)
    back = util.convert_hex_to_one(hex_addr)
    assert original == back


def test_convert_passes_through_one_address():
    addr = "one155jp2y76nazx8uw5sa94fr0m4s5aj8e5xm6fu3"
    hex_addr = util.convert_one_to_hex(addr)
    result = util.convert_hex_to_one(hex_addr)
    assert result == addr


@pytest.mark.skip(reason="requires go installation")
def test_get_gopath():
    path = util.get_gopath()
    assert "go" in path


def test_json_load_valid():
    data = '{"key": "value"}'
    result = util.json_load(data)
    assert result["key"] == "value"


def test_json_load_invalid():
    with pytest.raises(Exception):
        util.json_load("{invalid json}")
