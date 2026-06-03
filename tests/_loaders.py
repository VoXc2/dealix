"""Shared loaders + canonical gate logic for the Dealix Market/Commercial tests.

These functions are the authoritative Python mirror of scripts/_lib/dealix.js.
A cross-language check (tests/test_gtm_quality_gate.py) runs the Node gate over
the same eval cases to confirm both implementations agree.

Dependency: PyYAML (dev). Install with:  pip install pyyaml
(See requirements-dev.txt / tests/README.md.)
"""
from __future__ import annotations
import json
from pathlib import Path

import yaml  # PyYAML — dev dependency

ROOT = Path(__file__).resolve().parents[1]


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def load_yaml(rel: str):
    return yaml.safe_load(read_text(rel))


def load_json(rel: str):
    return json.loads(read_text(rel))


def load_jsonl(rel: str) -> list[dict]:
    out = []
    for i, line in enumerate(read_text(rel).splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as e:  # pragma: no cover - surfaces bad data
            raise AssertionError(f"Invalid JSON in {rel} line {i}: {e}") from e
    return out


# ---- canonical reference data ------------------------------------------------

def forbidden() -> dict:
    d = load_yaml("data/commercial/forbidden_claims.yaml")
    return {
        "phrases": [p.lower() for p in (d["forbidden_ar"] + d["forbidden_en"])],
        "prefixes": [p.lower() for p in d["forbidden_subject_prefixes"]],
    }


def suppression(rel: str = "data/outreach/suppression_list.jsonl") -> set[str]:
    return {str(r["value"]).lower() for r in load_jsonl(rel)}


def catalog_ids() -> set[str]:
    return {o["id"] for o in load_yaml("data/commercial/product_catalog.yaml")["offers"]}


REQUIRED_DRAFT_FIELDS = [
    "prospect_id", "company", "sector", "pain_hypothesis", "offer_match",
    "personalization_score", "evidence_level", "risk_level", "opt_out",
    "approval_status", "send_status",
]
COLD_TYPES = {"first_touch", "follow_up_1", "follow_up_2"}
SENDABLE_VERDICTS = {"LIMITED_SEND_READY", "RAMP_READY"}


# ---- gate logic (mirror of scripts/_lib/dealix.js) ---------------------------

def gate_draft(d: dict, fb: dict, sup: set[str]) -> dict:
    reasons: list[str] = []
    subj = str(d.get("subject", "")).lower()
    body = str(d.get("body", "")).lower()

    if any(f not in d or d.get(f) is None for f in REQUIRED_DRAFT_FIELDS):
        reasons.append("missing_required_field")
    if any(ph and (ph in subj or ph in body) for ph in fb["phrases"]):
        reasons.append("forbidden_claim")
    if any(pre and subj.startswith(pre) for pre in fb["prefixes"]):
        reasons.append("fake_thread")
    if d.get("personalization_score") == "P0":
        reasons.append("below_p1")
    if d.get("draft_type") in COLD_TYPES and not (d.get("opt_out") or {}).get("included"):
        reasons.append("missing_unsubscribe")
    dom = str(d.get("recipient_domain", "")).lower()
    comp = str(d.get("company", "")).lower()
    if (dom and dom in sup) or (comp and comp in sup):
        reasons.append("suppressed")

    reasons = list(dict.fromkeys(reasons))
    return {"ok": not reasons, "reasons": reasons}


def is_send_ready(d: dict, fb: dict, sup: set[str], verdict: str) -> bool:
    """A draft is send-ready ONLY if it passes all gates AND is approved AND the
    deliverability verdict allows sending AND it is not suppressed."""
    g = gate_draft(d, fb, sup)
    return (
        g["ok"]
        and d.get("approval_status") == "approved"
        and verdict in SENDABLE_VERDICTS
    )


def find_forbidden(text: str, fb: dict) -> list[str]:
    t = str(text).lower()
    return [ph for ph in fb["phrases"] if ph and ph in t]


# ---- commercial rule logic ---------------------------------------------------

def evaluate_pricing(x: dict) -> dict:
    reasons = []
    custom = set(load_yaml("data/commercial/pricing_rules.yaml")["custom_offer_ids"])
    if x.get("final_price") is not None and x.get("approval_status") != "approved":
        reasons.append("final_price_without_approval")
    if x.get("offer_id") in custom and x.get("tier") == "starter":
        reasons.append("custom_scope_at_starter_price")
    return {"ok": not reasons, "reasons": reasons}


def evaluate_proposal(x: dict) -> dict:
    reasons = []
    if not x.get("qualified"):
        reasons.append("opportunity_not_qualified")
    if not x.get("product_match"):
        reasons.append("missing_product_match")
    if not x.get("pain_category"):
        reasons.append("missing_pain_category")
    return {"ok": not reasons, "reasons": reasons}


def evaluate_fit(x: dict) -> dict:
    """Walk-away / disqualification rules (docs/commercial/DISQUALIFICATION_RULES_AR.md)."""
    bad = (
        x.get("wants_mass_sending")
        or x.get("wants_guaranteed_sales")
        or x.get("refuses_approval")
        or x.get("requests_scraping")
        or not x.get("recurring_leads")
        or not x.get("decision_maker_access")
        or not x.get("ability_to_pay")
    )
    return {"ok": not bad, "reasons": [] if not bad else ["disqualified_bad_fit"]}


def evaluate_partner(x: dict) -> dict:
    ok = x["margin_pct"] >= x["min_margin_pct"]
    return {"ok": ok, "reasons": [] if ok else ["below_min_margin"]}
