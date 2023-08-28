#/bin/bash

# Update System
sudo apt-get update;
sudo apt-get install -y libopencv-dev python3-venv;

# Create project directory and setup virtual env
python3 -m venv purrvenv;
source purrvenv/bin/activate;

# Install OpenCV and other Python libraries
pip install --upgrade pip;
pip install --upgrade pip setuptools wheel;
pip3 install opencv-python opencv-python-headless RPi.GPIO flask;
