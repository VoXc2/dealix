# Dealix Enterprise Readiness Program — برنامج الجاهزية المؤسسية

**EN.** This folder is the single map that answers one question: *which parts of
Dealix are actually enterprise-grade, and which only look like it?* It does not
build new systems. It scores what exists, names real gaps, and commits the team
to proving **one** complete cross-layer workflow before scaling.

**AR.** هذا المجلد هو الخريطة الوحيدة التي تجيب على سؤال واحد: *أي أجزاء Dealix
جاهزة فعلاً على مستوى المؤسسات، وأيها يبدو كذلك فقط؟* لا يبني أنظمة جديدة — بل
يقيّم الموجود، ويسمّي الفجوات الحقيقية، ويُلزم الفريق بإثبات **مسار عمل واحد
كامل** عبر كل الطبقات قبل التوسّع.

> **The rule — القاعدة.** A layer is real only when all eight hold:
> `Code + Tests + Evals + Observability + Governance + Rollback + Metrics + Business Impact`.
> طبقة ناقصة واحدًا من الثمانية = غير جاهزة.

---

## How to read this program — كيف تقرأ البرنامج

| Document | Purpose |
|----------|---------|
| [`enterprise_readiness_model.md`](enterprise_readiness_model.md) | The 11-layer model, the 8-component definition of "real", the 6-release ladder. |
| [`scoring_system.md`](scoring_system.md) | The 0–100 rubric and the `PASS / FIX / BLOCKED` decision. |
| [`cross_layer_validation.md`](cross_layer_validation.md) | How layers connect; the end-to-end proof workflow; the 13-step real-arrival test; the maturity ladder. |
| [`multi_tenancy.md`](multi_tenancy.md) | As-built tenant isolation + readiness checklist. |
| [`rbac.md`](rbac.md) | As-built role-based access control + readiness checklist. |
| [`audit_logging.md`](audit_logging.md) | As-built audit trail + readiness checklist. |
| [`rollback.md`](rollback.md) | Rollback requirements and the drill that makes them real. |
| [`gap_analysis.md`](gap_analysis.md) | **Core deliverable.** All 11 layers scored against the current repo. |
| [`30_day_proof_workflow_plan.md`](30_day_proof_workflow_plan.md) | The 30-day plan: prove one workflow end-to-end, nothing else. |

---

## The 11 layers and their owners — الطبقات الإحدى عشرة ومالكوها

Every layer has exactly one accountable owner. "Owner" is a role, not a person —
the founder may hold several roles at once during the pilot phase.

| # | Layer — الطبقة | Owner role | Primary code/docs home |
|---|----------------|-----------|------------------------|
| 1 | Foundation — الأساس | Platform Engineer | `pyproject.toml`, `Dockerfile`, `.github/workflows/`, `api/main.py`, `db/migrations/` |
| 2 | Multi-tenancy — العزل متعدد المستأجرين | Platform Engineer | `api/middleware/tenant_isolation.py`, `TenantRecord` |
| 3 | RBAC — التحكم بالأدوار | Security Engineer | `api/security/rbac.py`, `api/security/auth_deps.py` |
| 4 | Agent Runtime — تشغيل الوكلاء | Agent Engineer | `auto_client_acquisition/secure_agent_runtime_os/`, `agent_governance/` |
| 5 | Workflow Engine — محرك المسارات | Agent Engineer | `auto_client_acquisition/workflow_os/`, `workflow_os_v10/` |
| 6 | Knowledge / Memory — المعرفة والذاكرة | Knowledge Engineer | `auto_client_acquisition/company_brain*/`, `knowledge_os/`, `core/memory/` |
| 7 | Governance — الحوكمة | Governance Lead | `auto_client_acquisition/governance_os/`, `docs/governance/` |
| 8 | Observability — المراقبة | Platform Engineer | `auto_client_acquisition/observability_v10/`, `docs/observability/` |
| 9 | Evals — التقييم | Quality Lead | `evals/` |
| 10 | Delivery Playbooks — كتيبات التسليم | Delivery Lead | `docs/playbooks/` |
| 11 | Continuous Improvement — التحسين المستمر | PM / Founder | `auto_client_acquisition/friction_log/`, `.github/workflows/weekly_self_improvement.yml` |

---

## Relationship to the existing gates — العلاقة بالبوابات القائمة

Dealix already has 11 commercial gates in [`../docs/readiness/`](../docs/readiness/)
(Gate 0 Founder Clarity → Gate 10 World-Class). **Those answer "can we sell?"**
This program's 11 layers answer **"is the system real?"** They are
complementary, not a replacement:

- The technical layers chiefly back **Gate 3 (Product Readiness)**,
  **Gate 4 (Governance Readiness)**, and **Gate 9 (Scale Readiness)**.
- A gate cannot pass on inflated confidence: if its backing layers score
  `BLOCKED` in [`gap_analysis.md`](gap_analysis.md), the gate is `BLOCKED` too.
- Both systems use the same three-way decision: `PASS / FIX / BLOCKED`.

There is **one** readiness truth, surfaced two ways. Do not fork it.

---

## How to run verification — كيف تُجري التحقق

```bash
# Repo-level readiness tooling (already in the repo)
python scripts/verify_dealix_ready.py
python scripts/verify_dealix_ready.py --skip-tests

# Layer scoring is manual — follow scoring_system.md, record in gap_analysis.md
```

This program is **documentation only**. It changes no application code, no
schema, no endpoint. Adopting it cannot break anything that runs today.

---

## ملخص بالعربية

برنامج الجاهزية المؤسسية يحوّل Dealix من «مجموعة وحدات» إلى نظام تشغيل قابل
للقياس. لا يبني جديدًا؛ يقيس الموجود عبر 11 طبقة، ويعتمد تعريفًا صارمًا
للجاهزية (ثمانية مكوّنات)، ويُلزم الفريق بإثبات مسار عمل واحد كامل قبل التوسّع.
أي طبقة لا تثبت المكوّنات الثمانية تُعَدّ غير جاهزة، ولا تُباع، ولا يُبنى فوقها.
