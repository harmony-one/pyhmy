from .common import (
    default_endpoint,
    default_timeout
)
from .request import (
    rpc_request
)


def get_node_metadata(endpoint = default_endpoint, timeout = default_timeout):
    """
    Get config for the node

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
    return rpc_request('hmy_getNodeMetadata', endpoint, [], timeout)['result']


def get_sharding_structure(endpoint = default_endpoint, timeout = default_timeout):
    """
    Get network sharding structure

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list
        # TODO: Add link to reference RPC documentation
    """
    return rpc_request('hmy_getShardingStructure', endpoint, [], timeout)['result']


def get_leader_address(endpoint = default_endpoint, timeout = default_timeout):
    """
    Get current leader one address

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    str
        One address of current leader
    """
    return rpc_request('hmy_getLeader', endpoint, [], timeout)['result']


def get_latest_header(endpoint = default_endpoint, timeout = default_timeout):
    """
    Get block header of latest block

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
    return rpc_request('hmy_latestHeader', endpoint, [], timeout)['result']


def get_latest_headers(endpoint = default_endpoint, timeout = default_timeout):
    """
    Get block header of latest block for beacon chain & shard chain

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
    return rpc_request('hmy_getLatestChainHeaders', endpoint, [], timeout)['result']


def get_block_number(endpoint = default_endpoint, timeout = default_timeout):
    """
    Get current block number

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Current block number
    """
    return int(rpc_request('hmy_blockNumber', endpoint, [], timeout)['result'])


def get_current_epoch(endpoint = default_endpoint, timeout = default_timeout):
    """
    Get current epoch number

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Current epoch number
    """
    return int(rpc_request('hmy_getEpoch', endpoint, [], timeout)['result'])


def get_block_by_hash(block_hash, endpoint = default_endpoint, include_full_tx = False, timeout = default_timeout):
    """
    Get block by hash

    Parameters
    ----------
    block_hash: str
        Block hash to fetch
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    include_full_tx: :obj:`bool`, optional
        Include list of full transactions data for each block
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict
        # TODO: Add link to reference RPC documentation
    """
    params = [
        block_hash,
        include_full_tx
    ]
    return rpc_request('hmy_getBlockByHash', endpoint, params, timeout)['result']


def get_block_by_number(block_num, endpoint = default_endpoint, include_full_tx = False, timeout = default_timeout):
    """
    Get block by number

    Parameters
    ----------
    block_num: int
        Block number to fetch
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    include_full_tx: :obj:`bool`, optional
        Include list of full transactions data for each block
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict
        # TODO: Add link to reference RPC documentation
    """
    params = [
        str(hex(block_num)),
        include_full_tx
    ]
    return rpc_request('hmy_getBlockByNumber', endpoint, params, timeout)['result']


def get_blocks(start_block, end_block, endpoint = default_endpoint, include_full_tx = False,
        include_signers = False, timeout = default_timeout
    ):
    """
    Get list of blocks from a range

    Parameters
    ----------
    start_block: int
        First block to fetch (inclusive)
    end_block: int
        Last block to fetch (inclusive)
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    include_full_tx: :obj:`bool`, optional
        Include list of full transactions data for each block
    include_signers: :obj:`bool`, optional
        Include list of signers for each block
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list
        # TODO: Add link to reference RPC documentation
    """
    params = [
        str(hex(start_block)),
        str(hex(end_block)),
        {
            'withSigners': include_signers,
            'fullTx': include_full_tx,
        },
    ]
    return rpc_request('hmy_getBlocks', endpoint, params, timeout)['result']


def get_block_signers(block_num, endpoint = default_endpoint, timeout = default_timeout):
    """
    Get list of block signers

    Parameters
    ----------
    block_num: int
        Block number to get signers for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list
        List of one addresses that signed the block
    """
    params = [
        str(hex(block_num))
    ]
    return rpc_request('hmy_getBlockSigners', endpoint, params, timeout)['result']


def get_validators(epoch, endpoint = default_endpoint, timeout = default_timeout):
    """
    Get list of validators for a particular epoch

    Parameters
    ----------
    epoch: int
        Epoch to get list of validators for
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
        epoch
    ]
    return rpc_request('', endpoint, params, timeout)['result']
