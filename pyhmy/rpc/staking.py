from .request import (
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
        List of one addresses for all validators on chain
    """
    return rpc_request('hmy_getAllValidatorAddresses', endpoint=endpoint, timeout=timeout)['result']


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
    dict
        # TODO: Add link to reference RPC documentation
    """
    params = [
        validator_addr
    ]
    return rpc_request('hmy_getValidatorInformation', params=params, endpoint=endpoint, timeout=timeout)['result']


def get_validator_information_by_block(validator_addr, block_num, endpoint=_default_endpoint, timeout=_default_timeout):
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
    list
        # TODO: Add link to reference RPC documentation
    """
    params = [
        validator_addr,
        str(hex(block_num))
    ]
    return rpc_request('hmy_getValidatorInformationByBlockNumber', params=params, endpoint=endpoint, timeout=timeout)['result']


def get_all_validator_information(page=-1, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get validator information for all validators on chain

    Parameters
    ----------
    page: :obj:`int`, optional
        Page to request (-1 for all validators)
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list
        # TODO: Add link to reference RPC documentation
    """
    params = [
        page
    ]
    return rpc_request('hmy_getAllValidatorInformation', params=params, endpoint=endpoint, timeout=timeout)['result']


def get_all_validator_information_by_block(block_num, page=-1, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get validator information at block number for all validators on chain

    Parameters
    ----------
    block_num: int
        Block number to get validator information for
    page: :obj:`int`, optional
        Page to request (-1 for all validators)
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list
        # TODO: Add link to reference RPC documentation
    """
    params = [
        page,
        str(hex(block_num))
    ]
    return rpc_request('hmy_getAllValidatorInformationByBlockNumber', params=params, endpoint=endpoint, timeout=timeout)['result']


###################
# Delegation RPCs #
###################
def get_delegations_by_delegator(delegator_addr, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get list of delegations by a delegator

    Parameters
    ----------
    delegator_addr: str
        Delegator address to get list of delegations for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list
        # TODO: Add link to reference RPC documentation
    """
    params = [
        delegator_addr
    ]
    return rpc_request('hmy_getDelegationsByDelegator', params=params, endpoint=endpoint, timeout=timeout)['result']


def get_delegations_by_delegator_by_block(delegator_addr, block_num, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
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
    list
        # TODO: Add link to reference RPC documentation
    """
    params = [
        delegator_addr,
        str(hex(block_num))
    ]
    return rpc_request('hmy_getDelegationsByDelegatorByBlockNumber', params=params, endpoint=endpoint, timeout=timeout)['result']


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
    list
        # TODO: Add link to reference RPC documentation
    """
    params = [
        validator_addr
    ]
    return rpc_request('hmy_getDelegationsByValidator', params=params, endpoint=endpoint, timeout=timeout)['result']


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
    dict
        # TODO: Add link to reference RPC documentation
    """
    return rpc_request('hmy_getCurrentUtilityMetrics', endpoint=endpoint, timeout=timeout)['result']


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
    dict
        # TODO: Add link to reference RPC documentation
    """
    return rpc_request('hmy_getStakingNetworkInfo', endpoint=endpoint, timeout=timeout)['result']


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
    dict
        # TODO: Add link to reference RPC documentation
    """
    return rpc_request('hmy_getSuperCommittees', endpoint=endpoint, timeout=timeout)['result']


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
    dict
        # TODO: Add link to reference RPC documentation
    """
    return rpc_request('hmy_getMedianRawStakeSnapshot', endpoint=endpoint, timeout=timeout)['result']
