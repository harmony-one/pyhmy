from web3.auto import w3
from eth_account import Account


def import_keystore(key_path: str, password: str = None):
    with open(key_path) as keyfile:
        encrypted_key = keyfile.read()
        if password is None:
            private_key = encrypted_key
        else:       
            private_key = w3.eth.account.decrypt(encrypted_key, password)

    return Account.from_key(private_key)