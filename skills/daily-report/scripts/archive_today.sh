#!/bin/bash
# Archives ~/wiki/today/{journal.md,research/} into the dated journal/research
# paths for today, then removes ~/wiki/today/. Run once per day, at day's end.
set -euo pipefail

archive() {
  local wiki="$1" today_date="$2"
  local year="${today_date%%-*}" month="${today_date:5:2}"

  if [ -f "$wiki/today/journal.md" ]; then
    mkdir -p "$wiki/journal/$year/$month"
    local dest="$wiki/journal/$year/$month/$today_date.md"
    if [ -f "$dest" ]; then
      cat "$wiki/today/journal.md" >> "$dest"
    else
      mv "$wiki/today/journal.md" "$dest"
    fi
  fi

  if [ -d "$wiki/today/research" ]; then
    mkdir -p "$wiki/research/$year/$month/$today_date"
    for d in "$wiki/today/research"/*/; do
      [ -d "$d" ] || continue
      mv "$d" "$wiki/research/$year/$month/$today_date/"
    done
  fi

  rm -rf "$wiki/today"
}

self_test() {
  local tmp
  tmp="$(mktemp -d)"
  mkdir -p "$tmp/today/research/00-demo/explores"
  echo "- 09:00:00: did a thing" > "$tmp/today/journal.md"
  echo "notes" > "$tmp/today/research/00-demo/explores/01-x.md"

  archive "$tmp" "2026-01-15"

  [ -f "$tmp/journal/2026/01/2026-01-15.md" ] || { echo "FAIL: journal not archived"; exit 1; }
  [ -f "$tmp/research/2026/01/2026-01-15/00-demo/explores/01-x.md" ] || { echo "FAIL: research not archived"; exit 1; }
  [ ! -d "$tmp/today" ] || { echo "FAIL: today/ not cleared"; exit 1; }

  rm -rf "$tmp"
  echo "self-test passed"
}

if [ "${1:-}" = "--test" ]; then
  self_test
  exit 0
fi

archive "$HOME/wiki" "$(date +%Y-%m-%d)"
echo "archived ~/wiki/today/ into ~/wiki/journal/ and ~/wiki/research/ for $(date +%Y-%m-%d)"
