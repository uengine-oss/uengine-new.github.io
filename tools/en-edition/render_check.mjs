// Render the built English pages in a real browser and report any Korean a visitor would actually see.
//   node render_check.mjs en/index.html en/contents/processgpt.html ...
// Prints, per page: count of Korean characters in visible text + the first few offending snippets.
import { chromium } from '@playwright/test';

const BASE = process.env.SITE_URL || 'http://127.0.0.1:8777';
const pages = process.argv.slice(2);
const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, locale: 'en-US' });
const page = await ctx.newPage();
let grand = 0;

for (const p of pages) {
    let visible = '';
    try {
        await page.goto(`${BASE}/${p}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
        await page.waitForTimeout(2500);
        // innerText only returns rendered text, so hidden/commented markup is excluded by construction.
        visible = await page.evaluate(() => document.body.innerText);
    } catch (e) {
        console.log(`${p}: LOAD ERROR ${e.message.slice(0, 120)}`);
        continue;
    }
    const hits = visible.match(/[^\n]*[가-힣][^\n]*/g) || [];
    const n = (visible.match(/[가-힣]/g) || []).length;
    grand += n;
    console.log(`${p}: ${n} Korean chars visible${hits.length ? '' : ' — clean'}`);
    for (const h of hits.slice(0, 5)) console.log(`    ${h.trim().slice(0, 110)}`);
}
console.log(`TOTAL visible Korean across ${pages.length} pages: ${grand}`);
await browser.close();
