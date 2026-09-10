from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from scripts.ops.verify_merge_authority_gate import (
    GateError,
    expected_action_hash,
    verify_snapshot,
)

REPO = "Dealix-sa/dealix"
PR = 42
HEAD = "a" * 40
BASE = "b" * 40
ACTOR = "VoXc2"
NOW = datetime(2026, 9, 10, 12, 0, tzinfo=timezone.utc)


def snapshot(
    *,
    draft: bool = False,
    body: str = "MERGE_RECOMMENDATION=READY",
    head: str = HEAD,
    base: str = BASE,
    expires_hours: int = 2,
) -> dict:
    idempotency = f"merge:{REPO}#{PR}:{head}"
    action_hash = expected_action_hash(REPO, PR, head, base, base, idempotency)
    expires = NOW + timedelta(hours=expires_hours)
    comment = "\n".join(
        [
            "DEALIX_L5_MERGE_AUTHORITY",
            "decision: GRANT",
            f"pr: {PR}",
            f"head_sha: {head}",
            f"base_sha: {base}",
            f"expires_at: {expires.isoformat()}",
            f"authority_source: github_comment:{ACTOR}",
            f"rollback_ref: {base}",
            f"idempotency_key: {idempotency}",
            f"action_hash: {action_hash}",
        ]
    )
    return {
        "repo": REPO,
        "number": PR,
        "head_sha": head,
        "base_sha": base,
        "draft": draft,
        "state": "open",
        "body": body,
        "now": NOW.isoformat(),
        "comments": [
            {
                "user": {"login": ACTOR},
                "body": comment,
                "created_at": NOW.isoformat(),
            }
        ],
    }


def test_exact_authority_passes() -> None:
    authority = verify_snapshot(snapshot(), {ACTOR})
    assert authority.head_sha == HEAD


def test_draft_is_blocked_even_with_authority() -> None:
    with pytest.raises(GateError, match="draft"):
        verify_snapshot(snapshot(draft=True), {ACTOR})


def test_explicit_hold_is_blocked_even_with_authority() -> None:
    with pytest.raises(GateError, match="declares hold"):
        verify_snapshot(snapshot(body="MERGE_RECOMMENDATION=HOLD"), {ACTOR})


def test_stale_head_invalidates_prior_authority() -> None:
    current = snapshot()
    current["head_sha"] = "c" * 40
    with pytest.raises(GateError, match="head SHA is stale"):
        verify_snapshot(current, {ACTOR})


def test_unallowlisted_comment_does_not_grant_authority() -> None:
    with pytest.raises(GateError, match="no valid allowlisted"):
        verify_snapshot(snapshot(), {"another-user"})


def test_expired_authority_is_blocked() -> None:
    with pytest.raises(GateError, match="expired"):
        verify_snapshot(snapshot(expires_hours=-1), {ACTOR})


def test_authority_more_than_24_hours_is_blocked() -> None:
    with pytest.raises(GateError, match="24-hour"):
        verify_snapshot(snapshot(expires_hours=25), {ACTOR})


def test_tampered_action_hash_is_blocked() -> None:
    current = snapshot()
    current["comments"][0]["body"] = current["comments"][0]["body"].replace(
        "sha256:", "sha256:deadbeef"
    )
    with pytest.raises(GateError, match="action_hash mismatch"):
        verify_snapshot(current, {ACTOR})


def test_long_authority_cannot_age_into_valid_window() -> None:
    current = snapshot(expires_hours=48)
    current["now"] = (NOW + timedelta(hours=30)).isoformat()
    with pytest.raises(GateError, match="24-hour"):
        verify_snapshot(current, {ACTOR})
