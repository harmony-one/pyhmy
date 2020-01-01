import decimal
import json

import pytest

from pyhmy import util


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
