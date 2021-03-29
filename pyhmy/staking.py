from .rpc.request import (
    rpc_request
)

from .exceptions import (
    InvalidRPCReplyError
)


_default_endpoint = 'http://localhost:9500'
_default_timeout = 30


##################
# Validator RPCs #
##################
def get_all_validator_addresses(page_num = -1, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get list of all created validator addresses on chain

    Parameters
    ----------
    page_num: int
        Page to request (page size is 100), -1 for all validators
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list
         List of wallet addresses that have created validators on the network
    """
    params = [
        page_num
    ]
    method = "hmyv2_getAllValidatorAddresses"
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_validator_information(validator_addr, endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
    """
    Get validator information for validator address

    Parameters
    ----------
    validator_addr:str
        One address of the validator to get information for 
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict
        https://api.hmny.io/#df5f1631-7397-48e8-87b4-8dd873235b9c
    """
    params = [
        validator_addr
    ]
    method = "hmyv2_getValidatorInformation"
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e
    

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
        https://api.hmny.io/#df5f1631-7397-48e8-87b4-8dd873235b9c
    """
    params = [
        validator_addr,
        block_num
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
        https://api.hmny.io/#df5f1631-7397-48e8-87b4-8dd873235b9c
    """
    params = [
        page
    ]
    method = "hmyv2_getAllValidatorInformation"
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


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
        https://api.hmny.io/#659ad999-14ca-4498-8f74-08ed347cab49
    """
    params = [
        page,
        block_num
    ]
    method = "hmyv2_getAllValidatorInformationByBlockNumber"
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_elected_validator_address(endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get elected validtor address

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list
         List of wallet addresses that are currently elected

    """
    method = "hmyv2_getElectedValidatorAddresses"
    try:
        return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


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
        https://api.hmny.io/#454b032c-6072-4ecb-bf24-38b3d6d2af69
    """
    params = [
        delegator_addr
    ]
    method = "hmyv2_getDelegationsByDelegator"
    return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']


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
        https://api.hmny.io/#454b032c-6072-4ecb-bf24-38b3d6d2af69
    """
    params = [
        delegator_addr,
        block_num
    ]
    method = "hmyv2_getDelegationsByDelegator "
    return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']


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
        https://api.hmny.io/#2e02d8db-8fec-41d9-a672-2c9862f63f39
    """
    params = [
        validator_addr
    ]
    method = "hmyv2_getDelegationsByValidator"
    return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']


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
        https://api.hmny.io/#78dd2d94-9ff1-4e0c-bbac-b4eec1cdf10b
    """
    method = "hmyv2_getCurrentUtilityMetrics"
    return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']


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
        https://api.hmny.io/#4a10fce0-2aa4-4583-bdcb-81ee0800993b
    """
    method = "hmyv2_getStakingNetworkInfo"
    return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']


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
        https://api.hmny.io/#8eef2fc4-92db-4610-a9cd-f7b75cfbd080
    """
    method = "hmyv2_getSuperCommittees"
    return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']


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
        https://api.hmny.io/#bef93b3f-6763-4121-9c17-f0b0d9e5cc40
    """
    method = "hmyv2_getMedianRawStakeSnapshot"
    return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']

