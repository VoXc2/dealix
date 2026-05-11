"""Hermes/OpenClaw service application planner."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .catalog import load_agent_profiles
from .launch_ops import services_for_segment

VALID_PROFILES = {"hermes_agents", "openclaw_runtime", "hybrid_governed_execution"}


@dataclass(frozen=True)
class AgentApplicationPlan:
    service_id: str
    profile: str
    business_goal: str
    applications: list[str]
    core_strengths: list[str]
    kpi_focus: list[str]
    guardrails: list[str]
    rollout_steps: list[str]


def _load_data() -> dict[str, Any]:
    return load_agent_profiles()


def recommended_profile_for_service(service_id: str) -> str:
    data = _load_data()
    recs = data.get("service_profile_recommendations", {})
    profile = recs.get(service_id)
    if profile not in VALID_PROFILES:
        raise ValueError(f"No Hermes/OpenClaw profile recommendation for service '{service_id}'")
    return profile


def _resolve_profile(service_id: str, profile: str | None) -> str:
    if profile:
        if profile not in VALID_PROFILES:
            raise ValueError(
                f"Invalid profile '{profile}'. Valid profiles: {sorted(VALID_PROFILES)}"
            )
        return profile
    return recommended_profile_for_service(service_id)


def build_agent_application_plan(service_id: str, profile: str | None = None) -> AgentApplicationPlan:
    data = _load_data()
    service_apps = data.get("service_applications", {})
    profiles = data.get("profiles", {})
    if service_id not in service_apps:
        raise ValueError(f"Service '{service_id}' is not mapped in service_applications")

    chosen_profile = _resolve_profile(service_id, profile)
    profile_data = profiles.get(chosen_profile)
    if not profile_data:
        raise ValueError(f"Profile '{chosen_profile}' not found in profiles config")

    service_data = service_apps[service_id]
    guardrails = [
        "no_cold_whatsapp",
        "no_linkedin_automation",
        "no_scraping",
        "no_live_send_without_approval",
        "no_live_charge_without_approval",
        "no_public_proof_without_consent",
    ]
    rollout_steps = [
        "Baseline current workflow KPIs and risk controls.",
        "Map Hermes/OpenClaw profile to service playbook and owners.",
        "Enable approval gates and action-mode policy for all external actions.",
        "Run shadow mode for 7-14 days with evidence logging.",
        "Promote to controlled production with weekly executive review.",
    ]
    return AgentApplicationPlan(
        service_id=service_id,
        profile=chosen_profile,
        business_goal=service_data["business_goal"],
        applications=list(service_data["applications"]),
        core_strengths=list(profile_data["core_strengths"]),
        kpi_focus=list(profile_data["kpi_focus"]),
        guardrails=guardrails,
        rollout_steps=rollout_steps,
    )


def render_agent_application_plan(service_id: str, profile: str | None = None, lang: str = "ar") -> str:
    plan = build_agent_application_plan(service_id=service_id, profile=profile)
    lines: list[str] = []
    if lang == "ar":
        lines.append(f"خطة تطبيق Hermes/OpenClaw — {plan.service_id}")
        lines.append(f"الملف المقترح: {plan.profile}")
        lines.append(f"الهدف التجاري: {plan.business_goal}")
        lines.append("أفضل التطبيقات داخل الخدمة:")
    else:
        lines.append(f"Hermes/OpenClaw Application Plan — {plan.service_id}")
        lines.append(f"Recommended profile: {plan.profile}")
        lines.append(f"Business goal: {plan.business_goal}")
        lines.append("Best in-service applications:")
    for item in plan.applications:
        lines.append(f"- {item}")

    lines.append("Core strengths:")
    for item in plan.core_strengths:
        lines.append(f"- {item}")

    lines.append("KPI focus:")
    for item in plan.kpi_focus:
        lines.append(f"- {item}")

    lines.append("Guardrails:")
    for item in plan.guardrails:
        lines.append(f"- {item}")

    lines.append("Rollout steps:")
    for idx, step in enumerate(plan.rollout_steps, start=1):
        lines.append(f"{idx}. {step}")
    return "\n".join(lines)


def render_segment_rollout_plan(
    segment: str,
    profile: str | None = None,
    lang: str = "ar",
) -> str:
    services = services_for_segment(segment)
    if not services:
        raise ValueError(f"No services found for segment '{segment}'")

    lines: list[str] = []
    if lang == "ar":
        lines.append(f"خطة دمج Hermes/OpenClaw للشريحة: {segment}")
    else:
        lines.append(f"Hermes/OpenClaw rollout for segment: {segment}")

    for svc in services:
        service_id = svc["service_id"]
        resolved_profile = _resolve_profile(service_id, profile)
        lines.append(f"- {service_id}: {resolved_profile}")
    return "\n".join(lines)
