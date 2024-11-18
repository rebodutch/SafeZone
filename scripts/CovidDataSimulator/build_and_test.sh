#!/bin/bash
# Step 1: 設定變數
IMAGE_NAME="covid_data_simulator"
CONTAINER_NAME="covid_data_simulator"
DOCKERFILE_PATH="./services/CovidDataSimulator"

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

# Step 5: 運行 Docker 容器做測試
# 運行單元測試
echo "Running unit tests..."
docker run --rm --name $CONTAINER_NAME $IMAGE_NAME pytest services/test/

# Step 5: 運行 Docker 容器（使其在後台運行，提供測試所需的服務）
echo "Starting Docker container..."
docker run -d --name $CONTAINER_NAME -p $HOST_PORT:$CONTAINER_PORT $IMAGE_NAME

# 等待幾秒讓服務啟動
echo "Waiting for the service to start..."
sleep 5

# 運行集成測試
echo "Running integration tests..."
docker run --rm --name $CONTAINER_NAME $IMAGE_NAME pytest test/test_main.py