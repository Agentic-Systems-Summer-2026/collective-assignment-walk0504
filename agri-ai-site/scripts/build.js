#!/usr/bin/env node
// build.js — reads data/results.json, writes dist/index.html
// Run: node scripts/build.js

import { readFileSync, writeFileSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dir = dirname(fileURLToPath(import.meta.url));
const root  = join(__dir, "..");

const results = JSON.parse(readFileSync(join(root, "data", "results.json"), "utf8"));

const cards = results
  .map(
    ({ title, summary, url }) => `
    <article class="card">
      <h2><a href="${url}" target="_blank" rel="noopener noreferrer">${title}</a></h2>
      <p>${summary}</p>
    </article>`
  )
  .join("\n");

const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Top 5 AI Technologies Changing Agriculture in 2026</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: system-ui, sans-serif;
      background: #f4f7f2;
      color: #1a2e14;
      min-height: 100vh;
      padding: 2rem 1rem 4rem;
    }

    header {
      text-align: center;
      margin-bottom: 2.5rem;
    }

    header h1 {
      font-size: clamp(1.6rem, 4vw, 2.4rem);
      line-height: 1.25;
      color: #2a6b2a;
    }

    header p.subtitle {
      margin-top: 0.5rem;
      color: #5a7a55;
      font-size: 1rem;
    }

    .grid {
      display: grid;
      gap: 1.25rem;
      max-width: 820px;
      margin: 0 auto;
      grid-template-columns: 1fr;
    }

    .card {
      background: #fff;
      border-radius: 10px;
      padding: 1.4rem 1.6rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.07);
      border-left: 4px solid #4caf50;
      transition: transform 0.15s, box-shadow 0.15s;
    }

    .card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 18px rgba(0,0,0,0.11);
    }

    .card h2 {
      font-size: 1.05rem;
      font-weight: 600;
      line-height: 1.4;
    }

    .card h2 a {
      color: #2a6b2a;
      text-decoration: none;
    }

    .card h2 a:hover { text-decoration: underline; }

    .card p {
      margin-top: 0.55rem;
      color: #3d5a38;
      font-size: 0.93rem;
      line-height: 1.6;
    }

    footer {
      text-align: center;
      margin-top: 3rem;
      font-size: 0.8rem;
      color: #7a9a75;
    }
  </style>
</head>
<body>
  <header>
    <h1>🌱 Top 5 AI Technologies Changing Agriculture in 2026</h1>
    <p class="subtitle">Sourced via Tavily · ${new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}</p>
  </header>

  <main class="grid">
${cards}
  </main>

  <footer>Built with AI research · Data: results.json</footer>
</body>
</html>`;

mkdirSync(join(root, "dist"), { recursive: true });
writeFileSync(join(root, "dist", "index.html"), html, "utf8");
console.log("✅  Built dist/index.html");
