#!/bin/bash

# Define the name of the virtual environment directory
ENV_DIR="virtual_env"

# Check if the virtual environment directory exists
if [ -d "$ENV_DIR" ]; then
    echo "Virtual environment '$ENV_DIR' already exists."
else
    # Create a virtual environment
    python -m venv $ENV_DIR
    echo "Virtual environment '$ENV_DIR' created."
fi

python main.py

# Activate the virtual environment
if [ -f "$ENV_DIR/Scripts/activate" ]; then
    # Windows
    source $ENV_DIR/Scripts/activate
else
    # macOS/Linux
    source $ENV_DIR/bin/activate
fi

# Install the requirements from requirements.txt
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Requirements installed successfully."
else
    echo "requirements.txt not found."
fi

# Deactivate the virtual environment
deactivate

echo "Setup complete."