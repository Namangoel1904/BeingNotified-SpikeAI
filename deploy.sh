#!/bin/bash
set -e

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

nohup uvicorn app.main:app --host 0.0.0.0 --port 8080 &
