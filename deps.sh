#!/bin/bash

# Update System
sudo apt-get update;
sudo apt-get install -y python3-venv;

# Create a virtual environment
python3 -m venv purrvenv;
source purrvenv/bin/activate;

# Upgrade pip for better performance and compatibility
pip install --upgrade pip setuptools wheel;

# Add piwheels for faster pip installations on Raspberry Pi
echo "deb http://www.piwheels.org/simple bullseye main" | sudo tee /etc/apt/sources.list.d/piwheels.list;
sudo apt update;

# Install OpenCV system dependencies
sudo apt-get install -y libopencv-dev;

# Install Python libraries using piwheels for faster installations
pip install opencv-python opencv-python-headless RPi.GPIO flask;
