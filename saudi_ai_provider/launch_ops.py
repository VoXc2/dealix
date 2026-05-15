"""Final launch and enterprise offer-stack helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .catalog import load_final_service_stack
from .verifier import VerificationResult


@dataclass(frozen=True)
class LaunchPackResult:
    output_path: Path
    included_services: list[str]
    segment: str
    lang: str


def services_for_segment(segment: str) -> list[dict[str, Any]]:
    stack = load_final_service_stack()
    services = stack.get("services", [])
    return [svc for svc in services if segment in svc.get("target_segments", [])]


def render_offer_stack(segment: str, lang: str = "ar") -> str:
    services = services_for_segment(segment)
    if not services:
        raise ValueError(f"No services configured for segment '{segment}'")

    lines: list[str] = []
    if lang == "ar":
        lines.append(f"حزمة الخدمات التنفيذية — الشريحة: {segment}")
        lines.append("النموذج التجاري: Setup + Managed Retainer + Expansion")
    else:
        lines.append(f"Executive Service Stack — Segment: {segment}")
        lines.append("Commercial model: Setup + Managed Retainer + Expansion")

    for service in services:
        service_id = service["service_id"]
        outcome = service["core_outcome"]
        buyers = ", ".join(service["buyers"])
        setup_min, setup_max = service["setup_fee_sar_range"]
        monthly_min, monthly_max = service["monthly_retainer_sar_range"]
        lines.append(f"- {service_id}")
        lines.append(f"  Outcome: {outcome}")
        lines.append(f"  Buyers: {buyers}")
        lines.append(f"  Setup SAR: {setup_min} - {setup_max}")
        lines.append(f"  Monthly SAR: {monthly_min} - {monthly_max}")
        lines.append("  KPI Targets:")
        for kpi in service["kpi_targets"]:
            lines.append(f"  - {kpi}")
    return "\n".join(lines)


def build_launch_pack(
    *,
    segment: str,
    lang: str,
    verification: VerificationResult,
    output_path: Path | None = None,
) -> LaunchPackResult:
    services = services_for_segment(segment)
    if not services:
        raise ValueError(f"No services configured for segment '{segment}'")

    target = output_path or Path("out/launch") / f"final_launch_pack_{segment}_{lang}.md"
    target.parent.mkdir(parents=True, exist_ok=True)

    stack_text = render_offer_stack(segment=segment, lang=lang)
    generated_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    readiness = (
        verification.sellable_now
        and verification.deliverable_now
        and verification.operable_now
        and verification.compliance_now
    )
    lines = [
        "# Dealix Final Launch Pack",
        f"- generated_at: {generated_at}",
        f"- segment: {segment}",
        f"- lang: {lang}",
        f"- launch_ready: {'yes' if readiness else 'no'}",
        "",
        "## Readiness Verdict",
        f"- SELLABLE_NOW: {'true' if verification.sellable_now else 'false'}",
        f"- DELIVERABLE_NOW: {'true' if verification.deliverable_now else 'false'}",
        f"- OPERABLE_NOW: {'true' if verification.operable_now else 'false'}",
        f"- COMPLIANCE_NOW: {'true' if verification.compliance_now else 'false'}",
        f"- NEXT_FOUNDER_ACTION: {verification.next_founder_action}",
        "",
        "## Executive Offer Stack",
        stack_text,
    ]
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return LaunchPackResult(
        output_path=target,
        included_services=[service["service_id"] for service in services],
        segment=segment,
        lang=lang,
    )
