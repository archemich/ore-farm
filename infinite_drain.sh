while true
do
  echo "Launch command."
  python ./drain_wallets.py $1  --rpc https://cosmological-fluent-breeze.solana-mainnet.quiknode.pro/da33bbd33484e23e34e4dcf9ff040642b5c3ea1f/ --keys $2 --tokens ore sol
  echo 'Stop.\n'
done
