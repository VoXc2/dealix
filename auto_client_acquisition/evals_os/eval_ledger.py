"""Eval ledger — append-only JSONL log of suite runs.

Stores each ``EvalRunSummary`` so pass-rate trends are auditable and
regressions can be detected against the previous run of the same suite.
"""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from auto_client_acquisition.evals_os.schemas import EvalRunSummary

__all__ = ["emit_eval_run", "list_eval_runs", "last_run", "clear_for_test"]

_DEFAULT_PATH = "var/eval-ledger.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_EVAL_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def emit_eval_run(summary: EvalRunSummary) -> EvalRunSummary:
    if not summary.customer_id.strip():
        raise ValueError("summary.customer_id is required")
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(summary.to_dict(), ensure_ascii=False) + "\n")
    return summary


def list_eval_runs(
    *,
    customer_id: str,
    suite_id: str | None = None,
    limit: int = 100,
    since_days: int = 180,
) -> list[dict[str, Any]]:
    if not customer_id:
        return []
    path = _path()
    if not path.exists():
        return []
    cutoff = datetime.now(timezone.utc).timestamp() - since_days * 86400
    out: list[dict[str, Any]] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except Exception:  # noqa: BLE001
            continue
        if data.get("customer_id") != customer_id:
            continue
        if suite_id is not None and data.get("suite_id") != suite_id:
            continue
        try:
            ts = datetime.fromisoformat(data.get("occurred_at", "")).timestamp()
        except Exception:  # noqa: BLE001
            ts = 0.0
        if ts < cutoff:
            continue
        out.append(data)
    return out[-limit:]


def last_run(*, customer_id: str, suite_id: str) -> dict[str, Any] | None:
    """Most recent run of ``suite_id`` for ``customer_id`` (for regression
    comparison), or ``None`` if there is no prior run."""
    runs = list_eval_runs(customer_id=customer_id, suite_id=suite_id, limit=1)
    return runs[-1] if runs else None


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")
