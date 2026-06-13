set -e

# Promote a preview-validated dev image to its official release tag by
# server-side retag (ADR-2: build once, promote everywhere — no rebuild).
# Env: IMAGE_NAME, SOURCE_VERSION (0.X.Y-<sha>), RELEASE_VERSION (0.X.Y).

REMOTE="ghcr.io/rebodutch"

SOURCE_REF="$REMOTE/$IMAGE_NAME:$SOURCE_VERSION"
RELEASE_REF="$REMOTE/$IMAGE_NAME:$RELEASE_VERSION"

echo "Promoting $SOURCE_REF -> $RELEASE_REF (server-side retag)..."
docker buildx imagetools create -t "$RELEASE_REF" "$SOURCE_REF"

SOURCE_DIGEST=$(docker buildx imagetools inspect "$SOURCE_REF" | awk '/^Digest:/{print $2}')
RELEASE_DIGEST=$(docker buildx imagetools inspect "$RELEASE_REF" | awk '/^Digest:/{print $2}')

if [ "$SOURCE_DIGEST" != "$RELEASE_DIGEST" ]; then
    echo "ERROR: digest mismatch after retag of $IMAGE_NAME:"
    echo "  $SOURCE_REF -> $SOURCE_DIGEST"
    echo "  $RELEASE_REF -> $RELEASE_DIGEST"
    exit 1
fi

echo "Promoted $IMAGE_NAME: $RELEASE_DIGEST"
