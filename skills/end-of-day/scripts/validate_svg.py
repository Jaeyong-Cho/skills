#!/usr/bin/env python3
"""
Validate that SVG file(s) are well-formed XML.

Catches the failure mode where a browser silently renders nothing (or an
error banner) because the SVG isn't valid XML — most commonly an unescaped
`&` in a CSS @import/url() or comparison operator inside a <style> block,
or a stray unescaped `<`/`>`. Python's XML parser rejects the same things a
browser's XML parser would, so a pass here means the file will at least
parse — it does not check visual layout, overflow, or color contrast.

Usage:
  python validate_svg.py file1.svg [file2.svg ...]

Exit code 0 if every file is well-formed and root tag is <svg>, 1 otherwise.
"""
import sys
import xml.etree.ElementTree as ET


def validate_svg_wellformed(path):
    """Raise ValueError with a human-readable message if `path` isn't a
    well-formed SVG. Returns silently on success."""
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        raise ValueError(f"not well-formed XML: {e}") from e
    root = tree.getroot()
    tag = root.tag.rsplit("}", 1)[-1]  # strip namespace
    if tag != "svg":
        raise ValueError(f"root element is <{tag}>, expected <svg>")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    failed = False
    for path in sys.argv[1:]:
        try:
            validate_svg_wellformed(path)
        except ValueError as e:
            print(f"{path}: FAIL — {e}")
            failed = True
        except OSError as e:
            print(f"{path}: FAIL — {e}")
            failed = True
        else:
            print(f"{path}: OK")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
