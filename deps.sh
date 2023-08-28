#/bin/bash

# Update System
sudo apt-get update;
sudo apt-get install -y libopencv-dev python3-venv;

# Clone GitHub Repo
git clone https://github.com/wfairbanks/purrtect.git;

# CD to repo
cd purrtect;

# Create project directory and setup virtual env
python3 -m venv purrvenv;
source purrvenv/bin/activate;

# Install OpenCV and other Python libraries
pip3 install opencv-python opencv-python-headless RPi.GPIO flask;

# Activate Venv
source purrvenv/bin/activate;

#Launch App
cd myapp;
python3 app.py
