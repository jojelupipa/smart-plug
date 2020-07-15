#! /bin/bash
# PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
# NAME="Raspbian GNU/Linux"

# Download mosquitto
curl https://mosquitto.org/files/source/mosquitto-1.6.8.tar.gz -o mosquitto-1.6.8.tar.gz
# Unzip mosquitto
tar -xzvf mosquitto-1.6.8.tar.gz

# Build and install mosquitto
cd mosquitto-1.6.8/
make
sudo apt-get update
sudo apt-get install mosquitto

# Add mosquitto user
sudo addusr mosquitto

# Installing python and pip
sudo apt-get install python3 python3-pip
