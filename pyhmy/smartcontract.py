from .rpc.request import (
    rpc_request
)


_default_endpoint = 'http://localhost:9500'
_default_timeout = 30   


def call(to_address,block_num,from_address='',gas=100,gasPrice=1000, value=0, data="",endpoint=_default_endpoint, timeout=_default_timeout) -> str:
    """
    Executes a smart contract code without saving state

    Parameters
    ----------
    block_num:int
        Block number
    to_address: str
        smart contract address
    from_address: str
        Wallet address, optional
    gas: int
        Gas to execute the smart contract call, optional
    gasPrice: int
        Gas price to execute smart contract call, optional
    value: int
        Value sent with the smart contract call, optional
    data: str
        Hash of smart contract method and parameters, optional
    block_num:number
        block number
    
    Returns
    -------
    str:
        value of the executed smart contract

    """
    params = [
        {
            'to': to_address,
            'from': from_address,
            'gas': gas,
            'gasPrice': gasPrice,
            'value': value,
            'data': data
        },
        block_num
    ]
    method = 'hmyv2_call'
    response = rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)
    try:
        return response['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e

    def estimate_gas(to_address,block_num,from_address='',gas=100,gasPrice=1000, value=0, data="",endpoint=_default_endpoint, timeout=_default_timeout) -> str:
    """
    Executes a smart contract code without saving state

    Parameters
    ----------
    block_num:int
        Block number
    to_address: str
        smart contract address
    from_address: str
        Wallet address, optional
    gas: int
        Gas to execute the smart contract call, optional
    gasPrice: int
        Gas price to execute smart contract call, optional
    value: int
        Value sent with the smart contract call, optional
    data: str
    block_num:number
        block number

    Returns
    -------
    str:
        value of the executed smart contract

    """
    params = [
        {
            'to': to_address,
            'from': from_address,
            'gas': gas,
            'gasPrice': gasPrice,
            'value': value,
            'data': data
        },
        block_num
    ]
    method = 'hmyv2_estimateGas'
    try:
        return response['result']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e
