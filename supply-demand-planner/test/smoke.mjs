// Headless browser smoke test against standalone.html (run `npm run build` first).
// Needs Playwright with Chromium available: npx playwright install chromium
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";
const here = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
const errors = [];
page.on("console", (m) => { if (m.type() === "error" && !/ERR_CONNECTION|fonts|net::/.test(m.text())) errors.push(m.text().slice(0, 300)); });
page.on("pageerror", (e) => errors.push("pageerror: " + e.message));
const fail = (msg) => { console.error("FAIL:", msg); process.exitCode = 1; };
const expect = (cond, msg) => (cond ? console.log("ok  ", msg) : fail(msg));

await page.goto("file://" + path.resolve(here, "..", "standalone.html"));
await page.evaluate(() => localStorage.clear()); await page.reload();
await page.waitForSelector(".sdp"); await page.waitForTimeout(600);

expect(!!(await page.$(".stamp")), "default ask (1 lift + 3 heavy trays) returns a date");
expect((await page.$$(".kpi")).length === 4, "four KPI tiles");

await page.fill(".who", "Test Planner");
await page.fill(".hold-name", "Acme"); await page.click("text=Place soft hold"); await page.waitForTimeout(250);
expect((await page.$$("tr.proposed")).length === 1, "soft hold lands on the calendar as proposed");
await page.click(".queue-item >> text=Accept"); await page.waitForTimeout(200);
expect((await page.$$("tr.proposed")).length === 0, "planner can accept from the review queue");

await page.fill("#ql", "3"); await page.waitForTimeout(250);
expect(/Not in this plan/.test(await page.textContent(".verdict")), "oversized ask explains the existing shortfall");
await page.fill("#ql", "1");

const cells = await page.$$("tr.num input.cellin"); await cells[0].fill("9"); await page.waitForTimeout(250);
expect(!!(await page.$(".draft-dot")), "editing a build cell creates a draft");
expect(await page.$eval("text=Approve as Jeff → new version", (b) => b.disabled), "approval is blocked until the checklist passes");
await page.click("text=Mark supply inputs keyed"); await page.selectOption("#reason", "strategic"); await page.fill(".consensus input", "Q4 2026: 20 SL / 60 HT / 16 LT");
await page.click("text=Supply detail rows"); await page.waitForTimeout(200);
for (const inp of await page.$$("tr.supply input.cellin[placeholder='–']")) await inp.fill("2");
const ack = await page.$("text=Acknowledge (leadership)"); if (ack) await ack.click();
await page.waitForTimeout(250);
expect(!(await page.$eval("text=Approve as Jeff → new version", (b) => b.disabled)), "approval unblocks once every checklist item passes");
await page.click("text=Approve as Jeff → new version"); await page.waitForTimeout(250);
expect(/P-\d{4}-\d{2}-\d{2}/.test(await page.textContent(".chip")), "approving mints a dated plan version");
expect((await page.$$(".versions li")).length === 2, "superseded plan kept in version history");

await page.click("text=+ Add deployment"); await page.waitForTimeout(150);
await page.fill(".modal input[placeholder='Customer or placeholder name']", "Rivian"); await page.click(".modal >> text=Save"); await page.waitForTimeout(200);
await page.reload(); await page.waitForSelector(".sdp"); await page.waitForTimeout(400);
expect((await page.textContent("table.grid")).includes("Rivian"), "state survives reload");

await page.click("text=Next 8 wks"); await page.waitForTimeout(150);
expect((await page.$$("table.grid thead th")).length < 15, "focus window narrows the grid");

expect(errors.length === 0, "no page errors" + (errors.length ? " — " + errors.join(" | ") : ""));
await browser.close();
