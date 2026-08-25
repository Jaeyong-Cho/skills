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
import shutil
import stat
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "template.html"
SERVE_SCRIPT = SKILL_DIR / "scripts" / "serve.sh"

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


def render_section(number, key, value, diagrams_by_target):
    heading = title_case(key)
    parts = [f"<h2>{number}. {html.escape(heading)}</h2>"]
    if isinstance(value, str):
        parts.append(paragraphs_html(value))
    elif isinstance(value, dict):
        for sub_index, (sub_key, sub_value) in enumerate(value.items(), start=1):
            sub_number = f"{number}-{sub_index}"
            if isinstance(sub_value, dict):
                sub_title = sub_value.get("title", "")
                sub_text = sub_value.get("text", "")
                if sub_title:
                    parts.append(f"<h3>{sub_number}. {html.escape(sub_title)}</h3>")
                parts.append(paragraphs_html(sub_text))
            else:
                parts.append(paragraphs_html(sub_value))
            for diagram in diagrams_by_target.get(f"{key}.{sub_key}", []):
                parts.append(figure_html(diagram))
    else:
        raise ValueError(f"section {key!r} must be a string or an object, got {type(value)}")
    # Figures targeting the section as a whole (no subsection named) always
    # land at the end, after every subsection's own figures.
    for diagram in diagrams_by_target.get(key, []):
        parts.append(figure_html(diagram))
    return "\n".join(parts)


def valid_diagram_targets(manifest):
    """Every string a diagram's "section" field can name: each top-level
    section key, plus "{key}.{sub_key}" for each subsection of a section
    given as an object — sub-title granularity, per MANIFEST-FORMAT.md."""
    targets = set(SECTION_ORDER)
    for key in SECTION_ORDER:
        value = manifest.get(key)
        if isinstance(value, dict):
            targets.update(f"{key}.{sub_key}" for sub_key in value)
    return targets


def build(manifest):
    missing = [k for k in REQUIRED_KEYS if k not in manifest]
    if missing:
        raise ValueError(f"manifest missing required key(s): {', '.join(missing)}")

    targets = valid_diagram_targets(manifest)
    diagrams_by_target = {}
    appendix = []
    for diagram in manifest["diagrams"]:
        section = diagram.get("section")
        if section in targets:
            diagrams_by_target.setdefault(section, []).append(diagram)
        else:
            appendix.append(diagram)

    body_parts = []
    for number, key in enumerate(SECTION_ORDER, start=1):
        body_parts.append(render_section(number, key, manifest[key], diagrams_by_target))

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


def write_output(manifest_dir, html_output):
    """Write index.html and copy in an executable serve.sh, both as
    siblings of manifest.json. Returns (index_path, serve_path)."""
    out_path = manifest_dir / "index.html"
    out_path.write_text(html_output, encoding="utf-8")

    serve_path = manifest_dir / "serve.sh"
    shutil.copyfile(SERVE_SCRIPT, serve_path)
    serve_path.chmod(serve_path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return out_path, serve_path


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
    out_path, serve_path = write_output(manifest_path.parent, output)
    print(f"OK: wrote {out_path} and {serve_path}")
    sys.exit(0)


def self_test():
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
                {"id": "fig3", "file": "assets/fig3.svg", "caption": "Cap 3", "section": "background.bg2"},
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
        # fig3 targets background.bg2 (sub-title granularity): it must sit
        # right after that subsection's own heading/text, not after bg1's.
        prior_work_pos = html_out.index("<h3>2-2. Prior Work</h3>")
        bg1_pos = html_out.index("Plain subsection text.")
        fig3_pos = html_out.index("assets/fig3.svg")
        assert bg1_pos < prior_work_pos < fig3_pos, "fig3 should land after bg2's own content, not before it"
        methodology_pos = html_out.index("<h2>3. Methodology</h2>")
        assert fig3_pos < methodology_pos, "fig3 should still be inside Background, before Methodology starts"

        bad_manifest = dict(manifest)
        del bad_manifest["conclusion"]
        try:
            build(bad_manifest)
            raise AssertionError("should have raised on missing key")
        except ValueError:
            pass

        index_path, serve_path = write_output(tmp, html_out)
        assert index_path.is_file() and index_path.read_text(encoding="utf-8") == html_out
        assert serve_path.is_file(), "serve.sh should be copied alongside index.html"
        assert serve_path.stat().st_mode & stat.S_IXUSR, "serve.sh should be executable"
        assert serve_path.read_text(encoding="utf-8") == SERVE_SCRIPT.read_text(encoding="utf-8")

        print("self-test passed")
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--test":
        self_test()
    else:
        main()
