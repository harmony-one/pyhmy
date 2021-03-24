from .rpc.request import (
    rpc_request
)


_default_endpoint = 'http://localhost:9500'
_default_timeout = 30   


def call(block_num,to_address,from_address,gas,gasPrice, value, data, endpoint=_default_endpoint, timeout=_default_timeout) -> str:
    """
    Executes a smart contract code without saving state

    Parameters
    ----------
    block_num:int
        Block number
    to: str
        smart contract address
    from: str
        Wallet address, optional
    gas: int
        Gas to execute the smart contract call, optional
    gasPrice: int
        Gas price to execute smart contract call, optional
    value: int
        Value sent with the smart contract call, optional
    data: str
        Hash of smart contract method and parameters, optional
    
    Returns
    -------
    str:
        value of the executed smart contract



    """