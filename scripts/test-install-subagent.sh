#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/bin"
ln -s "$(command -v node)" "$TMP/bin/node"
cat > "$TMP/bin/pi" <<'SH'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$PI_LOG"
if [ "${1:-}" = "--list-models" ]; then
  printf 'provider model context max-out thinking images\nalpha one 1K 1K yes no\nbeta two 2K 2K yes yes\n'
fi
SH
chmod +x "$TMP/bin/pi"

SOURCE="$TMP/home/.pi/agent/git/github.com/HazAT/pi-interactive-subagents/pi-extension/subagents/cmux.ts"
mkdir -p "$(dirname "$SOURCE")"
cat > "$SOURCE" <<'TS'
    if (!pane.startsWith("%")) {
      throw new Error(`Unexpected tmux split-window output: ${pane}`);
    }

    return pane;
TS

printf '2\n4\n' | HOME="$TMP/home" PATH="$TMP/bin:/usr/bin:/bin" PI_LOG="$TMP/pi.log" \
  "$ROOT/install.sh" --subagent >/dev/null

for file in "$TMP/home/.pi/agent/agents"/*.md; do
  grep -q '^model: beta/two$' "$file"
  grep -q '^thinking: medium$' "$file"
done
node -e '
  const settings = require(process.argv[1]);
  if (settings.subagents.defaultModel !== "beta/two") process.exit(1);
  if (settings.subagents.defaultThinking !== "medium") process.exit(1);
  if ("tuiMode" in settings || "terminal" in settings) process.exit(1);
' "$TMP/home/.pi/agent/settings.json"
node -e '
  const models = require(process.argv[1]);
  if (models.providers.beta.modelOverrides.two.contextWindow !== 1000000) process.exit(1);
' "$TMP/home/.pi/agent/models.json"
[ "$(grep -c '^install ' "$TMP/pi.log")" -eq 1 ]
grep -q '^install git:github.com/HazAT/pi-interactive-subagents$' "$TMP/pi.log"
grep -q 'select-layout", "-t", pane, "even-horizontal"' "$SOURCE"
[ ! -e "$TMP/home/.agents" ]
[ ! -e "$TMP/home/.local" ]

echo "subagent installer test passed"
