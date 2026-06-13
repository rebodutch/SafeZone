set -e

# Promote the three CLI images (sibling of cli/push-image.sh; promotion has no
# per-image variance, so each delegates to the generic promote-image.sh).
# Env: SOURCE_VERSION, RELEASE_VERSION.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

for IMAGE_NAME in safezone-cli-command safezone-cli-relay safezone-cli-ops; do
    IMAGE_NAME="$IMAGE_NAME" bash "$SCRIPT_DIR/../promote-image.sh"
done
