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

2. install the dependencies using Poetry:

    ```BASH
    cd better-rvc
    poetry install
    ```

## Project Structure

``` plaintext
.
├── LoRa
│   ├── esp32_s3_lora_recevier
│   │   └── esp32_s3_lora_recevier.ino
│   └── esp32_s3_lora_sender
│       └── esp32_s3_lora_sender.ino
├── poetry.lock
├── pyproject.toml
├── README.md
└── servo
    ├── README.md
    └── servo.py
```
