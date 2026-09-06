"""Evidence-first targeting intelligence for Dealix commercial execution.

This module is intentionally upstream of outreach.  It scores commercial value,
checks dossier completeness, and evaluates channel eligibility without granting
external send authority.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Iterable, Mapping
from urllib.parse import urlparse
import re

SCHEMA = "dealix.targeting-dossier.v1"

SCORE_WEIGHTS: dict[str, int] = {
    "icp_fit": 15,
    "problem_evidence": 20,
    "why_now": 20,
    "offer_fit": 10,
    "buyer_partner_route": 10,
    "proofability": 10,
    "economic_value": 10,
    "evidence_confidence": 5,
}

RELATIONSHIP_STATES = {
    "UNKNOWN",
    "RESEARCH_ONLY",
    "KNOWN",
    "WARM",
    "INBOUND",
    "ACTIVE_CONVERSATION",
}
CONSENT_STATES = {
    "UNKNOWN",
    "NOT_REQUIRED_FOR_INTERNAL_RESEARCH",
    "OPTED_IN",
    "OPTED_OUT",
    "SUPPRESSED",
}
EMAIL_STATES = {"BLOCKED", "DRAFT_ONLY", "ELIGIBLE"}
WHATSAPP_STATES = {"BLOCKED", "INBOUND_ONLY", "TEMPLATE_ELIGIBLE", "ELIGIBLE"}
VOICE_STATES = {"BLOCKED", "INBOUND_ONLY", "CALLBACK_REQUESTED", "ELIGIBLE"}
EVIDENCE_TIERS = {"A", "B", "C", "D", "E"}

_PRE_DRAFT_REQUIRED = (
    "why_them",
    "why_now",
    "problem_hypothesis",
    "business_cost",
    "offer_route",
    "proof_baseline",
    "one_cta",
)


def _clean(value: Any) -> str:
    return str(value or "").strip()


def _normalize_company_name(value: str) -> str:
    text = re.sub(r"[^a-z0-9\u0600-\u06ff]+", " ", value.casefold())
    return " ".join(text.split())


def normalize_domain(value: str) -> str:
    """Return a stable host key without path, scheme, port, or leading www."""
    raw = _clean(value).lower()
    if not raw:
        return ""
    parsed = urlparse(raw if "://" in raw else f"https://{raw}")
    host = (parsed.hostname or "").lower().rstrip(".")
    if host.startswith("www."):
        host = host[4:]
    return host


def entity_key(dossier: Mapping[str, Any]) -> str:
    """Build a deterministic dedupe key, preferring provider IDs then domain."""
    entity = dossier.get("entity") or {}
    if not isinstance(entity, Mapping):
        entity = {}

    provider_ids = entity.get("provider_ids") or []
    if isinstance(provider_ids, Mapping):
        provider_ids = [f"{k}:{v}" for k, v in sorted(provider_ids.items()) if _clean(v)]
    if isinstance(provider_ids, Iterable) and not isinstance(provider_ids, (str, bytes)):
        ids = sorted(_clean(v) for v in provider_ids if _clean(v))
        if ids:
            return "provider:" + "|".join(ids)

    domain = normalize_domain(_clean(entity.get("domain")))
    if domain:
        return f"domain:{domain}"

    company = _normalize_company_name(_clean(entity.get("company")))
    return f"name:{company}" if company else ""


def _score_value(value: Any, *, field: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid score dimension: {field}") from exc
    if not 0 <= number <= 100:
        raise ValueError(f"score dimension out of range: {field}")
    return number


def score_target_value(dossier: Mapping[str, Any]) -> float:
    """Return weighted Target Value in [0, 100]. Missing dimensions fail closed."""
    dimensions = dossier.get("score_dimensions") or {}
    if not isinstance(dimensions, Mapping):
        raise ValueError("score_dimensions must be an object")

    missing = [name for name in SCORE_WEIGHTS if name not in dimensions]
    if missing:
        raise ValueError("missing score dimensions: " + ",".join(missing))

    total = 0.0
    for name, weight in SCORE_WEIGHTS.items():
        total += _score_value(dimensions[name], field=name) * weight
    return round(total / 100.0, 2)


def priority_band(score: float) -> str:
    if score >= 85:
        return "P0"
    if score >= 70:
        return "P1"
    if score >= 55:
        return "P2"
    return "DEFER"


def _parse_datetime(value: Any) -> datetime | None:
    text = _clean(value)
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def evidence_issues(dossier: Mapping[str, Any], *, now: datetime | None = None) -> list[str]:
    """Validate evidence provenance/timestamps and explicit expiry without guessing consent."""
    evidence = dossier.get("evidence") or []
    if not isinstance(evidence, list) or not evidence:
        return ["MISSING_EVIDENCE"]

    now_utc = (now or datetime.now(UTC)).astimezone(UTC)
    issues: list[str] = []
    for idx, item in enumerate(evidence):
        if not isinstance(item, Mapping):
            issues.append(f"EVIDENCE_{idx}_INVALID")
            continue
        tier = _clean(item.get("tier")).upper()
        if tier not in EVIDENCE_TIERS:
            issues.append(f"EVIDENCE_{idx}_TIER_INVALID")
        if not _clean(item.get("source_url")):
            issues.append(f"EVIDENCE_{idx}_SOURCE_MISSING")
        if _parse_datetime(item.get("observed_at")) is None:
            issues.append(f"EVIDENCE_{idx}_OBSERVED_AT_INVALID")
        expires = item.get("expires_at")
        if expires:
            expiry_dt = _parse_datetime(expires)
            if expiry_dt is None:
                issues.append(f"EVIDENCE_{idx}_EXPIRY_INVALID")
            elif expiry_dt < now_utc:
                issues.append(f"EVIDENCE_{idx}_EXPIRED")
    return issues


def _state(actionability: Mapping[str, Any], key: str, allowed: set[str], default: str) -> str:
    value = _clean(actionability.get(key)).upper() or default
    return value if value in allowed else "INVALID"


def actionability_state(dossier: Mapping[str, Any]) -> dict[str, Any]:
    raw = dossier.get("actionability") or {}
    if not isinstance(raw, Mapping):
        raw = {}
    relationship = _state(raw, "relationship", RELATIONSHIP_STATES, "UNKNOWN")
    consent = _state(raw, "consent", CONSENT_STATES, "UNKNOWN")
    email = _state(raw, "email", EMAIL_STATES, "BLOCKED")
    whatsapp = _state(raw, "whatsapp", WHATSAPP_STATES, "BLOCKED")
    voice = _state(raw, "voice", VOICE_STATES, "BLOCKED")
    suppressed = bool(raw.get("suppressed")) or consent in {"OPTED_OUT", "SUPPRESSED"}
    return {
        "relationship": relationship,
        "consent": consent,
        "email": email,
        "whatsapp": whatsapp,
        "voice": voice,
        "suppressed": suppressed,
    }


def pre_draft_gate(dossier: Mapping[str, Any], *, now: datetime | None = None) -> dict[str, Any]:
    """Fail closed unless a target has enough evidence for a founder-quality draft."""
    reasons: list[str] = []
    if _clean(dossier.get("schema")) not in {"", SCHEMA}:
        reasons.append("SCHEMA_UNSUPPORTED")
    if not entity_key(dossier):
        reasons.append("ENTITY_UNRESOLVED")
    for key in _PRE_DRAFT_REQUIRED:
        if not _clean(dossier.get(key)):
            reasons.append(f"MISSING_{key.upper()}")
    reasons.extend(evidence_issues(dossier, now=now))

    action = actionability_state(dossier)
    if "INVALID" in action.values():
        reasons.append("ACTIONABILITY_INVALID")
    if action["suppressed"]:
        reasons.append("SUPPRESSED")

    try:
        score = score_target_value(dossier)
    except ValueError:
        score = None
        reasons.append("TARGET_VALUE_INVALID")

    return {
        "pass": not reasons,
        "reasons": sorted(set(reasons)),
        "target_value": score,
        "priority": priority_band(score) if score is not None else "HOLD",
        "actionability": action,
        "external_authority_granted": False,
    }


def channel_gate(dossier: Mapping[str, Any], channel: str) -> dict[str, Any]:
    """Evaluate channel eligibility only. This never grants live-send authority."""
    action = actionability_state(dossier)
    channel_name = _clean(channel).lower()
    reasons: list[str] = []

    if action["suppressed"]:
        reasons.append("SUPPRESSED")

    relationship = action["relationship"]
    consent = action["consent"]

    if channel_name == "email":
        if action["email"] != "ELIGIBLE":
            reasons.append("EMAIL_NOT_ELIGIBLE")
        if relationship in {"UNKNOWN", "RESEARCH_ONLY"} and consent != "OPTED_IN":
            reasons.append("NO_RELATIONSHIP_OR_OPT_IN")
    elif channel_name == "whatsapp":
        if action["whatsapp"] not in {"TEMPLATE_ELIGIBLE", "ELIGIBLE"}:
            reasons.append("WHATSAPP_NOT_ELIGIBLE")
        if relationship not in {"INBOUND", "ACTIVE_CONVERSATION", "WARM", "KNOWN"} and consent != "OPTED_IN":
            reasons.append("NO_PERMISSIONED_WHATSAPP_ROUTE")
    elif channel_name == "voice":
        if action["voice"] not in {"CALLBACK_REQUESTED", "ELIGIBLE"}:
            reasons.append("VOICE_NOT_ELIGIBLE")
        if relationship not in {"INBOUND", "ACTIVE_CONVERSATION", "WARM", "KNOWN"} and consent != "OPTED_IN":
            reasons.append("NO_PERMISSIONED_VOICE_ROUTE")
    else:
        reasons.append("CHANNEL_UNSUPPORTED")

    return {
        "eligible": not reasons,
        "reasons": sorted(set(reasons)),
        "external_authority_granted": False,
    }


def rank_dossiers(dossiers: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Score and rank dossiers while preserving duplicate ambiguity as a hold reason."""
    ranked: list[dict[str, Any]] = []
    key_counts: dict[str, int] = {}
    materialized = list(dossiers)
    for dossier in materialized:
        key = entity_key(dossier)
        if key:
            key_counts[key] = key_counts.get(key, 0) + 1

    for dossier in materialized:
        row = dict(dossier)
        gate = pre_draft_gate(row)
        key = entity_key(row)
        reasons = list(gate["reasons"])
        if key and key_counts.get(key, 0) > 1:
            reasons.append("HOLD_DUPLICATE_ENTITY")
        gate["reasons"] = sorted(set(reasons))
        gate["pass"] = not gate["reasons"]
        row["targeting"] = gate
        row["entity_key"] = key
        ranked.append(row)

    ranked.sort(
        key=lambda item: (
            float((item.get("targeting") or {}).get("target_value") or -1),
            _clean((item.get("entity") or {}).get("company")),
        ),
        reverse=True,
    )
    return ranked
