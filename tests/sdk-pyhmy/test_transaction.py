import pytest

from pyhmy import (
    transaction
)

from pyhmy.rpc import (
    exceptions
)

from pyhmy.exceptions import (
    TxConfirmationTimedoutError
)


localhost_shard_one = 'http://localhost:9501'
tx_hash = '0x1fa20537ea97f162279743139197ecf0eac863278ac1c8ada9a6be5d1e31e633'
tx_block_num = None
tx_block_hash = None
cx_hash = '0x1fa20537ea97f162279743139197ecf0eac863278ac1c8ada9a6be5d1e31e633'
stx_hash = '0x57ec011aabdeb078a4816502224022f291fa8b07c82bbae8476f514a1d71c730'
stx_block_num = None
stx_block_hash = None
test_index = 0
fake_shard = 'http://example.com'

# raw_txt generated via:
# hmy transfer --from one12fuf7x9rgtdgqg7vgq0962c556m3p7afsxgvll --to one12fuf7x9rgtdgqg7vgq0962c556m3p7afsxgvll
# --from-shard 0 --to-shard 1 --amount 0.1 --dry-run
raw_tx = '0xf86d01843b9aca0082520880019452789f18a342da8023cc401e5d2b14a6b710fba988016345785d8a00008028a01095f775386e0e3203446179a7a62e5ce1e765c200b5d885f6bb5b141155bd4da0651350a31e1797035cbf878e4c26069e9895845071d01308573532512cca5820'
raw_tx_hash = '0x86bce2e7765937b776bdcf927339c85421b95c70ddf06ba8e4cc0441142b0f53'

raw_stx = '0xf9015680f90105943ad89a684095a53edb47d7ddc5e034d813366731d984746573748474657374847465737484746573748474657374ddc988016345785d8a0000c9880c7d713b49da0000c887b1a2bc2ec500008a022385a827e8155000008b084595161401484a000000f1b0282554f2478661b4844a05a9deb1837aac83931029cb282872f0dcd7239297c499c02ea8da8746d2f08ca2b037e89891f862b86003557e18435c201ecc10b1664d1aea5b4ec59dbfe237233b953dbd9021b86bc9770e116ed3c413fe0334d89562568a10e133d828611f29fee8cdab9719919bbcc1f1bf812c73b9ccd0f89b4f0b9ca7e27e66d58bbb06fcf51c295b1d076cfc878a0228f16f86157860000080843b9aca008351220027a018385211a150ca032c3526cef0aba6a75f99a18cb73f547f67bab746be0c7a64a028be921002c6eb949b3932afd010dfe1de2459ec7fe84403b9d9d8892394a78c'

def _test_transaction_rpc(fn, *args, **kwargs):
    if not callable(fn):
        pytest.fail(f'Invalid function: {fn}')

    try:
        response = fn(*args, **kwargs)
    except Exception as e:
        if isinstance(e, exceptions.RPCError) and 'does not exist/is not available' in str(e):
            pytest.skip(f'{str(e)}')
        if isinstance(e, TxConfirmationTimedoutError):
            pytest.skip(f'{str(e)}')
        pytest.fail(f'Unexpected error: {e.__class__} {e}')
    return response

@pytest.mark.run(order=1)
def test_get_pending_transactions(setup_blockchain):
    pool = _test_transaction_rpc(transaction.get_pending_transactions)
    assert isinstance(pool, list)

@pytest.mark.run(order=2)
def test_get_transaction_by_hash(setup_blockchain):
    tx = _test_transaction_rpc(transaction.get_transaction_by_hash, tx_hash, endpoint=localhost_shard_one)
    assert tx
    assert isinstance(tx, dict)
    assert 'blockNumber' in tx.keys()
    assert 'blockHash' in tx.keys()
    global tx_block_num
    tx_block_num = int(tx['blockNumber'])
    global tx_block_hash
    tx_block_hash = tx['blockHash']

@pytest.mark.run(order=3)
def test_get_transaction_by_block_hash_and_index(setup_blockchain):
    if not tx_block_hash:
        pytest.skip('Failed to get reference block hash')
    tx = _test_transaction_rpc(transaction.get_transaction_by_block_hash_and_index,
                               tx_block_hash, test_index, endpoint=localhost_shard_one)
    assert tx
    assert isinstance(tx, dict)

@pytest.mark.run(order=4)
def test_get_transaction_by_block_number_and_index(setup_blockchain):
    if not tx_block_num:
        pytest.skip('Failed to get reference block num')
    tx = _test_transaction_rpc(transaction.get_transaction_by_block_number_and_index, tx_block_num, test_index,
                               endpoint=localhost_shard_one)
    assert tx
    assert isinstance(tx, dict)

@pytest.mark.run(order=5)
def test_get_transaction_receipt(setup_blockchain):
    tx_receipt = _test_transaction_rpc(transaction.get_transaction_receipt, tx_hash, endpoint=localhost_shard_one)
    assert tx_receipt
    assert isinstance(tx_receipt, dict)

@pytest.mark.run(order=6)
def test_get_transaction_error_sink(setup_blockchain):
    errors = _test_transaction_rpc(transaction.get_transaction_error_sink)
    assert isinstance(errors, list)

@pytest.mark.run(order=7)
def test_send_and_confirm_raw_transaction(setup_blockchain):
    # Note: this test is not yet idempotent since the localnet will reject transactions which were previously finalized.
    # Secondly, this is a test that seems to return None values - for example the below curl call has the same null value
    # curl --location --request POST 'http://localhost:9501' \
    # --header 'Content-Type: application/json' \
    # --data-raw '{
    #     "jsonrpc": "2.0",
    #     "id": 1,
    #     "method": "hmyv2_getTransactionByHash",
    #     "params": [
    #         "0x86bce2e7765937b776bdcf927339c85421b95c70ddf06ba8e4cc0441142b0f53"
    #     ]
    # }'
    # {"jsonrpc":"2.0","id":1,"result":null}
    test_tx = _test_transaction_rpc(transaction.send_and_confirm_raw_transaction,
                raw_tx)         # mining stops by the time this transaction is submitted
                                # so it never confirms, which is why TxConfirmationTimedoutError
                                # is in the set up call
    assert isinstance(test_tx, dict)
    assert test_tx[ 'hash' ] == raw_tx_hash

@pytest.mark.run(order=8)
def test_get_pending_cx_receipts(setup_blockchain):
    pending = _test_transaction_rpc(transaction.get_pending_cx_receipts)
    assert isinstance(pending, list)

@pytest.mark.run(order=9)
def test_get_cx_receipt_by_hash(setup_blockchain):
    cx = _test_transaction_rpc(transaction.get_cx_receipt_by_hash, cx_hash)
    assert cx
    assert isinstance(cx, dict)

@pytest.mark.run(order=10)
def test_resend_cx_receipt(setup_blockchain):
    sent = _test_transaction_rpc(transaction.resend_cx_receipt, cx_hash)
    assert isinstance(sent, bool)
    assert not sent

@pytest.mark.run(order=11)
def test_get_staking_transaction_by_hash(setup_blockchain):
    staking_tx = _test_transaction_rpc(transaction.get_staking_transaction_by_hash, stx_hash)
    assert staking_tx
    assert isinstance(staking_tx, dict)
    assert 'blockNumber' in staking_tx.keys()
    assert 'blockHash' in staking_tx.keys()
    global stx_block_num
    stx_block_num = int(staking_tx['blockNumber'])
    global stx_block_hash
    stx_block_hash = staking_tx['blockHash']

@pytest.mark.run(order=12)
def test_get_transaction_by_block_hash_and_index(setup_blockchain):
    if not stx_block_hash:
        pytest.skip('Failed to get reference block hash')
    stx = _test_transaction_rpc(transaction.get_staking_transaction_by_block_hash_and_index, stx_block_hash, test_index)
    assert stx
    assert isinstance(stx, dict)

@pytest.mark.run(order=13)
def test_get_transaction_by_block_number_and_index(setup_blockchain):
    if not stx_block_num:
        pytest.skip('Failed to get reference block num')
    stx = _test_transaction_rpc(transaction.get_staking_transaction_by_block_number_and_index, stx_block_num, test_index)
    assert stx
    assert isinstance(stx, dict)

@pytest.mark.run(order=14)
def test_get_staking_transaction_error_sink(setup_blockchain):
    errors = _test_transaction_rpc(transaction.get_staking_transaction_error_sink)
    assert isinstance(errors, list)

@pytest.mark.run(order=15)
def test_send_raw_staking_transaction(setup_blockchain):
    test_stx_hash = _test_transaction_rpc(transaction.send_raw_staking_transaction, raw_stx, endpoint=localhost_shard_one)
    assert isinstance(test_stx_hash, str)
    assert test_stx_hash == stx_hash

@pytest.mark.run(order=16)
def test_get_pool_stats(setup_blockchain):
    test_pool_stats = _test_transaction_rpc(transaction.get_pool_stats, endpoint=localhost_shard_one)
    assert isinstance(test_pool_stats, dict)

@pytest.mark.run(order=17)
def test_get_pending_staking_transactions(setup_blockchain):
    pending_staking_transactions = _test_transaction_rpc(transaction.get_pending_staking_transactions, endpoint=localhost_shard_one)
    assert isinstance(pending_staking_transactions, list)

@pytest.mark.run(order=18)
def test_errors():
    with pytest.raises(exceptions.RPCError):
        transaction.get_pending_transactions(fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.get_transaction_error_sink(fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.get_pool_stats(fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.get_transaction_by_hash('', endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.get_transaction_by_block_hash_and_index('', 1, endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.get_transaction_by_block_number_and_index(1, 1, endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.get_transaction_receipt('', endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.send_raw_transaction('', endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.get_pending_cx_receipts(fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.get_cx_receipt_by_hash('', endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.resend_cx_receipt('', endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.get_staking_transaction_by_hash('', endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.get_staking_transaction_by_block_hash_and_index('', 1, endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.get_staking_transaction_by_block_number_and_index(1, 1, endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.get_staking_transaction_error_sink(endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.send_raw_staking_transaction('', endpoint=fake_shard)
    with pytest.raises(exceptions.RPCError):
        transaction.get_pending_staking_transactions(endpoint=fake_shard)
