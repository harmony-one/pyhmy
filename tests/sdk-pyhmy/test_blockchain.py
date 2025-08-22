import pytest
import requests

from pyhmy import blockchain

from pyhmy.rpc import exceptions

test_epoch_number = 0
genesis_block_number = 0
test_block_number = 1
test_block_hash = None
fake_shard = "https://faucet.hmny.io/"
address = "one155jp2y76nazx8uw5sa94fr0m4s5aj8e5xm6fu3"


def _test_blockchain_rpc( fn, *args, **kwargs ):
    if not callable( fn ):
        pytest.fail( f"Invalid function: {fn}" )

    try:
        response = fn( *args, **kwargs )
    except Exception as e:
        if isinstance( e,
                       exceptions.RPCError
                      ) and "does not exist/is not available" in str( e ):
            pytest.fail( f"{str(e)}" )
        pytest.fail( f"Unexpected error: {e.__class__} {e}" )
    return response


def test_get_node_metadata( setup_blockchain ):
    metadata = _test_blockchain_rpc( blockchain.get_node_metadata )
    assert isinstance( metadata, dict )


def test_get_sharding_structure( setup_blockchain ):
    sharding_structure = _test_blockchain_rpc(
        blockchain.get_sharding_structure
    )
    assert isinstance( sharding_structure, list )
    assert len( sharding_structure ) > 0


def test_get_leader_address( setup_blockchain ):
    leader = _test_blockchain_rpc( blockchain.get_leader_address )
    assert isinstance( leader, str )
    assert "one1" in leader


def test_get_block_number( setup_blockchain ):
    current_block_number = _test_blockchain_rpc( blockchain.get_block_number )
    assert isinstance( current_block_number, int )


def test_get_current_epoch( setup_blockchain ):
    current_epoch = _test_blockchain_rpc( blockchain.get_current_epoch )
    assert isinstance( current_epoch, int )


def tset_get_gas_price( setup_blockchain ):
    gas = _test_blockchain_rpc( blockchain.get_gas_price )
    assert isinstance( gas, int )


def test_get_num_peers( setup_blockchain ):
    peers = _test_blockchain_rpc( blockchain.get_num_peers )
    assert isinstance( peers, int )


def test_get_latest_header( setup_blockchain ):
    header = _test_blockchain_rpc( blockchain.get_latest_header )
    assert isinstance( header, dict )


def test_get_latest_chain_headers( setup_blockchain ):
    header_pair = _test_blockchain_rpc( blockchain.get_latest_chain_headers )
    assert isinstance( header_pair, dict )


def test_get_block_by_number( setup_blockchain ):
    global test_block_hash
    block = _test_blockchain_rpc(
        blockchain.get_block_by_number,
        test_block_number
    )
    assert isinstance( block, dict )
    assert "hash" in block.keys()
    test_block_hash = block[ "hash" ]


def test_get_block_by_hash( setup_blockchain ):
    if not test_block_hash:
        pytest.fail( "Failed to get reference block hash" )
    block = _test_blockchain_rpc(
        blockchain.get_block_by_hash,
        test_block_hash
    )
    assert isinstance( block, dict )


def test_get_block_transaction_count_by_number( setup_blockchain ):
    tx_count = _test_blockchain_rpc(
        blockchain.get_block_transaction_count_by_number,
        test_block_number
    )
    assert isinstance( tx_count, int )


def test_get_block_transaction_count_by_hash( setup_blockchain ):
    if not test_block_hash:
        pytest.fail( "Failed to get reference block hash" )
    tx_count = _test_blockchain_rpc(
        blockchain.get_block_transaction_count_by_hash,
        test_block_hash
    )
    assert isinstance( tx_count, int )


def test_get_blocks( setup_blockchain ):
    blocks = _test_blockchain_rpc(
        blockchain.get_blocks,
        genesis_block_number,
        test_block_number
    )
    assert isinstance( blocks, list )
    assert len( blocks ) == ( test_block_number - genesis_block_number + 1 )


def test_get_block_signers( setup_blockchain ):
    block_signers = _test_blockchain_rpc(
        blockchain.get_block_signers,
        test_block_number
    )
    assert isinstance( block_signers, list )
    assert len( block_signers ) > 0


def test_get_validators( setup_blockchain ):
    validators = _test_blockchain_rpc(
        blockchain.get_validators,
        test_epoch_number
    )
    assert isinstance( validators, dict )
    assert "validators" in validators.keys()
    assert len( validators[ "validators" ] ) > 0


def test_get_shard( setup_blockchain ):
    shard = _test_blockchain_rpc( blockchain.get_shard )
    assert isinstance( shard, int )
    assert shard == 0


def test_get_staking_epoch( setup_blockchain ):
    staking_epoch = _test_blockchain_rpc( blockchain.get_staking_epoch )
    assert isinstance( staking_epoch, int )


def test_get_prestaking_epoch( setup_blockchain ):
    prestaking_epoch = _test_blockchain_rpc( blockchain.get_prestaking_epoch )
    assert isinstance( prestaking_epoch, int )


def test_get_bad_blocks( setup_blockchain ):
    bad_blocks = _test_blockchain_rpc( blockchain.get_bad_blocks )
    assert isinstance( bad_blocks, list )


def test_get_validator_keys( setup_blockchain ):
    keys = _test_blockchain_rpc(
        blockchain.get_validator_keys,
        test_epoch_number
    )
    assert isinstance( keys, list )
    assert len( keys ) > 0


def test_get_block_signers_keys( setup_blockchain ):
    keys = _test_blockchain_rpc(
        blockchain.get_block_signers_keys,
        test_block_number
    )
    assert isinstance( keys, list )
    assert len( keys ) > 0


def test_chain_id( setup_blockchain ):
    chain_id = _test_blockchain_rpc( blockchain.chain_id )
    assert isinstance( chain_id, int )


def test_get_peer_info( setup_blockchain ):
    peer_info = _test_blockchain_rpc( blockchain.get_peer_info )
    assert isinstance( peer_info, dict )


def test_protocol_version( setup_blockchain ):
    protocol_version = _test_blockchain_rpc( blockchain.protocol_version )
    assert isinstance( protocol_version, int )


def test_is_last_block( setup_blockchain ):
    is_last_block = _test_blockchain_rpc( blockchain.is_last_block, 0 )
    assert isinstance( is_last_block, bool )
    assert not is_last_block


def test_epoch_last_block( setup_blockchain ):
    epoch_last_block = _test_blockchain_rpc( blockchain.epoch_last_block, 0 )
    assert isinstance( epoch_last_block, int )


def test_get_circulating_supply( setup_blockchain ):
    circulating_supply = _test_blockchain_rpc(
        blockchain.get_circulating_supply
    )
    assert isinstance( circulating_supply, str )


def test_get_total_supply( setup_blockchain ):
    total_supply = _test_blockchain_rpc( blockchain.get_total_supply )
    assert isinstance( total_supply, str ) or total_supply == None


def test_get_last_cross_links( setup_blockchain ):
    last_cross_links = _test_blockchain_rpc( blockchain.get_last_cross_links )
    assert isinstance( last_cross_links, list )


def test_get_gas_price( setup_blockchain ):
    gas_price = _test_blockchain_rpc( blockchain.get_gas_price )
    assert isinstance( gas_price, int )


def test_get_version( setup_blockchain ):
    version = _test_blockchain_rpc( blockchain.get_version )
    assert isinstance( version, int )


def test_get_header_by_number( setup_blockchain ):
    header_pair = _test_blockchain_rpc( blockchain.get_header_by_number, 0 )
    assert isinstance( header_pair, dict )


def test_get_block_staking_transaction_count_by_number( setup_blockchain ):
    tx_count = _test_blockchain_rpc(
        blockchain.get_block_staking_transaction_count_by_number,
        test_block_number
    )
    assert isinstance( tx_count, int )


def test_get_block_staking_transaction_count_by_hash( setup_blockchain ):
    if not test_block_hash:
        pytest.fail( "Failed to get reference block hash" )
    tx_count = _test_blockchain_rpc(
        blockchain.get_block_staking_transaction_count_by_hash,
        test_block_hash
    )
    assert isinstance( tx_count, int )


def test_is_block_signer( setup_blockchain ):
    is_signer = _test_blockchain_rpc(
        blockchain.is_block_signer,
        test_block_number,
        address
    )
    assert isinstance( is_signer, bool )


def test_get_signed_blocks( setup_blockchain ):
    signed_blocks = _test_blockchain_rpc(
        blockchain.get_signed_blocks,
        address
    )
    assert isinstance( signed_blocks, int )


def test_in_sync( setup_blockchain ):
    in_sync = _test_blockchain_rpc( blockchain.in_sync )
    assert isinstance( in_sync, bool )


def test_beacon_in_sync( setup_blockchain ):
    beacon_in_sync = _test_blockchain_rpc( blockchain.beacon_in_sync )
    assert isinstance( beacon_in_sync, bool )


def test_errors():
    with pytest.raises( exceptions.RPCError ):
        blockchain.chain_id( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_node_metadata( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_peer_info( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.protocol_version( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_shard( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_staking_epoch( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_prestaking_epoch( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_sharding_structure( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_leader_address( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.is_last_block( 0, fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.epoch_last_block( 0, fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_circulating_supply( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_total_supply( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_block_number( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_current_epoch( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_last_cross_links( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_gas_price( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_num_peers( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_version( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_latest_header( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_header_by_number( 0, fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_latest_chain_headers( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_block_by_number( 0, endpoint = fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_block_by_hash( "", endpoint = fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_block_transaction_count_by_number( 0, fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_block_transaction_count_by_hash( "", fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_block_staking_transaction_count_by_number(
            0,
            fake_shard
        )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_block_staking_transaction_count_by_hash( "", fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_blocks( 0, 1, endpoint = fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_block_signers( 0, fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_block_signers_keys( 0, fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.is_block_signer( 0, "", fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_signed_blocks( "", fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_validators( 1, fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.get_validator_keys( 0, fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.in_sync( fake_shard )
    with pytest.raises( exceptions.RPCError ):
        blockchain.beacon_in_sync( fake_shard )
