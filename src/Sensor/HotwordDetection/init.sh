#!/bin/sh

sudo apt-get install python-pyaudio python3-pyaudio sox libatlas-base-dev swig
pip install pyaudio

sudo rm -rf ./snowboy
git clone https://github.com/Kitt-AI/snowboy.git ./snowboy
cd ./snowboy/swig/Python3
sudo make

cp _snowboydetect.so ../../../res/
cp snowboydetect.py ../../../res/
cd ../../..
sudo rm -rf ./snowboy







