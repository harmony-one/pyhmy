import sys
import warnings

from ._version import __version__


from .util import (
    Typgpy,
    get_gopath,
    get_goversion,
    get_bls_build_variables,
    download_cli,
    json_load
)

from .logging import (
    ControlledLogger
)

if sys.version_info.major < 3:
    warnings.simplefilter("always", DeprecationWarning)
    warnings.warn(
        DeprecationWarning(
            "`pyhmy` does not support Python 2. Please use Python 3."
        )
    )
    warnings.resetwarnings()

if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    warnings.simplefilter("always", ImportWarning)
    warnings.warn(
        ImportWarning(
            "`pyhmy` does not work on Windows or Cygwin."
        )
    )
    warnings.resetwarnings()
