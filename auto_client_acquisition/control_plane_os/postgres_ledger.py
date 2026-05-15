"""Postgres-backed control-event ledger with JSONL fallback."""

from __future__ import annotations

import json
import os
from typing import Any

from auto_client_acquisition.control_plane_os.ledger import JsonlControlLedger
from auto_client_acquisition.control_plane_os.schemas import ControlEvent

try:  # pragma: no cover - import guard for lightweight environments
    from sqlalchemy import create_engine, text
except Exception:
    create_engine = None
    text = None


class PostgresControlLedger:
    def __init__(self, *, database_url: str | None = None) -> None:
        self._fallback = JsonlControlLedger()
        self._database_url = (database_url or os.getenv("DATABASE_URL", "")).strip()
        self._enabled = bool(self._database_url and create_engine and text)
        self._engine = create_engine(self._database_url) if self._enabled else None

    @property
    def enabled(self) -> bool:
        return self._enabled

    def append(self, event: ControlEvent) -> ControlEvent:
        if not self._enabled:
            return self._fallback.append(event)
        assert text is not None
        payload = dict(event.payload or {})
        sql = text(
            """
            INSERT INTO control_events (
                id, tenant_id, event_type, source_module, actor, subject_type, subject_id,
                run_id, correlation_id, decision, occurred_at, payload, redacted
            ) VALUES (
                :id, :tenant_id, :event_type, :source_module, :actor, :subject_type, :subject_id,
                :run_id, :correlation_id, :decision, :occurred_at, CAST(:payload AS JSONB), :redacted
            )
            """
        )
        with self._engine.begin() as conn:
            conn.execute(
                sql,
                {
                    "id": event.id,
                    "tenant_id": event.tenant_id,
                    "event_type": event.event_type,
                    "source_module": event.source_module,
                    "actor": event.actor,
                    "subject_type": event.subject_type,
                    "subject_id": event.subject_id,
                    "run_id": event.run_id,
                    "correlation_id": event.correlation_id,
                    "decision": event.decision,
                    "occurred_at": event.occurred_at,
                    "payload": json.dumps(payload, ensure_ascii=False),
                    "redacted": event.redacted,
                },
            )
        return event

    def list_events(self, *, tenant_id: str, run_id: str = "", limit: int = 500) -> list[ControlEvent]:
        if not self._enabled:
            return self._fallback.list_events(tenant_id=tenant_id, run_id=run_id, limit=limit)
        assert text is not None
        params: dict[str, Any] = {"tenant_id": tenant_id, "limit": limit}
        if run_id:
            params["run_id"] = run_id
            sql = text(
                """
                SELECT id, tenant_id, event_type, source_module, actor, subject_type, subject_id,
                       run_id, correlation_id, decision, occurred_at, payload, redacted
                FROM control_events
                WHERE tenant_id = :tenant_id AND run_id = :run_id
                ORDER BY occurred_at ASC
                LIMIT :limit
                """
            )
        else:
            sql = text(
                """
                SELECT id, tenant_id, event_type, source_module, actor, subject_type, subject_id,
                       run_id, correlation_id, decision, occurred_at, payload, redacted
                FROM control_events
                WHERE tenant_id = :tenant_id
                ORDER BY occurred_at ASC
                LIMIT :limit
                """
            )
        with self._engine.begin() as conn:
            rows = conn.execute(sql, params).mappings().all()
        out: list[ControlEvent] = []
        for row in rows:
            payload = row.get("payload")
            if isinstance(payload, str):
                try:
                    payload = json.loads(payload)
                except json.JSONDecodeError:
                    payload = {}
            out.append(
                ControlEvent(
                    id=str(row["id"]),
                    tenant_id=str(row["tenant_id"]),
                    event_type=str(row["event_type"]),
                    source_module=str(row["source_module"]),
                    actor=str(row["actor"]),
                    subject_type=str(row.get("subject_type") or ""),
                    subject_id=str(row.get("subject_id") or ""),
                    run_id=str(row.get("run_id") or ""),
                    correlation_id=str(row.get("correlation_id") or ""),
                    decision=str(row.get("decision") or ""),
                    occurred_at=str(row.get("occurred_at")),
                    payload=dict(payload or {}),
                    redacted=bool(row.get("redacted", True)),
                )
            )
        return out
