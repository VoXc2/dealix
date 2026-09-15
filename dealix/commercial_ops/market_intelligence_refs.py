"""Load commercial market intelligence pack (YAML) for digest and APIs."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

from dealix.commercial.official_source_watch import (
    OfficialSourceWatchRegistry,
    build_official_signal,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
REFS_PATH = REPO_ROOT / "dealix" / "config" / "market_intelligence_refs.yaml"
MARKET_SIGNAL_RECEIPTS_PATH = REPO_ROOT / "data" / "commercial" / "market_signal_receipts_v1.json"

OFFICIAL_HOST_AUTHORITIES = {
    "cst.gov.sa": "CST",
    "mc.gov.sa": "MOC",
    "moh.gov.sa": "MOH",
    "monshaat.gov.sa": "MONSHAAT",
    "nca.gov.sa": "NCA",
    "sama.gov.sa": "SAMA",
    "stats.gov.sa": "GASTAT",
    "zatca.gov.sa": "ZATCA",
}

# Pillar order for weekly rotation (founder reads one deep doc per week)
PILLAR_ROTATION = (
    "saas_market",
    "governed_ai",
    "pdpl_legal",
    "founder_revops",
    "content_gtm",
    "positioning",
    "cloud_residency",
    "sales_champion",
)


@lru_cache(maxsize=1)
def load_market_intelligence_refs() -> dict[str, Any]:
    if not REFS_PATH.is_file():
        return {"version": "0", "pillars": {}, "index": ""}
    data = yaml.safe_load(REFS_PATH.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def market_intelligence_pillars_flat() -> list[dict[str, str]]:
    refs = load_market_intelligence_refs()
    out: list[dict[str, str]] = []
    for key, item in (refs.get("pillars") or {}).items():
        if isinstance(item, dict) and item.get("path"):
            out.append(
                {
                    "id": str(key),
                    "doc": str(item["path"]),
                    "topic_ar": str(item.get("label_ar") or key),
                }
            )
    return sorted(out, key=lambda x: x["id"])


def _official_authority_for_url(url: str) -> str | None:
    host = (urlparse(url).hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    return OFFICIAL_HOST_AUTHORITIES.get(host)


def _registry_id_for_signal(authority: str, signal_id: str) -> str:
    key = signal_id.lower()
    if authority == "ZATCA" and "wave25" in key:
        return "zatca_wave25"
    if authority == "NCA" and "cyber" in key:
        return "nca_ai_cybersecurity"
    if authority == "MONSHAAT" and "jadeer" in key:
        return "monshaat_jadeer"
    return "UNKNOWN"


def _receipt_excerpt(item: dict[str, Any]) -> str:
    facts = [str(v).strip() for v in (item.get("facts") or []) if str(v).strip()]
    return " | ".join(facts[:2])


def _display_receipts_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def build_official_source_watch_digest_block(
    now: datetime | None = None,
    *,
    receipts_path: Path = MARKET_SIGNAL_RECEIPTS_PATH,
) -> dict[str, Any]:
    """Derive a read-only watch view from the existing canonical market receipts."""
    dt = now or datetime.now(UTC)
    if not receipts_path.is_file():
        return {
            "status": "HOLD_MISSING_CANONICAL_RECEIPTS",
            "source_path": _display_receipts_path(receipts_path),
            "signal_count": 0,
            "fresh_count": 0,
            "hold_count": 0,
            "skipped_count": 0,
            "signals": [],
            "authority": _research_only_authority(),
        }
    try:
        payload = json.loads(receipts_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {
            "status": "HOLD_INVALID_CANONICAL_RECEIPTS",
            "source_path": _display_receipts_path(receipts_path),
            "signal_count": 0,
            "fresh_count": 0,
            "hold_count": 0,
            "skipped_count": 0,
            "signals": [],
            "authority": _research_only_authority(),
        }

    registry = OfficialSourceWatchRegistry()
    skipped = 0
    for item in payload.get("signals") or []:
        if not isinstance(item, dict):
            skipped += 1
            continue
        url = str(item.get("source_ref") or "").strip()
        authority = _official_authority_for_url(url)
        excerpt = _receipt_excerpt(item)
        if not authority or not excerpt:
            skipped += 1
            continue
        signal_id = str(item.get("signal_id") or "UNKNOWN")
        source_registry_id = _registry_id_for_signal(authority, signal_id)
        facts = item.get("facts") or []
        inferences = item.get("inferences") or []
        signal = build_official_signal(
            source_authority=authority,
            canonical_url=url,
            canonical_ref=signal_id,
            sector=str(item.get("sector_family") or "UNKNOWN").lower(),
            topic=str(item.get("signal_family") or signal_id),
            title_en=signal_id,
            published_at=str(item.get("observed_at") or "UNKNOWN"),
            observed_at=str(item.get("ingested_at") or item.get("observed_at") or dt.isoformat()),
            expires_at=str(item.get("fresh_until") or "UNKNOWN"),
            evidence_excerpt=excerpt,
            evidence_ref=str(item.get("provenance_ref") or url),
            source_registry_id=source_registry_id,
            confidence=0.5,
            regulatory_impact=str(facts[0]) if facts else "UNKNOWN",
            commercial_impact=str(inferences[0]) if inferences else "UNKNOWN",
            now=dt,
        )
        registry.ingest(signal)

    fresh = registry.list_fresh(now=dt)
    held = registry.list_hold(now=dt)
    signals: list[dict[str, Any]] = []
    for sig in [*fresh, *held]:
        radar = sig.to_radar_signal()
        signals.append(
            {
                "signal_id": sig.signal_id,
                "source_authority": sig.source_authority,
                "canonical_ref": sig.canonical_ref,
                "sector": sig.sector,
                "freshness": sig.freshness_state(now=dt).value,
                "evidence_ref": sig.evidence_ref,
                "evidence_hash": sig.evidence_hash,
                "internal_action": sig.recommended_internal_action,
                "relationship_state": sig.relationship_state,
                "consent_state": sig.consent_state,
                "counts_as_pipeline": sig.counts_as_pipeline,
                "allows_external_send": sig.allows_external_send,
                "economic_governor_hint": sig.economic_governor_hint(),
                "radar_projection": {
                    "signal_id": radar.signal_id,
                    "source": radar.source.value,
                    "problem": radar.problem,
                    "commercial_implication": radar.commercial_implication,
                    "counts_as_relationship": radar.counts_as_relationship,
                    "counts_as_consent": radar.counts_as_consent,
                    "counts_as_pipeline": radar.counts_as_pipeline,
                    "counts_as_revenue": radar.counts_as_revenue,
                },
            }
        )
    return {
        "status": "PASS_READ_ONLY_EVIDENCE" if signals else "HOLD_NO_RECOGNIZED_OFFICIAL_RECEIPTS",
        "source_path": _display_receipts_path(receipts_path),
        "signal_count": len(signals),
        "fresh_count": len(fresh),
        "hold_count": len(held),
        "skipped_count": skipped,
        "signals": signals,
        "authority": _research_only_authority(),
    }


def _research_only_authority() -> dict[str, bool]:
    return {
        "relationship": False,
        "consent": False,
        "buyer_intent": False,
        "pipeline": False,
        "revenue": False,
        "external_send": False,
    }


def market_intelligence_status() -> dict[str, Any]:
    refs = load_market_intelligence_refs()
    pillars = refs.get("pillars") or {}
    missing: list[str] = []
    for _key, item in pillars.items():
        if not isinstance(item, dict):
            continue
        rel = item.get("path")
        if rel and not (REPO_ROOT / str(rel)).is_file():
            missing.append(str(rel))
    index = refs.get("index")
    if index and not (REPO_ROOT / str(index)).is_file():
        missing.append(str(index))
    return {
        "ok": bool(pillars) and not missing,
        "pillar_count": len(pillars),
        "missing_paths": missing,
        "index": index,
        "version": refs.get("version"),
    }

def pillar_of_week(now: datetime | None = None) -> dict[str, str] | None:
    """Rotate one pillar doc per ISO week for founder deep read."""
    refs = load_market_intelligence_refs()
    pillars = refs.get("pillars") or {}
    if not pillars:
        return None
    dt = now or datetime.now(UTC)
    week = dt.isocalendar().week
    key = PILLAR_ROTATION[week % len(PILLAR_ROTATION)]
    item = pillars.get(key)
    if not isinstance(item, dict):
        return None
    return {
        "id": key,
        "doc": str(item.get("path") or ""),
        "topic_ar": str(item.get("label_ar") or key),
    }


def build_market_intel_digest_block(now: datetime | None = None) -> dict[str, Any]:
    dt = now or datetime.now(UTC)
    st = market_intelligence_status()
    pow_doc = pillar_of_week(dt)
    is_friday = dt.weekday() == 4  # Monday=0
    refs = load_market_intelligence_refs()
    official_watch = build_official_source_watch_digest_block(dt)
    return {
        "status_ok": st["ok"],
        "pillar_of_week": pow_doc,
        "is_friday_review": is_friday,
        "friday_checklist": (
            "docs/commercial/MARKET_INTELLIGENCE_WEEKLY_REVIEW_CHECKLIST_AR.md"
            if is_friday
            else None
        ),
        "master_index": refs.get("index"),
        "implementation_playbook": "docs/commercial/MARKET_INTELLIGENCE_IMPLEMENTATION_PLAYBOOK_AR.md",
        "external_sources": refs.get("external_sources") or {},
        "official_source_watch": official_watch,
    }
