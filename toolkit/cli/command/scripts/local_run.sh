#!/bin/bash
set -e

IMAGE_NAME="safezone-cli:latest"
IMAGE_TAG="latest"
INSTANCE_NAME="safezone-cli"
AUTH_DIR="secrets"

# if the image is not found, pull it
if ! docker image inspect $IMAGE_NAME > /dev/null 2>&1; then
  echo "Docker image $IMAGE_NAME not found. Pulling..."
  docker pull ghcr.io/safezone/$IMAGE_NAME:$IMAGE_TAG
fi

# if auth dir is not found, create it
if [ ! -d "$AUTH_DIR" ]; then
  echo "[INFO] Creating $AUTH_DIR for secrets mount..."
  mkdir -p "$AUTH_DIR"
fi

# if the running daemon is not found, run it
if ! docker ps -q --filter "name=$INSTANCE_NAME" | grep -q .; then
  echo "Docker instance $INSTANCE_NAME not found. Running..."
  docker run --name=$INSTANCE_NAME -d -v $AUTH_DIR:/app/secrets $IMAGE_NAME
fi

# execute the command
docker exec -it $INSTANCE_NAME szcli "$@"
