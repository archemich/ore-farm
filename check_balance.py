#!/usr/bin/env python
import argparse
import csv
import subprocess
import tempfile
from pathlib import Path
from uuid import uuid4

from solana.transaction import Keypair
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keys', type=Path, help='csv with private keys as b58string', required=True)
    parser.add_argument('--rpc', required=True)
    parser.add_argument('--type', choices=['balance', 'rewards'], required=True)
    parser.add_argument('--threshold', type=float, default=0.001)
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
            keypair_path = Path(tmp_dir.name) / (str(uuid4()) +'.txt')
            keypair_path_keypair[str(keypair_path)] = b58str
            with keypair_path.open('w') as tmp_f:
                tmp_f.write(str(keypair))
                keypairs_paths.append(keypair_path)

    reward_sum = 0
    keys = []
    print('Checking accounts.')
    for keypair_path in tqdm(keypairs_paths):
        try:
            output = subprocess.check_output(['ore', '--rpc', args.rpc, '--keypair', keypair_path, args.type])
            reward = output.split()[0]
            if float(reward) > args.threshold:
                keys.append(keypair_path_keypair[str(keypair_path)])
            reward_sum += float(reward)
            print(f'{args.type}: {reward}')
        except Exception as e:
            print(f'IGNORED EXCEPTION: {e}')

    print(f'Total {args.type} sum: {reward_sum}')
    print('Writing to accounts to csv.')
    new_keys_csv=Path(__file__).parent / (args.type + '.csv')
    with new_keys_csv.open('w') as f:
        writer = csv.writer(f)
        for key in tqdm(keys):
            writer.writerow(key)

    tmp_dir.cleanup()


if __name__ == '__main__':
    main()
