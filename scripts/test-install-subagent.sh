#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/bin" "$TMP/home/.pi/agent/agents"
ln -s "$(command -v node)" "$TMP/bin/node"
cat > "$TMP/bin/pi" <<'SH'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$PI_LOG"
if [ "${1:-}" = "--list-models" ]; then printf 'provider model context max-out thinking images\nalpha one 1K 1K yes no\nbeta two 2K 2K yes yes\n'; fi
SH
chmod +x "$TMP/bin/pi"
printf '{"keep":true,"subagents":{"other":"preserve"}}\n' > "$TMP/home/.pi/agent/settings.json"
printf '{"providers":{"other":{"modelOverrides":{"keep":{"contextWindow":3}}}}}\n' > "$TMP/home/.pi/agent/models.json"
printf 'user agent\n' > "$TMP/home/.pi/agent/agents/user.md"
printf '2\n4\n' | HOME="$TMP/home" PATH="$TMP/bin:/usr/bin:/bin" PI_LOG="$TMP/pi.log" "$ROOT/bin/install-pi-subagent" >/dev/null
for file in "$TMP/home/.pi/agent/agents"/*.md; do [ "$(basename "$file")" = user.md ] && continue; grep -q '^model: beta/two$' "$file"; grep -q '^thinking: medium$' "$file"; done
[ -s "$TMP/home/.pi/agent/.installed-pi-subagents" ]
node -e 'const s=require(process.argv[1]); if(s.keep!==true||s.subagents.defaultModel!=="beta/two"||s.subagents.defaultThinking!=="medium"||s.subagents.other!=="preserve")process.exit(1)' "$TMP/home/.pi/agent/settings.json"
node -e 'const m=require(process.argv[1]); for(const [p,n] of [["beta","two"],["openai-codex","gpt-5.6-sol"],["openai-codex","gpt-5.6-terra"],["openai-codex","gpt-5.6-luna"],["openai-codex","gpt-6-astra"]])if(m.providers[p].modelOverrides[n].contextWindow!==1000000)process.exit(1); if(m.providers.other.modelOverrides.keep.contextWindow!==3)process.exit(1)' "$TMP/home/.pi/agent/models.json"
HOME="$TMP/home" PATH="$TMP/bin:/usr/bin:/bin" PI_LOG="$TMP/pi.log" "$ROOT/bin/uninstall-pi-subagent" >/dev/null
[ -f "$TMP/home/.pi/agent/agents/user.md" ]; [ ! -e "$TMP/home/.pi/agent/.installed-pi-subagents" ]
node -e 'const s=require(process.argv[1]); if(s.keep!==true||s.subagents.defaultModel||s.subagents.defaultThinking||s.subagents.other!=="preserve")process.exit(1)' "$TMP/home/.pi/agent/settings.json"
! HOME="$TMP/home" PATH="$TMP/bin:/usr/bin:/bin" "$ROOT/install.sh" --subagent >/dev/null 2>&1
rm -rf "$TMP/home/.pi/agent"; mkdir -p "$TMP/home/.pi/agent/agents"; printf 'user agent\n' > "$TMP/home/.pi/agent/agents/user.md"
printf '1\n' | HOME="$TMP/home" PATH="$TMP/bin:/usr/bin:/bin" PI_LOG="$TMP/pi.log" "$ROOT/install.sh" >/dev/null
[ -f "$TMP/home/.pi/agent/agents/user.md" ]; [ "$(find "$TMP/home/.pi/agent/agents" -type f | wc -l | tr -d ' ')" = 1 ]
node -e 'const s=require(process.argv[1]); if(s.subagents)process.exit(1)' "$TMP/home/.pi/agent/settings.json"
echo "subagent installer test passed"
