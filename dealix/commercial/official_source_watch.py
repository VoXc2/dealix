"""Official-Source Watch — Saudi market/regulatory change -> evidence-bound signal.

Smallest contract that turns official Saudi source changes into signals for the
existing Opportunity Graph / Economic Governor without pretending research is a
relationship.

Reuse (no parallel systems):
- ``dealix.commercial.saudi_market_radar.SignalSource`` — official authority enum.
- ``dealix.commercial.saudi_market_radar.RegulatorySignal`` — radar admission shape.
- ``dealix.company_intelligence.signal_contracts`` — CanonicalSignal/dedupe/stale.
- ``dealix.company_intelligence.source_contracts`` — provenance policy vocabulary.
- ``dealix.commercial.web_research_adapter`` — bounded read-only adapter pattern.
- ``config/market/market_signal_sources_v3.json`` — source registry (not graph).
- ``dealix.commercial.relationship_graph`` / ``consent_registry`` — truth firewall.

Truth firewall (structural, not advisory):
- research != relationship; public contact != consent; source mention != buyer
  intent; stale/unknown evidence != current fact.
- Every signal pins ``relationship_state=RESEARCH_ONLY`` and
  ``consent_state=NOT_PROVEN`` and all ``counts_as_*=False``.
- No method here sends, publishes, deploys, mutates DB/production, touches
  secrets/billing, or authorizes L5. Recommended actions are internal-only.

No live crawling in this task: adapter interfaces below are configuration-only
and disabled by default.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from dealix.commercial.saudi_market_radar import UNKNOWN, RegulatorySignal, SignalSource

UNKNOWN_REF = UNKNOWN

# Official authorities already used by Dealix, mapped onto the canonical
# SignalSource enum from saudi_market_radar (no second authority enum).
OFFICIAL_AUTHORITIES: dict[str, SignalSource] = {
    "CST": SignalSource.CST,
    "SDAIA": SignalSource.SDAIA_PDPL,
    "SDAIA_PDPL": SignalSource.SDAIA_PDPL,
    "NCA": SignalSource.NCA_ECC,
    "NCA_ECC": SignalSource.NCA_ECC,
    "ZATCA": SignalSource.ZATCA,
    "MOC": SignalSource.MINISTRY_COMMERCE,
    "MINISTRY_COMMERCE": SignalSource.MINISTRY_COMMERCE,
    "SAMA": SignalSource.SAMA,
    "MISA": SignalSource.MISA,
    "INVEST_SAUDI": SignalSource.MISA,
    "MOH": SignalSource.MOH,
    "REGA": SignalSource.REGA,
    "ETIMAD": SignalSource.ETIMAD,
    "MONSHAAT": SignalSource.MONSHAAT_JADEER,
    "MONSHAAT_JADEER": SignalSource.MONSHAAT_JADEER,
    "GASTAT": SignalSource.GASTAT,
    "SAUDI_OPEN_DATA": SignalSource.SAUDI_OPEN_DATA,
}

# Registry ids from config/market/market_signal_sources_v3.json that are
# official-source backed (subset relevant to regulatory/market watch).
OFFICIAL_REGISTRY_IDS = frozenset({
    "etimad_tenders",
    "zatca_wave25",
    "monshaat_jadeer",
    "nca_ai_cybersecurity",
    "misa_matchmaking",
    "rega_proptech_hub",
    "nupco_tenders",
})

INTERNAL_ACTIONS = (
    "INTERNAL_REVIEW_OFFICIAL_SOURCE",
    "PREPARE_DIAGNOSTIC_TEMPLATE",
    "REFRESH_EVIDENCE_BEFORE_USE",
    "HOLD_UNKNOWN_OR_STALE",
)

InternalAction = Literal[
    "INTERNAL_REVIEW_OFFICIAL_SOURCE",
    "PREPARE_DIAGNOSTIC_TEMPLATE",
    "REFRESH_EVIDENCE_BEFORE_USE",
    "HOLD_UNKNOWN_OR_STALE",
]


class FreshnessState(StrEnum):
    FRESH = "fresh"
    STALE = "stale"
    EXPIRED = "expired"
    HOLD = "hold"


def compute_evidence_hash(canonical_url: str, evidence_excerpt: str) -> str:
    """Deterministic evidence hash; stable across repeated watches."""
    payload = json.dumps(
        {"url": canonical_url or UNKNOWN, "excerpt": evidence_excerpt or ""},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def compute_dedupe_key(source_authority: str, canonical_ref: str, topic: str, sector: str) -> str:
    payload = json.dumps(
        {
            "source": (source_authority or UNKNOWN).strip().upper(),
            "ref": (canonical_ref or UNKNOWN).strip(),
            "topic": (topic or UNKNOWN).strip().lower(),
            "sector": (sector or UNKNOWN).strip().lower(),
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def resolve_authority(name: str) -> SignalSource | None:
    """Map a free-text authority name onto the canonical SignalSource enum."""
    if not name:
        return None
    return OFFICIAL_AUTHORITIES.get(name.strip().upper())


def recommend_internal_action(
    *,
    topic: str,
    freshness: FreshnessState,
    confidence: float,
    source_known: bool,
) -> InternalAction:
    """Signal -> internal-only next action. Never returns an external action."""
    if not source_known or freshness in (FreshnessState.EXPIRED, FreshnessState.HOLD):
        return "HOLD_UNKNOWN_OR_STALE"
    if freshness is FreshnessState.STALE:
        return "REFRESH_EVIDENCE_BEFORE_USE"
    if confidence < 0.5:
        return "REFRESH_EVIDENCE_BEFORE_USE"
    lowered = (topic or "").lower()
    if any(k in lowered for k in ("license", "permit", "tajweed", "wave", "mandate",
                                  "enforcement", "regulation", "compliance", "sanction",
                                  "sandbox", "tender", "procurement")):
        return "INTERNAL_REVIEW_OFFICIAL_SOURCE"
    return "PREPARE_DIAGNOSTIC_TEMPLATE"


class OfficialSourceSignal(BaseModel):
    """One evidence-bound official-source observation. Frozen, internal-only."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    signal_id: str
    source_authority: str = UNKNOWN  # e.g. ZATCA, SAMA, CST, ...
    source_registry_id: str = UNKNOWN  # id in market_signal_sources_v3.json
    canonical_url: str = UNKNOWN
    canonical_ref: str = UNKNOWN  # wave/tender/circular number or page slug
    sector: str = UNKNOWN
    topic: str = UNKNOWN
    title_en: str = UNKNOWN
    title_ar: str = UNKNOWN
    published_at: str = UNKNOWN  # ISO or UNKNOWN
    effective_at: str = UNKNOWN  # ISO or UNKNOWN
    observed_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    expires_at: str = UNKNOWN  # ISO or UNKNOWN
    evidence_excerpt: str = ""
    evidence_hash: str = UNKNOWN
    evidence_ref: str = UNKNOWN
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    regulatory_impact: str = UNKNOWN
    commercial_impact: str = UNKNOWN
    recommended_internal_action: InternalAction = "HOLD_UNKNOWN_OR_STALE"
    # Truth-firewall pins (structural constants, never derived from content).
    consent_state: Literal["NOT_PROVEN"] = "NOT_PROVEN"
    relationship_state: Literal["RESEARCH_ONLY"] = "RESEARCH_ONLY"
    counts_as_relationship: bool = False
    counts_as_consent: bool = False
    counts_as_buyer_intent: bool = False
    counts_as_pipeline: bool = False
    counts_as_revenue: bool = False
    allows_external_send: bool = False
    dedupe_key: str = UNKNOWN

    @model_validator(mode="after")
    def enforce_firewall(self) -> OfficialSourceSignal:
        # Firewall pins cannot be overridden via constructor payloads that
        # smuggle truthy values — pydantic frozen model would already hold
        # them, but double-assert for explicitness.
        if self.relationship_state != "RESEARCH_ONLY":
            raise ValueError("relationship_state must stay RESEARCH_ONLY")
        if self.consent_state != "NOT_PROVEN":
            raise ValueError("consent_state must stay NOT_PROVEN")
        for flag in (
            "counts_as_relationship",
            "counts_as_consent",
            "counts_as_buyer_intent",
            "counts_as_pipeline",
            "counts_as_revenue",
            "allows_external_send",
        ):
            if getattr(self, flag) is not False:
                raise ValueError(f"{flag} must stay False: research is not authority")
        if self.recommended_internal_action not in INTERNAL_ACTIONS:
            raise ValueError("recommended action must be internal-only")
        return self

    def freshness_state(self, *, now: datetime | None = None) -> FreshnessState:
        """Freshness from timestamps only; UNKNOWN/missing evidence -> HOLD."""
        if (
            self.source_authority == UNKNOWN
            or self.canonical_url == UNKNOWN
            or not self.evidence_excerpt
            or self.evidence_hash == UNKNOWN
        ):
            return FreshnessState.HOLD
        check = now or datetime.now(UTC)
        try:
            if self.expires_at != UNKNOWN:
                expiry = datetime.fromisoformat(self.expires_at.replace("Z", "+00:00"))
                if expiry.tzinfo is None:
                    return FreshnessState.HOLD
                if check >= expiry:
                    return FreshnessState.EXPIRED
                if check >= expiry - timedelta(days=7):
                    return FreshnessState.STALE
        except Exception:
            return FreshnessState.HOLD
        return FreshnessState.FRESH

    def is_actionable(self, *, now: datetime | None = None) -> bool:
        return (
            self.freshness_state(now=now) is FreshnessState.FRESH
            and self.confidence >= 0.5
            and self.source_authority != UNKNOWN
        )

    def to_canonical_signal_kwargs(self, *, tenant_id: str) -> dict[str, Any]:
        """Map onto dealix.company_intelligence.signal_contracts.build_signal kwargs.

        Uses current contracts only: MARKET/REGULATORY type, PUBLIC_SOURCE
        sensitivity, PUBLIC_SOURCE consent (still fail-closed for outreach —
        a signal never authorizes external action by itself).
        """
        from dealix.company_intelligence.signal_contracts import (
            ConsentStatus,
            SignalSensitivity,
            SignalType,
        )

        lowered = (self.topic or "").lower()
        signal_type = (
            SignalType.REGULATORY
            if any(k in lowered for k in ("regulation", "compliance", "license",
                                          "mandate", "enforcement", "tender",
                                          "procurement", "sandbox", "wave"))
            else SignalType.MARKET
        )
        try:
            expires = (
                datetime.fromisoformat(self.expires_at.replace("Z", "+00:00"))
                if self.expires_at != UNKNOWN
                else None
            )
        except Exception:
            expires = None
        return {
            "tenant_id": tenant_id,
            "deduplication_key": self.dedupe_key if self.dedupe_key != UNKNOWN else self.signal_id,
            "company_id": "market_watch_unlinked",
            "source_id": self.source_registry_id
            if self.source_registry_id != UNKNOWN
            else f"official_{self.source_authority.lower()}",
            "signal_type": signal_type,
            "sensitivity": SignalSensitivity.PUBLIC,
            "consent_status": ConsentStatus.PUBLIC_SOURCE,
            "claim": self.title_en if self.title_en != UNKNOWN else self.topic,
            "evidence_ref": self.evidence_ref if self.evidence_ref != UNKNOWN else self.evidence_hash,
            "confidence": self.confidence,
            "expires_at": expires,
        }

    def to_radar_signal(self) -> RegulatorySignal:
        """Admit into the existing SaudiMarketRadar shape (research-only)."""
        authority = resolve_authority(self.source_authority)
        try:
            expiry = (
                self.expires_at
                if self.expires_at != UNKNOWN
                else (datetime.now(UTC) + timedelta(days=90)).isoformat()
            )
        except Exception:
            expiry = (datetime.now(UTC) + timedelta(days=90)).isoformat()
        return RegulatorySignal(
            signal_id=self.signal_id,
            source=authority or SignalSource.SAUDI_OPEN_DATA,
            source_url=self.canonical_url,
            source_date=self.published_at,
            retrieved_at=self.observed_at,
            effective_date=self.effective_at,
            expiry_review_at=expiry,
            refresh_policy="official_source_watch_and_before_customer_use",
            title_ar=self.title_ar,
            title_en=self.title_en,
            scope=self.regulatory_impact,
            affected_sectors=[self.sector],
            buyer_type=UNKNOWN,
            problem=self.topic,
            trigger=self.recommended_internal_action,
            confidence=self.confidence,
            commercial_implication=f"INTERNAL ONLY: {self.commercial_impact}",
            compliance_implication="Research only; not advice; verify live official page before customer-specific use.",
            diagnostic_match=[],
            offer_match=[],
            evidence_strength=3 if self.confidence >= 0.7 else 2,
        )

    def economic_governor_hint(self) -> dict[str, Any]:
        """Evidence-weighted hint for the Economic Governor.

        Never creates an opportunity; repeated watches with the same dedupe
        key must not manufacture new demand.
        """
        return {
            "signal_id": self.signal_id,
            "dedupe_key": self.dedupe_key,
            "evidence_class": "public_source",
            "evidence_weight": 0.25,
            "creates_opportunity": False,
            "requires_fresh_evidence_before_scoring": True,
            "freshness": self.freshness_state().value,
            "actionable": self.is_actionable(),
            "internal_action": self.recommended_internal_action,
        }


def build_official_signal(
    *,
    source_authority: str,
    canonical_url: str,
    canonical_ref: str,
    sector: str,
    topic: str,
    title_en: str = UNKNOWN,
    title_ar: str = UNKNOWN,
    published_at: str = UNKNOWN,
    effective_at: str = UNKNOWN,
    expires_at: str = UNKNOWN,
    observed_at: str | None = None,
    evidence_excerpt: str = "",
    evidence_ref: str = UNKNOWN,
    source_registry_id: str = UNKNOWN,
    confidence: float = 0.5,
    regulatory_impact: str = UNKNOWN,
    commercial_impact: str = UNKNOWN,
    now: datetime | None = None,
) -> OfficialSourceSignal:
    """Bounded builder: UNKNOWN/HOLD when source metadata is absent, never invented."""
    authority = (source_authority or "").strip().upper()
    known = resolve_authority(authority) is not None
    url = (canonical_url or "").strip() or UNKNOWN
    ref = (canonical_ref or "").strip() or UNKNOWN
    if not known:
        authority = UNKNOWN
    if source_registry_id != UNKNOWN and source_registry_id not in OFFICIAL_REGISTRY_IDS:
        registry_id = UNKNOWN
    else:
        registry_id = source_registry_id
    excerpt = evidence_excerpt or ""
    evidence_hash = compute_evidence_hash(url, excerpt) if (known and url != UNKNOWN and excerpt) else UNKNOWN
    dedupe_key = compute_dedupe_key(authority, ref, topic or UNKNOWN, sector or UNKNOWN)
    signal_id = f"ows_{dedupe_key}"
    check_now = now or datetime.now(UTC)
    # Provisional freshness for action recommendation.
    provisional = FreshnessState.HOLD
    if known and url != UNKNOWN and excerpt and evidence_hash != UNKNOWN:
        provisional = FreshnessState.FRESH
        if expires_at != UNKNOWN:
            try:
                expiry = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
                if check_now >= expiry:
                    provisional = FreshnessState.EXPIRED
                elif check_now >= expiry - timedelta(days=7):
                    provisional = FreshnessState.STALE
            except Exception:
                provisional = FreshnessState.HOLD
    action = recommend_internal_action(
        topic=topic or UNKNOWN,
        freshness=provisional,
        confidence=confidence,
        source_known=known,
    )
    # Unknown-source signals hold at floor confidence: stale/unknown != fact.
    if not known:
        confidence = min(confidence, 0.3)
    return OfficialSourceSignal(
        signal_id=signal_id,
        source_authority=authority,
        source_registry_id=registry_id,
        canonical_url=url,
        canonical_ref=ref,
        sector=(sector or UNKNOWN).strip() or UNKNOWN,
        topic=(topic or UNKNOWN).strip() or UNKNOWN,
        title_en=title_en,
        title_ar=title_ar,
        published_at=published_at,
        effective_at=effective_at,
        observed_at=observed_at or check_now.isoformat(),
        expires_at=expires_at,
        evidence_excerpt=excerpt,
        evidence_hash=evidence_hash,
        evidence_ref=evidence_ref,
        confidence=confidence,
        regulatory_impact=regulatory_impact,
        commercial_impact=commercial_impact,
        recommended_internal_action=action,
        dedupe_key=dedupe_key,
    )


class OfficialSourceWatchRegistry:
    """In-memory dedupe registry; callers persist elsewhere (no second store)."""

    def __init__(self) -> None:
        self._by_dedupe: dict[str, OfficialSourceSignal] = {}

    def ingest(self, signal: OfficialSourceSignal) -> tuple[OfficialSourceSignal, bool]:
        """Ingest with dedupe: repeats return existing with created=False."""
        existing = self._by_dedupe.get(signal.dedupe_key)
        if existing is not None:
            return existing, False
        self._by_dedupe[signal.dedupe_key] = signal
        return signal, True

    def get(self, dedupe_key: str) -> OfficialSourceSignal | None:
        return self._by_dedupe.get(dedupe_key)

    def list_fresh(self, *, now: datetime | None = None) -> list[OfficialSourceSignal]:
        return [s for s in self._by_dedupe.values() if s.freshness_state(now=now) is FreshnessState.FRESH]

    def list_hold(self, *, now: datetime | None = None) -> list[OfficialSourceSignal]:
        return [
            s
            for s in self._by_dedupe.values()
            if s.freshness_state(now=now) in (FreshnessState.HOLD, FreshnessState.EXPIRED, FreshnessState.STALE)
        ]

    def to_dict(self, *, now: datetime | None = None) -> dict[str, Any]:
        return {
            "signals": [s.model_dump(mode="json") for s in self._by_dedupe.values()],
            "fresh_count": len(self.list_fresh(now=now)),
            "research_counts_as_relationship": False,
            "research_counts_as_consent": False,
            "research_counts_as_buyer_intent": False,
            "research_counts_as_pipeline": False,
            "research_counts_as_revenue": False,
        }


# ─── Bounded adapter interfaces (disabled by default, no live I/O) ───────────


class WatchAdapterReceipt(BaseModel):
    """Config-only receipt mirroring web_research_adapter authority pattern."""

    model_config = ConfigDict(extra="forbid")

    adapter: str
    enabled: bool = False
    status: str = "BLOCKED_DISABLED_BY_DEFAULT"
    observed_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    source_refs: list[str] = Field(default_factory=list)
    authority: dict[str, bool] = Field(
        default_factory=lambda: {
            "relationship": False,
            "consent": False,
            "opportunity": False,
            "offer": False,
            "external_send": False,
            "payment": False,
            "production": False,
        }
    )
    next_evidence: list[str] = Field(
        default_factory=lambda: ["ENABLE_EXPLICITLY_AND_VERIFY_SOURCE_TERMS_BEFORE_ANY_FETCH"]
    )


class ChangedetectionWatchAdapter:
    """changedetection.io watch config holder. No HTTP, no deployment."""

    ADAPTER = "CHANGEDETECTION_WATCH"

    def __init__(self, *, enabled: bool = False, watch_urls: list[str] | None = None) -> None:
        self._enabled = bool(enabled)
        self._watch_urls = list(watch_urls or [])

    @property
    def access_state(self) -> str:
        return "READ_ONLY_READY" if self._enabled and self._watch_urls else "BLOCKED_DISABLED_BY_DEFAULT"

    def plan(self, *, request_id: str) -> WatchAdapterReceipt:  # noqa: ARG002
        return WatchAdapterReceipt(
            adapter=self.ADAPTER,
            enabled=self._enabled,
            status=self.access_state,
            source_refs=list(self._watch_urls) if self._enabled else [],
        )

    def fetch(self, *, request_id: str) -> WatchAdapterReceipt:  # noqa: ARG002
        """Always blocked in this task: no live crawling or service deployment."""
        return WatchAdapterReceipt(adapter=self.ADAPTER, enabled=False)


class CrawlAIExtractAdapter:
    """Crawl4AI extraction config holder. No crawl, no browser launch."""

    ADAPTER = "CRAWL4AI_EXTRACT"

    def __init__(self, *, enabled: bool = False, allowlist: list[str] | None = None) -> None:
        self._enabled = bool(enabled)
        self._allowlist = list(allowlist or [])

    @property
    def access_state(self) -> str:
        return "READ_ONLY_READY" if self._enabled and self._allowlist else "BLOCKED_DISABLED_BY_DEFAULT"

    def plan(self, *, request_id: str) -> WatchAdapterReceipt:  # noqa: ARG002
        return WatchAdapterReceipt(
            adapter=self.ADAPTER,
            enabled=self._enabled,
            status=self.access_state,
            source_refs=list(self._allowlist) if self._enabled else [],
        )

    def fetch(self, *, request_id: str) -> WatchAdapterReceipt:  # noqa: ARG002
        """Always blocked in this task: no live crawling or service deployment."""
        return WatchAdapterReceipt(adapter=self.ADAPTER, enabled=False)


__all__ = [
    "OFFICIAL_AUTHORITIES",
    "OFFICIAL_REGISTRY_IDS",
    "INTERNAL_ACTIONS",
    "FreshnessState",
    "OfficialSourceSignal",
    "OfficialSourceWatchRegistry",
    "ChangedetectionWatchAdapter",
    "CrawlAIExtractAdapter",
    "WatchAdapterReceipt",
    "build_official_signal",
    "compute_dedupe_key",
    "compute_evidence_hash",
    "recommend_internal_action",
    "resolve_authority",
]
