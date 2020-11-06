import click
from commands import ether, account, erc20, tx


@click.group()
def entry_point():
    pass


entry_point.add_command(account.account)
entry_point.add_command(ether.ether)
entry_point.add_command(erc20.erc20)
entry_point.add_command(tx.tx)


if __name__ == '__main__':
    entry_point()