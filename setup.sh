sudo apt update
sudo apt upgrade -y

# Install uv as package control
sudo curl -LsSf https://astral.sh/uv/install.sh | sudo env UV_INSTALL_DIR="/bin" sh

# Install the required packages
sudo apt install python3-rpi.gpio v4l-utils ffmpeg -y

# Install RTSP server
mkdir mediamtx
wget -P ./mediamtx https://github.com/bluenviron/mediamtx/releases/download/v1.12.2/mediamtx_v1.12.2_linux_arm64.tar.gz
cd mediamtx
tar -xzf mediamtx_v1.12.2_linux_arm64.tar.gz

# Copy the service file to make the service start on boot
sudo cp /home/admin/better-rvc/service/mediamtx.service /etc/systemd/system/
sudo cp /home/admin/better-rvc/service/stream.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable mediamtx
sudo systemctl start mediamtx
sudo systemctl enable stream
sudo systemctl start stream