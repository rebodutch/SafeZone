#!/bin/bash
set -e

# Step 1: set variables
IMAGE_NAME="safezone_dashboard"
IMAGE_TAG="test"
CONTAINER_NAME="safezone_dashboard"
DOCKERFILE_PATH="./services/SafeZoneDashboard/environments/test"
TEST_PATH="./services/SafeZoneDashboard/environments/test/tests"

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
# manual test: integration test
echo "Running the manual test..."
docker run -it \
  -p 8080:8080 \
  -v "$(pwd)/utils:/app/utils" \
  --name "$CONTAINER_NAME" "$IMAGE_NAME:$IMAGE_TAG" \
  python3 /test/manual_test/integration_test/test.py