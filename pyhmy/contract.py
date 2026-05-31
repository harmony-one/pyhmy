"""
Basic smart contract functions on Harmony
For full ABI driven interaction, use something like web3py or brownie
"""

from .rpc.request import rpc_request

from .transaction import get_transaction_receipt, send_raw_transaction

from .exceptions import InvalidRPCReplyError

from .constants import DEFAULT_ENDPOINT, DEFAULT_TIMEOUT


#########################
# Smart contract RPCs
#########################
def call( # pylint: disable=too-many-arguments
    to_address,
    block_num,
    from_address=None,
    gas=None,
    gas_price=None,
    value=None,
    data=None,
    endpoint=DEFAULT_ENDPOINT,
    timeout=DEFAULT_TIMEOUT,
) -> str:
    """Execute a smart contract without saving state.

    Parameters
    ----------
    to_address: :obj:`str`
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
        If received unknown result from exceptionndpoint, or

    API Reference
    -------------
    https://api.hmny.io/?version=latest#d34b1f82-9b29-4b68-bac7-52fa0a8884b1
    """
    params = [
        {
            "to": to_address,
            "from": from_address,
            "gas": gas,
            "gasPrice": gas_price,
            "value": value,
            "data": data,
        },
        block_num,
    ]
    method = "hmyv2_call"
    try:
        return rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def estimate_gas( # pylint: disable=too-many-arguments
    to_address=None,
    from_address=None,
    gas=None,
    gas_price=None,
    value=None,
    data=None,
    endpoint=DEFAULT_ENDPOINT,
    timeout=DEFAULT_TIMEOUT,
) -> int:
    """Estimate the gas price needed for a smart contract call.

    Parameters
    ----------
    to_address: :obj:`str`, optional
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
        If received unknown result from exceptionndpoint, or

    API Reference
    -------------
    https://api.hmny.io/?version=latest#b9bbfe71-8127-4dda-b26c-ff95c4c22abd
    """
    params = [
        {
            "to": to_address,
            "from": from_address,
            "gas": gas,
            "gasPrice": gas_price,
            "value": value,
            "data": data,
        }
    ]
    method = "hmyv2_estimateGas"
    try:
        return int(
            rpc_request(
                method,
                params = params,
                endpoint = endpoint,
                timeout = timeout
            )[ "result" ],
            16,
        )
    except (KeyError, TypeError) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_code(
    address,
    block_num,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> str:
    """Get the code stored at the given address in the state for the given
    block number.

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
        If received unknown result from exceptionndpoint, or

    API Reference
    -------------
    https://api.hmny.io/?version=latest#e13e9d78-9322-4dc8-8917-f2e721a8e556
    https://github.com/harmony-one/harmony/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/contract.go#L59
    """
    params = [ address, block_num ]
    method = "hmyv2_getCode"
    try:
        return rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_storage_at(
    address,
    key,
    block_num,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> str:
    """Get the storage from the state at the given address, the key and the
    block number.

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
        If received unknown result from exceptionndpoint, or

    API Reference
    -------------
    https://api.hmny.io/?version=latest#fa8ac8bd-952d-4149-968c-857ca76da43f
    https://github.com/harmony-one/harmony/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/contract.go#L84
    """
    params = [ address, key, block_num ]
    method = "hmyv2_getStorageAt"
    try:
        return rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_contract_address_from_hash(
    tx_hash,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> str:
    """Get address of the contract which was deployed in the transaction
    represented by tx_hash.

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
        If received unknown result from exceptionndpoint, or
    ValueError
        If the transaction receipt has no contract address

    API Reference
    -------------
    https://github.com/harmony-one/harmony-test/blob/master/localnet/rpc_tests/test_contract.py#L36
    """
    try:
        receipt = get_transaction_receipt( tx_hash, endpoint, timeout )
        contract_addr = receipt.get( "contractAddress" )
        if not contract_addr:
            raise ValueError(
                f"Transaction {tx_hash} did not deploy a contract"
            )
        return contract_addr
    except KeyError as exception:
        raise InvalidRPCReplyError(
            "hmyv2_getTransactionReceipt",
            endpoint
        ) from exception


def deploy_contract( # pylint: disable=too-many-arguments
    bytecode,
    from_address,
    gas_limit=6721900,
    gas_price=1000000000,
    nonce=None,
    chain_id=2,
    shard_id=0,
    to_shard_id=0,
    data=None,
    endpoint=DEFAULT_ENDPOINT,
    timeout=DEFAULT_TIMEOUT,
) -> dict:
    """Deploy a smart contract and return the deployment result.

    This function constructs, signs, and sends a contract deployment
    transaction. It then waits for confirmation and returns the
    transaction receipt containing the contract address.

    Parameters
    ----------
    bytecode: :obj:`str`
        Compiled bytecode of the smart contract (hex-encoded, with 0x prefix)
    from_address: :obj:`str`
        Deployer's one address
    gas_limit: :obj:`int`, optional
        Gas limit for the deployment transaction
    gas_price: :obj:`int`, optional
        Gas price in ATTO
    nonce: :obj:`int`, optional
        Transaction nonce. If None, fetched automatically via get_account_nonce
    chain_id: :obj:`int`, optional
        Chain ID (default 2 for testnet)
    shard_id: :obj:`int`, optional
        Originating shard ID
    to_shard_id: :obj:`int`, optional
        Destination shard ID
    data: :obj:`str`, optional
        Additional constructor arguments (hex-encoded)
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict with the following keys:
        transaction_hash: :obj:`str` The hash of the deployment transaction
        contract_address: :obj:`str` The address of the deployed contract
        receipt: :obj:`dict` Full transaction receipt

    Raises
    ------
    ValueError
        If any required parameter is missing or invalid
    InvalidRPCReplyError
        If the RPC call fails
    """
    from .signing import sign_transaction
    from .transaction import send_and_confirm_raw_transaction

    tx = {
        "chainId": chain_id,
        "data": bytecode + (data or ""),
        "from": from_address,
        "gas": gas_limit,
        "gasPrice": gas_price,
        "shardID": shard_id,
        "toShardID": to_shard_id,
    }
    if nonce is not None:
        tx["nonce"] = nonce

    signed = sign_transaction(tx, None)
    tx_hash = send_and_confirm_raw_transaction(
        signed.raw_transaction.to_0x_hex(),
        endpoint=endpoint,
        timeout=timeout,
    )
    receipt = get_transaction_receipt(
        tx_hash["hash"] if isinstance(tx_hash, dict) else tx_hash,
        endpoint=endpoint,
        timeout=timeout,
    )
    return {
        "transaction_hash": receipt.get("transactionHash"),
        "contract_address": receipt.get("contractAddress"),
        "receipt": receipt,
    }


def get_logs( # pylint: disable=too-many-arguments
    from_block=None,
    to_block=None,
    address=None,
    topics=None,
    block_hash=None,
    endpoint=DEFAULT_ENDPOINT,
    timeout=DEFAULT_TIMEOUT,
) -> list:
    """Get event logs matching the given filter criteria.

    Parameters
    ----------
    from_block: :obj:`int` or :obj:`str`, optional
        Block number or tag ('latest', 'earliest', 'pending') to start from
    to_block: :obj:`int` or :obj:`str`, optional
        Block number or tag to end at
    address: :obj:`str` or :obj:`list`, optional
        Contract address(es) to filter by
    topics: :obj:`list`, optional
        Topic filters (each element can be a string or list of strings)
    block_hash: :obj:`str`, optional
        Block hash to get logs for (cannot be combined with from_block/to_block)
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list of log entries, each a dict with keys:
        address, topics, data, blockNumber, blockHash, transactionHash,
        transactionIndex, logIndex, removed

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#e7db3daf-8d4d-4e8f-8e3a-0b8d3e1f2a3b
    """
    params = []
    filter_obj = {}
    if block_hash:
        filter_obj["blockHash"] = block_hash
    else:
        if from_block is not None:
            filter_obj["fromBlock"] = (
                hex(from_block) if isinstance(from_block, int) else from_block
            )
        if to_block is not None:
            filter_obj["toBlock"] = (
                hex(to_block) if isinstance(to_block, int) else to_block
            )
    if address:
        filter_obj["address"] = address
    if topics:
        filter_obj["topics"] = topics
    params.append(filter_obj)
    method = "hmyv2_getLogs"
    try:
        return rpc_request(
            method,
            params=params,
            endpoint=endpoint,
            timeout=timeout,
        )["result"]
    except KeyError as exception:
        raise InvalidRPCReplyError(method, endpoint) from exception


def new_filter( # pylint: disable=too-many-arguments
    from_block=None,
    to_block=None,
    address=None,
    topics=None,
    endpoint=DEFAULT_ENDPOINT,
    timeout=DEFAULT_TIMEOUT,
) -> str:
    """Create a new event log filter.

    Parameters
    ----------
    from_block: :obj:`int` or :obj:`str`, optional
        Starting block for the filter
    to_block: :obj:`int` or :obj:`str`, optional
        Ending block for the filter
    address: :obj:`str` or :obj:`list`, optional
        Contract address(es) to filter
    topics: :obj:`list`, optional
        Topic filters
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    str
        Filter ID

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint
    """
    params = []
    filter_obj = {}
    if from_block is not None:
        filter_obj["fromBlock"] = (
            hex(from_block) if isinstance(from_block, int) else from_block
        )
    if to_block is not None:
        filter_obj["toBlock"] = (
            hex(to_block) if isinstance(to_block, int) else to_block
        )
    if address:
        filter_obj["address"] = address
    if topics:
        filter_obj["topics"] = topics
    params.append(filter_obj)
    method = "hmyv2_newFilter"
    try:
        return rpc_request(
            method,
            params=params,
            endpoint=endpoint,
            timeout=timeout,
        )["result"]
    except KeyError as exception:
        raise InvalidRPCReplyError(method, endpoint) from exception


def new_block_filter(
    endpoint=DEFAULT_ENDPOINT,
    timeout=DEFAULT_TIMEOUT,
) -> str:
    """Create a new block filter to track new blocks.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    str
        Filter ID

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.hmny.io/#b8a3c7d6-9e4f-4a2b-8d1c-3e5f6a7b8c9d
    """
    method = "hmyv2_newBlockFilter"
    try:
        return rpc_request(
            method,
            endpoint=endpoint,
            timeout=timeout,
        )["result"]
    except KeyError as exception:
        raise InvalidRPCReplyError(method, endpoint) from exception


def get_filter_changes(
    filter_id,
    endpoint=DEFAULT_ENDPOINT,
    timeout=DEFAULT_TIMEOUT,
) -> list:
    """Poll a filter for changes since the last poll.

    Parameters
    ----------
    filter_id: :obj:`str`
        Filter ID returned by newFilter or newBlockFilter
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list of log entries or block hashes since last poll

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint
    """
    method = "hmyv2_getFilterChanges"
    params = [filter_id]
    try:
        return rpc_request(
            method,
            params=params,
            endpoint=endpoint,
            timeout=timeout,
        )["result"]
    except KeyError as exception:
        raise InvalidRPCReplyError(method, endpoint) from exception


def uninstall_filter(
    filter_id,
    endpoint=DEFAULT_ENDPOINT,
    timeout=DEFAULT_TIMEOUT,
) -> bool:
    """Uninstall a filter.

    Parameters
    ----------
    filter_id: :obj:`str`
        Filter ID to uninstall
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    bool
        True if the filter was successfully uninstalled

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint
    """
    method = "hmyv2_uninstallFilter"
    params = [filter_id]
    try:
        return rpc_request(
            method,
            params=params,
            endpoint=endpoint,
            timeout=timeout,
        )["result"]
    except KeyError as exception:
        raise InvalidRPCReplyError(method, endpoint) from exception


def encode_abi_function(abi, fn_name, args=None):
    """Encode a function call using its ABI. This is a simplified helper.

    For full ABI encoding support, use web3 or eth_abi directly.

    Parameters
    ----------
    abi: :obj:`list`
        Full contract ABI as a list of dicts
    fn_name: :obj:`str`
        Name of the function to encode
    args: :obj:`list`, optional
        Arguments to pass to the function

    Returns
    -------
    str
        Hex-encoded function call data (with 0x prefix)

    Raises
    ------
    ValueError
        If the function is not found in the ABI or if encoding fails
    """
    try:
        from eth_abi import encode as eth_abi_encode
        from eth_utils import function_signature_to_4byte_selector
    except ImportError:
        raise ImportError(
            "eth_abi is required for ABI encoding. "
            "Install it with: pip install eth-abi"
        )

    fn_abi = None
    for item in abi:
        if item.get("name") == fn_name and item.get("type") == "function":
            fn_abi = item
            break
    if not fn_abi:
        raise ValueError(f"Function '{fn_name}' not found in ABI")

    inputs = fn_abi.get("inputs", [])
    types = [i["type"] for i in inputs]
    signature = f"{fn_name}({','.join(types)})"
    selector = function_signature_to_4byte_selector(signature)

    encoded_args = b""
    if args:
        for i, arg in enumerate(args):
            if types[i] == "address":
                from .util import convert_one_to_hex
                args[i] = convert_one_to_hex(arg)
        encoded_args = eth_abi_encode(types, args)

    return "0x" + selector.hex() + encoded_args.hex()


def call_by_abi( # pylint: disable=too-many-arguments
    abi,
    fn_name,
    contract_address,
    block_num="latest",
    args=None,
    from_address=None,
    endpoint=DEFAULT_ENDPOINT,
    timeout=DEFAULT_TIMEOUT,
) -> str:
    """Call a smart contract function using its ABI.

    Parameters
    ----------
    abi: :obj:`list`
        Full contract ABI as a list of dicts
    fn_name: :obj:`str`
        Name of the function to call
    contract_address: :obj:`str`
        Address of the contract (one address)
    block_num: :obj:`int` or :obj:`str`, optional
        Block number to call at
    args: :obj:`list`, optional
        Arguments to pass to the function
    from_address: :obj:`str`, optional
        Caller's address
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    str
        Raw return data from the contract call

    Raises
    ------
    ValueError
        If the function is not found in the ABI
    """
    from .util import convert_one_to_hex
    data = encode_abi_function(abi, fn_name, args)
    hex_addr = convert_one_to_hex(contract_address)
    return call(
        hex_addr,
        block_num,
        from_address=from_address,
        data=data,
        endpoint=endpoint,
        timeout=timeout,
    )
