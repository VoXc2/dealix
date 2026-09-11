"""Slack & Telegram L5 — governed, one ACTION_HASH per send, draft-only until approval."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

def action_hash(action_type: str, target: str, env: str, payload: str) -> str:
    raw = f"{action_type}|{target}|{env}|{payload}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

class SlackL5Packet(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action_type: str = "SEND_SLACK"
    target: str = "#founder-approvals"
    environment: str = "production"
    payload: str = ""  # Top3 + MONEY
    head_sha: str = UNKNOWN
    expected_value: str = UNKNOWN
    risk: str = UNKNOWN
    rollback: str = "delete_message"
    expiry: str = Field(default_factory=lambda: (datetime.now(UTC).isoformat()))
    idempotency_key: str = Field(default_factory=lambda: f"slack_{hashlib.sha256(str(datetime.now(UTC).timestamp()).encode()).hexdigest()[:8]}")
    action_hash: str = ""

    def compute_hash(self) -> str:
        self.action_hash = action_hash(self.action_type, self.target, self.environment, self.payload)
        return self.action_hash

class TelegramL5Packet(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action_type: str = "TELEGRAM_COMMAND"
    target: str = "@Samihanterjobs_bot"
    environment: str = "production"
    payload: str = ""
    head_sha: str = UNKNOWN
    evidence_ref: str = UNKNOWN
    idempotency_key: str = Field(default_factory=lambda: f"tg_{hashlib.sha256(str(datetime.now(UTC).timestamp()).encode()).hexdigest()[:8]}")
    action_hash: str = ""

    def compute_hash(self) -> str:
        self.action_hash = action_hash(self.action_type, self.target, self.environment, self.payload)
        return self.action_hash

__all__ = ["SlackL5Packet", "TelegramL5Packet", "action_hash", "UNKNOWN"]
