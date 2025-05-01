import pytest

from pyhmy import transaction

from pyhmy.rpc import exceptions

endpoint = "http://localhost:9620"
endpoint_shard_one = "http://localhost:9622"
fake_shard = "http://example.com"

# previously sent txs to get and check
tx_hash = "0xc26be5776aa57438bccf196671a2d34f3f22c9c983c0f844c62b2fb90403aa43"
tx_block_num = None
tx_block_hash = None
tx_index = None

cx_hash = "0xf73ba634cb96fc0e3e2c9d3b4c91379e223741be4a5aa56e6d6caf49c1ae75cf"

stx_hash = "0xc8177ace2049d9f4eb4a45fd6bd6b16f693573d036322c36774cc00d05a3e24f"
stx_block_num = None
stx_block_hash = None
stx_index = None

# new txs to send and check
raw_tx = "0xf86f0385174876e800825208808094c9c6d47ee5f2e3e08d7367ad1a1373ba9dd172418905b12aefafa80400008027a07a4952b90bf38723a9197179a8e6d2e9b3a86fd6da4e66a9cf09fdc59783f757a053910798b311245525bd77d6119332458c2855102e4fb9e564f6a3b710d18bb0"
raw_tx_hash = "0x7ccd80f8513f76ec58b357c7a82a12a95e025d88f1444e953f90e3d86e222571"

raw_stx = "0xf88302f494c9c6d47ee5f2e3e08d7367ad1a1373ba9dd1724194a5241513da9f4463f1d4874b548dfbac29d91f3489056bc75e2d631000008085174876e80082c35027a0808ea7d27adf3b1f561e8da4676814084bb75ac541b616bece87c6446e6cc54ea02f19f0b14240354bd42ad60b0c7189873c0be87044e13072b0981a837ca76f64"
raw_stx_hash = "0xe7d07ef6d9fca595a14ceb0ca917bece7bedb15efe662300e9334a32ac1da629"


def _test_transaction_rpc( fn, *args, **kwargs ):
    if not callable( fn ):
        pytest.fail( f"Invalid function: {fn}" )

    try:
        response = fn( *args, **kwargs )
    except Exception as e:
        if isinstance( e,
                       exceptions.RPCError
                      ) and "does not exist/is not available" in str( e ):
            pytest.skip( f"{str(e)}" )
        pytest.fail( f"Unexpected error: {e.__class__} {e}" )
    return response


def test_get_pending_transactions( setup_blockchain ):
    pool = _test_transaction_rpc( transaction.get_pending_transactions )
    assert isinstance( pool, list )


def test_get_transaction_by_hash( setup_blockchain ):
    tx = _test_transaction_rpc(
        transaction.get_transaction_by_hash,
        tx_hash,
        endpoint = endpoint
    )
    assert tx
    assert isinstance( tx, dict )
    assert "blockNumber" in tx.keys()
    assert "blockHash" in tx.keys()
    global tx_block_num
    tx_block_num = int( tx[ "blockNumber" ] )
    global tx_block_hash
    tx_block_hash = tx[ "blockHash" ]
    global tx_index
    tx_index = int( tx[ "transactionIndex" ] )


def test_get_transaction_by_block_hash_and_index( setup_blockchain ):
    if not tx_block_hash:
        pytest.skip( "Failed to get reference block hash" )
    tx = _test_transaction_rpc(
        transaction.get_transaction_by_block_hash_and_index,
        tx_block_hash,
        tx_index,
        endpoint = endpoint,
    )
    assert tx
    assert isinstance( tx, dict )


def test_get_transaction_by_block_number_and_index( setup_blockchain ):
    if not tx_block_num:
        pytest.skip( "Failed to get reference block num" )
    tx = _test_transaction_rpc(
        transaction.get_transaction_by_block_number_and_index,
        tx_block_num,
        tx_index,
        endpoint = endpoint,
    )
    assert tx
    assert isinstance( tx, dict )


def test_get_transaction_receipt( setup_blockchain ):
    tx_receipt = _test_transaction_rpc(
        transaction.get_transaction_receipt,
        tx_hash,
        endpoint = endpoint
    )
    assert tx_receipt
    assert isinstance( tx_receipt, dict )


def test_get_transaction_error_sink( setup_blockchain ):
    errors = _test_transaction_rpc( transaction.get_transaction_error_sink )
    assert isinstance( errors, list )


def test_send_and_confirm_raw_transaction( setup_blockchain ):
    # Note: this test is not yet idempotent since the localnet will reject transactions which were previously finalized.
    test_tx = _test_transaction_rpc(
        transaction.send_and_confirm_raw_transaction,
        raw_tx
    )
    assert isinstance( test_tx, dict )
    assert test_tx[ "hash" ] == raw_tx_hash


def test_get_pending_cx_receipts( setup_blockchain ):
    pending = _test_transaction_rpc( transaction.get_pending_cx_receipts )
    assert isinstance( pending, list )


def test_get_cx_receipt_by_hash( setup_blockchain ):
    cx = _test_transaction_rpc(
        transaction.get_cx_receipt_by_hash,
        cx_hash,
        endpoint_shard_one
    )
    assert cx
    assert isinstance( cx, dict )


def test_resend_cx_receipt( setup_blockchain ):
    sent = _test_transaction_rpc( transaction.resend_cx_receipt, cx_hash )
    assert isinstance( sent, bool )
    assert sent


def test_get_staking_transaction_by_hash( setup_blockchain ):
    staking_tx = _test_transaction_rpc(
        transaction.get_staking_transaction_by_hash,
        stx_hash
    )
    assert staking_tx
    assert isinstance( staking_tx, dict )
    assert "blockNumber" in staking_tx.keys()
    assert "blockHash" in staking_tx.keys()
    global stx_block_num
    stx_block_num = int( staking_tx[ "blockNumber" ] )
    global stx_block_hash
    stx_block_hash = staking_tx[ "blockHash" ]
    global stx_index
    stx_index = int( staking_tx[ "transactionIndex" ] )


def test_get_transaction_by_block_hash_and_index( setup_blockchain ):
    if not stx_block_hash:
        pytest.skip( "Failed to get reference block hash" )
    stx = _test_transaction_rpc(
        transaction.get_staking_transaction_by_block_hash_and_index,
        stx_block_hash,
        stx_index,
    )
    assert stx
    assert isinstance( stx, dict )


def test_get_transaction_by_block_number_and_index( setup_blockchain ):
    if not stx_block_num:
        pytest.skip( "Failed to get reference block num" )
    stx = _test_transaction_rpc(
        transaction.get_staking_transaction_by_block_number_and_index,
        stx_block_num,
        stx_index,
    )
    assert stx
    assert isinstance( stx, dict )


def test_get_staking_transaction_error_sink( setup_blockchain ):
    errors = _test_transaction_rpc(
        transaction.get_staking_transaction_error_sink
    )
    assert isinstance( errors, list )


def test_send_raw_staking_transaction( setup_blockchain ):
    test_stx = _test_transaction_rpc(
        transaction.send_and_confirm_raw_staking_transaction,
        raw_stx,
        endpoint = endpoint
    )
    assert isinstance( test_stx, dict )
    assert test_stx[ "hash" ] == raw_stx_hash


def test_get_pool_stats( setup_blockchain ):
    test_pool_stats = _test_transaction_rpc(
        transaction.get_pool_stats,
        endpoint = endpoint
    )
    assert isinstance( test_pool_stats, dict )


def test_get_pending_staking_transactions( setup_blockchain ):
    pending_staking_transactions = _test_transaction_rpc(
        transaction.get_pending_staking_transactions,
        endpoint = endpoint
    )
    assert isinstance( pending_staking_transactions, list )


def test_errors():
    with pytest.raises( exceptions.RPCError ):
        transaction.get_pending_transactions( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        transaction.get_transaction_error_sink( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        transaction.get_pool_stats( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        transaction.get_transaction_by_hash( "", endpoint = fake_shard )
    with pytest.raises( exceptions.RPCError ):
        transaction.get_transaction_by_block_hash_and_index(
            "",
            1,
            endpoint = fake_shard
        )
    with pytest.raises( exceptions.RPCError ):
        transaction.get_transaction_by_block_number_and_index(
            1,
            1,
            endpoint = fake_shard
        )
    with pytest.raises( exceptions.RPCError ):
        transaction.get_transaction_receipt( "", endpoint = fake_shard )
    with pytest.raises( exceptions.RPCError ):
        transaction.send_raw_transaction( "", endpoint = fake_shard )
    with pytest.raises( exceptions.RPCError ):
        transaction.get_pending_cx_receipts( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        transaction.get_cx_receipt_by_hash( "", endpoint = fake_shard )
    with pytest.raises( exceptions.RPCError ):
        transaction.resend_cx_receipt( "", endpoint = fake_shard )
    with pytest.raises( exceptions.RPCError ):
        transaction.get_staking_transaction_by_hash( "", endpoint = fake_shard )
    with pytest.raises( exceptions.RPCError ):
        transaction.get_staking_transaction_by_block_hash_and_index(
            "",
            1,
            endpoint = fake_shard
        )
    with pytest.raises( exceptions.RPCError ):
        transaction.get_staking_transaction_by_block_number_and_index(
            1,
            1,
            endpoint = fake_shard
        )
    with pytest.raises( exceptions.RPCError ):
        transaction.get_staking_transaction_error_sink( endpoint = fake_shard )
    with pytest.raises( exceptions.RPCError ):
        transaction.send_raw_staking_transaction( "", endpoint = fake_shard )
    with pytest.raises( exceptions.RPCError ):
        transaction.get_pending_staking_transactions( endpoint = fake_shard )
