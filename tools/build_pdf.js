// node tools/build_pdf.js designs/<concept>/kaart.html
// -> print/naamkaartjes.pdf (1 A5-pagina per gast, volgorde gasten.csv) en print/testvel.pdf (1 kaartje).
// Elke kaart wordt apart met Playwright page.pdf (210x148 mm, printBackground:false) gerenderd
// en daarna met pdfunite samengevoegd, zodat het template exact zoals ontworpen wordt gebruikt.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), os = require('os');
const { execFileSync } = require('child_process');
const root = path.join(__dirname, '..');
const tplPath = path.resolve(process.argv[2]);
const tpl = fs.readFileSync(tplPath, 'utf8');
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const names = fs.readFileSync(path.join(root, 'gasten.csv'), 'utf8').normalize('NFC')
  .split(/\r?\n/).slice(1).map(s => s.trim()).filter(Boolean);
(async () => {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'kaart-'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 559 } });
  const parts = [];
  for (const [i, n] of names.entries()) {
    const html = path.join(path.dirname(tplPath), `.build-${process.pid}.html`);
    fs.writeFileSync(html, tpl.split('{{naam}}').join(esc(n)));
    await page.goto('file://' + html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const bad = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'error').map(f => f.family));
    if (bad.length) throw new Error(`font laadt niet (${n}): ${bad}`);
    const out = path.join(tmpDir, String(i).padStart(3, '0') + '.pdf');
    await page.pdf({ path: out, width: '210mm', height: '148mm', printBackground: false, margin: { top: 0, right: 0, bottom: 0, left: 0 }, pageRanges: '1' });
    fs.unlinkSync(html); parts.push(out);
  }
  await browser.close();
  fs.mkdirSync(path.join(root, 'print'), { recursive: true });
  execFileSync('pdfunite', [...parts, path.join(root, 'print/naamkaartjes.pdf')]);
  fs.copyFileSync(parts[names.indexOf('Christine') >= 0 ? names.indexOf('Christine') : 0], path.join(root, 'print/testvel.pdf'));
  console.log(`print/naamkaartjes.pdf: ${parts.length} pagina's; print/testvel.pdf: 1 pagina`);
})();
