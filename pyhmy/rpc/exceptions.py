import requests


class RPCError(RuntimeError):
    """
    Exception raised when RPC call returns an error
    """

    def __init__(self, method, endpoint, error):
        super().__init__(f'Error in reply from {endpoint}: {method} returned {error}')

class InvalidRPCReplyError(RuntimeError):
    """
    Exception raised when RPC call returns unexpected result
    Generally indicates Harmony API has been updated & pyhmy library needs to be updated as well
    """

    def __init__(self, method, endpoint):
        super().__init__(f'Unexpected reply for {method} from {endpoint}')

class RequestsError(requests.exceptions.RequestException):
    """
    Wrapper for requests lib exceptions
    """

    def __init__(self, endpoint):
        super().__init__(f'Error connecting to {endpoint}')

class RequestsTimeoutError(requests.exceptions.Timeout):
    """
    Wrapper for requests lib Timeout exceptions
    """

    def __init__(self, endpoint):
        super().__init__(f'Error connecting to {endpoint}')
