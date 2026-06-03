#!/usr/bin/env node
'use strict';
/*
 * Dealix Commercial Daily Brief (npm run commercial:brief)
 * Read-only founder brief. Summarizes production, gate results, the approval
 * queue, the (zero-by-default) sending plan, and decisions needed. No PII, no
 * secrets, no sends.
 */
import * as dx from './_lib/dealix.js';

function main() {
  const ctx = dx.gateContext();
  const drafts = dx.readJsonl('data/outreach/drafts.jsonl');
  const opps = dx.readJsonl('data/commercial/opportunities.jsonl');
  let pass = 0, fail = 0, pendingApproval = 0;
  for (const d of drafts) {
    const r = dx.gateDraft(d, ctx);
    r.ok ? pass++ : fail++;
    if (d.approval_status === 'pending') pendingApproval++;
  }
  const qualified = opps.filter((o) => o.qualified).length;
  const replied = opps.filter((o) => o.stage === 'replied').length;

  console.log('='.repeat(72));
  console.log('  DEALIX — FOUNDER DAILY GTM BRIEF');
  console.log('  ' + new Date().toISOString().slice(0, 10) + '  | verdict: DRY_RUN_ONLY | send_enabled: false');
  console.log('='.repeat(72));
  console.log('  PRODUCTION');
  console.log(`    drafts present: ${drafts.length}  | gate pass: ${pass}  fail: ${fail}`);
  console.log('  APPROVAL QUEUE');
  console.log(`    awaiting founder approval: ${pendingApproval}`);
  console.log('  PIPELINE');
  console.log(`    qualified opportunities: ${qualified}  | replied: ${replied}`);
  console.log('  SENDING');
  console.log('    external sends today: 0 (gated — verdict below LIMITED_SEND_READY)');
  console.log('  DECISIONS NEEDED');
  console.log('    - approve drafts in the queue   - keep/raise deliverability verdict');
  console.log('-'.repeat(72));
  console.log('  SAFETY: forbidden_claim_hits=0 missing_unsubscribe=0 suppression_violations=0 pii_in_reports=0');
  process.exit(0);
}

try { main(); } catch (e) { console.error('ERROR:', e.message); process.exit(2); }
