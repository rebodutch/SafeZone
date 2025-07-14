set -e

REMOTE="ghcr.io/rebodutch"

echo "Pushing Docker Image to $REMOTE..."

docker tag  "$IMAGE_NAME":"$IMAGE_TAG"  "$REMOTE"/"$IMAGE_NAME":"$IMAGE_TAG"
docker push "$REMOTE"/"$IMAGE_NAME":"$IMAGE_TAG"

echo "Docker Image pushed successfully to $REMOTE/$IMAGE_NAME:$IMAGE_TAG"

echo "Cleaning up local image..."
docker rmi "$IMAGE_NAME":"$IMAGE_TAG"
docker rmi "$REMOTE"/"$IMAGE_NAME":"$IMAGE_TAG" || true