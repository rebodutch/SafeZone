#!/bin/bash
set -e

# Step 1: set variables
IMAGE_NAME="covid_data_simulator"
IMAGE_TAG="test"
CONTAINER_NAME="covid_data_simulator"
DOCKERFILE_PATH="./services/CovidDataSimulator"
TEST_PATH="./services/CovidDataSimulator/test"

# Step 2: compile
echo "No explicit compilation step required for Python..."

# Step 3: build docker image
echo "Building Docker image..."
docker build -t "$IMAGE_NAME:$IMAGE_TAG" -f "$DOCKERFILE_PATH/Dockerfile.test" "$DOCKERFILE_PATH"

# Step 4: stop the container if it is running from previous scripts
if [ "$(docker ps -aq -f name="$CONTAINER_NAME")" ]; then
    echo "Stopping existing container..."
    docker stop "$CONTAINER_NAME"

    echo "Removing existing container..."
    docker rm "$CONTAINER_NAME"
fi

# Step 5: run the tests in the container
# mkdir for test results
mkdir -p "$TEST_PATH/results"

# unit test
echo "Running unit tests..."
docker run --rm \
  -v "$(pwd)/services/CovidDataSimulator/data/test_data:/app/data" \
  -v "$(pwd)/$TEST_PATH/results:/test/results" \
  --name "$CONTAINER_NAME" "$IMAGE_NAME:$IMAGE_TAG" \
  sh -c "ls -R /app && ls -R /test && pytest test/unit_test --junitxml=/test/results/unit_test_results.xml"

# docker run --rm \
#   -v "$(pwd)/services/CovidDataSimulator/data/test_data:/app/data" \
#   -v "$(pwd)/$TEST_PATH/results:/test/results" \
#   --name "$CONTAINER_NAME" "$IMAGE_NAME:$IMAGE_TAG" \
#   pytest test/unit_test --junitxml=/test/results/unit_test_results.xml
# UNIT_TEST_EXIT_CODE=$?

if [ $UNIT_TEST_EXIT_CODE -ne 0 ]; then
    echo "Unit tests failed with exit code $UNIT_TEST_EXIT_CODE"
    exit $UNIT_TEST_EXIT_CODE
fi

# integration test
# echo "Running integration tests..."
# docker run --rm \
#   -v "$(pwd)/services/CovidDataSimulator/data/test_data:/app/data" \
#   -v "$(pwd)/$TEST_PATH/results:/test/results" \
#   --name "$CONTAINER_NAME" "$IMAGE_NAME:$IMAGE_TAG" \
#   pytest test/integration_test --junitxml=/test/results/integration_test_results.xml
# INTEGRATION_TEST_EXIT_CODE=$?

# if [ $INTEGRATION_TEST_EXIT_CODE -ne 0 ]; then
#     echo "Integration tests failed with exit code $INTEGRATION_TEST_EXIT_CODE"
#     exit $INTEGRATION_TEST_EXIT_CODE
# fi

echo "All tests passed successfully!"