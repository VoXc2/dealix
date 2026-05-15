# Cross-Layer Validation — التحقق العابر للطبقات

**EN.** A layer scored in isolation can still fail in production, because real
value only appears when layers connect. This document defines the connective
test: one workflow that exercises **all 11 layers at once**, plus the maturity
ladder that tells you where Dealix actually stands.

**AR.** الطبقة التي تُسجَّل بمعزل قد تفشل في الإنتاج، لأن القيمة الحقيقية لا تظهر
إلا حين تتصل الطبقات. تحدّد هذه الوثيقة الاختبار الرابط: مسار عمل واحد يُشغّل
**الطبقات الإحدى عشرة دفعة واحدة**، إضافةً إلى سلّم النضج الذي يحدّد موقع Dealix
الحقيقي.

---

## 1. The proof workflow — مسار العمل المُثبِت

The cross-layer test is a single inbound-lead workflow. Each step **must** touch
the layer named beside it, or that layer is not validated.

```
Inbound Lead
  → detect tenant            Layer 2  Multi-tenancy
  → check RBAC               Layer 3  RBAC
  → classify intent          Layer 4  Agent Runtime  (Sales Agent)
  → retrieve company context Layer 6  Knowledge / Memory  (cited, scoped)
  → score lead               Layer 5  Workflow Engine
  → draft response           Layer 4  Agent Runtime
  → risk check               Layer 7  Governance
  → approval if needed       Layer 7  Governance  (human-in-the-loop)
  → update CRM / Sheet       Layer 5  Workflow Engine
  → emit metrics + trace     Layer 8  Observability
  → eval the run             Layer 9  Evals
  → ROI / executive report   Layer 10 Delivery Playbooks
  → friction captured        Layer 11 Continuous Improvement
```

Layer 1 (Foundation) underlies all of it — the workflow cannot run unless the
repo builds, deploys, and migrates. So one workflow, run once, with evidence,
validates the whole stack.

---

## 2. The 13-step real-arrival test — اختبار الوصول الحقيقي

Run this scripted scenario. It is the acceptance test for the
[`30-day proof workflow plan`](30_day_proof_workflow_plan.md).

| # | Step | Layer evidenced |
|---|------|-----------------|
| 1 | Create tenant: *Demo Real Estate Co* | 2 |
| 2 | Create users: `owner`, `sales_manager`, `agent_operator` | 3 |
| 3 | Upload knowledge base: pricing, properties, FAQs | 6 |
| 4 | Run an inbound-lead scenario | 5 |
| 5 | Sales Agent qualifies the lead | 4 |
| 6 | Company Brain retrieves a **cited** answer | 6 |
| 7 | Workflow scores the lead | 5 |
| 8 | Governance requires approval to send an offer | 7 |
| 9 | A human approves | 7 |
| 10 | CRM / Sheet updates | 5 |
| 11 | Observability creates a `trace_id` | 8 |
| 12 | Eval report is generated | 9 |
| 13 | Executive ROI report is generated; rollback drill executed | 10, 5 |

Pass all 13 with evidence → **Client Pilot Ready**.

---

## 3. Cross-layer failure modes — أنماط الفشل العابرة

Validating layers individually misses these. The proof workflow catches them:

| Failure | Why isolation misses it |
|---------|-------------------------|
| Joined query leaks another tenant's rows | Layer 2 unit test passes; the leak is in Layer 5's query path. |
| Agent retrieves a doc the user may not see | Layer 4 and Layer 6 each pass; the permission check sits between them. |
| High-risk action skips approval inside a workflow step | Layer 7 passes standalone; Layer 5 calls the executor directly. |
| A `trace_id` exists but does not span the agent call | Layer 8 passes; the trace context is dropped at the Layer 4 boundary. |
| Eval passes but no business outcome moved | Layers 9 evidenced; Layer 10/11 never closed the loop. |

Rule: a layer is **cross-validated** only when the proof workflow exercises it
in sequence with its neighbours — not just in its own unit test.

---

## 4. The maturity ladder — سلّم النضج

| Stage | Criteria — المعايير |
|-------|---------------------|
| **Client Pilot Ready** | The 13-step test passes once, with evidence. |
| **Enterprise Ready** | The 13-step test passes for **3 separate clients**. |
| **Mission-Critical Ready** | Monitoring, incident response, SLOs, and a rollback **drilled under load** are all in place. |

Dealix advances one rung at a time. Do not claim a rung without the evidence
for it — and do not skip a rung.

---

## 5. Where this plugs in — نقطة الاتصال

- The per-layer scores live in [`gap_analysis.md`](gap_analysis.md).
- The scoring rubric is [`scoring_system.md`](scoring_system.md).
- The 30-day plan ([`30_day_proof_workflow_plan.md`](30_day_proof_workflow_plan.md))
  exists to make the 13-step test pass for the first client.
- A passing 13-step test is the evidence behind Gate 3, Gate 7, and Gate 9 in
  [`../docs/readiness/`](../docs/readiness/).

---

## ملخص بالعربية

التحقق العابر للطبقات يثبت أن الطبقات تتصل فعليًا، لا أنها تعمل منفردة. الأداة
هي مسار عمل واحد للعميل المحتمل يمرّ عبر الطبقات الإحدى عشرة، يُختبر عبر سيناريو
من 13 خطوة. نجاح الـ13 مرة واحدة = جاهز للتجربة مع عميل؛ ونجاحها لثلاثة عملاء =
جاهز مؤسسيًا؛ ومع المراقبة والاستجابة للحوادث وSLOs وتراجع مُجرَّب تحت الحِمل =
جاهز للأنظمة الحرجة.
