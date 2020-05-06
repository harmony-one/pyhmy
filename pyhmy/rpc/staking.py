from .request import (
    default_endpoint,
    default_timeout,
    rpc_request
)

##################
# Validator RPCs #
##################
def get_all_validator_addresses(endpoint = default_endpoint, timeout = default_timeout) -> list:
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
    return rpc_request('hmy_getAllValidatorAddresses', endpoint, [], timeout)['result']


def get_validator_information(validator_addr, endpoint = default_endpoint, timeout = default_timeout) -> dict:
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
    return rpc_request('hmy_getValidatorInformation', endpoint, params, timeout)['result']


def get_all_validator_information(page = -1, endpoint = default_endpoint, timeout = default_timeout) -> list:
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
    return rpc_request('hmy_getAllValidatorInformation', endpoint, params, timeout)['result']


###################
# Delegation RPCs #
###################
def get_delegations_by_delegator(delegator_addr, endpoint = default_endpoint, timeout = default_timeout) -> list:
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
    return rpc_request('hmy_getDelegationsByDelegator', endpoint, params, timeout)['result']


def get_delegations_by_validator(validator_addr, endpoint = default_endpoint, timeout = default_timeout) -> list:
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
    return rpc_request('hmy_getDelegationsByValidator', endpoint, params, timeout)['result']


########################
# Staking Network RPCs #
########################
def get_current_utility_metrics(endpoint = default_endpoint, timeout = default_timeout) -> dict:
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
    return rpc_request('hmy_getCurrentUtilityMetrics', endpoint, [], timeout)['result']


def get_staking_network_info(endpoint = default_endpoint, timeout = default_timeout) -> dict:
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
    return rpc_request('hmy_getStakingNetworkInfo', endpoint, [], timeout)['result']


def get_super_committees(endpoint = default_endpoint, timeout = default_timeout) -> dict:
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
    return rpc_request('hmy_getSuperCommittees', endpoint, [], timeout)['result']


def get_raw_median_stake_snapshot(endpoint = default_endpoint, timeout = default_timeout) -> dict:
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
    return rpc_request('hmy_getMedianRawStakeSnapshot', endpoint, [], timeout)['result']
