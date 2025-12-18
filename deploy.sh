#!/bin/bash
set -e

echo "🚀 Starting Spike AI BuildX service..."

# -----------------------------
# Python sanity check
# -----------------------------
if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ python3 not found"
  exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✅ Using Python $PYTHON_VERSION"

# -----------------------------
# Virtual environment
# -----------------------------
if [ ! -d ".venv" ]; then
  echo "🔧 Creating virtual environment"
  python3 -m venv .venv
fi

# Activate venv (guaranteed to exist now)
if [ ! -f ".venv/bin/activate" ]; then
  echo "❌ Virtual environment activation script not found"
  exit 1
fi

source .venv/bin/activate

# -----------------------------
# Dependencies
# -----------------------------
echo "📦 Installing dependencies"
pip install --upgrade pip
pip install -r requirements.txt

# -----------------------------
# Environment safety
# -----------------------------
# Prevent crash if LiteLLM key is not provided
export LITELLM_API_KEY=${LITELLM_API_KEY:-""}

# -----------------------------
# Start service
# -----------------------------
echo "🚀 Launching API server"
nohup uvicorn app.main:app --host 0.0.0.0 --port 8080 > server.log 2>&1 &

sleep 3

echo "✅ Service started on port 8080"
