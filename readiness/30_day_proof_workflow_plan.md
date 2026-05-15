# 30-Day Proof Workflow Plan — خطة الـ30 يومًا لمسار العمل المُثبِت

**EN.** The gap analysis ([`gap_analysis.md`](gap_analysis.md)) showed Dealix is
capability-rich and proof-poor. This plan fixes that — not by building more, but
by driving **one** workflow's slice of all 11 layers to `PASS`.

**AR.** أظهر تحليل الفجوات أن Dealix غني بالقدرات فقير بالإثبات. تعالج هذه الخطة
ذلك — لا ببناء المزيد، بل بدفع شريحة **مسار عمل واحد** من كل الطبقات الإحدى عشرة
إلى `PASS`.

---

## 1. The one workflow — مسار العمل الواحد

```
Inbound Lead
  → Sales Agent
  → Knowledge Retrieval (cited, tenant-scoped, permission-aware)
  → Governance Check
  → Human Approval
  → CRM / Sheet Update
  → Observability Trace
  → Eval Report
  → Executive ROI Report
```

This is the workflow from [`cross_layer_validation.md`](cross_layer_validation.md).
Nothing else is in scope for 30 days.

### The non-negotiable constraint — القيد غير القابل للتفاوض

> **Do not overbuild.** No new modules. No new `_v*` forks. For every capability
> with competing implementations (see `gap_analysis.md` §1), **pick one** and
> use only that. One complete workflow beats ten half-finished features.

---

## 2. Week-by-week — أسبوعًا بأسبوع

### Week 1 — Consolidate + Foundation (Layers 1, 2, 3)
- Pick the **one** canonical implementation per capability: workflow engine,
  agent runtime, company brain, knowledge, observability. Record the choices.
- Stand up tenant *Demo Real Estate Co* with 3 users
  (`owner`, `sales_manager`, `agent_operator`) and 2+ roles.
- Fix the **dead `require_role` stub** ([`rbac.md`](rbac.md) §3 gap 1).
- **Exit gate:** tenant + users + roles exist; every endpoint on the workflow
  path resolves `tenant_id`; RBAC guard works on every step.

### Week 2 — Agent + Workflow + Knowledge (Layers 4, 5, 6)
- Wire the chosen Sales Agent into the chosen workflow engine for the
  lead-qualification path.
- Add `tenant_id` to agent-run records so agent runs are tenant-scoped.
- Upload the demo knowledge base (pricing, properties, FAQs); make retrieval
  **cited, tenant-scoped, permission-aware**.
- **Exit gate:** the workflow runs end-to-end on test cases; retrieval returns a
  citation; zero cross-tenant / out-of-permission retrieval.

### Week 3 — Governance + Observability + Evals (Layers 7, 8, 9)
- Route the "send offer" step through risk → policy → **human approval** →
  execute → audit.
- Ensure one `trace_id` spans the whole run, including the agent call.
- Write the eval pack for the lead-qualification path; **wire evals as a release
  gate** (the single highest-leverage fix from `gap_analysis.md`).
- **Exit gate:** 100% of high-risk actions stop at approval; every step logged
  under one `trace_id`; eval report generated and gating.

### Week 4 — Delivery + Rollback + Proof (Layers 10, 11 + validation)
- Write the proof-workflow delivery + onboarding + QA playbook.
- Generate the executive ROI report from the run.
- Run the rollback drill ([`rollback.md`](rollback.md) §3) once; record RTO/RPO.
- Capture every friction point hit during the 30 days into the friction log.
- **Exit gate:** the 13-step real-arrival test
  ([`cross_layer_validation.md`](cross_layer_validation.md) §2) passes with
  evidence → **Client Pilot Ready**.

---

## 3. Acceptance gates — بوابات القبول

The plan succeeds only if **all** of these are true at day 30:

| # | Gate |
|---|------|
| 1 | The 13-step real-arrival test passes, with recorded evidence. |
| 2 | Workflow completion rate ≥ 90% on the test cases. |
| 3 | 100% of high-risk actions require human approval; each approval recorded. |
| 4 | Every important answer carries a citation; zero cross-tenant retrieval. |
| 5 | Every workflow step is logged under one `trace_id`. |
| 6 | An eval report is generated and **gates** the release. |
| 7 | An executive ROI report is produced from the run. |
| 8 | The rollback drill has been executed once, with RTO/RPO recorded. |
| 9 | The 11 affected layers are re-scored in `gap_analysis.md`; the workflow's slice of each is `PASS`. |

---

## 4. Re-scoring rule — قاعدة إعادة التسجيل

This plan does **not** make all 200+ modules ready. It makes **one workflow's
path** through each layer ready. At day 30, re-score in
[`gap_analysis.md`](gap_analysis.md) and state the scope explicitly: e.g.
*"Layer 5 — Workflow Engine: `PASS` for the lead-qualification path; the rest of
the layer remains `BLOCKED`."* Honest, scoped scores — never a blanket `PASS`.

---

## 5. What comes after — ما بعد الخطة

- Pass the 13-step test once → **Client Pilot Ready**.
- Repeat for 3 separate clients → **Enterprise Ready**.
- Add monitoring, incident response, SLOs, and a rollback drilled under load →
  **Mission-Critical Ready**.

Then — and only then — execute Releases 2–6 from
[`enterprise_readiness_model.md`](enterprise_readiness_model.md) to widen the
proven path into a full enterprise operating system.

---

## ملخص بالعربية

خطة 30 يومًا تدفع مسار عمل واحدًا (عميل محتمل ← وكيل مبيعات ← استرجاع معرفي
موثّق ← فحص حوكمة ← موافقة بشرية ← تحديث CRM ← أثر مراقبة ← تقرير تقييم ← تقرير
عائد تنفيذي) عبر الطبقات الإحدى عشرة. القيد: لا بناء جديد، واختيار نسخة قانونية
واحدة لكل قدرة. أربعة أسابيع، تسع بوابات قبول، وإعادة تسجيل مُحدَّدة النطاق في
نهاية المدة. النجاح = اجتياز اختبار الـ13 خطوة مرة واحدة = جاهز للتجربة مع عميل.
