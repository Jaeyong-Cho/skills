#!/usr/bin/env python3
"""Validate ways.json and generate the Markdown way documents."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from graph import render, validate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ways_json", type=Path)
    parser.add_argument("--output-root", type=Path, help="Markdown root; defaults to ways.json's directory")
    args = parser.parse_args()
    try:
        document = json.loads(args.ways_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"{args.ways_json}: {exc}", file=sys.stderr)
        return 1
    errors = validate(document)
    if errors:
        print("Refusing to generate Markdown; ways.json is invalid:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    output_root = args.output_root or args.ways_json.parent
    output_root.mkdir(parents=True, exist_ok=True)
    for goal_id in document["goals"]:
        goal_dir = output_root / document["nodes"][goal_id]["directory"]
        for relative_path, content in render(document, goal_id).items():
            destination = goal_dir / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
            print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
