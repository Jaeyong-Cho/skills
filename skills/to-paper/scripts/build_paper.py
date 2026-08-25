#!/usr/bin/env python3
"""
Build index.html from a to-paper manifest.json.

Numbering is derived, never read from the manifest: Introduction=1,
Background=2, Methodology=3, Results=4, Conclusion=5; a section given as an
object of subsections gets them numbered N-1, N-2... in key order. Every
section/subsection's prose is a JSON array of paragraph strings, one <p>
per element. See ../MANIFEST-FORMAT.md for the manifest schema.

Usage:
  python build_paper.py <manifest.json>

Writes index.html as a sibling of manifest.json. Exit code 0 on success,
1 if the manifest is missing a required key.
"""
import html
import json
import re
import shutil
import stat
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "template.html"
SERVE_SCRIPT = SKILL_DIR / "scripts" / "serve.sh"

SECTION_ORDER = ["introduction", "background", "methodology", "results", "conclusion"]
REQUIRED_KEYS = ["title", "abstract", *SECTION_ORDER, "diagrams"]
FIG_REF_RE = re.compile(r"\{\{fig:([\w-]+)\}\}")
SVG_BLOCK_RE = re.compile(r"<svg\b.*?</svg>", re.DOTALL)


def extract_svg_markup(path):
    """Pull the first <svg>...</svg> block out of `path` — a bare .svg file
    or a full diagram-design .diagram.html draft, either works identically,
    since a paper inlines the markup directly rather than pointing an <img>
    at a separately exported file. Skips export.md's standalone-file-only
    steps entirely (XML declaration, escaped Google Fonts @import) — those
    exist to make a .svg render correctly on its own outside any HTML page,
    which doesn't apply here: the markup lands inside index.html, which
    already has its own <head> and fonts."""
    text = path.read_text(encoding="utf-8")
    match = SVG_BLOCK_RE.search(text)
    if not match:
        raise ValueError(f"no <svg>...</svg> found in {path}")
    return match.group(0)


def render_fig_refs(escaped_text, figure_numbers):
    """Replace {{fig:some-id}} — already HTML-escaped, so the braces/colon
    survive untouched — with a link to that figure's number, e.g. Fig 3."""
    def repl(match):
        fig_id = match.group(1)
        number = figure_numbers.get(fig_id)
        if number is None:
            return f"[unknown fig: {html.escape(fig_id)}]"
        return f'<a href="#fig-{html.escape(fig_id)}">Fig {number}</a>'
    return FIG_REF_RE.sub(repl, escaped_text)


def paragraphs_html(paragraphs, figure_numbers):
    """paragraphs is a list of paragraph strings — a manifest section or
    subsection's text field. One <p> per element, in order."""
    return "\n".join(f"<p>{render_fig_refs(html.escape(p), figure_numbers)}</p>" for p in paragraphs)


def table_html(rows):
    header, *body = rows
    thead = "<tr>" + "".join(f"<th>{html.escape(str(c))}</th>" for c in header) + "</tr>"
    tbody = "\n".join(
        "<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>" for row in body
    )
    return f"<table><thead>{thead}</thead><tbody>{tbody}</tbody></table>"


def figure_html(diagram, figure_numbers, manifest_dir):
    number = figure_numbers[diagram["id"]]
    anchor = html.escape(diagram["id"])
    caption = html.escape(diagram.get("caption", ""))
    figcaption = f"<figcaption><strong>Fig {number}.</strong> {caption}</figcaption>"
    if diagram.get("type") == "table":
        return f'<figure class="table-figure" id="fig-{anchor}">{table_html(diagram["rows"])}{figcaption}</figure>'
    svg_markup = extract_svg_markup(manifest_dir / diagram["file"])
    return f'<figure id="fig-{anchor}">{svg_markup}{figcaption}</figure>'


def title_case(slug):
    return slug.replace("-", " ").replace("_", " ").title()


def render_section(number, key, value, diagrams_by_target, figure_numbers, manifest_dir):
    heading = title_case(key)
    parts = [f"<h2>{number}. {html.escape(heading)}</h2>"]
    if isinstance(value, list):
        parts.append(paragraphs_html(value, figure_numbers))
    elif isinstance(value, dict):
        for sub_index, (sub_key, sub_value) in enumerate(value.items(), start=1):
            sub_number = f"{number}-{sub_index}"
            if isinstance(sub_value, dict):
                sub_title = sub_value.get("title", "")
                sub_text = sub_value.get("text", [])
                if sub_title:
                    parts.append(f"<h3>{sub_number}. {html.escape(sub_title)}</h3>")
                parts.append(paragraphs_html(sub_text, figure_numbers))
            else:
                parts.append(paragraphs_html(sub_value, figure_numbers))
            for diagram in diagrams_by_target.get(f"{key}.{sub_key}", []):
                parts.append(figure_html(diagram, figure_numbers, manifest_dir))
    else:
        raise ValueError(f"section {key!r} must be a list of paragraphs or an object, got {type(value)}")
    # Figures targeting the section as a whole (no subsection named) always
    # land at the end, after every subsection's own figures.
    for diagram in diagrams_by_target.get(key, []):
        parts.append(figure_html(diagram, figure_numbers, manifest_dir))
    return "\n".join(parts)


def ordered_diagrams(manifest, diagrams_by_target, appendix):
    """Every diagram in the exact order render_section + the appendix loop
    will place it — figure numbers follow this reading order, not the
    diagrams array's order."""
    ordered = []
    for key in SECTION_ORDER:
        value = manifest[key]
        if isinstance(value, dict):
            for sub_key in value:
                ordered.extend(diagrams_by_target.get(f"{key}.{sub_key}", []))
        ordered.extend(diagrams_by_target.get(key, []))
    ordered.extend(appendix)
    return ordered


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


def build(manifest, manifest_dir):
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

    figure_numbers = {
        d["id"]: i + 1
        for i, d in enumerate(ordered_diagrams(manifest, diagrams_by_target, appendix))
    }

    body_parts = []
    for number, key in enumerate(SECTION_ORDER, start=1):
        body_parts.append(render_section(number, key, manifest[key], diagrams_by_target, figure_numbers, manifest_dir))

    if appendix:
        body_parts.append("<h2>Appendix: Figures</h2>")
        for diagram in appendix:
            body_parts.append(figure_html(diagram, figure_numbers, manifest_dir))

    template = TEMPLATE.read_text(encoding="utf-8")
    return (
        template
        .replace("{{TITLE}}", html.escape(manifest["title"]))
        .replace("{{ABSTRACT}}", render_fig_refs(html.escape(manifest["abstract"][0]), figure_numbers))
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
        output = build(manifest, manifest_path.parent)
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
        assets = tmp / "assets"
        assets.mkdir()
        # fig1: a bare .svg file (the export.md-produced shape).
        (assets / "fig1.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" width="200" height="100" '
            'role="img" aria-labelledby="fig1-t fig1-d">'
            '<title id="fig1-t">FIG1-MARKER</title><desc id="fig1-d">d</desc></svg>'
        )
        # fig2: a full diagram-design .diagram.html draft, proving extraction
        # works identically on the raw draft, not just an exported .svg —
        # the whole point of skipping the export step.
        (assets / "fig2.diagram.html").write_text(
            "<!DOCTYPE html><html><head><title>x</title></head><body>"
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" width="200" height="100" '
            'role="img" aria-labelledby="fig2-t fig2-d">'
            '<title id="fig2-t">FIG2-MARKER</title><desc id="fig2-d">d</desc></svg>'
            "</body></html>"
        )
        (assets / "fig3.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" width="200" height="100" '
            'role="img" aria-labelledby="fig3-t fig3-d">'
            '<title id="fig3-t">FIG3-MARKER</title><desc id="fig3-d">d</desc></svg>'
        )

        manifest = {
            "title": "A Small Study",
            "abstract": ["This is the abstract paragraph."],
            "introduction": ["First para, see {{fig:fig1}} and {{fig:nope}}.", "Second para."],
            "background": {
                "bg1": ["Plain subsection text."],
                "bg2": {"title": "Prior Work", "text": ["Some prior work text."]},
            },
            "methodology": ["One methodology paragraph."],
            "results": ["Some results."],
            "conclusion": ["We conclude."],
            "diagrams": [
                {"id": "fig1", "file": "assets/fig1.svg", "caption": "Cap 1", "section": "methodology"},
                {"id": "fig2", "file": "assets/fig2.diagram.html", "caption": "Cap 2", "section": "nowhere"},
                {"id": "fig3", "file": "assets/fig3.svg", "caption": "Cap 3", "section": "background.bg2"},
                {
                    "id": "tbl1",
                    "type": "table",
                    "rows": [["Metric", "Before", "After"], ["Latency", "85ms", "20ms"]],
                    "caption": "Cap 4",
                    "section": "results",
                },
            ],
        }
        html_out = build(manifest, tmp)
        assert "<h1>A Small Study</h1>" in html_out
        assert "<h2>1. Introduction</h2>" in html_out
        assert "<h2>2. Background</h2>" in html_out
        assert "<h3>2-2. Prior Work</h3>" in html_out
        assert "<h2>3. Methodology</h2>" in html_out
        assert "FIG1-MARKER" in html_out
        assert "<h2>Appendix: Figures</h2>" in html_out
        # fig2 came from a full .diagram.html draft, not a bare .svg — its
        # <svg> markup still got extracted and inlined correctly.
        assert "FIG2-MARKER" in html_out
        assert html_out.count("<body") == 1, "only the <svg> block should be inlined, not the whole draft page"
        assert "<title>x</title>" not in html_out, "the draft's own <title> must not leak into the paper"
        # fig3 targets background.bg2 (sub-title granularity): it must sit
        # right after that subsection's own heading/text, not after bg1's.
        prior_work_pos = html_out.index("<h3>2-2. Prior Work</h3>")
        bg1_pos = html_out.index("Plain subsection text.")
        fig3_pos = html_out.index("FIG3-MARKER")
        assert bg1_pos < prior_work_pos < fig3_pos, "fig3 should land after bg2's own content, not before it"
        methodology_pos = html_out.index("<h2>3. Methodology</h2>")
        assert fig3_pos < methodology_pos, "fig3 should still be inside Background, before Methodology starts"

        # A "table" diagram renders as a <table>, not an <img>/<svg>, but is
        # still a numbered, captioned <figure>.
        assert '<figure class="table-figure" id="fig-tbl1">' in html_out
        assert "<th>Metric</th><th>Before</th><th>After</th>" in html_out
        assert "<td>Latency</td><td>85ms</td><td>20ms</td>" in html_out

        # Figure numbers follow reading order (fig3 appears first in the
        # document, inside Background), not the diagrams array's order.
        assert "<figure id=\"fig-fig3\">" in html_out
        assert "<strong>Fig 1.</strong> Cap 3" in html_out
        assert "<figure id=\"fig-fig1\">" in html_out
        assert "<strong>Fig 2.</strong> Cap 1" in html_out
        assert "<strong>Fig 3.</strong> Cap 4" in html_out  # tbl1, in Results
        assert "<strong>Fig 4.</strong> Cap 2" in html_out  # fig2, appendix, is last
        # {{fig:fig1}} in the introduction resolves to a link with fig1's
        # actual number (2); an unknown id degrades visibly, doesn't crash.
        assert '<a href="#fig-fig1">Fig 2</a>' in html_out
        assert "[unknown fig: nope]" in html_out

        bad_manifest = dict(manifest)
        del bad_manifest["conclusion"]
        try:
            build(bad_manifest, tmp)
            raise AssertionError("should have raised on missing key")
        except ValueError:
            pass

        missing_svg_manifest = dict(manifest)
        missing_svg_manifest["diagrams"] = [dict(manifest["diagrams"][0], file="assets/does-not-exist.svg")]
        try:
            build(missing_svg_manifest, tmp)
            raise AssertionError("should have raised on a diagram file with no <svg> block")
        except (ValueError, OSError):
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
