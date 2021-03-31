import sys
sys.path.append("../")
from pyhmy import cli
import os

#set up binnary path
env = cli.download("./bin/test", replace=False)
cli.environment.update(env)
new_path = os.getcwd() + "/bin/test"
cli.set_binary(new_path)
print("The binary path is %s"%(cli.get_binary_path()))

#get a dict of account names
name_dict = cli.get_accounts_keystore()
print(name_dict)

#get keystore path
print("Your accounts are store in %s"%(cli.get_account_keystore_path()))

if "difeng" not in name_dict.keys():
    #create a user
    cli.single_call("hmy keys add difeng")
    print("difeng has been successfully created")

if "dfxx" not in name_dict.keys():
    #create a user
    cli.single_call("hmy keys add dfxx")
    print("dfxx has been successfully created")

if "test1" not in name_dict.keys():
    #create a user
    cli.single_call("hmy keys add test1")


#get address of account
difeng_address = cli.get_address("difeng")
dfxx_address = cli.get_address("dfxx")
test1_address = cli.get_address("test1")
print("The one address of account difeng is %s"%(difeng_address))
print("The one address of account dfxx is %s"%(dfxx_address))

#import keystore
cli.single_call("hmy keys import-ks /root/go/src/github.com/harmony-one/harmony/.hmy/keystore/one103q7qe5t2505lypvltkqtddaef5tzfxwsse4z7.keyimport_key1")


#remove address
cli.remove_address(test1_address)
print("%s has been successfully removed"%test1_address)

#go to website https://faucet.pops.one/
#input your address and get test one
#use --node testnet

#get balace of account dfxx
balance = cli.single_call("hmy --node=https://api.s0.b.hmny.io balances %s"%(dfxx_address))
print("The balance of dfxx is %s"%balance)

#transfer 200 one to difeng account
#"from", "to", "amount", "from-shard", "to-shard"
cli.single_call("transfer --node=https://api.s0.b.hmny.io  --from %s  --to %s --amount %s --from-shard %d --to-shard %d")%(dfxx_address,difeng_address,"200",0,0)

#get balace of account difeng
balance = cli.single_call("hmy --node=https://api.s0.b.hmny.io balances %s"%(difeng_address))
print("The balance of difeng is %s"%balance)
