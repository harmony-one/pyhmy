import pytest

from pyhmy import (
    contract
)

from pyhmy.rpc import (
    exceptions
)

explorer_endpoint = 'http://localhost:9599'
contract_tx_hash = '0xa605852dd2fa39ed42e101c17aaca9d344d352ba9b24b14b9af94ec9cb58b31f'
# deployedBytecode from json file
contract_code = '0x6080604052348015600f57600080fd5b506004361060285760003560e01c80634936cd3614602d575b600080fd5b604080516001815290519081900360200190f3fea2646970667358221220fa3fa0e8d0267831a59f4dd5edf39a513d07e98461cb06660ad28d4beda744cd64736f6c634300080f0033'
contract_address = None
fake_shard = 'http://example.com'

def _test_contract_rpc(fn, *args, **kwargs):
    if not callable(fn):
        pytest.fail(f'Invalid function: {fn}')

    try:
        response = fn(*args, **kwargs)
    except Exception as e:
        if isinstance(e, exceptions.RPCError) and 'does not exist/is not available' in str(e):
            pytest.skip(f'{str(e)}')
        elif isinstance(e, exceptions.RPCError) and 'estimateGas returned' in str(e):
            pytest.skip(f'{str(e)}')
        pytest.fail(f'Unexpected error: {e.__class__} {e}')
    return response

def test_get_contract_address_from_hash(setup_blockchain):
    global contract_address
    contract_address = _test_contract_rpc(contract.get_contract_address_from_hash, contract_tx_hash)
    assert isinstance(contract_address, str)

def test_call(setup_blockchain):
    if not contract_address:
        pytest.skip('Contract address not loaded yet')
    called = _test_contract_rpc(contract.call, contract_address, 'latest')
    assert isinstance(called, str) and called.startswith('0x')

def test_estimate_gas(setup_blockchain):
    if not contract_address:
        pytest.skip('Contract address not loaded yet')
    gas = _test_contract_rpc(contract.estimate_gas, contract_address)
    assert isinstance(gas, int)

def test_get_code(setup_blockchain):
    if not contract_address:
        pytest.skip('Contract address not loaded yet')
    code = _test_contract_rpc(contract.get_code, contract_address, 'latest')
    assert code == contract_code

def test_get_storage_at(setup_blockchain):
    if not contract_address:
        pytest.skip('Contract address not loaded yet')
    storage = _test_contract_rpc(contract.get_storage_at, contract_address, '0x0', 'latest')
    assert isinstance(storage, str) and storage.startswith('0x')

def test_errors():
    with pytest.raises(exceptions.RPCError):
        contract.get_contract_address_from_hash('', fake_shard)
    with pytest.raises(exceptions.RPCError):
        contract.call('', '', endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        contract.estimate_gas('', endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        contract.get_code('', 'latest', endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        contract.get_storage_at('', 1, 'latest', endpoint=fake_shard)
