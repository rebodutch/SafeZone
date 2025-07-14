set -e

REMOTE="ghcr.io/rebodutch"
COMMAND_IMAGE_NAME="safezone-cli-command"
RELAY_IMAGE_NAME="safezone-cli-relay"

echo "Pushing CLI Command Image to $REMOTE/$COMMAND_IMAGE_NAME:$IMAGE_TAG..."
docker tag "$COMMAND_IMAGE_NAME:$IMAGE_TAG" "$REMOTE/$COMMAND_IMAGE_NAME:$IMAGE_TAG"
docker push "$REMOTE/$COMMAND_IMAGE_NAME:$IMAGE_TAG"

echo "Pushing CLI Relay Image to $REMOTE/$RELAY_IMAGE_NAME:$IMAGE_TAG..."
docker tag "$RELAY_IMAGE_NAME:$IMAGE_TAG" "$REMOTE/$RELAY_IMAGE_NAME:$IMAGE_TAG"
docker push "$REMOTE/$RELAY_IMAGE_NAME:$IMAGE_TAG"

echo "Docker Image pushed successfully to $REMOTE/$IMAGE_NAME:$IMAGE_TAG"

echo "Cleaning up local image..."
docker rmi "$COMMAND_IMAGE_NAME:$IMAGE_TAG"
docker rmi "$RELAY_IMAGE_NAME:$IMAGE_TAG" || true
docker rmi "$REMOTE/$COMMAND_IMAGE_NAME:$IMAGE_TAG"
docker rmi "$REMOTE/$RELAY_IMAGE_NAME:$IMAGE_TAG" || true