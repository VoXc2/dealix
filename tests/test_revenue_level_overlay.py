"""Revenue Pipeline — L2-L7 evidence-level overlay tests.

Verifies the overlay is a faithful, complete labeling of the existing
``stage_policy`` machine and never contradicts its revenue truth.
"""

from __future__ import annotations

from typing import get_args

from auto_client_acquisition.revenue_pipeline.level_overlay import (
    LEVEL_FOR_STAGE,
    LEVEL_RANK,
    STAGE_EVENT_LABEL,
    event_label_for_stage,
    is_l7_candidate,
    is_l7_confirmed,
    level_for_stage,
    level_rank,
)
from auto_client_acquisition.revenue_pipeline.stage_policy import (
    PipelineStage,
    counts_as_commitment,
    counts_as_revenue,
)

# Canonical stage order, straight from the stage_policy Literal.
_ALL_STAGES: tuple[str, ...] = get_args(PipelineStage)
# Forward path excludes the off-path terminal stage.
_FORWARD_PATH: tuple[str, ...] = tuple(s for s in _ALL_STAGES if s != "closed_lost")


def test_every_stage_has_a_level_and_event_label():
    assert set(LEVEL_FOR_STAGE) == set(_ALL_STAGES)
    assert set(STAGE_EVENT_LABEL) == set(_ALL_STAGES)
    for stage in _ALL_STAGES:
        assert level_for_stage(stage) in LEVEL_RANK
        assert event_label_for_stage(stage).strip()


def test_l7_confirmed_iff_counts_as_revenue():
    """No revenue may be claimed before the policy says money landed."""
    for stage in _ALL_STAGES:
        is_confirmed = level_for_stage(stage) == "L7_confirmed"
        assert is_confirmed == counts_as_revenue(stage), (
            f"{stage}: L7_confirmed/{is_confirmed} != "
            f"counts_as_revenue/{counts_as_revenue(stage)}"
        )
        assert is_l7_confirmed(stage) == counts_as_revenue(stage)


def test_l7_candidate_is_commitment_without_revenue():
    for stage in _ALL_STAGES:
        expected = counts_as_commitment(stage) and not counts_as_revenue(stage)
        assert is_l7_candidate(stage) == expected
        if is_l7_candidate(stage):
            assert level_for_stage(stage) == "L7_candidate"


def test_level_is_monotonic_along_forward_path():
    """Evidence level never decreases as a deal advances forward."""
    ranks = [level_rank(level_for_stage(s)) for s in _FORWARD_PATH]
    assert ranks == sorted(ranks), (
        f"level not monotonic: {list(zip(_FORWARD_PATH, ranks, strict=True))}"
    )


def test_l5_not_reached_before_diagnostic_delivered():
    """L5 (used_in_meeting) is unreachable before diagnostic_delivered."""
    before = _FORWARD_PATH[: _FORWARD_PATH.index("diagnostic_delivered")]
    for stage in before:
        assert level_rank(level_for_stage(stage)) < level_rank("L5"), (
            f"{stage} reaches L5+ before diagnostic_delivered"
        )
    assert level_for_stage("diagnostic_delivered") == "L5"


def test_prepared_not_sent_is_l2():
    assert level_for_stage("message_drafted") == "L2"
    assert event_label_for_stage("message_drafted") == "prepared_not_sent"


def test_invoice_paid_is_l7_confirmed():
    assert level_for_stage("payment_received") == "L7_confirmed"
    assert event_label_for_stage("payment_received") == "invoice_paid"
