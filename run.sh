#!/bin/bash

# Step 1: Install the requirements
echo "Installing requirements from requirements.txt..."
pip install -r requirements.txt

# Step 2: Define default flags for find_links.py
FLAG=""
API_FLAG=""
NO_FLAG=""

# Step 3: Process command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        (-f|--flag) FLAG="-f";;           # Example: -f option
        (-nf|--no-flag) NO_FLAG="-nf";;   # Example: -nf option
        *) echo "Unknown parameter: $1"; exit 1;;
    esac
    shift
done

# Step 4: Run find_links.py with the provided flags
echo "Running find_links.py with options..."
python3 ./find_links.py $FLAG $NO_FLAG $API_FLAG

# Step 5: Run broken-link-check.py (no flags provided)
echo "Running broken-link-check.py..."
python3 ./broken-link-check.py
