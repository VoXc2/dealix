#!/usr/bin/env python3
"""Fail-closed verifier for exact, human-issued Dealix merge authority.

The verifier never creates authority. It validates a snapshot produced by the
GitHub workflow and accepts only a fresh, exact action-bound founder comment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MARKER = "DEALIX_L5_MERGE_AUTHORITY"
HOLD_MARKERS = (
    "MERGE_RECOMMENDATION=HOLD",
    "MERGE_RECOMMENDATION: HOLD",
    "PRODUCTION_GREEN=false",
    "PRODUCTION_GREEN: false",
)
MAX_AUTHORITY_HOURS = 24


class GateError(RuntimeError):
    pass


@dataclass(frozen=True)
class Authority:
    actor: str
    pr: int
    head_sha: str
    base_sha: str
    expires_at: datetime
    authority_source: str
    rollback_ref: str
    idempotency_key: str
    action_hash: str


def _parse_time(value: str) -> datetime:
    raw = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise GateError(f"invalid expires_at: {value!r}") from exc
    if parsed.tzinfo is None:
        raise GateError("expires_at must include a timezone")
    return parsed.astimezone(timezone.utc)


def _parse_comment(actor: str, body: str) -> Authority | None:
    lines = [line.strip() for line in body.splitlines()]
    if MARKER not in lines:
        return None
    marker_index = lines.index(MARKER)
    fields: dict[str, str] = {}
    for line in lines[marker_index + 1 :]:
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip().lower()] = value.strip()

    required = {
        "decision",
        "pr",
        "head_sha",
        "base_sha",
        "expires_at",
        "authority_source",
        "rollback_ref",
        "idempotency_key",
        "action_hash",
    }
    missing = sorted(required - fields.keys())
    if missing:
        raise GateError("authority comment missing: " + ", ".join(missing))
    if fields["decision"].upper() != "GRANT":
        raise GateError("authority decision is not GRANT")
    try:
        pr = int(fields["pr"])
    except ValueError as exc:
        raise GateError("authority pr must be an integer") from exc

    return Authority(
        actor=actor,
        pr=pr,
        head_sha=fields["head_sha"],
        base_sha=fields["base_sha"],
        expires_at=_parse_time(fields["expires_at"]),
        authority_source=fields["authority_source"],
        rollback_ref=fields["rollback_ref"],
        idempotency_key=fields["idempotency_key"],
        action_hash=fields["action_hash"],
    )


def expected_action_hash(
    repo: str,
    pr: int,
    head_sha: str,
    base_sha: str,
    rollback_ref: str,
    idempotency_key: str,
) -> str:
    payload = "|".join(
        ("merge", repo, str(pr), head_sha, base_sha, rollback_ref, idempotency_key)
    )
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def verify_snapshot(snapshot: dict[str, Any], authority_actors: set[str]) -> Authority:
    repo = str(snapshot.get("repo", "")).strip()
    pr = int(snapshot.get("number", 0))
    head_sha = str(snapshot.get("head_sha", "")).strip()
    base_sha = str(snapshot.get("base_sha", "")).strip()
    body = str(snapshot.get("body", "") or "")
    draft = bool(snapshot.get("draft", True))
    state = str(snapshot.get("state", "")).strip().lower()
    now = _parse_time(str(snapshot.get("now", "")))

    if not repo or pr <= 0 or not head_sha or not base_sha:
        raise GateError("snapshot missing repo/pr/head/base identity")
    if state != "open":
        raise GateError(f"PR must be open, got {state or 'unknown'}")
    if draft:
        raise GateError("PR is draft")
    for marker in HOLD_MARKERS:
        if marker.casefold() in body.casefold():
            raise GateError(f"PR body still declares hold: {marker}")
    if not authority_actors:
        raise GateError("no merge-authority actors configured")

    valid: list[tuple[datetime, Authority]] = []
    parse_errors: list[str] = []
    for comment in snapshot.get("comments", []):
        actor = str(((comment or {}).get("user") or {}).get("login", "")).strip()
        text = str((comment or {}).get("body", "") or "")
        if MARKER not in text or actor not in authority_actors:
            continue
        try:
            authority = _parse_comment(actor, text)
            if authority is None:
                continue
            created = _parse_time(str((comment or {}).get("created_at", "")))
            valid.append((created, authority))
        except GateError as exc:
            parse_errors.append(f"{actor}: {exc}")

    if not valid:
        detail = "; ".join(parse_errors[-3:]) if parse_errors else "none found"
        raise GateError(f"no valid allowlisted authority comment: {detail}")

    created_at, authority = max(valid, key=lambda item: item[0])
    if authority.pr != pr:
        raise GateError("authority PR number does not match current PR")
    if authority.head_sha != head_sha:
        raise GateError("authority head SHA is stale")
    if authority.base_sha != base_sha:
        raise GateError("authority base SHA is stale")
    if authority.rollback_ref != base_sha:
        raise GateError("rollback_ref must equal the exact pre-merge base SHA")
    expected_source = f"github_comment:{authority.actor}"
    if authority.authority_source != expected_source:
        raise GateError(f"authority_source must be {expected_source}")
    expected_idempotency = f"merge:{repo}#{pr}:{head_sha}"
    if authority.idempotency_key != expected_idempotency:
        raise GateError("idempotency_key is not exact for repo/PR/head")
    expected_hash = expected_action_hash(
        repo,
        pr,
        head_sha,
        base_sha,
        authority.rollback_ref,
        authority.idempotency_key,
    )
    if authority.action_hash != expected_hash:
        raise GateError("action_hash mismatch")
    if authority.expires_at <= now:
        raise GateError("merge authority is expired")
    if authority.expires_at <= created_at:
        raise GateError("merge authority expires_at must be after comment creation")
    lifetime_hours = (authority.expires_at - created_at).total_seconds() / 3600
    if lifetime_hours > MAX_AUTHORITY_HOURS:
        raise GateError("merge authority lifetime exceeds 24-hour bound")
    return authority


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument(
        "--authority-actors",
        default=os.getenv("DEALIX_MERGE_AUTHORITY_ACTORS", ""),
        help="comma-separated GitHub logins allowed to issue merge authority",
    )
    args = parser.parse_args()
    actors = {item.strip() for item in args.authority_actors.split(",") if item.strip()}
    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    try:
        authority = verify_snapshot(snapshot, actors)
    except (GateError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"MERGE_AUTHORITY_GATE=BLOCKED reason={exc}")
        return 2
    print("MERGE_AUTHORITY_GATE=PASS")
    print(f"AUTHORITY_ACTOR={authority.actor}")
    print(f"AUTHORITY_HEAD={authority.head_sha}")
    print(f"AUTHORITY_BASE={authority.base_sha}")
    print(f"AUTHORITY_EXPIRES_AT={authority.expires_at.isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
