#!/usr/bin/env node
// Dealix — Founder Daily Super Command (npm run commercial:brief)
// The assemble-and-publish step. Builds the founder's single daily command doc
// (all 13 required sections), the weekly board review, and publishes the Focus 5
// content queue + partner pipeline. Pure derivation from company_os/commercial/*.

import path from "node:path";
import {
  loadContext, evaluateBatch, runControlChecks, boardSummary, callsToMake,
  companiesToSend, miniProposalsWaiting, deliveryPipelines, deliveryGate,
  bestSystem, recommendSystem, today, systemName,
  REQUIRED_SUPER_COMMAND_SECTIONS, BOARD_STATUSES, writeReport,
} from "./lib/commercial.js";

function bestSector(ctx, evalResult) {
  const counts = {};
  for (const e of evalResult.top100) {
    const sys = ctx.systemById[e.system];
    const seg = sys && sys.target_segments && sys.target_segments[0];
    if (seg) counts[seg] = (counts[seg] || 0) + 1;
  }
  const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
  return sorted.length ? { sector: sorted[0][0], count: sorted[0][1] } : { sector: "—", count: 0 };
}

function criticalDecision(ctx, evalResult) {
  // Most-represented system among top_priority drafts → approve its batch first.
  const counts = {};
  for (const e of evalResult.evaluations) {
    if (e.status === "top_priority") counts[e.system] = (counts[e.system] || 0) + 1;
  }
  const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
  if (!sorted.length) return "لا توجد drafts بأولوية قصوى اليوم — راجع جودة الدفعة قبل الإرسال.";
  const [sys, n] = sorted[0];
  const sec = bestSector(ctx, evalResult).sector;
  return `اعتمد ${n} draft(s) من ${systemName(ctx, sys)} الموجهة لقطاع ${sec}، لأنها الأعلى وضوحًا في الألم والأقل تعقيدًا في التسليم اليوم.`;
}

function biggestRisk(ctx, evalResult, control) {
  if (control.critical.length) return `🔴 ${control.critical.length} مخالفة حرجة في بوابة التحكم — أوقف الإرسال حتى تُحل.`;
  const rejPct = evalResult.total ? Math.round((evalResult.counts.rejected / evalResult.total) * 100) : 0;
  const blocked = deliveryPipelines(ctx).filter((o) => !deliveryGate(o.delivery || {}).passed);
  if (blocked.length) return `🟠 ${blocked.length} تسليم بدون متطلبات مكتملة (delivery_blocked).`;
  if (rejPct >= 50) return `🟠 ${rejPct}% من الدفعة مرفوضة — جودة الكتابة تحتاج تحسينًا قبل التوسع.`;
  const bs = bestSystem(evalResult);
  if (bs.count && bs.count >= Math.ceil(evalResult.top100.length * 0.6))
    return `🟡 تركّز Top 100 في نظام واحد (${systemName(ctx, bs.system)}) — خطر تركيز القطاع.`;
  return "🟢 لا مخاطر حرجة اليوم — حافظ على الإيقاع.";
}

function renderSuperCommand(ctx, data) {
  const { evalResult, control, calls, sends, mps, deliveries, summary } = data;
  const date = today();
  const bs = bestSystem(evalResult);
  const sec = bestSector(ctx, evalResult);
  const pendingCash = mps.reduce((s, o) => s + (o.mini_proposal.starter_price_sar || 0), 0);

  let md = `# Founder Daily Super Command — أمر القيادة اليومي
*Date: ${date}*

> التقرير يجاوب: من نستهدف؟ لماذا؟ ماذا نرسل؟ من يتصل؟ ما العرض؟ ما التسليم؟ ما القرار الأهم؟

---

## 1. Today's critical decision
${criticalDecision(ctx, evalResult)}

---

## 2. 400 Draft status
- Batch scored: **${evalResult.total}** of **${evalResult.target}/day** target.
- 🟢 top_priority: ${evalResult.counts.top_priority} · 🟡 approval_queue: ${evalResult.counts.approval_queue} · 🟠 needs_rewrite: ${evalResult.counts.needs_rewrite} · 🔴 rejected: ${evalResult.counts.rejected}

---

## 3. Top 100 Approval Queue summary
- Qualified for approval queue: **${evalResult.top100.length}**.
- Rule: score ≥ 75 · recommended_system · Need Card · risk ≠ high · evidence · CTA.

---

## 4. Top 20 companies to send

| # | Company | System | Score |
|--:|---------|--------|------:|
`;
  if (sends.length === 0) md += `| — | — | — | — |\n`;
  sends.forEach((e, i) => {
    md += `| ${i + 1} | ${e.company} | ${systemName(ctx, e.system)} | ${e.total} |\n`;
  });

  md += `
> Sending is human-gated: these are recommended, not auto-sent.

---

## 5. Top 30 calls to make

| # | Company | System | Priority | Opener |
|--:|---------|--------|----------|--------|
`;
  if (calls.length === 0) md += `| — | — | — | — | — |\n`;
  calls.forEach((o, i) => {
    md += `| ${i + 1} | ${o.company} | ${systemName(ctx, o.system)} | ${o.call_priority} | ${(o.call_brief.opening_line || "").slice(0, 48)}… |\n`;
  });

  md += `
Full briefs: \`reports/sales_ops/CALL_FOLLOWUP_QUEUE.md\`

---

## 6. Mini proposals waiting approval (${mps.length})

| Opportunity | Company | System | Starter (SAR) |
|-------------|---------|--------|--------------:|
`;
  if (mps.length === 0) md += `| — | — | — | — |\n`;
  for (const o of mps) md += `| ${o.id} | ${o.company} | ${systemName(ctx, o.mini_proposal.system)} | ${o.mini_proposal.starter_price_sar} |\n`;

  md += `
---

## 7. Delivery pipelines status (${deliveries.length})

| Opportunity | Company | System | Stage | Gate |
|-------------|---------|--------|-------|------|
`;
  if (deliveries.length === 0) md += `| — | — | — | — | — |\n`;
  for (const o of deliveries) {
    const g = deliveryGate(o.delivery || {});
    md += `| ${o.id} | ${o.company} | ${systemName(ctx, o.system)} | ${o.stage} | ${g.passed ? "✅" : "🔴 blocked"} |\n`;
  }

  md += `
---

## 8. Website leads

| Lead | Company | Recommended system | Note |
|------|---------|--------------------|------|
`;
  const leads = ctx.websiteLeads.leads || [];
  if (leads.length === 0) md += `| — | — | — | لا توجد طلبات اليوم |\n`;
  for (const l of leads) {
    const rec = recommendSystem(l.intake_text);
    md += `| ${l.id} | ${l.company} | ${systemName(ctx, rec)} | ${l.demo ? "demo seed" : "→ Need Card + Mini Proposal draft"} |\n`;
  }

  md += `
> كل طلب من الموقع يولّد Client Need Card + نظامًا موصى به + مسودة Mini Proposal (باعتماد المؤسس).

---

## 9. Best performing system
${bs.system ? `${systemName(ctx, bs.system)} — ${bs.count} في Top 100.` : "—"}

## 10. Best sector
${sec.sector} — ${sec.count} في Top 100.

## 11. Biggest risk
${biggestRisk(ctx, evalResult, control)}

## 12. Cash / pricing opportunities
- Mini proposals pending approval: **${mps.length}** بقيمة افتتاحية إجمالية **${pendingCash} SAR** (تتطلب اعتماد المؤسس).
- Active/won deliveries: **${deliveries.length}** (إيراد قيد التنفيذ/التجديد).

## 13. Tomorrow recommendation
- اعتمد العروض المعلّقة (${mps.length}) وابدأ التسليمات الجاهزة.
- عزّز drafts الأنظمة الأقل تمثيلًا في Top 100 لتوازن القطاعات.
- حافظ على بوابة الأمان خضراء قبل أي توسع في الإرسال.

---

*Generated: ${date} | npm run commercial:brief*
`;
  return md;
}

function renderWeekly(ctx, data) {
  const { summary, evalResult, mps, deliveries } = data;
  const date = today();
  let md = `# Weekly Board Review — المراجعة الأسبوعية للوحة
*Week ending: ${date}*

---

## 1. Pipeline by Stage

| Stage | Count |
|-------|------:|
`;
  for (const s of BOARD_STATUSES) md += `| ${s} | ${summary[s] || 0} |\n`;

  md += `
---

## 2. This Week's Signals

| Signal | Value |
|--------|------:|
| Top 100 size | ${evalResult.top100.length} |
| Rejected drafts | ${evalResult.counts.rejected} |
| Mini proposals waiting | ${mps.length} |
| Delivery pipelines | ${deliveries.length} |
| Best system | ${systemName(ctx, bestSystem(evalResult).system)} |

---

## 3. Founder Review Questions
- هل وزّعنا الإرسال على الأنظمة الخمسة بتوازن؟
- هل العروض المعلّقة تتحرك خلال 48 ساعة؟
- هل كل تسليم نشط يحقق success metric وacceptance criteria؟
- ما القطاع الذي يستحق تركيزًا أكبر الأسبوع القادم؟

---

*Generated: ${date} | npm run commercial:brief*
`;
  return md;
}

function renderContentQueue(ctx) {
  const date = today();
  let md = `# Focus 5 — Content Queue
*Week of: ${ctx.content.week_of || date}*

> لا case studies وهمية. مسموح فقط: ${(ctx.content._meta && ctx.content._meta.allowed_proof_labels || []).join(" · ")}

---

## Weekly Themes

| System | Theme |
|--------|-------|
`;
  for (const t of ctx.content.weekly_themes || []) md += `| ${systemName(ctx, t.system)} | ${t.theme} |\n`;

  md += `
---

## 7-Day Queue

| Day | System | Format | Hook | Status | Proof label |
|-----|--------|--------|------|--------|-------------|
`;
  for (const q of ctx.content.queue || []) {
    md += `| ${q.day} | ${systemName(ctx, q.system)} | ${q.format} | ${q.hook} | ${q.status} | ${q.proof_label} |\n`;
  }
  md += `\n---\n\n*Generated: ${date} | npm run commercial:brief*\n`;
  return md;
}

function renderPartnerPipeline(ctx) {
  const date = today();
  let md = `# Focus 5 — Partner Pipeline
*Date: ${date}*

> النموذج: الشريك يجيب العلاقة، Dealix يشغّل النظام، الشريك يأخذ referral fee أو margin. لا تُشارك بيانات العميل بدون موافقة.

---

## Partner Fit

| Partner type | Recommended systems |
|--------------|---------------------|
`;
  for (const f of ctx.partners.partner_fit || []) {
    md += `| ${f.partner_type} | ${(f.systems || []).map((s) => systemName(ctx, s)).join(" / ")} |\n`;
  }

  md += `
---

## Pipeline

| ID | Partner | Type | Stage | Model | Next step |
|----|---------|------|-------|-------|-----------|
`;
  for (const p of ctx.partners.pipeline || []) {
    md += `| ${p.id} | ${p.partner} | ${p.partner_type} | ${p.stage} | ${p.model} | ${p.next_step} |\n`;
  }
  md += `\n---\n\n*Generated: ${date} | npm run commercial:brief*\n`;
  return md;
}

function main() {
  const ctx = loadContext();
  const evalResult = evaluateBatch(ctx);
  const control = runControlChecks(ctx, evalResult, []);
  const data = {
    evalResult,
    control,
    summary: boardSummary(ctx),
    calls: callsToMake(ctx, 30),
    sends: companiesToSend(ctx, evalResult, 20),
    mps: miniProposalsWaiting(ctx),
    deliveries: deliveryPipelines(ctx),
  };

  const superMd = renderSuperCommand(ctx, data);
  const cmdPath = writeReport("founder/DAILY_SUPER_COMMAND.md", superMd);
  const weeklyPath = writeReport("founder/WEEKLY_BOARD_REVIEW.md", renderWeekly(ctx, data));
  const contentPath = writeReport("content/FOCUS_5_CONTENT_QUEUE.md", renderContentQueue(ctx));
  const partnerPath = writeReport("partners/FOCUS_5_PARTNER_PIPELINE.md", renderPartnerPipeline(ctx));

  // Verify all 13 required sections are present (self-check).
  const missing = REQUIRED_SUPER_COMMAND_SECTIONS.filter((s) => !superMd.includes(s));

  console.log("=".repeat(72));
  console.log(`  DEALIX FOUNDER DAILY SUPER COMMAND — ${today()}`);
  console.log("=".repeat(72));
  console.log(`  Command:  ${path.relative(process.cwd(), cmdPath)}`);
  console.log(`  Weekly:   ${path.relative(process.cwd(), weeklyPath)}`);
  console.log(`  Content:  ${path.relative(process.cwd(), contentPath)}`);
  console.log(`  Partners: ${path.relative(process.cwd(), partnerPath)}`);
  console.log(`  Sections present: ${REQUIRED_SUPER_COMMAND_SECTIONS.length - missing.length}/${REQUIRED_SUPER_COMMAND_SECTIONS.length}`);
  if (missing.length) {
    console.log(`  🔴 MISSING SECTIONS: ${missing.join(", ")}`);
    console.log("=".repeat(72));
    process.exit(1);
  }
  console.log("  ✅ Founder brief complete (all required sections present).");
  console.log("=".repeat(72));
}

main();
