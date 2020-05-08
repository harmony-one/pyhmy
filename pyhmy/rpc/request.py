import json

import requests

from .exceptions import (
    JSONDecodeError,
    RequestsError,
    RequestsTimeoutError,
    RPCError
)


_default_endpoint = 'http://localhost:9500'
_default_timeout = 30


def base_request(method, params=None, endpoint=_default_endpoint, timeout=_default_timeout) -> str:
    """
    Basic RPC request

    Parameters
    ---------
    method: str
        RPC Method to call
    params: :obj:`list`, optional
        Parameters for the RPC method
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    str
        Raw output from the request

    Raises
    ------
    TypeError
        If params is not a list or None
    RequestsTimeoutError
        If request timed out
    RequestsError
        If other request error occured
    """
    if params is None:
        params = []
    elif not isinstance(params, list):
        raise TypeError(f'invalid type {params.__class__}')

    try:
        payload = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        headers = {
            'Content-Type': 'application/json'
        }

        resp = requests.request('POST', endpoint, headers=headers, data=json.dumps(payload),
                                timeout=timeout, allow_redirects=True)
        return resp.content
    except requests.exceptions.Timeout as err:
        raise RequestsTimeoutError() from err
    except requests.exceptions.RequestException as err:
        raise RequestsError() from err


def rpc_request(method, params=None, endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
    """
    RPC request

    Parameters
    ---------
    method: str
        RPC Method to call
    params: :obj:`list`, optional
        Parameters for the RPC method
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict
        Returns dictionary representation of RPC response
        Example format:
        {
            "jsonrpc": "2.0",
            "id": 1,
            "result": ...
        }

    Raises
    ------
    RPCError
        If RPC response returned a blockchain error
    JSONDecodeError
        If RPC response format is not compatible with JSON

    See Also
    --------
    base_request
    """
    raw_resp = base_request(method, params, endpoint, timeout)

    try:
        resp = json.loads(raw_resp)
        if 'error' in resp:
            raise RPCError(str(resp['error']))
        return resp
    except json.decoder.JSONDecodeError as err:
        raise JSONDecodeError() from err


# TODO: Add GET requests
