#!/usr/bin/env python
import argparse
from solana.transaction import Keypair

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('privatekeyb58')
    return parser.parse_args()

def main():
    args = parse_args()
    b58str = args.privatekeyb58
    kp = Keypair.from_base58_string(b58str)
    print(kp.to_json())

if __name__ == '__main__':
    main()
    