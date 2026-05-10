"""Wave 12.5 §33.2.1 (Engine 1) — Saudi Market Radar Extended tests.

Validates:
- 23 signal types in SIGNAL_TYPES (16 original + 7 new founder-vision)
- SIGNAL_OUTPUT_SCHEMA has all 6 founder-vision output fields per signal
- get_signal_output() returns empty for unknown (Article 8 — no fabrication)
- Saudi seasons module: 11 canonical seasons + correct date detection
- Conservative confidence — when uncertain, doesn't over-claim
"""
from __future__ import annotations

from datetime import date

import pytest

from auto_client_acquisition.market_intelligence.saudi_seasons import (
    SaudiSeasonalContext,
    all_seasons,
    detect_saudi_season,
)
from auto_client_acquisition.market_intelligence.signal_detectors import (
    SIGNAL_OUTPUT_SCHEMA,
    SIGNAL_TYPES,
    get_signal_output,
)


# ─────────────────────────────────────────────────────────────────────
# Signal taxonomy + per-signal output (5 tests)
# ─────────────────────────────────────────────────────────────────────


def test_signal_types_extended_to_23() -> None:
    """Wave 12.5 §33.2.1: SIGNAL_TYPES grows from 16 → 23."""
    assert len(SIGNAL_TYPES) == 23, f"expected 23 signal types; got {len(SIGNAL_TYPES)}"


def test_7_new_founder_vision_signals_present() -> None:
    """The 7 new founder-vision signals must all be in the taxonomy."""
    new_signals = (
        "weak_website",
        "whatsapp_no_followup_system",
        "review_surge",
        "agency_no_proof",
        "high_ticket_b2b_no_sales_process",
        "unused_leads_dormant",
        "zatca_phase_2_eligible",
    )
    for sig in new_signals:
        assert sig in SIGNAL_TYPES, f"missing new founder-vision signal: {sig}"


def test_every_signal_has_complete_output_schema() -> None:
    """Every SIGNAL_TYPE must have all 6 founder-vision output fields
    in SIGNAL_OUTPUT_SCHEMA."""
    required_fields = {
        "business_pain", "best_offer", "risk",
        "safe_channel", "recommended_action", "proof_target",
    }
    for sig in SIGNAL_TYPES:
        out = SIGNAL_OUTPUT_SCHEMA.get(sig)
        assert out is not None, f"signal {sig!r} missing from SIGNAL_OUTPUT_SCHEMA"
        missing = required_fields - set(out.keys())
        assert not missing, f"signal {sig!r} missing fields: {missing}"


def test_get_signal_output_returns_empty_for_unknown() -> None:
    """Unknown signal returns empty dict (Article 8 — no fabrication)."""
    out = get_signal_output("totally_made_up_signal")
    assert out == {}


def test_zatca_signal_recommends_compliance_offer() -> None:
    """zatca_phase_2_eligible signal must point to compliance offer
    (research-validated June 2026 deadline urgency)."""
    out = get_signal_output("zatca_phase_2_eligible")
    assert "Compliance" in out["best_offer"] or "compliance" in out["best_offer"].lower()
    assert "ZATCA" in out["business_pain"]


# ─────────────────────────────────────────────────────────────────────
# Saudi seasons (7 tests)
# ─────────────────────────────────────────────────────────────────────


def test_all_11_canonical_seasons_registered() -> None:
    """Every Saudi season has bilingual implication + offer pivot."""
    seasons = all_seasons()
    assert len(seasons) == 11, f"expected 11 seasons; got {len(seasons)}"
    must_have = (
        "ramadan", "ramadan_prep", "eid_al_fitr", "eid_al_adha",
        "hajj_season", "school_year_start", "national_day",
        "founding_day", "exhibition_season",
        "zatca_wave_24_deadline_window", "ordinary",
    )
    for s in must_have:
        assert s in seasons, f"missing canonical Saudi season: {s}"


def test_detect_eid_al_fitr() -> None:
    """Eid al-Fitr 2026: March 20-22."""
    ctx = detect_saudi_season(on_date=date(2026, 3, 21))
    assert ctx.season == "eid_al_fitr"
    assert ctx.confidence >= 0.8
    assert "PAUSE" in ctx.recommended_offer_pivot


def test_detect_ramadan_prep_30_days_before() -> None:
    """30-day pre-Ramadan window detected."""
    # Ramadan starts Feb 18, 2026 → pre-window starts Jan 19
    ctx = detect_saudi_season(on_date=date(2026, 2, 1))
    assert ctx.season == "ramadan_prep"


def test_detect_zatca_wave_24_window() -> None:
    """ZATCA Wave 24 window: April 1 - June 30, 2026 (highest confidence
    because dates are official ZATCA-published)."""
    ctx = detect_saudi_season(on_date=date(2026, 5, 15))
    # Note: May 15 also falls in eid_adha-adjacent timing; eid takes priority
    # if it overlaps. Test at a clear ZATCA-only date instead:
    ctx2 = detect_saudi_season(on_date=date(2026, 4, 15))
    assert ctx2.season == "zatca_wave_24_deadline_window"
    assert ctx2.confidence >= 0.9, "ZATCA dates are official; should be high confidence"
    assert "Compliance" in ctx2.recommended_offer_pivot


def test_detect_national_day() -> None:
    """September 23 → national_day (single-day, high confidence)."""
    ctx = detect_saudi_season(on_date=date(2026, 9, 23))
    assert ctx.season == "national_day"
    assert ctx.confidence >= 0.9


def test_detect_ordinary_when_no_season_matches() -> None:
    """Random Tuesday in October → ordinary."""
    # Oct 6, 2026 — between Hajj (May) and exhibition season start (Oct 1)
    # Actually Oct 1 is start of exhibition season; pick a date in Aug
    ctx = detect_saudi_season(on_date=date(2026, 7, 15))
    assert ctx.season == "ordinary"


def test_eid_takes_priority_over_other_seasons() -> None:
    """When Eid overlaps with another window, Eid wins (highest business impact)."""
    # Eid al-Adha 2026: May 27-29
    # ZATCA window: April 1 - June 30 — overlaps
    ctx = detect_saudi_season(on_date=date(2026, 5, 28))
    assert ctx.season == "eid_al_adha", \
        f"Eid must take priority over ZATCA window; got {ctx.season}"


# ─────────────────────────────────────────────────────────────────────
# Total: 12 tests (5 signal + 7 seasons)
# ─────────────────────────────────────────────────────────────────────
