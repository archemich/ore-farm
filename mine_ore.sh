while true
do
  echo "Running"
  ore \
    --rpc $1 \
    --keypair $2 \
    --priority-fee $3 \
  mine \
    --threads 2
  echo "Exited"
done
