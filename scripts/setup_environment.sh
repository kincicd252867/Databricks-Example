#!/bin/bash
# Setup Python environment for the project

PYTHON_VERSION=$1
VENV_DIR=$2

echo "Setting up Python $PYTHON_VERSION environment in $VENV_DIR"

# Install required Python version
sudo apt-get update
sudo apt-get install -y python$PYTHON_VERSION python$PYTHON_VERSION-venv python$PYTHON_VERSION-dev

# Create virtual environment
python$PYTHON_VERSION -m venv $VENV_DIR

# Activate virtual environment and install base requirements
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Environment setup complete"
