#!/bin/bash

# Step 1: 設定變數
IMAGE_NAME="covid_data_simulator_image"
CONTAINER_NAME="covid_data_simulator_container"
DOCKERFILE_PATH="./services/CovidDataSimulator"
HOST_PORT=8000
CONTAINER_PORT=8000

# Step 2: 編譯（如果需要，這裡示範 Python 環境通常不需要編譯）
echo "No explicit compilation step required for Python..."

# Step 3: 建置 Docker 映像
echo "Building Docker image..."
docker build -t $IMAGE_NAME $DOCKERFILE_PATH

# Step 4: 停止並移除現有容器
if [ $(docker ps -aq -f name=$CONTAINER_NAME) ]; then
    echo "Stopping existing container..."
    docker stop $CONTAINER_NAME

    echo "Removing existing container..."
    docker rm $CONTAINER_NAME
fi

# Step 5: 運行 Docker 容器
# echo "Running Docker container..."
docker run $CONTAINER_NAME
# docker run -d --name $CONTAINER_NAME -p $HOST_PORT:$CONTAINER_PORT $IMAGE_NAME

# echo "Container $CONTAINER_NAME is running at port $HOST_PORT."