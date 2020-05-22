from .rpc.exceptions import (
    RPCError,
    RequestsError,
    RequestsTimeoutError
)

class InvalidRPCReplyError(RuntimeError):
    """
    Exception raised when RPC call returns unexpected result
    Generally indicates Harmony API has been updated & pyhmy library needs to be updated as well
    """

    def __init__(self, method, endpoint):
        super().__init__(f'Unexpected reply for {method} from {endpoint}')
