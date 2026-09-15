"""Migrate preserved Railway rows into the current self-host schema.

Source must be a restored Railway backup, never the live Railway database.
All non-empty legacy rows are preserved losslessly in operational_event_streams.
Only proof_events and conversations receive typed projections; publication
consent/approval is never inferred from historical fields.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import asyncpg

ALLOWED_NONEMPTY = (
    "proof_events",
    "unsafe_action_attempts",
    "agent_run_costs",
    "daily_ops_runs",
    "support_tickets",
    "conversations",
)
STREAM_ID = "railway_legacy_20260915"
MIGRATION_VERSION = "railway_exit_v1"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SHA40_RE = re.compile(r"^[0-9a-f]{40}$")
RECEIPT_SCHEMA = "dealix.railway-data-migration-receipt.v1"
RECEIPT_TTL = timedelta(minutes=15)
MAX_BACKUP_AGE = timedelta(minutes=30)
LIVE_PROVIDER_HOST_MARKERS = ("railway", "rlwy.net")


def _url(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is required")
    return value.replace("postgresql+asyncpg://", "postgresql://", 1)


def _reject_live_provider_url(value: str, *, field: str) -> None:
    host = (urlparse(value).hostname or "").lower()
    if any(marker in host for marker in LIVE_PROVIDER_HOST_MARKERS):
        raise RuntimeError(f"{field} must not point at live Railway infrastructure")



def _parse_utc(value: str, *, field: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise RuntimeError(f"{field} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise RuntimeError(f"{field} must include timezone")
    return parsed.astimezone(UTC)


def _write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    payload = dict(receipt)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    payload["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(rendered, encoding="utf-8")
    os.chmod(tmp, 0o600)
    tmp.replace(path)
    os.chmod(path, 0o600)

def _dt(row: dict[str, Any]) -> datetime:
    for key in ("occurred_at", "created_at", "started_at", "finished_at"):
        value = row.get(key)
        if isinstance(value, datetime):
            return value.replace(tzinfo=UTC) if value.tzinfo is None else value
    return datetime.now(UTC)


def _dt_naive(row: dict[str, Any]) -> datetime:
    return _dt(row).astimezone(UTC).replace(tzinfo=None)


def _jsonable(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    return value


async def _rows(conn: asyncpg.Connection, table: str) -> list[dict[str, Any]]:
    records = await conn.fetch(f'SELECT to_jsonb(t) AS row FROM public."{table}" AS t ORDER BY id')
    rows: list[dict[str, Any]] = []
    for record in records:
        raw = record["row"]
        rows.append(json.loads(raw) if isinstance(raw, str) else dict(raw))
    return rows


async def main() -> int:
    if os.environ.get("DEALIX_DB_MIGRATION") != "YES":
        raise RuntimeError("DEALIX_DB_MIGRATION=YES is required")
    if os.environ.get("DEALIX_SOURCE_IS_RESTORED_BACKUP") != "YES":
        raise RuntimeError("DEALIX_SOURCE_IS_RESTORED_BACKUP=YES is required")
    backup_sha = os.environ.get("DEALIX_RAILWAY_BACKUP_SHA256", "").strip().lower()
    if not SHA256_RE.fullmatch(backup_sha):
        raise RuntimeError("DEALIX_RAILWAY_BACKUP_SHA256 must be an exact SHA256")
    target_release_sha = os.environ.get("DEALIX_TARGET_RELEASE_SHA", "").strip().lower()
    if not SHA40_RE.fullmatch(target_release_sha):
        raise RuntimeError("DEALIX_TARGET_RELEASE_SHA must be an exact 40-character SHA")
    migration_mode = os.environ.get("DEALIX_MIGRATION_MODE", "production").strip().lower()
    action_id = f"dealix-production-db-migration-v1:{target_release_sha}"
    if migration_mode == "production":
        if os.environ.get("DEALIX_L5_APPROVAL_ACTION") != action_id:
            raise RuntimeError(f"approval required: DEALIX_L5_APPROVAL_ACTION={action_id}")
    elif migration_mode != "scratch":
        raise RuntimeError("DEALIX_MIGRATION_MODE must be production or scratch")
    receipt_path_text = os.environ.get("DEALIX_DATA_MIGRATION_RECEIPT_PATH", "").strip()
    if not receipt_path_text:
        raise RuntimeError("DEALIX_DATA_MIGRATION_RECEIPT_PATH is required")
    backup_captured_at = _parse_utc(
        os.environ.get("DEALIX_RAILWAY_BACKUP_CAPTURED_AT", ""),
        field="DEALIX_RAILWAY_BACKUP_CAPTURED_AT",
    )
    started_at = datetime.now(UTC)
    age = started_at - backup_captured_at
    if age < timedelta(minutes=-1):
        raise RuntimeError("backup capture time is in the future")
    if age > MAX_BACKUP_AGE:
        raise RuntimeError("Railway source backup is stale; capture a fresh backup before migration")
    source_url = _url("DEALIX_RAILWAY_RESTORED_DATABASE_URL")
    target_url = _url("DATABASE_URL")
    _reject_live_provider_url(source_url, field="source")
    _reject_live_provider_url(target_url, field="target")
    target_parsed = urlparse(target_url)
    target_host = (target_parsed.hostname or "").lower()
    if target_host not in {"postgres", "dealix-postgres", "127.0.0.1", "localhost", "::1"}:
        raise RuntimeError("target must be the admitted self-host PostgreSQL instance")
    if migration_mode == "scratch":
        if os.environ.get("DEALIX_SCRATCH_MIGRATION") != "YES":
            raise RuntimeError("scratch mode requires DEALIX_SCRATCH_MIGRATION=YES")
        if target_host not in {"127.0.0.1", "localhost", "::1"} or (target_parsed.port or 5432) in {5432, 6432}:
            raise RuntimeError("scratch target must use loopback on a non-production PostgreSQL port")
    if source_url == target_url:
        raise RuntimeError("source and target databases must differ")
    source = await asyncpg.connect(source_url)
    target = await asyncpg.connect(target_url)
    try:
        await source.execute("SET default_transaction_read_only = on")
        source_nonempty: dict[str, int] = {}
        for name in await source.fetch("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename"):
            table = str(name["tablename"])
            count = int(await source.fetchval(f'SELECT count(*) FROM public."{table}"'))
            if count:
                source_nonempty[table] = count
        unexpected = sorted(set(source_nonempty) - set(ALLOWED_NONEMPTY))
        if unexpected:
            raise RuntimeError("unexpected non-empty source tables: " + ",".join(unexpected))

        required_targets = {"operational_event_streams", "proof_events", "conversations", "alembic_version"}
        targets = {str(r["tablename"]) for r in await target.fetch("SELECT tablename FROM pg_tables WHERE schemaname='public'")}
        missing = sorted(required_targets - targets)
        if missing:
            raise RuntimeError("target is not current bootstrapped schema: " + ",".join(missing))

        archived = typed_proof = typed_conversations = 0
        async with target.transaction():
            for table in ALLOWED_NONEMPTY:
                for row in await _rows(source, table):
                    source_id = str(row.get("id") or archived)
                    payload = {
                        "migration_version": MIGRATION_VERSION,
                        "source": "railway_production_backup",
                        "source_backup_sha256": backup_sha,
                        "source_table": table,
                        "source_row": _jsonable(row),
                    }
                    result = await target.execute(
                        """
                        INSERT INTO operational_event_streams(stream_id,event_id,payload,occurred_at)
                        VALUES($1,$2,$3::jsonb,$4)
                        ON CONFLICT(stream_id,event_id) DO NOTHING
                        """,
                        STREAM_ID,
                        f"{table}:{source_id}",
                        json.dumps(payload, ensure_ascii=False),
                        _dt(row),
                    )
                    if result.endswith("1"):
                        archived += 1

                    if table == "proof_events":
                        weight = row.get("weight")
                        try:
                            confidence = max(0.0, min(1.0, float(weight if weight is not None else 0.5)))
                        except (TypeError, ValueError):
                            confidence = 0.5
                        typed = await target.execute(
                            """
                            INSERT INTO proof_events(
                              id,event_type,customer_handle,service_id,summary_ar,summary_en,
                              evidence_source,confidence,consent_for_publication,
                              redacted_summary_ar,redacted_summary_en,approval_status,
                              risk_level,payload_json,created_at)
                            VALUES($1,$2,$3,$4,$5,$6,$7,$8,false,$9,$10,'approval_required',$11,$12::json,$13)
                            ON CONFLICT(id) DO NOTHING
                            """,
                            f"legacy:{source_id}",
                            str(row.get("unit_type") or "legacy_railway_proof"),
                            str(row.get("customer_id") or row.get("partner_id") or "legacy-unscoped"),
                            row.get("service_id"),
                            str(row.get("label_ar") or "إثبات تاريخي مرحّل — غير مصرح للنشر"),
                            "Migrated legacy proof event — not publication-authorized",
                            "railway_production_backup",
                            confidence,
                            "إثبات تاريخي مرحّل",
                            "Migrated legacy proof event",
                            str(row.get("risk_level") or "medium"),
                            json.dumps(payload, ensure_ascii=False),
                            _dt(row),
                        )
                        if typed.endswith("1"):
                            typed_proof += 1

                    if table == "conversations":
                        typed = await target.execute(
                            """
                            INSERT INTO conversations(
                              id,tenant_id,lead_id,channel,sender,inbound_message,outbound_response,
                              classification,sentiment,next_action,escalation_required,auto_sent,
                              created_at,deleted_at)
                            VALUES($1,NULL,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,NULL)
                            ON CONFLICT(id) DO NOTHING
                            """,
                            f"legacy:{source_id}", row.get("lead_id"),
                            str(row.get("channel") or "legacy"), row.get("sender"),
                            str(row.get("inbound_message") or ""), row.get("outbound_response"),
                            row.get("classification"), row.get("sentiment"), row.get("next_action"),
                            bool(row.get("escalation_required")), bool(row.get("auto_sent")), _dt_naive(row),
                        )
                        if typed.endswith("1"):
                            typed_conversations += 1

        source_total = sum(source_nonempty.values())
        archived_total = int(await target.fetchval("SELECT count(*) FROM operational_event_streams WHERE stream_id=$1", STREAM_ID))
        proof_total = int(await target.fetchval("SELECT count(*) FROM proof_events WHERE evidence_source='railway_production_backup'"))
        conversation_total = int(await target.fetchval("SELECT count(*) FROM conversations WHERE id LIKE 'legacy:%'"))
        public_consent_true = int(await target.fetchval(
            "SELECT count(*) FROM proof_events WHERE evidence_source='railway_production_backup' AND consent_for_publication=true"
        ))
        approval_not_required = int(await target.fetchval(
            "SELECT count(*) FROM proof_events WHERE evidence_source='railway_production_backup' AND approval_status<>'approval_required'"
        ))
        target_alembic_head = str(await target.fetchval("SELECT version_num FROM alembic_version LIMIT 1") or "")
        if archived_total != source_total:
            raise RuntimeError(f"archive count mismatch source={source_total} target={archived_total}")
        if proof_total != source_nonempty.get("proof_events", 0):
            raise RuntimeError("typed proof count mismatch")
        if conversation_total != source_nonempty.get("conversations", 0):
            raise RuntimeError("typed conversation count mismatch")
        if public_consent_true != 0 or approval_not_required != 0:
            raise RuntimeError("migrated proof governance invariant violated")
        if not target_alembic_head:
            raise RuntimeError("target Alembic head missing")

        completed_at = datetime.now(UTC)
        receipt = {
            "schema_version": RECEIPT_SCHEMA,
            "status": "PASS",
            "migration_version": MIGRATION_VERSION,
            "migration_mode": migration_mode,
            "target_release_sha": target_release_sha,
            "target_alembic_head": target_alembic_head,
            "source_backup_sha256": backup_sha,
            "source_captured_at": backup_captured_at.isoformat().replace("+00:00", "Z"),
            "migration_started_at": started_at.isoformat().replace("+00:00", "Z"),
            "migration_completed_at": completed_at.isoformat().replace("+00:00", "Z"),
            "expires_at": (completed_at + RECEIPT_TTL).isoformat().replace("+00:00", "Z"),
            "source_counts": source_nonempty,
            "source_rows": source_total,
            "archived_rows": archived_total,
            "typed_proof": proof_total,
            "typed_conversations": conversation_total,
            "publication_consent_inferred": False,
            "public_consent_true": public_consent_true,
            "approval_not_required": approval_not_required,
        }
        receipt_path = Path(receipt_path_text).expanduser()
        _write_receipt(receipt_path, receipt)
        print(
            "RAILWAY_DATA_MIGRATION=PASS "
            f"source_rows={source_total} archived_rows={archived_total} "
            f"typed_proof={proof_total} typed_conversations={conversation_total} "
            "publication_consent_inferred=false "
            f"receipt={receipt_path}"
        )
        return 0
    finally:
        await source.close()
        await target.close()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
