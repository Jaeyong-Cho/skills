#!/usr/bin/env bash
set -euo pipefail

TITLE="${1:?Usage: init.sh <project-title>}"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DIR="docs"

echo "→ mdbook init"
mdbook init "$DIR" --title "$TITLE" --ignore none

echo "→ mdbook-mermaid install"
mdbook-mermaid install "$DIR"

echo "→ download catppuccin theme"
mkdir -p "$DIR/theme"
CATPPUCCIN_TAG=$(curl -fsSL https://api.github.com/repos/catppuccin/mdBook/releases/latest \
  | grep '"tag_name"' | head -1 | cut -d'"' -f4)
curl -fsSL "https://github.com/catppuccin/mdBook/releases/download/${CATPPUCCIN_TAG}/catppuccin.css" \
  -o "$DIR/theme/catppuccin.css"

echo "→ copy kanagawa theme"
cp "$SKILL_DIR/kanagawa.css" "$DIR/theme/kanagawa.css"

echo "→ copy serve.sh"
cp "$SKILL_DIR/serve.sh" "$DIR/serve.sh"

echo "→ download catppuccin index.hbs"
curl -fsSL "https://raw.githubusercontent.com/catppuccin/mdBook/main/example/theme/index.hbs" \
  -o "$DIR/theme/index.hbs"

echo "→ patch index.hbs: add kanagawa button"
python3 - "$DIR/theme/index.hbs" <<'PYEOF'
import sys
path = sys.argv[1]
text = open(path).read()
old = '<li role="none"><button role="menuitem" class="theme" id="mocha">Mocha</button></li>'
new = old + '\n                            <li role="none"><button role="menuitem" class="theme" id="kanagawa">Kanagawa</button></li>'
open(path, 'w').write(text.replace(old, new, 1))
PYEOF

echo "→ update book.toml"
python3 - "$DIR/book.toml" <<'PYEOF'
import sys
path = sys.argv[1]
text = open(path).read()
css = 'additional-css = ["theme/catppuccin.css", "theme/kanagawa.css"]\ndefault-theme = "kanagawa"\npreferred-dark-theme = "kanagawa"\n'
if '[output.html]' in text:
    text = text.replace('[output.html]\n', '[output.html]\n' + css)
else:
    text += '\n[output.html]\n' + css
open(path, 'w').write(text)
PYEOF

echo "→ remove chapter_1.md"
rm -f "$DIR/src/chapter_1.md"
python3 - "$DIR/src/SUMMARY.md" <<'PYEOF'
import sys
path = sys.argv[1]
lines = [l for l in open(path) if 'chapter_1.md' not in l]
open(path, 'w').writelines(lines)
PYEOF

echo "✓ done — cd docs && ./serve.sh"
