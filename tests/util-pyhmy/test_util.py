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