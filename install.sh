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

  # qmd's own skill isn't part of this repo's skills/ dir — Copilot doesn't
  # read ~/.agents/skills like Claude/pi do, so mirror it in explicitly.
  if [ -d "$HOME/.agents/skills/qmd" ]; then
    cp -R "$HOME/.agents/skills/qmd" "$HOME/.copilot/skills/qmd"
    echo "  ✓ qmd skill → ~/.copilot/skills/qmd"
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
}

setup_pi() {
  echo "→ pi coding agent"

  command -v npx &>/dev/null || { echo "  npx not found, skipping ponytail"; return; }
  npx --yes skills add DietrichGebert/ponytail -a pi -g -y &>/dev/null \
    && echo "  ✓ ponytail (skills.sh)" \
    || echo "  ponytail install failed, run manually: npx skills add DietrichGebert/ponytail -a pi -g -y"
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

# ── qmd (local hybrid BM25/vector search over ~/wiki) ───────────────────────
# https://github.com/tobilu/qmd — CLI-only (no MCP). Installs the binary,
# its bundled agent-facing skill (this is what makes an agent discover qmd's
# CLI syntax at all — without it the skill file simply doesn't exist in any
# agent's skills dir), and indexes the personal wiki if ~/wiki exists.
# Every guard clause below returns 0 explicitly and every external call is
# tolerant of failure so a flaky/missing npm or qmd never aborts the rest of
# this script under `set -e`.

ensure_qmd_binary() {
  command -v qmd &>/dev/null && return 0
  if ! command -v npm &>/dev/null; then
    echo "  npm not found, skipping qmd"
    return 0
  fi
  echo "  installing qmd..."
  npm install -g @tobilu/qmd &>/dev/null \
    || echo "  qmd install failed, run manually: npm install -g @tobilu/qmd"
  return 0
}

ensure_qmd_skill() {
  command -v qmd &>/dev/null || return 0
  [ -d "$HOME/.agents/skills/qmd" ] && return 0
  if qmd skill install --global --yes &>/dev/null; then
    echo "  ✓ qmd skill → ~/.agents/skills/qmd (+ ~/.claude/skills/qmd)"
  else
    echo "  qmd skill install failed, run manually: qmd skill install --global --yes"
  fi
  return 0
}

# One qmd collection per top-level ~/wiki dir (qmd binds one root per name;
# a second `add` with the same name errors rather than merging), skipped if
# already added.
add_qmd_collection() {
  local name="$1" dir="$2" desc="$3"
  qmd collection show "$name" &>/dev/null && return 0
  qmd collection add "$dir" --name "$name" &>/dev/null \
    || { echo "  qmd collection add $name failed"; return 0; }
  qmd context add "qmd://$name" "$desc" &>/dev/null || true
  return 0
}

setup_qmd_collections() {
  [ -d "$HOME/wiki" ] || return 0
  command -v qmd &>/dev/null || return 0

  add_qmd_collection kb      "$HOME/wiki/kb"      "Synthesized, cross-referenced knowledge — check here first"
  add_qmd_collection journal "$HOME/wiki/journal" "Raw dated journal/research log — provenance, what happened when"
  add_qmd_collection roadmap "$HOME/wiki/roadmap" "Live EPIC/STORY/Task project plans"
  add_qmd_collection today   "$HOME/wiki/today"   "In-flight work not yet archived for the day"

  # qmd embed alone won't discover new/changed files — update finds them
  # (there's no per-collection -c filter on update, it's always all
  # collections), embed then vectorizes whatever update queued as pending.
  bash "$SKILLS_DIR/skills/kb-ingest/scripts/qmd_sync.sh"
  echo "  ✓ qmd collections (kb, journal, roadmap, today)"
  return 0
}

setup_qmd() {
  echo "→ qmd (local wiki search)"
  ensure_qmd_binary
  ensure_qmd_skill
  setup_qmd_collections
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
setup_qmd && echo ""
selected "claude"  && setup_claude  && echo ""
selected "copilot" && setup_copilot && echo ""
selected "pi"      && setup_pi      && echo ""
setup_agents_skills && echo ""
setup_bin && echo ""

echo "Done."
