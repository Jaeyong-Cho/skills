#!/usr/bin/env bash
# Self-check for commit-msg: asserts pass/reject cases. Run directly, from anywhere.
set -euo pipefail

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
hook="$dir/commit-msg"
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

check_pass() { printf '%s\n' "$1" > "$tmp"; "$hook" "$tmp" || { echo "FAIL (expected pass): $1"; exit 1; }; }
check_fail() { printf '%s\n' "$1" > "$tmp"; "$hook" "$tmp" 2>/dev/null && { echo "FAIL (expected reject): $1"; exit 1; }; return 0; }

check_pass "feat(setup): add commit-msg hook"
check_pass "fix(parser): handle empty scope"
check_pass "chore!: drop node 14 support"
check_pass "Merge branch 'main' into feature/x"
check_fail "added stuff"
check_fail "Feat(setup): wrong case"
check_fail "feat: $(python3 -c 'print("x"*120)' 2>/dev/null || perl -e 'print "x"x120')"

echo "ok: commit-msg self-check passed"
