import pytest

from pyhmy import (
    contract
)

from pyhmy.rpc import (
    exceptions
)

explorer_endpoint = 'http://localhost:9599'
contract_tx_hash = '0xa13414dd152173395c69a11e79dea31bf029660f747a42a53744181d05571e70'
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

@pytest.mark.run(order=1)
def test_get_contract_address_from_hash(setup_blockchain):
    global contract_address
    contract_address = _test_contract_rpc(contract.get_contract_address_from_hash, contract_tx_hash)
    assert isinstance(contract_address, str)

@pytest.mark.run(order=2)
def test_call(setup_blockchain):
    if not contract_address:
        pytest.skip('Contract address not loaded yet')
    called = _test_contract_rpc(contract.call, contract_address, 'latest')
    assert isinstance(called, str) and called.startswith('0x')

@pytest.mark.run(order=3)
def test_estimate_gas(setup_blockchain):
    if not contract_address:
        pytest.skip('Contract address not loaded yet')
    gas = _test_contract_rpc(contract.estimate_gas, contract_address)
    assert isinstance(gas, int)

@pytest.mark.run(order=4)
def test_get_code(setup_blockchain):
    if not contract_address:
        pytest.skip('Contract address not loaded yet')
    code = _test_contract_rpc(contract.get_code, contract_address, 'latest')
    assert code == '0x608060405234801561001057600080fd5b50600436106100415760003560e01c8063445df0ac146100465780638da5cb5b14610064578063fdacd576146100ae575b600080fd5b61004e6100dc565b6040518082815260200191505060405180910390f35b61006c6100e2565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6100da600480360360208110156100c457600080fd5b8101908080359060200190929190505050610107565b005b60015481565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141561016457806001819055505b5056fea265627a7a723158209b80813a158b44af65aee232b44c0ac06472c48f4abbe298852a39f0ff34a9f264736f6c63430005100032'

@pytest.mark.run(order=5)
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
