#!/usr/bin/env python3
"""Fail-closed verifier for Dealix founder event-market intelligence packs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PACK = ROOT / "data/founder/event_market_intelligence_2026-08-30.json"

EXPECTED_SCHEMA = "dealix.event-market-intelligence.v1"
EXPECTED_STATUS = "RESEARCH_ONLY_NO_RELATIONSHIP_TRUTH"
CANONICAL_PACKAGES = {
    "REVENUE_COMMAND_PILOT",
    "COMPANY_BRAIN_GOVERNED_AI_SPRINT",
    "SAUDI_MARKET_ACCESS_SPRINT",
    "PARTNER_IMPLEMENTATION_PROOF_LAYER",
    "FREE_MINI_DIAGNOSTIC_THEN_QUALIFIED_DISCOVERY",
    "RESEARCH_NURTURE_OR_SUPPRESS",
}
REQUIRED_CAPTURE = {
    "event_id",
    "company",
    "person_and_role_as_stated",
    "timestamp_and_location",
    "what_they_actually_said",
    "named_or_observed_pain",
    "current_workflow_or_owner_if_known",
    "follow_up_permission_or_channel_eligibility",
    "next_evidence",
    "next_action",
}


def fail(message: str) -> None:
    raise SystemExit(f"DEALIX_EVENT_MARKET_INTELLIGENCE=FAIL\nFAIL: {message}")


def load_pack(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load pack: {exc}")
    if not isinstance(payload, dict):
        fail("pack must be a JSON object")
    return payload


def validate_pack(payload: dict[str, Any]) -> None:
    if payload.get("schema") != EXPECTED_SCHEMA:
        fail("schema drift")
    if payload.get("status") != EXPECTED_STATUS:
        fail("event pack may not claim relationship truth")

    firewall = payload.get("truth_firewall", {})
    if not firewall or not all(value is False for value in firewall.values()):
        fail("truth firewall must remain all false")
    authority = payload.get("authority", {})
    if not authority or not all(value is False for value in authority.values()):
        fail("event research pack may grant no authority")

    windows = payload.get("event_windows", [])
    if len(windows) < 3:
        fail("expected Big5, LEAP and DeepFest event windows")
    for window in windows:
        if not window.get("event_id") or not window.get("dates") or not window.get("venue"):
            fail("event window missing identity/date/venue")
        sources = window.get("sources", [])
        if not sources or not all(str(source).startswith("https://") for source in sources):
            fail(f"event window lacks source-bound official URLs: {window.get('event_id')}")

    routes = payload.get("big5_founder_route", [])
    if not routes:
        fail("Big5 founder route missing")
    seen_companies: set[str] = set()
    for route in routes:
        if not route.get("hall"):
            fail("route hall missing")
        for target in route.get("targets", []):
            company = str(target.get("company", "")).strip()
            if not company or company in seen_companies:
                fail("target company missing or duplicated")
            seen_companies.add(company)
            if not target.get("stand"):
                fail(f"stand missing: {company}")
            if len(target.get("official_facts", [])) < 2:
                fail(f"official facts insufficient: {company}")
            if not str(target.get("dealix_hypothesis", "")).strip():
                fail(f"bounded Dealix hypothesis missing: {company}")
            if len(target.get("conversation_questions", [])) != 3:
                fail(f"exactly three founder questions required: {company}")
            if not target.get("next_evidence"):
                fail(f"next evidence missing: {company}")
            packages = set(target.get("package_hypotheses_only", []))
            if not packages or not packages.issubset(CANONICAL_PACKAGES):
                fail(f"non-canonical package hypothesis: {company}")

    lanes = payload.get("leap_deepfest_research_lanes", [])
    if len(lanes) < 3:
        fail("LEAP/DeepFest research lanes missing")
    for lane in lanes:
        if not lane.get("lane") or not lane.get("research_targets"):
            fail("LEAP/DeepFest lane missing target set")
        if not lane.get("conversation_goal") or not lane.get("next_evidence"):
            fail(f"lane missing goal/evidence: {lane.get('lane')}")

    if set(payload.get("founder_capture_minimum", [])) != REQUIRED_CAPTURE:
        fail("founder capture minimum drift")

    sla = payload.get("post_interaction_internal_sla", {})
    if sla.get("external_send") is not False:
        fail("post-interaction SLA may not auto-send")
    outputs = set(sla.get("outputs", []))
    required_outputs = {
        "interaction evidence receipt",
        "account context card",
        "qualified-problem hypothesis with unknowns",
        "package hypothesis only",
        "mini diagnostic outline",
        "discovery questions",
        "channel-eligible follow-up draft",
    }
    if not required_outputs.issubset(outputs):
        fail("post-interaction internal output coverage drift")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_PACK)
    args = parser.parse_args()
    payload = load_pack(args.path)
    validate_pack(payload)
    print("DEALIX_EVENT_MARKET_INTELLIGENCE=PASS")
    print(f"pack={args.path}")
    print("EVENT_DIRECTORY_TO_RELATIONSHIP=BLOCKED")
    print("PUBLIC_CONTACT_TO_CONSENT=BLOCKED")
    print("PACKAGE_OUTPUT=HYPOTHESIS_ONLY")
    print("POST_INTERACTION_EXTERNAL_SEND=FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
