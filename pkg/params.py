from pathlib import Path
import os

# home dir of user
home_dir = str(Path.home())
ks = ".eth_wallet_cli"
default_ks = os.path.join(home_dir, ks)
localURL = "http://localhost:8545"
mnemonic_len = 12
