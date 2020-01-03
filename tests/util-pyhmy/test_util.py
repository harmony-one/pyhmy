import shutil
import os
import decimal
import json
import subprocess
from pathlib import Path

import pytest

from pyhmy import util

TEMP_DIR = "/tmp/pyhmy-testing/test-util"


@pytest.fixture(scope="session", autouse=True)
def setup():
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR, exist_ok=True)


def test_json_load():
    dec = util.json_load('1.1', parse_float=decimal.Decimal)
    assert isinstance(dec, decimal.Decimal)
    assert float(dec) == 1.1
    ref_dict = {
        'test': 'val',
        'arr': [
            1,
            2,
            3
        ]
    }
    loaded_dict = util.json_load(json.dumps(ref_dict))
    assert str(ref_dict) == str(loaded_dict)


def test_download_cli():
    binary_name = "test-util-binary"
    path = f"{TEMP_DIR}/test_download_cli/{binary_name}"
    shutil.rmtree(Path(path).parent, ignore_errors=True)
    os.makedirs(Path(path).parent, exist_ok=True)
    existing_hmy_path = os.path.join(Path(path).parent, "hmy")
    Path(existing_hmy_path).touch()
    existing_hmy_path_mod = os.path.getmtime(existing_hmy_path)
    assert not os.path.exists(path), "test file is already present"
    new_path = util.download_cli(path=path, replace=True, verbose=False)
    assert new_path == os.path.realpath(path)
    assert os.path.exists(new_path), "file did not download"
    assert os.path.getmtime(existing_hmy_path) == existing_hmy_path_mod
    env = os.environ.copy()
    env.update(util.get_bls_build_variables())
    proc = subprocess.Popen([new_path, "version"], env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    assert err, "CLI version is suppose to have non-empty stderr"
    version = err.decode().strip()
    assert "harmony" in version.lower(), "cli version does not have `harmony` in it. Not harmony binary?"
