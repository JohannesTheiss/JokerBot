#!/bin/bash

CONTAINER_NAME="joker_bot"

# Remove containers, -f remove running container
docker rm -f "${CONTAINER_NAME}"

# Build an image from the Dockerfile, tag = joker_bot
docker build --tag="${CONTAINER_NAME}" .

# Run a command in a new container
# --name string : Assign a name to the container
# --rm          : Automatically remove the container when it exits
# --detach      : Run container in background and print container ID
docker run --detach --rm --name="${CONTAINER_NAME}" "${CONTAINER_NAME}"