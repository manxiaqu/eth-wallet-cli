import click
import pkg.params as params


# simple method to add options
def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


pw_option = click.option('--pw', prompt='Please enter password to encrypt private key', help='Your password used to '
                                                                                             'encrypt key')
pw_without_ensure_option = click.option('--pw', help='Your password used to encrypt key')
ks_option = click.option('--ks', default=params.default_ks, help='Path of keystore to store key file')
private_key_option = click.option('--priv', help='Private key of account you want to import')
mnemonic_option = click.option('--mnemonic', help='Your mnemonic to recover private key')
rpc_option = click.option('--rpc', default=params.localURL, help='Rpc url of ethereum node')
sender_option = click.option('--sender', help='Sender account address you want to use')
account_option = click.option('--account', help='Account address you want to query balance of')
sender_index_option = click.option('--index', help='Index of sender account in keystore you want to use')
gas_option = click.option('--gas', help='Gas limit you want pay for this transaction')
gas_price_option = click.option('--gas_price', help='Gas price per gas you want to pay for this transaction')
data_option = click.option('--data', help='Data of transaction you want to send')
receiver_option = click.option('--to', help='Receiver account address')
ether_amount_option = click.option('--amount', help='Amount of ether you want to send')
tx_hash_option = click.option('--tx', help='Transaction hash you want to query')
# erc20 token options
erc20_amount_option = click.option('--amount', help='Amount of erc20 token you want to send')
erc20_token_option = click.option('--token', help='ERC20 token address you want to use')
erc20_name_option = click.option('--name', help='Name of erc20 token you want to deploy')
erc20_symbol_option = click.option('--symbol', help='Symbol of erc20 token you want to deploy')

