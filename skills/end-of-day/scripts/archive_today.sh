#!/bin/bash
# Archives ~/wiki/today/{journal.md,research/} into the dated journal/research
# paths for today. Run once per day, at day's end.
set -euo pipefail

# The work day is dated by when it started, not by whatever calendar day
# archiving happens to run on: a session starting in the evening that runs
# past midnight (e.g. 20:00-01:00) still belongs to the day it started.
# $1 overrides the journal path (for the self-test); default is the real one.
work_date() {
  local journal="${1:-$HOME/wiki/today/journal.md}"
  if [ -f "$journal" ]; then
    date -r "$(stat -f %B "$journal")" +%Y-%m-%d
  else
    date +%Y-%m-%d
  fi
}

archive() {
  local wiki="$1" today_date="$2"
  local year="${today_date%%-*}" month="${today_date:5:2}"
  local dest="$wiki/research/$year/$month/$today_date"

  if [ -f "$wiki/today/journal.md" ]; then
    mkdir -p "$wiki/journal/$year/$month"
    local jdest="$wiki/journal/$year/$month/$today_date.md"
    if [ -f "$jdest" ]; then
      cat "$wiki/today/journal.md" >> "$jdest"
    else
      mv "$wiki/today/journal.md" "$jdest"
    fi
  fi

  if [ -d "$wiki/today/research" ]; then
    mkdir -p "$dest"
    for d in "$wiki/today/research"/*/; do
      [ -d "$d" ] || continue
      mv "$d" "$dest/"
    done
  fi

  rm -rf "$wiki/today"
}

self_test() {
  local tmp

  tmp="$(mktemp -d)"
  touch "$tmp/journal.md"
  [ "$(work_date "$tmp/journal.md")" = "$(date +%Y-%m-%d)" ] || { echo "FAIL: work_date should use the journal's creation date"; exit 1; }
  [ "$(work_date "$tmp/missing.md")" = "$(date +%Y-%m-%d)" ] || { echo "FAIL: work_date should fall back to today when no journal exists"; exit 1; }
  rm -rf "$tmp"

  tmp="$(mktemp -d)"
  mkdir -p "$tmp/today/research/00-demo/explores"
  echo "- 09:00:00: did a thing" > "$tmp/today/journal.md"
  echo "notes" > "$tmp/today/research/00-demo/explores/01-x.md"

  archive "$tmp" "2026-01-15"

  [ -f "$tmp/journal/2026/01/2026-01-15.md" ] || { echo "FAIL: journal not archived"; exit 1; }
  [ -f "$tmp/research/2026/01/2026-01-15/00-demo/explores/01-x.md" ] || { echo "FAIL: research not archived"; exit 1; }
  [ ! -d "$tmp/today" ] || { echo "FAIL: today/ not removed"; exit 1; }

  rm -rf "$tmp"
  echo "self-test passed"
}

if [ "${1:-}" = "--test" ]; then
  self_test
  exit 0
fi

# d-handoff and advisor call this so their dated output files agree with
# the date this script will archive under, even if invoked standalone.
if [ "${1:-}" = "--date" ]; then
  work_date
  exit 0
fi

archive "$HOME/wiki" "$(work_date)"
echo "archived ~/wiki/today/ into ~/wiki/journal/ and ~/wiki/research/ for $(work_date)"
