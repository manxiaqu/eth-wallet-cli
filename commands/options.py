import click
import pkg.params as params
from web3 import Web3


# simple method to add options
def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


def validate_mnemonic(ctx, param, value):
    """
    Check mnemonic is valid or not
    """
    if value is None or len(value.split()) != params.mnemonic_len:
        raise click.UsageError("Invalid mnemonic: {}, length isn't {}".format(value, params.mnemonic_len))

    return value


def validate_rpc(ctx, param, value):
    """
    Check rpc url is connectable
    """
    if value is None:
        raise click.UsageError("None rpc url set!")
    w3 = Web3(Web3.HTTPProvider(value))
    if not w3.isConnected():
        raise click.UsageError("Can't connect to rpc: {}".format(value))

    return value


def validate_address(ctx, param, value):
    """
    Check the address is valid or not
    """
    if value is None:
        raise click.UsageError("None address set!")
    if value.startswith("0x") or value.startswith("0X"):
        to_check = value[2:]
    else:
        to_check = value
    if len(bytes.fromhex(to_check)) != 20:
        raise click.UsageError("Invalid address: {}".format(value))

    return value


def validate_hash(ctx, param, value):
    """
    Check the hash is valid or not
    """
    if value is None:
        raise click.UsageError("None tx hash set!")
    if value.startswith("0x") or value.startswith("0X"):
        to_check = value[2:]
    else:
        to_check = value
    try:
        value_bytes = bytes.fromhex(to_check)
    except ValueError:
        raise click.UsageError("Invalid tx hash: {}".format(value))
    if len(value_bytes) != 32:
        raise click.UsageError("Invalid tx hash: {}, bytes length not 32".format(value))

    return value


def validate_priv(ctx, param, value):
    """
    Check the input is hex string or not
    """
    if value is None:
        raise click.UsageError("None hex data set!")
    if value.startswith("0x") or value.startswith("0X"):
        value = value[2:]
    try:
        value_bytes = bytes.fromhex(value)
    except ValueError:
        raise click.UsageError("Invalid hex format data: {}".format(value))

    if len(value_bytes) > 32:
        raise click.UsageError("Private key bytes len should <= 32, but actual: {}".format(value))

    return value


def validate_int(ctx, param, value):
    """
    Check the input is int or not
    """
    if value is None:
        value = 0
    try:
        value = int(value)
    except ValueError:
        raise click.UsageError("Invalid value: {}, it should be a int number!".format(value))

    return value


pw_option = click.option('--pw', prompt='Please enter password to encrypt private key', help='Your password used to '
                                                                                             'encrypt key')
pw_without_ensure_option = click.option('--pw', help='Your password used to encrypt key')
ks_option = click.option('--ks', default=params.default_ks, help='Path of keystore to store key file')
private_key_option = click.option('--priv', help='Private key of account you want to import')
mnemonic_option = click.option('--mnemonic', callback=validate_mnemonic, help='Your mnemonic to recover private key')
rpc_option = click.option('--rpc', default=params.localURL, callback=validate_rpc, help='Rpc url of ethereum node')
sender_option = click.option('--sender', help='Sender account address you want to use')
account_option = click.option('--account', help='Account address you want to query balance of')
sender_index_option = click.option('--index', help='Index of sender account in keystore you want to use')
gas_option = click.option('--gas', default=21000, callback=validate_int, help='Gas limit you want pay for this '
                                                                              'transaction')
gas_price_option = click.option('--gas_price', default=20000000000, callback=validate_int, help='Gas price per gas '
                                                                                                'you want to pay for '
                                                                                                'this transaction')
data_option = click.option('--data', help='Data of transaction you want to send')
receiver_option = click.option('--to', callback=validate_address, help='Receiver account address')
ether_amount_option = click.option('--amount', default=0, callback=validate_int, help='Amount of ether you want to send')
tx_hash_option = click.option('--tx', callback=validate_hash, help='Transaction hash you want to query')
# erc20 token options
erc20_amount_option = click.option('--amount', default=0, callback=validate_int, help='Amount of erc20 token you want '
                                                                                      'to send')
erc20_token_option = click.option('--token', callback=validate_address, help='ERC20 token address you want to use')
erc20_name_option = click.option('--name', default="", help='Name of erc20 token you want to deploy')
erc20_symbol_option = click.option('--symbol', default="", help='Symbol of erc20 token you want to deploy')
