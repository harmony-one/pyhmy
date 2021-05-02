# Pyhmy - Harmony's python utilities

**This library only supports Python 3.6+**

A Python library for interacting and working the [Harmony blockchain](https://harmony.one/)
and [related codebases](https://github.com/harmony-one).

[Full documentation is located on Harmony's GitBook](https://docs.harmony.one/) (in progress).

## Installation
```
pip install pyhmy

On MacOS:

Make sure you have Python3 installed, and use python3 to install pyhmy

sudo pip3 install pathlib
sudo pip3 install pyhmy
```

## Development

Clone the repository and then run the following:
```
make install
```

## Running tests

You need `docker` and `go` installed to quickly run a local blockchain with staking enabled (detailed instructions [here](https://github.com/harmony-one/harmony/blob/main/README.md)):
```
mkdir -p $(go env GOPATH)/src/github.com/harmony-one
cd $(go env GOPATH)/src/github.com/harmony-one
git clone https://github.com/harmony-one/mcl.git
git clone https://github.com/harmony-one/bls.git
git clone https://github.com/harmony-one/harmony.git
cd harmony
make test-rpc
```

Once the terminal displays `=== FINISHED RPC TESTS ===`, use another shell to run the following tests

```
make test
```

Or directly with `pytest` (reference [here](https://docs.pytest.org/en/latest/index.html) for more info):

```
py.test tests
```

## Releasing

You can release this library with the following command (assuming you have the credentials to upload):

```
make release
```
## Usage
```
test_net = 'https://api.s0.b.hmny.io'				# this is shard 0
test_net_shard_1 = 'https://api.s1.b.hmny.io'
test_address = 'one18t4yj4fuutj83uwqckkvxp9gfa0568uc48ggj7'

main_net = 'https://rpc.s0.t.hmny.io'
main_net_shard_1 = 'https://rpc.s1.t.hmny.io'
```
#### accounts
```
from pyhmy import account
```
##### Balance / account related information
````
balance = account.get_balance(test_address, endpoint=test_net)				# on shard 0, in ATTO
total_balance = account.get_total_balance(test_address, endpoint=test_net)	# on all shards, in ATTO
balance_by_shard = account.get_balance_on_all_shards(test_address, endpoint=test_net)	# list of dictionaries with shard and balance as keys
genesis_balance = account.get_balance_by_block(test_address, block_num=0, endpoint=test_net)
latest_balance = account.get_balance_by_block(test_address, block_num='latest', endpoint=test_net)	# block_num can be a string 'latest', or 'pending', if implemented at the RPC level
account_nonce = account.get_account_nonce(test_address, block_num='latest', endpoint=test_net)
````
##### Transaction counts
````
tx_count = account.get_transactions_count(test_address, tx_type='ALL', endpoint=test_net)
sent_tx_count = account.get_transactions_count(test_address, tx_type='SENT', endpoint=test_net)
received_tx_count = account.get_transactions_count(test_address, tx_type='RECEIVED', endpoint=test_net)
legacy_tx_count = account.get_transaction_count(test_address, block_num='latest', endpoint=test_net)	# API is legacy
legacy_tx_count_pending = account.get_transaction_count(test_address, block_num='pending', endpoint=test_net)
````
##### Staking transaction counts
````
stx_count = account.get_staking_transactions_count(test_address, tx_type='ALL', endpoint=test_net)
sent_stx_count = account.get_staking_transactions_count(test_address, tx_type='SENT', endpoint=test_net)
received_stx_count = account.get_staking_transactions_count(test_address, tx_type='RECEIVED', endpoint=test_net)
````
##### Transaction history
To get a list of hashes, use `include_full_tx=False`
````
first_100_tx_hashes = account.get_transaction_history(test_address, page=0, page_size=100, include_full_tx=False, endpoint=test_net)
````
To get the next 100 transactions, change the `page`
```
next_100_tx_hashes = account.get_transaction_history(test_address, page=1, page_size=100, include_full_tx=False, endpoint=test_net)
```
To get a list of full transaction details, use `include_full_tx=True` (see `get_transaction_by_hash` for the reply structure
````
first_3_full_tx = account.get_transaction_history(test_address, page=0, page_size=3, include_full_tx=True, endpoint=test_net)
````
To get newest transactions, use `order='DESC'`
````
last_3_full_tx = account.get_transaction_history(test_address, page=0, page_size=3, include_full_tx=True, order='DESC', endpoint=test_net)
````
To change the transaction type (SENT / RECEIVED / ALL), pass the `tx_type` parameter
```
first_100_received_tx_hashes = account.get_transaction_history(test_address, page=0, page_size=100, include_full_tx=False, tx_type='RECEIVED', endpoint=test_net)
```
##### Staking transaction history
To get a list of staking hashes, use `include_full_tx=False`
````
first_100_stx_hashes = account.get_staking_transaction_history(test_address, page=0, page_size=100, include_full_tx=False, endpoint=test_net)
````
To get the next 100 staking transactions, change the `page`
```
next_100_stx_hashes = account.get_staking_transaction_history(test_address, page=1, page_size=100, include_full_tx=False, endpoint=test_net)
```
To get a list of full staking transaction details, use `include_full_tx=True` (see `get_transaction_by_hash` for the reply structure
````
first_3_full_stx = account.get_staking_transaction_history(test_address, page=0, page_size=3, include_full_tx=True, endpoint=test_net)
````
To get newest staking transactions, use `order='DESC'`
````
last_3_full_stx = account.get_staking_transaction_history(test_address, page=0, page_size=3, include_full_tx=True, order='DESC', endpoint=test_net)
````
To change the staking transaction type (SENT / RECEIVED / ALL), pass the `tx_type` parameter
```
first_100_received_stx_hashes = account.get_staking_transaction_history(test_address, page=0, page_size=100, include_full_tx=False, tx_type='RECEIVED', endpoint=test_net)
```
#### Blockchain
```
from pyhmy import blockchain
from decimal import Decimal
```
##### Node / network information
```
chain_id = blockchain.chain_id(test_net)					# chain type, for example, mainnet or testnet
node_metadata = blockchain.get_node_metadata(test_net)		# metadata about the endpoint
peer_info = blockchain.get_peer_info(test_net)				# peers of the endpoint
protocol_version = blockchain.protocol_version(test_net)	# protocol version being used
num_peers = blockchain.get_num_peers(test_net)				# number of peers of the endpoin
version = blockchain.get_version(test_net)					# EVM chain id, https://chainid.network
is_node_in_sync = blockchain.in_sync(test_net)						# whether the node is in sync (not out of sync or not syncing)
is_beacon_in_sync = blockchain.beacon_in_sync(test_net)		# whether the beacon node is in sync
prestaking_epoch_number = blockchain.get_prestaking_epoch(test_net)
staking_epoch_number = blockchain.get_staking_epoch(test_net)
```
##### Sharding information
```
shard_id = blockchain.get_shard(test_net)							# get shard id of the endpoint
sharding_structure = blockchain.get_sharding_structure(test_net)	# list of dictionaries, each representing a shard
last_cross_links = blockchain.get_last_cross_links(test_net)		# list of dictionaries for each shard except test_net
```
##### Current network status
```
leader_address = blockchain.get_leader_address(test_net)
is_last_block = blockchain.is_last_block(block_num=0, test_net)
last_block_of_epoch5 = blockchain.epoch_last_block(block_num=5, test_net)
circulating_supply = Decimal(blockchain.get_circulating_supply(test_net))
premined = blockchain.get_total_supply(test_net)					# should be None?
current_block_num = blockchain.get_block_number(test_net)
current_epoch = blockchain.get_current_epoch(test_net)
gas_price = blockchain.get_gas_price(test_net)						# this returns 1 always
```
##### Block headers
```
latest_header = blockchain.get_latest_header(test_net)						# header contains hash, number, cross links, signature, time, etc (see get_latest_header for a full list)
latest_hash = latest_header['blockHash']
latest_number = latest_header['blockNumber']
previous_header = blockchain.get_header_by_number(latest_number-1, test_net)
chain_headers = blockchain.get_latest_chain_headers(test_net_shard_1)		# chain headers by beacon and shard
```
##### Blocks
###### By block number
Fetch the barebones information about the block as a dictionary
```
latest_block = blockchain.get_block_by_number(block_num='latest', endpoint=test_net)
```
Fetch a block with full information (`full_tx=True`) for each transaction in the block
```
block = blockchain.get_block_by_number(block_num=9017724, full_tx=True, include_tx=True, include_staking_tx=True, endpoint=test_net)
```
Fetch a block and only staking transactions (`include_tx=False, include_staking_tx=True`) for the block
```
block = blockchain.get_block_by_number(block_num='latest', include_tx=False, include_staking_tx=True, endpoint=test_net)
```
Fetch block signer addresses (`include_signers=True`) as a list
```
signers = blockchain.get_block_by_number(block_num=9017724, include_signers=True, endpoint=test_net)['signers']
```
Or, alternatively, use the direct `get_block_signers` method:
```
signers = blockchain.get_block_signers(block_num=9017724, endpoint=test_net)
```
Fetch the public keys for signers
```
signers_keys = blockchain.get_block_signers_keys(block_num=9017724, endpoint=test_net)
```
Check if an address is a signer for a block
```
is_block_signer = blockchain.is_block_signer(block_num=9017724, address='one1yc06ghr2p8xnl2380kpfayweguuhxdtupkhqzw', endpoint=test_net)
```
Fetch the number of blocks signed by a particular validator for the last epoch
```
number_signed_blocks = blockchain.get_signed_blocks(address='one1yc06ghr2p8xnl2380kpfayweguuhxdtupkhqzw', endpoint=test_net)
```
Fetch a list of validators and their public keys for specific epoch number
```
validators = blockchain.get_validators(epoch=12, endpoint=test_net)
validator_keys = blockchain.get_validator_keys(epoch=12, endpoint=test_net)
```
Fetch number of transactions
```
tx_count = blockchain.get_block_transaction_count_by_number(block_num='latest', endpoint=test_net)
```
Fetch number of staking transactactions
```
stx_count = blockchain.get_block_staking_transaction_count_by_number(block_num='latest', endpoint=test_net)
```
Fetch a list of blocks using the block numbers
```
blocks = blockchain.get_blocks(start_block=0, end_block=2, full_tx=False, include_tx=False, include_staking_tx=False, include_signers=False, endpoint=test_net)
```
###### By block hash
Most of the functions described above can be applied for fetching information about a block whose hash is known, for example:
```
block_hash = '0x44fa170c25f262697e5802098cd9eca72889a637ea52feb40c521f2681a6d720'
block = blockchain.get_block_by_hash(block_hash=block_hash, endpoint=test_net)
block_with_full_tx = blockchain.get_block_by_hash(block_hash=block_hash, full_tx=True, include_tx=True, include_staking_tx=True, endpoint=test_net)
block_with_only_staking_tx = blockchain.get_block_by_hash(block_hash=block_hash, include_tx=False, include_staking_tx=True, endpoint=test_net)
signers = blockchain.get_block_by_hash(block_hash=block_hash, include_signers=True, endpoint=test_net)['signers']
tx_count = blockchain.get_block_transaction_count_by_hash(block_hash=block_hash, endpoint=test_net)
stx_count = blockchain.get_block_staking_transaction_count_by_hash(block_hash=block_hash, endpoint=test_net)
```
#### Staking
```
from pyhmy import staking
validator_addr = 'one1xjanr7lgulc0fqyc8dmfp6jfwuje2d94xfnzyd'
delegator_addr = 'one1y2624lg0mpkxkcttaj0c85pp8pfmh2tt5zhdte'
```
##### Validation
```
all_validators = staking.get_all_validator_addresses(endpoint=test_net)							# list of addresses
validator_information = staking.get_validator_information(validator_addr, endpoint=test_net)	# dict with all info
validator_information_100 = staking.get_all_validator_information(page=0, endpoint=test_net)	# for all use page=-1
elected_validators = staking.get_elected_validator_addresses(endpoint=test_net)					# list of addresses
validators_for_epoch = staking.get_validators(epoch=73772, endpoint=test_net)					# dict with list of validators and balance
validators_information_100_for_block = staking.get_all_validator_information_by_block_number(block_num=9017724, page=0, endpoint=test_net)
validator_keys_for_epoch = staking.get_validator_keys(epoch=73772, endpoint=test_net)			# list of public keys
validator_information_at_block = staking.get_validator_information_by_block_number(validator_addr, block_num=9017724, endpoint=test_net)
self_delegation = staking.get_validator_self_delegation(validator_addr, endpoint=test_net)
total_delegation = staking.get_validator_total_delegation(validator_addr, endpoint=test_net)
```
##### Delegation
```
delegation_information = staking.get_all_delegation_information(page=-1, endpoint=test_net)
delegations_by_delegator = staking.get_delegations_by_delegator(delegator_addr, test_net)
delegations_by_delegator_at_block = staking.get_delegations_by_delegator_by_block_number(delegator_addr, block_num=9017724, endpoint=test_net)
delegation_by_delegator_and_validator = staking.get_delegation_by_delegator_and_validator(delegator_addr, validator_addr, test_net)
avail_redelegation_balance = staking.get_available_redelegation_balance(delegator_addr, test_net)
delegations_by_validator = staking.get_delegations_by_validator(validator_addr, test_net)		# list of delegations made to this validator, each a dictionary
```
##### Network
```
utility_metrics = staking.get_current_utility_metrics(test_net)
network_info = staking.get_staking_network_info(test_net)
super_committees = staking.get_super_committees(test_net)
super_committees_current = super_committees['current']		# list of voting committees as a dict
super_committees_previous = super_committees['previous']
total_staking = staking.get_total_staking(endpoint=test_net)	# by all validators, only for beaconchain
median_stake_snapshot = staking.get_raw_median_stake_snapshot(test_net)
```
##### Validator class
Instantiate a validator object and load it from the chain
```
from pyhmy.validator import Validator
validator = Validator(validator_addr)
validator.load_from_blockchain(test_net)
```
Create a new validator object and load from dictionary
```
from pyhmy.numbers import convert_one_to_atto
validator = Validator('one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9')
info = {
        'name': 'Alice',
        'identity': 'alice',
        'website': 'alice.harmony.one',
        'details': "Don't mess with me!!!",
        'security-contact': 'Bob',
        'min-self-delegation': convert_one_to_atto(10000),
        'amount': convert_one_to_atto(10001),
        'max-rate': '0.9',
        'max-change-rate': '0.05',
        'rate': '0.01',
        'bls-public-keys': ['0xb9486167ab9087ab818dc4ce026edb5bf216863364c32e42df2af03c5ced1ad181e7d12f0e6dd5307a73b62247608611'],
        'max-total-delegation': convert_one_to_atto(40000)
    }
validator.load(info)
```
Sign a validator creation transaction
```
signed_create_tx_hash = validator.sign_create_validator_transaction(
            nonce = 2,
            gas_price = 1,
            gas_limit = 100,
            private_key = '4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48',
            chain_id = None).rawTransaction.hex()
```
To edit validator, change its parameters using the `setter` functions, for example, `validator.set_details`, except the  `rate`, `bls_keys_to_add` and `bls_keys_to_remove` which can be passed to the below function:
```
signed_edit_tx_hash = validator.sign_edit_validator_transaction(
            nonce = 2,
            gas_price = 1,
            gas_limit = 100,
            rate = '0.06',
            bls_keys_to_add = "0xb9486167ab9087ab818dc4ce026edb5bf216863364c32e42df2af03c5ced1ad181e7d12f0e6dd5307a73b62247608611",
            bls_keys_to_remove = '0xb9486167ab9087ab818dc4ce026edb5bf216863364c32e42df2af03c5ced1ad181e7d12f0e6dd5307a73b62247608612',
            private_key = '4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48',
            chain_id = 2).rawTransaction.hex()
```

### Transactions
```
from pyhmy import transaction
```
##### Pool
```
pending_tx = transaction.get_pending_transactions(test_net)
pending_stx = transaction.get_pending_staking_transactions(test_net)
tx_error_sink = transaction.get_transaction_error_sink(test_net)
stx_error_sink = transaction.get_staking_transaction_error_sink(test_net)
pool_stats = transaction.get_pool_stats(test_net)
pending_cx_receipts = transaction.get_pending_cx_receipts(test_net)
```
##### Fetching transactions
```
tx_hash = '0x500f7f0ee70f866ba7e80592c06b409fabd7ace018a9b755a7f1f29e725e4423'
block_hash = '0xb94bf6e8a8a970d4d42dfe42f7f231af0ff7fd54e7f410395e3b306f2d4000d4'
tx = transaction.get_transaction_by_hash(tx_hash, test_net)			# dict with tx-level info like from / to / gas
tx_from_block_hash = transaction.get_transaction_by_block_hash_and_index(block_hash, tx_index=0, endpoint=test_net)
tx_from_block_number = transaction.get_transaction_by_block_number_and_index(9017724, tx_index=0, endpoint=test_net)
tx_receipt = transaction.get_transaction_receipt(tx_hash, test_net)
```
##### Fetching staking transactions
```
stx_hash = '0x3f616a8ef34f111f11813630cdcccb8fb6643b2affbfa91d3d8dbd1607e9bc33'
block_hash = '0x294dc88c7b6f3125f229a3cfd8d9b788a0bcfe9409ef431836adcd83839ba9f0'	# block number 9018043
stx = transaction.get_staking_transaction_by_hash(stx_hash, test_net)
stx_from_block_hash = transaction.get_staking_transaction_by_block_hash_and_index(block_hash, tx_index=0, endpoint=test_net)
stx_from_block_number = transaction.get_staking_transaction_by_block_number_and_index(9018043, tx_index=0, endpoint=test_net)
```
##### Cross shard transactions
```
cx_hash = '0xd324cc57280411dfac5a7ec2987d0b83e25e27a3d5bb5d3531262387331d692b'
cx_receipt = transaction.get_cx_receipt_by_hash(cx_hash, main_net_shard_1)	# the shard which receives the tx
tx_resent = transaction.resend_cx_receipt(cx_hash, main_net)				# beacon chain
```
##### Sending transactions
Sign it with your private key and use `send_raw_transaction`
```
from pyhmy import signing
tx = {
 'chainId': 2,
 'from': 'one18t4yj4fuutj83uwqckkvxp9gfa0568uc48ggj7',
 'gas': 6721900,
 'gasPrice': 1000000000,
 'nonce': 6055,
 'shardID': 0,
 'to': 'one1ngt7wj57ruz7kg4ejp7nw8z7z6640288ryckh9,
 'toShardID': 0,
 'value': 500000000000000000000
}
transaction.send_raw_transaction(signing.sign_transaction(tx, '01F903CE0C960FF3A9E68E80FF5FFC344358D80CE1C221C3F9711AF07F83A3BD').rawTransaction.hex(), test_net)
```
A similar approach can be followed for staking transactions
```
from pyhmy import staking_structures, staking_signinge
tx = {
  'chainId': 2,
 'delegatorAddress': 'one18t4yj4fuutj83uwqckkvxp9gfa0568uc48ggj7',
 'directive': staking_structures.Directive.CollectRewards,
 'gasLimit': 6721900,
 'gasPrice': 1,
 'nonce': 6056
}
transaction.send_raw_staking_transaction(staking_signing.sign_staking_transaction(tx, private_key = '01F903CE0C960FF3A9E68E80FF5FFC344358D80CE1C221C3F9711AF07F83A3BD').rawTransaction.hex(), test_net)
```
### Contracts
```
from pyhmy import contract
from pyhmy.util import convert_one_to_hex
contract_addr = 'one1rcs4yy4kln53ux60qdeuhhvpygn2sutn500dhw'
```
Call a contract without saving state
```
from pyhmy import numbers
result = contract.call(convert_one_to_hex(contract_addr), 'latest', value=hex(int(numbers.convert_one_to_atto(5)))
, gas_price=hex(1), gas=hex(100000), endpoint=test_net)
```
Estimate gas required for a smart contract call
```
estimated_gas = contract.estimate_gas(convert_one_to_hex(contract_addr), endpoint=test_net)
```
Fetch the byte code of the contract
```
byte_code = contract.get_code(convert_one_to_hex(contract_addr), 'latest', endpoint=test_net)
```
Get storage in the contract at `key`
```
storage = contract.get_storage_at(convert_one_to_hex(contract_addr), key='0x0', block_num='latest', endpoint=test_net)
```
Calling a function on a contract needs the contract ABI. The ABI can be obtained by compiling the contract.
```
from web3 import Web3
from web3 import providers
from pyhmy.util import convert_one_to_hex
contract_abi = '[{"constant":true,"inputs":[],"name":"manager","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"pickWinner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getPlayers","outputs":[{"name":"","type":"address[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"enter","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"players","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]'
w3 = Web3(providers.HTTPProvider(test_net))
lottery = w3.eth.contract(abi=contract_abi, address=convert_one_to_hex('one1rcs4yy4kln53ux60qdeuhhvpygn2sutn500dhw'))
lottery.functions.getPlayers().call()
```
To actually participate in a contract, you can sign a transaction from your account to it.
```
from pyhmy import signing
contract_addr = 'one1rcs4yy4kln53ux60qdeuhhvpygn2sutn500dhw'
tx = {
 'chainId': 2,
 'from': 'one18t4yj4fuutj83uwqckkvxp9gfa0568uc48ggj7',
 'gas': 6721900,
 'gasPrice': 1000000000,
 'nonce': 6054,
 'shardID': 0,
 'to': contract_addr,
 'toShardID': 0,
 'value': 500000000000000000000
}
tx_hash = transaction.send_raw_transaction(signing.sign_transaction(tx, '01F903CE0C960FF3A9E68E80FF5FFC344358D80CE1C221C3F9711AF07F83A3BD').rawTransaction.hex(), test_net)
```
To deploy a contract, sign a transaction from your account without a `to` field and with the byte code as `data` and send it.
```
from pyhmy import signing
from pyhmy import transaction
contract_tx = {
 'chainId': 2,	# test net data
 'data': '0x608060405234801561001057600080fd5b50600436106100415760003560e01c8063445df0ac146100465780638da5cb5b14610064578063fdacd576146100ae575b600080fd5b61004e6100dc565b6040518082815260200191505060405180910390f35b61006c6100e2565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6100da600480360360208110156100c457600080fd5b8101908080359060200190929190505050610107565b005b60015481565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141561016457806001819055505b5056fea265627a7a723158209b80813a158b44af65aee232b44c0ac06472c48f4abbe298852a39f0ff34a9f264736f6c63430005100032', 	# Migrations.sol
 'from': 'one18t4yj4fuutj83uwqckkvxp9gfa0568uc48ggj7',
 'gas': 6721900,
 'gasPrice': 1000000000,
 'nonce': 6049,
 'shardID': 0,
 'toShardID': 0
}
ctx_hash = transaction.send_raw_transaction(signing.sign_transaction(contract_tx, private_key = '01F903CE0C960FF3A9E68E80FF5FFC344358D80CE1C221C3F9711AF07F83A3BD').rawTransaction.hex(), test_net)
# the below may be need a time gap before the transaction reaches the chain
contract_address = transaction.get_transaction_receipt(ctx_hash, test_net)['contractAddress']
```
### Signing transactions
```
from pyhmy import signing
```
Create a `transaction_dict` with the parameters, and supply your private key to sign (but not submit) a transaction. A signed transaction can be submitted using `transaction.sendRawTransaction`.
```
transaction_dict = {
        'nonce': 2,
        'gasPrice': 1,
        'gas': 100,             # signing.py uses Ether, which by default calls it gas
        'to': '0x14791697260e4c9a71f18484c9f997b308e59325',
        'value': 5,
        'shardID': 0,
        'toShardID': 1,
        'chainId': 'HmyMainnet'
    }
signed_tx = signing.sign_transaction(transaction_dict, private_key = '4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48')
signed_hash = signed_tx.rawTransaction.hex()
```
For a transaction with is Ethereum-like, the `shardID` and `toShardID` are optional, which implies that the transaction is not cross-shard.
```
transaction_dict = {
        'nonce': 2,
        'gasPrice': 1,
        'gas': 100,             # signing.py uses Ether, which by default calls it gas
        'to': '0x14791697260e4c9a71f18484c9f997b308e59325',
        'value': 5,
    }
signed_tx = signing.sign_transaction(transaction_dict, private_key = '4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48')
signed_hash = signed_tx.rawTransaction.hex()
```
The `chainId` parameter is also optional, and [according to Ethereum](https://github.com/ethereum/eth-account/blob/00e7b10005c5fa7090086fcef37a76296c524e17/eth_account/_utils/transactions.py#L122), it should not be passed if "you want a transaction that can be replayed across networks." A full list of the possible values of `chainId` is provided below. You can pass either the `str` or the `int`. The RPC API may, however, reject the transaction, which is why it is recommended to pass either `1` or `2` for `mainnet` and `testnet` respectively.
```
Default = 0,
EthMainnet = 1,
Morden = 2,
Ropsten = 3,
Rinkeby = 4,
RootstockMainnet = 30,
RootstockTestnet = 31,
Kovan = 42,
EtcMainnet = 61,
EtcTestnet = 62,
Geth = 1337,
Ganache = 0,
HmyMainnet = 1,
HmyTestnet = 2,
HmyLocal = 2,
HmyPangaea = 3,
```
### Signing staking transactions
```
from pyhmy import staking_structures, staking_signing
```
To sign a transaction to collect rewards, supply the dictionary containing the `delegatorAddress` and the private key.
```
transaction_dict = {
    'directive': staking_structures.Directive.CollectRewards,
    'delegatorAddress': 'one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9',
    'nonce': 2,
    'gasPrice': 1,
    'gasLimit': 100,
}
signed_tx = staking_signing.sign_staking_transaction(transaction_dict, private_key = '4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48')
```
To sign a transaction to delegate or undelegate, supply the dictionary containing the `delegatorAddress`, the `validatorAddress`, the `amount` to delegate or undelegate, and the private key.
```
transaction_dict = {
        'directive': staking_structures.Directive.Delegate,
        'delegatorAddress': 'one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9',
        'validatorAddress': 'one1xjanr7lgulc0fqyc8dmfp6jfwuje2d94xfnzyd',
        'amount': 5,
        'nonce': 2,
        'gasPrice': 1,
        'gasLimit': 100,
    }
signed_tx = staking_signing.sign_staking_transaction(transaction_dict, '4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48')
transaction_dict = {
        'directive': staking_structures.Directive.Undelegate,
        'delegatorAddress': 'one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9',
        'validatorAddress': 'one1xjanr7lgulc0fqyc8dmfp6jfwuje2d94xfnzyd',
        'amount': 5,
        'nonce': 2,
        'gasPrice': 1,
        'gasLimit': 100,
    }
signed_tx = staking_signing.sign_staking_transaction(transaction_dict, '4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48')
```
For validator-related transactions, see the [section on the Validator class](#validator-class).
## Keeping your private key safe
You need `eth-keyfile` installed
```
pip install eth-keyfile
```
In a `Python` shell, you can save or load the key into / from a key file.
```
import eth_keyfile
from eth_utils import to_bytes, to_hex
import json
keyfile = eth_keyfile.create_keyfile_json(to_bytes(hexstr='01F903CE0C960FF3A9E68E80FF5FFC344358D80CE1C221C3F9711AF07F83A3BD'), b'password')
with open('keyfile.json', 'w+') as outfile:
    json.dump(keyfile, outfile)

private_key = to_hex(eth_keyfile.extract_key_from_keyfile('keyfile.json', b'password'))[2:].upper()
```
