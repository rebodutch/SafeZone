set -e

# Promote a preview-validated dev image to a release tag by digest-preserving
# registry copy (ADR-2: build once, promote everywhere — no rebuild).
# crane copy is a registry-native blob copy: the target digest is byte-identical
# to the source (unlike `buildx imagetools create`, which re-wraps a single-arch
# source in a new OCI index → a different top-level digest).
# Env: IMAGE_NAME, SOURCE_VERSION (0.X.Y-<sha>), TARGET_VERSION (0.X.Y or
# 0.X.Y-dryrun). crane authenticates via the docker config written by the
# workflow's docker/login-action step.

REMOTE="ghcr.io/rebodutch"

SRC="$REMOTE/$IMAGE_NAME:$SOURCE_VERSION"
DST="$REMOTE/$IMAGE_NAME:$TARGET_VERSION"

echo "Promoting $SRC -> $DST (crane copy, digest-preserving)..."
crane copy "$SRC" "$DST"

SRC_DIGEST=$(crane digest "$SRC")
DST_DIGEST=$(crane digest "$DST")

if [ "$SRC_DIGEST" != "$DST_DIGEST" ]; then
    echo "ERROR: digest mismatch after copy of $IMAGE_NAME:"
    echo "  $SRC -> $SRC_DIGEST"
    echo "  $DST -> $DST_DIGEST"
    exit 1
fi

echo "Promoted $IMAGE_NAME: $DST_DIGEST"
