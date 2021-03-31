import pytest
import requests

from pyhmy import (
    transaction
)

from pyhmy.rpc import (
    exceptions
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

raw_tx = '0xf86f80843b9aca008252080180943ad89a684095a53edb47d7ddc5e034d8133667318a152d02c7e14af68000008027a0ec6c8ad0f70b3c826fa77574c6815a8f73936fafb7b2701a7082ad7d278c95a9a0429f9f166b1c1d385a4ec8f8b86604c26e427c2b0a1c85d9cf4ec6bbd0719508'
raw_stx = '0xf9015680f90105943ad89a684095a53edb47d7ddc5e034d813366731d984746573748474657374847465737484746573748474657374ddc988016345785d8a0000c9880c7d713b49da0000c887b1a2bc2ec500008a022385a827e8155000008b084595161401484a000000f1b0282554f2478661b4844a05a9deb1837aac83931029cb282872f0dcd7239297c499c02ea8da8746d2f08ca2b037e89891f862b86003557e18435c201ecc10b1664d1aea5b4ec59dbfe237233b953dbd9021b86bc9770e116ed3c413fe0334d89562568a10e133d828611f29fee8cdab9719919bbcc1f1bf812c73b9ccd0f89b4f0b9ca7e27e66d58bbb06fcf51c295b1d076cfc878a0228f16f86157860000080843b9aca008351220027a018385211a150ca032c3526cef0aba6a75f99a18cb73f547f67bab746be0c7a64a028be921002c6eb949b3932afd010dfe1de2459ec7fe84403b9d9d8892394a78c'

def _test_transaction_rpc(fn, *args, **kwargs):
    if not callable(fn):
        pytest.fail(f'Invalid function: {fn}')

    try:
        response = fn(*args, **kwargs)
    except Exception as e:
        if isinstance(e, exceptions.RPCError) and 'does not exist/is not available' in str(e):
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
    tx_block_num = tx['blockNumber']
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
def test_send_raw_transaction(setup_blockchain):
    test_tx_hash = _test_transaction_rpc(transaction.send_raw_transaction, raw_tx)
    assert isinstance(test_tx_hash, str)
    assert test_tx_hash == tx_hash

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
    stx_block_num = staking_tx['blockNumber']
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
    test_stx_hash = _test_transaction_rpc(transaction.send_raw_staking_transaction, raw_stx)
    assert isinstance(test_stx_hash, str)
    assert test_stx_hash == stx_hash
