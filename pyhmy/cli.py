import subprocess
import pexpect
import os
import shutil
import re

from .util import get_bls_build_variables

DEFAULT_BIN_FILENAME = 'hmy'


def get_environment():
    """
    :returns All the environment variables needed to run the CLI with dynamic linking.

    Note that this assumes that the BLS & MCL repo are in the appropriate directory
    as stated here: https://github.com/harmony-one/harmony/blob/master/README.md
    """
    environment = {"HOME": os.environ.get("HOME")}
    environment.update(get_bls_build_variables())
    return environment


class HmyCLI:
    hmy_binary_path = None  # This class attr should be set by the __init__.py of this module.

    def __init__(self, environment, hmy_binary_path=None):
        """
        :param environment: Dictionary of environment variables to be used in the CLI
        :param hmy_binary_path: An optional path to the harmony binary; defaults to
                                class attribute.
        """
        if hmy_binary_path:
            assert os.path.isfile(hmy_binary_path)
            self.hmy_binary_path = hmy_binary_path.replace("./", "")
        if not self.hmy_binary_path:
            raise FileNotFoundError("Path to harmony CLI binary is not found")
        self.environment = environment
        self.version = ""
        self.keystore_path = ""
        self._addresses = {}
        self._set_version()
        self._set_keystore_path()
        self._sync_addresses()

    def __repr__(self) -> str:
        return f"<{self.version} @ {self.hmy_binary_path}>"

    def _set_version(self) -> None:
        """
        Internal method to set this instance's version according to the binary's version.
        """
        proc = subprocess.Popen([self.hmy_binary_path, "version"], env=self.environment,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if not err:
            raise RuntimeError(f"Could not get version.\n"
                               f"\tGot exit code {proc.returncode}. Expected non-empty error message.")
        self.version = err.decode().strip()

    def _set_keystore_path(self) -> None:
        """
        Internal method to set this instance's keystore path with the binary's keystore path.
        """
        response = self.single_call("hmy keys location").strip()
        if not os.path.exists(response):
            os.mkdir(response)
        self.keystore_path = response

    def _sync_addresses(self) -> None:
        """
        Internal method to sync this instance's address with the binary's keystore addresses.
        """
        response = self.single_call("hmy keys list")
        lines = response.split("\n")
        if "NAME" not in lines[0] or "ADDRESS" not in lines[0]:
            raise ValueError(f"Name or Address not found on first line of key list")
        for line in lines[1:]:
            if line:
                columns = line.split("\t")
                if len(columns) != 2:
                    raise ValueError("Unexpected format of keys list")
                name, address = columns
                self._addresses[name.strip()] = address

    def check_address(self, address) -> bool:
        """
        :param address: A 'one1...' address.
        :return: T/F If the address is in the CLI's keystore.
        """
        self._sync_addresses()
        return address in self._addresses.values()

    def get_address(self, name) -> str:
        """
        :param name: The alias of a key used in the CLI's keystore.
        :return: The associated 'one1...' address.
        """
        if name in self._addresses:
            return self._addresses[name]
        else:
            self._sync_addresses()
            return self._addresses.get(name, None)

    def get_accounts(self, address) -> list:
        """
        :param address: The 'one1...' address
        :return: A list of account names associated with
        """
        self._sync_addresses()
        return [acc for acc, addr in self._addresses.items() if address == addr]

    def remove_account(self, name) -> None:
        """
        :param name: The alias of a key used in the CLI's keystore.
        """
        if not self.get_address(name):
            return
        try:
            shutil.rmtree(f"{self.keystore_path}/{name}")
        except (shutil.Error, FileNotFoundError) as err:
            raise RuntimeError(f"Failed to delete dir: {self.keystore_path}/{name}\n"
                               f"\tException: {err}") from err
        del self._addresses[name]

    def remove_address(self, address):
        """
        :param address: The 'one1...' address to be removed.
        """
        for name in self.get_accounts(address):
            self.remove_account(name)

    def single_call(self, command, timeout=60):
        """
        :param command: String fo command to execute on CLI
        :param timeout: Optional timeout in seconds
        :returns: Decoded string of response from hmy CLI call
        :raises: RuntimeError if bad command
        """
        command_toks = command.split(" ")
        if re.match(".*hmy", command_toks[0]):
            command_toks = command_toks[1:]
        command_toks = [self.hmy_binary_path] + command_toks
        try:
            response = subprocess.check_output(command_toks, env=self.environment, timeout=timeout).decode()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
            raise RuntimeError(f"Bad arguments for CLI.\n "
                               f"\tException: {err}") from err
        return response

    def expect_call(self, command, timeout=60):
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
            proc = pexpect.spawn(f"{self.hmy_binary_path}", command_toks, env=self.environment, timeout=timeout)
        except (pexpect.ExceptionPexpect, pexpect.TIMEOUT) as err:
            raise RuntimeError(f"Bad arguments for CLI.\n "
                               f"\tException: {err}") from err
        return proc
