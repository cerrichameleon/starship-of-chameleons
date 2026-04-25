#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
TARGET_LINK="/usr/local/bin/starship"

if [ ! -w /usr/local/bin ]; then
  echo "Need sudo to install alias into /usr/local/bin"
  sudo ln -sf "$PROJECT_ROOT/starship" "$TARGET_LINK"
else
  ln -sf "$PROJECT_ROOT/starship" "$TARGET_LINK"
fi

echo "Installed launcher alias: starship"
echo "You can now run: starship"
