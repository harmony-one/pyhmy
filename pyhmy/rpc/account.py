from .request import (
    default_endpoint,
    default_timeout,
    rpc_request
)


def get_balance(address, endpoint = default_endpoint, timeout = default_timeout) -> int:
    """
    Get current account balance

    Parameters
    ----------
    address: str
        Address to get balance for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Account balance in ATTO
    """
    params = [
        address,
        'latest'
    ]
    return int(rpc_request('hmy_getBalance', endpoint, params, timeout)['result'])


def get_balance_by_block(address, block_num, endpoint = default_endpoint, timeout = default_timeout) -> int:
    """
    Get account balance at time of given block

    Parameters
    ----------
    address: str
        Address to get balance for
    block_num: int
        Block number to req
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Account balance in ATTO at given block
    """
    params = [
        address,
        str(hex(block_num))
    ]
    return int(rpc_request('hmy_getBalanceByBlockNumber', endpoint, params, timeout)['result'])


def get_transaction_count(address, endpoint = default_endpoint, timeout = default_timeout) -> int:
    """
    Get number of transactions & staking transactions sent by an account

    Parameters
    ----------
    address: str
        Address to get transaction count for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Number of transaction sent by the account (account nonce)
    """
    params = [
        address,
        'latest'
    ]
    return int(rpc_request('hmy_getTransactionCount', endpoint, params, timeout)['result'])


def get_transaction_history(address, page = 0, page_size = 1000, include_full_tx = False, tx_type = 'ALL',
        order = 'ASC', endpoint = default_endpoint, timeout = default_timeout
    ) -> dict:
    """
    Get list of transactions sent and/or received by the account

    Parameters
    ----------
    address: str
        Address to get transaction history for
    page: :obj:`int`, optional
        Page to request for pagination
    page-size: :obj:`int`, optional
        Size of page for pagination
    include_full_tx: :obj:`bool`, optional
        True to include full transaction data
        False to just get the transaction hash
    tx_type: :obj:`str`, optional
        'ALL' to get all transactions send & received by the address
        'SENT' to get all transactions sent by the address
        'RECEIVED' to get all transactions received by the address
    order: :obj:`str`, optional
        'ASC' to sort transactions in ascending order based on timestamp
        'DESC' to sort transactions in descending order based on timestamp
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
        {
            'address': address,
            'pageIndex': page,
            'pageSize': page_size,
            'fullTx': include_full_tx,
            'txType': tx_type,
            'order': order
        }
    ]
    return rpc_request('hmy_getTransactionsHistory', endpoint, params, timeout)['result']


def get_staking_transaction_history(address, page = 0, page_size = 1000, include_full_tx = False, tx_type = 'ALL',
        order = 'ASC', endpoint = default_endpoint, timeout = default_timeout
    ) -> dict:
    """
    Get list of staking transactions sent by the account

    Parameters
    ----------
    address: str
        Address to get staking transaction history for
    page: :obj:`int`, optional
        Page to request for pagination
    page-size: :obj:`int`, optional
        Size of page for pagination
    include_full_tx: :obj:`bool`, optional
        True to include full staking transaction data
        False to just get the staking transaction hash
    tx_type: :obj:`str`, optional
        'ALL' to get all staking transactions
    order: :obj:`str`, optional
        'ASC' to sort transactions in ascending order based on timestamp
        'DESC' to sort transactions in descending order based on timestamp
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
        {
            'address': address,
            'pageIndex': page,
            'pageSize': page_size,
            'fullTx': include_full_tx,
            'txType': tx_type,
            'order': order
        }
    ]
    return rpc_request('hmy_getStakingTransactionsHistory', endpoint, params, timeout)['result']
