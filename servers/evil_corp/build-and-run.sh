#!/bin/bash

dockername=h4tt-evilcorp-challenge
zipname=TOP-SECRET.zip
password=$(cat ./zip-file/password.txt)

echo $(whoami)

if [ $(whoami) != "root" ]; then
    echo "Encrypting and creating zip file"
    zip -e -j --password "${password}" ./app/public/${zipname} ./zip-file/flag.txt ./zip-file/top-secret.md

    echo "Require root priviliges to run the docker commands"
    echo "In particular this will:"
    echo "1. Build a new docker image for this challenge called ${dockername}"
    echo "2. Remove all dangling images, so images named <none>:<none>"
    echo "3. Run the newly built docker image set up the internals and run it on the host network"
    exec sudo "$0"
fi

echo "Building using name: ${dockername}"
docker build -t ${dockername} .

echo "Removing old dangling images..."
dangling_images=$(docker images -f dangling=true -q)
if [ ! -z ${dangling_images} ]; then
    docker rmi ${dangling_images}
else
    echo "No images to remove."
fi

echo "Running ${dockername}..."
docker run --network=host -it --rm ${dockername}
