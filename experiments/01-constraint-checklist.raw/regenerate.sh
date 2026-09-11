#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 analyze.py > output.json
printf '%s\n' "Wrote $(pwd)/output.json"
