import json
import socket

import pytest
import requests

from pyhmy.rpc import (
    exceptions,
    request
)


@pytest.fixture(scope="session", autouse=True)
def setup():
    endpoint = 'http://localhost:9500'
    timeout = 30
    method = 'hmyv2_getNodeMetadata'
    params = []
    payload = {
        "id": "1",
        "jsonrpc": "2.0",
        "method": method,
        "params": params
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request('POST', endpoint, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
    except Exception as e:
        pytest.skip("can not connect to local blockchain", allow_module_level=True)


def test_request_connection_error():
    # Find available port
    s = socket.socket()
    s.bind(('localhost', 0))
    port = s.getsockname()[1]
    s.close()

    if port == 0:
        pytest.skip("could not find available port")
    bad_endpoint = f'http://localhost:{port}'
    bad_request = None
    try:
        bad_request = request.rpc_request('hmyv2_getNodeMetadata', endpoint=bad_endpoint)
    except Exception as e:
        assert isinstance(e, exceptions.RequestsError)
    assert bad_request is None


def test_request_rpc_error():
    error_request = None
    try:
        error_request = request.rpc_request('hmyv2_getBalance')
    except (exceptions.RequestsTimeoutError, exceptions.RequestsError) as err:
        pytest.skip("can not connect to local blockchain", allow_module_level=True)
    except Exception as e:
        assert isinstance(e, exceptions.RPCError)
    assert error_request is None


def test_rpc_request():
    endpoint = 'http://localhost:9500'
    timeout = 30
    method = 'hmyv2_getNodeMetadata'
    params = []
    payload = {
        "id": "1",
        "jsonrpc": "2.0",
        "method": method,
        "params": params
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = None
    try:
        response = requests.request('POST', endpoint, headers=headers,
                                    data=json.dumps(payload), timeout=timeout, allow_redirects=True)
    except:
        pytest.skip("can not connect to local blockchain")
    assert response is not None

    resp = None
    try:
        resp = json.loads(response.content)
    except json.decoder.JSONDecodeError as err:
        pytest.skip('unable to decode response')
    assert resp is not None

    rpc_response = None
    try:
        rpc_response = request.rpc_request(method, params, endpoint, timeout)
    except exceptions.RPCError as e:
        assert 'error' in resp

    if rpc_response is not None:
        assert rpc_response == resp
