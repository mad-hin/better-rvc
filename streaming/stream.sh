#!/bin/bash
# Stream from webcam to local RTSP server (video only)

CAMERA="/dev/video10"
RTSP_URL="rtsp://localhost:8554/better-rvc" #rtsp://192.168.31.125:8554/mystream

# ffmpeg -f v4l2 -i "$CAMERA" \
# -c:v libx264 -preset veryfast -tune zerolatency -f rtsp "$RTSP_URL"

ffmpeg -f v4l2 -i /dev/video0 \
-c:v rawvideo -f v4l2 /dev/video99 \
-c:v libx264 -preset veryfast -tune zerolatency -f rtsp "$RTSP_URL"