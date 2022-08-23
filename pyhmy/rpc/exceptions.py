"""
RPC Specific Exceptions
"""

import requests


class RPCError( RuntimeError ):
    """Exception raised when RPC call returns an error."""
    def __init__( self, method, endpoint, error ):
        self.error = error
        super().__init__(
            f"Error in reply from {endpoint}: {method} returned {error}"
        )


class RequestsError( requests.exceptions.RequestException ):
    """Wrapper for requests lib exceptions."""
    def __init__( self, endpoint ):
        super().__init__( f"Error connecting to {endpoint}" )


class RequestsTimeoutError( requests.exceptions.Timeout ):
    """Wrapper for requests lib Timeout exceptions."""
    def __init__( self, endpoint ):
        super().__init__( f"Error connecting to {endpoint}" )
