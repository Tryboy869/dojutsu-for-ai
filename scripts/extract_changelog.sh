#!/usr/bin/env bash
# extract_changelog.sh — Extrait le contenu de la dernière section du CHANGELOG
set -euo pipefail
CHANGELOG="CHANGELOG.md"
# Tout entre le premier ## [...] et le second
awk "/^## \[/{count++; if(count==2) exit} count==1{print}" "$CHANGELOG"
