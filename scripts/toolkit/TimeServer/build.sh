#!/bin/bash
set -e

# Step 1: set variables
IMAGE_NAME="safezone_time_server"
IMAGE_TAG="latest" 
DOCKERFILE_PATH="./toolkit/time-server"

# Step 2: compile
echo "No explicit compilation step required for Python..."

# Step 3: build docker image
echo "Building Docker image..."
docker buildx build -t "$IMAGE_NAME:$IMAGE_TAG" -f "$DOCKERFILE_PATH/Dockerfile" .