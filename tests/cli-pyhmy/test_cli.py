import os

import pytest

from pyhmy import cli

BINARY_FILE_NAME = "cli_test_binary"


@pytest.fixture(scope="session", autouse=True)
def setup():
    from pyhmy.util import download_cli
    download_cli(BINARY_FILE_NAME, replace=False, verbose=True)
    assert os.path.exists(f"{os.getcwd()}/bin/{BINARY_FILE_NAME}")


@pytest.mark.run(order=0)
def test_bin_set():
    binary_path = f"{os.getcwd()}/bin/{BINARY_FILE_NAME}"
    cli.set_binary(binary_path)
    cli_binary_path = cli.get_binary_path()
    assert cli_binary_path == binary_path, f"Binary is invalid: {cli_binary_path} != {binary_path}"


def test_update_keystore():
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


