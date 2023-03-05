#!/bin/sh

python=python
venv=.venv
activate=$venv/bin/activate
requirements=requirements.txt
main=src/main.py

# Check if Python is installed
if ! command -v $python >/dev/null 2>&1; then
    echo "Python is required to run this script"
    exit 1
fi

# Create virtual environment
if [ ! -d "$venv" ]; then
    $python -m venv $venv || {
        echo "Failed to create virtual environment"
        exit 1
    }
fi

# Activate virtual environment
if [ ! -f "$activate" ]; then
    echo "Virtual environment activation script not found"
    exit 1
fi

. $activate || {
    echo "Failed to activate virtual environment"
    exit 1
}

# Install requirements if not running main.py
if [ "$1" != "run" ]; then
    pip install -r $requirements || {
        echo "Failed to install requirements"
        exit 1
    }
fi

# Run main.py if requested
if [ "$1" = "run" ]; then
    $python $main || {
        echo "Failed to run main.py"
        exit 1
    }
fi

echo "Script executed successfully"
