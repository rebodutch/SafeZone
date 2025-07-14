#!/bin/bash
set -e

CONTAINER_NAME=test-${IMAGE_NAME}-${IMAGE_TAG}

# echo envs for debugging
echo "IMAGE_NAME: $IMAGE_NAME"
echo "IMAGE_TAG: $IMAGE_TAG"
echo "BUILD_PATH: $BUILD_PATH"
echo "CONTAINER_NAME: $CONTAINER_NAME"

# Step 1: build testing image
echo "Building Docker image..."
docker buildx build -t "$IMAGE_NAME:$IMAGE_TAG" -f "$BUILD_PATH/Dockerfile.test" .

# Step 2: run the tests in the testing container
# integration test
echo "Running integration tests..."
docker run --rm \
  --name "$CONTAINER_NAME" "$IMAGE_NAME:$IMAGE_TAG" \
  pytest --cov=/app --cov-report=term-missing /test

echo "All tests passed successfully!"

# Step 3: clean up
echo "Cleaning up..."
docker rmi "$IMAGE_NAME":"$IMAGE_TAG"|| true