#!/usr/bin/env python3
"""
Scan {slug}/ directories under a root (e.g. questions/, or the legacy
experiments/) and build a single dashboard page that links to each entry's
report and viewpoint gallery. Generic over the directory name -- callers pass
it explicitly (see /goal-init and /experiment, which both pass "questions").

Usage:
  python build_dashboard.py [experiments_dir] [out_path]

Defaults: experiments_dir="experiments", out_path="{experiments_dir}/index.html"

Per experiment (a subdirectory of experiments_dir containing report.md), reads:
  {slug}/report.md            -> hypothesis (from "# Experiment: ..." heading)
                                  and verdict (from "**Verdict:** ...")
  {slug}/report.html          -> if present (via render_report.py), the Report
                                  card link points here instead of report.md,
                                  so it opens rendered in-browser, not as a
                                  markdown file download
  {slug}/gallery/index.html   -> first embedded <img src="data:..."> as a thumbnail

A subdirectory without report.md is skipped (not yet a finished experiment). A
missing gallery/index.html just renders the card without a thumbnail and with
the Gallery link disabled — the report may still exist on its own.
"""
import sys, os, re, html

CSS = """
:root {
  --bg-page: #f6f5f1; --bg: #faf9f5; --ink: #2a2920; --ink-2: #6c675f;
  --muted: #858179; --line: #e0ddd8; --line-strong: #a8a49c; --accent: #9a4929;
  --mono: "JetBrains Mono", ui-monospace, "SF Mono", "Cascadia Code", Consolas, monospace;
  --serif: Charter, "Iowan Old Style", "Palatino Linotype", Georgia, serif;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root:where(:not([data-theme="light"])) {
    --bg-page: #191918; --bg: #262624; --ink: #e8e4dc; --ink-2: #938e87;
    --muted: #5a5955; --line: #333330; --line-strong: #636360; --accent: #d97757;
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg-page: #191918; --bg: #262624; --ink: #e8e4dc; --ink-2: #938e87;
  --muted: #5a5955; --line: #333330; --line-strong: #636360; --accent: #d97757;
  color-scheme: dark;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  background: var(--bg-page); color: var(--ink); font-family: var(--serif);
  font-size: 1.05rem; line-height: 1.65; text-align: center; -webkit-font-smoothing: antialiased;
}
.wrap { width: 1180px; max-width: 100%; margin: 0 auto; padding: 4rem 1.5rem 6rem; }
.eyebrow {
  font-family: var(--mono); font-size: 0.92rem; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--accent); margin: 0 0 0.9rem;
}
h1 {
  font-family: var(--mono); font-weight: 600; font-size: clamp(1.6rem, 3.2vw, 2.1rem);
  line-height: 1.25; margin: 0 0 0.6rem; text-wrap: balance; letter-spacing: -0.01em;
}
.dek { color: var(--ink-2); font-size: 1.05rem; max-width: 90ch; margin: 0 auto 3rem; }
.grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem; text-align: left;
}
.card {
  border: 1px solid var(--line); border-radius: 10px; background: var(--bg);
  overflow: hidden; display: flex; flex-direction: column;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}
.card:hover {
  transform: translateY(-3px); border-color: var(--line-strong);
  box-shadow: 0 12px 28px -14px rgba(0, 0, 0, 0.28);
}
.thumb { background: var(--bg-page); aspect-ratio: 16/9; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.thumb img { display: block; width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease; }
.card:hover .thumb img { transform: scale(1.035); }
.thumb .no-thumb { font-family: var(--mono); font-size: 0.82rem; color: var(--muted); }
.body { padding: 1.4rem 1.5rem 1.6rem; display: flex; flex-direction: column; gap: 0.7rem; flex: 1; }
.badge {
  align-self: flex-start; font-family: var(--mono); font-size: 0.74rem; text-transform: uppercase;
  letter-spacing: 0.06em; padding: 0.25rem 0.7rem; border-radius: 20px;
}
.badge.supported { color: #2f8f4e; background: rgba(47, 143, 78, 0.14); }
.badge.refuted { color: #b3453f; background: rgba(179, 69, 63, 0.14); }
.badge.inconclusive { color: #a3821f; background: rgba(163, 130, 31, 0.14); }
.badge.unknown { color: var(--muted); background: rgba(133, 129, 121, 0.14); }
h3 { font-family: var(--serif); font-weight: 600; font-size: 1.22rem; margin: 0; letter-spacing: -0.01em; line-height: 1.42; }
.slug { font-family: var(--mono); font-size: 0.78rem; color: var(--muted); }
.links { margin-top: auto; padding-top: 0.8rem; border-top: 1px solid var(--line); display: flex; gap: 1.3rem; font-family: var(--mono); font-size: 0.86rem; }
.links a { color: var(--accent); text-decoration: none; }
.links a::after { content: " ->"; opacity: 0.6; }
.links a:hover { text-decoration: underline; }
.links .disabled { color: var(--muted); }
.empty { border: 1px dashed var(--line-strong); border-radius: 10px; padding: 3rem 1.5rem; color: var(--ink-2); font-family: var(--mono); font-size: 0.95rem; }
.stats { display: flex; flex-wrap: wrap; gap: 1rem; margin: 0 0 3rem; text-align: left; }
.stat { flex: 1 1 140px; border: 1px solid var(--line); border-radius: 10px; background: var(--bg); padding: 1rem 1.2rem; }
.stat .n { font-family: var(--mono); font-weight: 600; font-size: 1.6rem; line-height: 1.2; }
.stat .l { font-family: var(--mono); font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); }
.stat.supported .n { color: #2f8f4e; }
.stat.refuted .n { color: #b3453f; }
.stat.inconclusive .n { color: #a3821f; }
footer { margin-top: 3.5rem; padding-top: 1.6rem; border-top: 1px solid var(--line); font-size: 0.95rem; color: var(--ink-2); }
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Experiments Dashboard</title>
<style>{css}</style>
</head>
<body>
<div class="wrap">
  <p class="eyebrow">goal-init &middot; experiments dashboard</p>
  <h1>Experiments</h1>
  <p class="dek">{dek}</p>
  {stats}
  {body}
  <footer>Regenerated by <code>goal-init/scripts/build_dashboard.py</code> &mdash; also run automatically at the end of <code>/experiment</code>.</footer>
</div>
</body>
</html>
"""


def parse_report(path):
    text = open(path, encoding="utf-8").read()
    title_m = re.search(r"^#\s*Experiment:\s*(.+)$", text, re.MULTILINE)
    verdict_m = re.search(r"\*\*Verdict:\*\*\s*(\w+)", text)
    hypothesis = title_m.group(1).strip() if title_m else "(untitled experiment)"
    verdict = verdict_m.group(1).strip() if verdict_m else "Unknown"
    return hypothesis, verdict


def first_thumbnail(gallery_index_path):
    if not os.path.exists(gallery_index_path):
        return None
    text = open(gallery_index_path, encoding="utf-8").read()
    m = re.search(r'<img[^>]+src="(data:[^"]+)"', text)
    return m.group(1) if m else None


def stats_html(verdicts, gallery_count):
    total = len(verdicts)
    counts = {"supported": 0, "refuted": 0, "inconclusive": 0, "unknown": 0}
    for v in verdicts:
        key = v.lower() if v.lower() in counts else "unknown"
        counts[key] += 1

    items = [("Experiments", total, "")]
    for key, label in (("supported", "Supported"), ("refuted", "Refuted"), ("inconclusive", "Inconclusive")):
        if counts[key]:
            items.append((label, counts[key], key))
    items.append(("With gallery", f"{gallery_count}/{total}", ""))

    stats = "".join(
        f'<div class="stat {cls}"><div class="n">{html.escape(str(n))}</div><div class="l">{html.escape(label)}</div></div>'
        for label, n, cls in items
    )
    return f'<div class="stats">{stats}</div>'


def card_html(slug, hypothesis, verdict, thumb, has_gallery, has_report_html):
    badge_class = verdict.lower() if verdict.lower() in ("supported", "refuted", "inconclusive") else "unknown"
    thumb_html = (
        f'<img src="{thumb}" alt="{html.escape(slug)} preview" loading="lazy">'
        if thumb else '<span class="no-thumb">no gallery yet</span>'
    )
    gallery_link = (
        f'<a href="{html.escape(slug)}/gallery/index.html">Gallery</a>'
        if has_gallery else '<span class="disabled">Gallery</span>'
    )
    report_href = f"{html.escape(slug)}/report.html" if has_report_html else f"{html.escape(slug)}/report.md"
    return f'''
    <article class="card">
      <div class="thumb">{thumb_html}</div>
      <div class="body">
        <span class="badge {badge_class}">{html.escape(verdict)}</span>
        <h3>{html.escape(hypothesis)}</h3>
        <div class="slug">{html.escape(slug)}</div>
        <div class="links"><a href="{report_href}">Report</a>{gallery_link}</div>
      </div>
    </article>'''


def main():
    experiments_dir = sys.argv[1] if len(sys.argv) > 1 else "experiments"
    out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(experiments_dir, "index.html")

    slugs = []
    if os.path.isdir(experiments_dir):
        slugs = sorted(
            d for d in os.listdir(experiments_dir)
            if os.path.isdir(os.path.join(experiments_dir, d))
            and os.path.exists(os.path.join(experiments_dir, d, "report.md"))
        )

    cards = []
    verdicts = []
    gallery_count = 0
    for slug in slugs:
        base = os.path.join(experiments_dir, slug)
        hypothesis, verdict = parse_report(os.path.join(base, "report.md"))
        gallery_index = os.path.join(base, "gallery", "index.html")
        has_gallery = os.path.exists(gallery_index)
        has_report_html = os.path.exists(os.path.join(base, "report.html"))
        thumb = first_thumbnail(gallery_index)
        cards.append(card_html(slug, hypothesis, verdict, thumb, has_gallery, has_report_html))
        verdicts.append(verdict)
        gallery_count += 1 if has_gallery else 0

    if cards:
        dek = f"{len(cards)} experiment{'s' if len(cards) != 1 else ''} run so far, newest verdicts and viewpoint galleries below."
        stats = stats_html(verdicts, gallery_count)
        body = f'<div class="grid">{"".join(cards)}</div>'
    else:
        dek = "No experiments yet."
        stats = ""
        body = '<div class="empty">Run <code>/experiment</code> to produce the first one.</div>'

    out = TEMPLATE.format(css=CSS, dek=html.escape(dek), stats=stats, body=body)

    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"wrote {out_path} ({len(cards)} experiments)")


if __name__ == "__main__":
    main()
