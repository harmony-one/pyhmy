import sys
sys.path.append("../")

from pyhmy.cli import (single_call)

from pyhmy.account import (
    get_balance)

from pyhmy.staking import (
    get_all_validator_addresses,
    get_validator_information,
    get_elected_validator_address
)


single_call("hmy keys add test1")



local_test_address = 'one1zksj3evekayy90xt4psrz8h6j2v3hla4qwz4ur'

balance = get_balance(local_test_address)
print(balance)
