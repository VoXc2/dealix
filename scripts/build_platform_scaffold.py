#!/usr/bin/env python3
"""Dealix Enterprise Agentic Infrastructure — scaffold generator.

Builds the operating-model layer requested by the Enterprise Agentic
Infrastructure master prompt: /platform, /agents, /workflows, /governance,
/memory, /evals/*, /continuous_improvement, /releases, /changelogs, /versions.

Design rule (anti-duplication): Dealix already implements every capability
inside ``auto_client_acquisition/*`` (governance_os, agent_os, workflow_os,
knowledge_os, ...). This scaffold is a *governing operating-model layer*: it
indexes, documents, and scores those modules. It does NOT re-implement them.
Each generated ``architecture.md`` names the real module that implements the
capability, and each generated test asserts that module still exists on disk.

Idempotent: re-running overwrites generated docs but never deletes anything.

Usage:
    python scripts/build_platform_scaffold.py
    python scripts/build_platform_scaffold.py --check   # verify only, no write
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Ten enterprise-maturity dimensions (the "have you arrived?" model).
DIMENSIONS = [
    "observable",
    "governable",
    "evolvable",
    "measurable",
    "orchestrated",
    "workflow_native",
    "enterprise_safe",
    "agent_ready",
    "transformation_ready",
    "continuously_improving",
]


@dataclass
class System:
    key: str
    title: str
    path: str  # dir relative to repo root
    goal: str
    implemented_by: list[str]  # repo-relative paths to existing modules
    contract: str
    risk_tier: str  # low | medium | high | critical
    kpis: list[str]
    traces: list[str]
    dimensions: list[str]
    make_eval: bool = True


@dataclass
class Phase:
    num: int
    name: str
    goal: str
    systems: list[System] = field(default_factory=list)


def _sys(**kw) -> System:
    return System(**kw)


PHASES: list[Phase] = [
    Phase(1, "Foundation Maturity", "Turn Dealix from a project into a platform.", [
        _sys(key="foundation", title="Platform Foundation", path="platform/foundation",
             goal="Single bootstrap and capability registry for the whole platform.",
             implemented_by=["auto_client_acquisition/enterprise_os", "auto_client_acquisition/platform_v10"],
             contract="Inputs: tenant bootstrap request. Outputs: provisioned tenant + capability registry entry.",
             risk_tier="high",
             kpis=["tenant_provision_time_s", "capability_registry_coverage_pct", "bootstrap_success_rate"],
             traces=["foundation.bootstrap", "foundation.capability_register"],
             dimensions=["enterprise_safe", "transformation_ready"]),
        _sys(key="identity", title="Identity", path="platform/identity",
             goal="One identity per human, agent, and service principal.",
             implemented_by=["auto_client_acquisition/agent_identity_access_os", "api/security"],
             contract="Inputs: credential / token. Outputs: authenticated principal with claims.",
             risk_tier="critical",
             kpis=["auth_success_rate", "token_ttl_compliance_pct", "orphan_principal_count"],
             traces=["identity.authenticate", "identity.issue_token"],
             dimensions=["enterprise_safe", "governable"]),
        _sys(key="rbac", title="RBAC", path="platform/rbac",
             goal="No unrestricted access; no shared permissions.",
             implemented_by=["auto_client_acquisition/agent_identity_access_os", "api/security"],
             contract="Inputs: principal + resource + action. Outputs: allow / deny + reason.",
             risk_tier="critical",
             kpis=["unrestricted_role_count", "deny_decision_rate", "permission_review_age_days"],
             traces=["rbac.authorize"],
             dimensions=["governable", "enterprise_safe"]),
        _sys(key="multi_tenant", title="Multi-Tenant Architecture", path="platform/multi_tenant",
             goal="Every record bound to tenant_id; 100% data isolation.",
             implemented_by=["auto_client_acquisition/customer_data_plane", "auto_client_acquisition/data_os"],
             contract="Inputs: query scoped by tenant_id. Outputs: tenant-isolated result set.",
             risk_tier="critical",
             kpis=["cross_tenant_leak_count", "tenant_id_coverage_pct", "isolation_test_pass_rate"],
             traces=["multi_tenant.scope_query", "multi_tenant.provision"],
             dimensions=["enterprise_safe", "governable"]),
        _sys(key="security", title="Security", path="platform/security",
             goal="Secrets, encryption, and runtime hardening as a baseline, not an add-on.",
             implemented_by=["auto_client_acquisition/security_privacy",
                             "auto_client_acquisition/secure_agent_runtime_os", ".gitleaks.toml"],
             contract="Inputs: any request crossing a trust boundary. Outputs: hardened, audited request.",
             risk_tier="critical",
             kpis=["open_secret_findings", "mean_time_to_patch_h", "encrypted_at_rest_pct"],
             traces=["security.scan", "security.enforce_boundary"],
             dimensions=["enterprise_safe", "governable"]),
        _sys(key="deployment", title="Deployment / Infrastructure-as-Code", path="platform/deployment",
             goal="Reproducible, rollbackable deployments via IaC and CI.",
             implemented_by=["auto_client_acquisition/enterprise_rollout_os", "scripts/infra",
                             "Dockerfile", "docker-compose.yml", ".github"],
             contract="Inputs: release candidate. Outputs: staged deployment + rollback handle.",
             risk_tier="high",
             kpis=["deploy_lead_time_h", "rollback_time_min", "failed_deploy_rate"],
             traces=["deployment.stage", "deployment.promote", "deployment.rollback"],
             dimensions=["evolvable", "enterprise_safe"]),
        _sys(key="observability", title="Observability", path="platform/observability",
             goal="Traces, metrics, logs, and alerts from the first request.",
             implemented_by=["auto_client_acquisition/observability_v10",
                             "auto_client_acquisition/observability_adapters",
                             "auto_client_acquisition/auditability_os"],
             contract="Inputs: spans / metrics / log events. Outputs: queryable telemetry + alerts.",
             risk_tier="medium",
             kpis=["trace_coverage_pct", "alert_precision", "mean_time_to_detect_min"],
             traces=["observability.ingest", "observability.alert"],
             dimensions=["observable", "measurable"]),
    ]),
    Phase(2, "Agentic Runtime Maturity", "Run a governed digital workforce, not prompt->response.", [
        _sys(key="agents", title="Agent Catalog", path="agents",
             goal="Every agent has identity, role, permissions, memory scope, risk level, KPIs.",
             implemented_by=["auto_client_acquisition/agents", "auto_client_acquisition/ai_workforce_v10",
                             "core/agents"],
             contract="Inputs: agent goal. Outputs: agent card + governed execution result.",
             risk_tier="high",
             kpis=["governed_agent_pct", "agent_eval_pass_rate", "ungoverned_action_count"],
             traces=["agent.invoke", "agent.plan", "agent.execute"],
             dimensions=["agent_ready", "governable"]),
        _sys(key="agent_runtime", title="Agent Runtime", path="platform/agent_runtime",
             goal="goal -> plan -> memory -> tools -> execute -> validate -> approve -> analytics.",
             implemented_by=["auto_client_acquisition/agent_os",
                             "auto_client_acquisition/secure_agent_runtime_os",
                             "auto_client_acquisition/agentic_operations_os"],
             contract="Inputs: agent card + goal. Outputs: validated, approved, audited execution.",
             risk_tier="critical",
             kpis=["runtime_success_rate", "validation_block_rate", "p95_runtime_latency_ms"],
             traces=["runtime.plan", "runtime.tool_call", "runtime.validate", "runtime.approve"],
             dimensions=["agent_ready", "orchestrated", "governable"]),
        _sys(key="tool_registry", title="Tool Registry", path="platform/tool_registry",
             goal="Every tool is declared, permissioned, and guardrailed.",
             implemented_by=["auto_client_acquisition/agent_os/tool_permissions.py",
                             "auto_client_acquisition/tool_guardrail_gateway"],
             contract="Inputs: tool call request. Outputs: guardrail decision + scoped invocation.",
             risk_tier="high",
             kpis=["undeclared_tool_call_count", "guardrail_block_rate", "tool_permission_coverage_pct"],
             traces=["tool_registry.resolve", "tool_registry.guard"],
             dimensions=["agent_ready", "governable", "enterprise_safe"]),
        _sys(key="agent_memory", title="Agent Memory", path="platform/agent_memory",
             goal="Per-agent memory scope with isolation between agents and tenants.",
             implemented_by=["core/memory", "auto_client_acquisition/revenue_memory"],
             contract="Inputs: scoped read/write. Outputs: isolated agent memory.",
             risk_tier="high",
             kpis=["memory_scope_violation_count", "memory_recall_precision", "stale_memory_pct"],
             traces=["agent_memory.read", "agent_memory.write"],
             dimensions=["agent_ready", "enterprise_safe"]),
        _sys(key="escalation", title="Escalation", path="platform/escalation",
             goal="Every high-risk action escalates to a human above the loop.",
             implemented_by=["auto_client_acquisition/approval_center",
                             "auto_client_acquisition/governance_os/approval_matrix.py"],
             contract="Inputs: risky action. Outputs: human decision (approve / reject / modify).",
             risk_tier="high",
             kpis=["escalation_response_time_min", "auto_approved_high_risk_count", "escalation_sla_pct"],
             traces=["escalation.raise", "escalation.resolve"],
             dimensions=["governable", "enterprise_safe"]),
    ]),
    Phase(3, "Workflow Orchestration Maturity", "Value comes from workflow redesign, not AI alone.", [
        _sys(key="workflows", title="Workflow Catalog", path="workflows",
             goal="trigger -> conditions -> actions -> approvals -> retries -> compensation -> analytics.",
             implemented_by=["auto_client_acquisition/workflow_os",
                             "auto_client_acquisition/workflow_os_v10"],
             contract="Inputs: workflow trigger. Outputs: audited workflow run + analytics.",
             risk_tier="high",
             kpis=["workflow_completion_rate", "retry_success_rate", "unrecovered_failure_count"],
             traces=["workflow.trigger", "workflow.step", "workflow.compensate"],
             dimensions=["workflow_native", "orchestrated"]),
        _sys(key="workflow_engine", title="Workflow Engine", path="platform/workflow_engine",
             goal="Durable execution with retries, fallback, and compensation.",
             implemented_by=["auto_client_acquisition/workflow_os",
                             "auto_client_acquisition/workflow_os_v10"],
             contract="Inputs: workflow definition + event. Outputs: durable run state.",
             risk_tier="high",
             kpis=["engine_uptime_pct", "stuck_run_count", "p95_step_latency_ms"],
             traces=["workflow_engine.advance", "workflow_engine.retry"],
             dimensions=["workflow_native", "evolvable", "observable"]),
        _sys(key="orchestration", title="Orchestration", path="platform/orchestration",
             goal="Event-driven coordination of agents and workflows.",
             implemented_by=["auto_client_acquisition/orchestrator",
                             "auto_client_acquisition/agentic_operations_os"],
             contract="Inputs: event. Outputs: routed agent/workflow invocations.",
             risk_tier="high",
             kpis=["event_lag_ms", "orchestration_error_rate", "fan_out_depth"],
             traces=["orchestration.route", "orchestration.dispatch"],
             dimensions=["orchestrated", "workflow_native"]),
        _sys(key="execution_engine", title="Execution Engine", path="platform/execution_engine",
             goal="Deterministic execution of approved actions with full audit.",
             implemented_by=["auto_client_acquisition/execution_os",
                             "auto_client_acquisition/delivery_factory"],
             contract="Inputs: approved action. Outputs: executed + audit-logged result.",
             risk_tier="high",
             kpis=["execution_success_rate", "unaudited_execution_count", "p95_execution_latency_ms"],
             traces=["execution.run", "execution.audit"],
             dimensions=["orchestrated", "governable", "observable"]),
    ]),
    Phase(4, "Organizational Memory Maturity", "Proprietary operational memory is the moat.", [
        _sys(key="knowledge", title="Knowledge", path="platform/knowledge",
             goal="Ingestion + metadata + permission-aware enterprise knowledge.",
             implemented_by=["auto_client_acquisition/knowledge_os",
                             "auto_client_acquisition/company_brain"],
             contract="Inputs: documents + metadata. Outputs: indexed, permissioned knowledge.",
             risk_tier="medium",
             kpis=["ingestion_throughput_docs_h", "metadata_completeness_pct", "index_freshness_h"],
             traces=["knowledge.ingest", "knowledge.index"],
             dimensions=["transformation_ready", "measurable"]),
        _sys(key="retrieval", title="Retrieval", path="platform/retrieval",
             goal="Hybrid, permission-aware retrieval with citations and lineage.",
             implemented_by=["auto_client_acquisition/intelligence_os",
                             "auto_client_acquisition/revenue_memory"],
             contract="Inputs: query + principal. Outputs: ranked passages + citations + lineage.",
             risk_tier="medium",
             kpis=["retrieval_recall_at_10", "citation_coverage_pct", "permission_filtered_pct"],
             traces=["retrieval.search", "retrieval.cite"],
             dimensions=["transformation_ready", "governable", "measurable"]),
        _sys(key="reranking", title="Reranking", path="platform/reranking",
             goal="Confidence-scored reranking on top of first-stage retrieval.",
             implemented_by=["auto_client_acquisition/intelligence_os",
                             "auto_client_acquisition/intelligence"],
             contract="Inputs: candidate passages. Outputs: reranked passages + confidence.",
             risk_tier="low",
             kpis=["rerank_ndcg_at_10", "low_confidence_answer_pct", "rerank_latency_ms"],
             traces=["reranking.score"],
             dimensions=["measurable", "transformation_ready"]),
        _sys(key="memory", title="Organizational Memory", path="memory",
             goal="Durable organizational memory with lineage and permission-aware recall.",
             implemented_by=["auto_client_acquisition/revenue_memory", "core/memory"],
             contract="Inputs: events + decisions. Outputs: lineage-tracked organizational memory.",
             risk_tier="medium",
             kpis=["memory_lineage_coverage_pct", "answer_with_source_pct", "memory_growth_rate"],
             traces=["memory.append", "memory.recall"],
             dimensions=["transformation_ready", "continuously_improving"]),
    ]),
    Phase(5, "Governance Maturity", "Governance is runtime-enforced, not documentation.", [
        _sys(key="governance", title="Governance", path="governance",
             goal="Every action passes risk scoring -> policy -> approval -> execution -> audit.",
             implemented_by=["auto_client_acquisition/governance_os", "dealix/governance"],
             contract="Inputs: proposed action. Outputs: governed decision + audit record.",
             risk_tier="critical",
             kpis=["ungoverned_action_count", "policy_coverage_pct", "audit_completeness_pct"],
             traces=["governance.evaluate", "governance.audit"],
             dimensions=["governable", "enterprise_safe"]),
        _sys(key="policy_engine", title="Policy Engine", path="platform/policy_engine",
             goal="Declarative policies validated at runtime on every action.",
             implemented_by=["auto_client_acquisition/governance_os/policy_registry.py",
                             "auto_client_acquisition/governance_os/policy_check.py"],
             contract="Inputs: action + context. Outputs: policy verdict + violated rules.",
             risk_tier="critical",
             kpis=["policy_eval_count", "policy_violation_rate", "policy_eval_latency_ms"],
             traces=["policy_engine.check"],
             dimensions=["governable", "enterprise_safe"]),
        _sys(key="approval_engine", title="Approval Engine", path="platform/approval_engine",
             goal="Risk-tiered approval routing with SLAs and an approval matrix.",
             implemented_by=["auto_client_acquisition/governance_os/approval_matrix.py",
                             "auto_client_acquisition/approval_center"],
             contract="Inputs: action requiring approval. Outputs: routed approval decision.",
             risk_tier="high",
             kpis=["approval_sla_pct", "pending_approval_count", "approval_cycle_time_h"],
             traces=["approval_engine.route", "approval_engine.decide"],
             dimensions=["governable"]),
        _sys(key="risk_engine", title="Risk Engine", path="platform/risk_engine",
             goal="Score every action's risk before it runs.",
             implemented_by=["auto_client_acquisition/risk_resilience_os",
                             "auto_client_acquisition/governance_os/runtime_decision.py"],
             contract="Inputs: action + context. Outputs: risk score + tier + required controls.",
             risk_tier="high",
             kpis=["high_risk_action_pct", "risk_model_calibration_error", "unscored_action_count"],
             traces=["risk_engine.score"],
             dimensions=["governable", "measurable", "enterprise_safe"]),
    ]),
    Phase(6, "Evaluation Maturity", "Nothing reaches production without evals.", [
        _sys(key="retrieval", title="Retrieval Evals", path="evals/retrieval",
             goal="Recall, citation accuracy, and permission-leak checks for retrieval.",
             implemented_by=["evals/lead_intelligence_eval.yaml", "tests/governance"],
             contract="Inputs: retrieval cases. Outputs: pass/fail + recall/citation scores.",
             risk_tier="medium",
             kpis=["retrieval_eval_pass_rate", "citation_accuracy", "permission_leak_count"],
             traces=["evals.retrieval.run"],
             dimensions=["measurable", "continuously_improving"], make_eval=False),
        _sys(key="hallucination", title="Hallucination Evals", path="evals/hallucination",
             goal="Detect unsupported claims and ungrounded answers.",
             implemented_by=["evals/arabic_quality_eval.yaml", "tests/governance"],
             contract="Inputs: answer + sources. Outputs: groundedness verdict.",
             risk_tier="high",
             kpis=["hallucination_rate", "groundedness_score", "unsupported_claim_count"],
             traces=["evals.hallucination.run"],
             dimensions=["measurable", "enterprise_safe"], make_eval=False),
        _sys(key="workflow_execution", title="Workflow Execution Evals", path="evals/workflow_execution",
             goal="Verify workflows complete, retry, compensate, and audit correctly.",
             implemented_by=["evals/revenue_os_cases.jsonl", "tests/governance"],
             contract="Inputs: workflow scenarios. Outputs: execution-correctness verdict.",
             risk_tier="high",
             kpis=["workflow_eval_pass_rate", "compensation_correctness", "audit_gap_count"],
             traces=["evals.workflow.run"],
             dimensions=["measurable", "workflow_native"], make_eval=False),
        _sys(key="agent_behavior", title="Agent Behavior Evals", path="evals/agent_behavior",
             goal="Verify agents stay inside governance, memory, and tool boundaries.",
             implemented_by=["evals/personal_operator_cases.jsonl", "tests/governance"],
             contract="Inputs: agent scenarios. Outputs: behavior-conformance verdict.",
             risk_tier="high",
             kpis=["agent_eval_pass_rate", "boundary_violation_count", "tool_misuse_count"],
             traces=["evals.agent.run"],
             dimensions=["measurable", "agent_ready"], make_eval=False),
        _sys(key="governance", title="Governance Evals", path="evals/governance",
             goal="Verify policy, approval, and audit enforcement holds under test.",
             implemented_by=["evals/governance_eval.yaml", "tests/governance"],
             contract="Inputs: governance scenarios. Outputs: enforcement verdict.",
             risk_tier="critical",
             kpis=["governance_eval_pass_rate", "enforcement_gap_count", "audit_coverage_pct"],
             traces=["evals.governance.run"],
             dimensions=["measurable", "governable"], make_eval=False),
        _sys(key="business_impact", title="Business Impact Evals", path="evals/business_impact",
             goal="Tie platform behavior to ROI and operational outcomes.",
             implemented_by=["evals/outreach_quality_eval.yaml", "evals/company_brain_eval.yaml"],
             contract="Inputs: outcome scenarios. Outputs: business-impact score.",
             risk_tier="medium",
             kpis=["roi_eval_pass_rate", "value_realized_per_run", "impact_attribution_pct"],
             traces=["evals.business_impact.run"],
             dimensions=["measurable", "continuously_improving"], make_eval=False),
    ]),
    Phase(7, "Continuous Evolution Maturity", "Systems that evolve safely, forever.", [
        _sys(key="continuous_improvement", title="Continuous Improvement", path="continuous_improvement",
             goal="Feedback loops and regression detection feeding safe change.",
             implemented_by=["auto_client_acquisition/learning_flywheel",
                             "auto_client_acquisition/self_growth_os"],
             contract="Inputs: feedback + telemetry. Outputs: prioritized, gated improvements.",
             risk_tier="medium",
             kpis=["regression_detection_rate", "improvement_cycle_time_d", "feedback_actioned_pct"],
             traces=["improvement.detect", "improvement.gate"],
             dimensions=["continuously_improving", "evolvable"]),
        _sys(key="releases", title="Releases", path="releases",
             goal="Staged rollouts with evaluation and observability gates.",
             implemented_by=["auto_client_acquisition/enterprise_rollout_os"],
             contract="Inputs: release candidate. Outputs: gated, staged release.",
             risk_tier="high",
             kpis=["release_gate_pass_rate", "staged_rollout_pct", "post_release_incident_count"],
             traces=["release.gate", "release.stage"],
             dimensions=["evolvable", "continuously_improving"]),
        _sys(key="changelogs", title="Changelogs", path="changelogs",
             goal="Every change is recorded and attributable.",
             implemented_by=["CHANGELOG.md"],
             contract="Inputs: merged change. Outputs: changelog entry.",
             risk_tier="low",
             kpis=["changelog_coverage_pct", "undocumented_change_count"],
             traces=["changelog.record"],
             dimensions=["evolvable", "observable"]),
        _sys(key="versions", title="Versions", path="versions",
             goal="Every artifact is versioned and rollbackable.",
             implemented_by=["auto_client_acquisition/enterprise_rollout_os"],
             contract="Inputs: artifact. Outputs: version record + rollback handle.",
             risk_tier="medium",
             kpis=["versioned_artifact_pct", "rollback_success_rate"],
             traces=["versions.tag", "versions.rollback"],
             dimensions=["evolvable", "continuously_improving"]),
    ]),
]

ARTIFACTS = ["architecture.md", "readiness.md", "observability.md",
             "rollback.md", "metrics.md", "risk_model.md"]


def _modules_md(s: System) -> str:
    lines = []
    for m in s.implemented_by:
        exists = "" if (REPO / m).exists() else "  **(MISSING — investigate)**"
        lines.append(f"- `{m}`{exists}")
    return "\n".join(lines)


def architecture_md(s: System, ph: Phase) -> str:
    return f"""# {s.title} — Architecture

> Phase {ph.num}: {ph.name}
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

{s.goal}

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

{_modules_md(s)}

## Contract

{s.contract}

## Position in the operating model

- Risk tier: **{s.risk_tier}**
- Maturity dimensions advanced: {", ".join(s.dimensions)}
- Required companion artifacts: {", ".join(ARTIFACTS)}, `tests/`{", `evals/`" if s.make_eval else ""}

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
"""


def readiness_md(s: System) -> str:
    rows = "\n".join(
        f"| {d} | {'core' if d in s.dimensions else 'supporting'} | ☐ |"
        for d in DIMENSIONS
    )
    return f"""# {s.title} — Readiness

## Maturity checklist

| Dimension | Relevance | Verified |
|-----------|-----------|----------|
{rows}

## How you know you have arrived

- [ ] Every implementing module listed in `architecture.md` exists and imports cleanly.
- [ ] `tests/` for this system pass in CI.
- [ ] Telemetry in `observability.md` is emitting in a live environment.
- [ ] `rollback.md` procedure has been dry-run at least once.
- [ ] KPIs in `metrics.md` have live values, not placeholders.
- [ ] `risk_model.md` risk tier is reviewed and accepted by an owner.

Until all boxes are checked, this system is **scaffolded**, not **verified**.
"""


def observability_md(s: System) -> str:
    traces = "\n".join(f"- `{t}`" for t in s.traces)
    return f"""# {s.title} — Observability

## Traces

{traces}

## Metrics

See `metrics.md` — every KPI there must be exported as a metric.

## Logs

Structured logs MUST include `tenant_id`, `principal_id`, `trace_id`, and
`action`. No log line crosses a tenant boundary.

## Alerts

| Condition | Severity | Routes to |
|-----------|----------|-----------|
| KPI breaches its target threshold | warning | owning team |
| Risk-tier-{s.risk_tier} failure | page | on-call (`docs/ON_CALL.md`) |

Backed by: `auto_client_acquisition/observability_v10`, `auto_client_acquisition/auditability_os`.
"""


def rollback_md(s: System, ph: Phase) -> str:
    return f"""# {s.title} — Rollback

## Blast radius

Risk tier **{s.risk_tier}**. A failure here affects: {", ".join(s.dimensions)}.

## Procedure

1. Detect via the alerts in `observability.md`.
2. Freeze new traffic to this system (feature flag / route disable).
3. Roll the implementing modules back to the last known-good version
   (`releases/`, `versions/`, `auto_client_acquisition/enterprise_rollout_os`).
4. Re-run this system's `tests/` and Phase {ph.num} evals before un-freezing.
5. Record the incident in `changelogs/` and `auto_client_acquisition/auditability_os`.

## Approval

Rollback of a **{s.risk_tier}**-tier system is authorized by the system owner;
critical-tier rollbacks also notify the founder (humans above the loop).
"""


def metrics_md(s: System) -> str:
    rows = "\n".join(f"| `{k}` | _set target_ | _live value_ |" for k in s.kpis)
    return f"""# {s.title} — Metrics

| KPI | Target | Current |
|-----|--------|---------|
{rows}

Targets are owned by the system owner and reviewed in the weekly operating
review (`docs/company/WEEKLY_OPERATING_REVIEW.md`). Placeholder values mean the
system is not yet **measurable** — see `readiness.md`.
"""


def risk_model_md(s: System) -> str:
    return f"""# {s.title} — Risk Model

## Risk tier

**{s.risk_tier}**

## Risk factors

- Failure mode: incorrect or unavailable output from {s.title}.
- Governance exposure: any action here must still pass the governance chain
  (risk score -> policy -> approval -> execution -> audit).
- Data exposure: must respect `tenant_id` isolation and permission-aware access.

## Scoring

Each action routed through this system is scored by
`auto_client_acquisition/risk_resilience_os` and
`auto_client_acquisition/governance_os/runtime_decision.py`. Actions above the
**{s.risk_tier}** threshold escalate (see `platform/escalation`).

## Mitigations

- Retries + compensation (`platform/workflow_engine`).
- Rollback (`rollback.md`).
- Continuous evals (Phase 6).
- Human above the loop for high/critical actions.
"""


def test_py(s: System) -> str:
    safe = s.key.replace("-", "_")
    mods = repr(s.implemented_by)
    arts = repr(ARTIFACTS)
    rel = s.path
    return f'''"""Self-verification for the {s.title} operating-model system.

Asserts the scaffold is intact and still maps to real modules. This is the
anti-drift guard: if an implementing module is renamed or deleted, this fails.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parents[{len(Path(rel).parts) + 1}]
SYSTEM_DIR = REPO / "{rel}"
IMPLEMENTED_BY = {mods}
ARTIFACTS = {arts}


def test_artifacts_present():
    for name in ARTIFACTS:
        path = SYSTEM_DIR / name
        assert path.exists(), f"missing artifact: {{path}}"
        assert path.read_text(encoding="utf-8").strip(), f"empty artifact: {{path}}"


def test_implementing_modules_exist():
    missing = [m for m in IMPLEMENTED_BY if not (REPO / m).exists()]
    assert not missing, (
        f"{s.title} architecture.md references modules that no longer exist: "
        f"{{missing}}. Update architecture.md or restore the modules."
    )
'''


def eval_yaml(s: System) -> str:
    return f"""# {s.title} — eval spec
# Phase {[p.num for p in PHASES if s in p.systems][0]} evaluation gate.
system: {s.key}
path: {s.path}
description: {s.goal}
gate: nothing reaches production without this eval passing.
metrics:
{chr(10).join(f"  - {k}" for k in s.kpis)}
cases: []  # add concrete cases; wire to auto_client_acquisition runners.
"""


def maturity_os_md() -> str:
    phase_blocks = []
    for ph in PHASES:
        sys_lines = "\n".join(
            f"| {s.title} | `{s.path}` | {s.risk_tier} | {', '.join(s.implemented_by[:2])} |"
            for s in ph.systems
        )
        phase_blocks.append(
            f"### Phase {ph.num} — {ph.name}\n\n"
            f"_{ph.goal}_\n\n"
            f"| System | Path | Risk | Implemented by |\n"
            f"|--------|------|------|----------------|\n{sys_lines}\n"
        )
    total = sum(len(p.systems) for p in PHASES)
    return f"""# Dealix Enterprise Maturity Operating System

> Goal: **The operating infrastructure layer for the agentic enterprise.**

This is the governing operating-model layer over Dealix. It does **not**
re-implement the {total} systems below — every system maps to existing modules
in `auto_client_acquisition/*`, `core/*`, `dealix/*`, `api/*`. This layer
**indexes, documents, scores, and gates** them.

## How to know you have arrived

Do not measure features. Measure organizational capability across ten
dimensions: {", ".join(DIMENSIONS)}.

Run the scorer:

```bash
python platform/readiness_model.py
```

It prints `DEALIX_ENTERPRISE_MATURITY_VERDICT` and a per-dimension score.

## The seven phases

{chr(10).join(phase_blocks)}

## Operating rules

Every system ships: `architecture.md`, `readiness.md`, `observability.md`,
`rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
Every deployment: staged rollout + eval checks + observability verification +
rollback readiness.
Every workflow: retries + failure recovery + audit logging + approvals +
analytics.
Every agent: governance boundaries + memory isolation + tool permissions +
escalation rules + runtime validation.

Architecture principles: AI-first workflows; humans **above** the loop; governed
autonomy; event-driven orchestration; policy-enforced execution; continuous
evaluation; safe evolution.

_Generated by `scripts/build_platform_scaffold.py` — edit that, not the output._
"""


def readiness_manifest_yaml() -> str:
    lines = ["# Generated by scripts/build_platform_scaffold.py",
             "# Drives platform/readiness_model.py. module_status reflects the",
             "# underlying code; operating_layer_status reflects this governing layer.",
             f"dimensions: [{', '.join(DIMENSIONS)}]",
             "systems:"]
    for ph in PHASES:
        for s in ph.systems:
            mods_exist = all((REPO / m).exists() for m in s.implemented_by)
            lines += [
                f"  - key: {s.key}",
                f"    phase: {ph.num}",
                f"    path: {s.path}",
                f"    risk_tier: {s.risk_tier}",
                f"    dimensions: [{', '.join(s.dimensions)}]",
                f"    module_status: {'implemented' if mods_exist else 'incomplete'}",
                f"    operating_layer_status: scaffolded",
            ]
    return "\n".join(lines) + "\n"


def build(check_only: bool) -> int:
    problems: list[str] = []
    written = 0
    for ph in PHASES:
        for s in ph.systems:
            sysdir = REPO / s.path
            slug = s.path.replace("/", "_")
            files = {
                "architecture.md": architecture_md(s, ph),
                "readiness.md": readiness_md(s),
                "observability.md": observability_md(s),
                "rollback.md": rollback_md(s, ph),
                "metrics.md": metrics_md(s),
                "risk_model.md": risk_model_md(s),
                f"tests/test_{slug}.py": test_py(s),
            }
            if s.make_eval:
                files[f"evals/{s.key}_eval.yaml"] = eval_yaml(s)
            for rel, content in files.items():
                target = sysdir / rel
                if check_only:
                    if not target.exists():
                        problems.append(f"missing: {target}")
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
                written += 1
            for m in s.implemented_by:
                if not (REPO / m).exists():
                    problems.append(f"{s.key}: implementing module not found: {m}")

    extras = {
        "platform/ENTERPRISE_MATURITY_OS.md": maturity_os_md(),
        "platform/readiness_manifest.yaml": readiness_manifest_yaml(),
    }
    for rel, content in extras.items():
        target = REPO / rel
        if check_only:
            if not target.exists():
                problems.append(f"missing: {target}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written += 1

    if check_only:
        if problems:
            print("SCAFFOLD CHECK: FAIL")
            for p in problems:
                print(f"  - {p}")
            return 1
        print("SCAFFOLD CHECK: OK")
        return 0

    print(f"Scaffold written: {written} files across {sum(len(p.systems) for p in PHASES)} systems.")
    if problems:
        print("WARNINGS (module mapping drift):")
        for p in problems:
            print(f"  - {p}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="verify scaffold, do not write")
    args = ap.parse_args()
    sys.exit(build(check_only=args.check))
