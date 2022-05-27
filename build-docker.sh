#!/bin/bash

CONTAINER_NAME="joker_bot"

# Remove containers, -f remove running container
docker rm -f "${CONTAINER_NAME}"

# Build an image from the Dockerfile, tag = joker_bot
docker build --tag="${CONTAINER_NAME}" .

# Run a command in a new container
# --name string : Assign a name to the container
# --rm          : Automatically remove the container when it exits
docker run --rm --name="${CONTAINER_NAME}" "${CONTAINER_NAME}"