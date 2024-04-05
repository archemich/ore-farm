#!/usr/bin/env python
import argparse
import csv
from base58 import b58encode
from pathlib import Path
from solana.transaction import Keypair


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('txt', type=Path)
    parser.add_argument('output', type=Path)

    return parser.parse_args()


def main():
    args = parse_args()
    keys = []
    with args.txt.open() as f:
        for row in f:
            keypair = Keypair().from_json(row)
            keys.append(b58encode(bytes(keypair)).decode().strip())

    with args.output.open('w', newline='\n') as f:
        writer = csv.writer(f)
        for key in keys:
            writer.writerow([key])




if __name__ == '__main__':
    main()
