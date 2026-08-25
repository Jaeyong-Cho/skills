#!/usr/bin/env python3
"""
Lint a to-paper manifest.json for writing-quality and diagram rules.

Every section/subsection's prose is a JSON array of paragraph strings, one
element per paragraph — never a single "\n\n"-joined blob. abstract is that
same array, constrained to exactly one element. See ../MANIFEST-FORMAT.md.

Checks:
- title: fewer than 15 words.
- abstract: exactly one paragraph (array of length 1).
- every other section/subsection: a paragraph-count range that varies by
  section (a subsection inherits its parent section's range) — see
  SECTION_PARAGRAPH_RANGES below: introduction 3-5, background 4-8,
  methodology 2-4, results 2-4, discussion 3-6, conclusion 1-3.
- each non-table diagram's file also gets diagram-design's own
  self_check.py verifier run against it (single-file safety rules, motion
  contract) — not just the accessible-SVG subset re-checked below.
- every paragraph, anywhere: 3-8 sentences.
- every sentence, anywhere: at most 20 words.
- diagrams: at least 5 entries (a floor, not a target — more is fine),
  each with id/caption, each caption at most 140 characters (a long
  caption doesn't shrink the figure — see assets/template.html — it
  wraps, but a runaway caption is still a paragraph in disguise), and
  at least 3 different diagram_type/table kinds used across them (per
  DIAGRAM-SELECTION.md's Visual-type guide — don't draw five
  flowcharts). Two kinds:
  - svg (default, no "type" field) — a `diagram_type` naming its
    diagram-design visual type (e.g. "Flowchart", "Bar chart"), a
    `file` existing (relative to manifest.json's directory) and
    passing the same accessible-SVG contract diagram-design's
    scripts/self_check.py enforces: role="img", <title> first child,
    non-empty <title>/<desc> with diagram-prefixed ids, aria-labelledby
    naming title then desc — plus a viewBox (so scaling to the page's
    max-width never crops it) and explicit width/height attributes (an
    <img src> pointing at an SVG with only a viewBox renders at a
    300x150px default, ignoring max-width). Also flags any rect/circle/
    ellipse/line whose own coordinates place it outside the declared
    viewBox — the outermost <svg> clips to its viewBox by default (unlike
    the page-level max-width/height:auto scaling, which only shrinks
    content that already fits inside it), so a box added without widening
    the viewBox to match is silently cut off, not shrunk into view. A
    heuristic, not a real renderer: <path>/<text>/<polygon> bounding boxes
    aren't checked.
  - table ("type": "table") — a `rows` array: a header row plus at
    least one data row, every row the same length as the header;
    counts as its own kind ("table") toward the 3-kind minimum.
- every {{fig:some-id}} reference in any prose block names a real
  diagrams[].id (build_paper.py resolves these to "Fig N" links).

Usage:
  python lint_paper.py <manifest.json>

Exit code 0 if every check passes, 1 otherwise (one line per violation).
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from self_check import verify as diagram_self_check  # noqa: E402 (vendored copy, see self_check.py's docstring)

SECTION_ORDER = ["introduction", "background", "methodology", "results", "discussion", "conclusion"]
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
FIG_REF_RE = re.compile(r"\{\{fig:([\w-]+)\}\}")
SVG_BLOCK_RE = re.compile(r"<svg\b.*?</svg>", re.DOTALL)
MAX_TITLE_WORDS = 15
MAX_SENTENCE_WORDS = 20
MIN_PARAGRAPH_SENTENCES = 3
MAX_PARAGRAPH_SENTENCES = 8
# Paragraph-count range per top-level section, standard academic-writing
# guidance (a subsection inherits its parent section's range).
SECTION_PARAGRAPH_RANGES = {
    "introduction": (3, 5),
    "background": (4, 8),
    "methodology": (2, 4),
    "results": (2, 4),
    "discussion": (3, 6),
    "conclusion": (1, 3),
}
MIN_DIAGRAMS = 5
MIN_DIAGRAM_TYPES = 3
MAX_CAPTION_CHARS = 140


def words(text):
    return [w for w in re.split(r"\s+", text.strip()) if w]


def sentences(paragraph):
    return [s for s in SENTENCE_RE.split(paragraph.strip()) if s]


def paragraphs(text):
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def check_prose_block(label, paras, errors, *, one_paragraph=False, paragraph_range=None):
    """paras is a list of paragraph strings — a manifest section/subsection's
    text field, or paragraphs(some_markdown_text) for a plain-string caller.

    paragraph_range is a (min, max) tuple, typically SECTION_PARAGRAPH_RANGES
    looked up by the section's key; pass None to skip the paragraph-count
    check entirely (only sentence/word checks run)."""
    if one_paragraph:
        if len(paras) != 1:
            errors.append(f"{label}: must be exactly one paragraph, found {len(paras)}")
    elif paragraph_range is not None:
        lo, hi = paragraph_range
        if not (lo <= len(paras) <= hi):
            errors.append(f"{label}: expected {lo}-{hi} paragraphs, found {len(paras)}")
    for p_index, para in enumerate(paras, start=1):
        sents = sentences(para)
        if not (MIN_PARAGRAPH_SENTENCES <= len(sents) <= MAX_PARAGRAPH_SENTENCES):
            errors.append(
                f"{label} paragraph {p_index}: expected {MIN_PARAGRAPH_SENTENCES}-{MAX_PARAGRAPH_SENTENCES} sentences, found {len(sents)}"
            )
        for s_index, sent in enumerate(sents, start=1):
            w = words(sent)
            if len(w) > MAX_SENTENCE_WORDS:
                errors.append(
                    f"{label} paragraph {p_index} sentence {s_index}: {len(w)} words, max {MAX_SENTENCE_WORDS}"
                )


def check_fig_refs(label, text, valid_ids, errors):
    for m in FIG_REF_RE.finditer(text):
        fig_id = m.group(1)
        if fig_id not in valid_ids:
            errors.append(f"{label}: {{{{fig:{fig_id}}}}} references an unknown diagram id")


def check_section(key, value, valid_ids, errors):
    paragraph_range = SECTION_PARAGRAPH_RANGES.get(key)
    if isinstance(value, list):
        check_prose_block(key, value, errors, paragraph_range=paragraph_range)
        check_fig_refs(key, "\n\n".join(value), valid_ids, errors)
    elif isinstance(value, dict):
        for sub_key, sub_value in value.items():
            label = f"{key}.{sub_key}"
            paras = sub_value.get("text", []) if isinstance(sub_value, dict) else sub_value
            check_prose_block(label, paras, errors, paragraph_range=paragraph_range)
            check_fig_refs(label, "\n\n".join(paras), valid_ids, errors)
    else:
        errors.append(f"{key}: must be a list of paragraphs or an object of subsections, got {type(value).__name__}")


def local_tag(elem):
    return elem.tag.rsplit("}", 1)[-1]


# ponytail: geometry check covers only rect/circle/ellipse/line — the
# shapes with numeric coordinates cheap to read off attributes. <path>,
# <text>, and <polygon> bounding boxes need a real renderer to compute, so
# a stray label or curve past the edge won't be caught here; the taste-gate
# checklist's own eyeballing is still the backstop for those.
SVG_BOUNDS_SKIP_TAGS = {"defs", "marker", "symbol", "clipPath", "mask", "pattern"}
SVG_BOUNDS_TOLERANCE = 1.0


def check_svg_bounds(root, view_box, label, errors):
    """The outermost <svg> clips to its viewBox by default (UA overflow:
    hidden) — unlike the page-level max-width/height:auto scaling in
    assets/template.html, content drawn past the viewBox edge doesn't
    shrink into view, it's just gone. Flags the common, cheaply-detectable
    case: a shape whose own coordinates place it outside the declared
    viewBox (e.g. a legend row added without widening the viewBox to fit)."""
    parts = re.split(r"[ ,]+", view_box.strip())
    try:
        min_x, min_y, vb_w, vb_h = (float(p) for p in parts if p)
    except ValueError:
        return
    max_x, max_y = min_x + vb_w, min_y + vb_h

    def bbox_of(tag, elem):
        try:
            if tag == "rect":
                x, y = float(elem.get("x", "0")), float(elem.get("y", "0"))
                w, h = float(elem.get("width", "0")), float(elem.get("height", "0"))
                return (x, y, x + w, y + h)
            if tag == "circle":
                cx, cy, r = (float(elem.get(k, "0")) for k in ("cx", "cy", "r"))
                return (cx - r, cy - r, cx + r, cy + r)
            if tag == "ellipse":
                cx, cy = float(elem.get("cx", "0")), float(elem.get("cy", "0"))
                rx, ry = float(elem.get("rx", "0")), float(elem.get("ry", "0"))
                return (cx - rx, cy - ry, cx + rx, cy + ry)
            if tag == "line":
                x1, y1, x2, y2 = (float(elem.get(k, "0")) for k in ("x1", "y1", "x2", "y2"))
                return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        except ValueError:
            pass  # non-numeric (percentages, calc()) — outside this heuristic's reach
        return None

    def walk(elem):
        tag = local_tag(elem)
        if tag in SVG_BOUNDS_SKIP_TAGS:
            return
        bbox = bbox_of(tag, elem)
        if bbox is not None:
            x0, y0, x1, y1 = bbox
            if (
                x0 < min_x - SVG_BOUNDS_TOLERANCE
                or y0 < min_y - SVG_BOUNDS_TOLERANCE
                or x1 > max_x + SVG_BOUNDS_TOLERANCE
                or y1 > max_y + SVG_BOUNDS_TOLERANCE
            ):
                errors.append(
                    f"{label}: <{tag}> at ({x0:g},{y0:g})-({x1:g},{y1:g}) extends outside the "
                    f"viewBox ({min_x:g},{min_y:g})-({max_x:g},{max_y:g}) — the outermost <svg> "
                    "clips content past its viewBox by default (it won't scale into view), "
                    "widen the viewBox (and matching width/height) to enclose it"
                )
        for child in elem:
            walk(child)

    walk(root)


def check_svg_accessibility(svg_path, label, errors):
    """Same accessible-SVG contract as diagram-design's scripts/self_check.py
    (role=img, <title> first child, non-empty <title>/<desc>, diagram-prefixed
    ids, aria-labelledby naming title then desc) — applied to whatever
    <svg>...</svg> block build_paper.py would extract and inline from this
    file, whether it's a bare .svg or a full diagram-design .diagram.html
    draft; either way only that one block is checked, not the whole file."""
    text = svg_path.read_text(encoding="utf-8")
    match = SVG_BLOCK_RE.search(text)
    if not match:
        errors.append(f"{label}: no <svg>...</svg> block found")
        return
    try:
        root = ET.fromstring(match.group(0))
    except ET.ParseError as e:
        errors.append(f"{label}: <svg> block is not well-formed XML: {e}")
        return
    if local_tag(root) != "svg":
        errors.append(f"{label}: root element is <{local_tag(root)}>, expected <svg>")
        return
    if root.get("role") != "img":
        errors.append(f'{label}: <svg> needs role="img"')
    view_box = (root.get("viewBox") or "").strip()
    if not view_box:
        errors.append(
            f"{label}: <svg> needs a viewBox attribute — width/height alone won't scale "
            "cleanly to the page's max-width and can crop the figure"
        )
    else:
        check_svg_bounds(root, view_box, label, errors)
    if not (root.get("width") or "").strip() or not (root.get("height") or "").strip():
        errors.append(
            f"{label}: <svg> needs width and height attributes (matching viewBox), not just "
            "viewBox — they establish the correct aspect ratio unambiguously across renderers"
        )
    children = list(root)
    if not children or local_tag(children[0]) != "title":
        errors.append(f"{label}: <title> must be the first child of <svg>")
    title_el = next((c for c in children if local_tag(c) == "title"), None)
    desc_el = next((c for c in children if local_tag(c) == "desc"), None)
    if title_el is None or not (title_el.text or "").strip():
        errors.append(f"{label}: needs a non-empty <title>")
    if desc_el is None or not (desc_el.text or "").strip():
        errors.append(f"{label}: needs a non-empty <desc>")
    title_id = title_el.get("id", "") if title_el is not None else ""
    desc_id = desc_el.get("id", "") if desc_el is not None else ""
    if title_id in ("", "title") or desc_id in ("", "desc"):
        errors.append(f"{label}: <title>/<desc> ids must be diagram-prefixed, never bare 'title'/'desc'")
    labelled = (root.get("aria-labelledby", "") or "").split()
    if labelled != [title_id, desc_id]:
        errors.append(f"{label}: svg aria-labelledby must name the title id then the desc id")

    # Beyond this file's own viewBox/width/height/accessible-SVG checks
    # above (specific to embedding into the paper), run diagram-design's
    # own self_check.py against the whole file — single-file safety rules
    # (no remote assets, no executable attributes) and, if present, the
    # structural motion contract.
    for e in diagram_self_check(svg_path):
        errors.append(f"{label}: [self_check.py] {e}")


def check_table_rows(rows, label, errors):
    if not isinstance(rows, list) or len(rows) < 2:
        errors.append(f"{label}: 'rows' needs a header row plus at least one data row")
        return
    header_len = len(rows[0]) if isinstance(rows[0], list) else -1
    for r, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != header_len:
            errors.append(f"{label}: row {r} has a different column count than the header")


def check_diagrams(diagrams, manifest_dir, errors):
    if not isinstance(diagrams, list) or len(diagrams) < MIN_DIAGRAMS:
        errors.append(f"diagrams: need at least {MIN_DIAGRAMS}, found {len(diagrams) if isinstance(diagrams, list) else 0}")
        diagrams = diagrams if isinstance(diagrams, list) else []
    used_types = set()
    for i, diagram in enumerate(diagrams, start=1):
        is_table = diagram.get("type") == "table"
        required_fields = ("id", "caption", "rows") if is_table else ("id", "file", "caption", "diagram_type")
        for field in required_fields:
            if not diagram.get(field):
                errors.append(f"diagrams[{i}]: missing '{field}'")
        caption = diagram.get("caption", "")
        if len(caption) > MAX_CAPTION_CHARS:
            errors.append(f"diagrams[{i}]: caption is {len(caption)} chars, max {MAX_CAPTION_CHARS}")
        used_types.add("table" if is_table else diagram.get("diagram_type", "").strip().lower())
        if is_table:
            if diagram.get("rows"):
                check_table_rows(diagram["rows"], f"diagrams[{i}]", errors)
            continue
        file_field = diagram.get("file")
        if not file_field:
            continue
        svg_path = manifest_dir / file_field
        if not svg_path.is_file():
            errors.append(f"diagrams[{i}]: file not found: {file_field}")
            continue
        check_svg_accessibility(svg_path, f"diagrams[{i}] ({file_field})", errors)
    used_types.discard("")
    if len(used_types) < MIN_DIAGRAM_TYPES:
        errors.append(
            f"diagrams: need at least {MIN_DIAGRAM_TYPES} different diagram_type/table kinds, "
            f"found {len(used_types)} ({', '.join(sorted(used_types)) or 'none'}) — don't draw the same visual type repeatedly"
        )


def lint(manifest, manifest_dir):
    errors = []
    required = ["title", "abstract", *SECTION_ORDER, "diagrams"]
    missing = [k for k in required if k not in manifest]
    if missing:
        errors.append(f"manifest missing required key(s): {', '.join(missing)}")
        return errors

    title_words = words(manifest["title"])
    if len(title_words) >= MAX_TITLE_WORDS:
        errors.append(f"title: {len(title_words)} words, must be fewer than {MAX_TITLE_WORDS}")

    diagrams = manifest["diagrams"] if isinstance(manifest["diagrams"], list) else []
    valid_ids = {d.get("id") for d in diagrams if isinstance(d, dict) and d.get("id")}

    abstract = manifest["abstract"]
    if not isinstance(abstract, list):
        errors.append(f"abstract: must be a list of paragraphs (one element), got {type(abstract).__name__}")
        abstract = []
    check_prose_block("abstract", abstract, errors, one_paragraph=True)
    check_fig_refs("abstract", "\n\n".join(abstract), valid_ids, errors)

    for key in SECTION_ORDER:
        check_section(key, manifest[key], valid_ids, errors)

    check_diagrams(manifest["diagrams"], manifest_dir, errors)
    return errors


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    manifest_path = Path(sys.argv[1])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors = lint(manifest, manifest_path.parent)
    for e in errors:
        print(e)
    if errors:
        print(f"FAIL — {len(errors)} violation(s)")
        sys.exit(1)
    print("OK")
    sys.exit(0)


def self_test():
    import shutil
    import tempfile

    tmp = Path(tempfile.mkdtemp())
    try:
        three_sentences = " ".join(f"This is sentence number {i}." for i in range(3))

        def block(n_paragraphs):
            return [three_sentences for _ in range(n_paragraphs)]

        good_manifest = {
            "title": "A Short Study Title",
            "abstract": [three_sentences],
            "introduction": block(3),
            "background": {"bg1": block(4), "bg2": {"title": "Prior Work", "text": block(4)}},
            "methodology": block(3),
            "results": block(3),
            "discussion": block(3),
            "conclusion": block(2),
            "diagrams": [
                {"id": "fig1", "file": "assets/fig1.svg", "caption": "c1", "section": "methodology", "diagram_type": "Flowchart"},
                {"id": "fig2", "file": "assets/fig2.svg", "caption": "c2", "section": "results", "diagram_type": "Bar chart"},
                {"id": "fig3", "file": "assets/fig3.svg", "caption": "c3", "section": "background", "diagram_type": "Architecture"},
                {"id": "fig4", "file": "assets/fig4.svg", "caption": "c4", "section": "introduction", "diagram_type": "Flowchart"},
                {"id": "fig5", "file": "assets/fig5.svg", "caption": "c5", "section": "conclusion", "diagram_type": "Timeline"},
                {
                    "id": "tbl1",
                    "type": "table",
                    "rows": [["Metric", "Before", "After"], ["Latency", "85ms", "20ms"]],
                    "caption": "c6",
                    "section": "results",
                },
            ],
        }
        assets = tmp / "assets"
        assets.mkdir()
        for i, name in enumerate(("fig1.svg", "fig2.svg", "fig3.svg", "fig4.svg", "fig5.svg"), start=1):
            (assets / name).write_text(
                f'<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 200 100" '
                f'width="200" height="100" aria-labelledby="fig{i}-t fig{i}-d">'
                f'<title id="fig{i}-t">Figure {i}</title>'
                f'<desc id="fig{i}-d">What figure {i} shows.</desc>'
                f"</svg>"
            )
        (assets / "inaccessible.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>')
        (assets / "no-viewbox.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" role="img" width="200" height="100" '
            'aria-labelledby="nv-t nv-d">'
            '<title id="nv-t">No Viewbox</title><desc id="nv-d">Missing viewBox.</desc>'
            "</svg>"
        )
        (assets / "no-dims.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 200 100" '
            'aria-labelledby="nd-t nd-d">'
            '<title id="nd-t">No Dims</title><desc id="nd-d">Missing width/height.</desc>'
            "</svg>"
        )
        (assets / "out-of-bounds.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 200 100" '
            'width="200" height="100" aria-labelledby="oob-t oob-d">'
            '<title id="oob-t">Out Of Bounds</title><desc id="oob-d">A box past the viewBox edge.</desc>'
            '<rect x="150" y="80" width="100" height="60"/>'
            "</svg>"
        )
        (assets / "fig6.diagram.html").write_text(
            "<!DOCTYPE html><html><head><title>draft</title></head><body>"
            '<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 200 100" width="200" height="100" '
            'aria-labelledby="fig6-t fig6-d">'
            '<title id="fig6-t">Figure 6</title><desc id="fig6-d">What figure 6 shows.</desc>'
            "</svg></body></html>"
        )

        errors = lint(good_manifest, tmp)
        assert not errors, f"good manifest should lint clean, got: {errors}"

        # A diagram-design .diagram.html draft (never exported to a bare
        # .svg) lints exactly the same as one — only its <svg> block matters.
        draft_manifest = dict(good_manifest)
        draft_manifest["diagrams"] = good_manifest["diagrams"][:4] + [
            {"id": "fig6", "file": "assets/fig6.diagram.html", "caption": "c6", "section": "results", "diagram_type": "Sequence"}
        ]
        errors = lint(draft_manifest, tmp)
        assert not errors, f"a .diagram.html draft should lint clean too, got: {errors}"

        inaccessible_manifest = dict(good_manifest)
        inaccessible_manifest["diagrams"] = good_manifest["diagrams"][:4] + [
            {"id": "fig6", "file": "assets/inaccessible.svg", "caption": "c6", "section": "results"}
        ]
        errors = lint(inaccessible_manifest, tmp)
        joined = "\n".join(errors)
        assert any('role="img"' in e for e in errors), joined
        assert any("<title>" in e and "first child" in e for e in errors), joined
        assert any("aria-labelledby" in e for e in errors), joined

        no_viewbox_manifest = dict(good_manifest)
        no_viewbox_manifest["diagrams"] = good_manifest["diagrams"][:4] + [
            {"id": "fig7", "file": "assets/no-viewbox.svg", "caption": "c7", "section": "results"}
        ]
        errors = lint(no_viewbox_manifest, tmp)
        assert any("viewBox" in e for e in errors), "\n".join(errors)

        no_dims_manifest = dict(good_manifest)
        no_dims_manifest["diagrams"] = good_manifest["diagrams"][:4] + [
            {"id": "fig8", "file": "assets/no-dims.svg", "caption": "c8", "section": "results", "diagram_type": "Flowchart"}
        ]
        errors = lint(no_dims_manifest, tmp)
        assert any("width and height attributes" in e for e in errors), "\n".join(errors)

        out_of_bounds_manifest = dict(good_manifest)
        out_of_bounds_manifest["diagrams"] = good_manifest["diagrams"][:4] + [
            {"id": "fig9", "file": "assets/out-of-bounds.svg", "caption": "c9", "section": "results", "diagram_type": "Flowchart"}
        ]
        errors = lint(out_of_bounds_manifest, tmp)
        assert any("extends outside the viewBox" in e for e in errors), "\n".join(errors)

        low_variety_manifest = dict(good_manifest)
        low_variety_manifest["diagrams"] = [
            dict(d, id=f"fc{i}", file=f"assets/fig{i}.svg", diagram_type="Flowchart")
            for i, d in enumerate(good_manifest["diagrams"][:5], start=1)
        ]
        errors = lint(low_variety_manifest, tmp)
        assert any("different diagram_type" in e for e in errors), "\n".join(errors)

        missing_diagram_type_manifest = dict(good_manifest)
        missing_diagram_type_manifest["diagrams"] = [dict(good_manifest["diagrams"][0])]
        del missing_diagram_type_manifest["diagrams"][0]["diagram_type"]
        missing_diagram_type_manifest["diagrams"] += good_manifest["diagrams"][1:]
        errors = lint(missing_diagram_type_manifest, tmp)
        assert any("missing 'diagram_type'" in e for e in errors), "\n".join(errors)

        bad_table_manifest = dict(good_manifest)
        bad_table_manifest["diagrams"] = good_manifest["diagrams"][:5] + [
            {"id": "tbl2", "type": "table", "rows": [["A", "B"], ["x"]], "caption": "c7", "section": "results"}
        ]
        errors = lint(bad_table_manifest, tmp)
        assert any("column count" in e for e in errors), "\n".join(errors)

        long_caption_manifest = dict(good_manifest)
        long_caption_manifest["diagrams"] = list(good_manifest["diagrams"])
        long_caption_manifest["diagrams"][0] = dict(
            long_caption_manifest["diagrams"][0], caption="x" * (MAX_CAPTION_CHARS + 1)
        )
        errors = lint(long_caption_manifest, tmp)
        assert any("caption is" in e and "max" in e for e in errors), "\n".join(errors)

        bad_fig_ref_manifest = dict(good_manifest)
        # Add a 4th paragraph (still within introduction's 3-5 range) whose
        # extra sentence references a diagram id that doesn't exist.
        bad_fig_ref_manifest["introduction"] = block(3) + [three_sentences + " See {{fig:no-such-id}}."]
        errors = lint(bad_fig_ref_manifest, tmp)
        assert any("fig:no-such-id" in e and "unknown" in e for e in errors), "\n".join(errors)

        bad_manifest = dict(good_manifest)
        bad_manifest["title"] = " ".join(f"word{i}" for i in range(20))
        bad_manifest["abstract"] = block(2)  # two paragraphs, not one
        bad_manifest["introduction"] = block(1)  # too few paragraphs
        bad_manifest["diagrams"] = good_manifest["diagrams"][:2]  # only 2, below the floor of 5

        errors = lint(bad_manifest, tmp)
        joined = "\n".join(errors)
        assert any("title" in e for e in errors), joined
        assert any("abstract" in e and "one paragraph" in e for e in errors), joined
        assert any("introduction" in e for e in errors), joined
        assert any("diagrams" in e and "at least" in e for e in errors), joined

        missing_file_manifest = dict(good_manifest)
        missing_file_manifest["diagrams"] = good_manifest["diagrams"] + [
            {"id": "fig4", "file": "assets/missing.svg", "caption": "c4", "section": "results"}
        ]
        errors = lint(missing_file_manifest, tmp)
        assert any("not found" in e for e in errors), "\n".join(errors)

        print("self-test passed")
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--test":
        self_test()
    else:
        main()
