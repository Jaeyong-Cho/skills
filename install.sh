#!/usr/bin/env bash
set -e

SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
CLAUDE_SETTINGS="$CLAUDE_DIR/settings.json"
CLAUDE_MD="$SKILLS_DIR/CLAUDE.md"

echo "=== Skills Install ==="
echo ""

# ── Detect installed agents ───────────────────────────────────────────────────

declare -a DETECTED_KEYS
declare -a DETECTED_LABELS

detect() {
  local key="$1" label="$2"; shift 2
  for cmd in "$@"; do
    if eval "$cmd" &>/dev/null; then
      DETECTED_KEYS+=("$key")
      DETECTED_LABELS+=("$label")
      return
    fi
  done
}

detect "claude"  "Claude Code        (claude CLI)" "command -v claude"
detect "copilot" "GitHub Copilot CLI (copilot)"    "command -v copilot"

if [ ${#DETECTED_KEYS[@]} -eq 0 ]; then
  echo "No supported AI agents detected. Exiting."
  exit 0
fi

echo "Detected agents:"
for i in "${!DETECTED_KEYS[@]}"; do
  echo "  $((i+1))) ${DETECTED_LABELS[$i]}"
done
echo ""
read -rp "Which to set up? (numbers separated by spaces, or 'all') [all]: " SELECTION
SELECTION="${SELECTION:-all}"

selected() {
  local key="$1"
  [ "$SELECTION" = "all" ] && return 0
  for i in "${!DETECTED_KEYS[@]}"; do
    if [ "${DETECTED_KEYS[$i]}" = "$key" ]; then
      echo " $SELECTION " | grep -qw "$((i+1))" && return 0
    fi
  done
  return 1
}

# ── Shared: shell rc path ─────────────────────────────────────────────────────

shell_rc() {
  case "$SHELL" in
    */zsh)  echo "$HOME/.zshrc" ;;
    */bash) echo "$HOME/.bashrc" ;;
    *)      echo "" ;;
  esac
}

# ── Shared: PFJ_PATH ──────────────────────────────────────────────────────────

PFJ_PATH_VALUE=""

setup_pfj_path() {
  local rc
  rc="$(shell_rc)"

  if [ -n "$rc" ] && grep -q 'export PFJ_PATH=' "$rc" 2>/dev/null; then
    PFJ_PATH_VALUE=$(grep 'export PFJ_PATH=' "$rc" | tail -1 | sed 's/export PFJ_PATH="\(.*\)"/\1/' | sed "s/export PFJ_PATH='\(.*\)'/\1/" | sed 's/export PFJ_PATH=//')
    echo "  PFJ_PATH already in $rc: $PFJ_PATH_VALUE"
    return
  fi

  if [ -n "$PFJ_PATH" ]; then
    PFJ_PATH_VALUE="$PFJ_PATH"
    echo "  PFJ_PATH already set in environment: $PFJ_PATH"
    return
  fi

  read -rp "  pfj directory path [~/pofe]: " PFJ_INPUT
  PFJ_PATH_VALUE="${PFJ_INPUT:-$HOME/pofe}"
  PFJ_PATH_VALUE="${PFJ_PATH_VALUE/#\~/$HOME}"

  if [ -n "$rc" ]; then
    local marker="# PFJ_PATH — journal directory (added by skills/install.sh)"
    { echo ""; echo "$marker"
      echo "export PFJ_PATH=\"$PFJ_PATH_VALUE\""
    } >> "$rc"
    echo "  ✓ PFJ_PATH=$PFJ_PATH_VALUE → $rc"
    echo "  reload shell or: source $rc"
  fi
}

# ── Setup functions ───────────────────────────────────────────────────────────

setup_claude() {
  echo "→ Claude Code"

  if [ -f "$CLAUDE_DIR/CLAUDE.md" ] && [ ! -L "$CLAUDE_DIR/CLAUDE.md" ]; then
    cp "$CLAUDE_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md.bak"
    echo "  backed up existing CLAUDE.md"
  fi
  ln -sf "$CLAUDE_MD" "$CLAUDE_DIR/CLAUDE.md"
  echo "  ✓ ~/.claude/CLAUDE.md → $CLAUDE_MD"

  setup_pfj_path

  [ ! -f "$CLAUDE_SETTINGS" ] && echo '{}' > "$CLAUDE_SETTINGS"
  python3 -c "
import json
with open('$CLAUDE_SETTINGS') as f: d = json.load(f)
if d.get('env', {}).get('PFJ_PATH') != '$PFJ_PATH_VALUE':
    d.setdefault('env', {})['PFJ_PATH'] = '$PFJ_PATH_VALUE'
    with open('$CLAUDE_SETTINGS', 'w') as f: json.dump(d, f, indent=2)
    print('  ✓ PFJ_PATH mirrored to ~/.claude/settings.json')
else:
    print('  settings.json already up to date')
"
}

setup_copilot() {
  echo "→ GitHub Copilot CLI"

  mkdir -p "$HOME/.copilot"
  ln -sf "$SKILLS_DIR/AGENTS.md" "$HOME/.copilot/copilot-instructions.md"
  echo "  ✓ ~/.copilot/copilot-instructions.md → $SKILLS_DIR/AGENTS.md"

  setup_pfj_path
}

# ── Run selected setups ───────────────────────────────────────────────────────

echo ""
selected "claude"  && setup_claude  && echo ""
selected "copilot" && setup_copilot && echo ""

echo "Done."
