#!/bin/bash

# Define the name of the virtual environment directory
ENV_DIR="myenv"

# Activate the virtual environment
if [ -f "$ENV_DIR/Scripts/activate" ]; then
    # Windows
    source $ENV_DIR/Scripts/activate
else
    # macOS/Linux
    source $ENV_DIR/bin/activate
fi

# Run the Python script
python main.py

# Deactivate the virtual environment
deactivate
