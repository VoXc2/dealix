#!/usr/bin/env node
'use strict';
/*
 * Dealix Draft Quality / Compliance Gate (npm run commercial:quality)
 * Read-only. Applies brand/claims, personalization, unsubscribe, suppression,
 * fake-thread, and required-field gates to drafts. Exits non-zero if any
 * production draft fails, so CI blocks unsafe outbound.
 *
 * Usage:
 *   node scripts/draft-quality-gate.js                 # gate data/outreach/drafts.jsonl
 *   node scripts/draft-quality-gate.js --eval          # run labeled eval cases
 */
import * as dx from './_lib/dealix.js';

function main() {
  const evalMode = process.argv.includes('--eval');
  const ctx = dx.gateContext();
  console.log('='.repeat(72));
  console.log('  DEALIX DRAFT QUALITY / COMPLIANCE GATE');
  console.log('  defaults: dry_run=true approval_required=true send_enabled=false');
  console.log('='.repeat(72));

  if (evalMode) {
    const cases = dx.readJsonl('data/evals/gtm_draft_eval_cases.jsonl');
    let mismatches = 0;
    for (const c of cases) {
      const res = dx.gateDraft(c.draft, ctx);
      const got = res.ok ? 'pass' : 'fail';
      const ok = got === c.expect && (c.expect === 'pass' || res.reasons.includes(c.reason_code));
      if (!ok) mismatches++;
      console.log(`  [${ok ? 'OK' : 'XX'}] ${c.case_id}: expected ${c.expect}/${c.reason_code || '-'} got ${got} [${res.reasons.join(',')}]`);
    }
    console.log('-'.repeat(72));
    console.log(`  eval cases: ${cases.length} | mismatches: ${mismatches}`);
    process.exit(mismatches === 0 ? 0 : 1);
  }

  const drafts = dx.readJsonl('data/outreach/drafts.jsonl');
  const byType = {};
  let failed = 0;
  for (const d of drafts) {
    byType[d.draft_type] = (byType[d.draft_type] || 0) + 1;
    const res = dx.gateDraft(d, ctx);
    if (!res.ok) { failed++; console.log(`  FAIL ${d.draft_id}: ${res.reasons.join(', ')}`); }
  }
  console.log(`  drafts checked: ${drafts.length}`);
  for (const t of Object.keys(dx.DRAFT_MIX_TARGET)) {
    console.log(`    ${t}: ${byType[t] || 0} (daily target ${dx.DRAFT_MIX_TARGET[t]})`);
  }
  console.log(`  passed: ${drafts.length - failed} | failed: ${failed}`);
  console.log(`  forbidden_claim_hits=0 enforced | personalization floor=P1 | unsubscribe required for cold`);
  process.exit(failed === 0 ? 0 : 1);
}

try { main(); } catch (e) { console.error('ERROR:', e.message); process.exit(2); }
