"""
Basic pyhmy utils like is_shard_active
ONE address format conversion
Chain id (str) to int conversion
"""
import json
import subprocess
import os
import sys
import datetime

from eth_utils import to_checksum_address

from .blockchain import get_latest_header

from .rpc.exceptions import (
    RPCError,
    RequestsError,
    RequestsTimeoutError,
)

from .account import is_valid_address

from .bech32.bech32 import bech32_decode, bech32_encode, convertbits

class Typgpy(str):
    """Typography constants for pretty printing.

    Note that an ENDC is needed to mark the end of a 'highlighted' text
    segment.
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def chain_id_to_int(chain_id):
    """
    If chain_id is a string, converts it to int.
    If chain_id is an int, returns the int.

    Else raises TypeError
    """
    chain_ids = dict(
        Default=0,
        EthMainnet=1,
        Morden=2,
        Ropsten=3,
        Rinkeby=4,
        RootstockMainnet=30,
        RootstockTestnet=31,
        Kovan=42,
        EtcMainnet=61,
        EtcTestnet=62,
        Geth=1337,
        Ganache=0,
        HmyMainnet=1,
        HmyTestnet=2,
        HmyLocal=2,
        HmyPangaea=3,
    )

    # do not validate integer chainids, only known strings
    if isinstance(chain_id, str):
        assert (
            chain_id in chain_ids
        ), f"Chain {chain_id} unknown, specify an integer chainId"
        return chain_ids.get(chain_id)
    if isinstance(chain_id, int):
        return chain_id
    raise TypeError("chainId must be str or int")


def get_gopath():
    """
    :returns The go-path, assuming that go is installed.
    """
    return subprocess.check_output(["go", "env", "GOPATH"]).decode().strip()


def get_goversion():
    """
    :returns The go-version, assuming that go is installed.
    """
    return subprocess.check_output(["go", "version"]).decode().strip()


def convert_one_to_hex(addr):
    """Given a one address, convert it to hex checksum address."""
    if not is_valid_address(addr):
        return to_checksum_address(addr)
    _, data = bech32_decode(addr)
    buf = convertbits(data, 5, 8, False)
    address = "0x" + "".join(f"{x:02x}" for x in buf)
    return str(to_checksum_address(address))


def convert_hex_to_one(addr):
    """Given a hex address, convert it to a one address."""
    if is_valid_address(addr):
        return addr
    checksum_addr = str(to_checksum_address(addr))
    data = bytearray.fromhex(
        checksum_addr[2:] if checksum_addr.startswith("0x") else checksum_addr
    )
    buf = convertbits(data, 8, 5)
    return str(bech32_encode("one", buf))


def is_active_shard(endpoint, delay_tolerance=60):
    """
    :param endpoint: The endpoint of the SHARD to check
    :param delay_tolerance: The time (in seconds) that the shard timestamp can be behind
    :return: If shard is active or not
    """
    try:
        curr_time = datetime.datetime.utcnow()
        latest_header = get_latest_header(endpoint=endpoint)
        time_str = latest_header["timestamp"][:19] + ".0"  # Fit time format
        timestamp = datetime.datetime.strptime(
            time_str, "%Y-%m-%d %H:%M:%S.%f"
        ).replace(tzinfo=None)
        time_delta = curr_time - timestamp
        return abs(time_delta.seconds) < delay_tolerance
    except (RPCError, RequestsError, RequestsTimeoutError):
        return False


def get_bls_build_variables():
    """
    :returns The environment variables needed to build and/or run programs that
             use the Harmony BLS & MCL repo.
    :raises RuntimeError if openssl is not found.

    Note that this assumes that the BLS & MCL repo are in the appropriate directory
    as stated here: https://github.com/harmony-one/harmony/blob/master/README.md
    """
    variables = {}
    try:
        openssl_dir = (
            subprocess.check_output(["which", "openssl"])
            .decode()
            .strip()
            .split("\n", maxsplit=1)[0]
        )
    except (IndexError, subprocess.CalledProcessError) as exception:
        raise RuntimeError("`openssl` not found") from exception
    hmy_path = f"{get_gopath()}/src/github.com/harmony-one"
    bls_dir = f"{hmy_path}/bls"
    mcl_dir = f"{hmy_path}/mcl"
    assert os.path.exists(bls_dir), f"Harmony BLS repo not found at {bls_dir}"
    assert os.path.exists(mcl_dir), f"Harmony MCL repo not found at {mcl_dir}"
    if sys.platform.startswith("darwin"):
        variables[
            "CGO_CFLAGS"
        ] = f"-I{bls_dir}/include -I{mcl_dir}/include -I{openssl_dir}/include"
        variables["CGO_LDFLAGS"] = f"-L{bls_dir}/lib -L{openssl_dir}/lib"
        variables["LD_LIBRARY_PATH"] = f"{bls_dir}/lib:{mcl_dir}/lib:{openssl_dir}/lib"
        variables["DYLD_FALLBACK_LIBRARY_PATH"] = variables["LD_LIBRARY_PATH"]
    else:
        variables["CGO_CFLAGS"] = f"-I{bls_dir}/include -I{mcl_dir}/include"
        variables["CGO_LDFLAGS"] = f"-L{bls_dir}/lib"
        variables["LD_LIBRARY_PATH"] = f"{bls_dir}/lib:{mcl_dir}/lib"
    return variables


def json_load(string, **kwargs):
    """
    :param string: The JSON string to load
    :returns A dictionary loaded from a JSON string to a dictionary.
    :raises The exception caused by the load (if present).

    Note that this prints the failed input should an error arise.
    """
    try:
        return json.loads(string, **kwargs)
    except Exception as exception:
        print(f"{Typgpy.FAIL}Could not parse input: '{string}'{Typgpy.ENDC}")
        raise exception
