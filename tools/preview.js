// Preview: node tools/preview.js designs/<c>/kaart.html designs/<c>/preview.png [--guides] [Naam ...]
// Rendert de kaart per naam op 794x559 (A5 liggend @96dpi) met beige papier-preview
// (#e9ddc5, enkel preview!) en een stippellijn op de plooi. --guides toont ook de 8 mm veilige zone.
// Default namen: Christine Jef. Alle namen worden onder elkaar gezet in één PNG (2x schaal).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const args = process.argv.slice(2);
  const [htmlPath, outPath] = args;
  const guides = args.includes('--guides');
  let names = args.slice(2).filter(a => a !== '--guides');
  if (!names.length) names = ['Christine', 'Jef'];
  const tpl = fs.readFileSync(htmlPath, 'utf8');
  const dir = path.dirname(path.resolve(htmlPath));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 559 }, deviceScaleFactor: 2 });
  const shots = [];
  for (const n of names) {
    const tmp = path.join(dir, `.preview-${process.pid}.html`);
    fs.writeFileSync(tmp, tpl.split('{{naam}}').join(n));
    await page.goto('file://' + tmp);
    await page.evaluate(() => document.fonts.ready);
    await page.addStyleTag({ content: `html{background:#e9ddc5 !important}` });
    await page.evaluate((guides) => {
      const o = document.createElement('div');
      o.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:99999';
      o.innerHTML = `<div style="position:absolute;left:0;right:0;top:279.5px;border-top:1px dashed rgba(0,0,0,.25)"></div>` +
        (guides ? `<div style="position:absolute;left:32px;right:32px;top:32px;height:215.5px;outline:1px solid rgba(255,0,0,.5)"></div>
                   <div style="position:absolute;left:32px;right:32px;top:311.5px;height:215.5px;outline:1px solid rgba(255,0,0,.5)"></div>` : '');
      document.body.appendChild(o);
    }, guides);
    shots.push((await page.screenshot({ fullPage: false })).toString('base64'));
    fs.unlinkSync(tmp);
  }
  const p2 = await browser.newPage({ viewport: { width: 794 + 40, height: 100 }, deviceScaleFactor: 2 });
  await p2.setContent(`<body style="margin:0;padding:20px;background:#8a8478;display:flex;flex-direction:column;gap:20px">` +
    shots.map(s => `<img src="data:image/png;base64,${s}" style="width:794px;height:559px;box-shadow:0 2px 8px rgba(0,0,0,.35)">`).join('') + `</body>`);
  await p2.screenshot({ path: outPath, fullPage: true });
  await browser.close();
  console.log('preview ->', outPath);
})();
