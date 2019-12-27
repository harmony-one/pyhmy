import pyhmy
from pyhmy.util import download_cli
from pyhmy.logging import ControlledLogger
from pyhmy import cli

if __name__ == "__main__":
    download_cli("test")
    print(cli.get_version())
    print(cli.get_binary_path())
    print(cli.get_account_keystore_path())
    print(cli.single_call("hmy keys list"))
    logger = ControlledLogger("test", "logs/")
    print(pyhmy.get_goversion())
    logger.info("test info")
    logger.debug("test debug")
    logger.error("test error")
    logger.warning("test warning")
    logger.write()

