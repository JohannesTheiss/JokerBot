#!/bin/bash

CONTAINER_NAME="joker_bot"

# Remove one or more containers
# --force       : Force the removal of a running container (uses SIGKILL)
docker rm --force "${CONTAINER_NAME}"

# Build an image from a Dockerfile
# --tag list    : Name and optionally a tag in the 'name:tag' format
docker build --tag="${CONTAINER_NAME}" .

# Run a command in a new container
# --name string : Assign a name to the container
# --rm          : Automatically remove the container when it exits
# --detach      : Run container in background and print container ID
# -v            : Bind mount a volume
docker run -v $PWD/logs:/app/logs -v $PWD/json:/app/json --detach --rm -name="${CONTAINER_NAME}" "${CONTAINER_NAME}"

# Attach local standard input, output, and error streams to a running container
# --sig-proxy   : Proxy all received signals to the process (default true)
docker attach --sig-proxy=false "${CONTAINER_NAME}"