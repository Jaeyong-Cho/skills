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

# ── Plugin install (marketplace add is idempotent-unsafe on some CLIs —
#    ignore its exit code, only the install step's result decides success) ────

install_agent_plugin() {
  local cli="$1" marketplace_repo="$2" plugin_id="$3" label="$4"
  "$cli" plugin marketplace add "$marketplace_repo" &>/dev/null
  if "$cli" plugin install "$plugin_id" &>/dev/null; then
    echo "  ✓ $label"
  else
    echo "  $label install failed, run manually: $cli plugin marketplace add $marketplace_repo && $cli plugin install $plugin_id"
  fi
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
  for dir in references; do
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

  for dir in references; do
    [ -d "$SKILLS_DIR/$dir" ] || continue
    cp -R "$SKILLS_DIR/$dir" "$CLAUDE_SKILLS_DIR/"
  done
  echo "  ✓ skill library → $CLAUDE_SKILLS_DIR (skills, references)"
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
  setup_skill_journal_log_hook_claude

  ensure_rtk_binary
  if command -v rtk &>/dev/null; then
    rtk init -g --auto-patch &>/dev/null \
      && echo "  ✓ rtk hooks (rtk init -g)" \
      || echo "  rtk init failed, run manually: rtk init -g"
  fi

  if command -v claude &>/dev/null; then
    install_agent_plugin claude DietrichGebert/ponytail ponytail@ponytail "ponytail plugin"
    install_agent_plugin claude mattpocock/skills mattpocock-skills@mattpocock "mattpocock-skills plugin (grilling, grill-me)"
  fi
}

setup_copilot() {
  echo "→ GitHub Copilot CLI"

  mkdir -p "$HOME/.copilot"
  ln -sf "$SKILLS_DIR/copilot-instructions.md" "$HOME/.copilot/copilot-instructions.md"
  echo "  ✓ ~/.copilot/copilot-instructions.md → $SKILLS_DIR/copilot-instructions.md"

  # Install skills and references for Copilot CLI, if the user has a ~/.copilot/skills directory.
  if [ -d "$HOME/.copilot" ]; then
      # Clear existing skills and references to avoid duplicates
      rm -rf "$HOME/.copilot/skills" "$HOME/.copilot/references"
      cp -R "$SKILLS_DIR/skills/." "$HOME/.copilot/skills"
      cp -R "$SKILLS_DIR/references/." "$HOME/.copilot/skills/references"
      echo "  ✓ skills and references → ~/.copilot"
  fi

  setup_skill_journal_log_hook_copilot

  # tmux-agent-status itself has no Copilot CLI integration (process presence
  # auto-detection only) — unrelated to Copilot's own hook support, which
  # does exist (see setup_skill_journal_log_hook_copilot above).
  echo "  note: tmux-agent-status has no Copilot CLI support (process presence only)"

  ensure_rtk_binary
  if command -v rtk &>/dev/null; then
    rtk init -g --copilot --auto-patch &>/dev/null \
      && echo "  ✓ rtk hooks (rtk init -g --copilot)" \
      || echo "  rtk init failed, run manually: rtk init -g --copilot"
  fi

  if command -v copilot &>/dev/null; then
    install_agent_plugin copilot DietrichGebert/ponytail ponytail@ponytail "ponytail plugin"
    install_agent_plugin copilot mattpocock/skills mattpocock-skills@mattpocock "mattpocock-skills plugin (grilling, grill-me)"
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

# ── JSON hook wiring (shared) ────────────────────────────────────────────────
# add_json_hook merges one hook command into settings.json without clobbering
# existing hooks/settings, and is idempotent (skips if the command is already
# registered for that event). Used below by both tmux-agent-status and the
# skill-journal-log hook. matcher is optional — omit it to fire on every
# event of that type (tmux-agent-status wants that); pass a tool name (e.g.
# "Skill") to scope a PostToolUse/PreToolUse hook to just that tool.

add_json_hook() {
  local settings="$1" event="$2" cmd="$3" matcher="${4:-}"
  local tmp
  tmp="$(mktemp)"
  jq --arg event "$event" --arg cmd "$cmd" --arg matcher "$matcher" '
    .hooks[$event] = ((.hooks[$event] // []) as $existing |
      if ($existing | any(.hooks[]?.command == $cmd)) then $existing
      else $existing + [
        (if $matcher != "" then {"matcher": $matcher} else {} end)
        + {"hooks": [{"type": "command", "command": $cmd}]}
      ]
      end)
  ' "$settings" > "$tmp" && mv "$tmp" "$settings"
}

# https://github.com/samleeney/tmux-agent-status — skips if jq or the plugin
# (installed via TPM) aren't present.
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

# Logs every Skill-tool invocation to today's journal file — deterministic
# by design, since a model reliably forgets a passive "remember to log this"
# instruction over a long session. See hooks/skill-journal-log.sh.
setup_skill_journal_log_hook_claude() {
  if ! command -v jq &>/dev/null; then
    echo "  jq not found, skipping skill-journal-log hook"
    return
  fi

  local settings="$CLAUDE_DIR/settings.json"
  [ -f "$settings" ] || echo '{}' > "$settings"

  add_json_hook "$settings" "PostToolUse" "$SKILLS_DIR/hooks/skill-journal-log.sh" "Skill"
  echo "  ✓ skill-journal-log hook → ~/.claude/settings.json"
}

# Copilot CLI hooks are separate personal JSON files under ~/.copilot/hooks/
# (schema confirmed empirically: PreToolUse payload has tool_name/tool_input
# like Claude Code, but tool_name is "skill" lowercase, and there's no
# PostToolUse-success event — only PreToolUse and PostToolUseFailure — so
# this uses PreToolUse, same as the invocation-moment logging it already does
# on Claude Code. No matcher field exists in this schema; the script itself
# filters by tool_name (see hooks/skill-journal-log.sh).
setup_skill_journal_log_hook_copilot() {
  local hooks_dir="$HOME/.copilot/hooks"
  mkdir -p "$hooks_dir"
  cat > "$hooks_dir/skill-journal-log.json" <<EOF
{
  "version": 1,
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "bash": "$SKILLS_DIR/hooks/skill-journal-log.sh",
        "timeoutSec": 5
      }
    ]
  }
}
EOF
  echo "  ✓ skill-journal-log hook → ~/.copilot/hooks/skill-journal-log.json"
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
