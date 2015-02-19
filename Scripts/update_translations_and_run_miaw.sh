#!/bin/bash

echo "Enter CrowdIn API key:"

read -s API_KEY

echo "Building on Crowd In"
./export_translations.py $API_KEY
echo "Downloading and updating"
./update_translations.py -p $API_KEY
echo "Running MiawKit"
cd ..
Scripts/./miaw -v -g -w --no-date -d -o BeMyEyes/Source/
echo "Done"