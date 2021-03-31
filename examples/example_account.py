import sys
sys.path.append("../")
from pyhmy import account

explorer_endpoint = 'http://localhost:9599'
endpoint_shard_one = 'http://localhost:9501'
local_test_address = 'one1zksj3evekayy90xt4psrz8h6j2v3hla4qwz4ur'
test_validator_address = 'one18tvf56zqjkjnak686lwutcp5mqfnvee35xjnhc'
genesis_block_number = 0
test_block_number = 1


#get account balance
balance = account.get_balance(local_test_address)
print("The balance of %s is %d"%(local_test_address,balance))
