#!/usr/bin/env bash
set -euo pipefail

TITLE="${1:?Usage: init.sh <project-title>}"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "→ mdbook init"
mdbook init "$TITLE" --title "$TITLE" --ignore none

echo "→ mdbook-mermaid install"
mdbook-mermaid install "$TITLE"

echo "→ download catppuccin theme"
CATPPUCCIN_TAG=$(curl -fsSL https://api.github.com/repos/catppuccin/mdBook/releases/latest \
  | grep '"tag_name"' | head -1 | cut -d'"' -f4)
curl -fsSL "https://github.com/catppuccin/mdBook/releases/download/${CATPPUCCIN_TAG}/catppuccin.css" \
  -o "$TITLE/theme/catppuccin.css"

echo "→ copy kanagawa theme"
cp "$SKILL_DIR/kanagawa.css" "$TITLE/theme/kanagawa.css"

echo "→ download catppuccin index.hbs"
curl -fsSL "https://raw.githubusercontent.com/catppuccin/mdBook/main/example/theme/index.hbs" \
  -o "$TITLE/theme/index.hbs"

echo "→ patch index.hbs: add kanagawa button"
python3 - "$TITLE/theme/index.hbs" <<'PYEOF'
import sys
path = sys.argv[1]
text = open(path).read()
old = '<li role="none"><button role="menuitem" class="theme" id="mocha">Mocha</button></li>'
new = old + '\n                            <li role="none"><button role="menuitem" class="theme" id="kanagawa">Kanagawa</button></li>'
open(path, 'w').write(text.replace(old, new, 1))
PYEOF

echo "→ update book.toml"
cat >> "$TITLE/book.toml" << 'TOML'

[output.html]
additional-css = ["theme/catppuccin.css", "theme/kanagawa.css"]
default-theme = "kanagawa"
preferred-dark-theme = "kanagawa"
TOML

echo "✓ done — cd $TITLE && mdbook serve"
