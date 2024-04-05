#!/usr/bin/env python
import argparse
import csv
import logging
import subprocess
import threading
import signal
import sys
from typing import List
from pathlib import Path

from solana.transaction import Keypair

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keys', type=Path, help='csv with private keys as b58string', required=True)
    parser.add_argument('--rpc', required=True)

    parser.add_argument('--task', choices=['claim', 'mine'], required=True)
    return parser.parse_args()

def mine_ore(rpc, keypair_path, log_path):
        with log_path.open('w') as f:
            f.write('')
            logging.debug(f'Launch mining for {keypair_path}. LogPath: {log_path}')
            subprocess.call(['sh', './mine_ore.sh', rpc, keypair_path], stdout=f)

def claim_ore(rpc, keypair_path, log_path):
        with log_path.open('w') as f:
            f.write('')
            logging.debug(f'Launch claiming for {keypair_path}. LogPath: {log_path}')
            subprocess.call(['sh', './claim_ore.sh', rpc, keypair_path], stdout=f)

def main():
    args = parse_args()

    keypairs_paths : List[Path]= []
    current_path = Path(__file__).parent
    keypairs_base_path = Path(__file__).parent / 'keypairs'
    keypairs_base_path.mkdir(parents=True, exist_ok=True)
    log_base_path = current_path / 'logs'
    log_base_path.mkdir(parents=True, exist_ok=True)

    with args.keys.open() as f:
        reader = csv.reader(f)
        for b58str in reader:
            keypair = Keypair.from_base58_string(b58str[0]).to_json()
            keypair_path = keypairs_base_path / f'id_{b58str[0]}.json'
            with keypair_path.open('w') as kpf:
                kpf.write(str(keypair))
                keypairs_paths.append(keypair_path)
    
    threads : List[threading.Thread]= []
    target = None
    if args.task == 'mine':
        target = mine_ore
    elif args.task == 'claim':
        target = claim_ore
    for keypair_path in keypairs_paths:
        log_path = log_base_path / (keypair_path.name + '.log')
        t = threading.Thread(target=target, args=[args.rpc, keypair_path, log_path])
        t.start()
        threads.append(t)
    
    def signal_handler(sig, frame):
        for t in threads:
            t.join(1)
            sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        pass
    

if __name__ == '__main__':
    main()
