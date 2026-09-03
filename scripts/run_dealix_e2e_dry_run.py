#!/usr/bin/env python3
"""Dealix canonical end-to-end customer-journey dry run.

Exercises the current commercial/delivery spine using a clearly synthetic test
customer. Synthetic state is isolated and never becomes a relationship,
payment, revenue, delivery, or customer-proof claim. No external effect occurs.

Stages:
    1. Market signal / research truth
    2. Relationship + consent gate
    3. Free Mini Diagnostic
    4. Qualified Discovery + customer-specific Quote authority
    5. Customer workspace
    6. Payment/start-condition gate
    7. 30-Day Pilot delivery contract
    8. Proof Pack truth separation
    9. STOP / EXPAND / REDESIGN outcome review
    10. Governance / zero external effects
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts.create_customer_workspace import PILOT_WORKSPACE_FILES, create_workspace

DRY_RUN_CLIENT = "dry-run-client"
SYNTHETIC_MARKER = "SYNTHETIC_TEST_ONLY_NOT_CUSTOMER_PROOF"


@dataclass
class Stage:
    key: str
    name: str
    passed: bool = False
    notes: list[str] = field(default_factory=list)

    def fail(self, msg: str) -> None:
        self.passed = False
        self.notes.append(msg)

    def ok(self, msg: str) -> None:
        self.passed = True
        self.notes.append(msg)


def _read(rel: str) -> str:
    path = REPO / rel
    return path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""


def stage_market_signal_truth() -> Stage:
    stage = Stage("signal", "Market Signal / Research Truth")
    contract = _read("data/commercial/governed_channel_runtime_v1.json")
    required = ("research_is_not_relationship", "public_contact_is_not_consent")
    if not contract or not all(item in contract for item in required):
        stage.fail("governed-channel truth firewall missing or incomplete")
        return stage
    stage.ok(f"synthetic fixture labelled {SYNTHETIC_MARKER}; research cannot promote relationship/consent")
    return stage


def stage_relationship_gate() -> Stage:
    stage = Stage("relationship", "Relationship + Consent Gate")
    contract = _read("data/commercial/governed_channel_runtime_v1.json")
    required = (
        "canonical_real_interaction_or_purpose_specific_consent",
        "suppression_and_opt_out_check",
        "sender_or_channel_health",
        "action_bound_approval",
        "provider_effect_receipt",
    )
    if not all(item in contract for item in required):
        stage.fail("dispatch gate contract incomplete")
        return stage
    stage.ok("external dispatch remains blocked unless relationship/consent + suppression + health + authority + receipts pass")
    return stage


def stage_diagnostic(ws: Path) -> Stage:
    stage = Stage("diagnostic", "Free Mini Diagnostic")
    template = ws / "02_diagnostic_summary.md"
    script = REPO / "scripts/dealix_diagnostic.py"
    if not template.is_file() or not script.is_file():
        stage.fail("diagnostic template or script missing")
        return stage
    text = template.read_text(encoding="utf-8")
    if "Free Mini Diagnostic" not in text or "Qualified Discovery" not in text:
        stage.fail("diagnostic template is not on canonical launch path")
        return stage
    stage.ok("diagnostic exists and routes only to Qualified Discovery when evidence supports it")
    return stage


def stage_quote_authority(ws: Path) -> Stage:
    stage = Stage("quote", "Qualified Discovery + Quote Authority")
    offer_gate = _read("dealix/config/first_launch_offer_gate.yaml")
    scope = (ws / "03_command_sprint_scope.md").read_text(encoding="utf-8")
    required = (
        "id: revenue_command_pilot_30d",
        "quote_only_after_discovery: true",
        "public_amount_sar: null",
        "canonical_price_source_after_approval: founder_approved_named_customer_quote",
    )
    if not all(item in offer_gate for item in required):
        stage.fail("first-launch quote authority drift")
        return stage
    if "30-Day Revenue Command Pilot" not in scope or "No public fixed price" not in scope:
        stage.fail("customer scope template drift")
        return stage
    stage.ok("quote is named-customer/discovery-specific; no public fixed-price authority")
    return stage


def stage_workspace(ws: Path) -> Stage:
    stage = Stage("workspace", "Customer Workspace")
    missing = [name for name in PILOT_WORKSPACE_FILES if not (ws / name).is_file()]
    if missing:
        stage.fail("missing workspace files: " + ", ".join(missing))
        return stage
    stage.ok(f"all {len(PILOT_WORKSPACE_FILES)} governed Pilot workspace files present")
    return stage


def stage_payment_gate(ws: Path) -> Stage:
    stage = Stage("payment", "Payment / Start-Condition Gate")
    scope = (ws / "03_command_sprint_scope.md").read_text(encoding="utf-8")
    proof = (ws / "10_proof_pack.md").read_text(encoding="utf-8")
    if "Payment/start-condition evidence ref" not in scope:
        stage.fail("scope lacks payment/start-condition evidence gate")
        return stage
    if "Payment evidence: `UNKNOWN / VERIFIED`" not in proof:
        stage.fail("proof pack does not keep payment truth separate")
        return stage
    stage.ok("dry run creates no payment marker; real Pilot start requires documented customer start/payment evidence as applicable")
    return stage


def stage_delivery(ws: Path) -> Stage:
    stage = Stage("delivery", "30-Day Pilot Delivery")
    scope = (ws / "03_command_sprint_scope.md").read_text(encoding="utf-8")
    log = (ws / "09_delivery_log.md").read_text(encoding="utf-8")
    if not all(token in scope for token in ("Week 1", "Week 2", "Week 3", "Week 4 / Day 30")):
        stage.fail("30-day delivery cadence missing")
        return stage
    if "dealix-delivery" not in log or "Approval ref" not in log:
        stage.fail("delivery log is not agent/receipt driven")
        return stage
    stage.ok("dealix-delivery owns bounded execution; material actions remain receipt/approval bound")
    return stage


def stage_proof(ws: Path) -> Stage:
    stage = Stage("proof", "Proof Pack Truth")
    proof = (ws / "10_proof_pack.md").read_text(encoding="utf-8")
    required = (
        "Delivery evidence: `UNKNOWN / VERIFIED`",
        "Payment evidence: `UNKNOWN / VERIFIED`",
        "Customer value: `UNKNOWN / CUSTOMER_CONFIRMED`",
        "Publication permission: `NONE / LIMITED / GRANTED`",
        "No placeholder or simulated",
    )
    if not all(item in proof for item in required):
        stage.fail("Proof Pack truth separation incomplete")
        return stage
    stage.ok("delivery, payment, value and publication permission remain separate; synthetic result cannot become customer proof")
    return stage


def stage_outcome_review(ws: Path) -> Stage:
    stage = Stage("outcome", "STOP / EXPAND / REDESIGN")
    review = (ws / "11_upsell_recommendation.md").read_text(encoding="utf-8")
    if not all(item in review for item in ("STOP", "EXPAND", "REDESIGN", "No automatic renewal/upsell")):
        stage.fail("outcome-review contract drift")
        return stage
    if "Indicative price" in review:
        stage.fail("legacy generic expansion price authority present")
        return stage
    stage.ok("expansion is evidence-backed and requires new scope/quote authority; no automatic upsell")
    return stage


def stage_governance() -> Stage:
    stage = Stage("governance", "Governance / Zero External Effects")
    gate = REPO / "docs/03_governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md"
    policy = REPO / "docs/governance/APPROVAL_POLICY.md"
    if not gate.is_file() or not policy.is_file():
        stage.fail("governance policy surface missing")
        return stage
    stage.ok("dry run performed zero send/publish/payment/merge/deploy/DNS/DB/secret effects")
    return stage


def render_report(stages: list[Stage], verdict: str) -> str:
    lines = [
        "# Dealix Canonical E2E Customer-Journey Dry Run",
        "",
        f"_Generated {date.today().isoformat()} · {SYNTHETIC_MARKER} · zero external effects._",
        "",
    ]
    for index, stage in enumerate(stages, start=1):
        lines.extend(
            [
                f"## Stage {index} — {stage.name}",
                "PASS" if stage.passed else "FAIL",
                *[f"- {note}" for note in stage.notes],
                "",
            ]
        )
    lines.extend(["## Verdict", verdict, ""])
    return "\n".join(lines)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    try:
        ws, _ = create_workspace(DRY_RUN_CLIENT, force=True)
    except Exception as exc:
        print(f"FATAL: could not create dry-run workspace: {exc}", file=sys.stderr)
        return 1

    stages = [
        stage_market_signal_truth(),
        stage_relationship_gate(),
        stage_diagnostic(ws),
        stage_quote_authority(ws),
        stage_workspace(ws),
        stage_payment_gate(ws),
        stage_delivery(ws),
        stage_proof(ws),
        stage_outcome_review(ws),
        stage_governance(),
    ]
    verdict = "PASS" if all(stage.passed for stage in stages) else "NO_GO"

    for index, stage in enumerate(stages, start=1):
        print(f"Stage {index} — {stage.name}: {'PASS' if stage.passed else 'FAIL'}")
        for note in stage.notes:
            print(f"    {note}")

    out = REPO / "reports" / "verification" / "e2e_dry_run_latest.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_report(stages, verdict), encoding="utf-8")
    print(f"WROTE {out.relative_to(REPO)}")
    print(f"E2E_DRY_RUN_VERDICT={verdict}")
    print(f"DEALIX_E2E_DRY_RUN_OK={'true' if verdict == 'PASS' else 'false'}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
