#!/usr/bin/env python
import argparse
import csv
import tempfile
import subprocess
from pathlib import Path

from tqdm import tqdm
from solana.transaction import Keypair


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
    for keypair_path in tqdm(keypairs_paths):
        try:
            output = subprocess.check_output(['ore', '--rpc', args.rpc, '--keypair', keypair_path, 'balance'])
            reward = output.split()[0].decode()
            if reward == 'Error':
                key = keypair_path_keypair[str(keypair_path)]
                keys.append(key)
                print(f'{key} id bad!')
        except Exception as e:
            print(f'IGNORED EXCEPTION: {e}')

    print('Writing accounts to csv.')
    with args.outfile.open('w') as f:
        writer = csv.writer(f)
        for key in tqdm(keys):
            writer.writerow([key])

    tmp_dir.cleanup()


if __name__ == '__main__':
    main()
