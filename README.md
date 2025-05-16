# better-rvc

## Overview

This project is an IoT project that improves the Remote Video Capture (RVC) system by auto moving the camera to the best position for capturing the video.

## Hardware List

- Raspberry Pi 4
- MG90S Servo
- ESP32 WROOM module
- SX1278 LoRa module
- 0.96 inch OLED Display
- A usb webcam (e.g. Logitech C270)
- A light sensor

## Pre-requisites

- Python 3.12 or higher
- Linux OS (e.g. Raspberry Pi OS)

## Installation

1. Clone the repository:

    ```BASH
    git clone https://github.com/mad-hin/better-rvc.git
    ```

    or if you have GitHub CLI installed:

    ```BASH
    gh repo clone mad-hin/better-rvc
    ```

2. install the dependencies:

    ```BASH
    cd better-rvc
    bash setup.sh
    ```

## Usage

1. **Run the main program**:

    ```BASH
    uv run main.py
    ```

2. **View the streaming service**:

    ```BASH
    ffplay rtsp://<your-raspberry-pi-ip>:8554/better-rvc
    ```

    or if you have `vlc` installed:

    open `vlc` and go to `Media -> Open Network Stream` and enter the URL `rtsp://<your-raspberry-pi-ip>:8554/better-rvc`.

## Troubleshooting

If you encounter any issues related to the streaming service/cv, you may try the following:

1. Re-create the virtual device `sudo modprobe v4l2loopback devices=1 video_nr=99 card_label="VirtualCam"`
2. Restart the streaming service `sudo systemctl restart stream.service`

If you have issue in running with `uv`, you may try the following:

- (Re)install `uv` using `sudo curl -LsSf https://astral.sh/uv/install.sh | sudo env UV_INSTALL_DIR="/bin" sh`

## Project Structure

``` plaintext
.
├── cv_recognition
│   ├── camera.py
│   ├── filter_data.py
│   ├── inference_all.py
│   ├── picamera_fps_demo.py
│   ├── README.markdown
│   ├── rvc_get_data.py
│   └── test.py
├── LoRa
│   ├── esp32_s3_lora_ble_controller
│   │   └── esp32_s3_lora_ble_controller.ino
│   ├── esp32_s3_lora_recevier
│   │   └── esp32_s3_lora_recevier.ino
│   ├── esp32_s3_lora_sender
│   │   └── esp32_s3_lora_sender.ino
│   ├── image
│   │   └── LoRa_explain.jpg
│   ├── modified ble keyboard library
│   │   └── ESP32-BLE-Keyboard.zip
│   ├── README.md
│   └── uart_test.py
├── main.py
├── PCB
│   ├── esp32_lora_v1-2025-04-27_152140.zip
│   └── ibom.html
├── pyproject.toml
├── README.md
├── service
│   ├── mediamtx.service
│   ├── stream.service
│   └── virtual_cam.service
├── servo
│   ├── README.md
│   ├── servo.py
│   ├── test_servo_180.py
│   └── test_servo.py
├── setup.sh
├── streaming
│   └── stream.sh
└── uv.lock
```
