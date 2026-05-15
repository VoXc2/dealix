# Enterprise Readiness Model — نموذج الجاهزية المؤسسية

**EN.** The market does not reward "more AI". It rewards AI placed inside real
workflows, with governance, measurement, and monitoring. This model defines what
"real" means for Dealix and how the team gets there release by release.

**AR.** السوق لا يكافئ «المزيد من الذكاء الاصطناعي»، بل يكافئ الذكاء الاصطناعي
الموضوع داخل مسارات عمل حقيقية مع حوكمة وقياس ومراقبة. يحدّد هذا النموذج معنى
«الجاهزية» لـ Dealix وكيف يصل الفريق إليها إصدارًا بعد إصدار.

References: NIST AI Risk Management Framework (Govern / Map / Measure / Manage),
OpenTelemetry (traces · metrics · logs), McKinsey — *The State of AI*.

---

## 1. The definition of "real" — تعريف «الجاهزية الحقيقية»

A layer is **real** only when **all eight** components are present and evidenced.
Miss one — the layer is not ready.

```
Layer is real =
    Code              الكود موجود ويعمل
  + Tests             اختبارات تثبت السلوك
  + Evals             تقييمات تثبت الجودة
  + Observability     traces / metrics / logs
  + Governance        سياسة وموافقة وتدقيق
  + Rollback          تراجع مُجرَّب
  + Metrics           مقاييس تشغيلية حية
  + Business Impact   أثر تجاري مُثبَت
```

| Component | What evidence looks like |
|-----------|--------------------------|
| Code | Working implementation in the repo, not a stub or a `_v*` fork that nobody uses. |
| Tests | `pytest` cases that fail if the behaviour breaks. |
| Evals | A YAML/JSONL pack in `evals/` defining "good" and a threshold. |
| Observability | Every action emits a `trace_id`; metrics and logs are queryable. |
| Governance | High-risk actions pass policy + approval; everything is audit-logged. |
| Rollback | A documented, **drilled** path back to the last good state. |
| Metrics | Live operational numbers (completion rate, latency, error rate). |
| Business Impact | A measured outcome a customer would pay for. |

The full scoring rubric for these eight is in [`scoring_system.md`](scoring_system.md).

---

## 2. The 11 layers — الطبقات الإحدى عشرة

| # | Layer | What it guarantees |
|---|-------|--------------------|
| 1 | Foundation | The repo builds, deploys, migrates, and runs CI reproducibly. |
| 2 | Multi-tenancy | One tenant's data is never visible to another. |
| 3 | RBAC | Every action is checked against the actor's role. |
| 4 | Agent Runtime | Agents run inside boundaries with a kill-switch. |
| 5 | Workflow Engine | Multi-step flows are durable, retryable, observable. |
| 6 | Knowledge / Memory | Answers are cited, permission-aware, tenant-scoped. |
| 7 | Governance | Risk → policy → approval → execution → audit on every action. |
| 8 | Observability | Every workflow and agent action is traceable and alertable. |
| 9 | Evals | No release ships without passing eval gates. |
| 10 | Delivery Playbooks | Any team member can deliver and hand over a client. |
| 11 | Continuous Improvement | Friction is captured and fed back into releases. |

Each layer is scored individually in [`gap_analysis.md`](gap_analysis.md).

---

## 3. The 6-release ladder — سلّم الإصدارات الستة

Do not "build all the layers". Build them in order. Each release has hard
acceptance criteria; a release is not done until they pass.

### Release 0 — Repo Re-Architecture *(this delivery)*
Establish the readiness program without breaking anything.
**Acceptance:** every layer has a home and an owner; every layer has a readiness
checklist; no existing endpoint broke.

### Release 1 — Client Pilot Foundation *(this delivery, documented as-built)*
Serve one client safely.
**Acceptance:** 1 tenant · 3 users · 2 roles; every API resolves `tenant_id`;
every sensitive action produces an audit log; rollback drilled at least once.

### Release 2 — First Real Agent + Workflow
One agent inside one workflow, end to end.
**Acceptance:** workflow completion ≥ 90% on test cases; every high-risk action
stops at approval; every step logged; every failure has retry or fallback.

### Release 3 — Knowledge + Memory
The real Company Brain.
**Acceptance:** every important answer carries a citation; zero cross-tenant
retrieval; zero retrieval outside the user's permission; retrieval eval ≥ threshold.

### Release 4 — Governance Runtime
Governance as runtime, not documents.
**Acceptance:** 100% of high-risk actions require approval; every approval is
recorded; every policy violation surfaces on a dashboard.

### Release 5 — Observability + Evals + Release Gates
Where Dealix becomes enterprise.
**Acceptance:** every workflow has a `trace_id`; every agent action is logged;
every release passes eval gates; every release has a rollback plan. **No update
ships without evals.**

### Release 6 — Executive Intelligence + Delivery System
The layer that sells larger contracts.
**Acceptance:** ROI report can be produced; client handover can be delivered;
monthly review can be run; any team member can follow a playbook.

> **Scope of this delivery.** Only Release 0 + Release 1 are executed now, as
> documentation. Releases 2–6 stay here as the committed acceptance criteria —
> built only after the 30-day proof workflow (see
> [`30_day_proof_workflow_plan.md`](30_day_proof_workflow_plan.md)) is greenlit.

---

## 4. The anti-pattern — النمط الممنوع

**Do not overbuild.** One complete cross-layer workflow beats ten half-finished
features. The current repo already shows the failure mode: parallel `_v6` /
`_v10` module forks, three `company_brain*` variants, two `observability_*`
trees. Sprawl is not progress. The model rewards depth (all 8 components on one
workflow) over breadth (many shallow modules).

---

## ملخص بالعربية

الجاهزية الحقيقية = ثمانية مكوّنات مجتمعة لكل طبقة. هناك 11 طبقة، وتُبنى عبر
6 إصدارات مرتّبة لكل منها معايير قبول صارمة. هذا التسليم ينفّذ الإصدارين 0 و1
كوثائق فقط، ويترك 3–6 كمعايير قبول مُلزِمة تُبنى بعد إثبات مسار العمل الواحد.
القاعدة الذهبية: مسار واحد كامل أفضل من عشر ميزات ناقصة.
