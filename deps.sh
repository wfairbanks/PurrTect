#!/bin/bash

# Update System
sudo apt-get update;
sudo apt-get install -y python3-venv;

# Create a virtual environment
python3 -m venv purrvenv;
source purrvenv/bin/activate;

# Upgrade pip for better performance and compatibility
pip install --upgrade pip; 
pip install --upgrade setuptools;
pip install --upgrade wheel;

# Install Python libraries using piwheels for faster installations
pip install RPi.GPIO;
pip install "opencv-python-headless<4.3";
pip install flask;
