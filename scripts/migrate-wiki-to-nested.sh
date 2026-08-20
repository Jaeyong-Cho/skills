#!/bin/bash
# Migrates ~/wiki from flat journal/research structure to nested
# journal/YYYY/MM/YYYY-MM-DD/{journal.md,handoff.md,report.md,research/} structure.
# Run once; idempotent — running it twice changes nothing the second time.
set -euo pipefail

migrate() {
  local wiki="$1"

  # Migrate each flat journal file to nested structure
  if [ -d "$wiki/journal" ]; then
    find "$wiki/journal" -maxdepth 4 -type f -name "????-??-??.md" | while read -r jfile; do
      local dir=$(dirname "$jfile")
      local basename=$(basename "$jfile" .md)
      local nested_dir="$dir/$basename"

      # Skip if already migrated (nested dir exists with journal.md inside)
      if [ -d "$nested_dir" ] && [ -f "$nested_dir/journal.md" ]; then
        continue
      fi

      # Assertion: destination must be a directory or not exist
      if [ -e "$nested_dir" ] && [ ! -d "$nested_dir" ]; then
        echo "ERROR: $nested_dir exists but is not a directory (half-migrated fixture?)" >&2
        exit 1
      fi

      # Create nested directory
      mkdir -p "$nested_dir"

      # Move the flat journal file to journal.md
      if [ -f "$jfile" ]; then
        mv "$jfile" "$nested_dir/journal.md"
      fi

      # Move matching handoff file
      local handoff_file="$dir/$basename-handoff.md"
      if [ -f "$handoff_file" ]; then
        mv "$handoff_file" "$nested_dir/handoff.md"
      fi

      # Move matching report file
      local report_file="$dir/$basename-report.md"
      if [ -f "$report_file" ]; then
        mv "$report_file" "$nested_dir/report.md"
      fi

      # Move matching research directory
      local research_source="$wiki/research/$(echo "$basename" | cut -d- -f1)/$(echo "$basename" | cut -d- -f2)/$basename"
      if [ -d "$research_source" ]; then
        mkdir -p "$nested_dir/research"
        # Move all subdirectories from research_source into nested_dir/research
        for subdir in "$research_source"/*/; do
          [ -d "$subdir" ] || continue
          mv "$subdir" "$nested_dir/research/"
        done
        # Clean up empty research_source directory
        rmdir "$research_source" 2>/dev/null || true
      fi
    done
  fi

  # Fix index.md link lines: ./YYYY-MM-DD.md -> ./YYYY-MM-DD/journal.md
  if [ -d "$wiki/journal" ]; then
    find "$wiki/journal" -name "index.md" -type f | while read -r idx; do
      # Only update links that point to flat files (not already nested)
      sed -i '' 's|\./\([0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}\)\.md|\./\1/journal.md|g' "$idx" 2>/dev/null || true
    done
  fi

  # Remove top-level research/ and advisor/ directories
  rm -rf "$wiki/research" "$wiki/advisor"

  echo "Migration complete: $wiki"
}

self_test() {
  local tmp
  local year="2026" month="01" day="15"
  local datestr="$year-$month-$day"

  tmp="$(mktemp -d)"

  # Test 1: Fresh migration
  mkdir -p "$tmp/journal/$year/$month"
  mkdir -p "$tmp/research/$year/$month/$datestr/00-demo"
  echo "journal content" > "$tmp/journal/$year/$month/$datestr.md"
  echo "handoff content" > "$tmp/journal/$year/$month/$datestr-handoff.md"
  echo "report content" > "$tmp/journal/$year/$month/$datestr-report.md"
  echo "research content" > "$tmp/research/$year/$month/$datestr/00-demo/notes.md"

  # Create an index.md with flat links
  cat > "$tmp/journal/$year/$month/index.md" << 'EOF'
# 2026-01

- [2026-01-15](./2026-01-15.md)
EOF

  migrate "$tmp"

  [ -f "$tmp/journal/$year/$month/$datestr/journal.md" ] || { echo "FAIL: journal not migrated to nested dir"; exit 1; }
  [ -f "$tmp/journal/$year/$month/$datestr/handoff.md" ] || { echo "FAIL: handoff not migrated"; exit 1; }
  [ -f "$tmp/journal/$year/$month/$datestr/report.md" ] || { echo "FAIL: report not migrated"; exit 1; }
  [ -f "$tmp/journal/$year/$month/$datestr/research/00-demo/notes.md" ] || { echo "FAIL: research not migrated"; exit 1; }
  [ ! -f "$tmp/journal/$year/$month/$datestr.md" ] || { echo "FAIL: old flat journal file still exists"; exit 1; }
  [ ! -d "$tmp/research" ] || { echo "FAIL: research/ directory not removed"; exit 1; }
  grep -q "./2026-01-15/journal.md" "$tmp/journal/$year/$month/index.md" || { echo "FAIL: index.md link not updated"; exit 1; }

  rm -rf "$tmp"

  # Test 2: Idempotent re-run (already migrated)
  tmp="$(mktemp -d)"
  mkdir -p "$tmp/journal/$year/$month/$datestr"
  mkdir -p "$tmp/journal/$year/$month/$datestr/research/00-demo"
  echo "journal content" > "$tmp/journal/$year/$month/$datestr/journal.md"
  echo "research content" > "$tmp/journal/$year/$month/$datestr/research/00-demo/notes.md"

  migrate "$tmp"

  [ -f "$tmp/journal/$year/$month/$datestr/journal.md" ] || { echo "FAIL: idempotent run corrupted journal"; exit 1; }
  [ -f "$tmp/journal/$year/$month/$datestr/research/00-demo/notes.md" ] || { echo "FAIL: idempotent run corrupted research"; exit 1; }
  [ ! -d "$tmp/research" ] || { echo "FAIL: research/ not removed on idempotent run"; exit 1; }

  rm -rf "$tmp"

  # Test 3: Advisor removal
  tmp="$(mktemp -d)"
  mkdir -p "$tmp/journal/$year/$month"
  mkdir -p "$tmp/advisor/$year/$month"
  echo "advisor content" > "$tmp/advisor/$year/$month/$datestr.md"

  migrate "$tmp"

  [ ! -d "$tmp/advisor" ] || { echo "FAIL: advisor/ directory not removed"; exit 1; }

  rm -rf "$tmp"

  echo "self-test passed"
}

if [ "${1:-}" = "--test" ]; then
  self_test
  exit 0
fi

migrate "$HOME/wiki"
