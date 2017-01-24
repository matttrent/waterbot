#!/bin/bash

# only run the following script on mondays
if [ "$(date +%u)" = 1 ]; 
    then python scripts/state_plot.py; 
else
    echo "not monday"
fi
