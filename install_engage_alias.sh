#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
TARGET_LINK="/usr/local/bin/engage"
TARGET_SOURCE="$PROJECT_ROOT/starship"

if [ ! -e "$TARGET_SOURCE" ]; then
  echo "Expected launcher not found: $TARGET_SOURCE" >&2
  exit 1
fi

if [ ! -w /usr/local/bin ]; then
  echo "Need sudo to install engage into /usr/local/bin"
  sudo ln -sf "$TARGET_SOURCE" "$TARGET_LINK"
else
  ln -sf "$TARGET_SOURCE" "$TARGET_LINK"
fi

echo "Installed launcher alias: engage -> $TARGET_SOURCE"
echo "engage now opens the Starship onboarding flow first."
