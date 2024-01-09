#!/bin/bash

if [ ! -d "results" ]; then
    # Create the "result" folder if not found
    mkdir results &
    echo "Created 'results' folder."
fi

# Get all offers from all scripts
python3 Hemkop.py results &
python3 ICA.py results &
python3 Williys.py results &
