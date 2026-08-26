#!/usr/bin/env python3
"""
Build index.html from a to-paper manifest.json.

Numbering is derived, never read from the manifest: Introduction=1,
Background=2, Methodology=3, Results=4, Discussion=5, Conclusion=6; a
section given as an object of subsections gets them numbered N-1, N-2... in
key order. Every section/subsection's prose is a JSON array of paragraph
strings, one <p> per element (or one <ul> if an element is itself a list of
item strings — a bullet list). A diagram's "section" field can target a
whole section/subsection, or "{target}@{N}" for that target's Nth paragraph
specifically, placing the figure right after just that one paragraph
instead of at the end of the whole section/subsection. A table ("type":
"table") is not a figure: it's numbered as its own "Table N" sequence,
separate from "Fig N", cited with {{tbl:some-id}} instead of {{fig:...}}.
An optional trailing "appendix" key, same shape as any section, renders
as an unnumbered "Appendix" heading after Conclusion — for raw
output/stats too detailed for the word/sentence-limited prose sections;
lint_paper.py skips its prose-quality checks entirely. See
../MANIFEST-FORMAT.md for the manifest schema.

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

SECTION_ORDER = ["introduction", "background", "methodology", "results", "discussion", "conclusion"]
REQUIRED_KEYS = ["title", "abstract", *SECTION_ORDER, "diagrams"]
FIG_REF_RE = re.compile(r"\{\{(fig|tbl):([\w-]+)\}\}")
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


def render_fig_refs(escaped_text, figure_numbers, table_numbers):
    """Replace {{fig:some-id}} / {{tbl:some-id}} — already HTML-escaped, so
    the braces/colon survive untouched — with a link to that figure's or
    table's number, e.g. Fig 3 / Table 2. Tables get their own numbering
    sequence and prefix, separate from figures — a table is not a figure."""
    def repl(match):
        kind, ref_id = match.group(1), match.group(2)
        numbers, label, prefix = (
            (figure_numbers, "Fig", "fig") if kind == "fig" else (table_numbers, "Table", "tbl")
        )
        number = numbers.get(ref_id)
        if number is None:
            return f"[unknown {kind}: {html.escape(ref_id)}]"
        return f'<a href="#{prefix}-{html.escape(ref_id)}">{label} {number}</a>'
    return FIG_REF_RE.sub(repl, escaped_text)


def paragraph_html(p, figure_numbers, table_numbers):
    """One paragraph-array element -> one <p>, or one <ul> if the element
    is itself a list of item strings (a bullet list)."""
    if isinstance(p, list):
        items = "".join(
            f"<li>{render_fig_refs(html.escape(item), figure_numbers, table_numbers)}</li>" for item in p
        )
        return f"<ul>{items}</ul>"
    return f"<p>{render_fig_refs(html.escape(p), figure_numbers, table_numbers)}</p>"


def render_paragraphs_with_diagrams(paragraphs, target, diagrams_by_target, figure_numbers, table_numbers, manifest_dir):
    """paragraphs is a list of paragraph strings/bullet-list arrays — a
    manifest section or subsection's text field. One <p>/<ul> per element,
    in order, with any diagram targeting "{target}@{N}" (1-based) inlined
    right after that Nth paragraph — finer-grained than the whole-target
    placement the caller still handles separately for plain "{target}"."""
    parts = []
    for idx, p in enumerate(paragraphs, start=1):
        parts.append(paragraph_html(p, figure_numbers, table_numbers))
        for diagram in diagrams_by_target.get(f"{target}@{idx}", []):
            parts.append(figure_html(diagram, figure_numbers, table_numbers, manifest_dir))
    return "\n".join(parts)


def table_html(rows):
    header, *body = rows
    thead = "<tr>" + "".join(f"<th>{html.escape(str(c))}</th>" for c in header) + "</tr>"
    tbody = "\n".join(
        "<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>" for row in body
    )
    return f"<table><thead>{thead}</thead><tbody>{tbody}</tbody></table>"


def figure_html(diagram, figure_numbers, table_numbers, manifest_dir):
    anchor = html.escape(diagram["id"])
    caption = html.escape(diagram.get("caption", ""))
    if diagram.get("type") == "table":
        # A table is not a figure — its own "Table N" sequence/anchor
        # prefix, never folded into the Fig N count.
        number = table_numbers[diagram["id"]]
        figcaption = f"<figcaption><strong>Table {number}.</strong> {caption}</figcaption>"
        return f'<figure class="table-figure" id="tbl-{anchor}">{table_html(diagram["rows"])}{figcaption}</figure>'
    number = figure_numbers[diagram["id"]]
    figcaption = f"<figcaption><strong>Fig {number}.</strong> {caption}</figcaption>"
    svg_markup = extract_svg_markup(manifest_dir / diagram["file"])
    return f'<figure id="fig-{anchor}">{svg_markup}{figcaption}</figure>'


def title_case(slug):
    return slug.replace("-", " ").replace("_", " ").title()


def render_section(number, key, value, diagrams_by_target, figure_numbers, table_numbers, manifest_dir):
    """number is None for the optional trailing "appendix" section — it
    renders an unnumbered "<h2>Appendix</h2>" (and unnumbered "<h3>"
    subsection titles) instead of the "N. "/"N-M. " prefixes every fixed
    section gets."""
    heading = title_case(key)
    heading_prefix = f"{number}. " if number is not None else ""
    parts = [f"<h2>{heading_prefix}{html.escape(heading)}</h2>"]
    if isinstance(value, list):
        parts.append(render_paragraphs_with_diagrams(value, key, diagrams_by_target, figure_numbers, table_numbers, manifest_dir))
    elif isinstance(value, dict):
        for sub_index, (sub_key, sub_value) in enumerate(value.items(), start=1):
            sub_number = f"{number}-{sub_index}" if number is not None else None
            sub_target = f"{key}.{sub_key}"
            if isinstance(sub_value, dict):
                sub_title = sub_value.get("title", "")
                sub_text = sub_value.get("text", [])
                if sub_title:
                    sub_prefix = f"{sub_number}. " if sub_number is not None else ""
                    parts.append(f"<h3>{sub_prefix}{html.escape(sub_title)}</h3>")
                parts.append(render_paragraphs_with_diagrams(sub_text, sub_target, diagrams_by_target, figure_numbers, table_numbers, manifest_dir))
            else:
                parts.append(render_paragraphs_with_diagrams(sub_value, sub_target, diagrams_by_target, figure_numbers, table_numbers, manifest_dir))
            # Figures targeting the subsection as a whole (no @N paragraph
            # anchor) land at the end of that subsection, after its own
            # paragraph-anchored figures.
            for diagram in diagrams_by_target.get(sub_target, []):
                parts.append(figure_html(diagram, figure_numbers, table_numbers, manifest_dir))
    else:
        raise ValueError(f"section {key!r} must be a list of paragraphs or an object, got {type(value)}")
    # Figures targeting the section as a whole (no subsection or @N
    # paragraph anchor named) always land at the very end, after every
    # subsection's own figures.
    for diagram in diagrams_by_target.get(key, []):
        parts.append(figure_html(diagram, figure_numbers, table_numbers, manifest_dir))
    return "\n".join(parts)


def section_keys(manifest):
    """SECTION_ORDER plus the optional trailing "appendix" key if present —
    a diagram can target it too, and it's placed/numbered exactly like any
    other section (render_section just gets number=None for it, see
    build())."""
    keys = list(SECTION_ORDER)
    if "appendix" in manifest:
        keys.append("appendix")
    return keys


def ordered_diagrams(manifest, diagrams_by_target, orphan_diagrams):
    """Every diagram in the exact order render_section + the orphan-diagram
    appendix loop will place it — figure numbers follow this reading
    order, not the diagrams array's order. orphan_diagrams are diagrams
    whose "section" named nothing real, placed in a final "Appendix:
    Figures" block — distinct from the manifest's own optional "appendix"
    section (a diagrams[]-targetable section like any other, included via
    section_keys() below)."""
    def paragraph_anchored(target, paragraphs):
        ordered = []
        for idx in range(1, len(paragraphs) + 1):
            ordered.extend(diagrams_by_target.get(f"{target}@{idx}", []))
        return ordered

    ordered = []
    for key in section_keys(manifest):
        value = manifest[key]
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                sub_target = f"{key}.{sub_key}"
                paras = sub_value.get("text", []) if isinstance(sub_value, dict) else sub_value
                ordered.extend(paragraph_anchored(sub_target, paras))
                ordered.extend(diagrams_by_target.get(sub_target, []))
        else:
            ordered.extend(paragraph_anchored(key, value))
        ordered.extend(diagrams_by_target.get(key, []))
    ordered.extend(orphan_diagrams)
    return ordered


def valid_diagram_targets(manifest):
    """Every string a diagram's "section" field can name: each top-level
    section key (including the optional "appendix"), "{key}.{sub_key}" for
    each subsection of a section given as an object (sub-title
    granularity), and "{target}@{N}" (1-based) for any of those targets'
    Nth paragraph specifically — paragraph-level granularity, placing the
    figure right after that one paragraph instead of at the end of the
    whole section/subsection. Per MANIFEST-FORMAT.md."""
    targets = set(section_keys(manifest))
    for key in section_keys(manifest):
        value = manifest.get(key)
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                sub_target = f"{key}.{sub_key}"
                targets.add(sub_target)
                paras = sub_value.get("text", []) if isinstance(sub_value, dict) else sub_value
                if isinstance(paras, list):
                    targets.update(f"{sub_target}@{i}" for i in range(1, len(paras) + 1))
        elif isinstance(value, list):
            targets.update(f"{key}@{i}" for i in range(1, len(value) + 1))
    return targets


def build(manifest, manifest_dir):
    missing = [k for k in REQUIRED_KEYS if k not in manifest]
    if missing:
        raise ValueError(f"manifest missing required key(s): {', '.join(missing)}")

    targets = valid_diagram_targets(manifest)
    diagrams_by_target = {}
    orphan_diagrams = []
    for diagram in manifest["diagrams"]:
        section = diagram.get("section")
        if section in targets:
            diagrams_by_target.setdefault(section, []).append(diagram)
        else:
            orphan_diagrams.append(diagram)

    # A table is not a figure: it gets its own "Table N" sequence, counted
    # separately from "Fig N" — both still follow overall reading order.
    figure_numbers, table_numbers = {}, {}
    fig_i = tbl_i = 0
    for d in ordered_diagrams(manifest, diagrams_by_target, orphan_diagrams):
        if d.get("type") == "table":
            tbl_i += 1
            table_numbers[d["id"]] = tbl_i
        else:
            fig_i += 1
            figure_numbers[d["id"]] = fig_i

    body_parts = []
    for number, key in enumerate(SECTION_ORDER, start=1):
        body_parts.append(render_section(number, key, manifest[key], diagrams_by_target, figure_numbers, table_numbers, manifest_dir))

    # The optional raw-data appendix (unnumbered, exempt from lint's
    # prose-quality checks) — distinct from the orphan-diagram appendix
    # below.
    if "appendix" in manifest:
        body_parts.append(render_section(None, "appendix", manifest["appendix"], diagrams_by_target, figure_numbers, table_numbers, manifest_dir))

    if orphan_diagrams:
        body_parts.append("<h2>Appendix: Figures</h2>")
        for diagram in orphan_diagrams:
            body_parts.append(figure_html(diagram, figure_numbers, table_numbers, manifest_dir))

    template = TEMPLATE.read_text(encoding="utf-8")
    return (
        template
        .replace("{{TITLE}}", html.escape(manifest["title"]))
        .replace("{{ABSTRACT}}", render_fig_refs(html.escape(manifest["abstract"][0]), figure_numbers, table_numbers))
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
            "introduction": ["First para, see {{fig:fig1}}, {{tbl:tbl1}} and {{fig:nope}}.", "Second para."],
            "background": {
                "bg1": ["Plain subsection text."],
                "bg2": {"title": "Prior Work", "text": ["Some prior work text."]},
            },
            "methodology": ["One methodology paragraph."],
            "results": ["Some results."],
            "discussion": ["One discussion paragraph."],
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

        # A "table" diagram renders as a <table>, not an <img>/<svg>, and is
        # a numbered, captioned <figure> — but a table is not a figure: its
        # own "Table N" sequence/anchor prefix, never folded into Fig N.
        assert '<figure class="table-figure" id="tbl-tbl1">' in html_out
        assert "<th>Metric</th><th>Before</th><th>After</th>" in html_out
        assert "<td>Latency</td><td>85ms</td><td>20ms</td>" in html_out
        assert "<strong>Table 1.</strong> Cap 4" in html_out  # tbl1, in Results

        # Figure numbers follow reading order (fig3 appears first in the
        # document, inside Background), not the diagrams array's order, and
        # skip over tbl1 entirely (it's numbered in its own sequence).
        assert "<figure id=\"fig-fig3\">" in html_out
        assert "<strong>Fig 1.</strong> Cap 3" in html_out
        assert "<figure id=\"fig-fig1\">" in html_out
        assert "<strong>Fig 2.</strong> Cap 1" in html_out
        assert "<strong>Fig 3.</strong> Cap 2" in html_out  # fig2, appendix, is last
        # {{fig:fig1}} in the introduction resolves to a link with fig1's
        # actual number (2); an unknown id degrades visibly, doesn't crash.
        assert '<a href="#fig-fig1">Fig 2</a>' in html_out
        assert "[unknown fig: nope]" in html_out
        # {{tbl:tbl1}} resolves the same way, into a link to tbl1's own
        # "Table 1" number/anchor, not the figure sequence.
        assert '<a href="#tbl-tbl1">Table 1</a>' in html_out

        # The optional "appendix" key: unnumbered heading, unnumbered
        # subsection title, placed after Conclusion but before the
        # orphan-diagram "Appendix: Figures" block, and a diagram can
        # target it ("appendix" / "appendix.<sub>") like any real section.
        appendix_manifest = dict(manifest)
        appendix_manifest["appendix"] = {
            "raw-timings": {"title": "Raw Timings", "text": ["latency_ms,85,20", "throughput_rps,120,410"]},
        }
        appendix_manifest["diagrams"] = manifest["diagrams"] + [
            {"id": "fig9", "file": "assets/fig1.svg", "caption": "Raw data chart.", "section": "appendix.raw-timings"}
        ]
        html_out = build(appendix_manifest, tmp)
        assert "<h2>Appendix</h2>" in html_out, "the raw-data appendix heading must be unnumbered"
        assert "<h3>Raw Timings</h3>" in html_out, "its subsection title must be unnumbered too"
        assert "latency_ms,85,20" in html_out
        conclusion_pos = html_out.index("<h2>6. Conclusion</h2>")
        appendix_pos = html_out.index("<h2>Appendix</h2>")
        appendix_figures_pos = html_out.index("<h2>Appendix: Figures</h2>")
        fig9_pos = html_out.index('id="fig-fig9"')
        assert conclusion_pos < appendix_pos < fig9_pos < appendix_figures_pos, (
            "the raw-data appendix (and diagrams targeting it) must land after Conclusion "
            "but before the orphan-diagram appendix"
        )

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

        # Paragraph-level diagram placement ("{target}@{N}") and bullet
        # lists (a paragraph-array element that's itself a list of items).
        anchored_manifest = dict(manifest)
        anchored_manifest["introduction"] = [
            "First para.",
            ["Bullet one.", "Bullet two.", "Bullet three."],
            "Second para.",
        ]
        anchored_manifest["diagrams"] = [
            {"id": "fig1", "file": "assets/fig1.svg", "caption": "Cap 1", "section": "introduction@1"},
        ]
        html_out = build(anchored_manifest, tmp)
        assert "<ul><li>Bullet one.</li><li>Bullet two.</li><li>Bullet three.</li></ul>" in html_out
        first_para_pos = html_out.index("First para.")
        fig1_pos = html_out.index("FIG1-MARKER")
        bullets_pos = html_out.index("Bullet one.")
        second_para_pos = html_out.index("Second para.")
        assert first_para_pos < fig1_pos < bullets_pos < second_para_pos, (
            "a diagram targeting introduction@1 must land right after the 1st paragraph, "
            "before the 2nd (the bullet list)"
        )

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
