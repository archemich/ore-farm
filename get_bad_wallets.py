#!/usr/bin/env python

"""
How to use:
python3 get_bad_wallets.py --keys <csv> --rpc <url>
"""

import argparse
import csv
import tempfile
import subprocess
from pathlib import Path

from tqdm import tqdm
from solana.transaction import Keypair
from solana.rpc.types import RPCError


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keys', type=Path, help='csv with private keys as b58string', required=True)
    parser.add_argument('--rpc', required=True)
    parser.add_argument('--outfile', type=Path, default=(Path(__file__).parent / 'broken.csv'))
    return parser.parse_args()


def main():
    args = parse_args()
    keypairs_paths = []
    tmp_dir = tempfile.TemporaryDirectory()
    keypair_path_keypair= {}
    with args.keys.open() as f:
        reader = csv.reader(f)
        for b58str in reader:
            keypair = Keypair.from_base58_string(b58str[0]).to_json()
            keypair_path = Path(tmp_dir.name) / (str(b58str[0]) +'.tmp')
            keypair_path_keypair[str(keypair_path)] = b58str[0]
            with keypair_path.open('w') as tmp_f:
                tmp_f.write(str(keypair))
                keypairs_paths.append(keypair_path)

    keys = []
    print('Checking accounts.')

    def handle_error(keypair_path):
        key = keypair_path_keypair[str(keypair_path)]
        keys.append(key)
        print(f'{key} is bad!')

    for keypair_path in tqdm(keypairs_paths):
        try:
            output = subprocess.check_output(['ore', '--rpc', args.rpc, '--keypair', keypair_path, 'balance'])
            balance = output.split()[0].decode()
            if balance == 'Error':
                handle_error(keypair_path)
                continue

            output = subprocess.check_output(['ore', '--rpc', args.rpc, '--keypair', keypair_path, 'rewards'])
            reward = output.split()[0].decode()
        except Exception as e:
            handle_error(keypair_path)

    print('Writing accounts to csv.')
    with args.outfile.open('w') as f:
        writer = csv.writer(f)
        for key in tqdm(keys):
            writer.writerow([key])

    tmp_dir.cleanup()


if __name__ == '__main__':
    main()
