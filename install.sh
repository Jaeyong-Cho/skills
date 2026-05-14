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

# ── 3. GitHub Copilot CLI ─────────────────────────────────────────────────────

echo ""
echo "→ GitHub Copilot CLI"

if ! command -v gh &>/dev/null; then
  echo "  gh not found — skipping Copilot CLI setup"
else
  # Detect shell rc file
  SHELL_RC=""
  case "$SHELL" in
    */zsh)  SHELL_RC="$HOME/.zshrc" ;;
    */bash) SHELL_RC="$HOME/.bashrc" ;;
  esac

  MARKER="# gh copilot aliases (added by skills/install.sh)"

  if [ -n "$SHELL_RC" ] && ! grep -qF "$MARKER" "$SHELL_RC" 2>/dev/null; then
    {
      echo ""
      echo "$MARKER"
      echo 'eval "$(gh copilot alias -- zsh 2>/dev/null || gh copilot alias -- bash 2>/dev/null)"'
    } >> "$SHELL_RC"
    echo "  ✓ added gh copilot aliases to $SHELL_RC (ghcs = suggest, ghce = explain)"
    echo "  reload shell or run: source $SHELL_RC"
  else
    echo "  already configured"
  fi
fi

echo ""
echo "Done."
