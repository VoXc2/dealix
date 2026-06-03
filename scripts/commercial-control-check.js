#!/usr/bin/env node
'use strict';
/*
 * Dealix Commercial Control Check (npm run commercial:check)
 * Read-only repo-wide safety gate. Verifies the non-negotiables hold across the
 * data layer. Exits non-zero on any CRITICAL violation so unsafe states block CI.
 */
import * as dx from './_lib/dealix.js';

function main() {
  const ctx = dx.gateContext();
  const critical = [];
  const warn = [];

  // 1. No mailbox may have sending enabled.
  for (const a of dx.readJsonl('data/outreach/email_accounts.jsonl')) {
    if (a.send_enabled === true) critical.push(`email account ${a.account_id} has send_enabled=true`);
  }
  // 2. Sending batches must be plan-only/dry-run unless explicitly approved with an approver.
  for (const b of dx.readJsonl('data/outreach/sending_batches.jsonl')) {
    if (b.send_enabled === true) critical.push(`batch ${b.batch_id} has send_enabled=true`);
    if (b.status !== 'approved' && b.dry_run !== true) critical.push(`batch ${b.batch_id} not approved and not dry_run`);
    if (b.status === 'approved' && !b.approved_by) critical.push(`batch ${b.batch_id} approved without approved_by`);
    if (b.planned_count > 0 && !dx.SENDABLE_VERDICTS.has(b.deliverability_verdict)) {
      critical.push(`batch ${b.batch_id} plans ${b.planned_count} sends but verdict ${b.deliverability_verdict} is not sendable`);
    }
  }
  // 3. Every production draft must pass the gate.
  for (const d of dx.readJsonl('data/outreach/drafts.jsonl')) {
    const r = dx.gateDraft(d, ctx);
    if (!r.ok) critical.push(`draft ${d.draft_id} fails gate: ${r.reasons.join(',')}`);
  }
  // 4. Outbound content carries no forbidden claims.
  for (const post of dx.readJsonl('data/content/post_ideas.jsonl')) {
    const blob = String(post.hook || '').toLowerCase();
    for (const ph of ctx.forbidden.phrases) if (ph && blob.includes(ph)) critical.push(`post ${post.idea_id} contains forbidden claim`);
  }
  // 5. Proposals: a set final_price requires founder approval.
  for (const pr of dx.readJsonl('data/commercial/proposals.jsonl')) {
    if (pr.final_price != null && pr.approval_status !== 'approved') {
      critical.push(`proposal ${pr.proposal_id} has final_price without approval`);
    }
    if (pr.includes_out_of_scope !== true) warn.push(`proposal ${pr.proposal_id} missing out-of-scope`);
  }
  // 6. Partner margins must meet the floor.
  for (const pt of dx.readJsonl('data/partners/partner_opportunities.jsonl')) {
    if (typeof pt.margin_pct === 'number' && typeof pt.min_margin_pct === 'number' && pt.margin_pct < pt.min_margin_pct) {
      critical.push(`partner ${pt.partner_id} margin ${pt.margin_pct}% below floor ${pt.min_margin_pct}%`);
    }
  }

  console.log('='.repeat(72));
  console.log('  DEALIX COMMERCIAL CONTROL CHECK');
  console.log('='.repeat(72));
  console.log(`  CRITICAL: ${critical.length} | WARN: ${warn.length}`);
  critical.forEach((m) => console.log('  [CRITICAL] ' + m));
  warn.forEach((m) => console.log('  [WARN] ' + m));
  console.log('-'.repeat(72));
  console.log('  OVERALL: ' + (critical.length === 0 ? 'COMPLIANT' : 'NON-COMPLIANT'));
  process.exit(critical.length === 0 ? 0 : 1);
}

try { main(); } catch (e) { console.error('ERROR:', e.message); process.exit(2); }
