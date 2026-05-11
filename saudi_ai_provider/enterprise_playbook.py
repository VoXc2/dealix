"""Enterprise playbook generator for profile-aware customer delivery."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .agent_stack import build_agent_application_plan
from .commercial import _default_roi_inputs, generate_customer_proposal_bundle
from .kpis import kpis_for_service
from .playbooks import playbook_for_service
from .pricing import compute_roi, get_service_pricing, resolve_segment_by_employees


@dataclass(frozen=True)
class EnterprisePlaybookBundle:
    proposal: Path
    sow: Path
    kpi_contract: Path
    governance_contract: Path
    profile: str


def _write_kpi_contract(
    target: Path,
    *,
    service_id: str,
    company_name: str,
    profile: str,
    north_star: str,
    business_kpis: list[str],
    operational_kpis: list[str],
    guardrail_kpis: list[str],
    target_benchmarks: list[str],
    monthly_roi: float,
    annual_roi: float,
) -> None:
    lines = [
        f"# KPI Contract — {company_name}",
        "",
        f"- Service ID: {service_id}",
        f"- Profile: {profile}",
        f"- North Star: {north_star}",
        "",
        "## Business KPIs",
        *[f"- {item}" for item in business_kpis],
        "",
        "## Operational KPIs",
        *[f"- {item}" for item in operational_kpis],
        "",
        "## Guardrail KPIs",
        *[f"- {item}" for item in guardrail_kpis],
        "",
        "## Target Benchmarks",
        *[f"- {item}" for item in target_benchmarks],
        "",
        "## ROI Baseline",
        f"- Projected Monthly ROI: {monthly_roi} SAR",
        f"- Projected Annual ROI: {annual_roi} SAR",
        "",
        "## Evidence Requirements",
        "- before_after_kpi_baseline_export",
        "- workflow_execution_logs",
        "- approval_and_action_trace",
    ]
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_governance_contract(
    target: Path,
    *,
    service_id: str,
    company_name: str,
    profile: str,
    business_goal: str,
    applications: list[str],
    guardrails: list[str],
    rollout_steps: list[str],
    requirements: list[str],
    stopping_conditions: list[str],
    decision_gate: str,
    next_step: str,
    approval_required: bool,
) -> None:
    lines = [
        f"# Governance Contract — {company_name}",
        "",
        f"- Service ID: {service_id}",
        f"- Profile: {profile}",
        f"- Business Goal: {business_goal}",
        f"- Approval Required: {'yes' if approval_required else 'no'}",
        "",
        "## Governed Applications",
        *[f"- {item}" for item in applications],
        "",
        "## Guardrails",
        *[f"- {item}" for item in guardrails],
        "",
        "## Customer Requirements",
        *[f"- {item}" for item in requirements],
        "",
        "## Decision Gate",
        f"- {decision_gate}",
        "",
        "## Rollout Steps",
        *[f"{idx}. {step}" for idx, step in enumerate(rollout_steps, start=1)],
        "",
        "## Stopping Conditions",
        *[f"- {item}" for item in stopping_conditions],
        "",
        "## Next Step",
        f"- {next_step}",
    ]
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_enterprise_playbook_bundle(
    *,
    service_id: str,
    intake: dict,
    profile: str | None = None,
    segment: str | None = None,
    lang: str = "ar",
    output_dir: Path | None = None,
) -> EnterprisePlaybookBundle:
    employees = int(intake.get("company_size", intake.get("employees", 100)))
    resolved_segment = segment or resolve_segment_by_employees(employees)
    company_name = str(intake.get("company_name", "customer"))
    company_slug = "".join(c.lower() if c.isalnum() else "_" for c in company_name).strip("_")

    base_dir = output_dir or Path("out/offers/enterprise_playbooks") / company_slug
    base_dir.mkdir(parents=True, exist_ok=True)

    profile_plan = build_agent_application_plan(service_id, profile=profile)
    proposal_bundle = generate_customer_proposal_bundle(
        service_id=service_id,
        intake=intake,
        lang=lang,
        segment=resolved_segment,
        output_dir=base_dir,
    )

    kpis = kpis_for_service(service_id)
    playbook = playbook_for_service(service_id)
    pricing = get_service_pricing(service_id=service_id, segment=resolved_segment)
    roi = compute_roi(service_id, _default_roi_inputs(service_id, intake))

    stem = f"{service_id.lower()}_{company_slug}"
    kpi_contract = base_dir / f"{stem}_kpi_contract.md"
    governance_contract = base_dir / f"{stem}_governance_contract.md"

    _write_kpi_contract(
        kpi_contract,
        service_id=service_id,
        company_name=company_name,
        profile=profile_plan.profile,
        north_star=str(kpis["north_star"]),
        business_kpis=list(kpis["business_kpis"]),
        operational_kpis=list(kpis["operational_kpis"]),
        guardrail_kpis=list(kpis["guardrail_kpis"]),
        target_benchmarks=list(kpis["target_benchmarks"]),
        monthly_roi=roi.monthly_savings_sar,
        annual_roi=roi.annual_roi_sar,
    )

    _write_governance_contract(
        governance_contract,
        service_id=service_id,
        company_name=company_name,
        profile=profile_plan.profile,
        business_goal=profile_plan.business_goal,
        applications=profile_plan.applications,
        guardrails=profile_plan.guardrails,
        rollout_steps=profile_plan.rollout_steps,
        requirements=list(pricing.get("requires", [])) or ["Provide decision owner and data owner."],
        stopping_conditions=list(playbook["stopping_conditions"]),
        decision_gate=str(playbook["decision_gate"]),
        next_step=str(playbook["next_step"]),
        approval_required=True,
    )

    return EnterprisePlaybookBundle(
        proposal=proposal_bundle["proposal"],
        sow=proposal_bundle["sow"],
        kpi_contract=kpi_contract,
        governance_contract=governance_contract,
        profile=profile_plan.profile,
    )
