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

class InvalidValidatorError(ValueError):
    """
    Exception raised Validator does not pass sanity checks
    """

    errors = {
        1: 'Invalid ONE address',
        2: 'Field not initialized',
        3: 'Invalid field input',
        4: 'Error checking blockchain',
        5: 'Unable to import validator information from blockchain'
    }

    def __init__(self, err_code, msg):
        self.code = err_code
        self.msg = msg
        super().__init__(msg)

    def __str__(self):
        return f'[Errno {self.code}] {self.errors[self.code]}: {self.msg}'
