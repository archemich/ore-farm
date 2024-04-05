import argparse
import csv
import sys
from pathlib import Path
from solana.rpc.api import Client
from solana.rpc.types import TokenAccountOpts, TxOpts
from solana.transaction import Keypair, Transaction, Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import transfer_checked, TransferCheckedParams

DRY_RUN = False
ORE_ADDRESS = 'oreoN2tQbHXVaZsr3pf66A48miqcBXCDJozganhEJgz'
SUPPORTED_TOKENS = ['ore', 'sol']


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('target_wallet')
    parser.add_argument('--rpc', required=True)
    parser.add_argument('--keys', type=Path, required=True, help='csv file with private keys.')
    parser.add_argument('--tokens', required=True, choices=SUPPORTED_TOKENS, nargs='+')
    parser.add_argument('--dry-run', action='store_true')
    return parser.parse_args()


def drain_ore(private_key:str, target_wallet: str, client: Client):
    mint = Pubkey.from_string(ORE_ADDRESS)
    keypair = Keypair.from_base58_string(private_key)
    source_wallet = keypair.pubkey()
    dest_wallet = Pubkey.from_string(target_wallet)

    token_opts = TokenAccountOpts(mint=mint)
    token_account_from = client.get_token_accounts_by_owner(owner=source_wallet, opts=token_opts).value[0].pubkey
    token_account_to = client.get_token_accounts_by_owner(owner=dest_wallet, opts=token_opts).value[0].pubkey
    balance = client.get_token_account_balance(pubkey=token_account_from)
    if balance.value.amount == '0':
        print(f'{source_wallet} has 0 ore.')
        return

    tx = Transaction().add(
        transfer_checked(TransferCheckedParams(
            TOKEN_PROGRAM_ID,
            token_account_from,
            mint,
            token_account_to,
            source_wallet,
            int(balance.value.amount),
            int(balance.value.decimals)
        ))
    )
    amount = balance.value.ui_amount_string
    if not DRY_RUN:
        resp = client.send_transaction(tx, keypair, opts=TxOpts(max_retries=10))
        print(f'Sent: {amount} Ore.')
        print(f'From: {source_wallet}.')
        print(f'To: {dest_wallet}.')
        print(f'Result: {resp}.')
        return resp.value
    else:
        print(f'Will be sent {amount} from {source_wallet} to {dest_wallet}.')


def main():
    """Drain all money from wallets in csv to primary wallet."""
    args = parse_args()
    global DRY_RUN
    if args.dry_run:
        DRY_RUN = True
    if args.rpc[-1] == '/':
        args.rpc = args.rpc[:-1]

    client = Client(args.rpc)
    if not client.is_connected():
        print('Can\'t connect to RPC.')
        sys.exit(1)

    callees = []
    for token in args.tokens:
        callees.append(globals()[f'drain_{token}'])
    with args.keys.open() as f:
        reader = csv.reader(f)
        for row in reader:
            for callee in callees:
                # Supposed to be drain ore be called first and sol last.
                callee(row[0], args.target_wallet, client)


if __name__ =='__main__':
    main()
