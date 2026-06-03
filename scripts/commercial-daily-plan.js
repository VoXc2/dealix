#!/usr/bin/env node
/**
 * Dealix — Commercial Daily Plan  (npm run commercial:plan)
 *
 * Produces today's prioritized commercial action plan from the pipeline,
 * outreach queue, follow-ups, and prospect list. Every action is a DRAFT or a
 * NEEDS-APPROVAL item — the plan never instructs an external send.
 *
 * Prints to stdout and writes company_os/war_room/COMMERCIAL_DAILY_PLAN.md.
 */

import { writeFileSync } from "node:fs";
import { resolve } from "node:path";
import {
  ROOT,
  loadOutreachQueue,
  loadApprovalQueue,
  loadFollowups,
  loadProspects,
  loadSuppressionList,
  knownOfferKeywords,
  evaluateDraft,
  printHeader,
  today,
} from "./lib/commercial.js";

function build() {
  const dateStr = today();
  const { queue = [] } = loadOutreachQueue();
  const approvals = loadApprovalQueue();
  const { followups = [] } = loadFollowups();
  const prospects = loadProspects();
  const suppression = loadSuppressionList();
  const offerKeywords = knownOfferKeywords();

  // Approvals to review (highest risk + priority first)
  const pendingApprovals = approvals
    .filter((a) => a.requires_approval && !a.approved)
    .sort((a, b) => riskRank(b.risk) - riskRank(a.risk));

  // Drafts that are clear vs blocked
  const draftResults = queue.map((d) => ({
    draft: d,
    result: evaluateDraft(d, { suppression, offerKeywords }),
  }));
  const clearDrafts = draftResults.filter((x) => x.result.pass);
  const blockedDrafts = draftResults.filter((x) => !x.result.pass);

  // Follow-ups due today or overdue
  const dueFollowups = followups.filter(
    (f) => f.status === "scheduled" && (f.scheduled_date ?? "9999") <= dateStr,
  );

  // Prospect next actions due
  const dueProspects = prospects.filter(
    (p) => p.next_action && (p.next_date ?? "9999") <= dateStr,
  );

  const lines = [];
  lines.push(`# Dealix — Commercial Daily Plan`);
  lines.push("");
  lines.push(`_Generated ${dateStr}. Dry-run. Drafts only — every external action requires founder approval._`);
  lines.push("");

  lines.push(`## 1. Approvals to review (${pendingApprovals.length})`);
  if (pendingApprovals.length === 0) lines.push("- _None pending._");
  for (const a of pendingApprovals) {
    lines.push(`- **[${a.risk?.toUpperCase() ?? "?"}]** ${a.id} · ${a.company} · ${a.type}`);
  }
  lines.push("");

  lines.push(`## 2. Drafts ready for approval (${clearDrafts.length})`);
  if (clearDrafts.length === 0) lines.push("- _None._");
  for (const { draft } of clearDrafts) {
    lines.push(`- ${draft.id} · ${draft.company} · "${draft.draft_subject}" — _needs approval before send_`);
  }
  lines.push("");

  if (blockedDrafts.length > 0) {
    lines.push(`## 3. Drafts blocked by the quality gate (${blockedDrafts.length})`);
    for (const { draft, result } of blockedDrafts) {
      const codes = result.failures.map((f) => f.code).join(", ");
      lines.push(`- ${draft.id} · ${draft.company} — fix: ${codes}`);
    }
    lines.push("");
  }

  lines.push(`## 4. Follow-ups due (${dueFollowups.length})`);
  if (dueFollowups.length === 0) lines.push("- _None due._");
  for (const f of dueFollowups) {
    lines.push(`- ${f.id} · ${f.company} · seq ${f.sequence} (${f.scheduled_date}) — _draft, needs approval_`);
  }
  lines.push("");

  lines.push(`## 5. Prospect next actions due (${dueProspects.length})`);
  if (dueProspects.length === 0) lines.push("- _None due._");
  for (const p of dueProspects.slice(0, 20)) {
    lines.push(`- ${p.company} · ${p.next_action} (${p.next_date})`);
  }
  lines.push("");

  return { dateStr, markdown: lines.join("\n") + "\n", counts: {
    approvals: pendingApprovals.length,
    clearDrafts: clearDrafts.length,
    blockedDrafts: blockedDrafts.length,
    followups: dueFollowups.length,
    prospects: dueProspects.length,
  } };
}

function riskRank(risk) {
  return { high: 3, medium: 2, low: 1 }[risk] ?? 0;
}

function main() {
  printHeader(`DEALIX COMMERCIAL DAILY PLAN — ${today()}`);
  const { markdown, counts } = build();
  const outPath = resolve(ROOT, "company_os/war_room/COMMERCIAL_DAILY_PLAN.md");
  writeFileSync(outPath, markdown, "utf-8");

  console.log(`  Approvals to review .......... ${counts.approvals}`);
  console.log(`  Drafts ready for approval .... ${counts.clearDrafts}`);
  console.log(`  Drafts blocked by gate ....... ${counts.blockedDrafts}`);
  console.log(`  Follow-ups due ............... ${counts.followups}`);
  console.log(`  Prospect actions due ......... ${counts.prospects}`);
  console.log("");
  console.log(`  Written: company_os/war_room/COMMERCIAL_DAILY_PLAN.md`);
  return 0;
}

process.exit(main());
