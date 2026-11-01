#!/usr/bin/env python3
"""Download a Google Font family as TTF into fonts/<slug>/ and write fonts/<slug>/font.css.

Usage: python3 tools/fetch_font.py "Family Name" "wght@400;700"   (axis spec optional)
       python3 tools/fetch_font.py "Fraunces" "ital,opsz,wght@0,9..144,400;0,9..144,900"
The CSS uses paths relative to the repo root (fonts/<slug>/...). From designs/<c>/kaart.html
reference them as ../../fonts/<slug>/<file>.ttf (or just <link> ../../fonts/<slug>/font.css).
"""
import re, sys, os, urllib.request, urllib.parse
fam = sys.argv[1]; spec = sys.argv[2] if len(sys.argv) > 2 else ""
q = fam.replace(" ", "+") + (":" + spec if spec else "")
url = f"https://fonts.googleapis.com/css2?family={q}&display=block"
css = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "curl/8"})).read().decode()
slug = re.sub(r"[^a-z0-9]+", "-", fam.lower()).strip("-")
d = os.path.join(os.path.dirname(__file__), "..", "fonts", slug); os.makedirs(d, exist_ok=True)
out = []
for block in re.findall(r"@font-face\s*{[^}]*}", css):
    style = re.search(r"font-style:\s*(\w+)", block).group(1)
    weight = re.search(r"font-weight:\s*([\d ]+)", block).group(1).strip().replace(" ", "-")
    src = re.search(r"url\(([^)]+)\)", block).group(1)
    # Google splits by unicode-range for some fonts; we only fetch latin (default UA gives full TTF)
    rng = re.search(r"unicode-range:[^;]+;", block)
    name = f"{slug}-{style}-{weight}.ttf"
    p = os.path.join(d, name)
    if not os.path.exists(p):
        urllib.request.urlretrieve(src, p)
    out.append(block.replace(src, name))
open(os.path.join(d, "font.css"), "w").write("\n".join(out) + "\n")
print(f"fonts/{slug}/font.css")
print("\n".join(sorted(os.listdir(d))))
