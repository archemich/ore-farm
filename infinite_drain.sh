while true
do
  echo "Launch command."
  python ./drain_wallets.py $1  --rpc https://serene-convincing-county.solana-mainnet.quiknode.pro/4d151bbf7cacc083bdd9cffe910456b419323591 --keys $2 --tokens ore
  echo 'Stop.\n'
  sleep 5s
done