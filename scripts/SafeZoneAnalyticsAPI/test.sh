#!/bin/bash
set -e

# Step 1: set variables
IMAGE_NAME="safezone_analytics_api"
IMAGE_TAG="test"
CONTAINER_NAME="safezone_analytics_api"
DOCKERFILE_PATH="./services/SafeZoneAnalyticsAPI/environments/test"
TEST_PATH="./services/SafeZoneAnalyticsAPI/environments/test/tests"

# Step 2: compile
echo "No explicit compilation step required for Python..."

# Step 3: build docker image
echo "Building Docker image..."
docker build -t "$IMAGE_NAME:$IMAGE_TAG" -f "$DOCKERFILE_PATH/Dockerfile.test" .

# Step 4: stop the container if it is running from previous scripts
if [ "$(docker ps -aq -f name="$CONTAINER_NAME")" ]; then
    echo "Stopping existing container..."
    docker stop "$CONTAINER_NAME"

    echo "Removing existing container..."
    docker rm "$CONTAINER_NAME"
fi

# Step 5: run the tests in the container
# unit test
echo "Running unit tests..."
docker run --rm \
  -v "$(pwd)/services/SafeZoneAnalyticsAPI/environments/test/data:/data" \
  -v "$(pwd)/utils:/app/utils" \
  --name "$CONTAINER_NAME" "$IMAGE_NAME:$IMAGE_TAG" \
  pytest test/unit_test

# # integration test
echo "Running integration tests..."
docker run --rm \
  -v "$(pwd)/services/SafeZoneAnalyticsAPI/environments/test/data:/data" \
  -v "$(pwd)/utils:/app/utils" \
  --name "$CONTAINER_NAME" "$IMAGE_NAME:$IMAGE_TAG" \
  pytest test/integration_test

echo "All tests passed successfully!"