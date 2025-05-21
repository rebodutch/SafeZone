#!/bin/bash
set -e

repo="ghcr.io/safezone-io/safezone-cli"

docker buildx build \
    -t $repo/safezone-cli:latest \
    --push .