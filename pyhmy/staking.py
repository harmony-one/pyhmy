from .rpc.request import (
    rpc_request
)

_default_endpoint = 'http://localhost:9500'
_default_timeout = 30

##################
# Validator RPCs #
##################
def get_all_validator_addresses(endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get list of all created validator addresses on chain

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list
        List of :obj:`str`, one addresses for all validators on chain

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#69b93657-8d3c-4d20-9c9f-e51f08c9b3f5
    """
    method = 'hmyv2_getAllValidatorAddresses'
    try:
        return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_validator_information(validator_addr, endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
    """
    Get validator information for validator address

    Parameters
    ----------
    validator_addr: str
        One address of the validator to get information for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    :obj:`dict` Dictionary with the following keys
        validator: :obj:`dict` Dictionary with the following keys
            address: :obj:`str` Address of the validator
            bls-public-keys: :obj:`list` List of associated public BLS keys
            last-epoch-in-committee: :obj:`int` Last epoch any key of the validator was elected
            min-self-delegation: :obj:`int` Amount that validator must delegate to self in ATTO
            max-total-delegation: :obj:`int` Total amount that validator will aceept delegations until, in ATTO
            rate: :obj:`str` Current commission rate
            max-rate: :obj:`str` Max commission rate a validator can charge
            max-change-rate: :obj:`str` Maximum amount the commission rate can increase in one epoch
            update-height: :obj:`int` Last block number as which validator edited their information
            name: :obj:`str` Validator name, displayed on the Staking Dashboard
            identity: :obj:`str` Validator identity, must be unique
            website: :obj:`str` Validator website, displayed on the Staking Dashboard
            security-contact: :obj:`str` Method to contact the validators
            details: :obj:`str` Validator details, displayed on the Staking Dashboard
            creation-height: :obj:`int` Block number in which the validator was created
            delegations: :obj:`list` List of delegations, see get_delegations_by_delegator for format
        metrics: :obj:`dict` BLS key earning metrics for current epoch (or None if no earnings in the current epoch)
            by-bls-key: :obj:`list` List of dictionaries, each with the following keys
                key: :obj:`dict` Dictionary with the following keys
                    bls-public-key: :obj:`str` BLS public key
                    group-percent: :obj:`str` Key voting power in shard
                    effective-stake: :obj:`str` Effective stake of key
                    raw-stake: :obj:`str` Actual stake of key
                    earning-account: :obj:`str` Validator wallet address
                    overall-percent: :obj:`str` Percent of effective stake
                    shard-id: :obj:`int` Shard ID that key is on
                earned-reward: :obj:`int` Lifetime reward key has earned
        total-delegation: :obj:`int` Total amount delegated to validator
        currently-in-committee: :obj:`bool` if key is currently elected
        epos-status: :obj:`str` Currently elected, eligible to be elected next epoch, or not eligible to be elected next epoch
        epos-winning-stake: :obj:`str` Total effective stake of the validator
        booted-status: :obj:`str` Banned status
        active-status: :obj:`str` Active or inactive
        lifetime: :obj:`dict` Lifetime statistics as following keys:
            reward-accumulated: :obj:`int` Lifetime reward accumulated by the validator
            blocks: :obj:`dict` with the following keys
                to-sign: :obj:`int` Number of blocks available in the validator to sign
                signed: :obj:`int` Number of blocks the validator has signed
            apr: :obj:`str` Approximate return rate
            epoch-apr: :obj:`list` List of APR per epoch
                epoch: :obj:`int` Epoch number
                value: :obj:`str` Calculated APR for that epoch

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#659ad999-14ca-4498-8f74-08ed347cab49
    """
    method = 'hmyv2_getValidatorInformation'
    params = [
        validator_addr
    ]
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_elected_validator_addresses(endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get list of elected validator addresses

    Parameters
    ----------
    validator_addr: str
        One address of the validator to get information for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    :obj:`list` List of wallet addresses that are currently elected

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#e90a6131-d67c-4110-96ef-b283d452632d
    """
    method = 'hmyv2_getElectedValidatorAddresses'
    try:
        return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_validators(epoch, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get validators list for a particular epoch

    Parameters
    ----------
    epoch: :obj:`int`
        epoch number
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    :obj:`dict` Dictionary with the following keys:
        shardID: :obj:`int` Shard ID of the endpoint
        validators: obj:`list` List of dictionaries
            address: obj:`str` One address of validator
            balance: :obj:`int` Balance of validator

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/harmony-one/harmony/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/staking.go#L152
    """
    method = 'hmyv2_getValidators'
    params = [
        epoch
    ]
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_validator_keys(epoch, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get validator BLS keys in the committee for a particular epoch

    Parameters
    ----------
    epoch: :obj:`int`
        epoch number
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    :obj:`list` List of public keys in the elected committee

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/harmony-one/harmony/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/staking.go#L152
    """
    method = 'hmyv2_getValidatorKeys'
    params = [
        epoch
    ]
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_validator_information_by_block_number(validator_addr, block_num, endpoint=_default_endpoint, timeout=_default_timeout):
    """
    Get validator information for validator address at a block

    Parameters
    ----------
    validator_addr: str
        One address of the validator to get information for
    block_num: int
        Block number to query validator information at
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict, see get_validator_information for structure

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/harmony-one/harmony/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/staking.go#L319
    """
    method = 'hmyv2_getValidatorInformationByBlockNumber'
    params = [
        validator_addr,
        block_num
    ]
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_all_validator_information(page=-1, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get validator information for all validators on chain

    Parameters
    ----------
    page: :obj:`int`, optional
        Page to request (-1 for all validators), page size is 100 otherwise
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list of validators, see get_validator_information for description

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#df5f1631-7397-48e8-87b4-8dd873235b9c
    """
    method = 'hmyv2_getAllValidatorInformation'
    params = [
        page
    ]
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_validator_self_delegation(address, endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get the amount self delegated by validator

    Parameters
    ----------
    address: :obj:`str`
        one address of the validator
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int, validator stake in ATTO

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/harmony-one/harmony/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/staking.go#L352
    """
    method = 'hmyv2_getValidatorSelfDelegation'
    params = [
        address
    ]
    try:
        return int(rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result'])
    except (KeyError, TypeError) as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_validator_total_delegation(address, endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get the total amount delegated t ovalidator (including self delegated)

    Parameters
    ----------
    address: :obj:`str`
        one address of the validator
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int, total validator stake in ATTO

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/harmony-one/harmony/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/staking.go#L379
    """
    method = 'hmyv2_getValidatorTotalDelegation'
    params = [
        address
    ]
    try:
        return int(rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result'])
    except (KeyError, TypeError) as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_all_validator_information_by_block_number(block_num, page=-1, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get validator information at block number for all validators on chain

    Parameters
    ----------
    block_num: int
        Block number to get validator information for
    page: :obj:`int`, optional
        Page to request (-1 for all validators), page size is 100
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list of validators, see get_validator_information for description
    note that metrics field is overwritten & will always display current epoch data

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#a229253f-ca76-4b9d-88f5-9fd96e40d583
    """
    method = 'hmyv2_getAllValidatorInformationByBlockNumber'
    params = [
        page,
        block_num
    ]
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

###################
# Delegation RPCs #
###################
def get_all_delegation_information(page=-1, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get delegation information for all delegators on chain

    Parameters
    ----------
    page: :obj:`int`, optional
        Page to request (-1 for all validators), page size is 100
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list of list of dictionaries
        each sub-list will have the same validator but different delegator
            each dictionary represents a dict, see get_delegations_by_delegator for description

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/harmony-one/harmony/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/staking.go#L413
    """
    method = 'hmyv2_getAllDelegationInformation'
    params = [
        page,
    ]
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_delegations_by_delegator(delegator_addr, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get list of delegations by a delegator

    Parameters
    ----------
    delegator_addr: :obj:`str`
        Address of the delegator
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    :obj:`list` List of delegations, each a dict with the following keys
        validator_address: :obj:`str` Validator wallet address
        delegator_address: :obj:`str` Delegator wallet address
        amount: :obj:`int` Amount delegated in ATTO
        reward: :obj:`int` Unclaimed rewards in ATTO
        Undelegations: :obj:`dict` List of pending undelegations, each a dict
            Amount: :obj:`int` Amount to be undelegated in ATTO
            Epoch: :obj:`int` Epoch number of the undelegation

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#454b032c-6072-4ecb-bf24-38b3d6d2af69
    """
    method = 'hmyv2_getDelegationsByDelegator'
    params = [
        delegator_addr
    ]
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_delegations_by_delegator_by_block_number(delegator_addr, block_num, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get list of delegations by a delegator at a specific block

    Parameters
    ----------
    delegator_addr: str
        Delegator address to get list of delegations for
    block_num: int
        Block number to query delgator information at
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list of delegations, see get_delegations_by_delegator for fields

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#8ce13bda-e768-47b9-9dbe-193aba410b0a
    """
    method = 'hmyv2_getDelegationsByDelegatorByBlockNumber'
    params = [
        delegator_addr,
        block_num
    ]
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_delegation_by_delegator_and_validator(delegator_addr, validator_address,
    endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
    """
    Get list of delegations by a delegator at a specific block

    Parameters
    ----------
    delegator_addr: str
        Delegator address to get delegation for
    validator_addr: str
        Validator address to get delegation for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    one delegation (or None if such delegation doesn't exist), see get_delegations_by_delegator for fields

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/harmony-one/harmony/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/staking.go#L605
    """
    method = 'hmyv2_getDelegationByDelegatorAndValidator'
    params = [
        delegator_addr,
        validator_address
    ]
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_available_redelegation_balance(delegator_addr, endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get amount of locked undelegated tokens

    Parameters
    ----------
    delegator_addr: str
        Delegator address to amount of locked undelegated tokens
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int, representing the amount of locked undelegated tokens in ATTO

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/harmony-one/harmony/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/staking.go#L653
    """
    method = 'hmyv2_getAvailableRedelegationBalance'
    params = [
        delegator_addr
    ]
    try:
        return int(rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result'])
    except (KeyError, TypeError) as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_delegations_by_validator(validator_addr, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get list of delegations to a validator

    Parameters
    ----------
    validator_addr: str
        Validator address to get list of delegations for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list of delegations, see get_delegations_by_delegator for fields

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#2e02d8db-8fec-41d9-a672-2c9862f63f39
    """
    method = 'hmyv2_getDelegationsByValidator'
    params = [
        validator_addr
    ]
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

########################
# Staking Network RPCs #
########################
def get_current_utility_metrics(endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
    """
    Get current utility metrics of network

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    :obj: `dict` with the following keys:
        AccumulatorSnapshot: :obj:`int` Total block reward given out in ATTO
        CurrentStakedPercentage: :obj:`str` Percent of circulating supply staked
        Deviation: :obj:`str` Change in percentage of circulating supply staked
        Adjustment: :obj:`str` Change in circulating supply staked

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#78dd2d94-9ff1-4e0c-bbac-b4eec1cdf10b
    """
    method = 'hmyv2_getCurrentUtilityMetrics'
    try:
        return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_staking_network_info(endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
    """
    Get staking network information

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    :obj: `dict` with the following keys
        total-supply: :obj:`str` Total number of pre-mined tokens
        circulating-supply: :obj:`str` Number of tokens available in the network
        epoch-last-block: :obj:`int` Last block of epoch
        total-staking: :obj:`int` Total amount staked in ATTO
        median-raw-stake: :obj:`int` Effective median stake in ATTO

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#4a10fce0-2aa4-4583-bdcb-81ee0800993b
    """
    method = 'hmyv2_getStakingNetworkInfo'
    try:
        return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_super_committees(endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
    """
    Get voting committees for current & previous epoch

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict with two keys, 'previous' and 'current', each a dict with the following keys
        quorum-deciders: :obj:`dict` dictionary with keys
            shard-X: :obj:`dict` Shard of committees, with the following keys
                committee-members: :obj:`list` List of committee members
                    bls-public-key: :obj:`str` BLS public key
                    earning-account: :obj:`str` Wallet address to which rewards are being paid
                    is-harmony-slot: :obj:`bool` if slot is Harmony owned
                    voting-power-%: :obj:`str` Normalized voting power of key
                    voting-power-unnormalized: :obj:`str` Voting power of key
                policy: :obj:`str` Current election policy
                count: :obj:`int` Number of BLS keys on shard
                external-validator-slot-count: :obj:`int` Number of external BLS keys in committee
                hmy-voting-power: :obj:`str` Voting power of harmony in percent
                staked-voting-power: :obj:`str` Voting power that is staked
                total-effective-stake: :obj:`str` Total effective stake
                total-raw-stake: :obj:`str` Total raw stake
            is-harmony-slot - Boolean : If slot is Harmony owned
            earning-account - String : Wallet address that rewards are being paid to
            bls-public-key - String : BLS public key
            voting-power-unnormalized - String : Voting power of key
            voting-power-% - String
        epoch: :obj:`int` Current / previous epoch
        epos-median-stake: :obj:`str` Effective median stake
        external-slot-count: :obj:`int` Available  committee slots

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#8eef2fc4-92db-4610-a9cd-f7b75cfbd080
    """
    method = 'hmyv2_getSuperCommittees'
    try:
        return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_total_staking(endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get total staking by validators, only meant to be called on beaconchain

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int with total staking by validators

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/harmony-one/harmony/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/staking.go#L102
    """
    method = 'hmyv2_getTotalStaking'
    try:
        return int(rpc_request(method, endpoint=endpoint, timeout=timeout)['result'])
    except (KeyError, TypeError) as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_raw_median_stake_snapshot(endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
    """
    Get median stake & additional committee data of the current epoch

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    :obj: `dict` Dictionary with the following keys
        epos-median-stake: :obj:`str` Effective median stake
        max-external-slots: :obj:`int` Number of available committee slots
        epos-slot-winners: :obj:`list` List of dictionaries, each with the following keys
            slot-owner: :obj:`str` Wallet address of BLS key
            bls-public-key: :obj:`str` BLS public key
            raw-stake: :obj:`str` Actual stake
            eposed-stake: :obj:`str` Effective stake
        epos-slot-candidates: :obj:`list` List of dictionaries, each with the following keys
            stake: :obj:`int` Actual stake in Atto
            keys-at-auction: :obj:`list` List of BLS public keys
            percentage-of-total-auction-stake: :obj:`str` Percent of total network stake
            stake-per-key: :obj:`int` Stake per BLS key in Atto
            validator: :obj:`str` Wallet address of validator

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#bef93b3f-6763-4121-9c17-f0b0d9e5cc40
    """
    method = 'hmyv2_getMedianRawStakeSnapshot'
    try:
        return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e
