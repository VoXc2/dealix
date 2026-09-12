from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial.economic_cell import Sector


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "dealix/config/commercial_reset_2026_09_12.yaml"
FRESH_POLICY_PATH = ROOT / "config/company/fresh_market_execution_policy.json"
LEGACY_OWNER_ALIASES = (
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
)
LAYERS = ("group", "sector", "arm")
CANONICAL_SECTOR_IDS = frozenset(sector.value for sector in Sector)


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("commercial reset config must be a mapping")
    return payload


def load_fresh_policy(path: Path = FRESH_POLICY_PATH) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("fresh-market policy must be a mapping")
    return payload


def _resolve_identity(
    *,
    config: dict[str, Any],
    layer: str,
    role: str,
    sector: str = "",
    arm: str = "",
    legacy_agent: str = "",
) -> tuple[str, str, str, str]:
    architecture = config["architecture"]
    if legacy_agent:
        aliases = architecture["legacy_owner_aliases"]
        if legacy_agent not in aliases:
            raise ValueError(f"unknown legacy owner alias: {legacy_agent}")
        layer = "group"
        role = aliases[legacy_agent]

    if layer not in LAYERS:
        raise ValueError(f"layer must be one of {LAYERS}")

    if layer == "group":
        if role not in architecture["group_roles"]:
            raise ValueError(f"invalid group role: {role}")
        return f"dealix.group.{role}", "dealix.group", layer, role

    if not sector:
        raise ValueError(f"sector is required for {layer} packets")
    if sector not in CANONICAL_SECTOR_IDS:
        raise ValueError(
            f"unknown canonical sector: {sector}; use dealix.commercial.economic_cell.Sector.value"
        )

    if layer == "sector":
        if role not in architecture["sector_role_templates"]:
            raise ValueError(f"invalid sector role: {role}")
        return f"dealix.{sector}.{role}", f"dealix.{sector}", layer, role

    if not arm:
        raise ValueError("arm is required for arm packets")
    allowed = set(architecture["arm_pod_roles"])
    allowed.update(architecture["additional_specialists_allowed_when_justified"])
    if role not in allowed:
        raise ValueError(f"invalid arm role: {role}")
    return f"dealix.{sector}.{arm}.{role}", f"dealix.{sector}.{arm}", layer, role


def build_work_packet(
    *,
    opportunity_id: str,
    entity: str,
    stage: str,
    problem: str,
    function: str = "OPPORTUNITY_SCORING",
    layer: str = "group",
    role: str = "",
    sector: str = "",
    arm: str = "",
    agent: str = "",
    relationship_state: str = "UNKNOWN",
    consent_state: str = "UNKNOWN",
    next_state_sought: str = "",
    evidence_refs: list[str] | None = None,
    facts: list[str] | None = None,
    inferences: list[str] | None = None,
    missing_evidence: list[str] | None = None,
    urgency: str = "NORMAL",
) -> dict[str, Any]:
    config = load_config()
    policy = load_fresh_policy()
    routing = config["commercial_function_routing"].get(function)
    if not isinstance(routing, dict):
        raise ValueError(f"unknown commercial function: {function}")

    role = role or str(routing[f"{layer}_role"])
    identity, parent, resolved_layer, resolved_role = _resolve_identity(
        config=config,
        layer=layer,
        role=role,
        sector=sector,
        arm=arm,
        legacy_agent=agent,
    )

    pricing = config["pricing"]
    return {
        "schema_version": "2026-09-12-agentic-holding-v2",
        "commercial_reset": config["name"],
        "architecture": policy["architecture"]["model"],
        "opportunity_id": opportunity_id,
        "entity": entity,
        "stage": stage,
        "sector": sector or None,
        "arm": arm or None,
        "problem": problem,
        "problem_evidence": evidence_refs or [],
        "relationship_state": relationship_state,
        "consent_state": consent_state,
        "solution_family": None,
        "facts": facts or [],
        "inferences": inferences or [],
        "missing_evidence": missing_evidence or [],
        "next_state_sought": next_state_sought,
        "next_action": "derive from current evidence, commercial function and authority scope",
        "commercial_function": function,
        "agent_identity": identity,
        "agent_parent": parent,
        "agent_layer": resolved_layer,
        "agent_role": resolved_role,
        "legacy_owner_alias": agent or None,
        "routing": routing,
        "urgency": urgency,
        "runtime_activation": policy["architecture"]["runtime_workers"],
        "resource_governor_inputs": config["architecture"]["runtime_governor_inputs"],
        "authority_required": "exact action-bound authority for any material external effect",
        "safe_to_send": False,
        "price_authority": pricing["quote_authority"],
        "pricing_reference_authority": pricing["internal_reference_authority"],
        "truth_firewall": config["truth_firewall"],
        "output_or_receipt_ref": None,
    }


def build_holding_blueprint() -> dict[str, Any]:
    config = load_config()
    architecture = config["architecture"]
    arm_templates: list[dict[str, Any]] = []
    try:
        from dealix.commercial.arm_registry import get_active_arms

        arms = get_active_arms()
    except Exception:
        arms = []
    for current in arms:
        arm_templates.append(
            {
                "arm_id": current.arm_id,
                "legacy_owner_alias": current.owner_agent,
                "activation": "on-demand-after-sector-fit",
                "pod_roles": list(architecture["arm_pod_roles"]),
                "identity_template": f"dealix.<sector>.{current.arm_id}.<role>",
            }
        )

    return {
        "architecture": architecture["model"],
        "legacy_fixed_five_permanent_agents": architecture[
            "legacy_fixed_five_permanent_agents"
        ],
        "legacy_owner_aliases": architecture["legacy_owner_aliases"],
        "group_roles": architecture["group_roles"],
        "sector_role_templates": architecture["sector_role_templates"],
        "arm_pod_roles": architecture["arm_pod_roles"],
        "arm_templates": arm_templates,
        "runtime_workers": architecture["runtime_workers"],
        "orphan_agents_allowed": architecture["orphan_agents_allowed"],
    }


def build_daily_packets() -> dict[str, Any]:
    config = load_config()
    money_now = [
        row["id"] for row in config["campaigns"] if row.get("status") == "MONEY_NOW"
    ]
    group_functions = (
        "TOP_ECONOMIC_ORDERING",
        "MARKET_INTELLIGENCE",
        "OPPORTUNITY_SCORING",
        "PRICING_PREP",
        "GOVERNANCE_REVIEW",
        "DELIVERY",
        "PROOF",
        "ENGINEERING",
        "CONTENT",
        "SELF_IMPROVEMENT",
    )
    group_packets = [
        build_work_packet(
            opportunity_id=f"DAILY:{function}",
            entity="Dealix",
            stage="INTERNAL_EXECUTION",
            problem="Execute the highest-value evidence-backed company work",
            function=function,
        )
        for function in group_functions
    ]
    sector_packets = []
    for sector in config["sector_priority"]["A1"]:
        if sector not in CANONICAL_SECTOR_IDS:
            raise ValueError(f"noncanonical priority sector: {sector}")
        sector_packets.append(
            {
                "sector": sector,
                "agent_identity": f"dealix.{sector}.sector-ceo",
                "agent_parent": f"dealix.{sector}",
                "runtime_activation": "lazy_resource_governed",
                "activation_functions": [
                    "MARKET_INTELLIGENCE",
                    "OPPORTUNITY_SCORING",
                    "DIAGNOSTIC",
                    "SOLUTION_DESIGN",
                    "CONTENT",
                    "PROOF",
                ],
                "money_now_campaigns": money_now,
                "safe_to_send": False,
            }
        )
    return {
        "group_packets": group_packets,
        "sector_company_packets": sector_packets,
        "holding_blueprint": build_holding_blueprint(),
        "dispatch_policy": "lazy_resource_governed",
        "external_effects": "exact_action_bound",
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render Dealix Commercial Reset hierarchical agent packets"
    )
    parser.add_argument("--daily", action="store_true")
    parser.add_argument("--blueprint", action="store_true")
    parser.add_argument("--agent", default="", help="legacy owner alias compatibility")
    parser.add_argument("--layer", choices=LAYERS, default="group")
    parser.add_argument("--role", default="")
    parser.add_argument("--function", default="OPPORTUNITY_SCORING")
    parser.add_argument("--opportunity-id", default="")
    parser.add_argument("--entity", default="")
    parser.add_argument("--sector", default="")
    parser.add_argument("--arm", default="")
    parser.add_argument("--stage", default="RESEARCH_ONLY")
    parser.add_argument("--problem", default="")
    parser.add_argument("--relationship-state", default="UNKNOWN")
    parser.add_argument("--consent-state", default="UNKNOWN")
    parser.add_argument("--next-state-sought", default="")
    parser.add_argument("--urgency", default="NORMAL")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if args.blueprint:
        payload: Any = build_holding_blueprint()
    elif args.daily:
        payload = build_daily_packets()
    else:
        payload = build_work_packet(
            agent=args.agent,
            layer=args.layer,
            role=args.role,
            function=args.function,
            opportunity_id=args.opportunity_id,
            entity=args.entity,
            sector=args.sector,
            arm=args.arm,
            stage=args.stage,
            problem=args.problem,
            relationship_state=args.relationship_state,
            consent_state=args.consent_state,
            next_state_sought=args.next_state_sought,
            urgency=args.urgency,
        )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())