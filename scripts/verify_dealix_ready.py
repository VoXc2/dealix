#!/usr/bin/env python3
"""verify_dealix_ready.py — runs all 11 Dealix Stage Gates.

سكربت التحقق الرئيسي — يفحص كل البوابات الإحدى عشرة دفعة واحدة.

Usage:
    python scripts/verify_dealix_ready.py

Exit codes:
    0  → sales unlocked (Gates 0/1/2/4/5/6 all PASS)
    1  → sales blocked (at least one mandatory gate FAILED)

Mandatory gates for sales unlock: 0, 1, 2, 4, 5, 6.
Gates 3 (product MVP), 7, 8, 9, 10 are tracked but do not block sales.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# ── Required artifacts per gate ─────────────────────────────────────────────

GATE_0_FILES = (
    "docs/company/POSITIONING.md",
    "docs/company/MISSION_VISION.md",
    "docs/company/OPERATING_PRINCIPLES.md",
    "docs/company/ICP.md",
    "docs/company/NORTH_STAR_METRICS.md",
    "docs/company/SERVICE_CATALOG.md",
    "docs/company/PRICING.md",
    "docs/company/BUSINESS_MODEL.md",
)

# Gate 1 — 3 starting offers × 10 required files per folder
STARTING_OFFERS = (
    "lead_intelligence_sprint",
    "ai_quick_win_sprint",
    "company_brain_sprint",
)
GATE_1_PER_OFFER_FILES = (
    "offer.md",
    "scope.md",
    "intake.md",
    "qa_checklist.md",
    "proof_pack_template.md",
    "sample_output.md",
    "upsell.md",
    "handoff.md",
    "delivery_checklist.md",
    "report_template.md",
)

# AI Quick Win uses process_intake.md, Company Brain may use document_request.md
# We accept any of: intake.md / process_intake.md / inbox_intake.md / document_request.md
GATE_1_INTAKE_ALIASES = (
    "intake.md",
    "process_intake.md",
    "inbox_intake.md",
    "document_request.md",
)
GATE_1_DATA_REQUEST_ALIASES = (
    "data_request.md",
    "document_request.md",
)

GATE_2_FILES = (
    "docs/delivery/DELIVERY_STANDARD.md",
    "docs/delivery/DELIVERY_LIFECYCLE.md",
    "docs/delivery/CLIENT_ONBOARDING.md",
    "docs/delivery/SCOPE_CONTROL.md",
    "docs/delivery/CHANGE_REQUEST_PROCESS.md",
    "docs/delivery/HANDOFF_PROCESS.md",
    "docs/delivery/RENEWAL_PROCESS.md",
)

GATE_3_FILES = (
    "auto_client_acquisition/customer_data_plane/validation_rules.py",
    "auto_client_acquisition/customer_data_plane/data_quality_score.py",
    "auto_client_acquisition/customer_data_plane/pii_detection.py",
    "auto_client_acquisition/revenue_os/lead_scoring.py",
    "auto_client_acquisition/revenue_os/icp_builder.py",
    "auto_client_acquisition/revenue_os/roi_calculator.py",
    "dealix/trust/pii_detector.py",
    "dealix/trust/forbidden_claims.py",
    "dealix/trust/approval_matrix.py",
    "dealix/reporting/executive_report.py",
    "dealix/reporting/proof_pack.py",
    "dealix/reporting/weekly_summary.py",
    "auto_client_acquisition/delivery_factory/client_intake.py",
    "auto_client_acquisition/delivery_factory/scope_builder.py",
    "auto_client_acquisition/delivery_factory/qa_review.py",
    "auto_client_acquisition/delivery_factory/delivery_checklist.py",
    "auto_client_acquisition/delivery_factory/client_handoff.py",
    "auto_client_acquisition/delivery_factory/renewal_recommendation.py",
    "auto_client_acquisition/delivery_factory/stage_machine.py",
    "auto_client_acquisition/delivery_factory/event_writer.py",
)

GATE_4_FILES = (
    "docs/governance/COMPLIANCE_PERIMETER.md",
    "docs/governance/PDPL_DATA_RULES.md",
    "docs/governance/APPROVAL_MATRIX.md",
    "docs/governance/FORBIDDEN_ACTIONS.md",
    "docs/governance/PII_REDACTION_POLICY.md",
    "docs/governance/AUDIT_LOG_POLICY.md",
    "docs/governance/DATA_RETENTION.md",
)

GATE_5_FILES = (
    "demos/revenue_intelligence_demo.py",
    "demos/ai_quick_win_demo.py",
    "demos/company_brain_demo.py",
    "demos/data/sample_saudi_accounts.csv",
    "docs/services/lead_intelligence_sprint/sample_output.md",
    "docs/services/ai_quick_win_sprint/sample_output.md",
    "docs/services/company_brain_sprint/sample_output.md",
)

GATE_6_FILES = (
    "docs/SALES_PLAYBOOK.md",
    "docs/sales/persona_value_matrix.md",
    "docs/sales/roi_model_saudi.md",
    "docs/sales/roi_deck_outline.md",
    "docs/sales/enablement_program.md",
    "templates/outbound_messages.md",
    "templates/sow/revenue_intelligence_sprint.md",
    "templates/sow/ai_quick_win_sprint.md",
    "templates/sow/company_brain_sprint.md",
    "auto_client_acquisition/revenue_os/roi_calculator.py",
)

GATE_7_FILES = (
    "docs/delivery/CLIENT_ONBOARDING.md",
    "docs/delivery/HANDOFF_PROCESS.md",
    "templates/sow/revenue_intelligence_sprint.md",
)

# Gates 8/9/10 require numeric evidence from operating-cadence telemetry which
# this script cannot directly query. We check that the framework files exist
# and mark the gate as "framework-ready" but leave the empirical PASS/FIX to
# the weekly CEO review.
GATE_8_FILES = (
    "docs/customer-success/expansion_playbook.md",
    "docs/customer-success/cs_framework.md",
)
GATE_9_FILES = (
    "docs/strategy/dealix_delivery_standard_and_quality_system.md",
    "docs/strategy/dealix_maturity_and_verification.md",
    "auto_client_acquisition/delivery_factory/qa_review.py",
    "auto_client_acquisition/delivery_factory/stage_machine.py",
)
GATE_10_FILES = (
    "docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md",
    "docs/strategy/dealix_operating_partner_positioning.md",
    "docs/strategy/dealix_maturity_and_verification.md",
)


# ── Helpers ────────────────────────────────────────────────────────────────

def _exists_one_of(folder: Path, aliases: tuple[str, ...]) -> str | None:
    for name in aliases:
        if (folder / name).exists():
            return name
    return None


def _check_files(paths: tuple[str, ...]) -> tuple[list[str], list[str]]:
    """Return (present, missing) lists."""
    present: list[str] = []
    missing: list[str] = []
    for p in paths:
        if (REPO / p).exists():
            present.append(p)
        else:
            missing.append(p)
    return present, missing


def _print_gate(num: int, name: str, status: str, missing: list[str]) -> None:
    icon = {"PASS": "PASS", "PASS-MVP": "PASS-MVP", "FIX": "FIX", "DO-NOT-SELL": "DO-NOT-SELL"}[status]
    print(f"[{icon}] Gate {num}: {name}")
    for m in missing:
        print(f"        missing: {m}")


# ── Gate evaluators ────────────────────────────────────────────────────────

def gate_0() -> tuple[str, list[str]]:
    _, missing = _check_files(GATE_0_FILES)
    return ("PASS" if not missing else "FIX"), missing


def gate_1() -> tuple[str, list[str]]:
    missing: list[str] = []
    for offer in STARTING_OFFERS:
        folder = REPO / "docs" / "services" / offer
        if not folder.exists():
            missing.append(f"docs/services/{offer}/ (folder)")
            continue
        # Required files per offer (some have aliases)
        for fname in (
            "offer.md",
            "scope.md",
            "qa_checklist.md",
            "proof_pack_template.md",
            "sample_output.md",
            "upsell.md",
            "handoff.md",
            "delivery_checklist.md",
            "report_template.md",
        ):
            if not (folder / fname).exists():
                missing.append(f"docs/services/{offer}/{fname}")
        if _exists_one_of(folder, GATE_1_INTAKE_ALIASES) is None:
            missing.append(f"docs/services/{offer}/intake.md (or alias)")
        if _exists_one_of(folder, GATE_1_DATA_REQUEST_ALIASES) is None:
            missing.append(f"docs/services/{offer}/data_request.md (or alias)")
    return ("PASS" if not missing else "FIX"), missing


def gate_2() -> tuple[str, list[str]]:
    _, missing = _check_files(GATE_2_FILES)
    return ("PASS" if not missing else "FIX"), missing


def gate_3() -> tuple[str, list[str]]:
    _, missing = _check_files(GATE_3_FILES)
    # Phase-1 MVP — passing with all 5 OS modules in place
    return ("PASS-MVP" if not missing else "FIX"), missing


def gate_4() -> tuple[str, list[str]]:
    _, missing = _check_files(GATE_4_FILES)
    return ("PASS" if not missing else "FIX"), missing


def gate_5() -> tuple[str, list[str]]:
    _, missing = _check_files(GATE_5_FILES)
    return ("PASS" if not missing else "FIX"), missing


def gate_6() -> tuple[str, list[str]]:
    _, missing = _check_files(GATE_6_FILES)
    return ("PASS" if not missing else "FIX"), missing


def gate_7() -> tuple[str, list[str]]:
    _, missing = _check_files(GATE_7_FILES)
    return ("PASS" if not missing else "FIX"), missing


def gate_8() -> tuple[str, list[str]]:
    """Framework-ready; empirical PASS requires real retainer customer."""
    _, missing = _check_files(GATE_8_FILES)
    return ("FIX" if missing else "FIX"), missing  # always FIX pre-revenue


def gate_9() -> tuple[str, list[str]]:
    _, missing = _check_files(GATE_9_FILES)
    return ("FIX" if missing else "FIX"), missing  # empirical evidence needed


def gate_10() -> tuple[str, list[str]]:
    _, missing = _check_files(GATE_10_FILES)
    return ("FIX" if missing else "FIX"), missing  # numerical targets pending


# ── Main ────────────────────────────────────────────────────────────────────

def main() -> int:
    print("== Dealix Readiness — 11 Stage Gates ==\n")

    gates = [
        ("Founder Clarity", gate_0),
        ("Offer Readiness", gate_1),
        ("Delivery Readiness", gate_2),
        ("Product Readiness (MVP)", gate_3),
        ("Governance Readiness", gate_4),
        ("Demo Readiness", gate_5),
        ("Sales Readiness", gate_6),
        ("Client Delivery Readiness", gate_7),
        ("Retainer Readiness", gate_8),
        ("Scale Readiness", gate_9),
        ("World-Class Readiness", gate_10),
    ]

    results: list[tuple[int, str, str]] = []
    for idx, (name, evaluator) in enumerate(gates):
        status, missing = evaluator()
        _print_gate(idx, name, status, missing)
        results.append((idx, name, status))

    # Sales unlock decision: Gates 0, 1, 2, 4, 5, 6 must all be PASS or PASS-MVP
    mandatory = {0, 1, 2, 4, 5, 6}
    blockers = [
        (idx, name) for idx, name, status in results
        if idx in mandatory and status not in ("PASS", "PASS-MVP")
    ]

    print("\n" + "=" * 60)
    if not blockers:
        print("DEALIX_READY_FOR_SALES=true")
        print(f"READY_SERVICES={sum(1 for r in results if r[0] == 1 and r[2] == 'PASS')}/3")
        print("SALES_UNLOCKED=true")
        print("\nSellable services (officially):")
        print("  1. Lead Intelligence Sprint — SAR 9,500")
        print("  2. AI Quick Win Sprint — SAR 12,000")
        print("  3. Company Brain Sprint — SAR 20,000")
        return 0

    print("DEALIX_READY_FOR_SALES=false")
    print("SALES_UNLOCKED=false")
    print("\nBlocking gates:")
    for idx, name in blockers:
        print(f"  - Gate {idx}: {name}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
