#!/usr/bin/env python3
"""Verify docs/services/<folder> contains required blueprint files."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]

REQUIRED_BY_FOLDER: dict[str, tuple[str, ...]] = {
    "lead_intelligence_sprint": (
        "offer.md",
        "scope.md",
        "intake.md",
        "data_request.md",
        "delivery_checklist.md",
        "qa_checklist.md",
        "report_template.md",
        "proof_pack_template.md",
        "sample_output.md",
        "handoff.md",
        "upsell.md",
    ),
    "ai_quick_win_sprint": (
        "offer.md",
        "scope.md",
        "process_intake.md",
        "workflow_map.md",
        "delivery_checklist.md",
        "qa_checklist.md",
        "roi_estimate.md",
        "proof_pack_template.md",
        "sample_output.md",
        "handoff.md",
        "upsell.md",
    ),
    "company_brain_sprint": (
        "offer.md",
        "scope.md",
        "document_request.md",
        "access_rules.md",
        "eval_cases.md",
        "delivery_checklist.md",
        "qa_checklist.md",
        "report_template.md",
        "proof_pack_template.md",
        "sample_output.md",
        "handoff.md",
        "upsell.md",
    ),
    "ai_support_desk_sprint": (
        "offer.md",
        "scope.md",
        "inbox_intake.md",
        "faq_request.md",
        "escalation_rules.md",
        "delivery_checklist.md",
        "qa_checklist.md",
        "support_report_template.md",
        "proof_pack_template.md",
        "sample_output.md",
        "handoff.md",
        "upsell.md",
    ),
    "ai_governance_program": (
        "offer.md",
        "scope.md",
        "ai_tool_inventory.md",
        "data_inventory.md",
        "risk_assessment.md",
        "policy_template.md",
        "approval_matrix.md",
        "audit_requirements.md",
        "sample_output.md",
        "handoff.md",
    ),
    "client_ai_policy_pack": (
        "offer.md",
        "policy_template.md",
        "employee_guide.md",
        "approval_matrix.md",
        "tool_usage_rules.md",
    ),
    # --- Governed Revenue & AI Operations catalog (Phase 5, 2026-05-16) ---
    "governed_revenue_ops_diagnostic": (
        "offer.md",
        "scope.md",
        "intake.md",
        "data_request.md",
        "delivery_checklist.md",
        "qa_checklist.md",
        "report_template.md",
        "proof_pack_template.md",
        "sample_output.md",
        "handoff.md",
        "upsell.md",
    ),
    "revenue_intelligence_sprint": (
        "offer.md",
        "scope.md",
        "intake.md",
        "data_request.md",
        "delivery_checklist.md",
        "qa_checklist.md",
        "report_template.md",
        "proof_pack_template.md",
        "sample_output.md",
        "handoff.md",
        "upsell.md",
    ),
    "governed_ops_retainer": (
        "offer.md",
        "scope.md",
        "intake.md",
        "data_request.md",
        "delivery_checklist.md",
        "qa_checklist.md",
        "report_template.md",
        "proof_pack_template.md",
        "sample_output.md",
        "handoff.md",
        "upsell.md",
    ),
    "ai_governance_for_revenue_teams": (
        "offer.md",
        "scope.md",
        "intake.md",
        "delivery_checklist.md",
        "qa_checklist.md",
        "report_template.md",
        "proof_pack_template.md",
        "sample_output.md",
        "handoff.md",
        "upsell.md",
    ),
    "crm_data_readiness_for_ai": (
        "offer.md",
        "scope.md",
        "intake.md",
        "data_request.md",
        "delivery_checklist.md",
        "qa_checklist.md",
        "report_template.md",
        "proof_pack_template.md",
        "sample_output.md",
        "handoff.md",
        "upsell.md",
    ),
    "board_decision_memo": (
        "offer.md",
        "scope.md",
        "intake.md",
        "qa_checklist.md",
        "report_template.md",
        "proof_pack_template.md",
        "sample_output.md",
        "handoff.md",
    ),
    "trust_pack_lite": (
        "offer.md",
        "scope.md",
        "intake.md",
        "qa_checklist.md",
        "report_template.md",
        "proof_pack_template.md",
        "sample_output.md",
        "handoff.md",
    ),
}

# Normalized markers (lowercase) required in each offer.md
_OFFER_MARKERS: tuple[str, ...] = (
    "## promise",
    "## price",
    "## duration",
    "## best for",
    "## deliverables",
    "## not included",
    "## success metric",
)


def _offer_blueprint_errors(folder: str, base: Path) -> list[str]:
    p = base / "offer.md"
    if not p.is_file():
        return [f"missing_offer:{folder}"]
    text = p.read_text(encoding="utf-8").lower()
    return [f"offer_missing_section:{folder}:{m}" for m in _OFFER_MARKERS if m not in text]


def load_mappings() -> list[dict[str, str]]:
    path = REPO / "docs" / "company" / "SERVICE_ID_MAP.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return list(data.get("mappings") or [])


def verify_service_files() -> tuple[bool, list[str]]:
    errors: list[str] = []
    for row in load_mappings():
        folder = row.get("folder")
        if not folder:
            continue
        base = REPO / "docs" / "services" / folder
        required = REQUIRED_BY_FOLDER.get(folder)
        if not required:
            errors.append(f"unknown_service_folder:{folder}")
            continue
        for name in required:
            p = base / name
            if not p.is_file():
                errors.append(f"missing:{folder}/{name}")
        errors.extend(_offer_blueprint_errors(folder, base))
    return (not errors, errors)


def main() -> int:
    ok, errors = verify_service_files()
    for e in errors:
        print(e, file=sys.stderr)
    print(f"SERVICE_FILES_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
