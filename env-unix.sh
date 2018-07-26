#!/bin/sh
# RUN ON UNIX/LINUX ONLY FFS!
if [ ! -d "venv" ]; then
    # Create virtualenv
    virtualenv venv
fi
source venv/bin/activate
pip install -r requirements.txt
clear
echo Now running in virtual environment, run deactivate to exit