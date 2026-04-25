#!/usr/bin/env bash
set -euo pipefail

repo="/home/node/.openclaw/workspace/git/repositories/starship"
cd "$repo"

# exact onboarding/runtime-manifest cluster only
git add -- \
  README.md \
  RUN_STARSHIP.md \
  PROVIDER_HELP.md \
  run_starship.py \
  install_starship_alias.sh \
  install_engage_alias.sh \
  src/starship_protocol/brain_selection.py \
  src/starship_protocol/engineering.py \
  src/starship_protocol/onboarding_ui.py \
  src/starship_protocol/runtime.py \
  src/starship_protocol/runtime_manifest.py \
  src/starship_protocol/web_ui.py \
  docs/onboarding_milestone_summary_2026-04-24.md

printf '\nStaged onboarding cluster:\n\n'
git diff --cached --stat -- \
  README.md \
  RUN_STARSHIP.md \
  PROVIDER_HELP.md \
  run_starship.py \
  install_starship_alias.sh \
  install_engage_alias.sh \
  src/starship_protocol/brain_selection.py \
  src/starship_protocol/engineering.py \
  src/starship_protocol/onboarding_ui.py \
  src/starship_protocol/runtime.py \
  src/starship_protocol/runtime_manifest.py \
  src/starship_protocol/web_ui.py \
  docs/onboarding_milestone_summary_2026-04-24.md

printf '\nReview staged patch with:\n'
printf 'git diff --cached -- README.md RUN_STARSHIP.md PROVIDER_HELP.md run_starship.py install_starship_alias.sh install_engage_alias.sh src/starship_protocol/brain_selection.py src/starship_protocol/engineering.py src/starship_protocol/onboarding_ui.py src/starship_protocol/runtime.py src/starship_protocol/runtime_manifest.py src/starship_protocol/web_ui.py docs/onboarding_milestone_summary_2026-04-24.md\n'

printf '\nIf the staged diff looks right, commit with something like:\n'
printf "git commit -m 'Make Starship onboarding-first with real provider readiness'\n"

printf '\nTip: README.md is intentionally included, because its status and launcher notes now match the onboarding-first flow and canonical launcher installer paths.\n'
