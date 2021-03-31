import sys
sys.path.append("../")
from pyhmy import account
from pyhmy import blockchain
from pyhmy import cli
import os

explorer_endpoint = 'http://localhost:9599'
endpoint_shard_one = 'http://localhost:9501'
local_test_address = 'one1zksj3evekayy90xt4psrz8h6j2v3hla4qwz4ur'
test_validator_address = 'one18tvf56zqjkjnak686lwutcp5mqfnvee35xjnhc'
genesis_block_number = 0
test_block_number = 1

#get local test key from keystore
keys = [item.split(".")[0] for item in os.listdir("/root/go/src/github.com/harmony-one/harmony/.hmy/keystore")]
for key in keys:
    balance = account.get_balance(key)
    print("There are %d one in %s"%(balance,key))


#current block number
cur_block_num = blockchain.get_block_number()

#get balance at certain block
account.get_balance_by_block(keys[-1],cur_block_num)

#get balance on all shards
account.get_balance_on_all_shards(keys[-1])

#restore keys[-1] from keystore by cli
cli.single_call("hmy keys import-ks /root/go/src/github.com/harmony-one/harmony/.hmy/keystore/%s.key"%key)
balance_before = account.get_balance(keys[-1])

#send 2 one from keys[-1] to local_test_address
cli.single_call("hmy transfer --from %s --to %s --amount %d --from-shard %s --to-shard %s"%(key,local_test_address,2,0,0))
balance_after= account.get_balance(keys[-1])

diff = balance_before - balance_after
print("The difference between before and after is %d"%(diff))



