#!/bin/bash

# Function to check if brew is installed
function check_brew {
    if ! command -v brew &> /dev/null
    then
        echo "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "Homebrew is already installed."
    fi
}

# Function to check if displayplacer is installed
function check_displayplacer {
    if ! command -v displayplacer &> /dev/null
    then
        echo "displayplacer not found. Installing displayplacer..."
        brew install displayplacer
    else
        echo "displayplacer is already installed."
    fi
}

# Check and install brew if not present
check_brew

# Check and install displayplacer if not present
check_displayplacer

# Run the Python script
echo "Running DarwinCustomRes.py..."
python3 "$(dirname "$0")/DarwinCustomRes.py"
