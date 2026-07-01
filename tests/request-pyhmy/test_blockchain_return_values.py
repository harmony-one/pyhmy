from pyhmy import blockchain


def test_get_total_supply_returns_rpc_result( monkeypatch ):
    expected = "15260238647.49999999480981481"

    def mock_rpc_request( method, endpoint = None, timeout = None ):
        assert method == "hmyv2_getTotalSupply"
        return { "result": expected }

    monkeypatch.setattr( blockchain, "rpc_request", mock_rpc_request )

    assert blockchain.get_total_supply() == expected
