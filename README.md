## How to launch bot

Connect to server using Yandex LoginOS via ssh.

Install requirements:

``` bash
mkdir ~/ore
sudo apt update && sudo apt install build-essential -y
sudo apt install python3 -y
sudo apt install python3-pip -y
curl https://sh.rustup.rs -sSf | sh
sh -c "$(curl -sSfL https://release.solana.com/v1.18.4/install)"
source ~/.profile
cargo install ore-cli
```

Go to your host pc, open POWERSHELL (it's convenient for Windows) and copy to the server scripts.

```bash
set LOGIN_NAME <YOUR_LOGIN>
set SERVER_IP <SERVER_IP>
set KEYS <YOUR_CSVFILE>
```
```bash
scp main.py ${LOGIN_NAME}@${SERVER_IP}:~/ore/
scp launch_ore.sh ${LOGIN_NAME}@${SERVER_IP}:~/ore/
scp requirements.txt ${LOGIN_NAME}@${SERVER_IP}:~/ore/
scp ${KEYS} ${LOGIN_NAME}@${SERVER_IP}:~/ore/
```

Go back to the server and launch script
```bash
export RPC_URL=<YOUR_RPC>
export KEYS=<YOUR_CSVFILE>
tmux
cd ~/ore
pip install -r requirements.txt
python3 main.py --rpc $RPC_URL --keys $KEYS &
```
Deatch session so script not stopped when leave server with `Ctrl-B D` in tmux.
The script supposed to be launch in tmux so it works even when you logout the server.