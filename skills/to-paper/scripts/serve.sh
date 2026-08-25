#!/bin/bash
# Serves the current directory (a to-paper output dir) over HTTP so
# index.html's relative assets/*.svg paths resolve. Run from inside that
# directory: ./serve.sh [port], then open http://localhost:<port>.

python3 -m http.server "${1:-4802}"
