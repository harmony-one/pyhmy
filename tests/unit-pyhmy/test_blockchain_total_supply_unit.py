import pytest

from pyhmy import blockchain
from pyhmy.exceptions import InvalidRPCReplyError


def test_get_total_supply_returns_rpc_result(monkeypatch):
    def fake_rpc_request(*_args, **_kwargs):
        return {"result": "12345.6789"}

    monkeypatch.setattr(blockchain, "rpc_request", fake_rpc_request)
    assert blockchain.get_total_supply() == "12345.6789"


def test_get_total_supply_allows_none(monkeypatch):
    def fake_rpc_request(*_args, **_kwargs):
        return {"result": None}

    monkeypatch.setattr(blockchain, "rpc_request", fake_rpc_request)
    assert blockchain.get_total_supply() is None


def test_get_total_supply_raises_on_missing_result(monkeypatch):
    def fake_rpc_request(*_args, **_kwargs):
        return {}

    monkeypatch.setattr(blockchain, "rpc_request", fake_rpc_request)
    with pytest.raises(InvalidRPCReplyError):
        blockchain.get_total_supply()
