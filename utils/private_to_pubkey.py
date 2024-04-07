import argparse
from pathlib import Path
from solana.transaction import Keypair

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=Path, required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    rows = args.file.open('r').readlines()
    rows = [r.rstrip() for r in rows]
    print(rows[0])
    outpath = Path(args.file).parent / (args.file.stem + '.pub' + args.file.suffix)
    pubkeys = [str(Keypair.from_base58_string(key).pubkey()) for key in rows]
    with outpath.open('w') as f:
        pubkeys =[p+'\n' for p in pubkeys]
        f.writelines(pubkeys)




if __name__ == '__main__':
    main()