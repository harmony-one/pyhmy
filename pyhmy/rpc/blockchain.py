from .request import (
    _default_endpoint,
    _default_timeout,
    rpc_request
)


################
# Network RPCs #
################
def get_node_metadata(endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
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
    return rpc_request('hmy_getNodeMetadata', endpoint=endpoint, timeout=timeout)['result']


def get_sharding_structure(endpoint=_default_endpoint, timeout=_default_timeout) -> list:
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
    return rpc_request('hmy_getShardingStructure', endpoint=endpoint, timeout=timeout)['result']


def get_leader_address(endpoint=_default_endpoint, timeout=_default_timeout) -> str:
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
    return rpc_request('hmy_getLeader', endpoint=endpoint, timeout=timeout)['result']


def get_block_number(endpoint=_default_endpoint, timeout=_default_timeout) -> int:
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
    return int(rpc_request('hmy_blockNumber', endpoint=endpoint, timeout=timeout)['result'], 0)


def get_current_epoch(endpoint=_default_endpoint, timeout=_default_timeout) -> int:
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
    return int(rpc_request('hmy_getEpoch', endpoint=endpoint, timeout=timeout)['result'], 0)


def get_gas_price(endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get network gas price

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Network gas price
    """
    return int(rpc_request('hmy_gasPrice', endpoint=endpoint, timeout=timeout)['result'])


def get_num_peers(endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get number of peers connected to the node

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Number of connected peers
    """
    return int(rpc_request('net_peerCount', endpoint=endpoint, timeout=timeout)['result'], 0)


##############
# Block RPCs #
##############
def get_latest_header(endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
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
    return rpc_request('hmy_latestHeader', endpoint=endpoint, timeout=timeout)['result']


def get_latest_headers(endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
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
    return rpc_request('hmy_getLatestChainHeaders', endpoint=endpoint, timeout=timeout)['result']


def get_block_by_number(block_num, endpoint=_default_endpoint, include_full_tx=False, timeout=_default_timeout) -> dict:
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
    return rpc_request('hmy_getBlockByNumber', params=params, endpoint=endpoint, timeout=timeout)['result']


def get_block_by_hash(block_hash, endpoint=_default_endpoint, include_full_tx=False, timeout=_default_timeout) -> dict:
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
    return rpc_request('hmy_getBlockByHash', params=params, endpoint=endpoint, timeout=timeout)['result']


def get_block_transaction_count_by_number(block_num, endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get block by number

    Parameters
    ----------
    block_num: int
        Block number to get transaction count
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    include_full_tx: :obj:`bool`, optional
        Include list of full transactions data for each block
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Number of transactions in the block
    """
    params = [
        str(hex(block_num))
    ]
    return int(rpc_request('hmy_getBlockTransactionCountByNumber', params=params,
        endpoint=endpoint, timeout=timeout)['result'], 0
    )


def get_block_transaction_count_by_hash(block_hash, endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get block by hash

    Parameters
    ----------
    block_hash: str
        Block hash to get transaction count
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    include_full_tx: :obj:`bool`, optional
        Include list of full transactions data for each block
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Number of transactions in the block
    """
    params = [
        block_hash
    ]
    return int(rpc_request('hmy_getBlockTransactionCountByHash', params=params,
        endpoint=endpoint, timeout=timeout)['result'], 0
    )


def get_blocks(start_block, end_block, endpoint=_default_endpoint, include_full_tx=False,
        include_signers=False, timeout=_default_timeout
    ) -> list:
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
    return rpc_request('hmy_getBlocks', params=params, endpoint=endpoint, timeout=timeout)['result']


def get_block_signers(block_num, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
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
    return rpc_request('hmy_getBlockSigners', params=params, endpoint=endpoint, timeout=timeout)['result']


def get_validators(epoch, endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
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
    return rpc_request('hmy_getValidators', params=params, endpoint=endpoint, timeout=timeout)['result']
