#!/bin/bash

# install requirements
cd /home/ubuntu/ftf-re-api

# setup and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# install any new requirements
pip3 install -r requirements.txt

# start apache
sudo service apache2 start