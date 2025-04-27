# better-rvc

## Overview

This project is an IoT project that improves the Remote Video Capture (RVC) system by auto moving the camera to the best position for capturing the video.

## Hardware List

- Raspberry Pi 3B+
- MG90S Servo

## Pre-requisites

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/docs/#installation)

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

## Project Structure

``` plaintext
.
├── LoRa
│   ├── esp32_s3_lora_recevier
│   │   └── esp32_s3_lora_recevier.ino
│   ├── esp32_s3_lora_sender
│   │   └── esp32_s3_lora_sender.ino
│   └── modified ble keyboard library
│       └── ESP32-BLE-Keyboard.zip
├── PCB
│   ├── esp32_lora_v1-2025-04-27_152140.zip
│   └── ibom.html
├── README.md
├── poetry.lock
├── pyproject.toml
├── servo
│   ├── README.md
│   ├── __pycache__
│   │   └── servo.cpython-312.pyc
│   ├── servo.py
│   └── test_servo.py
└── setup.sh
```
