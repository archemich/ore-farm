LOGIN=$1
SERVER_IP=$2

scp main.py $LOGIN@$SERVER_IP:~/
scp mine_ore.sh $LOGIN@$SERVER_IP:~/
scp claim_ore.sh $LOGIN@$SERVER_IP:~/
scp check_balance.py $LOGIN@$SERVER_IP:~/
scp requirements.txt $LOGIN@$SERVER_IP:~/
scp install.sh $LOGIN@$SERVER_IP:~/