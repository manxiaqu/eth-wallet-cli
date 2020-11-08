import click
import commands.options as options
from pkg.txmanager import TxManager
import pkg.utils as utils


transfer_options = [
    options.rpc_option,
    options.private_key_option,
    options.sender_option,
    options.sender_index_option,
    options.receiver_option,
    options.erc20_amount_option,
    options.erc20_token_option,
    options.ks_option,
    options.pw_without_ensure_option,
]
deploy_options = [
    options.rpc_option,
    options.private_key_option,
    options.erc20_name_option,
    options.erc20_symbol_option,
    options.sender_option,
    options.sender_index_option,
    options.ks_option,
    options.pw_without_ensure_option,
]
get_balance_options = [
    options.rpc_option,
    options.erc20_token_option,
    options.account_option,
]
total_supply_options = [
    options.rpc_option,
    options.erc20_token_option,
]


@click.group()
def erc20():
    """
    Interact with ethereum to send erc20 token, get balance and so on
    """
    pass


@click.command()
@options.add_options(transfer_options)
def transfer(rpc, priv, sender, index, to, amount, token, ks, pw):
    """
    Transfer erc20 token from sender to receiver
    """
    try:
        account = utils.get_account(ks, priv, sender, index, pw)
        TxManager(rpc).transfer_erc20_token(account, to, amount, token)
    except:
        print("Transfer failed")


@click.command()
@options.add_options(deploy_options)
def deploy(rpc, priv, name, symbol, sender, index, ks, pw):
    """
    Deploy a new erc20 token to the network
    """

    try:
        account = utils.get_account(ks, priv, sender, index, pw)
        TxManager(rpc).deploy_erc20_token(account, name, symbol)
    except:
        print("Deploy failed")


@click.command()
@options.add_options(get_balance_options)
def get_balance(rpc, token, account):
    """
    Get the balance of an account of erc20 token
    """

    balance, symbol = TxManager(rpc).get_erc20_token_balance(token, account)
    symbol = symbol.decode("utf-8")
    print("The balance of account {} of erc20 token {} is {} {}".format(account, token, balance, symbol))


@click.command()
@options.add_options(total_supply_options)
def total_supply(rpc, token):
    """
    Get the total supply of erc20 token
    """

    balance, symbol = TxManager(rpc).get_total_supply(token)
    symbol = symbol.decode("utf-8")
    print("The total supply of erc20 token {} is {} {}".format(token, balance, symbol))


erc20.add_command(transfer)
erc20.add_command(deploy)
erc20.add_command(total_supply)
erc20.add_command(get_balance)
