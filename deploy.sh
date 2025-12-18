#!/bin/bash
set -e

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# DO NOT hardcode secrets
export LITELLM_API_KEY=${LITELLM_API_KEY:-""}

nohup uvicorn app.main:app --host 0.0.0.0 --port 8080 > server.log 2>&1 &

sleep 3
echo "Service started on port 8080"
