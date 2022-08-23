"""
`pyhmy` for interacting with the Harmony blockchain
"""
import sys
import warnings

from ._version import __version__

if sys.version_info.major < 3:
    warnings.simplefilter( "always", DeprecationWarning )
    warnings.warn(
        DeprecationWarning(
            "`pyhmy` does not support Python 2. Please use Python 3."
        )
    )
    warnings.resetwarnings()

if sys.platform.startswith( "win32" ) or sys.platform.startswith( "cygwin" ):
    warnings.simplefilter( "always", ImportWarning )
    warnings.warn(
        ImportWarning( "`pyhmy` does not work on Windows or Cygwin." )
    )
    warnings.resetwarnings()
