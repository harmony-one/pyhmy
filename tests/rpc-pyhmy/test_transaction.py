import pytest
import requests

from pyhmy.rpc import (
    transaction,
    exceptions
)


tx_hash = '0xfe6af62e5037d2e33412a5837e5753ebed2e4f9ab7da988bd7aa35d17ae4283f'
tx_block_num = None
tx_block_hash = None
cx_hash = None  # TODO: Add cross shard to conftest
stx_hash = '0x57ec011aabdeb078a4816502224022f291fa8b07c82bbae8476f514a1d71c730'
stx_block_num = None
stx_block_hash = None
test_index = 0

raw_tx = '0xf86f80843b9aca008252088080943ad89a684095a53edb47d7ddc5e034d8133667318a152d02c7e14af68000008028a0e453ffec54139efccb6b689df723f12b969710fbf1438abc1dcf5618e1c3b0d5a0595543cffcc8e41549bfc74900e6c7317ed1e667cfa71e07da1d8a663d363823'
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
def test_get_pneding_transactions(setup_blockchain):
    _test_transaction_rpc(transaction.get_pending_transactions)

@pytest.mark.run(order=2)
def test_get_transaction_by_hash(setup_blockchain):
    tx = _test_transaction_rpc(transaction.get_transaction_by_hash, tx_hash)
    assert tx is not None
    global tx_block_num
    tx_block_num = int(tx['blockNumber'], 0)
    global tx_block_hash
    tx_block_hash = tx['blockHash']

@pytest.mark.run(order=3)
def test_get_transaction_by_block_hash_and_index(setup_blockchain):
    if not tx_block_hash:
        pytest.skip('Failed to get reference block hash')
    tx = _test_transaction_rpc(transaction.get_transaction_by_block_hash_and_index, tx_block_hash, test_index)
    assert tx is not None

@pytest.mark.run(order=4)
def test_get_transaction_by_block_number_and_index(setup_blockchain):
    if not tx_block_num:
        pytest.skip('Failed to get reference block num')
    tx = _test_transaction_rpc(transaction.get_transaction_by_block_number_and_index, tx_block_num, test_index)
    assert tx is not None

@pytest.mark.run(order=5)
def test_get_transaction_receipt(setup_blockchain):
    tx_receipt = _test_transaction_rpc(transaction.get_transaction_receipt, tx_hash)
    assert tx_receipt is not None

@pytest.mark.run(order=6)
def test_get_transaction_error_sink(setup_blockchain):
    _test_transaction_rpc(transaction.get_transaction_error_sink)

@pytest.mark.run(order=7)
def test_send_raw_transaction(setup_blockchain):
    test_tx_hash = _test_transaction_rpc(transaction.send_raw_transaction, raw_tx)
    assert test_tx_hash == tx_hash

# TODO: Add a cross shard transaction in conftest to test Cross Shard transaction RPCs
@pytest.mark.run(order=8)
def test_get_pending_cx_receipts(setup_blockchain):
    _test_transaction_rpc(transaction.get_pending_cx_receipts)

@pytest.mark.run(order=9)
def test_get_cx_receipt_by_hash(setup_blockchain):
    if not cx_hash:
        pytest.skip(f'test not implemented')
    _test_transaction_rpc(transaction.get_cx_receipt_by_hash, cx_hash)

@pytest.mark.run(order=10)
def test_resend_cx_receipt(setup_blockchain):
    if not cx_hash:
        pytest.skip(f'test not implemented')
    _test_transaction_rpc(transaction.resend_cx_receipt, cx_hash)

@pytest.mark.run(order=11)
def test_get_staking_transaction_by_hash(setup_blockchain):
    staking_tx = _test_transaction_rpc(transaction.get_staking_transaction_by_hash, stx_hash)
    assert staking_tx is not None
    global stx_block_num
    stx_block_num = int(staking_tx['blockNumber'], 0)
    global stx_block_hash
    stx_block_hash = staking_tx['blockHash']

@pytest.mark.run(order=12)
def test_get_transaction_by_block_hash_and_index(setup_blockchain):
    if not stx_block_hash:
        pytest.skip('Failed to get reference block hash')
    stx = _test_transaction_rpc(transaction.get_staking_transaction_by_block_hash_and_index, stx_block_hash, test_index)
    assert stx is not None

@pytest.mark.run(order=13)
def test_get_transaction_by_block_number_and_index(setup_blockchain):
    if not stx_block_num:
        pytest.skip('Failed to get reference block num')
    stx = _test_transaction_rpc(transaction.get_staking_transaction_by_block_number_and_index, stx_block_num, test_index)
    assert stx is not None

@pytest.mark.run(order=14)
def test_get_staking_transaction_error_sink(setup_blockchain):
    _test_transaction_rpc(transaction.get_staking_transaction_error_sink)

@pytest.mark.run(order=15)
def test_send_raw_staking_transaction(setup_blockchain):
    test_stx_hash = _test_transaction_rpc(transaction.send_raw_staking_transaction, raw_stx)
    assert test_stx_hash == stx_hash
