#!/usr/bin/env python3
"""
Albert Miles Removals — static site generator.
Reads page fragments from _fragments/*.txt and assembles full HTML pages
from the shared header/footer partials. Output is plain static HTML.

Fragment format:
  @path output/path.html          (relative to site root, e.g. services/house-removals.html)
  @title Page <title>
  @desc  Meta description
  @canonical https://example.com/path.html
  @active nav-link-id             (optional: sets aria-current, e.g. index.html)
  @schema JSON-LD block           (optional)
  @body
  ...page <main> content...
"""
import os
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
FRAG_DIR = ROOT / "_fragments"
PARTIALS = ROOT / "_partials"
OUT = ROOT

def read_partial(name):
    return (PARTIALS / name).read_text(encoding="utf-8")

HEADER = read_partial("header.html")
FOOTER = read_partial("footer.html")

BASE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<link rel="canonical" href="{{CANONICAL}}">
<meta name="robots" content="index, follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ROOT}}assets/css/style.css">
{{SCHEMA}}
</head>
<body>
"""

def parse_fragment(text):
    fields = {}
    m = re.search(r"@body\n(.*)$", text, re.S)
    body = m.group(1) if m else ""
    head = text[: m.start()] if m else text
    # meta lines come in order, last wins
    order = []
    for line in head.splitlines():
        if line.startswith("@"):
            key, _, val = line.partition(" ")
            key = key[1:].strip()
            val = val.strip()
            if key in ("schema", "body"):
                continue
            fields[key] = val
            order.append(key)
    # handle multi-line schema
    sm = re.search(r"@schema\s*(.*?)(?=\n@body|\Z)", text, re.S)
    if sm:
        fields["schema"] = sm.group(1).strip()
    fields["body"] = body
    return fields

def active_attr(fields, root):
    active = fields.get("active", "")
    if not active:
        return ""
    target = root + active
    return f' aria-current="page"'

SITE_URL = "https://www.albertmilesremovals.co.uk"
# pages not produced from fragments (handwritten), included in the sitemap
STATIC_PAGES = ["index.html", "about.html"]


def build():
    count = 0
    built = []
    for frag in sorted(FRAG_DIR.glob("*.txt")):
        fields = parse_fragment(frag.read_text(encoding="utf-8"))
        out_rel = fields.get("path")
        if not out_rel:
            print(f"SKIP {frag.name}: no @path")
            continue
        depth = len(pathlib.PurePosixPath(out_rel).parts) - 1
        root = "../" * depth
        title = fields.get("title", "Albert Miles Removals")
        desc = fields.get("desc", "Albert Miles Removals — professional house and office removals across the West Midlands.")
        canonical = fields.get("canonical", "")
        schema = fields.get("schema", "").strip()
        if schema:
            schema = "<script type=\"application/ld+json\">\n" + schema + "\n</script>"

        head = (BASE_HEAD
                .replace("{{TITLE}}", title)
                .replace("{{DESC}}", desc)
                .replace("{{CANONICAL}}", canonical)
                .replace("{{SCHEMA}}", schema)
                .replace("{{ROOT}}", root))
        header = HEADER.replace("{{ROOT}}", root)
        # mark active nav link
        active = fields.get("active", "")
        if active:
            header = re.sub(
                r'<a href="' + re.escape(root + active) + r'">',
                '<a href="' + root + active + '" aria-current="page">',
                header,
            )
        footer = FOOTER.replace("{{ROOT}}", root)

        html = head + header + "\n" + fields["body"].strip() + "\n\n" + footer
        out_path = OUT / out_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        count += 1
        built.append(out_rel)
        print(f"built {out_rel} ({len(html)} bytes)")

    # sitemap.xml
    urls = STATIC_PAGES + built
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in urls:
        lines.append(f"  <url><loc>{SITE_URL}/{u}</loc></url>")
    lines.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # robots.txt
    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        f"\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )
    (OUT / "robots.txt").write_text(robots, encoding="utf-8")

    print(f"\nDone. {count} pages generated, sitemap.xml and robots.txt written.")

if __name__ == "__main__":
    build()
