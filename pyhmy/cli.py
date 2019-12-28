import subprocess
import pexpect
import os
import shutil
import re

from .util import get_bls_build_variables, get_gopath

_accounts = {}  # Internal accounts keystore, guaranteed to be up to date.
_account_keystore_path = "~/.hmy/account-keys"  # Internal path to account keystore, will match the current binary.
_binary_path = "hmy"  # Internal binary path.
_environment = os.environ.copy()  # Internal environment dict for Subprocess & Pexpect.


def _cache_account_function(fn):
    """
    Internal decorator to cache account related functions. The cached value gets
    removed as soon as the account keystore directory gets changed or edited.
    """
    cache = {}
    last_mod_hash = None

    def wrap(*args, **kwargs):
        nonlocal last_mod_hash
        key = (args, frozenset(kwargs.items()))
        mod_hash = hash(_account_keystore_path + str(os.path.getmtime(_account_keystore_path)))
        if last_mod_hash is None or mod_hash != last_mod_hash or key not in cache.keys():
            last_mod_hash = mod_hash
            cache[key] = fn(*args, **kwargs)
        return cache[key]

    return wrap


def _get_default_hmy_binary_path(file_name="hmy"):
    """
    Internal function to get the binary path by looking for the first file with
    the same name as the param in the current working directory.

    :param file_name: The file name to look for.
    """
    assert '/' not in file_name, "file name must not be a path."
    for root, dirs, files in os.walk(os.getcwd()):
        if file_name in files:
            return os.path.join(root, file_name)
    return ""


@_cache_account_function
def _get_current_accounts_keystore():
    """
    Internal function that gets the current keystore from the CLI.

    :returns A dictionary where the keys are the account names/aliases and the
             values are their 'one1...' addresses.
    """
    curr_addresses = {}
    response = single_call("hmy keys list")
    lines = response.split("\n")
    if "NAME" not in lines[0] or "ADDRESS" not in lines[0]:
        raise ValueError("Name or Address not found on first line of key list")
    if lines[1] != "":
        raise ValueError("Unknown format: No blank line between label and data")
    for line in lines[2:]:
        columns = line.split("\t")
        if len(columns) != 2:
            break  # Done iterating through all of the addresses.
        name, address = columns
        curr_addresses[name.strip()] = address
    return curr_addresses


def _set_account_keystore_path():
    """
    Internal function to set the account keystore path according to the binary.
    """
    global _account_keystore_path
    response = single_call("hmy keys location").strip()
    if not os.path.exists(response):
        os.mkdir(response)
    _account_keystore_path = response


def _sync_accounts():
    """
    Internal function that UPDATES the accounts keystore with the CLI's keystore.
    """
    _accounts.clear()
    _accounts.update(_get_current_accounts_keystore())


def get_accounts_keystore():
    """
    :returns A dictionary where the keys are the account names/aliases and the
             values are their 'one1...' addresses. The returned dictionary
             will be maintained as keys gets added and removed.
    """
    _sync_accounts()
    return _accounts


def set_binary(path):
    """
    :param path: The path of the CLI binary to use.

    Note that the exposed keystore will be updated accordingly.
    """
    global _binary_path
    assert os.path.isfile(path), f"`{path}` is not a file"
    _binary_path = path
    _set_account_keystore_path()
    _sync_accounts()


def get_binary_path():
    """
    :return: The absolute path of the CLI binary.
    """
    return os.path.abspath(_binary_path)


def get_version():
    """
    :return: The version string of the CLI binary.
    """
    proc = subprocess.Popen([_binary_path, "version"], env=_environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if not err:
        raise RuntimeError(f"Could not get version.\n"
                           f"\tGot exit code {proc.returncode}. Expected non-empty error message.")
    return err.decode().strip()


def get_account_keystore_path():
    """
    :return: The absolute path to the account keystore of the CLI binary.
    """
    return os.path.abspath(_account_keystore_path)


@_cache_account_function
def check_address(address):
    """
    :param address: A 'one1...' address.
    :return: Boolean of if the address is in the CLI's keystore.
    """
    return address in get_accounts_keystore().values()


@_cache_account_function
def get_address(name):
    """
    :param name: The alias of a key used in the CLI's keystore.
    :return: The associated 'one1...' address.
    """
    return get_accounts_keystore().get(name, None)


@_cache_account_function
def get_accounts(address):
    """
    :param address: The 'one1...' address
    :return: A list of account names associated with the param
    """
    return [acc for acc, addr in get_accounts_keystore().items() if address == addr]


def remove_account(name):
    """
    Note that this edits the keystore directly since there is currently no
    way to remove an address using the CLI.

    :param name: The alias of a key used in the CLI's keystore.
    :raises RuntimeError: If it failed to remove an account.
    """
    if not get_address(name):
        return
    keystore_path = f"{get_account_keystore_path()}/{name}"
    try:
        shutil.rmtree(keystore_path)
    except (shutil.Error, FileNotFoundError) as err:
        raise RuntimeError(f"Failed to delete dir: {keystore_path}\n"
                           f"\tException: {err}") from err
    _sync_accounts()


def remove_address(address):
    """
    :param address: The 'one1...' address to be removed.
    """
    for name in get_accounts(address):
        remove_account(name)
    _sync_accounts()


def single_call(command, timeout=60):
    """
    :param command: String of command to execute on CLI
    :param timeout: Optional timeout in seconds
    :returns: Decoded string of response from hmy CLI call
    :raises: RuntimeError if bad command
    """
    command_toks = command.split(" ")
    if re.match(".*hmy", command_toks[0]):
        command_toks = command_toks[1:]
    command_toks = [_binary_path] + command_toks
    try:
        response = subprocess.check_output(command_toks, env=_environment, timeout=timeout).decode()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
        raise RuntimeError(f"Bad CLI args: `{command}`\n "
                           f"\tException: {err}") from err
    return response


def expect_call(command, timeout=60):
    """
    :param command: String fo command to execute on CLI
    :param timeout: Optional timeout in seconds
    :return: A pexpect child program
    :raises: RuntimeError if bad command
    """
    command_toks = command.split(" ")
    if re.match(".*hmy", command_toks[0]):
        command_toks = command_toks[1:]
    try:
        proc = pexpect.spawn(f"{_binary_path}", command_toks, env=_environment, timeout=timeout)
    except (pexpect.ExceptionPexpect, pexpect.TIMEOUT) as err:
        raise RuntimeError(f"Bad CLI args: `{command}`\n "
                           f"\tException: {err}") from err
    return proc


if os.path.exists(f"{get_gopath()}/src/github.com/harmony-one/bls") \
        and os.path.exists(f"{get_gopath()}/src/github.com/harmony-one/mcl"):  # Check prevents needless import fails.
    _environment.update(get_bls_build_variables())  # Needed if using dynamically linked CLI binary.
set_binary(_get_default_hmy_binary_path())
