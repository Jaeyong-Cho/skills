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

detect "claude"   "Claude Code        (claude CLI)"  "command -v claude"
detect "copilot"  "GitHub Copilot CLI (copilot)"     "command -v copilot"
detect "vscode"   "VS Code + Copilot  (code)"        \
  "[ -f \"$HOME/Library/Application Support/Code/User/settings.json\" ]" \
  "[ -f \"$HOME/.config/Code/User/settings.json\" ]"
detect "cursor"   "Cursor             (cursor)"      \
  "command -v cursor" "[ -d '/Applications/Cursor.app' ]"
detect "windsurf" "Windsurf           (windsurf)"    \
  "command -v windsurf" "[ -d '/Applications/Windsurf.app' ]"

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

  # Already in shell rc?
  if [ -n "$rc" ] && grep -q 'export PFJ_PATH=' "$rc" 2>/dev/null; then
    PFJ_PATH_VALUE=$(grep 'export PFJ_PATH=' "$rc" | tail -1 | sed 's/export PFJ_PATH="\(.*\)"/\1/' | sed "s/export PFJ_PATH='\(.*\)'/\1/" | sed 's/export PFJ_PATH=//')
    echo "  PFJ_PATH already in $rc: $PFJ_PATH_VALUE"
    return
  fi

  # Already in environment?
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

  # CLAUDE.md symlink
  if [ -f "$CLAUDE_DIR/CLAUDE.md" ] && [ ! -L "$CLAUDE_DIR/CLAUDE.md" ]; then
    cp "$CLAUDE_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md.bak"
    echo "  backed up existing CLAUDE.md"
  fi
  ln -sf "$CLAUDE_MD" "$CLAUDE_DIR/CLAUDE.md"
  echo "  ✓ ~/.claude/CLAUDE.md → $CLAUDE_MD"

  # PFJ_PATH in shell rc (shared)
  setup_pfj_path

  # Also mirror into Claude settings.json (Claude Code reads env from here)
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

  # AGENTS.md symlink (copilot reads AGENTS.md from COPILOT_CUSTOM_INSTRUCTIONS_DIRS)
  ln -sf "$SKILLS_DIR/AGENTS.md" "$CLAUDE_DIR/AGENTS.md"
  echo "  ✓ ~/.claude/AGENTS.md → $SKILLS_DIR/AGENTS.md"

  # PFJ_PATH in shell rc (shared)
  setup_pfj_path

  # COPILOT_CUSTOM_INSTRUCTIONS_DIRS in shell rc
  local rc
  rc="$(shell_rc)"
  local marker="# copilot custom instructions (added by skills/install.sh)"
  if [ -n "$rc" ] && ! grep -qF "$marker" "$rc" 2>/dev/null; then
    { echo ""; echo "$marker"
      echo "export COPILOT_CUSTOM_INSTRUCTIONS_DIRS=\"\$HOME/.claude\""
    } >> "$rc"
    echo "  ✓ COPILOT_CUSTOM_INSTRUCTIONS_DIRS → $rc"
  else
    echo "  COPILOT_CUSTOM_INSTRUCTIONS_DIRS already configured"
  fi
}

setup_vscode() {
  echo "→ VS Code + Copilot"
  local settings=""
  for candidate in \
    "$HOME/Library/Application Support/Code/User/settings.json" \
    "$HOME/.config/Code/User/settings.json"
  do
    [ -f "$candidate" ] && settings="$candidate" && break
  done
  [ -z "$settings" ] && echo "  settings.json not found — skipping" && return

  python3 - "$settings" "$CLAUDE_MD" <<'PYEOF'
import json, sys
settings_path, claude_md_path = sys.argv[1], sys.argv[2]
try:
    with open(settings_path) as f: s = json.load(f)
except json.JSONDecodeError:
    print("  WARNING: settings.json invalid JSON — skipping"); sys.exit(0)
entry = {"file": claude_md_path}
keys = ["github.copilot.chat.codeGeneration.instructions",
        "github.copilot.chat.reviewSelection.instructions"]
changed = False
for key in keys:
    lst = s.get(key, [])
    if not any(i.get("file") == claude_md_path for i in lst):
        lst.append(entry); s[key] = lst; changed = True
if changed:
    with open(settings_path, "w") as f: json.dump(s, f, indent=2)
    print("  ✓ added CLAUDE.md reference to Copilot instructions")
else:
    print("  already configured")
PYEOF
}

setup_cursor() {
  echo "→ Cursor"
  local rules_dir="$HOME/.cursor/rules"
  mkdir -p "$rules_dir"
  local dest="$rules_dir/global.md"
  if [ -L "$dest" ] || [ ! -f "$dest" ]; then
    ln -sf "$CLAUDE_MD" "$dest"
    echo "  ✓ $dest → $CLAUDE_MD"
  else
    echo "  $dest already exists (not a symlink) — skipping"
  fi
}

setup_windsurf() {
  echo "→ Windsurf"
  local rules_dir="$HOME/.codeium/windsurf"
  mkdir -p "$rules_dir"
  local dest="$rules_dir/global_rules.md"
  if [ -L "$dest" ] || [ ! -f "$dest" ]; then
    ln -sf "$CLAUDE_MD" "$dest"
    echo "  ✓ $dest → $CLAUDE_MD"
  else
    echo "  $dest already exists (not a symlink) — skipping"
  fi
}

# ── Run selected setups ───────────────────────────────────────────────────────

echo ""
selected "claude"   && setup_claude   && echo ""
selected "copilot"  && setup_copilot  && echo ""
selected "vscode"   && setup_vscode   && echo ""
selected "cursor"   && setup_cursor   && echo ""
selected "windsurf" && setup_windsurf && echo ""

echo "Done."
