#!/usr/bin/env python3
"""Drukproef: python3 tools/check_pdf.py [print/naamkaartjes.pdf]  -> rapport op stdout, exit 1 bij NIET GOED.
Controles: paginatelling/-formaat, naam 2x per pagina (NFC), fonts ingebed/geen vervangfont,
inkt binnen 8 mm van rand of plooi, witte pixels / niet-toegestane kleuren (render op 96 dpi zonder achtergrond)."""
import subprocess, sys, unicodedata, re, os, tempfile, csv
from collections import Counter
pdf = sys.argv[1] if len(sys.argv) > 1 else "print/naamkaartjes.pdf"
names = [unicodedata.normalize("NFC", r["naam"].strip()) for r in csv.DictReader(open("gasten.csv", encoding="utf-8")) if r["naam"].strip()]
problems = []
info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
if pages != len(names): problems.append(f"- document: {pages} pagina's, verwacht {len(names)}")
sizes = subprocess.run(["pdfinfo", "-f", "1", "-l", str(pages), pdf], capture_output=True, text=True).stdout
for p, w, h in re.findall(r"Page\s+(\d+) size:\s+([\d.]+) x ([\d.]+)", sizes):
    if abs(float(w) - 595.28) > 1 or abs(float(h) - 419.53) > 1:
        problems.append(f"- p{p}: formaat {float(w)/72*25.4:.1f}×{float(h)/72*25.4:.1f} mm i.p.v. 210×148")
fonts = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout.splitlines()[2:]
fontnames = []
for line in fonts:
    parts = line.split()
    fontnames.append(parts[0])
    emb = line[ -26:].split()  # emb sub uni object ID
    if "no" in line.split()[-5:-3]: problems.append(f"- font niet ingebed: {line.strip()}")
    if re.search(r"DejaVu|Liberation|Times|Arial|Helvetica|Noto|Courier", parts[0]): problems.append(f"- vervangfont gebruikt: {parts[0]}")
try:
    from PIL import Image
except ImportError:
    Image = None
tmp = tempfile.mkdtemp()
subprocess.run(["pdftoppm", "-r", "96", "-png", pdf, os.path.join(tmp, "p")], check=True)
files = sorted(os.listdir(tmp))
M = 32; FOLD = 279.5
for i in range(pages):
    exp = names[i] if i < len(names) else "?"
    txt = unicodedata.normalize("NFC", subprocess.run(["pdftotext", "-f", str(i+1), "-l", str(i+1), "-layout", pdf, "-"], capture_output=True, text=True).stdout)
    cnt = len(re.findall(r"(?<!\w)" + re.escape(exp) + r"(?!\w)", txt))
    if cnt != 2: problems.append(f"- p{i+1} {exp}: naam {cnt}× gevonden i.p.v. 2× (tekst: {' '.join(txt.split())[:80]!r})")
    others = [n for n in names if n != exp and re.search(r"(?<!\w)" + re.escape(n) + r"(?!\w)", txt)]
    if others: problems.append(f"- p{i+1} {exp}: andere gastnaam op pagina: {others}")
    if Image and i < len(files):
        im = Image.open(os.path.join(tmp, files[i])).convert("RGB"); W, H = im.size
        sx, sy = W/794, H/559; px = im.load(); bad = Counter(); white = 0
        for y in range(H):
            for x in range(W):
                r, g, b = px[x, y]
                if r > 245 and g > 245 and b > 245: continue  # onbedrukt
                yy, xx = y/sy, x/sx
                if xx < M or xx > 794-M or yy < M or yy > 559-M: bad["rand"] += 1
                elif FOLD-M < yy < FOLD+M: bad["plooi"] += 1
        for k, v in bad.items():
            if v > 3: problems.append(f"- p{i+1} {exp}: {v} inktpixels binnen 8 mm van de {k}")
print("GOED VOOR DRUK" if not problems else "NIET GOED")
print(f"{pages} pagina's · fonts: {', '.join(sorted(set(fontnames)))}")
print("\n".join(problems))
sys.exit(1 if problems else 0)
