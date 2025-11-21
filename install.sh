#!/bin/bash
set -e

echo "Installing recorder system..."

# Install Python libraries
pip3 install RPi.GPIO evdev --break-system-packages

# Create directories
mkdir -p /home/pi/recorder
mkdir -p /home/pi/videos
mkdir -p /home/pi/logs

# Set permissions
chmod +x /home/pi/recorder/recorder.py

# Install systemd service
sudo cp recorder.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable recorder.service
sudo systemctl start recorder.service

echo "Installation complete!"
echo "Check status: sudo systemctl status recorder"
echo "View logs: journalctl -u recorder -f"