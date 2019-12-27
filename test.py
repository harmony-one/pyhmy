import pyhmy
from pyhmy.util import download_cli
from pyhmy.logging import ControlledLogger

if __name__ == "__main__":
    # download_cli("test")
    logger = ControlledLogger("test", "logs/")
    CLI = pyhmy.HmyCLI(environment=pyhmy.get_environment())
    z = pyhmy.get_goversion()

