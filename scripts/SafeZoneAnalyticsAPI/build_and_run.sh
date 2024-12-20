#!/bin/bash
set -e

# Step 1: set variables
IMAGE_NAME="safezone_analytics_api"
IMAGE_TAG="test"
CONTAINER_NAME="safezone_analytics_api"
DOCKERFILE_PATH="./services/SafeZoneAnalyticsAPI/environments/dev"

# the variables "maybe" is setted by outer procedure.
# Set default value for environment variable
if [ -z "${SERVICE_PORT}" ]; then
  export SERVICE_PORT=8020
fi

# Step 2: compile
echo "No explicit compilation step required for Python..."

# Step 3: build docker image
echo "Building Docker image..."
docker build -t "$IMAGE_NAME:$IMAGE_TAG" -f "$DOCKERFILE_PATH/Dockerfile.dev" .

# Step 4: stop the container if it is running from previous scripts
if [ "$(docker ps -aq -f name="$CONTAINER_NAME")" ]; then
    echo "Stopping existing container..."
    docker stop "$CONTAINER_NAME"

    echo "Removing existing container..."
    docker rm "$CONTAINER_NAME"
fi

# Step 5: run the tests in the container
# unit test
echo "Container is Running..."
docker run -it \
  -v "$(pwd)/utils:/app/utils" \
  -p $SERVICE_PORT:$SERVICE_PORT \
  --name "$CONTAINER_NAME" "$IMAGE_NAME:$IMAGE_TAG" \
  python /app/main.py