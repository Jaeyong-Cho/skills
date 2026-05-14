#!/usr/bin/env bash
set -e

SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
CLAUDE_SETTINGS="$CLAUDE_DIR/settings.json"

echo "=== Skills Install ==="
echo ""

# ── 1. CLAUDE.md symlink ──────────────────────────────────────────────────────

echo "→ CLAUDE.md"
if [ -f "$CLAUDE_DIR/CLAUDE.md" ] && [ ! -L "$CLAUDE_DIR/CLAUDE.md" ]; then
  cp "$CLAUDE_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md.bak"
  echo "  backed up existing CLAUDE.md → CLAUDE.md.bak"
fi
ln -sf "$SKILLS_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
echo "  ✓ ~/.claude/CLAUDE.md → $SKILLS_DIR/CLAUDE.md"

# ── 2. PFJ_PATH in Claude settings.json ─────────────────────────────────────

echo ""
echo "→ Claude settings (PFJ_PATH)"
if [ ! -f "$CLAUDE_SETTINGS" ]; then
  echo '{}' > "$CLAUDE_SETTINGS"
fi

EXISTING=$(python3 -c "
import json
try:
    d = json.load(open('$CLAUDE_SETTINGS'))
    print(d.get('env', {}).get('PFJ_PATH', ''))
except:
    print('')
" 2>/dev/null || echo "")

if [ -n "$EXISTING" ]; then
  echo "  already set: $EXISTING"
else
  read -rp "  pfj directory path [~/pofe]: " PFJ_INPUT
  PFJ_RAW="${PFJ_INPUT:-$HOME/pofe}"
  PFJ_PATH="${PFJ_RAW/#\~/$HOME}"

  python3 -c "
import json
path = '$CLAUDE_SETTINGS'
with open(path) as f:
    d = json.load(f)
d.setdefault('env', {})['PFJ_PATH'] = '$PFJ_PATH'
with open(path, 'w') as f:
    json.dump(d, f, indent=2)
print('  ✓ PFJ_PATH =', '$PFJ_PATH')
"
fi

# ── 3. GitHub Copilot (VS Code) ───────────────────────────────────────────────

echo ""
echo "→ GitHub Copilot (VS Code)"

VSCODE_SETTINGS=""
for candidate in \
  "$HOME/Library/Application Support/Code/User/settings.json" \
  "$HOME/Library/Application Support/Code - Insiders/User/settings.json" \
  "$HOME/.config/Code/User/settings.json"
do
  if [ -f "$candidate" ]; then
    VSCODE_SETTINGS="$candidate"
    break
  fi
done

if [ -z "$VSCODE_SETTINGS" ]; then
  echo "  VS Code settings not found — skipping Copilot setup"
else
  CLAUDE_MD_PATH="$CLAUDE_DIR/CLAUDE.md"
  python3 - "$VSCODE_SETTINGS" "$CLAUDE_MD_PATH" <<'PYEOF'
import json, sys

settings_path, claude_md_path = sys.argv[1], sys.argv[2]

with open(settings_path) as f:
    content = f.read()

try:
    settings = json.loads(content)
except json.JSONDecodeError:
    print("  WARNING: VS Code settings.json is not valid JSON — skipping")
    sys.exit(0)

entry = {"file": claude_md_path}
keys = [
    "github.copilot.chat.codeGeneration.instructions",
    "github.copilot.chat.reviewSelection.instructions",
]

changed = False
for key in keys:
    instructions = settings.get(key, [])
    if not any(i.get("file") == claude_md_path for i in instructions):
        instructions.append(entry)
        settings[key] = instructions
        changed = True

if changed:
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)
    print(f"  ✓ added CLAUDE.md reference to Copilot instructions")
else:
    print(f"  already configured")
PYEOF
fi

echo ""
echo "Done."
