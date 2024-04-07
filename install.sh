mkdir ore
cp ~/* ~/ore

mkdir ~/ore
sudo apt update && sudo apt install build-essential python3 python3-pip -y
curl https://sh.rustup.rs -sSf | sh
sh -c "$(curl -sSfL https://release.solana.com/v1.18.4/install)"
source ~/.profile
cargo install ore-cli