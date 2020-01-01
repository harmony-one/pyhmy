import json
import subprocess
import os
import stat
import sys

import requests


class Typgpy(str):
    """
    Typography constants for pretty printing.

    Note that an ENDC is needed to made the end of a 'highlighted' text segment.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
        openssl_dir = subprocess.check_output(["which", "openssl"]).decode().strip().split("\n")[0]
    except (IndexError, subprocess.CalledProcessError) as e:
        raise RuntimeError("`openssl` not found") from e
    hmy_path = f"{get_gopath()}/src/github.com/harmony-one"
    bls_dir = f"{hmy_path}/bls"
    mcl_dir = f"{hmy_path}/mcl"
    assert os.path.exists(bls_dir), f"Harmony BLS repo not found at {bls_dir}"
    assert os.path.exists(mcl_dir), f"Harmony MCL repo not found at {mcl_dir}"
    if sys.platform.startswith("darwin"):
        variables["CGO_CFLAGS"] = f"-I{bls_dir}/include -I{mcl_dir}/include -I{openssl_dir}/include"
        variables["CGO_LDFLAGS"] = f"-L{bls_dir}/lib -L{openssl_dir}/lib"
        variables["LD_LIBRARY_PATH"] = f"{bls_dir}/lib:{mcl_dir}/lib:{openssl_dir}/lib"
        variables["DYLD_FALLBACK_LIBRARY_PATH"] = variables["LD_LIBRARY_PATH"]
    else:
        variables["CGO_CFLAGS"] = f"-I{bls_dir}/include -I{mcl_dir}/include"
        variables["CGO_LDFLAGS"] = f"-L{bls_dir}/lib"
        variables["LD_LIBRARY_PATH"] = f"{bls_dir}/lib:{mcl_dir}/lib"
    return variables


def download_cli(bin_name="hmy", replace=True, verbose=True):
    """
    This function will download the statically linked CLI binary into a bin directory
    within the current working directory.

    :param bin_name: The desired filename of the binary
    :param replace: A flag to force a replacement of the binary/file.
    :param verbose: A flag to enable a report message once the binary is downloaded.
    """
    assert isinstance(bin_name, str), "binary name must be a string"
    assert bin_name, "binary name must be non-empty"
    assert '/' not in bin_name, "binary name must not be path"
    if os.path.exists(f"{os.getcwd()}/bin/{bin_name}") and not replace:
        return
    old_cwd = os.getcwd()
    os.makedirs(f"{old_cwd}/bin", exist_ok=True)
    os.chdir(f"{old_cwd}/bin")
    hmy_script_path = f"{os.getcwd()}/hmy.sh"
    with open(hmy_script_path, 'w') as f:
        f.write(requests.get("https://raw.githubusercontent.com/harmony-one/go-sdk/master/scripts/hmy.sh")
                .content.decode())
    os.chmod(hmy_script_path, os.stat(hmy_script_path).st_mode | stat.S_IEXEC)
    if os.path.exists(f"{os.getcwd()}/hmy"):
        os.rename(f"{os.getcwd()}/hmy", f"{os.getcwd()}/.hmy_temp")
    subprocess.call([hmy_script_path, '-d'])
    os.rename(f"{os.getcwd()}/hmy", f"{os.getcwd()}/{bin_name}")
    if os.path.exists(f"{os.getcwd()}/.hmy_temp"):
        os.rename(f"{os.getcwd()}/.hmy_temp", f"{os.getcwd()}/hmy")
    if verbose:
        print(f"Saved harmony binary to: {os.getcwd()}/{bin_name}")
    os.chdir(old_cwd)


def json_load(string, **kwargs):
    """
    :param string: The JSON string to load
    :returns A dictionary loaded from a JSON string to a dictionary.
    :raises The exception caused by the load (if present).

    Note that this prints the failed input should an error arise.
    """
    try:
        return json.loads(string, **kwargs)
    except Exception as e:
        print(f"{Typgpy.FAIL}Could not parse input: '{string}'{Typgpy.ENDC}")
        raise e from e
