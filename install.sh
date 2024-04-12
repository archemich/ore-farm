mkdir ore
mv main.py ~/ore
mv mine_ore.sh ~/ore
mv claim_ore.sh ~/ore
mv check_balance.py ~/ore
mv get_bad_wallets.py ~/ore
mv requirements.txt ~/ore
mv install.sh ~/ore

mkdir ~/ore
sudo apt update && sudo apt install build-essential python3 python3-pip -y
pip install -r ~/ore/requirements.txt
curl https://sh.rustup.rs -sSf | sh
sh -c "$(curl -sSfL https://release.solana.com/v1.18.4/install)"
. "$HOME/.cargo/env"
cargo install ore-cli