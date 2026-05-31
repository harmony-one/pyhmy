# Pyhmy Usage Samples

This directory contains runnable samples demonstrating how to use the pyhmy SDK.

## Prerequisites

```bash
pip install pyhmy web3
```

## Samples

### 1. Account Operations

```python
# samples/account_ops.py
"""Example: Account balance, nonce, and transaction history queries."""
from pyhmy import account, util

# Testnet endpoints
test_net = "https://api.s0.b.hmny.io"
test_address = "one18t4yj4fuutj83uwqckkvxp9gfa0568uc48ggj7"

# Get balance in ATTO
balance = account.get_balance(test_address, endpoint=test_net)
print(f"Balance: {balance} ATTO")

# Convert to ONE
from pyhmy.numbers import convert_atto_to_one
print(f"Balance: {convert_atto_to_one(balance)} ONE")

# Get nonce
nonce = account.get_account_nonce(test_address, endpoint=test_net)
print(f"Nonce: {nonce}")

# Transaction history
tx_history = account.get_transaction_history(
    test_address, page=0, page_size=5, include_full_tx=True, endpoint=test_net
)
print(f"Recent transactions: {len(tx_history)}")

# Check if address is valid
print(f"Is valid: {account.is_valid_address(test_address)}")
print(f"Is valid (hex): {account.is_valid_address('0x1234')}")

# Address conversion
hex_addr = util.convert_one_to_hex(test_address)
one_addr = util.convert_hex_to_one(hex_addr)
print(f"Hex: {hex_addr}")
print(f"Back to ONE: {one_addr}")
```

### 2. Blockchain Queries

```python
# samples/blockchain_ops.py
"""Example: Fetching blockchain data (blocks, headers, network info)."""
from pyhmy import blockchain
from decimal import Decimal

test_net = "https://api.s0.b.hmny.io"

# Node info
chain_id = blockchain.chain_id(endpoint=test_net)
print(f"Chain ID: {chain_id}")

metadata = blockchain.get_node_metadata(endpoint=test_net)
print(f"Shard: {metadata['shard-id']}")
print(f"Role: {metadata['role']}")
print(f"Version: {metadata['version']}")

# Current block number
block_num = blockchain.get_block_number(endpoint=test_net)
print(f"Current block: {block_num}")

# Get latest block
block = blockchain.get_block_by_number(
    block_num='latest', include_tx=True, endpoint=test_net
)
print(f"Latest block hash: {block['hash']}")
print(f"Transactions in block: {len(block.get('transactions', []))}")

# Supply info
circ_supply = Decimal(blockchain.get_circulating_supply(endpoint=test_net))
print(f"Circulating supply: {circ_supply} ONE")

# Epoch info
epoch = blockchain.get_current_epoch(endpoint=test_net)
print(f"Current epoch: {epoch}")

# Gas price
gas_price = blockchain.get_gas_price(endpoint=test_net)
print(f"Gas price: {gas_price}")

# Sharding structure
shards = blockchain.get_sharding_structure(endpoint=test_net)
for shard in shards:
    print(f"Shard {shard['shardID']}: {shard['http']}")
```

### 3. Transactions

```python
# samples/transaction_ops.py
"""Example: Fetching and sending transactions."""
from pyhmy import transaction, signing

test_net = "https://api.s0.b.hmny.io"
test_net_shard_1 = "https://api.s1.b.hmny.io"

# Fetch a transaction by hash
tx_hash = "0x500f7f0ee70f866ba7e80592c06b409fabd7ace018a9b755a7f1f29e725e4423"
tx = transaction.get_transaction_by_hash(tx_hash, endpoint=test_net)
if tx:
    print(f"From: {tx.get('from')}")
    print(f"To: {tx.get('to')}")
    print(f"Value: {tx.get('value')} ATTO")
    print(f"Gas: {tx.get('gas')}")

# Get transaction receipt
receipt = transaction.get_transaction_receipt(tx_hash, endpoint=test_net)
if receipt:
    print(f"Status: {receipt.get('status')}")
    print(f"Gas used: {receipt.get('gasUsed')}")

# Pool info
pool_stats = transaction.get_pool_stats(endpoint=test_net)
print(f"Pool stats: {pool_stats}")

# Cross shard receipt
cx_receipt = transaction.get_cx_receipt_by_hash(
    tx_hash, endpoint=test_net_shard_1
)
```

### 4. Staking Operations

```python
# samples/staking_ops.py
"""Example: Staking and delegation queries."""
from pyhmy import staking

test_net = "https://api.s0.b.hmny.io"
validator_addr = "one1xjanr7lgulc0fqyc8dmfp6jfwuje2d94xfnzyd"
delegator_addr = "one1y2624lg0mpkxkcttaj0c85pp8pfmh2tt5zhdte"

# List all validators
all_validators = staking.get_all_validator_addresses(endpoint=test_net)
print(f"Total validators: {len(all_validators)}")

# Get validator info
info = staking.get_validator_information(validator_addr, endpoint=test_net)
if info:
    v = info.get("validator", {})
    print(f"Validator: {v.get('name', 'N/A')}")
    print(f"Rate: {v.get('rate', 'N/A')}")
    print(f"Total delegation: {info.get('total-delegation', 'N/A')}")

# Delegation info
delegations = staking.get_delegations_by_delegator(
    delegator_addr, endpoint=test_net
)
for d in delegations:
    print(f"Delegated to {d['validator_address']}: {d['amount']} ATTO")

# Network info
net_info = staking.get_staking_network_info(endpoint=test_net)
print(f"Total staking: {net_info.get('total-staking', 'N/A')}")

# Utility metrics
metrics = staking.get_current_utility_metrics(endpoint=test_net)
print(f"Staked %: {metrics.get('CurrentStakedPercentage', 'N/A')}")
```

### 5. Smart Contracts

```python
# samples/contract_ops.py
"""Example: Smart contract interaction."""
from pyhmy import contract, signing, transaction
from pyhmy.util import convert_one_to_hex, convert_hex_to_one

test_net = "https://api.s0.b.hmny.io"
contract_addr = "one1rcs4yy4kln53ux60qdeuhhvpygn2sutn500dhw"

# Get contract code
hex_addr = convert_one_to_hex(contract_addr)
code = contract.get_code(hex_addr, "latest", endpoint=test_net)
print(f"Has code: {code != '0x'}")

# Get storage at key
storage = contract.get_storage_at(
    hex_addr, "0x0", "latest", endpoint=test_net
)
print(f"Storage at 0x0: {storage}")

# Call contract (read-only)
result = contract.call(
    hex_addr, "latest", gas_price=hex(1), gas=hex(100000), endpoint=test_net
)
print(f"Call result: {result}")

# Estimate gas
gas = contract.estimate_gas(
    hex_addr, data="0x", endpoint=test_net
)
print(f"Estimated gas: {gas}")

# Get contract address from deployment tx
tx_hash = "0xa605852dd2fa39ed42e101c17aaca9d344d352ba9b24b14b9af94ec9cb58b31f"
addr = contract.get_contract_address_from_hash(tx_hash, endpoint=test_net)
print(f"Contract address from tx: {addr}")
```

### 6. Signing Transactions

```python
# samples/signing_ops.py
"""Example: Signing regular and staking transactions."""
from pyhmy import signing, staking_signing, staking_structures, transaction

PRIVATE_KEY = "4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48"

# Sign a regular (non-staking) transaction
tx_dict = {
    "nonce": 2,
    "gasPrice": 1,
    "gas": 100,
    "to": "one1z3u3d9expexf5u03sjzvn7vhkvywtye9nqmmlu",
    "value": 5,
    "shardID": 0,
    "toShardID": 0,
    "chainId": "HmyTestnet",
}
signed_tx = signing.sign_transaction(tx_dict, PRIVATE_KEY)
print(f"Signed tx hash: {signed_tx.hash.hex()}")
print(f"Raw tx (hex): {signed_tx.raw_transaction.to_0x_hex()}")

# To send the transaction (uncomment to actually send):
# tx_hash = transaction.send_raw_transaction(
#     signed_tx.raw_transaction.to_0x_hex(),
#     endpoint="https://api.s0.b.hmny.io"
# )
# print(f"Sent, tx hash: {tx_hash}")

# Sign a staking transaction (collect rewards)
stx_dict = {
    "directive": staking_structures.Directive.CollectRewards,
    "delegatorAddress": "one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9",
    "nonce": 2,
    "gasPrice": 1,
    "gasLimit": 100,
    "chainId": 2,
}
signed_stx = staking_signing.sign_staking_transaction(stx_dict, PRIVATE_KEY)
print(f"Signed staking tx hash: {signed_stx.hash.hex()}")

# Sign a delegation transaction
delegate_dict = {
    "directive": staking_structures.Directive.Delegate,
    "delegatorAddress": "one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9",
    "validatorAddress": "one1xjanr7lgulc0fqyc8dmfp6jfwuje2d94xfnzyd",
    "amount": 5,
    "nonce": 2,
    "gasPrice": 1,
    "gasLimit": 100,
    "chainId": 2,
}
signed_del = staking_signing.sign_staking_transaction(delegate_dict, PRIVATE_KEY)
print(f"Signed delegation tx hash: {signed_del.hash.hex()}")
```

### 7. Creating a Validator

```python
# samples/create_validator.py
"""Example: Creating a new validator using the Validator class."""
from pyhmy.validator import Validator
from pyhmy.numbers import convert_one_to_atto

# Create a validator object
val = Validator("one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9")

# Load configuration
info = {
    "name": "MyValidator",
    "identity": "my-validator-id",
    "website": "https://myvalidator.com",
    "details": "A great validator",
    "security-contact": "admin@myvalidator.com",
    "min-self-delegation": convert_one_to_atto(10000),
    "amount": convert_one_to_atto(10001),
    "max-rate": "0.9",
    "max-change-rate": "0.05",
    "rate": "0.07",
    "bls-public-keys": [
        "0xb9486167ab9087ab818dc4ce026edb5bf216863364c32e42df2af03c5ced1ad181e7d12f0e6dd5307a73b62247608611"
    ],
    "bls-key-sigs": [
        "0x68f800b6adf657b674903e04708060912b893b7c7b500788808247550ab3e186e56a44ebf3ca488f8ed1a42f6cef3a04bd5d2b2b7eb5a767848d3135b362e668ce6bba42c7b9d5666d8e3a83be707b5708e722c58939fe9b07c170f3b7062414"
    ],
    "max-total-delegation": convert_one_to_atto(40000),
}
val.load(info)

# Sign the create validator transaction
signed = val.sign_create_validator_transaction(
    nonce=2,
    gas_price=int(convert_one_to_atto(1)),
    gas_limit=100,
    private_key="4edef2c24995d15b0e25cbd152fb0e2c05d3b79b9c2afd134e6f59f91bf99e48",
    chain_id=2,
)
print(f"Signed create validator tx: {signed.raw_transaction.to_0x_hex()}")

# Check on chain
print(f"Validator exists: {val.does_validator_exist()}")
```
