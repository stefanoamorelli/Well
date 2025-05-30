#!/bin/bash

echo "🚀 Launching Receipt Gen AI API..."
echo

# Activate the virtual environment
source venv/bin/activate

# Add the src folder to PYTHONPATH
export PYTHONPATH="$(pwd)/src"

# Start the API with auto-reload
uvicorn core.api.app:app --reload
