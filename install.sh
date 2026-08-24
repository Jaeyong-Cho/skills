#!/usr/bin/env bash
set -e

SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
CLAUDE_MD="$SKILLS_DIR/CLAUDE.md"
CLAUDE_SKILLS_DIR="$CLAUDE_DIR/skills"

# overwrite (default): copy over existing files, leave stale/renamed skills
#   and manually-added skills alone.
# clean (--clean): also remove skills this repo installed previously but no
#   longer ships (renamed/deleted), tracked via the install manifest.
MODE="overwrite"
for arg in "$@"; do
  case "$arg" in
    --clean) MODE="clean" ;;
    --overwrite) MODE="overwrite" ;;
  esac
done

echo "=== Skills Install ($MODE) ==="
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
detect "pi"      "pi coding agent    (pi CLI)"     "command -v pi"

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
  local dest="$1"
  local source_root destination_root dir manifest name

  mkdir -p "$dest"
  source_root="$(cd "$SKILLS_DIR" && pwd -P)"
  destination_root="$(cd "$dest" && pwd -P)"

  if [ "$source_root" = "$destination_root" ]; then
    echo "  ✓ skill library already at $dest"
    return
  fi

  # clean: clear what a previous run of this script installed so
  # renamed/removed skills (e.g. socratic → deleted, viz-gallery → renamed
  # viewpoints) don't linger. Tracked via a manifest since "skills" flattens
  # directly under $dest alongside anything else that may live there.
  # overwrite (default): skip this, cp -R below merges in place and leaves
  # stale/renamed and manually-added skills untouched.
  manifest="$dest/.installed-by-skills-repo"
  if [ "$MODE" = "clean" ]; then
    if [ -f "$manifest" ]; then
      while IFS= read -r name; do
        [ -n "$name" ] && rm -rf "${dest:?}/$name"
      done < "$manifest"
    fi
    for dir in references template; do
      rm -rf "${dest:?}/$dir"
    done
  fi

  # "skills" is special: its contents must land directly under $dest (e.g.
  # $dest/archi), not nested one level deeper as $dest/skills/archi — Claude
  # Code and the agentskills.io standard only discover skills at
  # $dest/<name>/SKILL.md.
  if [ -d "$SKILLS_DIR/skills" ]; then
    cp -R "$SKILLS_DIR/skills/." "$dest/"
    (cd "$SKILLS_DIR/skills" && ls -1) > "$manifest"
  fi

  for dir in references template; do
    [ -d "$SKILLS_DIR/$dir" ] || continue
    cp -R "$SKILLS_DIR/$dir" "$dest/"
  done
  echo "  ✓ skill library → $dest (skills, references, template)"
}

setup_claude() {
  echo "→ Claude Code"

  install_skill_library "$CLAUDE_SKILLS_DIR"

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
    install_agent_plugin claude DietrichGebert/ponytail ponytail@ponytail "ponytail plugin"
  fi

  setup_boy_scout claude
}

setup_copilot() {
  echo "→ GitHub Copilot CLI"

  mkdir -p "$HOME/.copilot"
  ln -sf "$SKILLS_DIR/copilot-instructions.md" "$HOME/.copilot/copilot-instructions.md"
  echo "  ✓ ~/.copilot/copilot-instructions.md → $SKILLS_DIR/copilot-instructions.md"

  # Install skills and references for Copilot CLI, if the user has a ~/.copilot/skills directory.
  if [ -d "$HOME/.copilot" ]; then
      if [ "$MODE" = "clean" ]; then
        rm -rf "$HOME/.copilot/skills" "$HOME/.copilot/references"
      fi
      cp -R "$SKILLS_DIR/skills/." "$HOME/.copilot/skills"
      cp -R "$SKILLS_DIR/references/." "$HOME/.copilot/skills/references"
      cp -R "$SKILLS_DIR/template/." "$HOME/.copilot/skills/template"
      echo "  ✓ skills, references, and template → ~/.copilot"
  fi

  # tmux-agent-status itself has no Copilot CLI integration (process presence
  # auto-detection only).
  echo "  note: tmux-agent-status has no Copilot CLI support (process presence only)"

  ensure_rtk_binary
  if command -v rtk &>/dev/null; then
    rtk init -g --copilot --auto-patch &>/dev/null \
      && echo "  ✓ rtk hooks (rtk init -g --copilot)" \
      || echo "  rtk init failed, run manually: rtk init -g --copilot"
  fi

  if command -v copilot &>/dev/null; then
    install_agent_plugin copilot DietrichGebert/ponytail ponytail@ponytail "ponytail plugin"
  fi

  setup_boy_scout copilot
}

setup_pi() {
  echo "→ pi coding agent"

  if command -v npx &>/dev/null; then
    npx --yes skills add DietrichGebert/ponytail -a pi -g -y &>/dev/null \
      && echo "  ✓ ponytail (skills.sh)" \
      || echo "  ponytail install failed, run manually: npx skills add DietrichGebert/ponytail -a pi -g -y"
  else
    echo "  npx not found, skipping ponytail"
  fi

  command -v pi &>/dev/null || return
  local pkg
  for pkg in \
    "https://github.com/nicobailon/pi-powerline-footer" \
    "https://github.com/MasuRii/pi-tool-display" \
    "npm:@narumitw/pi-usage" \
    "npm:pi-must-have-extension"
  do
    if pi install "$pkg" &>/dev/null; then
      echo "  ✓ $pkg"
    else
      echo "  $pkg install failed, run manually: pi install $pkg"
    fi
  done

  setup_boy_scout pi
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

# ── boy-scout binary ─────────────────────────────────────────────────────────
# https://github.com/Jaeyong-Cho/boy-scout — private repo, no release binary
# yet, so build from source via its Makefile (installs to ~/.agents/bin).

ensure_boy_scout_binary() {
  command -v boy-scout &>/dev/null && return
  [ -x "$HOME/.agents/bin/boy-scout" ] && return

  command -v go &>/dev/null || { echo "  go not found, skipping boy-scout"; return; }

  echo "  installing boy-scout..."
  local tmp
  tmp="$(mktemp -d)"
  if git clone --depth 1 https://github.com/Jaeyong-Cho/boy-scout.git "$tmp" &>/dev/null \
    && make -C "$tmp" install &>/dev/null; then
    echo "  ✓ boy-scout → ~/.agents/bin/boy-scout"
  else
    echo "  boy-scout install failed, run manually: git clone git@github.com:Jaeyong-Cho/boy-scout.git && cd boy-scout && make install"
  fi
  rm -rf "$tmp"
}

# setup_boy_scout runs `boy-scout setup --global <target>` (target one of
# claude/copilot/pi/agents, matching boy-scout's own setup targets).
setup_boy_scout() {
  local target="$1" bin
  ensure_boy_scout_binary
  if command -v boy-scout &>/dev/null; then
    bin="boy-scout"
  elif [ -x "$HOME/.agents/bin/boy-scout" ]; then
    bin="$HOME/.agents/bin/boy-scout"
  else
    return
  fi
  "$bin" setup --global "$target" &>/dev/null \
    && echo "  ✓ boy-scout setup --global $target" \
    || echo "  boy-scout setup failed, run manually: boy-scout setup --global $target"
}

# ── JSON hook wiring (shared) ────────────────────────────────────────────────
# add_json_hook merges one hook command into settings.json without clobbering
# existing hooks/settings, and is idempotent (skips if the command is already
# registered for that event). Used below by tmux-agent-status. matcher is
# optional — omit it to fire on every event of that type (tmux-agent-status
# wants that); pass a tool name (e.g. "Skill") to scope a
# PostToolUse/PreToolUse hook to just that tool.

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

# ── Agent Skills standard (~/.agents/skills) ────────────────────────────────
# https://agentskills.io/specification — global skills dir read by pi and
# other harnesses that follow the standard, independent of Claude/Copilot.

setup_agents_skills() {
  echo "→ Agent Skills standard (~/.agents/skills)"
  install_skill_library "$HOME/.agents/skills"
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
selected "pi"      && setup_pi      && echo ""
setup_agents_skills && echo ""
setup_bin && echo ""

echo "Done."
