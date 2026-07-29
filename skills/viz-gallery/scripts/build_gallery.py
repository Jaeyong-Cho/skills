#!/usr/bin/env python3
"""
Fill references/template.html from a JSON manifest and write a self-contained
index.html — every image inlined as a data URI, so the page opens standalone.

Usage:
  python build_gallery.py manifest.json index.html

Manifest schema:
{
  "eyebrow": "viz-gallery · <dataset name>",
  "title": "...", "dek": "...",
  "meta": [["rows", "576"], ["columns", "8"], ...],
  "stats": [["0.72", "r sales x units"], ...],
  "footer": "...",
  "cards": [
    {"category": "Trend & time", "title": "...", "image": "chart.png",
     "why": "...", "insights": "...", "sl": "...", "best": "..."}
  ]
}

"category" must be one of the catalog.md categories (case-insensitive):
comparison, distribution, relationship, composition, trend & time, hierarchy,
network, geospatial, multivariate. "image" is a path (relative to the
manifest file, or absolute) to a PNG/JPEG/SVG, or an existing data: URI.
"""
import sys, os, json, base64, mimetypes, html

SLOT_HEX = {
    1: "#856c02", 2: "#2876b2", 3: "#9f5c0b", 4: "#00a2a3",
    5: "#b05555", 6: "#296926", 7: "#805ba7", 8: "#617613",
}
# Slot assignment follows catalog.md's category order; multivariate (9th
# category, no slot of its own) reuses slot 1 rather than crowding a new hue in.
CATEGORY_SLOT = {
    "comparison": 1, "distribution": 2, "relationship": 3, "composition": 4,
    "trend & time": 5, "hierarchy": 6, "network": 7, "geospatial": 8,
    "multivariate": 1,
}
# From palette.md: white text wins the contrast check on every slot except 4 (cyan).
SLOT_TEXT = {slot: ("#2a2920" if slot == 4 else "#ffffff") for slot in SLOT_HEX}


def embed_image(path, base_dir):
    if path.startswith("data:"):
        return path
    full = path if os.path.isabs(path) else os.path.join(base_dir, path)
    mime = mimetypes.guess_type(full)[0] or "image/png"
    with open(full, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"


def mono(s):
    """Escape, then turn `backtick` spans into <code> — the only markup card text gets."""
    parts = html.escape(s).split("`")
    return "".join(f"<code>{p}</code>" if i % 2 else p for i, p in enumerate(parts))


def card_html(card, base_dir):
    slot = CATEGORY_SLOT[card["category"].strip().lower()]
    chip_bg, chip_fg = SLOT_HEX[slot], SLOT_TEXT[slot]
    img = embed_image(card["image"], base_dir)
    return f'''
    <article class="card">
      <div class="card-media"><img src="{img}" alt="{html.escape(card["title"])}" loading="lazy"></div>
      <div class="card-body">
        <div class="card-head">
          <span class="chip" style="background:{chip_bg};color:{chip_fg}">{html.escape(card["category"])}</span>
          <h3>{html.escape(card["title"])}</h3>
        </div>
        <dl>
          <dt>Why this form</dt><dd>{mono(card["why"])}</dd>
          <dt>Insights</dt><dd>{mono(card["insights"])}</dd>
          <dt>Strengths / limitations</dt><dd>{mono(card["sl"])}</dd>
          <dt>Best used for</dt><dd>{mono(card["best"])}</dd>
        </dl>
      </div>
    </article>'''


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
    stats = "\n".join(f'<div class="stat"><span class="n">{html.escape(v)}</span><span class="l">{html.escape(l)}</span></div>' for v, l in m.get("stats", []))
    swatches = "\n".join(
        f'<div class="swatch"><span class="swatch-color" style="background:{SLOT_HEX[i]}"></span>'
        f'<span class="swatch-hex">{SLOT_HEX[i]}</span></div>' for i in range(1, 9)
    )
    cards = "\n".join(card_html(c, base_dir) for c in m["cards"])

    out = (tpl
           .replace("{{EYEBROW}}", html.escape(m.get("eyebrow", "viz-gallery")))
           .replace("{{TITLE}}", html.escape(m["title"]))
           .replace("{{DEK}}", mono(m.get("dek", "")))
           .replace("{{META_ROW}}", meta_row)
           .replace("{{STATS}}", stats)
           .replace("{{SWATCHES}}", swatches)
           .replace("{{CARDS}}", cards)
           .replace("{{FOOTER}}", mono(m.get("footer", ""))))

    with open(out_path, "w") as f:
        f.write(out)
    print(f"wrote {out_path} ({len(out)} bytes, {len(m['cards'])} cards)")


if __name__ == "__main__":
    main()
