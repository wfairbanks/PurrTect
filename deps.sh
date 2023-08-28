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
echo "deb http://www.piwheels.org/simple stretch main" | sudo tee -a /etc/apt/sources.list.d/piwheels.list;
sudo apt update;
pip install opencv-python, opencv-python-headless RPi.GPIO flask;
