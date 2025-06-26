#!/bin/bash
set -e

# Step 1: set variables
IMAGE_NAME="safezone_analytics_api"
DOCKERFILE_PATH="./services/SafeZoneAnalyticsAPI"

# Step 2: compile
echo "No explicit compilation step required for Python..."

# Step 3: build docker image
echo "Building Docker image..."
docker buildx build -t "$IMAGE_NAME" -f "$DOCKERFILE_PATH/Dockerfile" .