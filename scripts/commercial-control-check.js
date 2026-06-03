#!/usr/bin/env node
/**
 * Dealix — Commercial Control Check  (npm run commercial:check)
 *
 * The commercial control-room safety gate. Verifies the invariants that keep
 * Dealix from behaving like a spam tool:
 *
 *   1. External sending is disabled (dry-run by default).
 *   2. Every queued outreach item is approval-gated (nothing auto-sent).
 *   3. No queued recipient is on the suppression list.
 *   4. Every draft clears the quality gate (no critical failures).
 *   5. The AI action ledger contains no executed-but-unapproved action.
 *
 * Read-only. Exits non-zero (BLOCKED) if any invariant is violated.
 */

import {
  SEND_ENABLED,
  DRY_RUN,
  loadOutreachQueue,
  loadApprovalQueue,
  loadLedger,
  loadSuppressionList,
  knownOfferKeywords,
  evaluateDraft,
  isSuppressed,
  printHeader,
  hr,
  today,
} from "./lib/commercial.js";

function main() {
  printHeader(`DEALIX COMMERCIAL CONTROL CHECK — ${today()}`);

  const blockers = [];
  const notes = [];

  // 1. External sending disabled
  if (SEND_ENABLED) {
    blockers.push("External sending is ENABLED (DEALIX_SEND_ENABLED=true). Disable it.");
  } else {
    console.log("  [1] External sending ............. ✅ disabled (dry-run)");
  }

  // 2. Every queued outreach item is approval-gated
  const { queue = [] } = loadOutreachQueue();
  const notGated = queue.filter(
    (d) => !["pending_approval", "draft", "needs_review"].includes(d.status ?? ""),
  );
  if (notGated.length > 0) {
    blockers.push(
      `${notGated.length} outreach item(s) are not approval-gated: ${notGated
        .map((d) => d.id)
        .join(", ")}`,
    );
  } else {
    console.log(`  [2] Outreach approval-gating ..... ✅ ${queue.length} item(s) all gated`);
  }

  // 3. Suppression honored
  const suppression = loadSuppressionList();
  const suppressedHits = queue
    .map((d) => ({ d, hit: isSuppressed(d, suppression) }))
    .filter((x) => x.hit);
  if (suppressedHits.length > 0) {
    blockers.push(
      `${suppressedHits.length} queued recipient(s) are on the suppression list: ${suppressedHits
        .map((x) => x.d.company)
        .join(", ")}`,
    );
  } else {
    console.log("  [3] Suppression list ............. ✅ no queued recipient suppressed");
  }

  // 4. Quality gate
  const offerKeywords = knownOfferKeywords();
  const results = queue.map((d) => evaluateDraft(d, { suppression, offerKeywords }));
  const criticalDrafts = results.filter((r) =>
    r.failures.some((f) => f.severity === "CRITICAL"),
  );
  if (criticalDrafts.length > 0) {
    blockers.push(
      `${criticalDrafts.length} draft(s) have CRITICAL quality failures (run commercial:quality)`,
    );
  } else {
    console.log(`  [4] Draft quality gate ........... ✅ ${results.length} draft(s), 0 critical`);
  }

  // 5. Ledger: no executed-but-unapproved action that required approval
  const ledger = loadLedger();
  const unapprovedActions = ledger.filter(
    (e) => e.requires_approval === true && e.approved !== true,
  );
  // These are expected to sit awaiting approval — only a violation if marked done/sent.
  const executedUnapproved = unapprovedActions.filter((e) =>
    /sent|executed|delivered/i.test(e.action ?? ""),
  );
  if (executedUnapproved.length > 0) {
    blockers.push(
      `${executedUnapproved.length} ledger action(s) were executed without approval`,
    );
  } else {
    console.log("  [5] AI action ledger ............. ✅ no executed-unapproved action");
  }

  // Informational: founder approval queue depth
  const approvals = loadApprovalQueue();
  const pending = approvals.filter((a) => a.requires_approval && !a.approved);
  const highRisk = pending.filter((a) => a.risk === "high");
  notes.push(`${pending.length} item(s) awaiting founder approval (${highRisk.length} high-risk).`);
  notes.push(`${unapprovedActions.length} ledger action(s) awaiting approval.`);

  console.log("");
  console.log(`  ${hr("-")}`);
  for (const n of notes) console.log(`  • ${n}`);
  console.log("");

  if (blockers.length > 0) {
    console.log("  CONTROL STATUS: 🔴 BLOCKED");
    for (const b of blockers) console.log(`    - ${b}`);
    console.log(hr());
    return 1;
  }

  console.log("  CONTROL STATUS: ✅ READY (dry-run; awaiting founder approval to send)");
  console.log(hr());
  return DRY_RUN ? 0 : 0;
}

process.exit(main());
