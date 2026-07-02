#!/usr/bin/env bash
set -e

SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
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

# ── Setup functions ───────────────────────────────────────────────────────────

setup_claude() {
  echo "→ Claude Code"

  if [ -f "$CLAUDE_DIR/CLAUDE.md" ] && [ ! -L "$CLAUDE_DIR/CLAUDE.md" ]; then
    cp "$CLAUDE_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md.bak"
    echo "  backed up existing CLAUDE.md"
  fi
  ln -sf "$CLAUDE_MD" "$CLAUDE_DIR/CLAUDE.md"
  echo "  ✓ ~/.claude/CLAUDE.md → $CLAUDE_MD"

  setup_tmux_agent_status_claude
}

setup_copilot() {
  echo "→ GitHub Copilot CLI"

  mkdir -p "$HOME/.copilot"
  ln -sf "$SKILLS_DIR/copilot-instructions.md" "$HOME/.copilot/copilot-instructions.md"
  echo "  ✓ ~/.copilot/copilot-instructions.md → $SKILLS_DIR/AGENTS.md"

  # Copilot CLI has no hooks API — tmux-agent-status can only see it via
  # process presence auto-detection, not working/done transitions.
  echo "  note: tmux-agent-status has no hook support for Copilot CLI (process presence only)"
}

# ── tmux-agent-status hook wiring ────────────────────────────────────────────
# https://github.com/samleeney/tmux-agent-status — merges into settings.json
# without clobbering existing hooks/settings; skips if jq or the plugin
# (installed via TPM) aren't present.

add_json_hook() {
  local settings="$1" event="$2" cmd="$3"
  local tmp
  tmp="$(mktemp)"
  jq --arg event "$event" --arg cmd "$cmd" '
    .hooks[$event] = ((.hooks[$event] // []) as $existing |
      if ($existing | any(.hooks[]?.command == $cmd)) then $existing
      else $existing + [{"hooks": [{"type": "command", "command": $cmd}]}]
      end)
  ' "$settings" > "$tmp" && mv "$tmp" "$settings"
}

setup_tmux_agent_status_claude() {
  local hook_script="$HOME/.tmux/plugins/tmux-agent-status/hooks/better-hook.sh"
  if [ ! -x "$hook_script" ]; then
    return
  fi
  if ! command -v jq &>/dev/null; then
    echo "  jq not found, skipping tmux-agent-status hooks"
    return
  fi

  local settings="$CLAUDE_DIR/settings.json"
  [ -f "$settings" ] || echo '{}' > "$settings"

  local event
  for event in UserPromptSubmit PreToolUse Stop Notification; do
    add_json_hook "$settings" "$event" "~/.tmux/plugins/tmux-agent-status/hooks/better-hook.sh $event"
  done
  echo "  ✓ tmux-agent-status hooks → ~/.claude/settings.json"
}

# ── Bin scripts ──────────────────────────────────────────────────────────────

setup_bin() {
  local bin_src="$SKILLS_DIR/bin"
  local bin_dst="$HOME/.local/bin"
  [ -d "$bin_src" ] || return
  mkdir -p "$bin_dst"
  echo "→ bin scripts → $bin_dst"
  for f in "$bin_src"/*; do
    local name
    name="$(basename "$f")"
    ln -sf "$f" "$bin_dst/$name"
    echo "  ✓ $name"
  done
}

# ── Run selected setups ───────────────────────────────────────────────────────

echo ""
selected "claude"  && setup_claude  && echo ""
selected "copilot" && setup_copilot && echo ""
setup_bin && echo ""

echo "Done."
