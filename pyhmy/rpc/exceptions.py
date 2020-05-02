import json
import requests


class RPCError(RuntimeError):
    """
    Exception raised when RPC call returns an error
    """

class JSONDecodeError(json.decoder.JSONDecodeError):
    """
    Wrapper for json lib DecodeError exception
    """

class RequestsError(requests.exceptions.RequestException):
    """
    Wrapper for requests lib exceptions
    """

class RequestsTimeoutError(requests.exceptions.Timeout):
    """
    Wrapper for requests lib Timeout exceptions
    """
