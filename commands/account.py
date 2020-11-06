import click
import commands.options as options
from pkg.keystore import KeyStore

new_options = [
    options.pw_option,
    options.ks_option,
]
show_options = [
    options.ks_option,
]
load_options = [
    options.ks_option,
    options.private_key_option,
    options.pw_option,
]
recover_options = [
    options.mnemonic_option,
    options.ks_option,
    options.pw_option,
]


@click.group()
def account():
    """
    Manage accounts in keystore
    """
    pass


@click.command()
@options.add_options(new_options)
def new(pw, ks):
    """Create a new ethereum account encrypted by password"""

    KeyStore(ks).generate_account(pw)


@click.command()
@options.add_options(show_options)
def show(ks):
    """Show the list of current stored accounts in keystore"""

    accounts = KeyStore(ks).get_accounts()
    print("Total accounts: {}".format(len(accounts)))
    for i, addr in enumerate(accounts):
        print("Account index:{}, address: {}".format(i, addr))


@click.command()
@options.add_options(load_options)
def load(ks, priv, pw):
    """Import a account into keystore using private key"""

    KeyStore(ks).import_from_key(priv, pw)


@click.command()
@options.add_options(recover_options)
def recover(mnemonic, ks, pw):
    """Try to recover user account by mnemonic"""

    KeyStore(ks).import_from_mnemo(mnemonic, pw)


account.add_command(new)
account.add_command(show)
account.add_command(load)
account.add_command(recover)
