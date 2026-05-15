# Dealix — Enterprise Agentic Infrastructure

> الهدف: تحويل Dealix من *AI SaaS* إلى **operating infrastructure layer for the
> agentic enterprise** — طبقة بنية تشغيلية لمؤسسات تعمل بالذكاء الاصطناعي أولاً.

This document is the charter for the enterprise operating-model layer. It maps
the seven maturity phases to the code that already implements them, and defines
how Dealix proves it has "arrived".

## Design principle — index, do not duplicate

Dealix already implements every capability the maturity model describes, inside
`auto_client_acquisition/*` (`governance_os`, `agent_os`, `workflow_os`,
`knowledge_os`, `secure_agent_runtime_os`, `observability_v10`, ...), plus
`core/*`, `dealix/*`, and `api/*`.

The new top-level layer — `platform/`, `agents/`, `workflows/`, `governance/`,
`memory/`, `evals/*`, `continuous_improvement/`, `releases/`, `changelogs/`,
`versions/` — is a **governing operating-model layer**, not a second
implementation. Each of its 34 systems:

- names the existing module(s) that implement it (`architecture.md`),
- carries the six required artifacts (`architecture.md`, `readiness.md`,
  `observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`),
- ships a `tests/` self-check that **fails if its implementing module is
  renamed or deleted** — an anti-drift guard.

The whole layer is generated and verified by
[`scripts/build_platform_scaffold.py`](../../scripts/build_platform_scaffold.py).
Edit the generator, not the generated files.

## The seven phases

| Phase | Maturity | Top-level home |
|-------|----------|----------------|
| 1 | Foundation — project → platform | `platform/` |
| 2 | Agentic Runtime — governed digital workforce | `agents/`, `platform/agent_runtime` ... |
| 3 | Workflow Orchestration — value via workflow redesign | `workflows/`, `platform/workflow_engine` ... |
| 4 | Organizational Memory — the moat | `platform/knowledge`, `memory/` ... |
| 5 | Governance — runtime-enforced, not docs | `governance/`, `platform/policy_engine` ... |
| 6 | Evaluation — nothing ships without evals | `evals/{retrieval,hallucination,...}` |
| 7 | Continuous Evolution — evolve safely, forever | `continuous_improvement/`, `releases/` ... |

Full system-by-system map: [`platform/ENTERPRISE_MATURITY_OS.md`](../../platform/ENTERPRISE_MATURITY_OS.md).

## How you know you have arrived — كيف تعرف أنك وصلت؟

Do not measure features. Measure **organizational capability** across ten
dimensions: `observable`, `governable`, `evolvable`, `measurable`,
`orchestrated`, `workflow_native`, `enterprise_safe`, `agent_ready`,
`transformation_ready`, `continuously_improving`.

```bash
python platform/readiness_model.py          # human-readable scorecard
python platform/readiness_model.py --json   # machine-readable
python scripts/build_platform_scaffold.py --check   # scaffold integrity
```

The scorer prints `DEALIX_ENTERPRISE_MATURITY_VERDICT`:

- **ARRIVED** — every dimension ≥ 85.
- **ON_TRACK** — every dimension ≥ 60. *(current state: capabilities exist in
  code; the governing layer is scaffolded but not yet verified.)*
- **EARLY** — at least one dimension below 60.

Raise the score by completing each system's `readiness.md` checklist:
implementing modules import cleanly, `tests/` pass in CI, telemetry is live,
rollback has been dry-run, KPIs hold real values, risk tier is owner-accepted.
Only then does a system move from **scaffolded** to **verified**.

## Operating rules

- Every deployment: staged rollout + eval checks + observability verification +
  rollback readiness.
- Every workflow: retries + failure recovery + audit logging + approvals +
  analytics.
- Every agent: governance boundaries + memory isolation + tool permissions +
  escalation rules + runtime validation.
- Every action: risk score → policy → approval → execution → audit.
- Humans stay **above** the loop, not in it.

---

## Architect charter (master prompt — reference)

> Preserved verbatim as the standing brief for any agent extending this layer.

You are the Chief Architect and Enterprise AI Transformation Engineer for
Dealix. Your mission is to evolve Dealix from an AI SaaS platform into a fully
enterprise-grade Agentic Operating Infrastructure platform capable of supporting
AI-first organizations, digital workforce orchestration, governed autonomy,
organizational intelligence, and enterprise workflow execution.

Think like: McKinsey AI transformation partner; enterprise systems architect;
AI infrastructure engineer; workflow orchestration architect; governance and
observability lead; agent runtime designer; organizational operating-model
strategist.

Responsibilities:

1. Build Dealix as a multi-tenant enterprise platform.
2. Design all systems as observable, governed, measurable, and evolvable.
3. Ensure all workflows are retryable, observable, auditable, governed, versioned.
4. Ensure all agents have identity, permissions, memory scope, risk levels,
   evaluation systems, governance enforcement.
5. Build organizational memory with citations, lineage, permission-aware
   retrieval, hybrid retrieval, reranking.
6. Build runtime governance: policy engines, approval engines, audit systems,
   risk scoring, compliance checks.
7. Build enterprise observability: traces, metrics, alerts, incident tracking,
   workflow analytics.
8. Build evaluation infrastructure: hallucination, workflow-execution,
   retrieval, governance, and business-impact evals.
9. Build continuous evolution: versioning, staged rollout, rollback, regression
   detection, feedback loops.
10. Build executive intelligence: operational insights, ROI tracking, strategic
    briefs, forecasting, organizational intelligence.

Architecture principles: AI-first workflows; humans above the loop; governed
autonomy; operational intelligence; workflow-native architecture; event-driven
orchestration; enterprise-grade observability; continuous evaluation; safe
evolution; modular infrastructure; policy-enforced execution.

Every system includes: `architecture.md`, `readiness.md`, `observability.md`,
`rollback.md`, `metrics.md`, `risk_model.md`, tests, evals. Every deployment
includes staged rollout, evaluation checks, observability verification, rollback
readiness. Every workflow includes retries, failure recovery, audit logging,
approvals, analytics. Every agent includes governance boundaries, memory
isolation, tool permissions, escalation rules, runtime validation.

Goal: evolve Dealix into *"the operating infrastructure layer for the agentic
enterprise."*

---

_Generated structure: `scripts/build_platform_scaffold.py`. Scorer:
`platform/readiness_model.py`. Guard test: `tests/test_platform_scaffold.py`._
