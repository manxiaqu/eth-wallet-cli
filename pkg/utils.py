from eth_account import Account
from pkg.keystore import KeyStore
import pprint

pp = pprint.PrettyPrinter(indent=4)


def get_account(ks, priv, address, index, pw):
    if priv is not None:
        account = Account.from_key(priv)
    else:
        accounts = KeyStore(ks)
        if address is not None:
            account = accounts.decrypt_account_by_address(address, pw)

        if index is not None:
            index = int(index)
            account = accounts.decrypt_account_by_index(index, pw)
    return account


def pretty_print_dict(dict_data):
    # parsed = json.loads(json_data)
    # print(pp.pformat(dict_data))
    pp.pprint(dict_data)
    # print(json.dumps(dict_data, indent=4, sort_keys=True))