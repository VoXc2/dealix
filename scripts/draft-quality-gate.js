#!/usr/bin/env node
/**
 * Dealix — Draft Quality Gate  (npm run commercial:quality)
 *
 * Runs every outbound draft in company_os/revenue/outreach_queue.json through
 * the commercial safety gates: no guaranteed claims, no fake Re:/Fwd: subject,
 * suppression check, offer/product mapping, approval-gating, personalization,
 * and PII hygiene.
 *
 * Read-only and dry-run. Exits non-zero if any draft has a CRITICAL failure,
 * so it can be used as a CI / pre-send gate.
 */

import {
  loadOutreachQueue,
  loadSuppressionList,
  knownOfferKeywords,
  evaluateDraft,
  printHeader,
  hr,
  today,
} from "./lib/commercial.js";

function main() {
  printHeader(`DEALIX DRAFT QUALITY GATE — ${today()}`);

  const { queue = [] } = loadOutreachQueue();
  const suppression = loadSuppressionList();
  const offerKeywords = knownOfferKeywords();

  if (queue.length === 0) {
    console.log("  No outbound drafts in the queue. Nothing to check.");
    return 0;
  }

  const results = queue.map((d) =>
    evaluateDraft(d, { suppression, offerKeywords }),
  );

  const reasonCounts = {};
  let pass = 0;
  let fail = 0;
  let criticalDrafts = 0;

  for (const r of results) {
    const tag = r.pass ? "✅ PASS" : "❌ FAIL";
    console.log(`  ${tag}  ${r.id ?? "?"}  ${r.company ?? ""}`);
    for (const f of r.failures) {
      console.log(`         ↳ [${f.severity}] ${f.code}: ${f.detail}`);
      reasonCounts[f.code] = (reasonCounts[f.code] ?? 0) + 1;
    }
    for (const w of r.warnings) {
      console.log(`         ↳ [warn] ${w.code}: ${w.detail}`);
    }
    if (r.pass) pass++;
    else fail++;
    if (r.failures.some((f) => f.severity === "CRITICAL")) criticalDrafts++;
  }

  console.log("");
  console.log(`  ${hr("-")}`);
  console.log(`  pass_count: ${pass}`);
  console.log(`  fail_count: ${fail}`);
  console.log(`  drafts_with_critical: ${criticalDrafts}`);

  const topReasons = Object.entries(reasonCounts).sort((a, b) => b[1] - a[1]);
  if (topReasons.length > 0) {
    console.log("");
    console.log("  Top rejection reasons:");
    for (const [code, count] of topReasons) {
      console.log(`    - ${code}: ${count}`);
    }
  }

  console.log("");
  if (criticalDrafts > 0) {
    console.log("  GATE STATUS: 🔴 BLOCKED — critical failures must be fixed before approval.");
  } else if (fail > 0) {
    console.log("  GATE STATUS: 🟠 REVIEW — non-critical issues to resolve.");
  } else {
    console.log("  GATE STATUS: ✅ CLEAR — all drafts passed (still require founder approval to send).");
  }
  console.log(hr());

  return criticalDrafts > 0 ? 1 : 0;
}

process.exit(main());
