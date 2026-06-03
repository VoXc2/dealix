#!/usr/bin/env node
// Dealix Commercial Daily Plan (commercial:plan)
// Turns scored drafts + prospects + follow-ups into a Sales Ops Board status,
// a Call Brief queue, and a Mini Proposal queue. Nothing is sent automatically.

import path from "node:path";
import {
  COMMERCIAL_DIR, REVENUE_DIR, REPORTS_DIR,
  today, loadJson, loadCsv, loadConfig, writeFileEnsured, systemById,
} from "./commercial-lib.js";

const BOARD_STAGES = [
  "researched", "need_card_ready", "draft_ready", "approved", "sent",
  "call_due", "called", "interested", "mini_proposal_ready", "proposal_sent",
  "won", "delivery_started", "active", "renewal_candidate", "lost", "do_not_contact",
];

function deriveStage(prospect, scoredById, suppressedSet) {
  if (suppressedSet.has(prospect.company.toLowerCase())) return "do_not_contact";
  const scored = scoredById.get(prospect.company.toLowerCase());
  if (scored && scored.gate_pass && scored.total >= 75) return "draft_ready";
  if (scored && scored.client_need_card) return "need_card_ready";
  return "researched";
}

function callBrief(prospect, sys, objection) {
  const painAr = prospect.pain || "تحدي في تشغيل الإيرادات";
  const sysName = sys ? sys.customer_facing_name_ar : "نظام تشغيل الإيرادات";
  return {
    company: prospect.company,
    priority: Number(prospect.score) >= 8 ? "P1" : Number(prospect.score) >= 6 ? "P2" : "P3",
    recommended_system: sysName,
    opening_line: `السلام عليكم، معك فريق Dealix. تواصلنا معكم بخصوص ${painAr}. عندك دقيقتين نوضح الفكرة؟`,
    questions: [
      `كيف تتعاملون حاليًا مع ${painAr}؟`,
      "وش أكثر مرحلة تشعرون فيها أن الفرص تتأخر أو تضيع؟",
      "لو قدرنا نكشف هذا بدقة خلال أيام، يهمكم نبدأ بجلسة تشخيص قصيرة؟",
    ],
    expected_objection: objection ? { objection: objection.objection, response: objection.response } : null,
    next_step: "حجز جلسة تشخيص 15 دقيقة، ثم إعداد Mini Proposal للاعتماد",
    owner: "Founder",
  };
}

function main() {
  const cfg = loadConfig();
  const prospects = loadCsv(path.join(REVENUE_DIR, "prospects.csv"));
  const followups = loadJson(path.join(REVENUE_DIR, "followups.json"), { followups: [] });
  const proposals = loadJson(path.join(REVENUE_DIR, "proposals.json"), { active_proposals: [] });
  const scores = loadJson(path.join(COMMERCIAL_DIR, "draft_scores.json"), { drafts: [] });
  const objections = loadJson(path.join(REVENUE_DIR, "objections.json"), { common_objections: [] });

  const date = today();
  const suppressedSet = new Set(
    (cfg.suppression.do_not_contact_companies || []).map((c) => c.toLowerCase())
  );
  const scoredByCompany = new Map(scores.drafts.map((d) => [d.company.toLowerCase(), d]));

  // Board counts
  const counts = Object.fromEntries(BOARD_STAGES.map((s) => [s, 0]));
  const boardRows = prospects.map((p) => {
    const stage = deriveStage(p, scoredByCompany, suppressedSet);
    counts[stage] += 1;
    const scored = scoredByCompany.get(p.company.toLowerCase());
    return {
      company: p.company,
      segment: p.segment,
      stage,
      score: scored ? scored.total : "",
      recommended_system: scored ? scored.recommended_system_name : "",
      owner: "Founder",
    };
  });

  // Call queue: follow-ups due today/overdue and still scheduled
  const dueFollowups = (followups.followups || []).filter(
    (f) => (f.scheduled_date || "9999-12-31") <= date && f.status === "scheduled"
  );
  const prospectByCompany = new Map(prospects.map((p) => [p.company.toLowerCase(), p]));
  const callQueue = dueFollowups.map((f, i) => {
    const p = prospectByCompany.get(f.company.toLowerCase()) || { company: f.company, pain: "", score: "0" };
    const scored = scoredByCompany.get(f.company.toLowerCase());
    const sys = scored ? systemById(cfg.systems, scored.recommended_system) : null;
    const objection = objections.common_objections[i % Math.max(1, objections.common_objections.length)];
    return callBrief(p, sys, objection);
  });

  // Mini proposal queue: built only from positive signals (interested/positive_reply).
  // Current pipeline has none yet — surfaced honestly with the trigger model.
  const miniProposalQueue = (proposals.active_proposals || []).map((ap) => ({
    company: ap.company,
    recommended_system: ap.offer || "Revenue Operating System",
    approval_status: "pending_founder_approval",
  }));

  const boardOut = { generated: date, stages: BOARD_STAGES, counts, board: boardRows, call_queue: callQueue, mini_proposal_queue: miniProposalQueue };
  writeFileEnsured(path.join(COMMERCIAL_DIR, "sales_board.json"), JSON.stringify(boardOut, null, 2) + "\n");

  // ---- markdown ----
  const countRows = BOARD_STAGES.map((s) => `| ${s} | ${counts[s]} |`).join("\n");
  const boardTable = boardRows
    .sort((a, b) => (Number(b.score) || 0) - (Number(a.score) || 0))
    .map((r) => `| ${r.company} | ${r.segment} | ${r.stage} | ${r.score || "—"} | ${r.recommended_system || "—"} | ${r.owner} |`)
    .join("\n");

  const callTable = callQueue.length
    ? callQueue
        .map(
          (c, i) =>
            `### ${i + 1}. ${c.company} — ${c.priority} (${c.recommended_system})
- **Opening:** ${c.opening_line}
- **Questions:**
  1. ${c.questions[0]}
  2. ${c.questions[1]}
  3. ${c.questions[2]}
- **Expected objection:** ${c.expected_objection ? `${c.expected_objection.objection} → ${c.expected_objection.response}` : "—"}
- **Next step:** ${c.next_step}
- **Owner:** ${c.owner}`
        )
        .join("\n\n")
    : "_No calls due today (no scheduled follow-ups at or before today's date)._";

  const md = `# Sales Ops Board — Status
*Date: ${date} | Generated by scripts/commercial-daily-plan.js*

> One board, 16 stages, one owner per stage. AI prepares; the founder decides.
> Stage model: \`docs/sales_ops/LEAD_STATUS_MODEL_AR.md\` · Owners: \`docs/sales_ops/OWNER_ASSIGNMENT_POLICY_AR.md\`

---

## 1. Board Stage Counts

| Stage | Count |
|-------|------:|
${countRows}

---

## 2. Companies on the Board

| Company | Segment | Stage | Draft Score | Recommended System | Owner |
|---------|---------|-------|------------:|--------------------|-------|
${boardTable || "| — | — | — | — | — | — |"}

---

## 3. Call Brief Queue (due today)

> Each brief satisfies the Call Brief Quality Gate: opening line, discovery questions, expected objection, next step.

${callTable}

---

## 4. Mini Proposal Queue

> A Mini Proposal is generated only after a positive signal (positive_reply, send_more_info, price_question, successful_call, diagnostic_request). It is **never sent automatically** — \`approval_status = pending_founder_approval\`.

${miniProposalQueue.length
      ? miniProposalQueue.map((m) => `- **${m.company}** → ${m.recommended_system} (${m.approval_status})`).join("\n")
      : "_0 mini proposals waiting. None of the current prospects has returned a positive signal yet._"}

---

*Generated: ${date} | Reproduce: \`npm run commercial:plan\` | Machine output: company_os/commercial/sales_board.json*
`;

  writeFileEnsured(path.join(REPORTS_DIR, "sales_ops", "SALES_OPS_BOARD_STATUS.md"), md);

  console.log(`✅ Daily plan complete.`);
  console.log(`   Board companies: ${boardRows.length} | Calls due: ${callQueue.length} | Mini proposals waiting: ${miniProposalQueue.length}`);
  console.log(`   → reports/sales_ops/SALES_OPS_BOARD_STATUS.md`);
}

main();
