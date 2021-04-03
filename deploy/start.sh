#!/bin/bash

# install requirements
cd /home/ubuntu/ftf-re-api
pip3 install -r requirements.txt

# setup and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# start apache
sudo service apache2 start