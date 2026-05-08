#!/usr/bin/env node
/**
 * Minimal smoke: GET root HTML from Next.js dev server.
 * Usage: SMOKE_URL=http://127.0.0.1:3000 node scripts/frontend_smoke.mjs
 */
const url = process.env.SMOKE_URL || "http://127.0.0.1:3000";
fetch(url)
  .then((r) => {
    process.stdout.write(`smoke ${url} -> ${r.status}\n`);
    process.exit(r.ok ? 0 : 1);
  })
  .catch((e) => {
    process.stderr.write(`smoke failed: ${e}\n`);
    process.exit(1);
  });
