#!/usr/bin/env python3
"""Lint a canonical ways.json file."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from graph import validate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ways_json", type=Path)
    args = parser.parse_args()
    try:
        document = json.loads(args.ways_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"{args.ways_json}: {exc}", file=sys.stderr)
        return 1
    errors = validate(document)
    if errors:
        for error in errors:
            print(f"{args.ways_json}: {error}", file=sys.stderr)
        return 1
    print(f"{args.ways_json}: valid ({len(document['nodes'])} nodes, {len(document['edges']['depends_on'])} dependencies)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
