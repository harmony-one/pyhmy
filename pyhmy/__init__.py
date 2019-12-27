import sys
import warnings
import pkg_resources

from .cli import (
    HmyCLI,
    get_environment,
)

from .util import (
    Typgpy,
    get_gopath,
    get_goversion,
    json_load
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

__version__ = pkg_resources.get_distribution("pyhmy").version
