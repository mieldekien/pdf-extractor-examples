# Gedeelde briefing naamkaartjes (gelezen door alle agents)

- Gasten: `gasten.csv` (kolom `naam`, 37 namen) = enige bron van waarheid. Testnamen: Jef, Christine, Naïs.
- Drager: A5 beige karton (~#e9ddc5), liggend 210×148 mm = 794×559 px @96dpi. Plooi horizontaal op y=279.5px.
  Onderste helft (y 279.5–559) = voorkant rechtop. Bovenste helft (y 0–279.5) = achterkant, 180° gedraaid (transform: rotate(180deg)).
- GEEN achtergrond drukken (papier is beige). Geen wit. Inkt: donkergroen, olijf, donkerbruin, roestrood, zwart; max 2–3 kleuren; platte vlakken/lijnen; geen foto's, geen gradients.
- Veilige zone: alles (tekst én illustratie) ≥ 32 px (8 mm) van de randen én van de plooilijn. Per helft dus x 32–762, y 32–247.5 resp. 311.5–527.
- Contrast tekst op #e9ddc5 ≥ 4.5:1; moet in zwart-wit werken.
- Vaste lettergrootte voor alle namen: kies de grootte zodat de breedste naam (test Christine, Laetitia, Delphine, Elouise, Katleen) in de veilige zone past. Geen auto-fit per naam.
- Enkel Google Fonts, lokaal: `python3 tools/fetch_font.py "Family" "wght@400;700"` → `fonts/<slug>/font.css`; in kaart.html linken als `../../fonts/<slug>/font.css`.
- Template: `designs/<concept>/kaart.html`, één pagina, `@page{size:210mm 148mm;margin:0}`, html/body exact 794×559, overflow hidden, `{{naam}}` als placeholder (mag meermaals voorkomen). Illustraties als inline SVG.
- Preview: `node tools/preview.js designs/<c>/kaart.html designs/<c>/preview.png Christine Jef` (beige enkel in preview). Controle: `... --guides Christine Naïs Laetitia` naar /tmp.
