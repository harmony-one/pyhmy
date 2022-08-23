import os
import shutil
from pathlib import Path

import pytest

from pyhmy import cli

TEMP_DIR = "/tmp/pyhmy-testing/test-cli"
BINARY_FILE_PATH = f"{TEMP_DIR}/bin/cli_test_binary"


@pytest.fixture(scope="session", autouse=True)
def setup():
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR, exist_ok=True)


def test_download_cli():
    env = cli.download(BINARY_FILE_PATH, replace=False, verbose=False)
    cli.environment.update(env)
    assert os.path.exists(BINARY_FILE_PATH)


def test_is_valid():
    bad_file_path = os.path.realpath(f"{TEMP_DIR}/test_is_valid/bad_hmy")
    shutil.rmtree(Path(bad_file_path).parent, ignore_errors=True)
    os.makedirs(Path(bad_file_path).parent, exist_ok=True)
    Path(bad_file_path).touch()
    assert os.path.exists(BINARY_FILE_PATH), "harmony cli did not download"
    assert os.path.exists(bad_file_path), "did not create bad binary"
    assert cli.is_valid_binary(BINARY_FILE_PATH)
    assert not cli.is_valid_binary(bad_file_path)


def test_bad_bin_set():
    bad_file_path = os.path.realpath(f"{TEMP_DIR}/test_bad_bin_set/hmy")
    shutil.rmtree(Path(bad_file_path).parent, ignore_errors=True)
    os.makedirs(Path(bad_file_path).parent, exist_ok=True)
    Path(bad_file_path).touch()
    is_set = cli.set_binary(bad_file_path)
    assert not is_set
    assert cli.get_binary_path() != bad_file_path


def test_bin_set():
    cli.set_binary(BINARY_FILE_PATH)
    cli_binary_path = cli.get_binary_path()
    assert os.path.realpath(cli_binary_path) == os.path.realpath(BINARY_FILE_PATH)


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
