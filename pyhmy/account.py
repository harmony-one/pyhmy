"""
Interact with accounts on the Harmony blockchain
"""
from .rpc.request import rpc_request

from .rpc.exceptions import RPCError, RequestsError, RequestsTimeoutError

from .exceptions import InvalidRPCReplyError

from .blockchain import get_sharding_structure

from .bech32.bech32 import bech32_decode

from .constants import DEFAULT_ENDPOINT, DEFAULT_TIMEOUT


def is_valid_address( address ) -> bool:
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
    """
    if not address.startswith( "one1" ):
        return False
    hrp, _ = bech32_decode( address )
    if not hrp:
        return False
    return True


def get_balance(
    address,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get current account balance.

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

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#da8901d2-d237-4c3b-9d7d-10af9def05c4
    """
    method = "hmyv2_getBalance"
    params = [ address ]
    try:
        balance = rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
        return int( balance )  # v2 returns the result as it is
    except TypeError as exception:  # check will work if rpc returns None
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_balance_by_block(
    address,
    block_num,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get account balance for address at a given block number.

    Parameters
    ----------
    address: str
        Address to get balance for
    block_num: int
        Block to get balance at
    endpoint: :obj:`str`, optional
        Endpoint to send request to
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

    API Reference
    -------------
    https://api.hmny.io/#9aeae4b8-1a09-4ed2-956b-d7c96266dd33
    https://github.com/harmony-one/harmony/blob/9f320436ff30d9babd957bc5f2e15a1818c86584/rpc/blockchain.go#L92
    """
    method = "hmyv2_getBalanceByBlockNumber"
    params = [ address, block_num ]
    try:
        balance = rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
        return int( balance )
    except TypeError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_account_nonce(
    address,
    block_num = "latest",
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get the account nonce.

    Parameters
    ----------
    address: str
        Address to get transaction count for
    block_num: :obj:`int` or 'latest'
        Block to get nonce at
    endpoint: :obj:`str`, optional
        Endpoint to send request to
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

    API Reference
    -------------
    https://github.com/harmony-one/harmony/blob/9f320436ff30d9babd957bc5f2e15a1818c86584/rpc/transaction.go#L51
    """
    method = "hmyv2_getAccountNonce"
    params = [ address, block_num ]
    try:
        nonce = rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
        return int( nonce )
    except TypeError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_nonce(
    address,
    block_num = "latest",
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """See get_account_nonce."""
    return get_account_nonce( address, block_num, endpoint, timeout )


def get_transaction_count(
    address,
    block_num,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get the number of transactions the given address has sent for the given
    block number Legacy for apiv1. For apiv2, please use
    get_account_nonce/get_transactions_count/get_staking_transactions_count
    apis for more granular transaction counts queries.

    Parameters
    ----------
    address: str
        Address to get transaction count for
    block_num: :obj:`int` or 'latest'
        Block to get nonce at
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        The number of transactions the given address has sent for the given block number

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/harmony-one/harmony/blob/9f320436ff30d9babd957bc5f2e15a1818c86584/rpc/transaction.go#L69
    """
    method = "hmyv2_getTransactionCount"
    params = [ address, block_num ]
    try:
        nonce = rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
        return int( nonce )
    except TypeError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_transactions_count(
    address,
    tx_type,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get the number of regular transactions from genesis of input type.

    Parameters
    ----------
    address: str
        Address to get transaction count for
    tx_type: str
        Type of transactions to include in the count
        currently supported are 'SENT', 'RECEIVED', 'ALL'
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Count of transactions of type tx_type

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#fc97aed2-e65e-4cf4-bc01-8dadb76732c0
    https://github.com/harmony-one/harmony/blob/9f320436ff30d9babd957bc5f2e15a1818c86584/rpc/transaction.go#L114
    """
    method = "hmyv2_getTransactionsCount"
    params = [ address, tx_type ]
    try:
        tx_count = rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
        return int( tx_count )
    except TypeError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_staking_transactions_count(
    address,
    tx_type,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get the number of staking transactions from genesis of input type
    ("SENT", "RECEIVED", "ALL")

    Parameters
    ----------
    address: str
        Address to get staking transaction count for
    tx_type: str
        Type of staking transactions to include in the count
        currently supported are 'SENT', 'RECEIVED', 'ALL'
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Count of staking transactions of type tx_type

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#ddc1b029-f341-4c4d-ba19-74b528d6e5e5
    https://github.com/harmony-one/harmony/blob/9f320436ff30d9babd957bc5f2e15a1818c86584/rpc/transaction.go#L134
    """
    method = "hmyv2_getStakingTransactionsCount"
    params = [ address, tx_type ]
    try:
        tx_count = rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
        return int( tx_count )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_transaction_history( # pylint: disable=too-many-arguments
    address,
    page=0,
    page_size=1000,
    include_full_tx=False,
    tx_type="ALL",
    order="ASC",
    endpoint=DEFAULT_ENDPOINT,
    timeout=DEFAULT_TIMEOUT,
) -> list:
    """Get list of transactions sent and/or received by the account.

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
        'ASC' to sort transactions in ascending order based on timestamp (oldest first)
        'DESC' to sort transactions in descending order based on timestamp (newest first)
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list of transactions
    if include_full_tx is True, each transaction is a dictionary with the following keys
        see transaction/get_transaction_by_hash for a description
    if include_full_tx is False, each element represents the transaction hash

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#2200a088-81b5-4420-a291-312a7c6d880e
    https://github.com/harmony-one/harmony/blob/9f320436ff30d9babd957bc5f2e15a1818c86584/rpc/transaction.go#L255
    """
    params = [
        {
            "address": address,
            "pageIndex": page,
            "pageSize": page_size,
            "fullTx": include_full_tx,
            "txType": tx_type,
            "order": order,
        }
    ]
    method = "hmyv2_getTransactionsHistory"
    try:
        tx_history = rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )
        return tx_history[ "result" ][ "transactions" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_staking_transaction_history( # pylint: disable=too-many-arguments
    address,
    page=0,
    page_size=1000,
    include_full_tx=False,
    tx_type="ALL",
    order="ASC",
    endpoint=DEFAULT_ENDPOINT,
    timeout=DEFAULT_TIMEOUT,
) -> list:
    """Get list of staking transactions sent by the account.

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
    list of transactions
    if include_full_tx is True, each transaction is a dictionary with the following kets
        blockHash: :obj:`str` Block hash that transaction was finalized or
            "0x0000000000000000000000000000000000000000000000000000000000000000" if tx is pending
        blockNumber: :obj:`int` Block number that transaction was finalized; None if tx is pending
        from: :obj:`str` Wallet address
        timestamp: :obj:`int` Timestamp in Unix time when transaction was finalized
        gas: :obj:`int` Gas limit in Atto
        gasPrice :obj:`int` Gas price in Atto
        hash: :obj:`str` Transaction hash
        nonce: :obj:`int` Wallet nonce for the transaction
        transactionIndex: :obj:`int` Index of transaction in block; None if tx is pending
        type: :obj:`str` Type of staking transaction
            for example, "CollectRewards", "Delegate", "Undelegate"
        msg: :obj:`dict` Message attached to the staking transaction
        r: :obj:`str` First 32 bytes of the transaction signature
        s: :obj:`str` Next  32 bytes of the transaction signature
        v: :obj:`str` Recovery value + 27, as hex string
    if include_full_tx is False, each element represents the transaction hash

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#c5d25b36-57be-4e43-a23b-17ace350e322
    https://github.com/harmony-one/harmony/blob/9f320436ff30d9babd957bc5f2e15a1818c86584/rpc/transaction.go#L303
    """
    params = [
        {
            "address": address,
            "pageIndex": page,
            "pageSize": page_size,
            "fullTx": include_full_tx,
            "txType": tx_type,
            "order": order,
        }
    ]
    # Using v2 API, because getStakingTransactionHistory not implemented in v1
    method = "hmyv2_getStakingTransactionsHistory"
    try:
        stx_history = rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
        return stx_history[ "staking_transactions" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_balance_on_all_shards(
    address,
    skip_error = True,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> list:
    """Get current account balance in all shards & optionally report errors
    getting account balance for a shard.

    Parameters
    ----------
    address: str
        Address to get balance for
    skip_error: :obj:`bool`, optional
        True to ignore errors getting balance for shard
        False to include errors when getting balance for shard
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds per request

    Returns
    -------
    list of dictionaries, each dictionary to contain shard number and balance of that shard in ATTO
        Example reply:
        [
            {
                'shard': 0,
                'balance': 0,
            },
            ...
        ]
    """
    balances = []
    sharding_structure = get_sharding_structure(
        endpoint = endpoint,
        timeout = timeout
    )
    for shard in sharding_structure:
        try:
            balances.append(
                {
                    "shard": shard[ "shardID" ],
                    "balance": get_balance(
                        address,
                        endpoint = shard[ "http" ],
                        timeout = timeout
                    ),
                }
            )
        except ( KeyError, RPCError, RequestsError, RequestsTimeoutError ):
            if not skip_error:
                balances.append(
                    {
                        "shard": shard[ "shardID" ],
                        "balance": None
                    }
                )
    return balances


def get_total_balance(
    address,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get total account balance on all shards.

    Parameters
    ----------
    address: str
        Address to get balance for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
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

    See also
    ------
    get_balance_on_all_shards
    """
    try:
        balances = get_balance_on_all_shards(
            address,
            skip_error = False,
            endpoint = endpoint,
            timeout = timeout
        )
        return sum( b[ "balance" ] for b in balances )
    except TypeError as exception:
        raise RuntimeError from exception
