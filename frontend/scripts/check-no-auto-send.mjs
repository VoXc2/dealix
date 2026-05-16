#!/usr/bin/env node
/**
 * No-auto-send guard.
 *
 * Dealix is a Governed Revenue & AI Operations Company: no UI control may
 * auto-send an external message. Every outbound action must route to the
 * Approval Center. This script greps the frontend `src` tree and fails the
 * build if any source line matches a forbidden auto-send phrase.
 *
 * Run from `frontend/`:
 *   node scripts/check-no-auto-send.mjs
 *
 * The project has no test runner configured in package.json, so this script
 * is the enforcement mechanism (a Jest/Vitest test was not added because
 * neither runner is installed).
 */

import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, extname } from "node:path";
import { fileURLToPath } from "node:url";

const SRC_DIR = join(fileURLToPath(new URL(".", import.meta.url)), "..", "src");
const EXTENSIONS = new Set([".ts", ".tsx", ".js", ".jsx"]);

// Forbidden auto-send phrases (English + Arabic).
const FORBIDDEN = /send automatically|auto-send|إرسال تلقائي|أرسل تلقائي/i;

/** @param {string} dir @param {string[]} acc */
function walk(dir, acc) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const st = statSync(full);
    if (st.isDirectory()) {
      walk(full, acc);
    } else if (EXTENSIONS.has(extname(entry))) {
      acc.push(full);
    }
  }
  return acc;
}

const violations = [];
for (const file of walk(SRC_DIR, [])) {
  const lines = readFileSync(file, "utf8").split("\n");
  lines.forEach((line, i) => {
    if (FORBIDDEN.test(line)) {
      violations.push(`${file}:${i + 1}: ${line.trim()}`);
    }
  });
}

if (violations.length > 0) {
  console.error("No-auto-send check FAILED. Forbidden auto-send phrasing found:");
  for (const v of violations) console.error("  " + v);
  console.error(
    "\nEvery outbound action must route through the Approval Center.",
  );
  process.exit(1);
}

console.log("No-auto-send check passed: no auto-send controls found in src/.");
