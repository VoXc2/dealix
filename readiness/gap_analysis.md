# Gap Analysis — تحليل الفجوات

**EN.** This is the core deliverable: every one of the 11 layers scored against
the **current** Dealix repository, using the rubric in
[`scoring_system.md`](scoring_system.md). The headline result is deliberate and
honest — most layers do **not** pass, and the reason is not missing capability.

**AR.** هذا هو المُخرَج الأساسي: كل طبقة من الطبقات الإحدى عشرة مُسجَّلة مقابل
مستودع Dealix **الحالي**، وفق المعيار في [`scoring_system.md`](scoring_system.md).
النتيجة الرئيسية متعمَّدة وصادقة — معظم الطبقات **لا تنجح**، والسبب ليس نقص
القدرة.

---

## 0. How to read this — كيف تقرأ هذا

- `BLOCKED` here means **unproven against the 8-component bar — not broken.**
  Most BLOCKED layers have working code; what they lack is evals-as-gates, live
  metrics, a drilled rollback, or a single canonical implementation.
- **Confidence.** Layers 1–3 were deep-read against source
  ([`multi_tenancy.md`](multi_tenancy.md), [`rbac.md`](rbac.md),
  [`audit_logging.md`](audit_logging.md)). Layers 4–11 are scored from module
  inventory + exploration; their component scores are **preliminary** and must
  be confirmed during the 30-day plan.
- **Infra-layer Evals.** For infrastructure layers (1, 2, 3, 8) the Evals
  component is satisfied by adversarial / property / security tests, since there
  is no model output to grade.
- Scores use 0 / 6 / 12.5 per component (sum 100). `PASS ≥ 85 · FIX 70–84 ·
  BLOCKED < 70`.

---

## 1. Summary — الملخص

| # | Layer | Score | Verdict |
|---|-------|------:|---------|
| 1 | Foundation | 72 | `FIX` |
| 2 | Multi-tenancy | 70 | `FIX` |
| 3 | RBAC | 64 | `BLOCKED` |
| 4 | Agent Runtime | 57 | `BLOCKED` |
| 5 | Workflow Engine | 57 | `BLOCKED` |
| 6 | Knowledge / Memory | 54 | `BLOCKED` |
| 7 | Governance | 83 | `FIX` |
| 8 | Observability | 57 | `BLOCKED` |
| 9 | Evals | 60 | `BLOCKED` |
| 10 | Delivery Playbooks | 57 | `BLOCKED` |
| 11 | Continuous Improvement | 54 | `BLOCKED` |

**0 PASS · 3 FIX · 8 BLOCKED.**

### The headline finding — الاستنتاج الرئيسي

Dealix is **capability-rich and proof-poor.** `auto_client_acquisition/` alone
holds **200+ modules**. Almost every layer has working code. Yet not one layer
clears the bar, because three things are systematically missing:

1. **Evals are not release gates.** `evals/` has 5 packs, but nothing blocks a
   release on them.
2. **No drilled rollback.** No layer has a recorded rollback drill.
3. **Version sprawl.** Parallel `_v6` / `_v10` forks and triplicated modules
   mean no layer has a single, canonical "this is the one" implementation.

This is the expected result for a feature-rich repo that has **never been
measured this way**. The fix is not more building — it is the 30-day proof
workflow ([`30_day_proof_workflow_plan.md`](30_day_proof_workflow_plan.md)).

### The cross-cutting risk — الخطر العابر: التشعّب (Sprawl)

| Capability | Competing implementations |
|------------|---------------------------|
| Workflow | `workflow_os/` **and** `workflow_os_v10/` |
| Observability | `observability_v6/`, `observability_v10/`, `agent_observability/` |
| Company Brain | `company_brain/`, `company_brain_mvp/`, `company_brain_v6/` |
| Knowledge | `knowledge_os/`, `knowledge_v10/` |
| Agent runtime | `agent_os/`, `secure_agent_runtime_os/`, `ai_workforce/`, `ai_workforce_v10/` |

Each fork splits tests, evals, and observability across versions, so no version
is fully real. **Picking one canonical implementation per capability is a
prerequisite for any layer reaching `PASS`.**

---

## 2. Per-layer detail — تفصيل كل طبقة

Scorecard order: Code · Tests · Evals · Observability · Governance · Rollback ·
Metrics · Impact.

### Layer 1 — Foundation · Platform Engineer
**Modules:** `pyproject.toml`, `requirements.txt`, `Dockerfile`,
`docker-compose.yml`, `api/main.py`, `db/migrations/` (Alembic),
`.github/workflows/` (ruff, bandit, gitleaks, pytest).
**Scorecard:** 9 · 12.5 · 9 · 9 · 9 · 6 · 9 · 9 → **72 · `FIX`**
**Residual gaps:**
- Run the rollback drill ([`rollback.md`](rollback.md) §3) — currently undrilled.
- Module-version sprawl undermines "single canonical impl" (Code capped at 9).

### Layer 2 — Multi-tenancy · Platform Engineer
**Modules:** `api/middleware/tenant_isolation.py`, `TenantRecord` + `tenant_id`
FKs in `db/models.py`, `tests/test_tenant_isolation_v1.py`.
**Scorecard:** 12.5 · 9 · 6 · 9 · 12.5 · 6 · 6 · 9 → **70 · `FIX`**
**Residual gaps:** see [`multi_tenancy.md`](multi_tenancy.md) §3 — endpoint-coverage
proof, super-admin audit enforcement, confirm DB row-level security.

### Layer 3 — RBAC · Security Engineer
**Modules:** `api/security/rbac.py`, `api/security/auth_deps.py`, `RoleRecord`.
**Scorecard:** 9 · 9 · 6 · 9 · 9 · 6 · 6 · 9 → **64 · `BLOCKED`**
**Residual gaps:** see [`rbac.md`](rbac.md) §3 — the **dead `require_role` stub**
(real defect), endpoint-coverage proof, `RoleRecord` docstring/enum mismatch.

### Layer 4 — Agent Runtime · Agent Engineer
**Modules:** `auto_client_acquisition/secure_agent_runtime_os/` (kill-switch,
four-boundaries, policy-engine, deployment-rings), `agent_governance/`
(registry, policy), `AgentRunRecord`; competing `agent_os/`, `ai_workforce*/`.
**Scorecard:** 9 · 6 · 9 · 6 · 9 · 6 · 6 · 6 → **57 · `BLOCKED`**
**Residual gaps:**
- No single canonical runtime — `secure_agent_runtime_os` vs `agent_os` vs
  `ai_workforce*`. Pick one.
- `AgentRunRecord` has **no `tenant_id`** — agent runs are not tenant-scoped.
- Kill-switch / boundaries exist but lack tests proving they fire.

### Layer 5 — Workflow Engine · Agent Engineer
**Modules:** `workflow_os/` (approval-flow, metrics, mapper, model),
`workflow_os_v10/` (state-machine, checkpoint, idempotency, retry-policy);
`api/routers/revenue_os.py` `run_workflow`.
**Scorecard:** 6 · 6 · 9 · 6 · 9 · 9 · 6 · 6 → **57 · `BLOCKED`**
**Residual gaps:**
- Two engine versions — `workflow_os` vs `workflow_os_v10`. Pick one.
- No measured workflow completion rate (target ≥ 90%).
- Rollback primitives exist (`checkpoint`/`idempotency`/`retry_policy`) but the
  in-flight-rollback drill ([`rollback.md`](rollback.md)) is unrun.

### Layer 6 — Knowledge / Memory · Knowledge Engineer
**Modules:** `company_brain/`, `company_brain_mvp/`, `company_brain_v6/`,
`knowledge_os/`, `knowledge_v10/`, `core/memory/`, pgvector
(`ContactEmbeddingRecord`); `evals/company_brain_eval.yaml`.
**Scorecard:** 6 · 6 · 9 · 6 · 6 · 6 · 6 · 9 → **54 · `BLOCKED`**
**Residual gaps:**
- Three `company_brain*` forks + two `knowledge*` modules. Pick one.
- No proof that retrieval is permission-aware and tenant-scoped (hard-fail risk
  per [`scoring_system.md`](scoring_system.md) §3).
- Citation enforcement on important answers not evidenced.

### Layer 7 — Governance · Governance Lead
**Modules:** `auto_client_acquisition/governance_os/` (incl. `rules/no_fake_proof.yaml`),
`docs/governance/` (28 docs), `approval_center/`, `channel_policy_gateway/`,
`evals/governance_eval.yaml`, `tests/test_doctrine_guardrails.py`,
`tests/governance/test_phase2_doctrine.py`.
**Scorecard:** 12.5 · 12.5 · 12.5 · 9 · 12.5 · 6 · 9 · 9 → **83 · `FIX`**
**Residual gaps:** the most mature layer. Just short of `PASS` — needs a
governance rollback path and a policy-violation dashboard with live metrics
(Release 4 criteria).

### Layer 8 — Observability · Platform Engineer
**Modules:** `observability_v6/`, `observability_v10/`, `agent_observability/`,
`structlog`, OpenTelemetry (baseline, "in-flight"), `docs/observability/`,
`docs/observability/sentry_alerts.yaml`.
**Scorecard:** 6 · 6 · 6 · 9 · 9 · 6 · 9 · 6 → **57 · `BLOCKED`**
**Residual gaps:**
- Two observability versions. Pick one; finish the OTel wiring.
- No proof that a `trace_id` spans an agent call end-to-end (Layer 4 boundary).
- Workflow-health dashboard + policy-violation alerts not wired.

### Layer 9 — Evals · Quality Lead
**Modules:** `evals/` — `lead_intelligence_eval.yaml`, `company_brain_eval.yaml`,
`outreach_quality_eval.yaml`, `governance_eval.yaml`, `arabic_quality_eval.yaml`,
`revenue_os_cases.jsonl`, `personal_operator_cases.jsonl`.
**Scorecard:** 9 · 6 · 12.5 · 6 · 9 · 6 · 6 · 6 → **60 · `BLOCKED`**
**Residual gaps:**
- Eval packs exist but are **not wired as release gates** — the single biggest
  reason every other layer is unproven.
- No eval coverage for the proof workflow's lead-qualification path.
- No eval runner in CI.

### Layer 10 — Delivery Playbooks · Delivery Lead
**Modules:** `docs/playbooks/` (16 sector/function playbooks).
**Scorecard:** 9 · 6 · 6 · 6 · 9 · 6 · 6 · 9 → **57 · `BLOCKED`**
**Residual gaps:**
- No delivery / onboarding / QA / monthly-review playbook for the proof
  workflow itself.
- No evidence a playbook was followed end-to-end to deliver a real handover.

### Layer 11 — Continuous Improvement · PM / Founder
**Modules:** `auto_client_acquisition/friction_log/`, `bottleneck_radar/`,
`learning_flywheel/`, `.github/workflows/weekly_self_improvement.yml`.
**Scorecard:** 9 · 6 · 6 · 6 · 9 · 6 · 6 · 6 → **54 · `BLOCKED`**
**Residual gaps:**
- Friction is captured, but there is no closed loop from friction → release.
- No metric for how much captured friction actually got fixed.

---

## 3. What this means — ماذا يعني هذا

| Decision | Implication |
|----------|-------------|
| Sell now | Only on the strength of Layer 7 (Governance, `FIX`) and the existing commercial gates — **not** on a clean readiness `PASS`. |
| Build now | **Stop adding modules.** Per-capability consolidation comes first. |
| Next 30 days | Drive **one** workflow's slice of all 11 layers to `PASS` — see [`30_day_proof_workflow_plan.md`](30_day_proof_workflow_plan.md). |

The path to enterprise is not 200 modules at 57/100. It is **one workflow at
90+/100, proven across every layer.**

---

## ملخص بالعربية

Dealix غني بالقدرات وفقير بالإثبات: 0 PASS، 3 FIX (الأساس، العزل، الحوكمة)،
و8 BLOCKED. السبب ليس نقص القدرة بل ثلاثة أمور: التقييمات ليست بوابات إصدار،
ولا يوجد تراجع مُجرَّب، وتشعّب الإصدارات (`_v6`/`_v10` ونسخ مكرّرة) يمنع وجود
نسخة قانونية واحدة لكل قدرة. الطريق إلى الجاهزية المؤسسية ليس 200 وحدة بدرجة
57، بل مسار عمل واحد بدرجة 90+ مُثبَت عبر كل الطبقات.
