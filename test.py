import os
import pyhmy
from pyhmy.util import download_cli
from pyhmy.logging import ControlledLogger
from pyhmy import cli


def test_updated_keystore():
    cli.single_call("hmy keys add test1")
    addrs = cli.get_accounts_keystore()
    assert "test1" in addrs.keys()
    check_addr = addrs["test1"]
    accounts_list = cli.get_accounts(check_addr)
    check_acc = accounts_list[0]
    assert check_acc == "test1"
    raw_cli_keys_list_print = cli.single_call("hmy keys list", timeout=2)
    assert check_addr in raw_cli_keys_list_print
    assert check_acc in raw_cli_keys_list_print
    assert addrs[check_acc] == check_addr
    cli.remove_address(check_addr)
    assert check_addr not in addrs.values()
    assert "test1" not in addrs.keys()


def test_bin_set():
    download_cli("test", replace=False)
    new_path = os.getcwd() + "/bin/test"
    cli.set_binary(new_path)
    assert new_path == cli.get_binary_path()


def test_basic_logger():
    logger = ControlledLogger("test", "logs/")
    logger.info("test info")
    logger.debug("test debug")
    logger.error("test error")
    logger.warning("test warning")
    logger.write()
    # TODO: finish this test


if __name__ == "__main__":
    print(pyhmy.get_goversion())
    download_cli(replace=False)
    print(cli.get_version())
    print(cli.get_binary_path())
    print(cli.get_account_keystore_path())
    print(cli.single_call("hmy keys list"))

    test_bin_set()
    test_updated_keystore()
    test_basic_logger()

