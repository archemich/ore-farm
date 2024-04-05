while true
do
  echo "Running"
  ore \
    --rpc $1 \
    --keypair $2 \
    --priority-fee 1000000 \
  mine \
    --threads 2
  echo "Exited"
done
