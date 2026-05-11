from __future__ import annotations

from pathlib import Path

from saudi_ai_provider.launch_ops import build_launch_pack, render_offer_stack, services_for_segment
from saudi_ai_provider.verifier import VerificationResult


def _passing_verification() -> VerificationResult:
    return VerificationResult(
        sellable_now=True,
        deliverable_now=True,
        operable_now=True,
        compliance_now=True,
        blockers=[],
        deliverability_blockers=[],
        operability_blockers=[],
        compliance_blockers=[],
        marker_results={},
        next_founder_action="Start enterprise demos this week.",
    )


def test_services_for_segment_enterprise_has_high_value_offers() -> None:
    services = services_for_segment("enterprise")
    assert services
    service_ids = {service["service_id"] for service in services}
    assert "AI_GOVERNANCE_OS" in service_ids
    assert "AI_REVENUE_COMMAND_CENTER" in service_ids


def test_render_offer_stack_outputs_pricing_lines() -> None:
    output = render_offer_stack(segment="enterprise", lang="ar")
    assert "حزمة الخدمات التنفيذية" in output
    assert "Setup SAR" in output
    assert "Monthly SAR" in output


def test_build_launch_pack_writes_markdown(tmp_path: Path) -> None:
    target = tmp_path / "launch_pack.md"
    result = build_launch_pack(
        segment="enterprise",
        lang="ar",
        verification=_passing_verification(),
        output_path=target,
    )
    assert result.output_path == target
    text = target.read_text(encoding="utf-8")
    assert "SELLABLE_NOW: true" in text
    assert "launch_ready: yes" in text
