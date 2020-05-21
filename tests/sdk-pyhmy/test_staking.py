import pytest
import requests

from pyhmy import (
    staking
)

from pyhmy.rpc import (
    exceptions
)


explorer_endpoint = 'http://localhost:9599'
test_validator_address = 'one18tvf56zqjkjnak686lwutcp5mqfnvee35xjnhc'

def _test_staking_rpc(fn, *args, **kwargs):
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
def test_get_all_validator_addresses(setup_blockchain):
    validator_addresses = _test_staking_rpc(staking.get_all_validator_addresses)
    assert isinstance(validator_addresses, list)
    assert len(validator_addresses) > 0
    assert test_validator_address in validator_addresses

@pytest.mark.run(order=2)
def test_get_validator_information(setup_blockchain):
    info = _test_staking_rpc(staking.get_validator_information, test_validator_address)
    assert isinstance(info, dict)

@pytest.mark.run(order=3)
def test_get_all_validator_information(setup_blockchain):
    all_validator_information = _test_staking_rpc(staking.get_all_validator_information)
    assert isinstance(all_validator_information, list)
    assert len(all_validator_information) > 0

@pytest.mark.run(order=4)
def test_get_delegations_by_delegator(setup_blockchain):
    delegations = _test_staking_rpc(staking.get_delegations_by_delegator, test_validator_address)
    assert isinstance(delegations, list)
    assert len(delegations) > 0

@pytest.mark.run(order=5)
def test_get_delegations_by_validator(setup_blockchain):
    delegations = _test_staking_rpc(staking.get_delegations_by_validator, test_validator_address)
    assert isinstance(delegations, list)
    assert len(delegations) > 0

@pytest.mark.run(order=6)
def test_get_current_utility_metrics(setup_blockchain):
    metrics = _test_staking_rpc(staking.get_current_utility_metrics)
    assert isinstance(metrics, dict)

@pytest.mark.run(order=7)
def test_get_staking_network_info(setup_blockchain):
    info = _test_staking_rpc(staking.get_staking_network_info)
    assert isinstance(info, dict)

@pytest.mark.run(order=8)
def test_get_super_committees(setup_blockchain):
    committee = _test_staking_rpc(staking.get_super_committees)
    assert isinstance(committee, dict)

@pytest.mark.run(order=9)
def test_get_raw_median_stake_snapshot(setup_blockchain):
    median_stake = _test_staking_rpc(staking.get_raw_median_stake_snapshot)
    assert isinstance(median_stake, dict)

@pytest.mark.run(order=10)
def test_get_validator_information_by_block(setup_blockchain):
    # Apparently validator information not created until block after create-validator transaction is accepted, so +1 block
    info = _test_staking_rpc(staking.get_validator_information_by_block, test_validator_address, setup_blockchain + 1, endpoint=explorer_endpoint)
    assert isinstance(info, dict)

@pytest.mark.run(order=11)
def test_get_validator_information_by_block(setup_blockchain):
    # Apparently validator information not created until block after create-validator transaction is accepted, so +1 block
    info = _test_staking_rpc(staking.get_all_validator_information_by_block, setup_blockchain + 1, endpoint=explorer_endpoint)
    assert isinstance(info, list)

@pytest.mark.run(order=12)
def test_get_delegations_by_delegator_by_block(setup_blockchain):
    delegations = _test_staking_rpc(staking.get_delegations_by_delegator_by_block, test_validator_address, setup_blockchain + 1, endpoint=explorer_endpoint)
    assert isinstance(delegations, list)
