#!/bin/bash
export DOCKER_HOST=tcp://docker:2376
export DOCKER_TLS_VERIFY=1
export DOCKER_CERT_PATH=/certs/client
export DOCKER_TLS_CERTDIR=/certs
docker run -it --rm --user eviluser talk-to-me-challenge
