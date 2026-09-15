#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def parse_time(value: str) -> datetime:
    text = value.strip()
    if re.fullmatch(r"\d{8}T\d{6}Z", text):
        return datetime.strptime(text, "%Y%m%dT%H%M%SZ").replace(tzinfo=UTC)
    parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp missing timezone")
    return parsed.astimezone(UTC)


def load_receipt(path: Path, schema: str) -> dict[str, Any]:
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o077:
        raise RuntimeError(f"receipt permissions too broad: {path} mode={mode:o}")
    data = json.loads(path.read_text(encoding="utf-8"))
    signature = str(data.pop("payload_sha256", ""))
    canonical = json.dumps(
        data, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    if signature != hashlib.sha256(canonical).hexdigest():
        raise RuntimeError(f"receipt integrity failure: {path}")
    if data.get("schema_version") != schema or data.get("status") != "PASS":
        raise RuntimeError(f"receipt schema/status failure: {path}")
    return data


def verify_file_sha(parent: Path, filename: str, expected: str) -> None:
    if not SHA256.fullmatch(expected):
        raise RuntimeError("invalid file sha256 in receipt")
    path = parent / filename
    if not path.is_file():
        raise RuntimeError(f"receipt artifact missing: {path}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError(f"artifact checksum mismatch: {path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--source-backup-receipt", required=True)
    parser.add_argument("--migration-receipt", required=True)
    parser.add_argument("--selfhost-backup-receipt", required=True)
    parser.add_argument("--quiescence-receipt", required=True)
    args = parser.parse_args()
    expected = args.expected_sha.lower()
    if not SHA40.fullmatch(expected):
        raise RuntimeError("expected release sha must be exact 40-char sha")

    source_path = Path(args.source_backup_receipt).resolve()
    migration_path = Path(args.migration_receipt).resolve()
    target_path = Path(args.selfhost_backup_receipt).resolve()
    quiet_path = Path(args.quiescence_receipt).resolve()
    source = load_receipt(source_path, "dealix.railway-source-backup-receipt.v1")
    migration = load_receipt(migration_path, "dealix.railway-data-migration-receipt.v1")
    target = load_receipt(target_path, "dealix.selfhost-backup-receipt.v1")
    quiet = load_receipt(quiet_path, "dealix.railway-quiescence-receipt.v1")

    if source.get("backup_role") != "railway-source":
        raise RuntimeError("source backup role mismatch")
    if target.get("backup_role") != "selfhost-target":
        raise RuntimeError("self-host backup role mismatch")
    verify_file_sha(source_path.parent, str(source["dump_file"]), str(source["dump_sha256"]))
    verify_file_sha(target_path.parent, str(target["archive_file"]), str(target["archive_sha256"]))

    source_sha = str(source["dump_sha256"])
    source_fp = str(source.get("database_fingerprint_sha256", ""))
    if not SHA256.fullmatch(source_fp):
        raise RuntimeError("source backup receipt missing database fingerprint")
    if source.get("pg_restore_list") != "PASS":
        raise RuntimeError("Railway source restore-list proof missing")
    if int(source.get("postgres_major", 0)) != 18 or source.get("pgvector_required") is not True:
        raise RuntimeError("Railway source is not PG18+pgvector authority")
    if migration.get("source_backup_sha256") != source_sha:
        raise RuntimeError("migration source backup sha mismatch")
    if quiet.get("source_backup_sha256") != source_sha:
        raise RuntimeError("quiescence source backup sha mismatch")
    if quiet.get("database_fingerprint_sha256") != source_fp:
        raise RuntimeError("Railway quiescence fingerprint mismatch")
    for name, value in (
        ("source", source.get("release_sha")),
        ("migration", migration.get("target_release_sha")),
        ("target", target.get("release_sha")),
        ("quiescence", quiet.get("target_release_sha")),
    ):
        if value != expected:
            raise RuntimeError(f"{name} release sha mismatch")

    if migration.get("migration_mode") != "production":
        raise RuntimeError("scratch migration receipt cannot authorize cutover")
    if migration.get("publication_consent_inferred") is not False:
        raise RuntimeError("migration receipt inferred publication consent")
    if int(migration.get("public_consent_true", -1)) != 0:
        raise RuntimeError("migrated proof publication consent is not zero")
    if int(migration.get("approval_not_required", -1)) != 0:
        raise RuntimeError("migrated proof approval invariant failed")
    if int(migration.get("source_rows", -1)) != int(migration.get("archived_rows", -2)):
        raise RuntimeError("migration row parity failed")

    if target.get("postgres_restore_list") != "PASS":
        raise RuntimeError("self-host backup restore-list proof missing")
    if int(target.get("postgres_major", 0)) != 18 or target.get("pgvector_required") is not True:
        raise RuntimeError("self-host backup is not PG18+pgvector authority")
    expected_counts = (
        ("railway_archived_rows", "archived_rows"),
        ("railway_proof_rows", "typed_proof"),
        ("railway_conversation_rows", "typed_conversations"),
    )
    for backup_key, migration_key in expected_counts:
        if int(target.get(backup_key, -1)) != int(migration.get(migration_key, -2)):
            raise RuntimeError(f"self-host backup count mismatch: {backup_key}")

    now = datetime.now(UTC)
    source_at = parse_time(str(source["source_snapshot_started_at"]))
    migration_started = parse_time(str(migration["migration_started_at"]))
    migration_completed = parse_time(str(migration["migration_completed_at"]))
    migration_expires = parse_time(str(migration["expires_at"]))
    target_at = parse_time(str(target["created_at"]))
    quiet_at = parse_time(str(quiet["checked_at"]))
    quiet_expires = parse_time(str(quiet["expires_at"]))

    if source_at > migration_started or migration_started > migration_completed:
        raise RuntimeError("invalid source/migration receipt ordering")
    if target_at < migration_completed:
        raise RuntimeError("self-host backup predates completed migration")
    if quiet_at < migration_completed or quiet_at < target_at:
        raise RuntimeError("quiescence proof must follow migration and target backup")
    if now > migration_expires:
        raise RuntimeError("data migration receipt expired")
    if now > quiet_expires:
        raise RuntimeError("Railway quiescence receipt expired")
    if now - source_at > timedelta(minutes=30):
        raise RuntimeError("source backup is too old for cutover")
    if now - target_at > timedelta(minutes=30):
        raise RuntimeError("self-host backup is too old for cutover")
    if quiet_expires - quiet_at > timedelta(minutes=5, seconds=5):
        raise RuntimeError("quiescence receipt TTL exceeds five-minute bound")

    print(
        "SELFHOST_CUTOVER_RECEIPTS=PASS "
        f"release_sha={expected} "
        f"alembic={migration.get('target_alembic_head')} "
        f"source_rows={migration.get('source_rows')} "
        f"quiescence_expires={quiet.get('expires_at')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
