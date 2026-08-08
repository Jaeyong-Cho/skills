#!/bin/bash
# Archives ~/wiki/today/{journal.md,research/} into the dated journal/research
# paths for today, archives any goal moved to "## Done" in ~/wiki/goals.md
# into that same dated research folder, then relinks remaining "## Active"
# goals into a fresh ~/wiki/today/research/. Run once per day, at day's end.
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

# Next zero-padded NN- sequence number unused among NN-* dirs in $1.
next_seq() {
  local dir="$1" max=-1 n d
  for d in "$dir"/[0-9][0-9]-*/; do
    [ -e "$d" ] || continue
    d="${d%/}"
    n="${d##*/}"; n="${n%%-*}"
    n=$((10#$n))
    (( n > max )) && max=$n
  done
  printf '%02d' $((max + 1))
}

# Moves every goal listed under "## Done" in goals.md into $dest/NN-<slug>/
# and drops it from goals.md (it's now archived history, same as a one-off
# research job).
archive_done_goals() {
  local wiki="$1" dest="$2"
  local goals_md="$wiki/goals.md"
  [ -f "$goals_md" ] || return 0

  local in_done=0 out="" slug
  while IFS= read -r line; do
    case "$line" in
      "## Done") in_done=1; out+="$line"$'\n'; continue ;;
      "## "*) in_done=0; out+="$line"$'\n'; continue ;;
    esac
    if [ "$in_done" -eq 1 ] && [[ "$line" == "- "*": "* ]]; then
      slug="${line#- }"; slug="${slug%%:*}"
      if [ -d "$wiki/goals/$slug" ]; then
        mkdir -p "$dest"
        mv "$wiki/goals/$slug" "$dest/$(next_seq "$dest")-$slug"
        continue
      fi
    fi
    out+="$line"$'\n'
  done < "$goals_md"
  printf '%s' "$out" > "$goals_md"
}

# Symlinks every goal listed under "## Active" in goals.md into
# $wiki/today/research/NN-<slug>, so it shows up in today's work area.
relink_active_goals() {
  local wiki="$1"
  local goals_md="$wiki/goals.md"
  [ -f "$goals_md" ] || return 0

  local in_active=0 slug
  while IFS= read -r line; do
    case "$line" in
      "## Active") in_active=1; continue ;;
      "## "*) in_active=0; continue ;;
    esac
    if [ "$in_active" -eq 1 ] && [[ "$line" == "- "*": "* ]]; then
      slug="${line#- }"; slug="${slug%%:*}"
      if [ -d "$wiki/goals/$slug" ]; then
        mkdir -p "$wiki/today/research"
        ln -s "$wiki/goals/$slug" "$wiki/today/research/$(next_seq "$wiki/today/research")-$slug"
      fi
    fi
  done < "$goals_md"
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

  archive_done_goals "$wiki" "$dest"

  rm -rf "$wiki/today"

  relink_active_goals "$wiki"
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

  mkdir -p "$tmp/goals/vendor-eval" "$tmp/goals/old-goal"
  printf '# Goals\n\n## Active\n- vendor-eval: Evaluate vendor X vs Y\n\n## Done\n- old-goal: Finished thing\n' > "$tmp/goals.md"

  archive "$tmp" "2026-01-15"

  [ -f "$tmp/journal/2026/01/2026-01-15.md" ] || { echo "FAIL: journal not archived"; exit 1; }
  [ -f "$tmp/research/2026/01/2026-01-15/00-demo/explores/01-x.md" ] || { echo "FAIL: research not archived"; exit 1; }
  [ -d "$tmp/research/2026/01/2026-01-15/01-old-goal" ] || { echo "FAIL: done goal not archived"; exit 1; }
  [ ! -d "$tmp/goals/old-goal" ] || { echo "FAIL: done goal dir not removed"; exit 1; }
  grep -q "old-goal" "$tmp/goals.md" && { echo "FAIL: done goal still listed in goals.md"; exit 1; }
  grep -q "^- vendor-eval:" "$tmp/goals.md" || { echo "FAIL: active goal dropped from goals.md"; exit 1; }
  [ -L "$tmp/today/research/00-vendor-eval" ] || { echo "FAIL: active goal not relinked into today/research"; exit 1; }

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
