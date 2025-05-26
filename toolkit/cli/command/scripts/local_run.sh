#!/bin/bash
set -e

# --------- Customizable Section ---------
IMAGE_REPO="ghcr.io/safezone"
IMAGE_NAME="safezone_cli_command"
IMAGE_TAG="latest"
INSTANCE_NAME="safezone_cli_daemon"
AUTH_DIR="$(pwd)/secrets/google_oath"
# --------------------------------

# 1. Remove exited containers (to avoid zombie containers occupying the name)
if docker ps -a --filter "name=$INSTANCE_NAME" --filter "status=exited" | grep -q $INSTANCE_NAME; then
  echo "Found exited $INSTANCE_NAME, removing..."
  docker rm $INSTANCE_NAME
fi

# 2. Pull image if not found
if ! docker image inspect "$IMAGE_NAME:$IMAGE_TAG" > /dev/null 2>&1; then
  echo "Docker image $IMAGE_NAME:$IMAGE_TAG not found. Pulling..."
  docker pull "$IMAGE_REPO/$IMAGE_NAME:$IMAGE_TAG"
fi

# 3. Run daemon if not already running
if ! docker ps -q --filter "name=$INSTANCE_NAME" | grep -q .; then
  echo "Docker instance $INSTANCE_NAME not found. Running..."
  docker run --name=$INSTANCE_NAME -d \
    -v "$AUTH_DIR":/app/secrets \
    -u $(id -u):$(id -g) \
    "$IMAGE_NAME:$IMAGE_TAG" bash -c "tail -f /dev/null"
fi

# 4. Execute CLI command, aligning paths with local environment
docker exec -it \
  -u $(id -u):$(id -g) \
  $INSTANCE_NAME szcli "$@"

