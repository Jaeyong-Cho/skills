#!/bin/bash
# ---
# type: Shell Script
# title: Append to KB ingestion log
# description: Appends a formatted line to the KB ingestion log, creating the log file if needed.
# tags: [kb, log, archive]
# timestamp: 2026-08-20T00:00:00+09:00
# ---

set -euo pipefail

append_log() {
  local log_file="$1" date="$2" slugs="$3"

  # Assertion: log-file path must be non-empty
  [ -n "$log_file" ] || { echo "ERROR: log file path is empty"; exit 1; }

  # Assertion: parent directory must be creatable
  local parent_dir="$(dirname "$log_file")"
  mkdir -p "$parent_dir" || { echo "ERROR: could not create parent directory: $parent_dir"; exit 1; }

  # Append the log line
  local log_line="## [$date] ingest | $slugs"
  echo "$log_line" >> "$log_file"

  # Assertion: verify the appended line matches the format
  local last_line
  last_line=$(tail -1 "$log_file")
  [[ "$last_line" =~ ^##\ \[[0-9]{4}-[0-9]{2}-[0-9]{2}\]\ ingest\ \| ]] || {
    echo "ERROR: appended line does not match expected format: $last_line"
    exit 1
  }
}

self_test() {
  local tmp log_file

  tmp="$(mktemp -d)"
  log_file="$tmp/log.md"

  # Test 1: Fresh file creation
  append_log "$log_file" "2026-01-15" "a,b"
  [ -f "$log_file" ] || { echo "FAIL: log file not created"; exit 1; }
  grep -q "^## \[2026-01-15\] ingest | a,b$" "$log_file" || { echo "FAIL: log line not formatted correctly"; exit 1; }

  # Test 2: Append without clobbering
  append_log "$log_file" "2026-01-16" "c,d"
  local line_count
  line_count=$(grep -c "^## \[" "$log_file" || true)
  [ "$line_count" = "2" ] || { echo "FAIL: append clobbered previous line or didn't append"; exit 1; }

  # Test 3: Newest entry is last
  local newest
  newest=$(grep "^## \[" "$log_file" | tail -1)
  [[ "$newest" =~ 2026-01-16 ]] || { echo "FAIL: newest entry is not last"; exit 1; }

  # Test 4: Parent directory creation with nested path
  local nested_log="$tmp/nested/deep/log.md"
  append_log "$nested_log" "2026-01-17" "e"
  [ -f "$nested_log" ] || { echo "FAIL: nested log file not created"; exit 1; }

  rm -rf "$tmp"
  echo "self-test passed"
}

if [ "${1:-}" = "--test" ]; then
  self_test
  exit 0
fi

# Normal usage: append_log <log-file> <date> <slugs>
[ $# -eq 3 ] || { echo "Usage: append_log.sh <log-file> <YYYY-MM-DD> <comma-separated-slugs>"; exit 1; }
append_log "$1" "$2" "$3"
