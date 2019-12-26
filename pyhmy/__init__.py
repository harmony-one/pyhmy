#
# This package relies on the fact that there is a CLI binary from some path
# starting at the root of the file script importing this package.
# This package requires the pexpect package: https://pypi.org/project/pexpect/ .
#

from pyhmy.cli import HmyCLI, get_environment
import os

# Find the CLI binary for HmyCLI.
for root, dirs, files in os.walk(os.path.curdir):
    if "hmy" in files:
        HmyCLI.hmy_binary_path = os.path.join(root, "hmy")
        break
