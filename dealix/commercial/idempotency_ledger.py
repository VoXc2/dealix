"""Durable replay/reconciliation ledger for Dealix external effects.

The ledger reserves an idempotency key before a provider effect. Ambiguous
outcomes become UNKNOWN and cannot be retried until independent reconciliation.
Confirmed non-delivery becomes ABORTED and requires a new key + fresh approval.

Schema upgrades are fail-closed and preserve existing rows. In particular, old
ledgers whose CHECK constraint did not include ABORTED are transactionally
rebuilt before reconciliation can use UNKNOWN -> ABORTED.
"""
from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

LedgerState = Literal["RESERVED", "COMMITTED", "UNKNOWN", "ABORTED"]
ReserveStatus = Literal[
    "RESERVED_NEW",
    "REPLAY_COMMITTED",
    "IN_FLIGHT_OR_UNKNOWN",
    "RECONCILED_NOT_DELIVERED",
    "CONFLICT",
]

_TABLE = "external_effect_idempotency"
def _now() -> str:
    return datetime.now(UTC).isoformat()


def _evidence_ref(value: str) -> str:
    text = value.strip()
    if not text:
        raise ValueError("reconciliation evidence_ref is required")
    return text


def _confirmed_delivery_receipt(receipt: dict[str, object]) -> dict[str, object]:
    if not isinstance(receipt, dict):
        raise ValueError("confirmed delivery receipt must be an object")
    provider = receipt.get("provider")
    provider_message_id = receipt.get("provider_message_id")
    status = receipt.get("status")
    if not all(
        isinstance(value, str) and value.strip()
        for value in (provider, provider_message_id, status)
    ):
        raise ValueError("confirmed delivery receipt is incomplete")
    if status != "CONFIRMED_DELIVERED":
        raise ValueError("confirmed delivery receipt status is not confirmed")
    return dict(receipt)


def _confirmed_delivery_receipt(receipt: dict[str, object]) -> dict[str, object]:
    """Require provider-backed delivery identity before UNKNOWN -> COMMITTED."""
    required = ("provider", "provider_message_id", "status")
    if not isinstance(receipt, dict):
        raise ValueError("confirmed delivery receipt must be an object")
    for key in required:
        value = receipt.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"confirmed delivery receipt requires nonblank {key}")
    if receipt["status"] != "CONFIRMED_DELIVERED":
        raise ValueError("confirmed delivery receipt status must be CONFIRMED_DELIVERED")
    return dict(receipt)


@dataclass(frozen=True)
class ReserveResult:
    status: ReserveStatus
    state: LedgerState | None
    receipt: dict[str, object] | None = None
    reconciliation: dict[str, object] | None = None


class SqliteIdempotencyLedger:
    """SQLite ledger stored outside the repository/control-plane source tree."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        parent_preexisted = self.path.parent.exists()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not parent_preexisted:
            try:
                os.chmod(self.path.parent, 0o700)
            except OSError:
                # Permission hardening is best-effort; never block ledger startup.
                pass
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(str(self.path), timeout=30, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA synchronous=FULL")
        connection.execute("PRAGMA busy_timeout=30000")
        return connection

    @staticmethod
    def _create_schema(connection: sqlite3.Connection, table: str) -> None:
        connection.execute(
            f"""
            CREATE TABLE {table} (
                idempotency_key TEXT PRIMARY KEY,
                action_hash TEXT NOT NULL,
                packet_integrity_sha256 TEXT NOT NULL,
                state TEXT NOT NULL CHECK(state IN ('RESERVED','COMMITTED','UNKNOWN','ABORTED')),
                receipt_json TEXT,
                reconciliation_json TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            existing_sql_row = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (_TABLE,)
            ).fetchone()
            if existing_sql_row is None:
                self._create_schema(connection, _TABLE)
                connection.execute("COMMIT")
            else:
                existing_sql = str(existing_sql_row["sql"] or "")
                columns = {
                    str(row[1])
                    for row in connection.execute(f"PRAGMA table_info({_TABLE})")
                }
                needs_rebuild = (
                    "ABORTED" not in existing_sql
                    or "reconciliation_json" not in columns
                )
                if needs_rebuild:
                    replacement = f"{_TABLE}_v2_rebuild"
                    connection.execute(f"DROP TABLE IF EXISTS {replacement}")
                    self._create_schema(connection, replacement)
                    reconciliation_expr = (
                        "reconciliation_json"
                        if "reconciliation_json" in columns
                        else "NULL"
                    )
                    connection.execute(
                        f"""
                        INSERT INTO {replacement} (
                            idempotency_key,
                            action_hash,
                            packet_integrity_sha256,
                            state,
                            receipt_json,
                            reconciliation_json,
                            created_at,
                            updated_at
                        )
                        SELECT
                            idempotency_key,
                            action_hash,
                            packet_integrity_sha256,
                            state,
                            receipt_json,
                            {reconciliation_expr},
                            created_at,
                            updated_at
                        FROM {_TABLE}
                        """
                    )
                    connection.execute(f"DROP TABLE {_TABLE}")
                    connection.execute(
                        f"ALTER TABLE {replacement} RENAME TO {_TABLE}"
                    )
                connection.execute("COMMIT")
        try:
            os.chmod(self.path, 0o600)
        except OSError:
            # Restrictive file mode is best-effort and must not hide the ledger result.
            pass

    @staticmethod
    def _decode(row: sqlite3.Row, key: str) -> dict[str, object] | None:
        raw = row[key] if key in row.keys() else None
        return json.loads(raw) if raw else None

    def reserve(
        self,
        *,
        idempotency_key: str,
        action_hash: str,
        packet_integrity_sha256: str,
    ) -> ReserveResult:
        key = idempotency_key.strip()
        if not key:
            raise ValueError("idempotency_key is required")
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                f"SELECT * FROM {_TABLE} WHERE idempotency_key=?", (key,)
            ).fetchone()
            if row is None:
                now = _now()
                connection.execute(
                    f"INSERT INTO {_TABLE} "
                    "(idempotency_key,action_hash,packet_integrity_sha256,state,receipt_json,reconciliation_json,created_at,updated_at) "
                    "VALUES (?,?,?,?,?,?,?,?)",
                    (
                        key,
                        action_hash,
                        packet_integrity_sha256,
                        "RESERVED",
                        None,
                        None,
                        now,
                        now,
                    ),
                )
                connection.execute("COMMIT")
                return ReserveResult(status="RESERVED_NEW", state="RESERVED")

            if (
                row["action_hash"] != action_hash
                or row["packet_integrity_sha256"] != packet_integrity_sha256
            ):
                connection.execute("COMMIT")
                return ReserveResult(status="CONFLICT", state=row["state"])

            state: LedgerState = row["state"]
            receipt = self._decode(row, "receipt_json")
            reconciliation = self._decode(row, "reconciliation_json")
            connection.execute("COMMIT")
            if state == "COMMITTED":
                return ReserveResult(
                    status="REPLAY_COMMITTED",
                    state=state,
                    receipt=receipt,
                    reconciliation=reconciliation,
                )
            if state == "ABORTED":
                return ReserveResult(
                    status="RECONCILED_NOT_DELIVERED",
                    state=state,
                    reconciliation=reconciliation,
                )
            return ReserveResult(
                status="IN_FLIGHT_OR_UNKNOWN",
                state=state,
                reconciliation=reconciliation,
            )

    def commit(
        self,
        *,
        idempotency_key: str,
        action_hash: str,
        packet_integrity_sha256: str,
        receipt: dict[str, object],
    ) -> None:
        """Normal provider-success transition RESERVED -> COMMITTED."""
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                f"SELECT * FROM {_TABLE} WHERE idempotency_key=?",
                (idempotency_key,),
            ).fetchone()
            if row is None:
                connection.execute("ROLLBACK")
                raise RuntimeError("idempotency reservation missing")
            if (
                row["action_hash"] != action_hash
                or row["packet_integrity_sha256"] != packet_integrity_sha256
            ):
                connection.execute("ROLLBACK")
                raise RuntimeError("idempotency reservation identity mismatch")
            if row["state"] == "COMMITTED":
                connection.execute("COMMIT")
                return
            if row["state"] != "RESERVED":
                connection.execute("ROLLBACK")
                raise RuntimeError(
                    "cannot commit non-reserved idempotency state; use reconciliation"
                )
            connection.execute(
                f"UPDATE {_TABLE} SET state='COMMITTED',receipt_json=?,updated_at=? WHERE idempotency_key=?",
                (
                    json.dumps(receipt, sort_keys=True, separators=(",", ":")),
                    _now(),
                    idempotency_key,
                ),
            )
            connection.execute("COMMIT")

    def mark_unknown(
        self,
        *,
        idempotency_key: str,
        action_hash: str,
        packet_integrity_sha256: str,
    ) -> None:
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                f"SELECT * FROM {_TABLE} WHERE idempotency_key=?",
                (idempotency_key,),
            ).fetchone()
            if row is None:
                connection.execute("ROLLBACK")
                raise RuntimeError("idempotency reservation missing")
            if (
                row["action_hash"] != action_hash
                or row["packet_integrity_sha256"] != packet_integrity_sha256
            ):
                connection.execute("ROLLBACK")
                raise RuntimeError("idempotency reservation identity mismatch")
            if row["state"] == "RESERVED":
                connection.execute(
                    f"UPDATE {_TABLE} SET state='UNKNOWN',updated_at=? WHERE idempotency_key=?",
                    (_now(), idempotency_key),
                )
            connection.execute("COMMIT")

    def reconcile_unknown_committed(
        self,
        *,
        idempotency_key: str,
        action_hash: str,
        packet_integrity_sha256: str,
        receipt: dict[str, object],
        evidence_ref: str,
    ) -> None:
        """Audited UNKNOWN -> COMMITTED after independent delivery confirmation."""
        receipt = _confirmed_delivery_receipt(receipt)
        confirmed_receipt = _confirmed_delivery_receipt(receipt)
        reconciliation = {
            "resolution": "CONFIRMED_DELIVERED",
            "evidence_ref": _evidence_ref(evidence_ref),
            "resolved_at": _now(),
        }
        self._reconcile_unknown(
            idempotency_key=idempotency_key,
            action_hash=action_hash,
            packet_integrity_sha256=packet_integrity_sha256,
            state="COMMITTED",
            receipt=confirmed_receipt,
            reconciliation=reconciliation,
        )

    def reconcile_unknown_not_delivered(
        self,
        *,
        idempotency_key: str,
        action_hash: str,
        packet_integrity_sha256: str,
        evidence_ref: str,
    ) -> None:
        """Audited UNKNOWN -> ABORTED. Retry needs a new key + fresh approval."""
        reconciliation = {
            "resolution": "CONFIRMED_NOT_DELIVERED",
            "evidence_ref": _evidence_ref(evidence_ref),
            "resolved_at": _now(),
            "next_action": "CREATE_NEW_IDEMPOTENCY_KEY_AND_REAUTHORIZE_BEFORE_RETRY",
        }
        self._reconcile_unknown(
            idempotency_key=idempotency_key,
            action_hash=action_hash,
            packet_integrity_sha256=packet_integrity_sha256,
            state="ABORTED",
            receipt=None,
            reconciliation=reconciliation,
        )

    def _reconcile_unknown(
        self,
        *,
        idempotency_key: str,
        action_hash: str,
        packet_integrity_sha256: str,
        state: Literal["COMMITTED", "ABORTED"],
        receipt: dict[str, object] | None,
        reconciliation: dict[str, object],
    ) -> None:
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                f"SELECT * FROM {_TABLE} WHERE idempotency_key=?",
                (idempotency_key,),
            ).fetchone()
            if row is None:
                connection.execute("ROLLBACK")
                raise RuntimeError("idempotency reservation missing")
            if (
                row["action_hash"] != action_hash
                or row["packet_integrity_sha256"] != packet_integrity_sha256
            ):
                connection.execute("ROLLBACK")
                raise RuntimeError("idempotency reconciliation identity mismatch")
            if row["state"] != "UNKNOWN":
                connection.execute("ROLLBACK")
                raise RuntimeError("reconciliation requires UNKNOWN state")
            connection.execute(
                f"UPDATE {_TABLE} SET state=?,receipt_json=?,reconciliation_json=?,updated_at=? WHERE idempotency_key=?",
                (
                    state,
                    json.dumps(receipt, sort_keys=True, separators=(",", ":"))
                    if receipt is not None
                    else None,
                    json.dumps(reconciliation, sort_keys=True, separators=(",", ":")),
                    _now(),
                    idempotency_key,
                ),
            )
            connection.execute("COMMIT")

    def get(self, idempotency_key: str) -> dict[str, object] | None:
        with self._connect() as connection:
            row = connection.execute(
                f"SELECT * FROM {_TABLE} WHERE idempotency_key=?",
                (idempotency_key,),
            ).fetchone()
        return dict(row) if row is not None else None


__all__ = ["ReserveResult", "SqliteIdempotencyLedger"]
