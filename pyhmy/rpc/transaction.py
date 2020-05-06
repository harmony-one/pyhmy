from .request import (
    default_endpoint,
    default_timeout,
    rpc_request
)


#########################
# Transaction Pool RPCs #
#########################
def get_pending_transactions(endpoint = default_endpoint, timeout = default_timeout) -> list:
    """
    Get list of pending transactions

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
    return rpc_request('hmy_pendingTransactions', endpoint, [], timeout)['result']


####################
# Transaction RPCs #
####################
def get_transaction_by_hash(tx_hash, endpoint = default_endpoint, timeout = default_timeout) -> dict:
    """
    Get transaction by hash

    Parameters
    ----------
    tx_hash: str
        Transaction hash to fetch
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
        tx_hash
    ]
    return rpc_request('hmy_getTransactionByHash', endpoint, params, timeout)['result']


def get_transaction_by_block_hash_and_index(block_hash, tx_index,
        endpoint = default_endpoint, timeout = default_timeout
    ) -> dict:
    """
    Get transaction based on index in list of transactions for a block by block hash

    Parameters
    ----------
    block_hash: str
        Block hash for transaction
    tx_index: int
        Transaction hash to fetch
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
        block_hash,
        str(hex(tx_index))
    ]
    return rpc_request('hmy_getTransactionByBlockHashAndIndex', endpoint, params, timeout)['result']


def get_transaction_by_block_number_and_index(block_num, tx_index,
        endpoint = default_endpoint, timeout = default_timeout
    ) -> dict:
    """
    Get transaction based on index in list of transactions for a block by block number

    Parameters
    ----------
    block_num: int
        Block number for transaction
    tx_index: int
        Transaction hash to fetch
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
        str(hex(block_num)),
        str(hex(tx_index))
    ]
    return rpc_request('hmy_getTransactionByBlockNumberAndIndex', endpoint, params, timeout)['result']


def get_transaction_receipt(tx_receipt, endpoint = default_endpoint, timeout = default_timeout) -> dict:
    """
    Get transaction receipt

    Parameters
    ----------
    tx_receipt: str
        Transaction receipt to fetch
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
        tx_receipt
    ]
    return rpc_request('hmy_getTransactionByHash', endpoint, params, timeout)['result']


def get_transaction_error_sink(endpoint = default_endpoint, timeout = default_timeout) -> list:
    """
    Get transaction error sink

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
    return rpc_request('hmy_getCurrentTransactionErrorSink', endpoint, [], timeout)['result']


def send_raw_transaction(raw_tx, endpoint = default_endpoint, timeout = default_timeout) -> str:
    """
    Send transaction

    Parameters
    ----------
    raw_tx: str
        Hex representation of signed transaction
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    str
        Transaction hash
    """
    params = [
        raw_tx
    ]
    return rpc_request('hmy_sendRawTransaction', endpoint, params, timeout)['result']


###############################
# CrossShard Transaction RPCs #
###############################
def get_pending_cx_receipts(endpoint = default_endpoint, timeout = default_timeout) -> list:
    """
    Get list of pending cross shard transactions

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
    return rpc_request('hmy_getPendingCXReceipts', endpoint, [], timeout)['result']


def get_cx_receipt_by_hash(cx_hash, endpoint = default_endpoint, timeout = default_timeout) -> dict:
    """
    Get list of pending cross shard transactions

    Parameters
    ----------
    cx_hash: str
        Hash of cross shard transaction receipt
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
        cx_hash
    ]
    return rpc_request('hmy_getCXReceiptByHash', endpoint, params, timeout)['result']


def resend_cx_receipt(cx_receipt, endpoint = default_endpoint, timeout = default_timeout) -> bool:
    """
    Get list of pending cross shard transactions

    Parameters
    ----------
    cx_hash: str
        Hash of cross shard transaction receipt
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    bool
        If the receipt transactions was succesfully resent
    """
    params = [
        cx_receipt
    ]
    return rpc_request('hmy_resendCx', endpoint, params, timeout)['result']


############################
# Staking Transaction RPCs #
############################
def get_staking_transaction_by_hash(tx_hash, endpoint = default_endpoint, timeout = default_timeout) -> dict:
    """
    Get staking transaction by hash

    Parameters
    ----------
    tx_hash: str
        Hash of staking transaction to fetch
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict
        # TODO: Add link to reference RPC documentation
    """
    return rpc_request('hmy_getStakingTransactionByHash', endpoint, [], timeout)['result']


def get_staking_transaction_by_block_hash_and_index(block_hash, tx_index,
        endpoint = default_endpoint, timeout = default_timeout
    ) -> dict:
    """
    Get staking transaction based on index in list of staking transactions for a block by block hash

    Parameters
    ----------
    block_hash: str
        Block hash for staking transaction
    tx_index: int
        Index of staking transaction in block
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
        block_hash,
        str(hex(tx_index))
    ]
    return rpc_request('hmy_getStakingTransactionByBlockHashAndIndex', endpoint, params, timeout)['result']


def get_staking_transaction_by_block_number_and_index(block_num, tx_index,
        endpoint = default_endpoint, timeout = default_timeout
    ) -> dict:
    """
    Get staking transaction based on index in list of staking transactions for a block by block number

    Parameters
    ----------
    block_num: int
        Block number for staking transaction
    tx_index: int
        Index of staking transaction in block
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
        str(hex(block_num)),
        str(hex(tx_index))
    ]
    return rpc_request('hmy_getStakingTransactionByBlockNumberAndIndex', endpoint, params, timeout)['result']


def get_staking_transaction_error_sink(endpoint = default_endpoint, timeout = default_timeout) -> list:
    """
    Get staking transaction error sink

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
    return rpc_request('hmy_getStakingTransactionErrorSink', endpoint, [], timeout)['result']


def send_raw_staking_transaction(raw_tx, endpoint = default_endpoint, timeout = default_timeout) -> str:
    """
    Send staking transaction

    Parameters
    ----------
    raw_tx: str
        Hex representation of signed staking transaction
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    str
        Staking transaction hash
    """
    params = [
        raw_tx
    ]
    return rpc_request('hmy_sendRawStakingTransaction', endpoint, params, timeout)['result']
