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
fake_shard = 'http://example.com'

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
    info = _test_staking_rpc(staking.get_validator_information_by_block_number, test_validator_address, setup_blockchain + 1, endpoint=explorer_endpoint)
    assert isinstance(info, dict)

@pytest.mark.run(order=11)
def test_get_validator_information_by_block(setup_blockchain):
    # Apparently validator information not created until block after create-validator transaction is accepted, so +1 block
    info = _test_staking_rpc(staking.get_all_validator_information_by_block_number, setup_blockchain + 1, endpoint=explorer_endpoint)
    assert isinstance(info, list)

@pytest.mark.run(order=12)
def test_get_delegations_by_delegator_by_block(setup_blockchain):
    delegations = _test_staking_rpc(staking.get_delegations_by_delegator_by_block_number, test_validator_address, setup_blockchain + 1, endpoint=explorer_endpoint)
    assert isinstance(delegations, list)

@pytest.mark.run(order=13)
def test_get_elected_validator_addresses(setup_blockchain):
    validator_addresses = _test_staking_rpc(staking.get_elected_validator_addresses)
    assert isinstance(validator_addresses, list)
    assert len(validator_addresses) > 0

@pytest.mark.run(order=14)
def test_get_validators(setup_blockchain):
    validators = _test_staking_rpc(staking.get_validators, 2)
    assert isinstance(validators, dict)
    assert len(validators['validators']) > 0

@pytest.mark.run(order=15)
def test_get_validator_keys(setup_blockchain):
    validators = _test_staking_rpc(staking.get_validator_keys, 2)
    assert isinstance(validators, list)

@pytest.mark.run(order=16)
def test_get_validator_self_delegation(setup_blockchain):
    self_delegation = _test_staking_rpc(staking.get_validator_self_delegation, test_validator_address)
    assert isinstance(self_delegation, int)
    assert self_delegation > 0

@pytest.mark.run(order=17)
def test_get_validator_total_delegation(setup_blockchain):
    total_delegation = _test_staking_rpc(staking.get_validator_total_delegation, test_validator_address)
    assert isinstance(total_delegation, int)
    assert total_delegation > 0

@pytest.mark.run(order=18)
def test_get_all_delegation_information(setup_blockchain):
    delegation_information = _test_staking_rpc(staking.get_all_delegation_information, 0)
    assert isinstance(delegation_information, list)
    assert len(delegation_information) > 0

@pytest.mark.run(order=19)
def test_get_delegation_by_delegator_and_validator(setup_blockchain):
    delegation_information = _test_staking_rpc(staking.get_delegation_by_delegator_and_validator, test_validator_address, test_validator_address)
    assert isinstance(delegation_information, dict)

@pytest.mark.run(order=20)
def test_get_available_redelegation_balance(setup_blockchain):
    redelgation_balance = _test_staking_rpc(staking.get_available_redelegation_balance, test_validator_address)
    assert isinstance(redelgation_balance, int)
    assert redelgation_balance == 0

@pytest.mark.run(order=21)
def test_get_total_staking(setup_blockchain):
    total_staking = _test_staking_rpc(staking.get_total_staking)
    assert isinstance(total_staking, int)
    assert total_staking > 0

@pytest.mark.run(order=22)
def test_errors():
    with pytest.raises(exceptions.RPCError):
        staking.get_all_validator_addresses(fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_validator_information('', fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_elected_validator_addresses(fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_validators(1, fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_validator_keys(1, fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_validator_information_by_block_number('', 1, fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_all_validator_information(-1, fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_validator_self_delegation('', fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_validator_total_delegation('', fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_all_validator_information_by_block_number(1, 1, fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_all_delegation_information(1, fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_delegations_by_delegator('', fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_delegations_by_delegator_by_block_number('', 1, fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_delegation_by_delegator_and_validator('', '', fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_available_redelegation_balance('', fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_delegations_by_validator('', fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_current_utility_metrics(fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_staking_network_info(fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_super_committees(fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_total_staking(fake_shard)
    with pytest.raises(exceptions.RPCError):
        staking.get_raw_median_stake_snapshot(fake_shard)
