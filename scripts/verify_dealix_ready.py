#!/usr/bin/env python3
"""Dealix stage gates — files, readiness scores, demo packs, sell gate.

Prints per-gate PASS flags and DEALIX_READY_FOR_SALES (Gates 0,1,2,3,4,5,6).
Gate 1 uses readiness >= 85 per starter service (Offer bar). Gate 7+ optional for sales.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from auto_client_acquisition.delivery_os.service_readiness import (  # noqa: E402
    compute_service_readiness_score,
)

OFFER_READINESS_MIN = 85

GATE0_FILES = (
    "docs/company/POSITIONING.md",
    "docs/company/MISSION_VISION.md",
    "docs/company/OPERATING_PRINCIPLES.md",
    "docs/company/ICP.md",
    "docs/company/NORTH_STAR_METRICS.md",
)

GATE2_FILES = (
    "docs/delivery/DELIVERY_STANDARD.md",
    "docs/delivery/DELIVERY_LIFECYCLE.md",
    "docs/delivery/CLIENT_ONBOARDING.md",
    "docs/delivery/SCOPE_CONTROL.md",
    "docs/delivery/HANDOFF_PROCESS.md",
    "docs/delivery/RENEWAL_PROCESS.md",
)

GATE5_META_FILES = (
    "docs/delivery/DEMO_READINESS.md",
    "docs/sales/DEMO_SCRIPT.md",
)

LEAD_INTELLIGENCE_DEMO_FILES = (
    "demos/lead_intelligence_demo/demo.csv",
    "demos/lead_intelligence_demo/import_preview.md",
    "demos/lead_intelligence_demo/data_quality_report.md",
    "demos/lead_intelligence_demo/scoring_output.md",
    "demos/lead_intelligence_demo/top_50_accounts.md",
    "demos/lead_intelligence_demo/top_10_actions.md",
    "demos/lead_intelligence_demo/outreach_drafts.md",
    "demos/lead_intelligence_demo/mini_crm_board.md",
    "demos/lead_intelligence_demo/executive_report.md",
    "demos/lead_intelligence_demo/proof_pack.md",
)

AI_QUICK_WIN_DEMO_FILES = (
    "demos/ai_quick_win_demo/process_map.md",
    "demos/ai_quick_win_demo/before_after.md",
    "demos/ai_quick_win_demo/workflow.md",
    "demos/ai_quick_win_demo/approval_step.md",
    "demos/ai_quick_win_demo/time_saved_estimate.md",
    "demos/ai_quick_win_demo/sop.md",
    "demos/ai_quick_win_demo/proof_pack.md",
)

COMPANY_BRAIN_DEMO_FILES = (
    "demos/company_brain_demo/sample_docs/README.md",
    "demos/company_brain_demo/document_inventory.md",
    "demos/company_brain_demo/qa_examples.md",
    "demos/company_brain_demo/answers_with_citations.md",
    "demos/company_brain_demo/no_source_no_answer.md",
    "demos/company_brain_demo/eval_report.md",
    "demos/company_brain_demo/proof_pack.md",
)

GATE5_DEMO_FILES = (
    LEAD_INTELLIGENCE_DEMO_FILES + AI_QUICK_WIN_DEMO_FILES + COMPANY_BRAIN_DEMO_FILES + ("demos/README.md",)
)

GATE6_FILES = (
    "docs/sales/SALES_PLAYBOOK.md",
    "docs/sales/DISCOVERY_SCRIPT.md",
    "docs/sales/OFFER_PAGES.md",
    "docs/sales/OBJECTION_HANDLING.md",
    "docs/sales/PROPOSAL_TEMPLATE.md",
    "docs/sales/FOLLOW_UP_SEQUENCES.md",
)

GATE7_FILES = (
    "docs/delivery/client_onboarding/welcome_message.md",
    "docs/delivery/client_onboarding/data_request.md",
    "docs/delivery/client_onboarding/project_timeline.md",
    "docs/delivery/client_onboarding/roles_and_responsibilities.md",
    "docs/delivery/client_onboarding/review_call_agenda.md",
    "docs/delivery/client_onboarding/approval_process.md",
)

GATE8_FILES = ("docs/delivery/RETAINER_READINESS.md",)

ROOT_READINESS = "DEALIX_READINESS.md"

PRODUCT_PACKAGES = (
    "auto_client_acquisition/data_os",
    "auto_client_acquisition/revenue_os",
    "auto_client_acquisition/company_brain",
    "auto_client_acquisition/governance_os",
    "auto_client_acquisition/executive_reporting",
    "auto_client_acquisition/delivery_os",
)

STARTER_SERVICE_IDS = (
    "lead_intelligence_sprint",
    "quick_win_ops",
    "company_brain_sprint",
)


def _missing(paths: tuple[str, ...]) -> list[str]:
    return [p for p in paths if not (REPO / p).is_file()]


def _package_has_code(rel: str) -> bool:
    root = REPO / rel
    if not root.is_dir():
        return False
    return any(root.rglob("*.py"))


def _run_script(name: str, *, quiet: bool = True) -> bool:
    kwargs: dict = {"cwd": REPO}
    if quiet:
        kwargs["capture_output"] = True
        kwargs["text"] = True
    proc = subprocess.run(  # noqa: S603
        [sys.executable, str(REPO / "scripts" / name)],
        check=False,
        **kwargs,
    )
    return proc.returncode == 0


def _service_mappings() -> list[dict]:
    path = REPO / "docs" / "company" / "SERVICE_ID_MAP.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return list(data.get("mappings") or [])


def _print_readiness_report(
    *,
    gate0: bool,
    gate1: bool,
    gate2: bool,
    gate3: bool,
    gate4: bool,
    gate5: bool,
    gate6: bool,
    gate7: bool,
    gate8: bool,
    tests_ok: bool,
    dealix_ready_for_sales: bool,
    service_files_ok: bool,
) -> None:
    print("")
    print("=== DEALIX_READINESS_REPORT ===")
    print(f"Company Clarity: {'PASS' if gate0 else 'FIX'}")
    print(f"Offer Readiness: {'PASS' if gate1 else 'FIX'}")
    print(f"Delivery Readiness: {'PASS' if gate2 else 'FIX'}")
    print(f"Product Readiness: {'PASS' if gate3 else 'FIX'}")
    print(f"Governance Readiness: {'PASS' if gate4 else 'FIX'}")
    print(f"Demo Readiness: {'PASS' if gate5 else 'FIX'}")
    print(f"Sales Readiness: {'PASS' if gate6 else 'FIX'}")
    print(f"Client Delivery Readiness: {'PASS' if gate7 else 'FIX'}")
    print(f"Retainer Readiness: {'PASS' if gate8 else 'FIX'}")
    print(f"Tests: {'PASS' if tests_ok else 'FIX'}")
    print("")

    sellable: list[str] = []
    beta: list[str] = []
    blocked: list[str] = []
    for row in _service_mappings():
        sid = row.get("service_id") or ""
        folder = row.get("folder") or sid
        if not sid:
            continue
        sc = int(compute_service_readiness_score(sid)["score"])
        label = f"{folder} ({sid}) score={sc}"
        if sc >= 85:
            sellable.append(label)
        elif sc >= 70:
            beta.append(label)
        else:
            blocked.append(label)

    print("Sellable services (readiness >= 85):")
    for line in sellable or ["(none)"]:
        print(f"- {line}")
    print("")
    print("Beta services (70-84):")
    for line in beta or ["(none)"]:
        print(f"- {line}")
    print("")
    print("Not ready (<70):")
    for line in blocked or ["(none)"]:
        print(f"- {line}")
    print("")

    if dealix_ready_for_sales:
        decision = "SELL_READY_STACK"
    elif service_files_ok and sellable:
        decision = "SELL_ONLY_READY_SERVICES"
    else:
        decision = "DO_NOT_SELL_FULL_CATALOG"
    print(f"Decision: {decision}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-tests", action="store_true")
    args = ap.parse_args()

    m0 = list(_missing(GATE0_FILES))
    if not (REPO / ROOT_READINESS).is_file():
        m0.append(ROOT_READINESS)
    gate0 = not m0

    m2 = _missing(GATE2_FILES)
    gate2 = not m2

    m5_meta = _missing(GATE5_META_FILES)
    m5_demo = _missing(GATE5_DEMO_FILES)
    gate5 = not m5_meta and not m5_demo

    m6 = _missing(GATE6_FILES)
    gate6 = not m6

    m7 = _missing(GATE7_FILES)
    gate7 = not m7

    m8 = _missing(GATE8_FILES)
    gate8 = not m8

    gate3 = all(_package_has_code(p) for p in PRODUCT_PACKAGES)

    service_files_ok = _run_script("verify_service_files.py")
    governance_ok = _run_script("verify_governance_rules.py")
    ai_q_ok = _run_script("verify_ai_output_quality.py")

    starter_ready = 0
    starter_offer_pass = 0
    starter_scores: list[str] = []
    for sid in STARTER_SERVICE_IDS:
        info = compute_service_readiness_score(sid)
        score = int(info["score"])
        starter_scores.append(f"{sid}={score}")
        if score >= OFFER_READINESS_MIN:
            starter_offer_pass += 1
        if score >= 80:
            starter_ready += 1

    gate1 = service_files_ok and starter_offer_pass == len(STARTER_SERVICE_IDS)
    gate4 = governance_ok and ai_q_ok

    tests_ok = True
    if not args.skip_tests:
        tests_ok = (
            subprocess.call(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "tests/test_company_os_verify.py",
                    "tests/test_data_os_helpers.py",
                    "tests/test_reporting_os_proof_pack.py",
                    "tests/test_delivery_os_catalog.py",
                    "tests/test_knowledge_os_policy.py",
                    "tests/test_governance_approval_matrix.py",
                    "-q",
                    "--no-cov",
                ],
                cwd=REPO,
            )
            == 0
        )

    dealix_ready_for_sales = (
        gate0
        and gate1
        and gate2
        and gate3
        and gate4
        and gate5
        and gate6
        and tests_ok
    )

    all_tracked = (
        GATE0_FILES
        + GATE2_FILES
        + GATE5_META_FILES
        + GATE5_DEMO_FILES
        + GATE6_FILES
        + GATE7_FILES
        + GATE8_FILES
        + (ROOT_READINESS,)
    )

    print(f"GATE0_PASS={'true' if gate0 else 'false'}")
    print(f"GATE1_PASS={'true' if gate1 else 'false'}")
    print(f"GATE2_PASS={'true' if gate2 else 'false'}")
    print(f"GATE3_PASS={'true' if gate3 else 'false'}")
    print(f"GATE4_PASS={'true' if gate4 else 'false'}")
    print(f"GATE5_PASS={'true' if gate5 else 'false'}")
    print(f"GATE6_PASS={'true' if gate6 else 'false'}")
    print(f"GATE7_PASS={'true' if gate7 else 'false'}")
    print(f"GATE8_PASS={'true' if gate8 else 'false'}")
    print(
        f"STARTER_SERVICES_OFFER_PASS={starter_offer_pass}/{len(STARTER_SERVICE_IDS)} "
        f"({', '.join(starter_scores)}) min={OFFER_READINESS_MIN}"
    )
    print(f"STARTER_SERVICES_READY_80={starter_ready}/{len(STARTER_SERVICE_IDS)}")
    print(f"SERVICE_FILES_PASS={'true' if service_files_ok else 'false'}")
    print(f"GOVERNANCE_READY={'true' if governance_ok else 'false'}")
    print(f"DELIVERY_READY={'true' if gate2 else 'false'}")
    print(f"DEMO_READY={'true' if gate5 else 'false'}")
    print(f"SALES_READY={'true' if gate6 else 'false'}")
    print(f"MISSING_FILES={len(_missing(all_tracked))}")
    print(f"TESTS_PASS={'true' if tests_ok else 'false'}")
    print(f"DEALIX_READY_FOR_SALES={'true' if dealix_ready_for_sales else 'false'}")
    _print_readiness_report(
        gate0=gate0,
        gate1=gate1,
        gate2=gate2,
        gate3=gate3,
        gate4=gate4,
        gate5=gate5,
        gate6=gate6,
        gate7=gate7,
        gate8=gate8,
        tests_ok=tests_ok,
        dealix_ready_for_sales=dealix_ready_for_sales,
        service_files_ok=service_files_ok,
    )
    if not dealix_ready_for_sales:
        msg = (
            "SELL_ONLY_READY_SERVICES=true"
            if starter_ready > 0 and service_files_ok
            else "DO_NOT_SELL_FULL_CATALOG=true"
        )
        print(msg, file=sys.stderr)

    return 0 if dealix_ready_for_sales else 1


if __name__ == "__main__":
    raise SystemExit(main())
