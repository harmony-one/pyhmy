from .rpc.request import (
    rpc_request
)


_default_endpoint = 'http://localhost:9500'
_default_timeout = 30


#########################
# Transaction Pool RPCs #
#########################
def get_pending_transactions(endpoint=_default_endpoint, timeout=_default_timeout) -> list:
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
       https://api.hmny.io/#117e84f6-a0ec-444e-abe0-455701310389
    """
    method = "hmyv2_pendingTransactions" 
    return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']


def get_pool_stats(endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
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
    dict
        executable-count: Staking transaction hash
        non-executable-count: Type of staking transaction

    """
    method = "hmyv2_getPoolStats"
    return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']


def get_pending_staking_transactions(endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
    """
    Get list of pending staking transactions

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict
       https://api.hmny.io/#296cb4d0-bce2-48e3-bab9-64c3734edd27
    """
    method = "hmyv2_pendingStakingTransactions" 
    return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']


####################
# Transaction RPCs #
####################
def get_transaction_by_hash(tx_hash, endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
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
        https://api.hmny.io/#117e84f6-a0ec-444e-abe0-455701310389
        None if transaction hash not found
    """
    params = [
        tx_hash
    ]
    method = "hmyv2_getTransactionByHash"
    return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']


def get_transaction_by_block_hash_and_index(block_hash, tx_index,
        endpoint=_default_endpoint, timeout=_default_timeout
    ) -> dict:
    """
    Get transaction based on index in list of transactions in a block by block hash

    Parameters
    ----------
    block_hash: str
        Block hash for transaction
    tx_index: int
        Transaction index to fetch
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict
        https://api.hmny.io/#117e84f6-a0ec-444e-abe0-455701310389
    """
    params = [
        block_hash,
        str(hex(tx_index))
    ]
    method = "hmyv2_getTransactionByBlockHashAndIndex"
    return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']


def get_transaction_by_block_number_and_index(block_num, tx_index,
        endpoint=_default_endpoint, timeout=_default_timeout
    ) -> dict:
    """
    Get transaction based on index in list of transactions in a block by block number

    Parameters
    ----------
    block_num: int
        Block number for transaction
    tx_index: int
        Transaction index to fetch
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict
        https://api.hmny.io/#117e84f6-a0ec-444e-abe0-455701310389
    """
    params = [
        str(hex(block_num)),
        str(hex(tx_index))
    ]
    method = "hmyv2_getTransactionByBlockNumberAndIndex"
    return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']


def get_transaction_receipt(tx_receipt, endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
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
        https://api.hmny.io/#0c2799f8-bcdc-41a4-b362-c3a6a763bb5e
        None if transcation receipt hash not found
    """
    params = [
        tx_receipt
    ]
    method = "hmyv2_getTransactionReceipt"
    return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']


def get_transaction_error_sink(endpoint=_default_endpoint, timeout=_default_timeout) -> list:
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
        https://api.hmny.io/#9aedbc22-6262-44b1-8276-cd8ae19fa600
    """
    method = "hmyv2_getCurrentTransactionErrorSink"
    return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']


def send_raw_transaction(raw_tx, endpoint=_default_endpoint, timeout=_default_timeout) -> str:
    """
    Send signed transaction

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
    method = "hmyv2_sendRawTransaction"
    return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']


###############################
# CrossShard Transaction RPCs #
###############################
def get_pending_cx_receipts(endpoint=_default_endpoint, timeout=_default_timeout) -> list:
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
        https://api.hmny.io/#fe60070d-97b4-458d-9365-490b44c18851
    """
    method = "hmyv2_getPendingCXReceiptshmyv2_getPendingCXReceipts"
    return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']


def get_cx_receipt_by_hash(cx_hash, endpoint = _default_endpoint, timeout = _default_timeout) -> dict:
    """
    Get cross shard receipt by hash

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
        https://api.hmny.io/#3d6ad045-800d-4021-aeb5-30a0fbf724fe
        None if cx receipt hash not found
    """
    params = [
        cx_hash
    ]
    method = "hmyv2_getCXReceiptByHash"
    return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']


def resend_cx_receipt(cx_receipt, endpoint=_default_endpoint, timeout=_default_timeout) -> bool:
    """
    Send cross shard receipt

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
    method = "hmyv2_resendCx"
    return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']


############################
# Staking Transaction RPCs #
############################
def get_staking_transaction_by_hash(tx_hash, endpoint=_default_endpoint, timeout=_default_timeout) -> dict:
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
        https://api.hmny.io/#296cb4d0-bce2-48e3-bab9-64c3734edd27
        None if staking transaction hash not found
    """
    params = [
        tx_hash
    ]
    method = "hmyv2_getStakingTransactionByHash"
    return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']


def get_staking_transaction_by_block_hash_and_index(block_hash, tx_index,
        endpoint=_default_endpoint, timeout=_default_timeout
    ) -> dict:
    """
    Get staking transaction based on index in list of staking transactions for a block by block hash

    Parameters
    ----------
    block_hash: str
        Block hash for staking transaction
    tx_index: int
        Staking transaction index to fetch
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
    return rpc_request('hmy_getStakingTransactionByBlockHashAndIndex', params=params, endpoint=endpoint, timeout=timeout)['result']


def get_staking_transaction_by_block_number_and_index(block_num, tx_index,
        endpoint=_default_endpoint, timeout=_default_timeout
    ) -> dict:
    """
    Get staking transaction based on index in list of staking transactions for a block by block number

    Parameters
    ----------
    block_num: int
        Block number for staking transaction
    tx_index: int
        Staking transaction index to fetch
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict
        https://api.hmny.io/#296cb4d0-bce2-48e3-bab9-64c3734edd27
    """
    params = [
        block_num,
        tx_index
    ]

    method = "hmyv2_getStakingTransactionByBlockNumberAndIndex"
    return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']


def get_staking_transaction_error_sink(endpoint=_default_endpoint, timeout=_default_timeout) -> list:
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
        https://api.hmny.io/#bdd00e0f-2ba0-480e-b996-2ef13f10d75a
    """
    method = "hmyv2_getCurrentStakingErrorSink"
    return rpc_request(method, endpoint=endpoint, timeout=timeout)['result']


def send_raw_staking_transaction(raw_tx, endpoint=_default_endpoint, timeout=_default_timeout) -> str:
    """
    Send signed staking transaction

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
    method = "hmyv2_sendRawStakingTransaction"
    return rpc_request(method, params=params, endpoint=endpoint, timeout=timeout)['result']

