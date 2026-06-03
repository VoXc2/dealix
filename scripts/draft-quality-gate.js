#!/usr/bin/env node
// Dealix — Draft Quality Gate (npm run commercial:quality)
// Scores the daily 400-draft batch (Personalization 25 / Pain 20 / System fit 20
// / CTA 15 / Risk 10 / Tone 10), applies bands + hard email-gate fail conditions,
// builds the Top 100 Approval Queue, and writes the quality review.
// Exit 1 only on data-integrity errors (invalid score schema) — rejected drafts
// are expected business output, not a failure.

import fs from "node:fs";
import path from "node:path";
import {
  loadContext, evaluateBatch, today, systemName, SCORE_MAX, writeReport, REPORTS,
} from "./lib/commercial.js";

function renderReview(ctx, r) {
  const date = today();
  const pct = (n) => (r.total ? Math.round((n / r.total) * 100) : 0);
  let md = `# Daily Quality Gate Review — مراجعة بوابة الجودة اليومية
*Date: ${date} | Batch: ${r.total} drafts | Daily target: ${r.target}*

---

## 1. Score Model (out of 100)

| Criterion | Max |
|-----------|----:|
| Personalization | ${SCORE_MAX.personalization} |
| Pain clarity | ${SCORE_MAX.pain_clarity} |
| System fit | ${SCORE_MAX.system_fit} |
| CTA clarity | ${SCORE_MAX.cta_clarity} |
| Risk safety | ${SCORE_MAX.risk_safety} |
| Tone quality | ${SCORE_MAX.tone_quality} |

Bands: \`<65 rejected\` · \`65–74 needs_rewrite\` · \`75–84 approval_queue\` · \`85+ top_priority\`

---

## 2. Batch Status

| Status | Count | % |
|--------|------:|--:|
| 🟢 top_priority (85+) | ${r.counts.top_priority} | ${pct(r.counts.top_priority)}% |
| 🟡 approval_queue (75–84) | ${r.counts.approval_queue} | ${pct(r.counts.approval_queue)}% |
| 🟠 needs_rewrite (65–74) | ${r.counts.needs_rewrite} | ${pct(r.counts.needs_rewrite)}% |
| 🔴 rejected (<65 or gate fail) | ${r.counts.rejected} | ${pct(r.counts.rejected)}% |

> 400 Draft status: scored **${r.total}** of a **${r.target}/day** target.

---

## 3. Top 100 Approval Queue (${r.top100.length})

Inclusion requires: score ≥ 75 · recommended_system · Client Need Card · risk ≠ high · evidence_level · CTA.

| # | Company | System | Score | Band | Evidence |
|--:|---------|--------|------:|------|----------|
`;
  r.top100.forEach((e, i) => {
    md += `| ${i + 1} | ${e.company} | ${systemName(ctx, e.system)} | ${e.total} | ${e.band} | ${e.evidence_level} |\n`;
  });

  md += `
---

## 4. Rejections by Reason

| Reason | Count |
|--------|------:|
`;
  const reasons = Object.entries(r.rejectionReasons).sort((a, b) => b[1] - a[1]);
  if (reasons.length === 0) md += `| — | 0 |\n`;
  for (const [reason, n] of reasons) md += `| ${reason} | ${n} |\n`;

  md += `
---

## 5. Full Batch

| Draft | Company | System | Score | Status | Gate reasons |
|-------|---------|--------|------:|--------|--------------|
`;
  for (const e of r.evaluations) {
    const flag = e.status === "rejected" ? "🔴" : e.status === "top_priority" ? "🟢" : e.status === "approval_queue" ? "🟡" : "🟠";
    md += `| ${e.id} | ${e.company} | ${systemName(ctx, e.system)} | ${e.total} | ${flag} ${e.status} | ${e.gate.reasons.join(", ") || "—"} |\n`;
  }

  md += `
---

*Generated: ${date} | npm run commercial:quality*
`;
  return md;
}

function main() {
  const ctx = loadContext();
  const r = evaluateBatch(ctx);

  const reviewPath = writeReport("quality/DAILY_QUALITY_GATE_REVIEW.md", renderReview(ctx, r));

  // Machine-readable sidecar consumed by the daily plan + founder brief.
  const sidecar = {
    generated_at: today(),
    total: r.total,
    target: r.target,
    counts: r.counts,
    rejection_reasons: r.rejectionReasons,
    top_100: r.top100.map((e) => ({
      id: e.id, company: e.company, system: e.system, score: e.total, band: e.band, evidence_level: e.evidence_level,
    })),
  };
  const sidecarPath = path.join(REPORTS, "quality", "top_100_approval_queue.json");
  fs.mkdirSync(path.dirname(sidecarPath), { recursive: true });
  fs.writeFileSync(sidecarPath, JSON.stringify(sidecar, null, 2), "utf-8");

  // Print summary (governance_check.py style).
  console.log("=".repeat(72));
  console.log(`  DEALIX DRAFT QUALITY GATE — ${today()}`);
  console.log("=".repeat(72));
  console.log(`  Batch: ${r.total} / target ${r.target}`);
  console.log(`  🟢 top_priority: ${r.counts.top_priority}   🟡 approval_queue: ${r.counts.approval_queue}`);
  console.log(`  🟠 needs_rewrite: ${r.counts.needs_rewrite}   🔴 rejected: ${r.counts.rejected}`);
  console.log(`  Top 100 Approval Queue: ${r.top100.length}`);
  console.log(`  Report:  ${path.relative(process.cwd(), reviewPath)}`);
  console.log(`  Sidecar: ${path.relative(process.cwd(), sidecarPath)}`);

  const integrityErrors = r.evaluations.filter((e) => !e.scoreValid);
  if (integrityErrors.length) {
    console.log(`  🔴 DATA INTEGRITY ERRORS: ${integrityErrors.length} draft(s) with invalid scores`);
    console.log("=".repeat(72));
    process.exit(1);
  }
  console.log("  ✅ Quality gate complete (no data-integrity errors).");
  console.log("=".repeat(72));
}

main();
