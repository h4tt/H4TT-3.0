#!/bin/bash

zipname=${1}
password=$(cat ./password.txt)

echo ${password}

echo "Rebuilding the encrypted zip file..."
zip -e -j --password "$(cat password.txt)" ${zipname} flag.txt top-secret.md
