#!/usr/bin/env node
// build.js — copies index.html into dist for Netlify publish.
// Run: node scripts/build.js  (or via `netlify build`)

import { copyFileSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dir = dirname(fileURLToPath(import.meta.url));
const root  = join(__dir, "..");

mkdirSync(join(root, "dist"), { recursive: true });
copyFileSync(join(root, "index.html"), join(root, "dist", "index.html"));

console.log("✅  Built dist/index.html");
