import argparse
import csv
import sys
from pathlib import Path

from base58 import b58encode
from solana.transaction import Keypair

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-csv', type=Path, required=True)
    parser.add_argument('count', type=int, help='number of keys to generate')
    parser.add_argument('--force', action='store_true')
    return parser.parse_args()

def main():
    args = parse_args()
    if args.output_csv.exists() and not args.force:
        print('Add --force flag to overwrite csv file!')
        sys.exit(1)

    with args.output_csv.open('w', newline='\n') as f:
        writer = csv.writer(f)
        for i in range(args.count):
            keypair = Keypair()
            private_key = b58encode(bytes(keypair)).decode().strip()
            writer.writerow([private_key])
    

if __name__ =='__main__':
    main()