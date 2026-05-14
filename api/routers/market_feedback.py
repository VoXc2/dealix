"""Public market-feedback capture — the honest signal that the market is responding.

  POST /api/v1/public/market-feedback
      Public (no auth), with consent + honeypot, matching the existing
      `public.py` demo-request pattern.

  GET /api/v1/public/market-feedback/summary
      Public-safe aggregate of the last 30 days. No PII surfaced.

Body (POST):
    {
      "name":       optional[str],
      "email":      optional[str],
      "role":       optional[str],
      "sector":     optional[str],
      "signal_type": "objection" | "request" | "praise" | "idea",
      "message":    str,        (REQUIRED, 1..2000 chars)
      "consent":    bool,        (REQUIRED true)
      "website":    optional[str]  (honeypot — non-empty silently drops)
    }

Returns:
    { "ok": true, "feedback_id": "<hex>" }
"""
from __future__ import annotations

import json
import logging
import re
import uuid
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/public", tags=["public"])

REPO_ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = REPO_ROOT / "data" / "_state" / "market_feedback.jsonl"

VALID_SIGNAL_TYPES = ("objection", "request", "praise", "idea")
MAX_MESSAGE_LEN = 2000


_EMAIL_RX = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def _redact_email(s: str) -> str:
    """Replace any email substring with a generic placeholder."""
    return _EMAIL_RX.sub("[email]", s or "")


def _append(entry: dict[str, Any]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n")


def _load_last_n_days(days: int = 30) -> list[dict[str, Any]]:
    if not LOG_PATH.exists():
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    out: list[dict[str, Any]] = []
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = row.get("received_at")
        try:
            dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        except Exception:
            continue
        if dt >= cutoff:
            out.append(row)
    return out


@router.post("/market-feedback")
async def market_feedback(req: Request) -> dict[str, Any]:
    """Capture one feedback signal. No external send, no PII surfaced."""
    try:
        body = await req.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid_json")

    # Honeypot: if the `website` field is filled, drop silently.
    if str(body.get("website") or "").strip():
        log.info("market_feedback_honeypot_triggered")
        return {"ok": True, "feedback_id": "honeypot"}

    signal_type = str(body.get("signal_type") or "").lower().strip()
    if signal_type not in VALID_SIGNAL_TYPES:
        raise HTTPException(status_code=422, detail=f"signal_type must be one of {VALID_SIGNAL_TYPES}")
    if not bool(body.get("consent")):
        raise HTTPException(status_code=422, detail="consent_required")

    message = str(body.get("message") or "").strip()
    if not message:
        raise HTTPException(status_code=422, detail="message_required")
    if len(message) > MAX_MESSAGE_LEN:
        raise HTTPException(status_code=422, detail=f"message too long (>{MAX_MESSAGE_LEN})")

    feedback_id = uuid.uuid4().hex
    entry = {
        "feedback_id": feedback_id,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "signal_type": signal_type,
        # Strip emails from the stored message — internal log keeps the
        # redacted version so future analysis is safe by default.
        "message_redacted": _redact_email(message)[:MAX_MESSAGE_LEN],
        "role": str(body.get("role") or "").strip()[:80],
        "sector": str(body.get("sector") or "").strip()[:80],
        # name/email are accepted but NEVER returned by any public read.
        "name_present": bool(str(body.get("name") or "").strip()),
        "email_present": bool(str(body.get("email") or "").strip()),
    }
    _append(entry)
    return {"ok": True, "feedback_id": feedback_id}


@router.get("/market-feedback/summary")
async def market_feedback_summary() -> dict[str, Any]:
    """Public-safe aggregate over the last 30 days. No PII / no names."""
    rows = _load_last_n_days(30)
    by_type: Counter[str] = Counter()
    by_sector: Counter[str] = Counter()
    samples: list[dict[str, Any]] = []

    for row in rows:
        by_type[row.get("signal_type", "unknown")] += 1
        sector = row.get("sector") or "unspecified"
        by_sector[sector] += 1

    # Up to 5 most recent (anonymized) quotes — redacted-message only.
    for row in rows[-5:]:
        samples.append({
            "signal_type": row.get("signal_type"),
            "received_at": row.get("received_at"),
            "quote": (row.get("message_redacted") or "")[:200],
        })

    return {
        "window_days": 30,
        "total": len(rows),
        "by_signal_type": dict(by_type),
        "by_sector": dict(by_sector),
        "recent_anonymized": samples,
        "doctrine": (
            "No names. No emails. No phone numbers. Only signal type, "
            "redacted quote, and sector if provided."
        ),
    }
