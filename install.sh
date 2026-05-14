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

detect "claude"   "Claude Code        (claude CLI)"          "command -v claude"
detect "copilot"  "GitHub Copilot CLI (gh copilot)"          "gh extension list 2>/dev/null | grep -q copilot"
detect "vscode"   "VS Code + Copilot  (code)"                \
  "[ -f \"$HOME/Library/Application Support/Code/User/settings.json\" ]" \
  "[ -f \"$HOME/.config/Code/User/settings.json\" ]"
detect "cursor"   "Cursor             (cursor)"              \
  "command -v cursor" \
  "[ -d '/Applications/Cursor.app' ]"
detect "windsurf" "Windsurf           (windsurf)"            \
  "command -v windsurf" \
  "[ -d '/Applications/Windsurf.app' ]"

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
  if [ "$SELECTION" = "all" ]; then return 0; fi
  for i in "${!DETECTED_KEYS[@]}"; do
    if [ "${DETECTED_KEYS[$i]}" = "$key" ]; then
      local n=$((i+1))
      echo " $SELECTION " | grep -qw "$n" && return 0
    fi
  done
  return 1
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

  # PFJ_PATH
  [ ! -f "$CLAUDE_SETTINGS" ] && echo '{}' > "$CLAUDE_SETTINGS"
  EXISTING=$(python3 -c "
import json
try:
    d = json.load(open('$CLAUDE_SETTINGS'))
    print(d.get('env', {}).get('PFJ_PATH', ''))
except: print('')
" 2>/dev/null || echo "")

  if [ -n "$EXISTING" ]; then
    echo "  PFJ_PATH already set: $EXISTING"
  else
    read -rp "  pfj directory path [~/pofe]: " PFJ_INPUT
    PFJ_PATH="${PFJ_INPUT:-$HOME/pofe}"
    PFJ_PATH="${PFJ_PATH/#\~/$HOME}"
    python3 -c "
import json
with open('$CLAUDE_SETTINGS') as f: d = json.load(f)
d.setdefault('env', {})['PFJ_PATH'] = '$PFJ_PATH'
with open('$CLAUDE_SETTINGS', 'w') as f: json.dump(d, f, indent=2)
print('  ✓ PFJ_PATH =', '$PFJ_PATH')
"
  fi
}

setup_copilot() {
  echo "→ GitHub Copilot CLI"
  SHELL_RC=""
  case "$SHELL" in
    */zsh)  SHELL_RC="$HOME/.zshrc" ;;
    */bash) SHELL_RC="$HOME/.bashrc" ;;
  esac
  MARKER="# gh copilot aliases (added by skills/install.sh)"
  if [ -n "$SHELL_RC" ] && ! grep -qF "$MARKER" "$SHELL_RC" 2>/dev/null; then
    { echo ""; echo "$MARKER"
      echo 'eval "$(gh copilot alias -- "${SHELL##*/}" 2>/dev/null)"'
    } >> "$SHELL_RC"
    echo "  ✓ added ghcs/ghce aliases to $SHELL_RC"
    echo "  reload shell or: source $SHELL_RC"
  else
    echo "  already configured"
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
