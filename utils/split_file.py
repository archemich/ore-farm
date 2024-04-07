import argparse
import math
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=Path, required=True)
    parser.add_argument('split_on', type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    rows = args.file.open('r').readlines()
    split_by = math.ceil(len(rows) / args.split_on)
    print(split_by)
    for i in range(args.split_on):
        outpath = Path(args.file).parent / (args.file.stem + str(i+1) + args.file.suffix)

        with outpath.open('w') as f:
            f.writelines(rows[split_by * i: split_by * i + split_by])


if __name__ == '__main__':
    main()