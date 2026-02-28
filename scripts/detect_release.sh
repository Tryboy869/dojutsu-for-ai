#!/usr/bin/env bash
# detect_release.sh — Extrait la dernière version du CHANGELOG.md
# Exit 0 + prints version si nouvelle section détectée, exit 1 sinon
set -euo pipefail

CHANGELOG="CHANGELOG.md"
if [ ! -f "$CHANGELOG" ]; then
  echo "No CHANGELOG.md found" >&2
  exit 1
fi

# Extraire la première ligne ## [x.x.x]
LATEST=$(grep -m1 "^## \[" "$CHANGELOG" | sed "s/## \[//;s/\].*//" | tr -d "[:space:]")
if [ -z "$LATEST" ]; then
  echo "No version found in CHANGELOG" >&2
  exit 1
fi

TAG="v${LATEST}"

# Vérifier si le tag existe déjà
if git tag --list | grep -q "^${TAG}$"; then
  echo "Tag ${TAG} already exists — no new release" >&2
  exit 1
fi

echo "${TAG}"
