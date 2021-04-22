import pytest
import requests
import sys

sys.path.append("../../")
from pyhmy import (
        smartcontract
)

from pyhmy.rpc import (
    exceptions
)


explorer_endpoint = 'http://localhost:9599'
endpoint_shard_one = 'http://localhost:9501'
local_test_address = 'one1zksj3evekayy90xt4psrz8h6j2v3hla4qwz4ur'
smart_contract_address = "0x08AE1abFE01aEA60a47663bCe0794eCCD5763c19"
block_number = 370000



def _test_smartcontract_rpc(fn, *args, **kwargs):
    if not callable(fn):
        pytest.fail(f'Invalid function: {fn}')

    try:
        response = fn(*args, **kwargs)
    except Exception as e:
        if isinstance(e, exceptions.RPCError) and 'does not exist/is not available' in str(e):
            pytest.skip(f'{str(e)}')
        pytest.fail(f'Unexpected error: {e.__class__} {e}')
    return response

@pytest.mark.run(order=1)
def test_call(setup_blockchain):
    result = _test_smartcontract_rpc(smartcontract.call,smart_contract_address,block_number)
    assert isinstance(result, str)
    assert len(result) > 0
