sudo apt update
sudo apt upgrade -y

curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/admin/.local/bin:$PATH" # assumed the username is admin

# Install the required packages
sudo apt install python3-rpi.gpio