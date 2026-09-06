#!/usr/bin/env python3
"""Create the governed delivery workspace for an authorized Dealix Pilot.

Canonical split of responsibilities:
- ``customers/<slug>/`` = commercial account truth from real interaction through
  diagnostic, discovery, named-customer quote, acceptance, and start evidence.
- ``clients/<slug>/`` = post-handoff delivery evidence for the approved 30-Day
  Revenue Command Pilot.

A real delivery workspace cannot be created from a scraped/research target or a
mere quote/invoice. Synthetic tests are explicitly labelled and isolated.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLIENTS_DIR = REPO_ROOT / "clients"
CUSTOMERS_DIR = REPO_ROOT / "customers"
TEMPLATE_DIR = CLIENTS_DIR / "_template"

PHASES: dict[str, list[str]] = {
    "00_intake": ["intake_form.md", "stakeholder_map.md", "access_checklist.md"],
    "01_diagnosis": [
        "current_state.md",
        "pain_map.md",
        "bottlenecks.md",
        "opportunity_map.md",
        "risk_register.md",
    ],
    "02_solution": [
        "system_blueprint.md",
        "workflow_map.md",
        "data_model.md",
        "ai_policy.md",
        "acceptance_criteria.md",
    ],
    "03_delivery": ["sprint_plan.md", "test_plan.md", "uat_notes.md"],
    "04_training": ["user_guide.md", "admin_guide.md", "sop.md"],
    "05_proof": [
        "before_after.md",
        "weekly_command_report.md",
        "decisions_log.md",
        "actions_completed.md",
        "open_risks.md",
        "client_feedback.md",
        "next_30_days.md",
    ],
}
REQUIRED_PHASES = list(PHASES.keys())
REQUIRED_HANDOFF_REFS = (
    "qualified_discovery_evidence_ref",
    "approved_scope_ref",
    "approved_named_customer_quote_ref",
    "customer_acceptance_ref",
    "payment_or_documented_start_condition_ref",
    "approved_data_boundary_ref",
)
SYNTHETIC_MARKER = "SYNTHETIC_TEST_ONLY_NOT_CUSTOMER_PROOF"


def expected_files() -> list[Path]:
    return [Path(phase) / name for phase, names in PHASES.items() for name in names]


def template_complete() -> bool:
    return all((TEMPLATE_DIR / rel).is_file() for rel in expected_files())


def validate_commercial_handoff(
    commercial_workspace: str | None,
    handoff_refs: dict[str, str] | None,
    synthetic_test: bool,
) -> dict[str, str]:
    if synthetic_test:
        return {"mode": SYNTHETIC_MARKER}

    if not commercial_workspace:
        raise RuntimeError("commercial workspace is required before real client delivery")

    path = (REPO_ROOT / commercial_workspace).resolve()
    customers_root = CUSTOMERS_DIR.resolve()
    if not path.is_relative_to(customers_root) or not path.is_dir():
        raise RuntimeError("commercial workspace must be an existing customers/<slug>/ directory")

    required_files = (
        "00_intake.md",
        "02_diagnostic_summary.md",
        "03_command_sprint_scope.md",
        "06_approval_register.md",
        "07_next_action_board.md",
    )
    missing_files = [name for name in required_files if not (path / name).is_file()]
    if missing_files:
        raise RuntimeError("commercial workspace missing required files: " + ", ".join(missing_files))

    refs = {key: str((handoff_refs or {}).get(key, "")).strip() for key in REQUIRED_HANDOFF_REFS}
    missing_refs = [key for key, value in refs.items() if not value]
    if missing_refs:
        raise RuntimeError("commercial handoff missing evidence refs: " + ", ".join(missing_refs))

    return {"mode": "GOVERNED_REAL_HANDOFF", "commercial_workspace": str(path.relative_to(REPO_ROOT)), **refs}


def create_workspace(
    client_slug: str,
    client_name: str | None = None,
    overwrite: bool = False,
    *,
    commercial_workspace: str | None = None,
    handoff_refs: dict[str, str] | None = None,
    synthetic_test: bool = False,
) -> Path:
    """Create a delivery workspace only after the commercial handoff gate."""
    if not template_complete():
        raise RuntimeError("clients/_template is incomplete; delivery template review required")

    handoff = validate_commercial_handoff(commercial_workspace, handoff_refs, synthetic_test)
    target = CLIENTS_DIR / client_slug

    if target.exists():
        safe_synthetic_replace = synthetic_test and overwrite and client_slug.startswith("dry-run")
        if not safe_synthetic_replace:
            raise FileExistsError(
                f"Client workspace already exists: {target}. Real client workspaces are never auto-overwritten."
            )
        shutil.rmtree(target)

    target.mkdir(parents=True, exist_ok=True)
    for phase in REQUIRED_PHASES:
        shutil.copytree(TEMPLATE_DIR / phase, target / phase)

    handoff_payload = {
        "client_slug": client_slug,
        "client_name": client_name or client_slug,
        "delivery_owner": "dealix-delivery",
        "commercial_owner": "dealix-sales",
        "executive_owner": "dealix-pm",
        "pilot": "30-Day Revenue Command Pilot",
        "handoff": handoff,
        "truth_rules": [
            "quote_is_not_payment",
            "invoice_is_not_payment",
            "activity_is_not_delivery",
            "delivery_is_not_customer_value",
            "customer_value_is_not_publication_permission",
        ],
    }
    (target / "COMMERCIAL_HANDOFF.json").write_text(
        json.dumps(handoff_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (target / "README.md").write_text(
        "\n".join(
            [
                f"# {client_name or client_slug}",
                "",
                "Governed Dealix 30-Day Revenue Command Pilot delivery workspace.",
                "",
                "Commercial account truth remains in the linked customers/<slug>/ workspace.",
                "Delivery evidence lives here and feeds the customer-facing Proof Pack.",
                "Created by: scripts/delivery/create_client_workspace.py",
                f"Slug: {client_slug}",
                f"Handoff mode: {handoff['mode']}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a governed Dealix client delivery workspace.")
    parser.add_argument("--client-slug", required=True)
    parser.add_argument("--client-name", default=None)
    parser.add_argument("--commercial-workspace", default=None, help="customers/<slug>/")
    parser.add_argument("--qualified-discovery-ref", default="")
    parser.add_argument("--approved-scope-ref", default="")
    parser.add_argument("--quote-ref", default="")
    parser.add_argument("--customer-acceptance-ref", default="")
    parser.add_argument("--start-condition-ref", default="")
    parser.add_argument("--data-boundary-ref", default="")
    parser.add_argument("--synthetic-test", action="store_true")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allowed only for synthetic dry-run workspaces whose slug starts with dry-run",
    )
    args = parser.parse_args()

    refs = {
        "qualified_discovery_evidence_ref": args.qualified_discovery_ref,
        "approved_scope_ref": args.approved_scope_ref,
        "approved_named_customer_quote_ref": args.quote_ref,
        "customer_acceptance_ref": args.customer_acceptance_ref,
        "payment_or_documented_start_condition_ref": args.start_condition_ref,
        "approved_data_boundary_ref": args.data_boundary_ref,
    }
    try:
        path = create_workspace(
            args.client_slug,
            args.client_name,
            args.overwrite,
            commercial_workspace=args.commercial_workspace,
            handoff_refs=refs,
            synthetic_test=args.synthetic_test,
        )
    except (FileExistsError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"created client delivery workspace: {path}")
    print("CLIENT_DELIVERY_HANDOFF=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
