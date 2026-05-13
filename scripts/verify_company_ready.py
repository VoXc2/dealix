#!/usr/bin/env python3
"""Verify that Dealix is "Company Ready" — runs the 5 readiness checks.

سكربت التحقق من جاهزية الشركة — ينفّذ 5 فحوصات.

Usage:
    python scripts/verify_company_ready.py

Prints a readiness scorecard and exits with code 0 if ALL checks pass,
non-zero otherwise. Intended for the weekly operating cadence (W5.T30).
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Per W6.T35 — three starting offers
STARTING_OFFERS = (
    "lead_intelligence_sprint",
    "ai_quick_win_sprint",
    "company_brain_sprint",
)

# Per-service required files (Dealix Service Readiness Standard)
REQUIRED_SERVICE_FILES = (
    "offer.md",
    "scope.md",
    "intake.md",
    "qa_checklist.md",
    "proof_pack_template.md",
)

# Core company-level docs
REQUIRED_COMPANY_DOCS = (
    "docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md",
    "docs/strategy/dealix_operating_partner_positioning.md",
    "docs/strategy/service_portfolio_catalog.md",
    "docs/strategy/three_starting_offers.md",
    "docs/strategy/dealix_delivery_standard_and_quality_system.md",
    "docs/strategy/dealix_maturity_and_verification.md",
    "docs/company/OPERATING_PRINCIPLES.md",
    "docs/product/internal_os_modules.md",
)

# Core OS modules (the 5 Phase-1 modules)
REQUIRED_OS_FILES = (
    # Delivery OS
    "auto_client_acquisition/delivery_factory/client_intake.py",
    "auto_client_acquisition/delivery_factory/scope_builder.py",
    "auto_client_acquisition/delivery_factory/qa_review.py",
    "auto_client_acquisition/delivery_factory/delivery_checklist.py",
    "auto_client_acquisition/delivery_factory/client_handoff.py",
    "auto_client_acquisition/delivery_factory/renewal_recommendation.py",
    "auto_client_acquisition/delivery_factory/stage_machine.py",
    "auto_client_acquisition/delivery_factory/event_writer.py",
    # Data OS
    "auto_client_acquisition/customer_data_plane/validation_rules.py",
    "auto_client_acquisition/customer_data_plane/data_quality_score.py",
    "auto_client_acquisition/customer_data_plane/pii_detection.py",
    # Governance OS
    "dealix/trust/pii_detector.py",
    "dealix/trust/forbidden_claims.py",
    "dealix/trust/approval_matrix.py",
    # Reporting OS
    "dealix/reporting/__init__.py",
    "dealix/reporting/executive_report.py",
    "dealix/reporting/proof_pack.py",
    "dealix/reporting/weekly_summary.py",
    # Revenue OS extensions
    "auto_client_acquisition/revenue_os/lead_scoring.py",
    "auto_client_acquisition/revenue_os/icp_builder.py",
    "auto_client_acquisition/revenue_os/roi_calculator.py",
)

REQUIRED_SOW_TEMPLATES = (
    "templates/sow/revenue_intelligence_sprint.md",
    "templates/sow/ai_quick_win_sprint.md",
    "templates/sow/company_brain_sprint.md",
)

REQUIRED_DEMOS = (
    "demos/revenue_intelligence_demo.py",
    "demos/ai_quick_win_demo.py",
    "demos/company_brain_demo.py",
    "demos/data/sample_saudi_accounts.csv",
)


def _check(label: str, paths: tuple[str, ...]) -> tuple[bool, list[str]]:
    missing = [p for p in paths if not (REPO / p).exists()]
    ok = len(missing) == 0
    return ok, missing


def _check_service_folder(offer_slug: str) -> tuple[bool, list[str]]:
    base = Path("docs/services") / offer_slug
    paths = tuple(str(base / f) for f in REQUIRED_SERVICE_FILES)
    return _check(f"service:{offer_slug}", paths)


def _print(label: str, ok: bool, missing: list[str]) -> None:
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {label}")
    for m in missing:
        print(f"       missing: {m}")


def main() -> int:
    print("== Dealix Company Readiness ==")
    all_ok = True

    ok, missing = _check("company docs", REQUIRED_COMPANY_DOCS)
    _print("Company-level documentation", ok, missing)
    all_ok &= ok

    ok, missing = _check("OS modules", REQUIRED_OS_FILES)
    _print("OS modules (Delivery / Data / Governance / Reporting / Revenue)", ok, missing)
    all_ok &= ok

    ok, missing = _check("SOW templates", REQUIRED_SOW_TEMPLATES)
    _print("SOW templates for 3 starting offers", ok, missing)
    all_ok &= ok

    ok, missing = _check("demos + sample data", REQUIRED_DEMOS)
    _print("3 runnable demos + sample data", ok, missing)
    all_ok &= ok

    for offer in STARTING_OFFERS:
        ok, missing = _check_service_folder(offer)
        _print(f"service folder: {offer}", ok, missing)
        all_ok &= ok

    print("--")
    print(f"DEALIX_COMPANY_READY={'true' if all_ok else 'false'}")
    print(f"READY_SERVICES={'3/3' if all_ok else '0-2/3'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
