#!/bin/bash

trap "kill 0" EXIT
echo "Starting Application..."

# --- Backend Setup ---
cd back

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    if command -v python &> /dev/null; then
        python -m venv .venv
    else
        python3 -m venv .venv
    fi
fi

if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

echo "Installing dependencies..."
python -m pip install python-dotenv
python -m pip install -r requirements.txt

# --- Start Backend Servers ---

echo "Starting Master Server..."
sh ./scripts/linux/run_master.sh & 

echo "Starting Replica Server..."
sh ./scripts/linux/run_replica.sh &

# --- Init Data ---
echo "Waiting 5 seconds..."
sleep 5

echo "Initializing test data..."
python init_test_data.py &

# --- Frontend Setup ---
cd ..
cd front-app

echo "Starting Frontend..."
npm install
npm start &

# --- Keep Alive ---
wait