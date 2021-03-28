from .rpc.request import (
    rpc_request
)

from .rpc.exceptions import (
    RPCError,
    RequestsError,
    RequestsTimeoutError
)

from .exceptions import (
    InvalidRPCReplyError
)

from .blockchain import (
    get_sharding_structure
)

from bech32 import (
    bech32_decode
)

_default_endpoint = 'https://api.harmony.one'
_default_timeout = 30
_address_length = 42


def is_valid_address(address) -> bool:
    """
    Check if given string is valid one address
    NOTE: This function is NOT thread safe due to the C function used by the bech32 library.

    Parameters
    ----------
    address: str
        String to check if valid one address

    Returns
    -------
    bool
        Is valid address

    Example
    -------
    is_valid_address("one17wldapvva8atr3kptuwz23k3n9mwmljyucdj8r")
    """
    if not address.startswith('one1'):
        return False
    hrp, _ = bech32_decode(address)
    if not hrp:
        return False
    return True


def get_balance(address, endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get current account balance

    Parameters
    ----------
    address: str
        Address to get balance for
    endpoint: :obj:`str`, optional
        Endpoint to send request to. The endpoints for the mainnet/testnet are:
            Mainnet: https://api.harmony.one
            Testnet: https://api.s0.b.hmny.io
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Account balance in ATTO

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    Example
    -------
    get_balance("one17wldapvva8atr3kptuwz23k3n9mwmljyucdj8r", timeout=5, endpoint="https://api.s0.b.hmny.io")
    """
    method = 'hmy_getBalance'
    params = [
        address,
        'latest'
    ]
    balance = rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    try:
        return int(balance, 16)
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_balance_by_block(address, block_num, endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get account balance for address at a given block number

    Parameters
    ----------
    address: str
        Address to get balance for
    block_num: int
        Block to get balance at
    endpoint: :obj:`str`, optional
        Endpoint to send request to. The endpoints for the mainnet/testnet are:
            Mainnet: https://api.harmony.one
            Testnet: https://api.s0.b.hmny.io
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Account balance in ATTO

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    Examples
    -------
    get_balance_by_block("one17wldapvva8atr3kptuwz23k3n9mwmljyucdj8r", 10350610, endpoint="https://api.harmony.one")
    """

    method = 'hmyv2_getBalanceByBlockNumber'
    params = [
        address,
        str(hex(block_num))
    ]
    balance = rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    try:
        return balance
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_account_nonce(address, true_nonce=False, endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get the account nonce. This is a more abstract version of the get_account_transaction function that allows to get
    nonce based on pending transaction pool.

    Parameters
    ----------
    address: str
        Address to get transaction count for
    true_nonce: :obj:`bool`, optional
        True to get on-chain nonce
        False to get nonce based on pending transaction pool
    endpoint: :obj:`str`, optional
        Endpoint to send request to. The endpoints for the mainnet/testnet are:
            Mainnet: https://api.harmony.one
            Testnet: https://api.s0.b.hmny.io
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Account nonce

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    Exemples
    --------
    get_account_nonce("one17wldapvva8atr3kptuwz23k3n9mwmljyucdj8r", true_nonce=True)

    """
    method = 'hmy_getTransactionCount'
    params = [
        address,
        'latest' if true_nonce else 'pending'
    ]
    nonce = rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    try:
        return int(nonce, 16)
    except TypeError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_transaction_count(address, endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get number of transactions & staking transactions sent by an account

    Parameters
    ----------
    address: str
        Address to get transaction count for
    type: str
        Type of staking transaction (SENT, RECEIVED, ALL)
    endpoint: :obj:`str`, optional
        Endpoint to send request to. The endpoints for the mainnet/testnet are:
            Mainnet: https://api.harmony.one
            Testnet: https://api.s0.b.hmny.io
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Number of transactions sent by the account

    Examples
    --------
    get_transaction_count("one17wldapvva8atr3kptuwz23k3n9mwmljyucdj8r")

    See also
    --------
    get_account_nonce to get pending transactions as well
    """
    return get_account_nonce(address, true_nonce=True, endpoint=endpoint, timeout=timeout)


def get_transaction_history(address, page=0, page_size=1000, include_full_tx=False, tx_type='ALL',
                            order='ASC', endpoint=_default_endpoint, timeout=_default_timeout
                            ) -> list:
    """
    Get list of transactions sent and/or received by the account

    Parameters
    ----------
    address: str
        Address to get transaction history for
    page: :obj:`int`, optional
        Page to request for pagination
    page_size: :obj:`int`, optional
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
        Endpoint to send request to. The endpoints for the mainnet/testnet are:
            Mainnet: https://api.harmony.one
            Testnet: https://api.s0.b.hmny.io
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    Examples
    --------
    get_transaction_history("one190sr8pcn9hugpkmwgh3w3jhw0uunv9u9ruk94s", order='DESC', tx_type="SENT")
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
    method = 'hmy_getTransactionsHistory'
    tx_history = rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)
    try:
        return tx_history['result']['transactions']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_staking_transaction_history(address, page=0, page_size=1000, include_full_tx=False, tx_type='ALL',
                                    order='ASC', endpoint=_default_endpoint, timeout=_default_timeout
                                    ) -> list:
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
    endpoint: :obj:`str`, optional. The endpoints for the mainnet/testnet are:
            Mainnet: https://api.harmony.one
            Testnet: https://api.s0.b.hmny.io
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    Examples
    --------
    get_staking_transaction_history("one190sr8pcn9hugpkmwgh3w3jhw0uunv9u9ruk94s", order='DESC')
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
    # Using v2 API, because getStakingTransactionHistory not implemented in v1
    method = 'hmyv2_getStakingTransactionsHistory'
    stx_history = rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']
    try:
        return stx_history['staking_transactions']
    except KeyError as e:
        raise InvalidRPCReplyError(method, endpoint) from e


def get_staking_transaction_count(address, staking_type, endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get number of staking transactions sent by staking type
    @TODO The parameters are wrong and/or missing things.

    Parameters
    ----------
    address: str
        Address to get staking transaction history for
    tx_type: :obj:`str`, optional
        'ALL' to include all staking transactions

    Returns
    -------
    int
        Number of staking transactions sent by the account and by staking type

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint
    """
    params = [
        {
            'address': address,
            'staking_type': staking_type
        }
    ]
    # Using v2 API, because getStakingTransactionHistory not implemented in v1
    method = 'hmyv2_getStakingTransactionsCount'
    return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']


def get_balance_on_all_shards(address, skip_error=True, endpoint=_default_endpoint, timeout=_default_timeout) -> list:
    """
    Get current account balance in all shards & optionally report errors getting account balance for a shard

    Parameters
    ----------
    address: str
        Address to get balance for
    skip_error: :obj:`bool`, optional
        True to ignore errors getting balance for shard
        False to include errors when getting balance for shard
    endpoint: :obj:`str`, optional
        Endpoint to send request to. The endpoints for the mainnet/testnet are:
            Mainnet: https://api.harmony.one
            Testnet: https://api.s0.b.hmny.io
    timeout: :obj:`int`, optional
        Timeout in seconds per request

    Returns
    -------
    list
        Account balance per shard in ATTO
        Example reply:
        [
            {
                'shard': 0,
                'balance': 0,
            },
            ...
        ]
    Examples
    -----
    get_balance_on_all_shards("one190sr8pcn9hugpkmwgh3w3jhw0uunv9u9ruk94s", skip_error=False)
    """
    balances = []
    sharding_structure = get_sharding_structure(endpoint=endpoint, timeout=timeout)
    for shard in sharding_structure:
        try:
            balances.append({
                'shard': shard['shardID'],
                'balance': get_balance(address, endpoint=shard['http'], timeout=timeout)
            })
        except (KeyError, RPCError, RequestsError, RequestsTimeoutError):
            if not skip_error:
                balances.append({
                    'shard': shard['shardID'],
                    'balance': None
                })
    return balances


def get_total_balance(address, endpoint=_default_endpoint, timeout=_default_timeout) -> int:
    """
    Get total account balance on all shards

    Parameters
    ----------
    address: str
        Address to get balance for
    endpoint: :obj:`str`, optional
        Endpoint to send request to. The endpoints for the mainnet/testnet are:
            Mainnet: https://api.harmony.one
            Testnet: https://api.s0.b.hmny.io
    timeout: :obj:`int`, optional
        Timeout in seconds per request

    Returns
    -------
    int
        Total account balance in ATTO

    Raises
    ------
    RuntimeError
        If error occurred getting account balance for a shard

    Examples
    --------
    get_total_balance("one190sr8pcn9hugpkmwgh3w3jhw0uunv9u9ruk94s")
    """
    try:
        balances = get_balance_on_all_shards(address, skip_error=False, endpoint=endpoint, timeout=timeout)
        return sum(b['balance'] for b in balances)
    except TypeError as e:
        raise RuntimeError from e
