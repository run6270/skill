#!/usr/bin/env node
/* Render an A4 one-page HTML report to PDF and check likely single-page layout. */

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

function usage() {
  console.error("Usage: render_one_pager_pdf.js input.html output.pdf [--allow-overflow]");
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    usage();
    process.exit(2);
  }

  const input = path.resolve(args[0]);
  const output = path.resolve(args[1]);
  const allowOverflow = args.includes("--allow-overflow");

  if (!fs.existsSync(input)) {
    console.error(`[ERROR] Missing HTML file: ${input}`);
    process.exit(2);
  }

  let chromium;
  try {
    ({ chromium } = require("playwright"));
  } catch (error) {
    console.error("[ERROR] Missing dependency: playwright. Use the Codex bundled Node runtime or install playwright.");
    process.exit(2);
  }

  fs.mkdirSync(path.dirname(output), { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1 });
  await page.goto(`file://${input}`, { waitUntil: "networkidle" });
  const metrics = await page.evaluate(() => {
    const pageEl = document.querySelector(".page") || document.body;
    const rect = pageEl.getBoundingClientRect();
    return {
      bodyScrollHeight: document.body.scrollHeight,
      viewportHeight: window.innerHeight,
      pageHeight: rect.height,
      pageScrollHeight: pageEl.scrollHeight,
    };
  });

  const maxHeight = 1126;
  if (!allowOverflow && (metrics.bodyScrollHeight > maxHeight || metrics.pageScrollHeight > maxHeight)) {
    await browser.close();
    console.error(`[ERROR] HTML likely overflows one A4 page: ${JSON.stringify(metrics)}`);
    process.exit(3);
  }

  await page.pdf({
    path: output,
    format: "A4",
    printBackground: true,
    margin: { top: "0mm", right: "0mm", bottom: "0mm", left: "0mm" },
    preferCSSPageSize: true,
  });
  await browser.close();

  const check = spawnSync("python3", ["-c", [
    "from pypdf import PdfReader",
    "import sys",
    "p=sys.argv[1]",
    "print(len(PdfReader(p).pages))",
  ].join(";"), output], { encoding: "utf-8" });

  if (check.status === 0) {
    const pages = Number((check.stdout || "").trim());
    if (!allowOverflow && pages !== 1) {
      console.error(`[ERROR] PDF is ${pages} pages, expected 1: ${output}`);
      process.exit(4);
    }
    console.log(`${output} (${pages} page${pages === 1 ? "" : "s"})`);
  } else {
    console.log(`${output} (created; page-count check skipped because pypdf is unavailable)`);
  }
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
