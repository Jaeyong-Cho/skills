#!/bin/bash
# Archives ~/wiki/today/{journal.md,research/} into the dated journal nested
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

is_kept() {
  # $1: research dir basename (e.g. "00-demo"), $2: comma-separated keep list
  local base="$1" keep="$2" item
  IFS=',' read -ra parts <<< "$keep"
  for item in "${parts[@]}"; do
    [ "$item" = "$base" ] && return 0
  done
  return 1
}

archive() {
  local wiki="$1" today_date="$2" keep="${3:-}"
  local year="${today_date%%-*}" month="${today_date:5:2}"
  local dest="$wiki/journal/$year/$month/$today_date"

  # Assertion: destination must never equal the working directory
  [ "$dest" != "$wiki/today" ] || { echo "ERROR: date parsing bug would archive into $wiki/today"; exit 1; }

  if [ -f "$wiki/today/journal.md" ]; then
    mkdir -p "$dest"
    local jdest="$dest/journal.md"
    if [ -f "$jdest" ]; then
      cat "$wiki/today/journal.md" >> "$jdest"
    else
      mv "$wiki/today/journal.md" "$jdest"
    fi
    rm -f "$wiki/today/journal.md"
  fi

  if [ -d "$wiki/today/research" ]; then
    mkdir -p "$dest/research"
    for d in "$wiki/today/research"/*/; do
      [ -d "$d" ] || continue
      # research dirs named in $keep stay under today/research/ (still in progress)
      is_kept "$(basename "$d")" "$keep" && continue
      mv "$d" "$dest/research/"
    done
    rmdir "$dest/research" 2>/dev/null || true
  fi

  # Only remove today/ if nothing was kept behind; a kept research dir means
  # today/ (and today/research/) must survive for tomorrow's session.
  rmdir "$wiki/today/research" 2>/dev/null || true
  rmdir "$wiki/today" 2>/dev/null || true
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

  [ -f "$tmp/journal/2026/01/2026-01-15/journal.md" ] || { echo "FAIL: journal not archived to nested dir"; exit 1; }
  [ -f "$tmp/journal/2026/01/2026-01-15/research/00-demo/explores/01-x.md" ] || { echo "FAIL: research not archived to nested dir"; exit 1; }
  [ ! -d "$tmp/today" ] || { echo "FAIL: today/ not removed"; exit 1; }

  rm -rf "$tmp"

  tmp="$(mktemp -d)"
  mkdir -p "$tmp/today/research/00-keep-me/explores" "$tmp/today/research/01-archive-me"
  echo "- 09:00:00: did a thing" > "$tmp/today/journal.md"
  echo "notes" > "$tmp/today/research/00-keep-me/explores/01-x.md"
  echo "notes" > "$tmp/today/research/01-archive-me/notes.md"

  archive "$tmp" "2026-01-15" "00-keep-me"

  [ -f "$tmp/journal/2026/01/2026-01-15/research/01-archive-me/notes.md" ] || { echo "FAIL: unlisted topic not archived"; exit 1; }
  [ ! -e "$tmp/journal/2026/01/2026-01-15/research/00-keep-me" ] || { echo "FAIL: kept topic should not be archived"; exit 1; }
  [ -f "$tmp/today/research/00-keep-me/explores/01-x.md" ] || { echo "FAIL: kept topic should remain under today/research/"; exit 1; }
  [ ! -f "$tmp/today/journal.md" ] || { echo "FAIL: today/journal.md should be cleared once archived"; exit 1; }

  rm -rf "$tmp"
  echo "self-test passed"
}

if [ "${1:-}" = "--test" ]; then
  self_test
  exit 0
fi

# d-handoff calls this so its dated output file agrees with the date this
# script will archive under, even if invoked standalone.
if [ "${1:-}" = "--date" ]; then
  work_date
  exit 0
fi

# --keep "01-foo,02-bar": research topics to leave under today/research/
# instead of archiving (still in progress, carried to tomorrow as-is).
keep_arg=""
if [ "${1:-}" = "--keep" ]; then
  keep_arg="${2:-}"
fi

archive "$HOME/wiki" "$(work_date)" "$keep_arg"
echo "archived ~/wiki/today/ into ~/wiki/journal/YYYY/MM/YYYY-MM-DD/ for $(work_date)"
[ -n "$keep_arg" ] && echo "kept in progress under ~/wiki/today/research/: $keep_arg"
exit 0
