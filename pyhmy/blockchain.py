from .rpc.request import (
    rpc_request
)

from .exceptions import (
    InvalidRPCReplyError
)

_default_endpoint = 'http://localhost:9500'
_default_timeout = 30


################
# Network RPCs #
################
def get_shard(endpoint=_default_endpoint, timeout=_default_timeout) -> int:
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
    int
        Shard ID of node

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint
    """
    method = 'hmy_getNodeMetadata'
    try:
        return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']['shard-id']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_staking_epoch(endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get epoch number when blockchain switches to EPoS election

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Epoch at which blockchain switches to EPoS election

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint
    """
    method = 'hmy_getNodeMetadata'
    data = rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    try:
        return int(data['chain-config']['staking-epoch'])
    except (KeyError, TypeError) as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_prestaking_epoch(endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get epoch number when blockchain switches to allow staking features without election

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Epoch at which blockchain switches to allow staking features without election

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint
    """
    method = 'hmy_getNodeMetadata'
    data = rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    try:
        return int(data['chain-config']['prestaking-epoch'])
    except (KeyError, TypeError) as e:
        raise InvalidRPCReplyError(method, endpoint) from e


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
        https://api.hmny.io/#9669d49e-43c1-47d9-a3fd-e7786e5879df
    """
    return rpc_request('hmyv2_getShardingStructure', endpoint=endpoint, timeout=timeout)['result']


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
    return rpc_request('hmyv2_getLeader', endpoint=endpoint, timeout=timeout)['result']


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

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint
    """
    #update to v2
    method = 'hmyv2_blockNumber'
    try:
        return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


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

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint
    """
    #update to v2
    method = 'hmyv2_getEpoch'
    try:
        return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


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

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint
    """
    #update to v2
    method = 'hmyv2_gasPrice'
    try:
        return int(rpc_request(method, endpoint=endpoint, timeout=timeout)['result'], 16)
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


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
    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint
    """
    method = 'net_peerCount'
    try:
        return int(rpc_request(method, endpoint=endpoint, timeout=timeout)['result'], 16)
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_circulate_supply(endpoint=_default_endpoint, timeout=_default_timeout) -> int:
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
        Circulation supply of tokens in ONE

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint
    """
    #update to v2
    method = 'hmyv2_getCirculatingSupply'
    try:
        return int(rpc_request(method, endpoint=endpoint, timeout=timeout)['result'], 16)
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_last_cross_links(endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
    """
    Get last cross links

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returnss
    -------
    dict
        https://api.hmny.io/#4994cdf9-38c4-4b1d-90a8-290ddaa3040e

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint
    """
    #update to v2
    method = 'hmyv2_getLastCrossLinks'
    try:
        return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_total_supply(endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get total number of pre-mined tokens

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returnss
    -------
    int
        number of pre-mined tokens

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint
    """
    #update to v2
    method = 'hmyv2_getTotalSupply'
    try:
        return int(rpc_request(method, endpoint=endpoint, timeout=timeout)['result'],16)
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_validators(epoch, endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
    """
    Get list of validators for specific epoch number

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
        https://api.hmny.io/#4dfe91ad-71fa-4c7d-83f3-d1c86a804da5
    """
    params = [
        epoch
    ]
    #update to v2 and move from block subcategory to network subcategory
    method = 'hmyv2_getValidators'
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_validator_keys(epoch, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get list of validator public bls keys for specific epoch number

    Parameters
    ----------
    epoch: int
        Epoch to get list of validator keys for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list
        List of bls public keys in the validator committee
    """
    params = [
        epoch
    ]
    method = 'hmyv2_getValidatorKeys'
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


##############
# Node RPCs #
##############

def get_current_bad_blocks(endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Known issues with RPC not returning correctly

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds
    
    Returns
    -------
    list
        List of bad blocks in node memory
    """

    method = "hmyv2_getCurrentBadBlocks"
    try:
        return rpc_request(method,endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


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
    ------
    dict
        https://api.hmny.io/#03c39b56-8dfc-48ce-bdad-f85776dd8aec
    
    """
    method = "hmyv2_getNodeMetadata"
    try:
        return rpc_request(method,endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_protocol_version(endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get current protocol version

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds
    
    Returns
    ------
    int
    
    """
    method = "hmyv2_protocolVersion"
    try:
        return rpc_request(method,endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e  


def get_net_peer_count(endpoint=_default_endpoint, timeout=_default_timeout) -> str:
    """
    Get peer number in the net

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds
    
    Returns
    ------
    str 
        Number of peers represented as a Hex string
    
    """
    method = "net_peerCount"
    try:
        return rpc_request(method,endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e     


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
    method = "hmyv2_latestHeader"
    try:
        return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e     


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
        https://api.hmny.io/#7625493d-16bf-4611-8009-9635d063b4c0
    """
    method = "hmyv2_getLatestChainHeaders"
    try:
        return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e     


def get_header_by_number(endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
    """
    Get block headers by block number

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict
        https://api.hmny.io/#01148e4f-72bb-426d-a123-718a161eaec0
    """
    method = "hmyv2_getHeaderByNumber"
    try:
        return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e     


def get_block_by_number(block_num, include_full_tx= True, inclTx = True, inclStaking= True, endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
    """
    Get block by number

    Parameters
    ----------
    block_num: int
        Block number to fetch
    fullTx: bool
        Include full transaction data
    inclTx: bool
        Include regular transactions
    inclStaking: bool
        Include staking transactions
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict
        https://api.hmny.io/#52f8a4ce-d357-46f1-83fd-d100989a8243
    """
    params = [
        block_num,
        {
            "fullTx": include_full_tx,
            "inclTx": inclTx,
            "inclStaking": inclStaking
        }
    ]

    method = "hmyv2_getBlockByNumber"
    try:
        return rpc_request(method, params= params, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e     


def get_block_by_hash(block_hash, include_full_tx= True, inclTx = True, inclStaking= True, endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
    """
    Get block by hash

    Parameters
    ----------
    block_hash: str
        Block hash to fetch
    fullTx: bool
        Include full transaction data
    inclTx: bool
        Include regular transactions
    inclStaking: bool
        Include staking transactions
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict
        https://api.hmny.io/#52f8a4ce-d357-46f1-83fd-d100989a8243
        None if block hash is not found
    """
    params = [
        block_hash,
        {
            "fullTx": include_full_tx,
            "inclTx": inclTx,
            "inclStaking": inclStaking
        }
    ]
    method = "hmyv2_getBlockByHash"
    try:
        return rpc_request(method, params= params, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e     


def get_block_transaction_count_by_number(block_num, endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get transaction count for specific block number

    Parameters
    ----------
    block_num: int
        Block number to get transaction count for
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
        block_num
    ]
    method = "hmyv2_getBlockTransactionCountByNumber"
    try:
        return int(rpc_request('hmy_getBlockTransactionCountByNumber', params=params,
        endpoint=endpoint, timeout=timeout)['result'], 16)
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e     


def get_block_transaction_count_by_hash(block_hash, endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get transaction count for specific block hash for

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
    method = "hmyv2_getBlockTransactionCountByHash"
    try:
        return rpc_request(method, params=params,endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e     


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
        start_block,
        end_block,
        {
            'withSigners': include_signers,
            'fullTx': include_full_tx,
        },
    ]
    method = "hmy_getBlocks"
    try:
        return rpc_request(method, params=params,endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e    



def get_block_signers(start_block_num, end_block_num, withSigners = True, fullTx = True, inclStaking = True, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get list of block signers wallet for a series of blocks

    Parameters
    ----------
    start_block_num: int
        start block number to get signers for
    end_block_num: int
        end block number to get signers for
    withSigners: bool
        Include block signer wallet addresses
    fullTx： bool
        Include full transaction data
    inclStaking： bool
        Include full staking transactions
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
        start_block_num,
        end_block_num,
        {
            "fullTx": True,
            "inclTx": True,
            "inclStaking": True
        }
    ]
    method = "hmyv2_getBlockSigners"
    try:
        return rpc_request(method, params= params, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e     


def get_block_signer_keys(block_num, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get list of block signer public bls keys for specific block number

    Parameters
    ----------
    block_num: int
        Block number to get signer keys for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list
        List of bls public keys that signed the block
    """
    params = [
        block_num
    ]
    method = "hmyv2_getBlockSignersKeys"
    try:
        return rpc_request(method, params= params, endpoint=endpoint, timeout=timeout)['result']
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e     


def get_bad_blocks(endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get list of bad blocks in memory of specific node

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
    return rpc_request('hmy_getCurrentBadBlocks', endpoint=endpoint, timeout=timeout)['result']
