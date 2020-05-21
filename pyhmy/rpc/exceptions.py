import json
import requests


class RPCError(RuntimeError):
    """
    Exception raised when RPC call returns an error
    """

class InvalidRPCReplyError(RuntimeError):
    """
    Exception raised when RPC call returns unexpected result
    Generally indicates Harmony API has been updated & pyhmy library needs to be updated as well
    """

    def __init__(self, method, endpoint):
        self.message = f'Unexpected reply for {method} from {endpoint}'

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
