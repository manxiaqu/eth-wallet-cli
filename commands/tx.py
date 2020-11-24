import click
from web3.exceptions import TransactionNotFound

import commands.options as options
import pkg.utils as utils
from pkg.txmanager import TxManager
from web3 import Web3

send_options = [
    options.rpc_option,
    options.ks_option,
    options.private_key_option,
    options.sender_option,
    options.sender_index_option,
    options.pw_without_ensure_option,
    options.receiver_option,
    options.ether_amount_option,
    options.data_option,
    options.gas_option,
    options.gas_price_option,
]
get_options = [
    options.rpc_option,
    options.tx_hash_option,
]
receipt_options = [
    options.rpc_option,
    options.tx_hash_option,
]


@click.group()
def tx():
    """
    Interact with ethereum network to send transaction or get info
    """


# sign and send a transaction to eth network
@click.command()
@options.add_options(send_options)
def send(rpc, ks, priv, sender, index, pw, to, amount, data, gas, gas_price):
    """
    Sign and send a transaction to the ethereum network
    """
    sender = utils.get_account(ks, priv, sender, index, pw)
    # change ether to uint in wei.
    value = Web3.toWei(amount, 'ether')
    if data is None:
        data = ''
    tx = {
        'to': Web3.toChecksumAddress(to),
        'value': value,
        'gas': int(gas),
        'gasPrice': int(gas_price),
        'data': data,
    }

    try:
        TxManager(rpc).send_transaction(sender, tx)
    except ValueError as e:
        print("Send tx failed")


# get details of a transaction
@click.command()
@options.add_options(get_options)
def get(rpc, tx):
    """
    Get detail info of ethereum transaction
    """

    try:
        info = TxManager(rpc).get_transaction_info(tx)
        utils.pretty_print_dict(info)
    except TransactionNotFound:
        print("Tx {} not found".format(tx))


@click.command()
@options.add_options(receipt_options)
def receipt(rpc, tx):
    """
    Get receipt of ethereum transaction
    """
    # validate tx

    try:
        info = TxManager(rpc).get_transaction_receipt_info(tx)
        print(info)
    except TransactionNotFound:
        print("Tx receipt of {} not found".format(tx))


tx.add_command(send)
tx.add_command(get)
tx.add_command(receipt)
