"""Emit the JSON-Schema contracts for the Dealix engine into /schemas.

Each schema is authored here as a Python dict and written to a .json file so
the whole contract set stays consistent. Run:  python scripts/dealix/build_schemas.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "schemas"

D7 = "http://json-schema.org/draft-07/schema#"


def s(title, props, required, additional=False, **extra):
    schema = {
        "$schema": D7,
        "title": title,
        "type": "object",
        "properties": props,
        "required": required,
        "additionalProperties": additional,
    }
    schema.update(extra)
    return schema


def str_(min_len=1, **kw):
    d = {"type": "string", "minLength": min_len}
    d.update(kw)
    return d


def arr(items, min_items=1, **kw):
    d = {"type": "array", "items": items, "minItems": min_items}
    d.update(kw)
    return d


CORE_SYSTEM_ENUM = [
    "revenue-operating-system",
    "executive-command-os",
    "follow-up-recovery-os",
    "whatsapp-client-os",
    "proposal-proof-os",
]
COMPLEXITY_ENUM = ["low", "medium", "high"]
CONFIDENCE_ENUM = ["low", "medium", "high"]

SCHEMAS_DEF = {
    "business_system": s(
        "Internal Business System",
        {
            "id": str_(),
            "name_ar": str_(),
            "core_system": {"type": "string", "enum": CORE_SYSTEM_ENUM},
            "complexity": {"type": "string", "enum": COMPLEXITY_ENUM},
            "starter_price_sar": {"type": "integer", "minimum": 0},
            "deliverables_count": {"type": "integer", "minimum": 1},
            "internal_only": {"type": "boolean"},
        },
        ["id", "name_ar", "core_system", "complexity", "starter_price_sar"],
    ),
    "need_taxonomy": s(
        "Business Need",
        {
            "id": str_(),
            "name_ar": str_(),
            "category": str_(),
            "core_system": {"type": "string", "enum": CORE_SYSTEM_ENUM},
            "buyer_role_ar": str_(),
        },
        ["id", "name_ar", "category", "core_system", "buyer_role_ar"],
    ),
    "specialized_sprint": s(
        "Specialized Sprint",
        {
            "id": str_(),
            "name_ar": str_(),
            "need_id": str_(),
            "core_system": {"type": "string", "enum": CORE_SYSTEM_ENUM},
            "sector": str_(),
            "complexity": {"type": "string", "enum": COMPLEXITY_ENUM},
            "duration_days": {"type": "integer", "minimum": 1},
            "starter_price_sar": {"type": "integer", "minimum": 0},
            "deliverables": arr(str_(), min_items=3),
            "required_inputs": arr(str_(), min_items=2),
            "acceptance_criteria": arr(str_(), min_items=2),
        },
        ["id", "name_ar", "need_id", "core_system", "sector",
         "deliverables", "required_inputs", "acceptance_criteria"],
    ),
    "sector_need_map": s(
        "Sector Need Map",
        {
            "sector": str_(),
            "sector_name_ar": str_(),
            "needs": arr(str_(), min_items=1),
        },
        ["sector", "sector_name_ar", "needs"],
    ),
    "need_to_system_route": s(
        "Need To System Route",
        {
            "need_id": str_(),
            "core_system": {"type": "string", "enum": CORE_SYSTEM_ENUM},
            "specialized_systems": arr(str_(), min_items=1),
        },
        ["need_id", "core_system", "specialized_systems"],
    ),
    "account_intelligence_pack": s(
        "Account Intelligence Pack",
        {
            "company_name": str_(),
            "website": str_(),
            "domain": {"type": "string"},
            "sector": str_(),
            "subsector": {"type": "string"},
            "city": {"type": "string"},
            "country": {"type": "string"},
            "demo": {"type": "boolean"},
            "signals_detected": arr(str_(), min_items=1),
            "evidence_level": {"type": "string", "enum": ["public", "founder_provided", "inferred"]},
            "detected_business_needs": arr(str_(), min_items=1),
            "primary_need": str_(),
            "secondary_need": {"type": "string"},
            "need_confidence": {"type": "string", "enum": CONFIDENCE_ENUM},
            "recommended_core_system": {"type": "string", "enum": CORE_SYSTEM_ENUM},
            "recommended_specialized_system": str_(),
            "sector_specific_sprint": str_(),
            "delivery_variant": str_(),
            "buyer_roles": arr(str_(), min_items=1),
            "public_contact_channels": arr({"type": "string"}, min_items=0),
            "contact_confidence": {"type": "string", "enum": CONFIDENCE_ENUM},
            "email_angle": str_(),
            "call_angle": str_(),
            "mini_proposal_title": str_(),
            "required_inputs": arr(str_(), min_items=1),
            "acceptance_criteria": arr(str_(), min_items=1),
            "cash_priority_score": {"type": "number", "minimum": 0, "maximum": 100},
            "need_fit_score": {"type": "number", "minimum": 0, "maximum": 100},
            "account_score": {"type": "number", "minimum": 0, "maximum": 100},
            "final_account_score": {"type": "number", "minimum": 0, "maximum": 100},
            "next_action": str_(),
            "suppressed": {"type": "boolean"},
        },
        [
            "company_name", "website", "sector", "signals_detected", "evidence_level",
            "detected_business_needs", "primary_need", "need_confidence",
            "recommended_core_system", "recommended_specialized_system",
            "sector_specific_sprint", "buyer_roles", "contact_confidence",
            "email_angle", "call_angle", "mini_proposal_title", "required_inputs",
            "acceptance_criteria", "cash_priority_score", "need_fit_score",
            "account_score", "final_account_score", "next_action",
        ],
    ),
    "contact_discovery": s(
        "Contact Discovery Record",
        {
            "company_name": str_(),
            "channels": arr(
                s(
                    "Channel",
                    {
                        "type": {"type": "string", "enum": ["website", "email", "phone", "linkedin", "whatsapp_business", "contact_form"]},
                        "value": str_(),
                        "source": {"type": "string", "enum": ["public", "founder_provided"]},
                        "confidence": {"type": "string", "enum": CONFIDENCE_ENUM},
                    },
                    ["type", "value", "source", "confidence"],
                ),
                min_items=0,
            ),
            "invented": {"type": "boolean", "const": False},
        },
        ["company_name", "channels", "invented"],
    ),
    "email_draft": s(
        "Email Draft",
        {
            "company_name": str_(),
            "to_role": str_(),
            "subject": str_(),
            "body": str_(min_len=20),
            "core_system": {"type": "string", "enum": CORE_SYSTEM_ENUM},
            "sector_specific_sprint": str_(),
            "cta": str_(),
            "client_need_card_ref": str_(),
            "approval_required": {"type": "boolean", "const": True},
            "status": {"type": "string", "enum": ["draft", "approved", "rejected"]},
        },
        ["company_name", "to_role", "subject", "body", "core_system",
         "sector_specific_sprint", "cta", "client_need_card_ref", "approval_required"],
    ),
    "call_brief": s(
        "Call Brief",
        {
            "company_name": str_(),
            "buyer_role": str_(),
            "primary_need": str_(),
            "core_system": {"type": "string", "enum": CORE_SYSTEM_ENUM},
            "opening_ar": str_(),
            "questions": arr(str_(), min_items=2),
            "value_points": arr(str_(), min_items=1),
            "objections_ref": str_(),
            "next_step": str_(),
        },
        ["company_name", "buyer_role", "primary_need", "core_system",
         "opening_ar", "questions", "value_points", "next_step"],
    ),
    "mini_proposal": s(
        "Mini Proposal",
        {
            "company_name": str_(),
            "title": str_(),
            "core_system": {"type": "string", "enum": CORE_SYSTEM_ENUM},
            "sprint_id": str_(),
            "starter_price_sar": {"type": "integer", "minimum": 1},
            "deliverables": arr(str_(), min_items=2),
            "timeline_days": {"type": "integer", "minimum": 1},
            "required_inputs": arr(str_(), min_items=1),
            "open_scope": {"type": "boolean", "const": False},
            "approval_required": {"type": "boolean", "const": True},
            "status": {"type": "string", "enum": ["draft", "approved", "sent", "won", "lost"]},
        },
        ["company_name", "title", "core_system", "sprint_id", "starter_price_sar",
         "deliverables", "timeline_days", "required_inputs", "open_scope", "approval_required"],
    ),
    "delivery_pipeline": s(
        "Delivery Pipeline",
        {
            "client": str_(),
            "selected_system": {"type": "string", "enum": CORE_SYSTEM_ENUM},
            "sprint_id": str_(),
            "scope": str_(),
            "required_inputs": arr(str_(), min_items=1),
            "success_metric": str_(),
            "acceptance_criteria": arr(str_(), min_items=1),
            "owner": str_(),
            "stage": {"type": "string", "enum": ["intake", "build", "review", "handoff", "value_report", "closed"]},
            "inputs_received": {"type": "boolean"},
        },
        ["client", "selected_system", "sprint_id", "scope", "required_inputs",
         "success_metric", "acceptance_criteria", "owner", "stage"],
    ),
    "weekly_value_report": s(
        "Weekly Value Report",
        {
            "client": str_(),
            "week_of": str_(),
            "system": {"type": "string", "enum": CORE_SYSTEM_ENUM},
            "metrics": arr(
                s("Metric", {"name": str_(), "value": str_(), "evidence": str_()}, ["name", "value"]),
                min_items=1,
            ),
            "next_actions": arr(str_(), min_items=1),
        },
        ["client", "week_of", "system", "metrics", "next_actions"],
    ),
    "delivery_acceptance_gate": s(
        "Delivery Acceptance Gate",
        {
            "sprint_id": str_(),
            "criteria": arr(str_(), min_items=1),
            "owner": str_(),
            "required_inputs": arr(str_(), min_items=1),
        },
        ["sprint_id", "criteria", "owner", "required_inputs"],
    ),
    "cash_priority_score": s(
        "Cash Priority Score",
        {
            "company_name": str_(),
            "urgency": {"type": "number", "minimum": 0, "maximum": 100},
            "ticket_potential": {"type": "number", "minimum": 0, "maximum": 100},
            "speed_to_cash": {"type": "number", "minimum": 0, "maximum": 100},
            "score": {"type": "number", "minimum": 0, "maximum": 100},
        },
        ["company_name", "score"],
    ),
    "quality_gate": s(
        "Quality Gate Result",
        {
            "gate": str_(),
            "subject": str_(),
            "passed": {"type": "boolean"},
            "failures": arr({"type": "string"}, min_items=0),
        },
        ["gate", "subject", "passed", "failures"],
    ),
}


def main():
    SCHEMAS.mkdir(parents=True, exist_ok=True)
    written = []
    for name, schema in SCHEMAS_DEF.items():
        path = SCHEMAS / f"{name}.schema.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(schema, f, ensure_ascii=False, indent=2)
            f.write("\n")
        written.append(path.name)
    print(f"Wrote {len(written)} schemas to schemas/:")
    for w in sorted(written):
        print(f"  - {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
