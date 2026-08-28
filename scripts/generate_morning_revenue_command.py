#!/usr/bin/env python3
"""Generate the evidence-first Dealix Morning Revenue Command.

Only machine-readable evidence explicitly scoped to the Dealix company may
promote commercial/economic truth. Founder-personal, career, other-client,
research-only and unscoped documents are ignored for truth promotion.

Missing authoritative evidence is reported as UNKNOWN_NOT_EVIDENCE_BACKED.
The command is internal/read-only with respect to customers and external SaaS.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "founder_briefs"
CONTRACT_PATH = ROOT / "data/commercial/morning_revenue_command_contract.json"
WORKLOAD_PATH = ROOT / "data/commercial/agent_council_growth_workloads.json"
DEFAULT_CURRENT = Path(os.environ.get("DEALIX_COMPANY_OS_CURRENT", "/opt/dealix/company-os/current"))
UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"
DEALIX_SCOPES = {"dealix_company", "company:dealix", "dealix"}
KNOWN_CONTAINERS = ("money", "economic_truth", "pipeline", "commercial", "connectors", "metrics", "status")

FIELD_AUTHORITY: dict[str, tuple[str, ...]] = {
    "verified_revenue_sar": ("verified_revenue_sar", "verified_dealix_revenue_sar"),
    "verified_paid_pilots": ("verified_paid_pilots", "paid_pilots_verified"),
    "real_interactions": ("real_interactions", "real_interaction_count"),
    "verified_relationships": ("verified_relationships", "verified_relationship_count"),
    "qualified_problems": ("qualified_problems", "qualified_count"),
    "diagnostics_active": ("diagnostics_active", "diagnostics", "diagnostic_count"),
    "discoveries_active": ("discoveries_active", "discoveries", "discovery_count"),
    "customer_specific_proposals": ("customer_specific_proposals", "customer_specific_quotes"),
    "hubspot_status": ("hubspot_status", "hubspot_reconciliation_status"),
    "posthog_status": ("posthog_status", "posthog_ingestion_status"),
    "clay_status": ("clay_status", "clay_research_status"),
    "canva_status": ("canva_status", "canva_creative_status"),
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def iter_json_files(root: Path, max_files: int = 250, max_bytes: int = 2_000_000) -> Iterable[Path]:
    if not root.is_dir():
        return []
    found: list[Path] = []
    try:
        for path in sorted(root.rglob("*.json")):
            if len(found) >= max_files:
                break
            try:
                if path.is_file() and path.stat().st_size <= max_bytes:
                    found.append(path)
            except OSError:
                continue
    except OSError:
        return []
    return found


def evidence_metadata(doc: dict[str, Any]) -> tuple[str | None, str | None]:
    schema = doc.get("schema")
    scope = doc.get("scope") or doc.get("entity_scope") or doc.get("truth_scope")
    if not scope:
        company = doc.get("company_slug") or doc.get("company_id") or doc.get("company")
        if isinstance(company, str) and company.casefold() == "dealix":
            scope = "dealix_company"
    schema_s = str(schema).strip() if schema else None
    scope_s = str(scope).strip().casefold() if scope else None
    return schema_s, scope_s


def is_authoritative_dealix_doc(doc: dict[str, Any]) -> tuple[bool, str | None, str | None]:
    schema, scope = evidence_metadata(doc)
    if not schema or not schema.casefold().startswith("dealix."):
        return False, schema, scope
    if scope not in DEALIX_SCOPES:
        return False, schema, scope
    return True, schema, scope


def collect(current: Path) -> list[tuple[Path, dict[str, Any], str, str]]:
    docs: list[tuple[Path, dict[str, Any], str, str]] = []
    for path in iter_json_files(current):
        value = load_json(path)
        if not value:
            continue
        allowed, schema, scope = is_authoritative_dealix_doc(value)
        if allowed and schema and scope:
            docs.append((path, value, schema, scope))
    return docs


def lookup_key(doc: dict[str, Any], keys: tuple[str, ...]) -> tuple[Any, str | None]:
    for key in keys:
        if key in doc and doc[key] is not None:
            return doc[key], key
    for container_name in KNOWN_CONTAINERS:
        container = doc.get(container_name)
        if not isinstance(container, dict):
            continue
        for key in keys:
            if key in container and container[key] is not None:
                return container[key], key
    return None, None


def extract(
    docs: list[tuple[Path, dict[str, Any], str, str]], field: str
) -> tuple[Any, dict[str, str] | None]:
    keys = FIELD_AUTHORITY[field]
    for path, doc, schema, scope in docs:
        value, key = lookup_key(doc, keys)
        if value is not None and key:
            return value, {"path": str(path), "schema": schema, "scope": scope, "key": key}
    return UNKNOWN, None


def numeric(value: Any) -> Any:
    if value == UNKNOWN:
        return value
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        try:
            return int(float(value.strip().replace(",", "")))
        except ValueError:
            return value
    return value


def build(current: Path) -> dict[str, Any]:
    contract = load_json(CONTRACT_PATH)
    workloads = load_json(WORKLOAD_PATH)
    docs = collect(current)

    fields: dict[str, tuple[Any, dict[str, str] | None]] = {
        field: extract(docs, field) for field in FIELD_AUTHORITY
    }

    revenue = numeric(fields["verified_revenue_sar"][0])
    paid = numeric(fields["verified_paid_pilots"][0])
    relationships = numeric(fields["verified_relationships"][0])
    diagnostics = numeric(fields["diagnostics_active"][0])

    action = "CAPTURE_REAL_RELATIONSHIP_EVIDENCE"
    why = "No stronger evidence-backed commercial stage was found in authoritative Dealix company state."
    if isinstance(revenue, int) and revenue > 0:
        action = "PROOF_TO_EXPANSION_AND_REPEATABLE_DISTRIBUTION"
        why = "Verified revenue exists; compound it through permissioned proof, renewal, referral, and repeatable acquisition."
    elif isinstance(paid, int) and paid > 0:
        action = "VERIFY_PAYMENT_DELIVERY_AND_PROOF"
        why = "A verified paid-pilot state exists; preserve payment and delivery evidence before claiming proof."
    elif isinstance(diagnostics, int) and diagnostics > 0:
        action = "MOVE_ACTIVE_DIAGNOSTIC_TO_QUALIFIED_DISCOVERY"
        why = "An evidence-backed diagnostic is active; discovery is the closest canonical progression."
    elif isinstance(relationships, int) and relationships > 0:
        action = "MOVE_VERIFIED_RELATIONSHIP_TO_DIAGNOSTIC"
        why = "A verified relationship exists; establish qualified problem evidence and start the Mini Diagnostic path."

    return {
        "schema": "dealix.morning-revenue-command.runtime.v1",
        "scope": "dealix_company",
        "generated_at": datetime.now(UTC).isoformat(),
        "north_star": contract.get("north_star", "FIRST_VERIFIED_PAID_PILOT"),
        "source_root": str(current),
        "authoritative_source_documents_read": len(docs),
        "money": {
            "verified_revenue_sar": revenue,
            "verified_paid_pilots": paid,
            "closest_verified_money_path": action,
        },
        "pipeline": {
            "real_interactions": numeric(fields["real_interactions"][0]),
            "verified_relationships": relationships,
            "qualified_problems": numeric(fields["qualified_problems"][0]),
            "diagnostics_active": diagnostics,
            "discoveries_active": numeric(fields["discoveries_active"][0]),
            "customer_specific_proposals": numeric(fields["customer_specific_proposals"][0]),
        },
        "connectors": {
            "hubspot": fields["hubspot_status"][0],
            "posthog": fields["posthog_status"][0],
            "clay": fields["clay_status"][0],
            "canva": fields["canva_status"][0],
            "note": "Connector status is surfaced only from explicitly Dealix-company-scoped evidence; connector capability or schema presence is not live-ingestion proof.",
        },
        "agents": {
            "operating_model": "EXISTING_AGENT_COUNCIL_WITH_GROWTH_WORKLOADS",
            "growth_workload_count": len(workloads.get("roles", {})),
            "new_permanent_agents": 0,
            "new_schedulers": 0,
        },
        "approvals": {
            "material_gates": workloads.get("automation_policy", {}).get("specific_gate_required", []),
            "note": "Internal L0-L4 work may run autonomously; material commitments remain specifically gated.",
        },
        "next_best_action": {
            "action": action,
            "why_now": why,
            "expected_stage_movement": "TOWARD_FIRST_VERIFIED_PAID_PILOT",
        },
        "evidence_sources": {key: source for key, (_, source) in fields.items()},
        "truth_notes": [
            "Only evidence with a dealix.* schema and explicit Dealix company scope may promote Morning Command truth.",
            "Founder-personal, career, other-client, research-only and unscoped documents are ignored for truth promotion.",
            "UNKNOWN_NOT_EVIDENCE_BACKED means no current authoritative evidence was found; it never means fabricated zero.",
            "Research, enrichment, CRM records, analytics events, drafts, provider acceptance and invoices cannot promote economic truth by themselves.",
            "Verified revenue requires payment evidence; customer proof requires customer evidence and publication permission.",
        ],
    }


def render(command: dict[str, Any]) -> str:
    m = command["money"]
    p = command["pipeline"]
    c = command["connectors"]
    a = command["agents"]
    n = command["next_best_action"]
    return f"""# DEALIX MORNING REVENUE COMMAND

Generated: `{command['generated_at']}`  
North Star: **{command['north_star']}**

## MONEY
- Verified Dealix revenue SAR: **{m['verified_revenue_sar']}**
- Verified paid pilots: **{m['verified_paid_pilots']}**
- Closest verified-money path: **{m['closest_verified_money_path']}**

## PIPELINE
- Real interactions: **{p['real_interactions']}**
- Verified relationships: **{p['verified_relationships']}**
- Qualified problems: **{p['qualified_problems']}**
- Active diagnostics: **{p['diagnostics_active']}**
- Active discoveries: **{p['discoveries_active']}**
- Customer-specific proposals: **{p['customer_specific_proposals']}**

## CONNECTORS
- HubSpot: **{c['hubspot']}**
- PostHog: **{c['posthog']}**
- Clay: **{c['clay']}**
- Canva: **{c['canva']}**

## AGENT COUNCIL
- Operating model: **{a['operating_model']}**
- Growth workloads: **{a['growth_workload_count']}**
- New permanent agents: **0**
- New schedulers: **0**

## NEXT BEST ACTION
**{n['action']}**

{n['why_now']}

Expected movement: `{n['expected_stage_movement']}`

## TRUTH FIREWALL
Only explicitly Dealix-company-scoped evidence may promote commercial truth. `UNKNOWN_NOT_EVIDENCE_BACKED` means current authoritative evidence was not found; it must never be silently converted to zero or used to invent pipeline, revenue, delivery, consent, or customer proof.
"""


def atomic_write(path: Path, text: str) -> None:
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--current", type=Path, default=DEFAULT_CURRENT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    command = build(args.current)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    date = datetime.now(UTC).strftime("%Y-%m-%d")
    json_text = json.dumps(command, ensure_ascii=False, indent=2) + "\n"
    markdown = render(command)

    outputs = {
        args.out_dir / f"morning_revenue_command_{date}.json": json_text,
        args.out_dir / f"morning_revenue_command_{date}.md": markdown,
        args.out_dir / "morning_revenue_command_latest.json": json_text,
        args.out_dir / "morning_revenue_command_latest.md": markdown,
    }
    for path, text in outputs.items():
        atomic_write(path, text)

    print(f"MORNING_REVENUE_COMMAND_JSON={args.out_dir / 'morning_revenue_command_latest.json'}")
    print(f"MORNING_REVENUE_COMMAND_MD={args.out_dir / 'morning_revenue_command_latest.md'}")
    print("MORNING_REVENUE_COMMAND_VERDICT=PASS")
    if args.stdout:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
