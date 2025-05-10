sudo apt update
sudo apt upgrade -y

# Install uv as package control
sudo curl -LsSf https://astral.sh/uv/install.sh | sudo env UV_INSTALL_DIR="/bin" sh

# # Install the required packages
# sudo apt install python3-rpi.gpio