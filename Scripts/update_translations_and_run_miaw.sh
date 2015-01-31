#!/bin/bash

echo "Enter CrowdIn API key:"

read -s API_KEY

./update_translations.py -p $API_KEY
cd ..
Scripts/./miaw -v -g -w --no-date -d -o BeMyEyes/Source/