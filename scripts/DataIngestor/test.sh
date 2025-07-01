#!/bin/bash
set -e

# Step 1: set variables
IMAGE_NAME="data_ingestor"
IMAGE_TAG="test"
CONTAINER_NAME="data_ingestor_test_container"
DOCKERFILE_PATH="./services/DataIngestor"

# Step 2: compile
echo "No explicit compilation step required for Python..."

# Step 3: build docker image
echo "Building Docker image..."
docker buildx build -t "$IMAGE_NAME:$IMAGE_TAG" -f "$DOCKERFILE_PATH/Dockerfile.test" .

# Step 4: stop the container if it is running from previous scripts
if [ "$(docker ps -aq -f name="$CONTAINER_NAME")" ]; then
    echo "Stopping existing container..."
    docker stop "$CONTAINER_NAME"

    echo "Removing existing container..."
    docker rm "$CONTAINER_NAME"
fi

# Step 5: run the tests in the container
# integration test
echo "Running integration tests..."
docker run --rm \
  --name "$CONTAINER_NAME" "$IMAGE_NAME:$IMAGE_TAG" \
  pytest --cov=/app --cov-report=term-missing /test

echo "All tests passed successfully!"