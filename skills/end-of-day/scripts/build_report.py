#!/usr/bin/env python3
"""
Fill references/template.html from a JSON manifest and write a self-contained
report HTML — every diagram inlined as a data URI, so the page opens standalone.

Usage:
  python build_report.py manifest.json report.html

Manifest schema:
{
  "eyebrow": "END OF DAY", "title": "...", "dek": "...",
  "meta": [["date", "2026-08-06"], ["items", "5"]],
  "footer": "...",
  "items": [
    {"title": "...", "svg": "diagram.svg or null",
     "introduction": "...", "abstraction": "...", "detailed": "..."}
  ]
}

"svg" is a path (relative to the manifest file, or absolute) to an SVG
diagram, an existing data: URI, or null/omitted if that item's diagram
render failed or was skipped.
"""
import sys, os, re, json, base64, html
from validate_svg import validate_svg_wellformed


def slugify(title):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", title.lower())).strip("-")


def embed_svg(path, base_dir):
    if path.startswith("data:"):
        return path
    full = path if os.path.isabs(path) else os.path.join(base_dir, path)
    try:
        validate_svg_wellformed(full)
    except ValueError as e:
        sys.exit(f"{full}: invalid SVG, refusing to embed — {e}")
    with open(full, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/svg+xml;base64,{b64}"


def mono(s):
    """Escape, then turn `backtick` spans into <code> — the only markup card text gets."""
    parts = html.escape(s).split("`")
    return "".join(f"<code>{p}</code>" if i % 2 else p for i, p in enumerate(parts))


def card_html(item, base_dir):
    slug = slugify(item["title"])
    media = ""
    if item.get("svg"):
        img = embed_svg(item["svg"], base_dir)
        media = f'<div class="card-media"><img src="{img}" alt="{html.escape(item["title"])} diagram" loading="lazy"></div>'
    return f'''
    <article class="card" id="{slug}">
      {media}
      <div class="card-body">
        <div class="card-head"><h3>{html.escape(item["title"])}</h3></div>
        <dl>
          <dt>Introduction</dt><dd>{mono(item["introduction"])}</dd>
          <dt>Abstraction</dt><dd>{mono(item["abstraction"])}</dd>
          <dt>Detailed</dt><dd>{mono(item["detailed"])}</dd>
        </dl>
      </div>
    </article>'''


def toc_html(items):
    return "\n".join(
        f'<li><a href="#{slugify(item["title"])}">{html.escape(item["title"])}</a></li>'
        for item in items
    )


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    manifest_path, out_path = sys.argv[1], sys.argv[2]
    base_dir = os.path.dirname(os.path.abspath(manifest_path))
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "template.html")

    with open(manifest_path) as f:
        m = json.load(f)
    with open(template_path) as f:
        tpl = f.read()

    meta_row = "\n".join(f'<span>{html.escape(l)} <b>{html.escape(v)}</b></span>' for l, v in m.get("meta", []))
    cards = "\n".join(card_html(item, base_dir) for item in m["items"])

    out = (tpl
           .replace("{{EYEBROW}}", html.escape(m.get("eyebrow", "END OF DAY")))
           .replace("{{TITLE}}", html.escape(m["title"]))
           .replace("{{DEK}}", mono(m.get("dek", "")))
           .replace("{{META_ROW}}", meta_row)
           .replace("{{TOC}}", toc_html(m["items"]))
           .replace("{{CARDS}}", cards)
           .replace("{{FOOTER}}", mono(m.get("footer", ""))))

    with open(out_path, "w") as f:
        f.write(out)
    print(f"wrote {out_path} ({len(out)} bytes, {len(m['items'])} items)")


if __name__ == "__main__":
    main()
