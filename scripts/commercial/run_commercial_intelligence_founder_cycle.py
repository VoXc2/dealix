#!/usr/bin/env python3
"""Build the Dealix Commercial Intelligence founder brief in draft-only mode."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_intelligence import (
    GovernedSource,
    SourceKind,
    SourcePolicyStatus,
    score_source,
)

SOURCE_PATH = ROOT / "data/commercial_intelligence/ksa_source_registry.yaml"
OBJECTIVE_PATH = ROOT / "data/commercial_intelligence/dealix_department_objectives.yaml"
OFFER_GATE_PATH = ROOT / "dealix/config/first_launch_offer_gate.yaml"

OPERATING_TABLE_COLUMNS: dict[str, tuple[str, ...]] = {
    "strategy_backlog": ("id", "decision", "status", "owner", "evidence_gate"),
    "action_queue": ("id", "action", "owner", "priority", "completion_evidence"),
    "approval_queue": ("id", "question", "owner", "blocks"),
    "opportunity_graph": (
        "opportunity_id",
        "account_id",
        "stage",
        "evidence_level",
        "next_action",
    ),
    "proof_ledger": ("path", "sha256", "proof_type"),
    "self_improvement": ("metric", "baseline", "target", "review_cadence", "owner"),
    "contacts_radar": (
        "contact_id",
        "account_id",
        "role",
        "permission_state",
        "next_review",
    ),
}


def _load(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"invalid_yaml_mapping:{path}")
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _domain_source(row: dict[str, Any]) -> GovernedSource:
    return GovernedSource(
        tenant_id="dealix",
        source_id=str(row["id"]),
        name=str(row["name"]),
        kind=SourceKind(str(row["kind"])),
        policy_status=SourcePolicyStatus(str(row["policy_status"])),
        allowed_use=str(row["allowed_use"]),
        authority_score=int(row["authority_score"]),
        verifiability_score=int(row["verifiability_score"]),
        freshness_days=int(row["freshness_days"]),
        retention_days=int(row["retention_days"]),
        source_url=str(row["url"]) if row.get("url") else None,
    )


def build_cycle(*, run_date: date | None = None) -> dict[str, Any]:
    source_payload = _load(SOURCE_PATH)
    objective_payload = _load(OBJECTIVE_PATH)
    offer_gate = _load(OFFER_GATE_PATH)
    sources = [_domain_source(row) for row in source_payload.get("sources", [])]
    objectives = objective_payload.get("objectives", [])
    source_ids = [source.source_id for source in sources]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("duplicate_source_id")
    objective_keys = [f"{row.get('department')}::{row.get('metric')}" for row in objectives]
    if len(objective_keys) != len(set(objective_keys)):
        raise ValueError("duplicate_department_metric")

    scorecards = [
        {
            "source_id": source.source_id,
            "name": source.name,
            "kind": source.kind.value,
            "policy_status": source.policy_status.value,
            "source_score": score_source(source),
            "signals": 0,
            "external_action_allowed": False,
        }
        for source in sources
    ]
    review_queue = [
        {
            "source_id": source.source_id,
            "name": source.name,
            "reason": "terms_or_dataset_scope_review_required",
        }
        for source in sources
        if source.policy_status
        in {SourcePolicyStatus.REVIEW_REQUIRED, SourcePolicyStatus.RESEARCH_ONLY}
    ]
    dated = run_date or datetime.now(UTC).date()
    proof_ledger = [
        {
            "path": str(SOURCE_PATH.relative_to(ROOT)),
            "sha256": _sha256(SOURCE_PATH),
            "proof_type": "source_governance_input",
        },
        {
            "path": str(OBJECTIVE_PATH.relative_to(ROOT)),
            "sha256": _sha256(OBJECTIVE_PATH),
            "proof_type": "department_objective_input",
        },
        {
            "path": str(OFFER_GATE_PATH.relative_to(ROOT)),
            "sha256": _sha256(OFFER_GATE_PATH),
            "proof_type": "first_launch_decision_gate",
        },
    ]
    strategy_backlog = [
        {
            "id": "strategy_one_icp",
            "decision": "Validate one Saudi B2B service-business ICP for the first 90 days",
            "status": offer_gate["icp_hypothesis"]["status"],
            "owner": "founder",
            "evidence_gate": "five_qualified_first_party_conversations",
        },
        {
            "id": "strategy_one_offer",
            "decision": "Approve one customer-specific Revenue Command Pilot and one successor motion",
            "status": offer_gate["status"],
            "owner": "founder",
            "evidence_gate": "issue_917_catalog_reconciliation",
        },
        {
            "id": "strategy_one_proof_system",
            "decision": "Use baseline-to-proof as the sole outcome-claim path",
            "status": "evidence_required",
            "owner": "revenue_and_delivery",
            "evidence_gate": "client_accepted_proof_pack",
        },
    ]
    action_queue = [
        {
            "id": "action_qualified_conversations",
            "action": "Run five consented design-partner conversations using the same discovery scorecard",
            "owner": "founder",
            "priority": "P0",
            "completion_evidence": "five_redacted_interview_scorecards",
        },
        {
            "id": "action_offer_contract",
            "action": "Reconcile landing, API, service catalog, proposal, and checkout to the approved motion",
            "owner": "product_and_revenue",
            "priority": "P0",
            "completion_evidence": "pricing_and_offer_contract_test",
        },
        {
            "id": "action_legal_data",
            "action": "Approve terms, DPA/data map, retention, refund, SLA, tax, and e-invoice ownership",
            "owner": "founder_legal_finance",
            "priority": "P0",
            "completion_evidence": "dated_launch_trust_pack",
        },
        {
            "id": "action_demo_rehearsal",
            "action": "Rehearse the 18-minute evidence demo in Sales Arena and keep failing turns in shadow mode",
            "owner": "revenue",
            "priority": "P1",
            "completion_evidence": "arena_run_with_no_critical_failures",
        },
    ]
    approval_queue = [
        {
            "id": "approval_launch_offer_price",
            "question": "Approve the 30-day pilot scope and price after five qualified conversations?",
            "owner": "founder",
            "blocks": "public_price|proposal|checkout",
        },
        {
            "id": "approval_public_claim_set",
            "question": "Approve only dated, source-bound public claims and proof references?",
            "owner": "founder",
            "blocks": "landing_copy|case_study|outbound_draft",
        },
        {
            "id": "approval_launch_trust_pack",
            "question": "Approve legal, privacy, security, refund, SLA, tax, and e-invoice readiness evidence?",
            "owner": "founder_legal_finance",
            "blocks": "customer_data_access|live_charge|production_launch",
        },
    ]
    self_improvement = [
        {
            "metric": "qualified_conversation_to_pilot_decision",
            "baseline": "not_measured",
            "target": "set_after_first_five_conversations",
            "review_cadence": "weekly",
            "owner": "founder",
        },
        {
            "metric": "objection_response_first_party_validation_rate",
            "baseline": "not_measured",
            "target": "evidence_before_asset_promotion",
            "review_cadence": "weekly",
            "owner": "revenue",
        },
        {
            "metric": "pilot_proof_pack_acceptance_rate",
            "baseline": "not_measured",
            "target": "set_after_first_cohort",
            "review_cadence": "monthly",
            "owner": "delivery",
        },
    ]
    return {
        "run_date": dated.isoformat(),
        "mode": "draft_only",
        "tenant_id": "dealix",
        "sources": len(sources),
        "department_objectives": len(objectives),
        "signals": 0,
        "opportunities": 0,
        "source_scorecards": sorted(
            scorecards, key=lambda row: (-row["source_score"], row["name"])
        ),
        "source_review_queue": review_queue,
        "objectives": objectives,
        "first_launch_offer_gate": {
            "status": offer_gate["status"],
            "primary_motion": offer_gate["primary_motion"],
            "pricing_experiment": offer_gate["pricing_experiment"],
            "decision_issue": offer_gate["decision_issue"],
        },
        "truth_state": {
            "real_company_signals_loaded": False,
            "real_opportunities_created": False,
            "reason": "No tenant-authorized company evidence was supplied to this cycle.",
        },
        "strategy_backlog": strategy_backlog,
        "action_queue": action_queue,
        "approval_queue": approval_queue,
        "opportunity_graph": [],
        "proof_ledger": proof_ledger,
        "self_improvement": self_improvement,
        "contacts_radar": [],
        "proof_log": proof_ledger,
        "external_actions_executed": 0,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dealix Commercial Intelligence — Founder Cycle",
        "",
        f"- Date: `{payload['run_date']}`",
        f"- Mode: `{payload['mode']}`",
        f"- Sources governed: **{payload['sources']}**",
        f"- Department objectives: **{payload['department_objectives']}**",
        f"- Real signals loaded: **{payload['signals']}**",
        f"- Real opportunities created: **{payload['opportunities']}**",
        f"- External actions executed: **{payload['external_actions_executed']}**",
        f"- First launch offer gate: **{payload['first_launch_offer_gate']['status']}**",
        "",
        "## Truth state",
        "",
        payload["truth_state"]["reason"],
        "",
        "## Source scorecards",
        "",
        "| Source | Policy | Score | Signals |",
        "|---|---:|---:|---:|",
    ]
    for item in payload["source_scorecards"]:
        lines.append(
            f"| {item['name']} | {item['policy_status']} | {item['source_score']} | {item['signals']} |"
        )
    lines.extend(["", "## Department objectives", ""])
    for item in payload["objectives"]:
        target = (
            f"{item['target_value']} {item.get('target_unit') or ''}".strip()
            if item.get("target_value") is not None
            else "baseline required"
        )
        lines.append(
            f"- **{item['department']} / {item['metric']}** — {item['objective']} (target: {target})"
        )
    lines.extend(
        [
            "",
            "## Safe next actions",
            "",
            "1. Complete terms and dataset-scope review for queued sources.",
            "2. Load only tenant-authorized organization signals with evidence references.",
            "3. Validate pain hypotheses with first-party discovery before scoring them above L2.",
            "4. Create reviewable opportunities; keep all outbound in the canonical Approval Center.",
            "",
            "## Proof log",
            "",
        ]
    )
    for item in payload["proof_log"]:
        lines.append(f"- `{item['path']}` — `{item['sha256']}`")
    return "\n".join(lines) + "\n"


def write_operating_tables(payload: dict[str, Any], output: Path, dated: str) -> None:
    """Export the seven operating queues as Sheet-compatible CSV files."""
    for table_name, columns in OPERATING_TABLE_COLUMNS.items():
        path = output / f"{table_name}_{dated}.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(payload[table_name])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "reports/commercial_intelligence")
    parser.add_argument("--date", type=date.fromisoformat)
    args = parser.parse_args()
    payload = build_cycle(run_date=args.date)
    args.output.mkdir(parents=True, exist_ok=True)
    dated = payload["run_date"]
    (args.output / f"founder_cycle_{dated}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (args.output / f"founder_cycle_{dated}.md").write_text(
        render_markdown(payload), encoding="utf-8"
    )
    write_operating_tables(payload, args.output, dated)
    print("COMMERCIAL_INTELLIGENCE_FOUNDER_CYCLE=PASS")
    print(f"EXTERNAL_ACTIONS_EXECUTED={payload['external_actions_executed']}")
    print(f"REAL_OPPORTUNITIES_CREATED={payload['opportunities']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
