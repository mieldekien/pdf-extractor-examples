# De Jeftjes Academy — Instapkalender

Een zelfstandige kalender-widget voor de website (WordPress). Toont
automatisch de **eerstvolgende instapdatum**, een lijst van de volgende
instapmomenten, en een **Inschrijven**-knop die een vooringevulde e-mail
opent naar de academy.

- 📄 Eén bestand: [`kalender-embed.html`](./kalender-embed.html)
- 🔌 Geen plugin nodig — werkt in een gewoon "Custom HTML"-blok
- 🛠️ Alle instellingen staan bovenaan het bestand (data, e-mail, teksten, kleuren)
- 📱 Werkt op gsm en desktop

---

## 1. Instellingen aanpassen

Open `kalender-embed.html` en pas enkel het `CONFIG`-blok bovenaan aan:

```js
var CONFIG = {
  academy:   "De Jeftjes Academy",
  opleiding: "Onze opleiding",
  email:     "info@de-jeftjes.be",   // waar inschrijvingen naartoe gaan

  instapdata: [                       // vaste lijst, formaat JJJJ-MM-DD
    "2026-09-01",
    "2026-10-06",
    "2026-11-03"
  ],

  toonAantal:   6,                    // hoeveel volgende data tonen
  kleurPrimair: "#e8531f",            // knoppen / accenten
  kleurDonker:  "#1f2a44",            // titels
  kleurLicht:   "#fff7f3"             // achtergrond
};
```

- **Data die al voorbij zijn, verdwijnen automatisch.** De "eerstvolgende
  instapdatum" wordt telkens opnieuw berekend op basis van de dag van vandaag.
- Nieuwe data toevoegen = gewoon een regel bijzetten in `instapdata`.

---

## 2. Toevoegen aan de WordPress-site

1. Log in op het WordPress-beheer van `de-jeftjes.be`.
2. Maak een nieuwe pagina, bv. met titel **"Kalender"** (of open een
   bestaande pagina).
3. Klik op **+** om een blok toe te voegen → kies **"Custom HTML"**
   (Aangepaste HTML).
4. Open `kalender-embed.html`, kopieer **de volledige inhoud** en plak die
   in het HTML-blok.
5. Klik **Voorbeeld** om te controleren, en daarna **Publiceren**.
6. Noteer de URL van de pagina, bv. `https://www.de-jeftjes.be/wp/kalender/`.
   Die heb je nodig voor de QR-code (stap 3).

> Werkt de "Custom HTML" niet in jullie thema/pagebuilder? Dan kan de widget
> ook als aparte pagina geplaatst en via een `<iframe>` ingesloten worden —
> laat het weten, dan lever ik die variant.

---

## 3. QR-code maken (naar de kalenderpagina)

De QR-code is gewoon een afbeelding die naar de URL uit stap 2 verwijst.
Je maakt ze gratis en zonder account:

1. Ga naar een QR-generator, bv. `qr-code-generator.com` of `qrcode-monkey.com`.
2. Kies type **URL / Website**.
3. Plak de URL van je kalenderpagina, bv.
   `https://www.de-jeftjes.be/wp/kalender/`.
4. Download de QR-code als **PNG of SVG** (SVG = scherp op groot formaat, ideaal
   voor drukwerk zoals affiches en flyers).

Wie de QR-code scant, komt meteen op de kalender terecht en ziet automatisch
de eerstvolgende instapdatum met de inschrijfknop. ✅

> Tip: als de kalender-URL later verandert, moet de QR-code opnieuw gemaakt
> worden. Wil je dat vermijden, gebruik dan een "dynamische" QR-code (bij
> sommige generatoren) waarbij je de bestemming later kunt aanpassen.

---

## 4. Testen op je eigen pc (voor je het online zet)

Je hoeft niets te installeren:

1. Download het bestand `kalender-embed.html`.
2. Dubbelklik erop → het opent in je browser.
3. Je ziet de kalender precies zoals ze op de site zal verschijnen.
4. Klik op **Inschrijven** om te controleren dat je mailprogramma opent met
   een vooringevulde e-mail.

Aanpassingen maak je in dezelfde `CONFIG` bovenaan, opslaan, en de pagina
in je browser verversen.

---

## Hoe werkt "Inschrijven"?

De knop opent een vooringevulde e-mail (via `mailto:`) naar het adres uit
`CONFIG.email`, met daarin de gekozen instapdatum en velden voor naam,
telefoon en opmerking. De bezoeker hoeft enkel aan te vullen en te versturen.

Wil je later liever een echt inschrijfformulier (met velden op de pagina
zelf, of gekoppeld aan een bestaand systeem)? Dat kan als uitbreiding —
laat maar weten.
