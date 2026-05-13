#!/bin/bash
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)/.aeo"
mdbook serve -n 0.0.0.0 -p 4800
