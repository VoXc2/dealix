"""Migrate preserved Railway rows into the current self-host schema.

Source must be a restored Railway backup, never the live Railway database.
All non-empty legacy rows are preserved losslessly in operational_event_streams.
Only proof_events and conversations receive typed projections; publication
consent/approval is never inferred from historical fields.
"""
from __future__ import annotations

import asyncio
import json
import os
from datetime import UTC, datetime
from typing import Any

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


def _url(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is required")
    return value.replace("postgresql+asyncpg://", "postgresql://", 1)


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
    source = await asyncpg.connect(_url("DEALIX_RAILWAY_RESTORED_DATABASE_URL"))
    target = await asyncpg.connect(_url("DATABASE_URL"))
    try:
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

        backup_sha = os.environ.get("DEALIX_RAILWAY_BACKUP_SHA256", "unknown")
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
        if archived_total != source_total:
            raise RuntimeError(f"archive count mismatch source={source_total} target={archived_total}")
        if proof_total != source_nonempty.get("proof_events", 0):
            raise RuntimeError("typed proof count mismatch")
        if conversation_total != source_nonempty.get("conversations", 0):
            raise RuntimeError("typed conversation count mismatch")
        print(
            "RAILWAY_DATA_MIGRATION=PASS "
            f"source_rows={source_total} archived_rows={archived_total} "
            f"typed_proof={proof_total} typed_conversations={conversation_total} "
            "publication_consent_inferred=false"
        )
        return 0
    finally:
        await source.close()
        await target.close()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
