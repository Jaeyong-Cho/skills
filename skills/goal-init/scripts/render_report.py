#!/usr/bin/env python3
"""
Render a report.md (written by /experiment's Publish stage) to a standalone
report.html a reader can open in a browser -- rendered markdown, not a raw
.md download. Stdlib only, no markdown dependency: the report template is
fixed (headings, key: value lines, bullet lists, **bold**, links, code),
so a small line-based converter covers it.

Usage:
  python render_report.py <report.md> [out.html]

Default out path: same directory as report.md, named report.html.
Called by /experiment's Publish stage after report.md is written.
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
  font-size: 1.05rem; line-height: 1.68; -webkit-font-smoothing: antialiased;
}
.wrap { width: 780px; max-width: 100%; margin: 0 auto; padding: 4rem 1.5rem 6rem; }
h1 {
  font-family: var(--mono); font-weight: 600; font-size: clamp(1.5rem, 3vw, 1.9rem);
  line-height: 1.3; margin: 0 0 1rem; letter-spacing: -0.01em;
}
h2 {
  font-family: var(--mono); font-weight: 600; font-size: 1.05rem; text-transform: uppercase;
  letter-spacing: 0.06em; color: var(--ink-2); margin: 2.4rem 0 1rem; padding-top: 1.4rem;
  border-top: 1px solid var(--line);
}
h2:first-of-type { margin-top: 1.6rem; }
.verdict {
  display: inline-block; font-family: var(--mono); font-size: 0.85rem; text-transform: uppercase;
  letter-spacing: 0.06em; padding: 0.35rem 0.9rem; border-radius: 20px; margin-bottom: 1.6rem;
}
.verdict.supported { color: #2f8f4e; background: rgba(47, 143, 78, 0.14); }
.verdict.refuted { color: #b3453f; background: rgba(179, 69, 63, 0.14); }
.verdict.inconclusive { color: #a3821f; background: rgba(163, 130, 31, 0.14); }
.verdict.explored { color: var(--accent); background: rgba(154, 73, 41, 0.14); }
.verdict.unknown { color: var(--muted); background: rgba(133, 129, 121, 0.14); }
p { margin: 0 0 0.9rem; }
ul { margin: 0 0 0.9rem; padding-left: 1.4rem; }
li { margin: 0 0 0.5rem; }
.kv { display: flex; gap: 0.6rem; margin: 0 0 0.4rem; font-size: 0.98rem; }
.kv .k { font-family: var(--mono); font-size: 0.85rem; color: var(--muted); flex: 0 0 auto; padding-top: 0.15rem; }
.kv .v { flex: 1; }
a { color: var(--accent); }
code { font-family: var(--mono); font-size: 0.92em; background: var(--bg); border: 1px solid var(--line); border-radius: 4px; padding: 0.1em 0.4em; }
pre { background: var(--bg); border: 1px solid var(--line); border-radius: 8px; padding: 1rem 1.2rem; overflow-x: auto; }
pre code { border: none; padding: 0; background: none; }
footer { margin-top: 3rem; padding-top: 1.4rem; border-top: 1px solid var(--line); font-family: var(--mono); font-size: 0.85rem; color: var(--muted); }
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<div class="wrap">
{body}
<footer>Rendered by <code>goal-init/scripts/render_report.py</code> from <code>report.md</code>.</footer>
</div>
</body>
</html>
"""

KV_RE = re.compile(r"^([a-z][a-z0-9_]*):\s*(.*)$")


def inline(text):
    text = html.escape(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def render(md_text):
    lines = md_text.splitlines()
    out = []
    title = "Report"
    i = 0
    ul_open = False
    in_code = False
    code_lines = []

    def close_ul():
        nonlocal ul_open
        if ul_open:
            out.append("</ul>")
            ul_open = False

    while i < len(lines):
        line = lines[i]

        if in_code:
            if line.strip().startswith("```"):
                out.append("<pre><code>" + "\n".join(html.escape(l) for l in code_lines) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                code_lines.append(line)
            i += 1
            continue

        stripped = line.strip()

        if stripped.startswith("```"):
            close_ul()
            in_code = True
            i += 1
            continue

        if not stripped:
            close_ul()
            i += 1
            continue

        m = re.match(r"^(#{1,3})\s+(.*)$", stripped)
        if m:
            close_ul()
            level = len(m.group(1))
            text = m.group(2)
            if level == 1:
                title = text
            out.append(f"<h{level}>{inline(text)}</h{level}>")
            i += 1
            continue

        vm = re.match(r"^\*\*Verdict:\*\*\s*(\w+)\s*$", stripped)
        if vm:
            close_ul()
            verdict = vm.group(1)
            cls = verdict.lower() if verdict.lower() in ("supported", "refuted", "inconclusive", "explored") else "unknown"
            out.append(f'<div class="verdict {cls}">{html.escape(verdict)}</div>')
            i += 1
            continue

        if stripped.startswith("- "):
            if not ul_open:
                out.append("<ul>")
                ul_open = True
            out.append(f"<li>{inline(stripped[2:])}</li>")
            i += 1
            continue

        kv = KV_RE.match(stripped)
        if kv:
            close_ul()
            out.append(f'<div class="kv"><span class="k">{html.escape(kv.group(1))}</span><span class="v">{inline(kv.group(2))}</span></div>')
            i += 1
            continue

        close_ul()
        out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    close_ul()
    return title, "\n".join(out)


def main():
    if len(sys.argv) < 2:
        print("usage: render_report.py <report.md> [out.html]")
        sys.exit(1)

    md_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(md_path)), "report.html")

    text = open(md_path, encoding="utf-8").read()
    title, body = render(text)
    out = TEMPLATE.format(title=html.escape(title), css=CSS, body=body)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
