#!/usr/bin/env node
/**
 * Dealix — Commercial Daily Brief  (npm run commercial:brief)
 *
 * One-screen founder brief: pipeline snapshot, queue status, quality-gate
 * result, risks awaiting approval, and the single most important decision for
 * today. Read-only except for writing the brief markdown.
 *
 * Prints to stdout and writes company_os/war_room/COMMERCIAL_DAILY_BRIEF.md.
 */

import { writeFileSync } from "node:fs";
import { resolve } from "node:path";
import {
  ROOT,
  SEND_ENABLED,
  loadPipeline,
  loadOutreachQueue,
  loadApprovalQueue,
  loadFollowups,
  loadSuppressionList,
  knownOfferKeywords,
  evaluateDraft,
  printHeader,
  today,
} from "./lib/commercial.js";

function build() {
  const dateStr = today();
  const pipeline = loadPipeline();
  const { queue = [] } = loadOutreachQueue();
  const approvals = loadApprovalQueue();
  const { followups = [] } = loadFollowups();
  const suppression = loadSuppressionList();
  const offerKeywords = knownOfferKeywords();

  const results = queue.map((d) => evaluateDraft(d, { suppression, offerKeywords }));
  const clear = results.filter((r) => r.pass).length;
  const blocked = results.length - clear;

  const pending = approvals.filter((a) => a.requires_approval && !a.approved);
  const highRisk = pending.filter((a) => a.risk === "high");
  const dueFollowups = followups.filter(
    (f) => f.status === "scheduled" && (f.scheduled_date ?? "9999") <= dateStr,
  );

  const counts = pipeline.counts ?? {};
  const totalProspects = Object.values(counts).reduce((a, b) => a + b, 0);

  // Single most important decision
  let decision;
  if (SEND_ENABLED) {
    decision = "⚠️ External sending is ENABLED — confirm this is intended or set DEALIX_SEND_ENABLED back to false.";
  } else if (blocked > 0) {
    decision = `Fix ${blocked} draft(s) blocked by the quality gate before approving any outreach.`;
  } else if (highRisk.length > 0) {
    decision = `Review ${highRisk.length} high-risk approval item(s) (pricing / data handling).`;
  } else if (clear > 0) {
    decision = `Approve ${clear} clean draft(s) to move them from "researched" to "contacted".`;
  } else {
    decision = "Generate the next batch of outreach drafts (queue is empty).";
  }

  const lines = [];
  lines.push("# Dealix — Commercial Daily Brief");
  lines.push("");
  lines.push(`_${dateStr} · dry-run · approval-first_`);
  lines.push("");
  lines.push("## Pipeline snapshot");
  lines.push(`- Tracked prospects: **${totalProspects}**`);
  for (const stage of pipeline.pipeline_stages ?? []) {
    const c = counts[stage] ?? 0;
    if (c > 0) lines.push(`  - ${stage}: ${c}`);
  }
  lines.push("");
  lines.push("## Outbound queue");
  lines.push(`- Drafts: **${queue.length}** (clear: ${clear}, blocked: ${blocked})`);
  lines.push(`- Awaiting founder approval: **${pending.length}** (high-risk: ${highRisk.length})`);
  lines.push(`- Follow-ups due: **${dueFollowups.length}**`);
  lines.push("");
  lines.push("## Risks");
  if (highRisk.length === 0) lines.push("- No high-risk items pending.");
  for (const a of highRisk) {
    lines.push(`- **${a.id}** · ${a.company} · ${a.type} — ${a.details ?? a.draft_subject ?? ""}`);
  }
  lines.push("");
  lines.push("## One decision for today");
  lines.push(`> ${decision}`);
  lines.push("");

  return {
    markdown: lines.join("\n") + "\n",
    summary: { totalProspects, queue: queue.length, clear, blocked, pending: pending.length, highRisk: highRisk.length, dueFollowups: dueFollowups.length, decision },
  };
}

function main() {
  printHeader(`DEALIX COMMERCIAL DAILY BRIEF — ${today()}`);
  const { markdown, summary } = build();
  const outPath = resolve(ROOT, "company_os/war_room/COMMERCIAL_DAILY_BRIEF.md");
  writeFileSync(outPath, markdown, "utf-8");

  console.log(`  Pipeline: ${summary.totalProspects} prospects`);
  console.log(`  Drafts: ${summary.queue} (clear ${summary.clear} / blocked ${summary.blocked})`);
  console.log(`  Awaiting approval: ${summary.pending} (high-risk ${summary.highRisk})`);
  console.log(`  Follow-ups due: ${summary.dueFollowups}`);
  console.log("");
  console.log(`  DECISION → ${summary.decision}`);
  console.log("");
  console.log(`  Written: company_os/war_room/COMMERCIAL_DAILY_BRIEF.md`);
  return 0;
}

process.exit(main());
