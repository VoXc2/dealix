#!/usr/bin/env python3
"""Repository-side private launch readiness scorer for Dealix.

This verifier intentionally does NOT grant public/production readiness. A repo
can be structurally ready while Railway/DNS/TLS/deployed-SHA/runtime truth is
still blocked. Public launch authority must come from current production and
exact-head acceptance evidence, never from this static score alone.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts._wave8_scan import scan_files

CUSTOMER_TEMPLATE = REPO / "customers" / "_template"
PILOT_WORKSPACE_FILES = (
    "00_intake.md",
    "01_company_intelligence.md",
    "02_diagnostic_summary.md",
    "03_command_sprint_scope.md",
    "04_revenue_map.md",
    "05_proof_register.md",
    "06_approval_register.md",
    "07_next_action_board.md",
    "08_executive_command_brief.md",
    "09_delivery_log.md",
    "10_proof_pack.md",
    "11_upsell_recommendation.md",
)

SCAN_TARGETS = (
    "docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md",
    "dealix/config/first_launch_offer_gate.yaml",
    "docs/governance/registers/CLAIMS_REGISTER.md",
    "customers/_template/00_intake.md",
    "customers/_template/02_diagnostic_summary.md",
    "customers/_template/03_command_sprint_scope.md",
    "customers/_template/06_approval_register.md",
    "customers/_template/10_proof_pack.md",
    "customers/_template/11_upsell_recommendation.md",
    "scripts/commercial/run_self_operating_company_os.py",
)

UNSAFE_CLAIM_PATTERNS = (
    r"guaranteed\s+(revenue|results?|roi|return|income|sales)",
    r"guarantee\s+(you|your)\s+(revenue|results?|sales)",
    r"عائد\s+مضمون",
    r"أرباح\s+مضمونة",
    r"نضمن\s+(لك\s+)?(زيادة|أرباح|إيراد|نتائج|مبيعات)",
)

# Match executable/authority enablement, not safe prose such as "no auto-send".
DANGEROUS_AUTOMATION_PATTERNS = (
    r"DEALIX_EXTERNAL_SEND\s*=\s*1",
    r"DEALIX_EMAIL_LIVE_SEND\s*=\s*1",
    r"DEALIX_WHATSAPP_OUTBOUND\s*=\s*1",
    r"DEALIX_PUBLIC_PUBLISH\s*=\s*1",
    r"EXTERNAL_SEND_ENABLED\s*=\s*(true|1)",
    r"AUTO_WHATSAPP_ENABLED\s*=\s*(true|1)",
    r"AUTO_LINKEDIN_ENABLED\s*=\s*(true|1)",
    r"AUTO_PAYMENT_CAPTURE_ENABLED\s*=\s*(true|1)",
    r"AUTO_MERGE_ENABLED\s*=\s*(true|1)",
)


def exists(rel: str) -> bool:
    return (REPO / rel).is_file()


def any_exists(*rels: str) -> bool:
    return any(exists(rel) for rel in rels)


def text(rel: str) -> str:
    path = REPO / rel
    return path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""


def json_file(rel: str) -> dict:
    path = REPO / rel
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def template_complete() -> bool:
    return CUSTOMER_TEMPLATE.is_dir() and all(
        (CUSTOMER_TEMPLATE / name).is_file() for name in PILOT_WORKSPACE_FILES
    )


def canonical_offer_ok() -> bool:
    value = text("dealix/config/first_launch_offer_gate.yaml")
    required = (
        "id: revenue_command_pilot_30d",
        "duration_days: 30",
        "quote_only_after_discovery: true",
        "public_amount_sar: null",
        "fixed_price_allowed: false",
        "outcome_promise_allowed: false",
    )
    return all(item in value for item in required)


def governed_channel_ok() -> bool:
    payload = json_file("data/commercial/governed_channel_runtime_v1.json")
    value = json.dumps(payload, ensure_ascii=False)
    required = (
        "research_is_not_relationship",
        "public_contact_is_not_consent",
        "canonical_real_interaction_or_purpose_specific_consent",
        "suppression_and_opt_out_check",
        "action_bound_approval",
        "provider_effect_receipt",
    )
    return bool(payload) and all(item in value for item in required) and exists(
        "scripts/verify_governed_channel_runtime_v1.py"
    )


def customer_delivery_handoff_ok() -> bool:
    payload = json_file("data/commercial/client_delivery_control_manifest.json")
    handoff = payload.get("commercial_handoff", {}) if isinstance(payload, dict) else {}
    required = handoff.get("required_before_delivery_workspace", []) if isinstance(handoff, dict) else []
    return (
        payload.get("commercial_account_workspace") == "customers/<slug>/"
        and payload.get("delivery_workspace") == "clients/<slug>/"
        and len(required) >= 6
        and "payment_or_documented_start_condition_ref" in required
        and exists("scripts/delivery/create_client_workspace.py")
        and exists("scripts/commercial/generate_client_delivery_control.py")
    )


def agent_roster_ok() -> bool:
    return all(
        exists(path)
        for path in (
            ".claude/agents/dealix-pm.md",
            ".claude/agents/dealix-sales.md",
            ".claude/agents/dealix-delivery.md",
            ".claude/agents/dealix-engineer.md",
            ".claude/agents/dealix-content.md",
        )
    )


def module_status_ok() -> bool:
    if not all(exists(path) for path in ("docs/company/SERVICE_STATUS_RULES.md", "docs/company/SERVICE_REGISTRY.md")):
        return False
    registry = text("docs/company/SERVICE_REGISTRY.md").lower()
    return any(token in registry for token in ("live", "planned", "spec", "beta", "جاهز", "مخطط"))


def scan_hits(patterns: tuple[str, ...]) -> list[str]:
    return scan_files(REPO, SCAN_TARGETS, patterns)


def build_checks():
    claim_hits = scan_hits(UNSAFE_CLAIM_PATTERNS)
    dangerous_automation_hits = scan_hits(DANGEROUS_AUTOMATION_PATTERNS)

    p0 = [
        ("Canonical quote-only 30-Day Pilot authority", canonical_offer_ok(), "dealix/config/first_launch_offer_gate.yaml"),
        ("Free Mini Diagnostic implementation exists", exists("scripts/dealix_diagnostic.py"), "scripts/dealix_diagnostic.py"),
        ("Commercial authority source map exists", exists("data/commercial/commercial_authority_source_map_v1.json"), "data/commercial/commercial_authority_source_map_v1.json"),
        ("Governed omnichannel truth/dispatch contract", governed_channel_ok(), "data/commercial/governed_channel_runtime_v1.json"),
        ("Evidence-first Company OS runner", exists("scripts/commercial/run_self_operating_company_os.py"), "scripts/commercial/run_self_operating_company_os.py"),
        ("Customer commercial workspace template complete", template_complete(), "customers/_template/ (12 files)"),
        ("Commercial → delivery handoff contract", customer_delivery_handoff_ok(), "data/commercial/client_delivery_control_manifest.json"),
        ("Final Proof Pack template exists", exists("customers/_template/10_proof_pack.md"), "customers/_template/10_proof_pack.md"),
        ("Claims Register exists", exists("docs/governance/registers/CLAIMS_REGISTER.md"), "docs/governance/registers/CLAIMS_REGISTER.md"),
        ("Action-bound approval policy exists", any_exists("docs/governance/APPROVAL_POLICY.md", "docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md"), "docs/governance/APPROVAL_POLICY.md"),
        ("No External Action gate exists", exists("docs/03_governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md"), "docs/03_governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md"),
        ("No unsafe outcome claims in current authority surfaces", not claim_hits, f"{len(claim_hits)} hit(s)"),
        ("No dangerous external-automation enablement in current authority surfaces", not dangerous_automation_hits, f"{len(dangerous_automation_hits)} hit(s)"),
        ("No future module presented as live", module_status_ok(), "docs/company/SERVICE_REGISTRY.md"),
    ]
    p1 = [
        ("Five canonical agents exist", agent_roster_ok(), ".claude/agents/dealix-{pm,sales,delivery,engineer,content}.md"),
        ("Canonical customer E2E dry run exists", exists("scripts/run_dealix_e2e_dry_run.py"), "scripts/run_dealix_e2e_dry_run.py"),
        ("Customer lifecycle regression tests exist", exists("tests/test_customer_workspace_commercial_truth.py"), "tests/test_customer_workspace_commercial_truth.py"),
        ("Scheduled Company OS commercial-truth tests exist", exists("tests/test_self_operating_company_os_commercial_truth.py"), "tests/test_self_operating_company_os_commercial_truth.py"),
        ("Founder command surface exists", exists("scripts/ops/dealix_founder_master_command.sh"), "scripts/ops/dealix_founder_master_command.sh"),
        ("Client delivery control generator exists", exists("scripts/commercial/generate_client_delivery_control.py"), "scripts/commercial/generate_client_delivery_control.py"),
    ]
    p2 = [
        ("Answer Library plan exists", any_exists("docs/services/company_brain_sprint/answer_schema.md", "docs/sales-kit/dealix_objection_handler.md"), "docs/services/company_brain_sprint/answer_schema.md"),
        ("Partner/referral plan exists", any_exists("docs/growth/PARTNER_STRATEGY.md", "docs/AGENCY_PARTNER_PROGRAM.md"), "docs/growth/PARTNER_STRATEGY.md"),
        ("Growth metrics report exists", exists("reports/company_os/weekly/GROWTH_SCORECARD.md"), "reports/company_os/weekly/GROWTH_SCORECARD.md"),
        ("Brand/growth portfolio contract exists", exists("data/commercial/brand_growth_portfolio_v2.json"), "data/commercial/brand_growth_portfolio_v2.json"),
    ]
    return p0, p1, p2, claim_hits, dangerous_automation_hits


def verdict_for(score: int, p0_blockers: list[str]) -> str:
    if p0_blockers:
        return "No-Go" if score < 50 else "Internal Only"
    if score < 50:
        return "No-Go"
    if score < 70:
        return "Internal Only"
    if score < 85:
        return "Private Launch Candidate"
    return "Strong Private Launch Candidate"


def render_report(score: int, verdict: str, p0, p1, p2, p0_blk, p1_blk, p2_imp, next_fixes) -> str:
    def rows(items):
        return "\n".join(f"| {'PASS' if ok else 'FAIL'} | {name} | `{detail}` |" for name, ok, detail in items)

    def bullets(items):
        return "\n".join(f"- {item}" for item in items) if items else "- _(none)_"

    return f"""# Dealix — Repository Private Launch Readiness

_Generated by `scripts/verify_dealix_launch_readiness.py` on {date.today().isoformat()}._

## Score: {score}/100 → **{verdict}**

> **PUBLIC / PRODUCTION READINESS IS NOT INFERRED HERE.** A repository score cannot
> prove Railway deployed SHA, DNS/TLS, runtime health, exact-head sovereign acceptance,
> Telegram/OpenClaw Founder Control E2E, payment readiness, or live sender/channel health. Those require
> current external/runtime receipts.

## P0 — must pass
| | Check | Reference |
| --- | --- | --- |
{rows(p0)}

## P1 — should pass
| | Check | Reference |
| --- | --- | --- |
{rows(p1)}

## P2 — improvements
| | Check | Reference |
| --- | --- | --- |
{rows(p2)}

## P0 blockers
{bullets(p0_blk)}

## P1 blockers
{bullets(p1_blk)}

## P2 improvements
{bullets(p2_imp)}

## Next fixes
{bullets(next_fixes)}

## Mandatory external/runtime gates before public launch
- exact-head sovereign Trust/Commercial/E2E acceptance;
- Railway canonical `apps/web` deployment identity + deployed SHA;
- `dealix.me` / API direct health and stale-surface retirement;
- tenant/data boundary proof for the first real customer;
- Telegram/OpenClaw Founder Control end-to-end execution receipt;
- channel sender-health + consent/suppression + provider receipt path;
- payment/start-condition evidence before paid delivery;
- independent same-head review and action-bound production/merge authority.
"""


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    parser = argparse.ArgumentParser(description="Dealix repository private-launch readiness scorer")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)

    p0, p1, p2, claim_hits, dangerous_automation_hits = build_checks()

    def band_score(items, weight):
        return 0.0 if not items else weight * sum(1 for _, ok, _ in items if ok) / len(items)

    score = round(band_score(p0, 65) + band_score(p1, 25) + band_score(p2, 10))
    p0_blk = [name for name, ok, _ in p0 if not ok]
    p1_blk = [name for name, ok, _ in p1 if not ok]
    p2_imp = [name for name, ok, _ in p2 if not ok]
    verdict = verdict_for(score, p0_blk)
    next_fixes = (p0_blk + p1_blk + p2_imp)[:10]
    if claim_hits:
        next_fixes = (["Remove unsafe claim: " + claim_hits[0]] + next_fixes)[:10]
    if dangerous_automation_hits:
        next_fixes = (["Remove dangerous automation enablement: " + dangerous_automation_hits[0]] + next_fixes)[:10]

    for label, items in (("P0", p0), ("P1", p1), ("P2", p2)):
        for name, ok, _ in items:
            print(f"[{label}] {'PASS' if ok else 'FAIL'} — {name}")

    if not args.no_write:
        out = REPO / "reports" / "launch" / "private_launch_readiness.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_report(score, verdict, p0, p1, p2, p0_blk, p1_blk, p2_imp, next_fixes), encoding="utf-8")
        print(f"WROTE {out.relative_to(REPO)}")

    print(f"LAUNCH_READINESS_SCORE={score}")
    print(f"LAUNCH_VERDICT={verdict}")
    print("PUBLIC_PRODUCTION_READINESS=NOT_INFERRED")
    ok = score >= 70 and not p0_blk
    print(f"DEALIX_LAUNCH_READINESS_OK={'true' if ok else 'false'}")
    return 0 if score >= 50 else 1


if __name__ == "__main__":
    raise SystemExit(main())
