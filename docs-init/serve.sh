#!/usr/bin/env bash
set -euo pipefail

mdbook serve -n 0.0.0.0 -p 4800 "$@"
