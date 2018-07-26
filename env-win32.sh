#!/bin/sh
# RUN ON WINDOWS ONLY FFS!
if [ ! -d "venv" ]; then
    # Create virtualenv
    python -m virtualenv venv
fi
source venv/scripts/activate
pip install -r requirements.txt
clear
echo Now running in virtual environment, run deactivate to exit