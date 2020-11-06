from web3 import Web3
from eth_account import Account
import pkg.erc20_contract as TokenContract
from eth_abi import encode_single


class TxManager(object):
    """
    Transaction manager to send/get transactions
    """

    def __init__(self, rpc):
        self.rpc = rpc
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        # TODO: check w3 is connected
        self.w3.isConnected()

    def transfer_ether(self, f, to, value):
        # fetch nonce of sender who should be decrypted
        tx = {
            'nonce': self.w3.eth.getTransactionCount(f.address),
            'gasPrice': self.w3.eth.gasPrice,
            'to': Web3.toChecksumAddress(to),
            'value': value,
            'gas': 21000,
        }

        sign_and_send_transaction(tx, f.key, self.w3)

    def transfer_erc20_token(self, sender, to, amount, token):
        # get token decimal and convert amount in same uint
        token_ins = self.w3.eth.contract(address=token, abi=TokenContract.erc20_abi)
        decimals = token_ins.functions.decimals().call()

        value = int(amount) * (10**decimals)

        # build token transfer tx
        data = encode_single('(address,uint256)', [to, value])
        tx = {
            'to': Web3.toChecksumAddress(token),
            'nonce': self.w3.eth.getTransactionCount(sender.address),
            'gasPrice': self.w3.eth.gasPrice,
            'data': '0xa9059cbb' + data.hex(),
            'gas': 70000,
        }

        sign_and_send_transaction(tx, sender.key, self.w3)

    def deploy_erc20_token(self, sender, name, symbol):
        data = encode_single('(string,string)', [name, symbol])
        tx = {
            'nonce': self.w3.eth.getTransactionCount(sender.address),
            'gasPrice': self.w3.eth.gasPrice,
            'data': TokenContract.erc20_bytecode + data.hex(),
            'gas': 2000000,
        }

        sign_and_send_transaction(tx, sender.key, self.w3)

    def send_transaction(self, sender, tx):
        print(sender.address)
        tx['nonce'] = self.w3.eth.getTransactionCount(sender.address)
        print(tx)
        sign_and_send_transaction(tx, sender.key, self.w3)

    def get_balance(self, address):
        balance = self.w3.eth.getBalance(Web3.toChecksumAddress(address))
        # change the balance in uint ether
        return Web3.fromWei(balance, 'ether')

    def get_erc20_token_balance(self, token, address):
        data = encode_single('(address)', [address])
        tx = {
            'to': Web3.toChecksumAddress(token),
            'data': '0x70a08231' + data.hex(),
        }
        balance = int(self.w3.eth.call(tx).hex(), 16)

        tx = {
            'to': Web3.toChecksumAddress(token),
            'data': '0x95d89b41',
        }
        symbol = self.w3.eth.call(tx)

        tx = {
            'to': Web3.toChecksumAddress(token),
            'data': '0x313ce567',
        }
        decimals = int(self.w3.eth.call(tx).hex(), 16)
        balance = balance / (10 ** decimals)
        return balance, symbol

    def get_total_supply(self, token):
        tx = {
            'to': Web3.toChecksumAddress(token),
            'data': '0x18160ddd',
        }
        supply = int(self.w3.eth.call(tx).hex(), 16)

        tx = {
            'to': Web3.toChecksumAddress(token),
            'data': '0x95d89b41',
        }
        symbol = self.w3.eth.call(tx)

        tx = {
            'to': Web3.toChecksumAddress(token),
            'data': '0x313ce567',
        }
        decimals = int(self.w3.eth.call(tx).hex(), 16)
        balance = supply/(10**decimals)
        return balance, symbol

    def get_transaction_info(self, tx):
        return self.w3.eth.getTransaction(tx)

    def get_transaction_receipt_info(self, tx):
        return self.w3.eth.getTransactionReceipt(tx)


def sign_and_send_transaction(tx, key, w3):
    # sign transaction
    signed_tx = Account.sign_transaction(tx, key)

    # send transaction
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print("Successfully send transaction, hash: {}".format(tx_hash.hex()))

    # wait for tx packed in block
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    print("Transaction execution result: {}".format(tx_receipt.status == 1))
    # check this is a contract creation tx or not

    if tx_receipt['contractAddress'] is not None:
        print("Successfully create contract: {}".format(tx_receipt['contractAddress']))
