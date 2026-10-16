/*
 * Browsertest für Lernseiten
 * --------------------------
 * Lädt die Seite in einem echten Browser, spielt einen Bearbeitungsplan durch und
 * meldet, was dabei herauskommt. Prüft nebenbei auf JavaScript-Fehler und auf
 * horizontales Scrollen bei 768 px.
 *
 *   node test.js seite.html plan.json
 *
 * plan.json: Liste von Schritten, je Schritt
 *   { "karte":"k1",
 *     "stufe":"g",                                  (optional, nur bei Niveaustufen)
 *     "felder":{"z1":"5","z2":"-3"},
 *     "mc":{"mc1-wahl":"exakter Optionstext"},      (Text muss die Option eindeutig treffen)
 *     "wf":{"#k2":["wahr","falsch","wahr"]},
 *     "klick":["button[onclick=\"pruefeK1()\"]"],
 *     "zeige":["#fb1"] }
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const datei = process.argv[2];
  const plan = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const seite = await (await browser.newContext({ viewport: { width: 768, height: 1000 } })).newPage();
  const fehler = [];
  seite.on('pageerror', e => fehler.push(e.message));

  await seite.goto('file://' + path.resolve(datei));
  await seite.waitForTimeout(400);

  for (const s of plan) {
    if (s.karte) { await seite.click(`.tab[data-ziel="${s.karte}"]`); await seite.waitForTimeout(120); }
    if (s.stufe) {
      await seite.click(`.stufen-wahl[data-karte="${s.karte}"] .stufe-btn[data-s="${s.stufe}"]`);
      await seite.waitForTimeout(120);
    }
    for (const [id, wert] of Object.entries(s.felder || {})) await seite.fill('#' + id, wert);
    for (const [wrap, text] of Object.entries(s.mc || {})) {
      await seite.evaluate(([w, t]) => {
        const bs = [...document.querySelectorAll('#' + w + ' button')];
        const treffer = bs.filter(b => b.textContent.trim() === t.trim())[0]
                     || bs.filter(b => b.textContent.includes(t))[0];
        if (!treffer) throw new Error('Option nicht gefunden in ' + w + ': ' + t
                                      + ' | vorhanden: ' + bs.map(b => b.textContent).join(' || '));
        treffer.click();
      }, [wrap, text]);
    }
    for (const [scope, werte] of Object.entries(s.wf || {})) {
      await seite.evaluate(([sc, w]) => {
        document.querySelectorAll(sc + ' [data-aussage]').forEach((box, i) => {
          const b = [...box.querySelectorAll('.wf-buttons button')].find(x => x.dataset.w === w[i]);
          if (b) b.click();
        });
      }, [scope, werte]);
    }
    for (const sel of s.klick || []) await seite.click(sel);
    await seite.waitForTimeout(180);
    for (const z of s.zeige || []) {
      const t = await seite.$eval(z, e => e.className + ' | ' + e.textContent.trim().slice(0, 60));
      console.log('   ' + z + ': ' + t);
    }
  }

  const marken = await seite.evaluate(() =>
    [...document.querySelectorAll('.tab .done')].map(e => e.textContent || '–'));
  const ueberlauf = await seite.evaluate(() =>
    document.documentElement.scrollWidth - document.documentElement.clientWidth);
  console.log('   Fortschrittsmarken:', JSON.stringify(marken));
  console.log('   horizontales Scrollen bei 768 px:', ueberlauf);
  console.log('   JavaScript-Fehler:', fehler);
  await browser.close();
  process.exit(fehler.length || ueberlauf > 0 ? 1 : 0);
})();
