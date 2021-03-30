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

if "difeng" not in name_dict.keys():
    #create a user
    cli.single_call("hmy keys add difeng")

if "dfxx" not in name_dict.keys():
    #create a user
    cli.single_call("hmy keys add dfxx")

if "test1" not in name_dict.keys():
    #create a user
    cli.single_call("hmy keys add test1")

#get keystore path
print("Your accounts are store in %s"%(cli.get_account_keystore_path()))

# get address of account
difeng_address = cli.get_address("difeng")
dfxx_address = cli.get_address("dfxx")
test1_address = cli.get_address("test1")
print("The one address of account difeng is %s"%(difeng_address))
print("The one address of account dfxx is %s"%(dfxx_address))

#remove address
cli.remove_address(test1_address)
print("%s has been successfully removed"%test1_address)

#get balace of account difeng
balance = cli.single_call("hmy balances %s"%(difeng_address))
print("The balance of difeng is %s"%balance)




