"""Experiment Engine — proposes the next safe weekly experiment."""
from __future__ import annotations


def next_experiment(
    *,
    last_week_summary: dict | None = None,
    sector_focus: str = "marketing_agency",
) -> dict:
    """Suggest one experiment for the coming week. ``last_week_summary``
    is optional — when None, the system proposes a baseline experiment.
    """
    if last_week_summary is None:
        return {
            "hypothesis": (
                f"Sector {sector_focus} responds to Proof Pack-led messaging "
                "in 7 days within +30% above the previous warm-intro baseline."
            ),
            "segment": sector_focus,
            "offer": "7-Day Growth Proof Sprint @ 499 SAR",
            "channel": "founder_warm_intro",
            "safe_action": "send 5 manual warm intros",
            "success_metric": "≥ 2 replies + ≥ 1 mini diagnostic accepted",
            "expected_learning": (
                "validate sector + offer fit OR pivot to next sector"
            ),
            "stop_condition": "0 replies after 7 days",
            "action_mode": "suggest_only",
        }
    replies = last_week_summary.get("replies", 0)
    intros_sent = last_week_summary.get("intros_sent", 0)
    if intros_sent == 0:
        return {
            "hypothesis": "First execute baseline before proposing variants",
            "segment": sector_focus,
            "offer": "7-Day Growth Proof Sprint @ 499 SAR",
            "channel": "founder_warm_intro",
            "safe_action": "send 5 manual warm intros",
            "success_metric": "≥ 2 replies",
            "expected_learning": "baseline reply rate",
            "stop_condition": "skip",
            "action_mode": "suggest_only",
        }
    reply_rate = replies / intros_sent if intros_sent else 0
    if reply_rate < 0.2:
        return {
            "hypothesis": (
                f"Reply rate {reply_rate:.0%} too low — try different sector "
                "OR different message angle next week"
            ),
            "segment": "rotate_sector_or_message",
            "offer": "7-Day Growth Proof Sprint @ 499 SAR",
            "channel": "founder_warm_intro",
            "safe_action": "rotate to next priority sector (Tier 1B if 1A failed)",
            "success_metric": "≥ 2 replies in new sector",
            "expected_learning": "is the issue sector or message?",
            "stop_condition": "0 replies after rotation",
            "action_mode": "suggest_only",
        }
    return {
        "hypothesis": (
            f"Reply rate {reply_rate:.0%} healthy — scale current sector "
            "with 5 more warm intros AND test a 2nd message angle"
        ),
        "segment": sector_focus,
        "offer": "7-Day Growth Proof Sprint @ 499 SAR",
        "channel": "founder_warm_intro",
        "safe_action": "send 5 more warm intros + 1 message angle variant",
        "success_metric": "maintain or improve reply_rate",
        "expected_learning": "which message angle wins",
        "stop_condition": "reply rate drops > 50%",
        "action_mode": "suggest_only",
    }
