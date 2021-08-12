from .rpc.request import (
    rpc_request
)

from .transaction import (
    get_transaction_receipt
)


_default_endpoint = 'http://localhost:9500'
_default_timeout = 30


#########################
# Smart contract RPCs
#########################
def call(to, block_num, from_address=None, gas=None, gas_price=None, value=None, data=None,
        endpoint=_default_endpoint, timeout=_default_timeout) -> str:
    """
    Execute a smart contract without saving state

    Parameters
    ----------
    to: :obj:`str`
        Address of the smart contract
    block_num: :obj:`int`
        Block number to execute the contract for
    from_address: :obj:`str`, optional
        Wallet address
    gas: :obj:`str`, optional
        Gas to execute the smart contract (in hex)
    gas_price: :obj:`str`, optional
        Gas price to execute smart contract call (in hex)
    value: :obj:`str`, optional
        Value sent with the smart contract call (in hex)
    data: :obj:`str`, optional
        Hash of smart contract method and parameters
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    str
        Return value of the executed smart contract

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint, or

    API Reference
    -------------
    https://api.hmny.io/?version=latest#d34b1f82-9b29-4b68-bac7-52fa0a8884b1
    """
    params = [
        {
        'to': to,
        'from': from_address,
        'gas': gas,
        'gasPrice': gas_price,
        'value': value,
        'data': data
        },
        block_num
    ]
    method = 'hmyv2_call'
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def estimate_gas(to, from_address=None, gas=None, gas_price=None, value=None, data=None,
        endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Estimate the gas price needed for a smart contract call

    Parameters
    ----------
    to: :obj:`str`
        Address of the smart contract
    from_address: :obj:`str`, optional
        Wallet address
    gas: :obj:`str`, optional
        Gas to execute the smart contract (in hex)
    gas_price: :obj:`str`, optional
        Gas price to execute smart contract call (in hex)
    value: :obj:`str`, optional
        Value sent with the smart contract call (in hex)
    data: :obj:`str`, optional
        Hash of smart contract method and parameters
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Estimated gas price of smart contract call

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint, or

    API Reference
    -------------
    https://api.hmny.io/?version=latest#b9bbfe71-8127-4dda-b26c-ff95c4c22abd
    """
    params = [ {
        'to': to,
        'from': from_address,
        'gas': gas,
        'gasPrice': gas_price,
        'value': value,
        'data': data
    } ]
    method = 'hmyv2_estimateGas'
    try:
        return int(rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result'], 16)
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_code(address, block_num, endpoint=_default_endpoint, timeout=_default_timeout) -> str:
    """
    Get the code stored at the given address in the state for the given block number

    Parameters
    ----------
    address: :obj:`str`
        Address of the smart contract
    block_num: :obj:`int`
        Block number to get the code for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    str
        Byte code at the smart contract address for the given block

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint, or

    API Reference
    -------------
    https://api.hmny.io/?version=latest#e13e9d78-9322-4dc8-8917-f2e721a8e556
    https://github.com/harmony-one/harmony/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/contract.go#L59
    """
    params = [
        address,
        block_num
        ]
    method = 'hmyv2_getCode'
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_storage_at(address, key, block_num, endpoint=_default_endpoint, timeout=_default_timeout) -> str:
    """
    Get the storage from the state at the given address, the key and the block number

    Parameters
    ----------
    address: :obj:`str`
        Address of the smart contract
    key: :obj:`str`
        Hex representation of the storage location
    block_num: :obj:`int`
        Block number to get the code for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    str
        Data stored at the smart contract location

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint, or

    API Reference
    -------------
    https://api.hmny.io/?version=latest#fa8ac8bd-952d-4149-968c-857ca76da43f
    https://github.com/harmony-one/harmony/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/contract.go#L84
    """
    params = [
        address,
        key,
        block_num
        ]
    method = 'hmyv2_getStorageAt'
    try:
        return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

def get_contract_address_from_hash(tx_hash, endpoint=_default_endpoint, timeout=_default_timeout) -> str:
    """
    Get address of the contract which was deployed in the transaction
        represented by tx_hash

    Parameters
    ----------
    tx_hash: :obj:`str`
        Hash of the deployment transaction
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    str
        Address of the smart contract

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint, or

    API Reference
    -------------
    https://github.com/harmony-one/harmony-test/blob/master/localnet/rpc_tests/test_contract.py#L36
    """
    try:
        return get_transaction_receipt(tx_hash, endpoint, timeout)["contractAddress"]
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e
