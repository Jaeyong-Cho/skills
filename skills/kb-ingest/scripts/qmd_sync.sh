#!/bin/bash
# ---
# type: Shell Script
# title: qmd sync
# description: Refresh qmd's lexical index and vector embeddings for every collection — update discovers file changes (no -c filter exists, it's always all collections), embed only computes vectors for what update queues as pending. Neither alone is enough.
# tags: [wiki, qmd]
# timestamp: 2026-08-20T00:00:00+09:00
# ---

set -uo pipefail

if ! command -v qmd &>/dev/null; then
  echo "qmd not installed, skipping sync" >&2
  exit 0
fi

qmd update &>/dev/null || echo "qmd update failed" >&2
qmd embed &>/dev/null || echo "qmd embed failed" >&2
exit 0
