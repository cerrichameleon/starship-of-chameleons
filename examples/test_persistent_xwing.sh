#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
rm -f var/uhura_state.json
PYTHONPATH=src python3 examples/xwing_demo.py open --provider mock
printf '\n--- state ---\n'
cat var/uhura_state.json
printf '\n--- captain ---\n'
PYTHONPATH=src python3 examples/xwing_demo.py captain --provider mock --prompt 'status report'
printf '\n--- diagnose ---\n'
PYTHONPATH=src python3 examples/xwing_demo.py diagnose --provider mock
printf '\n--- close ---\n'
PYTHONPATH=src python3 examples/xwing_demo.py close --provider mock
printf '\n--- final state ---\n'
cat var/uhura_state.json
