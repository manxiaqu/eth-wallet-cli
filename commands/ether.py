import click
from web3 import Web3
from pkg.txmanager import TxManager
import commands.options as options
import pkg.utils as utils


transfer_options = [
    options.rpc_option,
    options.private_key_option,
    options.sender_option,
    options.sender_index_option,
    options.receiver_option,
    options.ether_amount_option,
    options.ks_option,
    options.pw_without_ensure_option,
]
get_balance_options = [
    options.rpc_option,
    options.account_option,
]


@click.group()
def ether():
    """
    Interact with ethereum to send ether or query ether balance
    """
    pass


@click.command()
@options.add_options(transfer_options)
def transfer(rpc, priv, sender, index, to, amount, ks, pw):
    """
    Transfer ether from sender account to receiver account
    """

    sender = utils.get_account(ks, priv, sender, index, pw)
    # change ether to uint in wei.
    value = Web3.toWei(amount, 'ether')
    TxManager(rpc).transfer_ether(sender, to, value)


@click.command()
@options.add_options(get_balance_options)
def get_balance(rpc, account):
    """
    Get the ether balance of ethereum account
    """

    balance_ether = TxManager(rpc).get_balance(account)
    print("The balance of account {} is {} ether".format(account, balance_ether))


ether.add_command(transfer)
ether.add_command(get_balance)
