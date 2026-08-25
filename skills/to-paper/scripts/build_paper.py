#!/usr/bin/env python3
"""
Build index.html from a to-paper manifest.json.

Numbering is derived, never read from the manifest: Introduction=1,
Background=2, Methodology=3, Results=4, Conclusion=5; a section given as an
object of subsections gets them numbered N-1, N-2... in key order. See
../MANIFEST-FORMAT.md for the manifest schema.

Usage:
  python build_paper.py <manifest.json>

Writes index.html as a sibling of manifest.json. Exit code 0 on success,
1 if the manifest is missing a required key.
"""
import html
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "template.html"

SECTION_ORDER = ["introduction", "background", "methodology", "results", "conclusion"]
REQUIRED_KEYS = ["title", "abstract", *SECTION_ORDER, "diagrams"]


def paragraphs_html(text):
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "\n".join(f"<p>{html.escape(p)}</p>" for p in parts)


def figure_html(diagram):
    src = html.escape(diagram["file"])
    caption = html.escape(diagram.get("caption", ""))
    return (
        f'<figure><img src="{src}" alt="{caption}">'
        f"<figcaption>{caption}</figcaption></figure>"
    )


def title_case(slug):
    return slug.replace("-", " ").replace("_", " ").title()


def render_section(number, key, value, diagrams_by_section):
    heading = title_case(key)
    parts = [f"<h2>{number}. {html.escape(heading)}</h2>"]
    if isinstance(value, str):
        parts.append(paragraphs_html(value))
    elif isinstance(value, dict):
        for sub_index, (_sub_key, sub_value) in enumerate(value.items(), start=1):
            sub_number = f"{number}-{sub_index}"
            if isinstance(sub_value, dict):
                sub_title = sub_value.get("title", "")
                sub_text = sub_value.get("text", "")
                if sub_title:
                    parts.append(f"<h3>{sub_number}. {html.escape(sub_title)}</h3>")
                parts.append(paragraphs_html(sub_text))
            else:
                parts.append(paragraphs_html(sub_value))
    else:
        raise ValueError(f"section {key!r} must be a string or an object, got {type(value)}")
    for diagram in diagrams_by_section.get(key, []):
        parts.append(figure_html(diagram))
    return "\n".join(parts)


def build(manifest):
    missing = [k for k in REQUIRED_KEYS if k not in manifest]
    if missing:
        raise ValueError(f"manifest missing required key(s): {', '.join(missing)}")

    diagrams_by_section = {}
    appendix = []
    for diagram in manifest["diagrams"]:
        section = diagram.get("section")
        if section in SECTION_ORDER:
            diagrams_by_section.setdefault(section, []).append(diagram)
        else:
            appendix.append(diagram)

    body_parts = []
    for number, key in enumerate(SECTION_ORDER, start=1):
        body_parts.append(render_section(number, key, manifest[key], diagrams_by_section))

    if appendix:
        body_parts.append("<h2>Appendix: Figures</h2>")
        for diagram in appendix:
            body_parts.append(figure_html(diagram))

    template = TEMPLATE.read_text(encoding="utf-8")
    return (
        template
        .replace("{{TITLE}}", html.escape(manifest["title"]))
        .replace("{{ABSTRACT}}", html.escape(manifest["abstract"]))
        .replace("{{BODY}}", "\n".join(body_parts))
    )


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    manifest_path = Path(sys.argv[1])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    try:
        output = build(manifest)
    except ValueError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
    out_path = manifest_path.parent / "index.html"
    out_path.write_text(output, encoding="utf-8")
    print(f"OK: wrote {out_path}")
    sys.exit(0)


def self_test():
    import shutil
    import tempfile

    tmp = Path(tempfile.mkdtemp())
    try:
        manifest = {
            "title": "A Small Study",
            "abstract": "This is the abstract paragraph.",
            "introduction": "First para.\n\nSecond para.",
            "background": {
                "bg1": "Plain subsection text.",
                "bg2": {"title": "Prior Work", "text": "Some prior work text."},
            },
            "methodology": "One methodology paragraph.",
            "results": "Some results.",
            "conclusion": "We conclude.",
            "diagrams": [
                {"id": "fig1", "file": "assets/fig1.svg", "caption": "Cap 1", "section": "methodology"},
                {"id": "fig2", "file": "assets/fig2.svg", "caption": "Cap 2", "section": "nowhere"},
            ],
        }
        html_out = build(manifest)
        assert "<h1>A Small Study</h1>" in html_out
        assert "<h2>1. Introduction</h2>" in html_out
        assert "<h2>2. Background</h2>" in html_out
        assert "<h3>2-2. Prior Work</h3>" in html_out
        assert "<h2>3. Methodology</h2>" in html_out
        assert "assets/fig1.svg" in html_out
        assert "<h2>Appendix: Figures</h2>" in html_out
        assert "assets/fig2.svg" in html_out

        bad_manifest = dict(manifest)
        del bad_manifest["conclusion"]
        try:
            build(bad_manifest)
            raise AssertionError("should have raised on missing key")
        except ValueError:
            pass

        print("self-test passed")
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--test":
        self_test()
    else:
        main()
