#!/bin/bash

dockername=web-challenge

bash ./create-enc-zip.sh

echo "Removing old ${dockername} image..."
docker rmi ${dockername}

echo "Building using name: ${dockername}"
docker build . -t ${dockername}

echo "Running ${dockername}..."
docker run -it --rm ${dockername}
