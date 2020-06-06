#!/bin/bash

sudo apt-get install git
sudo apt-get install python3-pip


cd /usr/bin
sudo git clone https://github.com/wabiloo/snatcha.git
cd snatcha/
pip3 install -r requirements.txt

sudo python3 webservice/app.py
