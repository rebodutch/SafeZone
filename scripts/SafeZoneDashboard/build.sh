#!/bin/bash
set -e

# Step 1: set variables
IMAGE_NAME="safezone_dashboard"
DOCKERFILE_PATH="./services/SafeZoneDashboard/environments/dev"

# Step 2: compile
echo "No explicit compilation step required for Python..."

# Step 3: build docker image
echo "Building Docker image..."
docker build -t "$IMAGE_NAME" -f "$DOCKERFILE_PATH/Dockerfile.dev" .