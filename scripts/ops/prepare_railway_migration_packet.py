#!/usr/bin/env python3
"""Prepare a deterministic, non-executing Railway Production DB migration packet."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from alembic.config import Config
from alembic.script import ScriptDirectory

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial.external_execution_gate import canonical_action_hash

SCHEMA = "dealix.railway-migration-packet.v1"
ACTION_TYPE = "PRODUCTION_DB_MIGRATION"
MAX_TTL_MINUTES = 60
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def _canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _validate_sha(value: str, *, field: str) -> str:
    text = value.strip().lower()
    if not SHA40.fullmatch(text):
        raise ValueError(f"{field} must be an exact 40-character lowercase Git SHA")
    return text


def _validate_ref(value: str, *, field: str) -> str:
    text = value.strip()
    upper = text.upper()
    lower = text.lower()
    placeholders = ("synthetic:", "synthetic://", "demo:", "demo://", "fake:", "fake://", "example:", "example://")
    if not text or upper.startswith("UNKNOWN") or upper in {"TBD", "TODO"} or lower.startswith(placeholders):
        raise ValueError(f"{field} must reference concrete non-synthetic evidence")
    return text


def _parse_aware(value: str, *, field: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include timezone")
    return parsed.astimezone(UTC)


def _git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def _repo_context(repo: Path) -> tuple[str, bool]:
    head = _validate_sha(_git(repo, "rev-parse", "HEAD"), field="builder_source_sha")
    dirty = bool(_git(repo, "status", "--porcelain"))
    return head, dirty


def _alembic_heads(repo: Path) -> list[str]:
    config = Config(str(repo / "alembic.ini"))
    config.set_main_option("script_location", str(repo / "db" / "migrations"))
    heads = sorted(ScriptDirectory.from_config(config).get_heads())
    if len(heads) != 1:
        raise ValueError(f"exactly one Alembic head is required, found {len(heads)}")
    return heads


def build_packet(
    *,
    project_id: str,
    environment_id: str,
    service_id: str,
    release_sha: str,
    builder_source_sha: str,
    alembic_heads: list[str],
    backup_ref: str,
    rollback_ref: str,
    created_at: datetime,
    ttl_minutes: int,
) -> dict[str, Any]:
    if len(alembic_heads) != 1 or not alembic_heads[0].strip():
        raise ValueError("exactly one concrete Alembic head is required")
    if ttl_minutes < 1 or ttl_minutes > MAX_TTL_MINUTES:
        raise ValueError(f"ttl_minutes must be between 1 and {MAX_TTL_MINUTES}")
    release_sha = _validate_sha(release_sha, field="release_sha")
    builder_source_sha = _validate_sha(builder_source_sha, field="builder_source_sha")
    project_id = _validate_ref(project_id, field="project_id")
    environment_id = _validate_ref(environment_id, field="environment_id")
    service_id = _validate_ref(service_id, field="service_id")
    backup_ref = _validate_ref(backup_ref, field="backup_ref")
    rollback_ref = _validate_ref(rollback_ref, field="rollback_ref")
    if created_at.tzinfo is None:
        raise ValueError("created_at must include timezone")
    created = created_at.astimezone(UTC)
    expires = created + timedelta(minutes=ttl_minutes)
    revision = alembic_heads[0].strip()
    target = f"railway:{project_id}:{environment_id}:{service_id}"
    idempotency_key = f"railway-db-migration:{environment_id}:{service_id}:{release_sha}:{revision}"
    payload_material = {
        "release_sha": release_sha,
        "builder_source_sha": builder_source_sha,
        "revision": revision,
        "operation": f"alembic upgrade {revision}",
        "project_id": project_id,
        "environment_id": environment_id,
        "service_id": service_id,
        "backup_ref": backup_ref,
        "rollback_ref": rollback_ref,
        "expires_at": expires.isoformat().replace("+00:00", "Z"),
        "idempotency_key": idempotency_key,
    }
    payload = _canonical_json(payload_material)
    action_hash = canonical_action_hash(
        action_type=ACTION_TYPE,
        target=target,
        environment="production",
        payload=payload,
    )
    return {
        "schema_version": SCHEMA,
        "packet_state": "PENDING_EXACT_L5_AUTHORITY",
        "execution_allowed": False,
        "action_type": ACTION_TYPE,
        "provider": "railway",
        "target": target,
        "environment": "production",
        "release_sha": release_sha,
        "builder_source_sha": builder_source_sha,
        "alembic_heads": [revision],
        "operation": f"alembic upgrade {revision}",
        "backup_ref": backup_ref,
        "rollback_ref": rollback_ref,
        "created_at": created.isoformat().replace("+00:00", "Z"),
        "expires_at": expires.isoformat().replace("+00:00", "Z"),
        "idempotency_key": idempotency_key,
        "payload_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "action_hash": action_hash,
        "approval_required": True,
        "authority_source_required": True,
        "automatic_predeploy_authority": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--environment-id", required=True)
    parser.add_argument("--service-id", required=True)
    parser.add_argument("--release-sha")
    parser.add_argument("--backup-ref", required=True)
    parser.add_argument("--rollback-ref", required=True)
    parser.add_argument("--ttl-minutes", type=int, default=15)
    parser.add_argument("--repo", default=str(REPO_ROOT))
    parser.add_argument("--output")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    try:
        source_sha, dirty = _repo_context(repo)
        if dirty:
            raise ValueError("dirty_source_worktree")
        release_sha = _validate_sha(args.release_sha or source_sha, field="release_sha")
        if release_sha != source_sha:
            raise ValueError("release_sha_must_equal_builder_source_sha")
        heads = _alembic_heads(repo)
        packet = build_packet(
            project_id=args.project_id, environment_id=args.environment_id, service_id=args.service_id,
            release_sha=release_sha, builder_source_sha=source_sha, alembic_heads=heads,
            backup_ref=args.backup_ref, rollback_ref=args.rollback_ref,
            created_at=datetime.now(UTC), ttl_minutes=args.ttl_minutes,
        )
    except ValueError as exc:
        reason = re.sub(r"[^a-zA-Z0-9_.:-]+", "_", str(exc)).strip("_")
        raise SystemExit(f"MIGRATION_PACKET=HOLD reason={reason}") from None
    rendered = json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
