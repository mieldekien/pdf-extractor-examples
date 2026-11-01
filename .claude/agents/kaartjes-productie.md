---
name: kaartjes-productie
description: Zet het gekozen kaartdesign + gasten.csv om naar drukklare PDF's (print/naamkaartjes.pdf en print/testvel.pdf) via Playwright.
tools: Read, Write, Edit, Bash, Glob, Grep
---
Lees `.claude/brief-naamkaartjes.md`. Gebruik `tools/build_pdf.js` (of verbeter het).
- Eén A5-pagina per gast, volgorde = gasten.csv, Playwright `page.pdf({width:'210mm',height:'148mm',printBackground:false})`.
- Fonts moeten ingebed zijn (controle: `pdffonts`), geen fallback-fonts.
- Maak ook `print/testvel.pdf` (1 kaartje, eerste gast) om op gewoon papier te testen.
Wijzig het design niet inhoudelijk; enkel productie-fixes.
