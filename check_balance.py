#!/usr/bin/env python
import argparse
import csv
import tempfile
import logging
import subprocess
import threading
import signal
import sys
from uuid import uuid4
from typing import List
from pathlib import Path

from solana.transaction import Keypair


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keys', type=Path, help='csv with private keys as b58string', required=True)
    parser.add_argument('--rpc', required=True)
    parser.add_argument('--type', choices=['balance', 'rewards'], required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    keypairs_paths = []
    tmp_dir = tempfile.TemporaryDirectory()

    with args.keys.open() as f:
        reader = csv.reader(f)
        for b58str in reader:
            keypair = Keypair.from_base58_string(b58str[0]).to_json()
            keypair_path = Path(tmp_dir.name) / (str(uuid4()) +'.txt')
            with keypair_path.open('w') as tmp_f:
                tmp_f.write(str(keypair))
                keypairs_paths.append(keypair_path)

    reward_sum = 0
    for keypair_path in keypairs_paths:
        try:
            output = subprocess.check_output(['ore', '--rpc', args.rpc, '--keypair', keypair_path, args.type])
            reward = output.split()[0]
            reward_sum += float(reward)
            print(f'reward: {reward}')
        except Exception as e:
            print(f'IGNORED EXCEPTION: {e}')

    print(f'Total reward sum: {reward_sum}')
    tmp_dir.cleanup()


if __name__ == '__main__':
    main()
