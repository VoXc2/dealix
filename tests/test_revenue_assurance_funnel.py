"""Funnel Scoreboard — ordering, targets, and bottleneck detection."""

from __future__ import annotations

from auto_client_acquisition.revenue_assurance_os.funnel_scoreboard import (
    FUNNEL_ORDER,
    build_scoreboard,
    worst_bottleneck,
)


def test_funnel_has_ten_ordered_stages() -> None:
    assert len(FUNNEL_ORDER) == 10
    assert FUNNEL_ORDER[0].value == "target_accounts"
    assert FUNNEL_ORDER[-1].value == "referrals"


def test_bottleneck_is_weakest_transition() -> None:
    counts = {
        "target_accounts": 100,
        "conversations": 90,  # 90% — healthy
        "proof_pack_requests": 5,  # 5.5% — weak
        "meetings": 4,
        "scopes": 3,
        "invoices": 2,
        "paid": 2,
        "proof_packs_delivered": 2,
        "upsells": 1,
        "referrals": 1,
    }
    assert worst_bottleneck(counts) == "proof_pack_requests"


def test_scoreboard_gaps_against_30d_targets() -> None:
    board = build_scoreboard({"target_accounts": 40}, period="30d")
    assert board.gaps["target_accounts"] == 60  # target 100 - 40
    assert board.on_track is False


def test_empty_counts_do_not_crash() -> None:
    board = build_scoreboard({})
    assert board.counts["paid"] == 0
    assert board.bottleneck_stage in {s.value for s in FUNNEL_ORDER}
