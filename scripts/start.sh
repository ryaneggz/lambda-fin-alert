#!/bin/bash

echo "Connect to prod? (yes/no)"
read answer
if [ "$answer" == "yes" ]; then
    echo "Start Prod Env locally"
    echo ""
    echo ""
    ENV_FILE=.env.production
elif [ "$answer" == "no" ]; then
    ENV_FILE=.env.local
    echo "Running script locally..."
else
    echo "Invalid input. Please enter 'yes' or 'no'."
fi

### Set Environment Variables
set -a # automatically export all variables
source $ENV_FILE
set +a

python main.py