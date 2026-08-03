#!/usr/bin/env bash
set -e

SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
CLAUDE_MD="$SKILLS_DIR/CLAUDE.md"
CLAUDE_SKILLS_DIR="$CLAUDE_DIR/skills"

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

install_skill_library() {
  local source_root destination_root dir manifest name

  mkdir -p "$CLAUDE_SKILLS_DIR"
  source_root="$(cd "$SKILLS_DIR" && pwd -P)"
  destination_root="$(cd "$CLAUDE_SKILLS_DIR" && pwd -P)"

  if [ "$source_root" = "$destination_root" ]; then
    echo "  ✓ skill library already at $CLAUDE_SKILLS_DIR"
    return
  fi

  # Clear what a previous run of this script installed so renamed/removed
  # skills (e.g. socratic → deleted, viz-gallery → renamed viewpoints) don't
  # linger. Tracked via a manifest since "skills" flattens directly under
  # $CLAUDE_SKILLS_DIR alongside anything else that may live there.
  manifest="$CLAUDE_SKILLS_DIR/.installed-by-skills-repo"
  if [ -f "$manifest" ]; then
    while IFS= read -r name; do
      [ -n "$name" ] && rm -rf "${CLAUDE_SKILLS_DIR:?}/$name"
    done < "$manifest"
  fi
  for dir in references preferences template; do
    rm -rf "${CLAUDE_SKILLS_DIR:?}/$dir"
  done

  # "skills" is special: its contents must land directly under
  # $CLAUDE_SKILLS_DIR (e.g. $CLAUDE_SKILLS_DIR/archi), not nested one level
  # deeper as $CLAUDE_SKILLS_DIR/skills/archi — Claude Code only discovers
  # skills at $CLAUDE_SKILLS_DIR/<name>/SKILL.md.
  if [ -d "$SKILLS_DIR/skills" ]; then
    cp -R "$SKILLS_DIR/skills/." "$CLAUDE_SKILLS_DIR/"
    (cd "$SKILLS_DIR/skills" && ls -1) > "$manifest"
  fi

  for dir in references preferences template; do
    [ -d "$SKILLS_DIR/$dir" ] || continue
    cp -R "$SKILLS_DIR/$dir" "$CLAUDE_SKILLS_DIR/"
  done
  echo "  ✓ skill library → $CLAUDE_SKILLS_DIR (skills, references, preferences, template)"
}

setup_claude() {
  echo "→ Claude Code"

  install_skill_library

  if [ -f "$CLAUDE_DIR/CLAUDE.md" ] && [ ! -L "$CLAUDE_DIR/CLAUDE.md" ]; then
    cp "$CLAUDE_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md.bak"
    echo "  backed up existing CLAUDE.md"
  fi
  ln -sf "$CLAUDE_MD" "$CLAUDE_DIR/CLAUDE.md"
  echo "  ✓ ~/.claude/CLAUDE.md → $CLAUDE_MD"

  setup_tmux_agent_status_claude

  ensure_rtk_binary
  if command -v rtk &>/dev/null; then
    rtk init -g --auto-patch &>/dev/null \
      && echo "  ✓ rtk hooks (rtk init -g)" \
      || echo "  rtk init failed, run manually: rtk init -g"
  fi

  if command -v claude &>/dev/null; then
    claude plugin marketplace add Egonex-AI/Understand-Anything &>/dev/null \
      && claude plugin install understand-anything &>/dev/null \
      && echo "  ✓ Understand-Anything plugin" \
      || echo "  Understand-Anything install failed, run manually: claude plugin marketplace add Egonex-AI/Understand-Anything && claude plugin install understand-anything"

    claude plugin marketplace add DietrichGebert/ponytail &>/dev/null \
      && claude plugin install ponytail@ponytail &>/dev/null \
      && echo "  ✓ ponytail plugin" \
      || echo "  ponytail install failed, run manually: claude plugin marketplace add DietrichGebert/ponytail && claude plugin install ponytail@ponytail"
  fi
}

setup_copilot() {
  echo "→ GitHub Copilot CLI"

  mkdir -p "$HOME/.copilot"
  ln -sf "$SKILLS_DIR/copilot-instructions.md" "$HOME/.copilot/copilot-instructions.md"
  echo "  ✓ ~/.copilot/copilot-instructions.md → $SKILLS_DIR/AGENTS.md"

  # Install skills, preferences and references for Copilot CLI, if the user has a ~/.copilot/skills directory.
  if [ -d "$HOME/.copilot" ]; then
      # Clear existing skills and references to avoid duplicates
      rm -rf "$HOME/.copilot/skills" "$HOME/.copilot/preferences" "$HOME/.copilot/references"
      cp -R "$SKILLS_DIR/skills/." "$HOME/.copilot/skills"
      cp -R "$SKILLS_DIR/references/." "$HOME/.copilot/skills/references"
      cp -R "$SKILLS_DIR/preferences/." "$HOME/.copilot/skills/preferences"
      cp -R "$SKILLS_DIR/template/." "$HOME/.copilot/skills/template"
      echo "  ✓ skills and references → ~/.copilot"
  fi

  # Copilot CLI has no hooks API — tmux-agent-status can only see it via
  # process presence auto-detection, not working/done transitions.
  echo "  note: tmux-agent-status has no hook support for Copilot CLI (process presence only)"

  ensure_rtk_binary
  if command -v rtk &>/dev/null; then
    rtk init -g --copilot --auto-patch &>/dev/null \
      && echo "  ✓ rtk hooks (rtk init -g --copilot)" \
      || echo "  rtk init failed, run manually: rtk init -g --copilot"
  fi

  if command -v copilot &>/dev/null; then
    copilot plugin install Egonex-AI/Understand-Anything:understand-anything-plugin &>/dev/null \
      && echo "  ✓ Understand-Anything plugin" \
      || echo "  Understand-Anything install failed, run manually: copilot plugin install Egonex-AI/Understand-Anything:understand-anything-plugin"

    copilot plugin marketplace add DietrichGebert/ponytail &>/dev/null \
      && copilot plugin install ponytail@ponytail &>/dev/null \
      && echo "  ✓ ponytail plugin" \
      || echo "  ponytail install failed, run manually: copilot plugin marketplace add DietrichGebert/ponytail && copilot plugin install ponytail@ponytail"
  fi
}

# ── rtk binary ───────────────────────────────────────────────────────────────
# https://github.com/rtk-ai/rtk — CLI proxy that filters/compresses command
# output before it reaches the agent's context.

ensure_rtk_binary() {
  command -v rtk &>/dev/null && return

  echo "  installing rtk..."
  if command -v brew &>/dev/null; then
    brew install rtk &>/dev/null
  else
    curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
  fi
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
