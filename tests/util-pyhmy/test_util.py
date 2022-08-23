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
    dec = util.json_load("1.1", parse_float=decimal.Decimal)
    assert isinstance(dec, decimal.Decimal)
    assert float(dec) == 1.1
    ref_dict = {"test": "val", "arr": [1, 2, 3]}
    loaded_dict = util.json_load(json.dumps(ref_dict))
    assert str(ref_dict) == str(loaded_dict)


def test_chain_id_to_int():
    assert util.chain_id_to_int(2) == 2
    assert util.chain_id_to_int("HmyMainnet") == 1


def test_get_gopath():
    assert isinstance(util.get_gopath(), str)


def test_get_goversion():
    assert isinstance(util.get_goversion(), str)


def test_convert_one_to_hex():
    assert (
        util.convert_one_to_hex("0xebcd16e8c1d8f493ba04e99a56474122d81a9c58")
        == "0xeBCD16e8c1D8f493bA04E99a56474122D81A9c58"
    )
    assert (
        util.convert_one_to_hex("one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9")
        == "0xeBCD16e8c1D8f493bA04E99a56474122D81A9c58"
    )


def test_convert_hex_to_one():
    assert (
        util.convert_hex_to_one("0xebcd16e8c1d8f493ba04e99a56474122d81a9c58")
        == "one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9"
    )
    assert (
        util.convert_hex_to_one("one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9")
        == "one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9"
    )


def test_get_bls_build_variables():
    assert isinstance(util.get_bls_build_variables(), dict)


def test_is_active_shard():
    assert isinstance(util.is_active_shard(""), bool)
