import json
import os
from datetime import datetime
from eth_account import Account
from os import listdir
from os.path import isfile, join
Account.enable_unaudited_hdwallet_features()


class KeyStore:
    """
    KeyStore is a manager managing accounts in keystore.
    """
    def __init__(self, path):
        # create dir if not exist
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path
        self.accounts = {}
        self.cur_acct = {}
        self.addresses = []

        # store account list in memory
        self.scan_accounts()

    def scan_accounts(self):
        for i, key_file in enumerate(list_files(self.path)):
            encrypted_account = read_account(key_file)
            address = "0x" + encrypted_account["address"]
            if i == 0:
                self.cur_acct["address"] = address
                self.cur_acct["file"] = key_file
                self.cur_acct["encrypted"] = encrypted_account

            self.accounts[address] = encrypted_account
            self.addresses.append(address)

    def get_accounts(self):
        return self.addresses

    def get_current_account(self):
        return self.cur_acct

    def generate_account(self, pw):
        acct, mnemonic = Account.create_with_mnemonic()
        self.cur_acct = acct

        # encrypt and save
        file_name = generate_key_file_name(acct.address)
        self.encrypt_and_save(acct.key, pw, file_name)

        # print info of user account
        print_account_info(acct, mnemonic, os.path.join(self.path, file_name))

    def import_from_key(self, key, pw):
        acct = Account.from_key(key)

        if acct.address.lower() in self.accounts.keys():
            print("You account {} is already exist in keystore".format(
                acct.address))
            return

        file_name = generate_key_file_name(acct.address)
        self.encrypt_and_save(acct.key, pw, file_name)

        # print info of user account
        print_import_account_info("key", acct,
                                  os.path.join(self.path, file_name))

    def import_from_mnemo(self, mnemo, pw):
        acct = Account.from_mnemonic(mnemo)

        if acct.address.lower() in self.accounts.keys():
            print("You account {} is already exist in keystore".format(
                acct.address))
            return

        file_name = generate_key_file_name(acct.address)
        self.encrypt_and_save(acct.key, pw, file_name)

        # print info of user account
        print_import_account_info("mnemonic", acct,
                                  os.path.join(self.path, file_name))

    def encrypt_and_save(self, key, pw, name):
        encrypted = Account.encrypt(key, pw)

        f = open(os.path.join(self.path, name), "w")
        f.write(json.dumps(encrypted))
        f.close()

    def decrypt_account_by_address(self, address, pw):
        key = Account.decrypt(self.accounts[address.lower()], pw)
        return Account.from_key(key)

    def decrypt_account_by_index(self, index, pw):
        if index >= len(self.addresses):
            # TODO: raise error
            pass
        k = self.addresses[index]

        priv = Account.decrypt(self.accounts[k], pw)
        return Account.from_key(priv)


# read keystore file to get address
def read_account(path):
    f = open(path, "r")
    return json.loads(f.read())


def print_account_info(account, mnemo, save_path):
    print("""
Your new key was generated

Public address of the key: {}
Mnemonic of the key: {}
Path of the secret key file: {}
    
- You can share your public address with anyone. Others need it to interact with you.
- You must NEVER share the secret key or mnemonic with anyone! The key controls access to your funds!
- You must BACKUP your key file! Without the key, it's impossible to access account funds!
- You must REMEMBER your password! Without the password, it's impossible to decrypt the key!
- You must BACKUP your mnemonic! Without the mnemonic, it's impossible to recover the key!
    """.format(account.address, mnemo, save_path))


def print_import_account_info(op, account, save_path):
    print("""
Your {} was imported

Public address of the key: {}
Path of the secret key file: {}
    
- You can share your public address with anyone. Others need it to interact with you.
- You must NEVER share the secret key or mnemonic with anyone! The key controls access to your funds!
- You must BACKUP your key file! Without the key, it's impossible to access account funds!
- You must REMEMBER your password! Without the password, it's impossible to decrypt the key!
- You must BACKUP your mnemonic! Without the mnemonic, it's impossible to recover the key!
    """.format(op, account.address, save_path))


# Keep same with ethereum
def generate_key_file_name(address):
    ts = datetime.utcnow()
    iso8601 = "{}-{}-{}-{}-{}-{}".format(ts.year, ts.month, ts.day, ts.hour,
                                         ts.minute, ts.second)
    return "UTC--{}--{}".format(iso8601, address)


def list_files(dir_path):
    return [join(dir_path, f) for f in listdir(dir_path) if isfile(join(dir_path, f))]