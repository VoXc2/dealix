#!/usr/bin/env node
'use strict';
/*
 * Dealix Commercial Daily Plan (npm run commercial:plan)
 * Read-only. Produces the 250/day draft-production plan and the sending batch
 * PLAN. A plan is NOT a send: planned sends are zero unless an account's
 * deliverability verdict is LIMITED_SEND_READY or better AND founder approves.
 */
import * as dx from './_lib/dealix.js';

function main() {
  const drafts = dx.readJsonl('data/outreach/drafts.jsonl');
  const accounts = dx.readJsonl('data/outreach/email_accounts.jsonl');
  const byType = {};
  for (const d of drafts) byType[d.draft_type] = (byType[d.draft_type] || 0) + 1;

  console.log('='.repeat(72));
  console.log('  DEALIX DAILY GTM PLAN  (plan only — no external send)');
  console.log('='.repeat(72));
  console.log('  1) DRAFT PRODUCTION TARGET (250/day)');
  let totalTarget = 0, totalHave = 0;
  for (const t of Object.keys(dx.DRAFT_MIX_TARGET)) {
    const have = byType[t] || 0, target = dx.DRAFT_MIX_TARGET[t];
    totalTarget += target; totalHave += have;
    console.log(`     ${t.padEnd(16)} have ${String(have).padStart(3)} / target ${String(target).padStart(3)}  gap ${Math.max(0, target - have)}`);
  }
  console.log(`     ${'TOTAL'.padEnd(16)} have ${String(totalHave).padStart(3)} / target ${String(totalTarget).padStart(3)}`);

  // Best available verdict across accounts.
  const order = ['NOT_READY', 'PAUSE_REQUIRED', 'DRY_RUN_ONLY', 'LIMITED_SEND_READY', 'RAMP_READY'];
  let best = 'NOT_READY';
  for (const a of accounts) if (order.indexOf(a.deliverability_verdict) > order.indexOf(best)) best = a.deliverability_verdict;
  const sendable = dx.SENDABLE_VERDICTS.has(best);

  console.log('\n  2) SENDING BATCH PLAN');
  console.log(`     best account verdict: ${best}`);
  console.log(`     sendable: ${sendable ? 'yes' : 'NO — verdict below LIMITED_SEND_READY'}`);
  console.log(`     planned sends today: ${sendable ? '(awaiting founder-approved ramp cap)' : 0}`);
  console.log(`     send_enabled: false (always, until founder enables a healthy account)`);

  console.log('\n  3) NEXT FOUNDER ACTIONS');
  console.log('     - review approval queue (reports/outreach/APPROVAL_QUEUE.md)');
  console.log('     - approve/keep deliverability verdict (no auto-escalation)');
  process.exit(0);
}

try { main(); } catch (e) { console.error('ERROR:', e.message); process.exit(2); }
