#!/bin/bash

# Define the name of the virtual environment directory
ENV_DIR="virtual_env"

# Function to run the Python script in the virtual environment
run_in_virtualenv() {
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
}

# Run the function in a sub-shell
(
    run_in_virtualenv
)