#!/usr/bin/env node
// Dealix — Commercial Daily Plan (npm run commercial:plan)
// Turns the board into today's actionable plan: sales-ops board status, the call
// follow-up queue (Top 30), companies to send (Top 20), mini proposals waiting
// approval, and delivery pipelines. Writes the sales-ops reports.

import path from "node:path";
import {
  loadContext, evaluateBatch, boardSummary, callsToMake, companiesToSend,
  miniProposalsWaiting, deliveryPipelines, deliveryGate, today, systemName,
  BOARD_STATUSES, writeReport,
} from "./lib/commercial.js";

function renderBoard(ctx, summary, mps, deliveries) {
  const date = today();
  let md = `# Sales Ops Board — حالة لوحة المبيعات
*Date: ${date}*

---

## 1. Board by Stage

| Stage | Count |
|-------|------:|
`;
  for (const s of BOARD_STATUSES) md += `| ${s} | ${summary[s] || 0} |\n`;

  md += `
---

## 2. Mini Proposals Waiting Founder Approval (${mps.length})

| Opportunity | Company | System | Starter (SAR) | Timeline | Approval |
|-------------|---------|--------|--------------:|----------|----------|
`;
  if (mps.length === 0) md += `| — | — | — | — | — | — |\n`;
  for (const o of mps) {
    const m = o.mini_proposal;
    md += `| ${o.id} | ${o.company} | ${systemName(ctx, m.system)} | ${m.starter_price_sar} | ${m.timeline} | ⏳ pending_founder_approval |\n`;
  }

  md += `
> Mini proposals are **never** sent automatically — they carry price + scope and require founder approval.

---

## 3. Delivery Pipelines (${deliveries.length})

| Opportunity | Company | System | Stage | Delivery Gate |
|-------------|---------|--------|-------|---------------|
`;
  if (deliveries.length === 0) md += `| — | — | — | — | — |\n`;
  for (const o of deliveries) {
    const g = deliveryGate(o.delivery || {});
    const status = g.passed ? "✅ ready" : `🔴 blocked (${g.reasons.join(", ")})`;
    md += `| ${o.id} | ${o.company} | ${systemName(ctx, o.system)} | ${o.stage} | ${status} |\n`;
  }

  md += `
---

## 4. Owners per Opportunity

| Opportunity | Company | Stage | Email | Call | Delivery |
|-------------|---------|-------|-------|------|----------|
`;
  for (const o of ctx.board.opportunities || []) {
    const ow = o.owners || {};
    md += `| ${o.id} | ${o.company} | ${o.stage} | ${ow.email_owner || "—"} | ${ow.call_owner || "—"} | ${ow.delivery_owner || "—"} |\n`;
  }

  md += `
---

*Generated: ${date} | npm run commercial:plan*
`;
  return md;
}

function renderCallQueue(ctx, calls) {
  const date = today();
  let md = `# Call Follow-up Queue — قائمة مكالمات المتابعة
*Date: ${date} | Top ${calls.length} calls today*

---

`;
  if (calls.length === 0) md += `> لا توجد مكالمات مجدولة اليوم.\n`;
  calls.forEach((o, i) => {
    const b = o.call_brief || {};
    md += `## ${i + 1}. ${o.company} — ${systemName(ctx, o.system)} \`${o.call_priority}\`

- **Objective:** ${o.next_step || "—"}
- **Opening line:** ${b.opening_line || "—"}
- **Questions:**
${(b.questions || []).map((q) => `  - ${q}`).join("\n") || "  - —"}
- **Expected objection:** ${b.expected_objection || "—"}
- **Next step:** ${b.next_step || "—"}
- **Owner:** ${(o.owners && o.owners.call_owner) || "—"}

---

`;
  });
  md += `*Generated: ${date} | npm run commercial:plan*\n`;
  return md;
}

function main() {
  const ctx = loadContext();
  const evalResult = evaluateBatch(ctx);
  const summary = boardSummary(ctx);
  const calls = callsToMake(ctx, 30);
  const sends = companiesToSend(ctx, evalResult, 20);
  const mps = miniProposalsWaiting(ctx);
  const deliveries = deliveryPipelines(ctx);

  const boardPath = writeReport("sales_ops/SALES_OPS_BOARD_STATUS.md", renderBoard(ctx, summary, mps, deliveries));
  const callPath = writeReport("sales_ops/CALL_FOLLOWUP_QUEUE.md", renderCallQueue(ctx, calls));

  console.log("=".repeat(72));
  console.log(`  DEALIX COMMERCIAL DAILY PLAN — ${today()}`);
  console.log("=".repeat(72));
  console.log(`  Top 20 companies to send: ${sends.length}`);
  console.log(`  Top 30 calls to make:     ${calls.length}`);
  console.log(`  Mini proposals waiting:   ${mps.length}`);
  console.log(`  Delivery pipelines:       ${deliveries.length}`);
  console.log(`  Board:  ${path.relative(process.cwd(), boardPath)}`);
  console.log(`  Calls:  ${path.relative(process.cwd(), callPath)}`);
  console.log("  ✅ Daily plan complete.");
  console.log("=".repeat(72));
}

main();
