import argparse
import sys

from solana.rpc.api import Client
from spl.token.client import Token
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts,TokenAccountOpts
from spl.token.instructions import transfer_checked, TransferCheckedParams, create_associated_token_account
from base58 import b58encode
from solana.transaction import Keypair, Transaction, Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rpc', required=True)
    return parser.parse_args()



def main():
    args = parse_args()

    program_id = TOKEN_PROGRAM_ID

    mint = Pubkey.from_string(TOKEN_ADDRESS)
    owner = Pubkey.from_string(SOURCE_PUB)
    dest = Pubkey.from_string(DEST_PUB)
    client = Client(args.rpc, commitment=Confirmed)
    if not client.is_connected():
        print('Can\'t connect to RPC.')
        sys.exit(1)
    token_opts = TokenAccountOpts(mint=mint)
    token_account_from = client.get_token_accounts_by_owner(owner=owner, opts=token_opts)
    token_account_to = client.get_token_accounts_by_owner(owner=dest, opts=token_opts, commitment=Confirmed)

    keypair = Keypair.from_base58_string(SOURCE_PRIVATE)

    tx = (Transaction()
    .add(
        transfer_checked(TransferCheckedParams(
            TOKEN_PROGRAM_ID,
            token_account_from.value[0].pubkey,
            mint,
            token_account_to.value[0].pubkey,
            owner,
            int(1e4),
            9
        ))
    ))
    resp = client.send_transaction(tx, keypair)

if __name__ =='__main__':
    main()