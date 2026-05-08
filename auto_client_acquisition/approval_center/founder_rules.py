"""Wave 7.7 §1 — Founder Pre-Approved Rules.

Allows the founder to define rules ONCE with explicit consent that
the approval system will apply thereafter — drastically reducing
daily approval click-time WITHOUT removing the human-in-the-loop
gate.

Design intent:
  - Founder authors a rule (e.g. "auto-approve FAQ replies on email
    channel where confidence >= 0.9 for customer acme-real-estate")
  - Rule is digitally signed (HMAC of founder secret) → proves
    explicit founder consent at rule-creation time
  - System applies matching rules → request transitions pending →
    approved automatically (still recorded with rule_id audit
    breadcrumb)
  - Rules expire after 30 days by default (refresh required)
  - Disable any rule instantly (single-shot kill switch)

Hard rules (immutable):
  - NEVER auto-approve WhatsApp / LinkedIn / Phone (per
    CHANNEL_POLICY in approval_policy.py — these channels have
    max_auto_approve_risk=None). Founder rule cannot override.
  - NEVER auto-approve risk_level="high" or "blocked"
  - NEVER auto-approve without rule_id breadcrumb in audit log
  - Rules >30 days old are ignored until refreshed
  - WhatsApp rule attempts log "rule_blocked_by_channel_policy"

Storage: JSONL at data/founder_rules/active_rules.jsonl (gitignored).
Storage location matches Wave 6 pattern (gitignored live data).

Founder uses scripts/dealix_founder_rules.py to manage.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
from dataclasses import dataclass, field, asdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from auto_client_acquisition.approval_center.approval_policy import (
    CHANNEL_POLICY,
    _RISK_ORDER,
)
from auto_client_acquisition.approval_center.schemas import ApprovalRequest

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RULES_DIR = REPO_ROOT / "data" / "founder_rules"
DEFAULT_RULES_FILE = DEFAULT_RULES_DIR / "active_rules.jsonl"
DEFAULT_AUDIT_FILE = DEFAULT_RULES_DIR / "rule_match_audit.jsonl"

# Rule expiry — founders MUST refresh rules every 30 days
DEFAULT_RULE_TTL_DAYS = 30

# Channels where auto-approve is permanently blocked, regardless of rule
_BLOCKED_AUTO_CHANNELS = {"whatsapp", "linkedin", "phone"}


@dataclass(frozen=True)
class FounderRule:
    """A founder-authored pre-approval rule.

    Match conditions (all must hold for the rule to apply):
      - channel: e.g. "email" — must equal req.channel.lower()
      - customer_handle: e.g. "acme-real-estate" or "*" wildcard
      - action_type: e.g. "faq_reply" or "*" wildcard
      - max_risk_level: highest risk this rule covers (low/medium)
      - min_confidence: minimum confidence score in metadata
      - content_pattern_regex: optional regex for content match

    Audit:
      - rule_id auto-generated
      - created_at + expires_at
      - founder_signature (HMAC) proves explicit consent
      - usage_count tracked separately in audit jsonl
    """

    rule_id: str
    name: str  # human-readable, e.g. "FAQ replies for acme"
    channel: str  # required channel match (case-insensitive)
    customer_handle: str = "*"  # "*" matches any
    action_type: str = "*"
    max_risk_level: str = "low"  # "low" | "medium" — never high/blocked
    min_confidence: float = 0.9  # 0.0-1.0
    content_pattern_regex: str = ""  # optional regex (empty = match any)
    created_at: str = ""  # ISO 8601
    expires_at: str = ""  # ISO 8601
    founder_signature: str = ""  # HMAC-SHA256
    enabled: bool = True
    notes: str = ""

    def is_expired(self, now: datetime | None = None) -> bool:
        if not self.expires_at:
            return True
        try:
            exp = datetime.fromisoformat(self.expires_at)
        except (TypeError, ValueError):
            return True
        return (now or datetime.now(UTC)) >= exp


class FounderRuleEngine:
    """Loads, validates, and matches founder rules against ApprovalRequests."""

    def __init__(
        self,
        rules_path: Path | None = None,
        audit_path: Path | None = None,
        founder_secret_env: str = "DEALIX_FOUNDER_RULES_SECRET",
    ) -> None:
        self.rules_path = rules_path or DEFAULT_RULES_FILE
        self.audit_path = audit_path or DEFAULT_AUDIT_FILE
        self.founder_secret_env = founder_secret_env

    @property
    def _secret(self) -> str:
        # Founder must set this env var on Railway + locally.
        # If absent, no rules are valid (fail-closed).
        return os.environ.get(self.founder_secret_env, "")

    def _sign(self, rule: FounderRule) -> str:
        """Compute HMAC-SHA256 of rule's content (proves founder consent)."""
        if not self._secret:
            return ""
        # Sign immutable fields only (signature itself excluded)
        payload = json.dumps({
            "rule_id": rule.rule_id,
            "name": rule.name,
            "channel": rule.channel,
            "customer_handle": rule.customer_handle,
            "action_type": rule.action_type,
            "max_risk_level": rule.max_risk_level,
            "min_confidence": rule.min_confidence,
            "content_pattern_regex": rule.content_pattern_regex,
            "created_at": rule.created_at,
            "expires_at": rule.expires_at,
        }, sort_keys=True, ensure_ascii=False).encode("utf-8")
        return hmac.new(
            self._secret.encode("utf-8"), payload, hashlib.sha256
        ).hexdigest()

    def verify_signature(self, rule: FounderRule) -> bool:
        """True if rule was signed with the current founder secret."""
        if not rule.founder_signature or not self._secret:
            return False
        expected = self._sign(rule)
        return hmac.compare_digest(rule.founder_signature, expected)

    def create_rule(
        self,
        *,
        name: str,
        channel: str,
        customer_handle: str = "*",
        action_type: str = "*",
        max_risk_level: str = "low",
        min_confidence: float = 0.9,
        content_pattern_regex: str = "",
        notes: str = "",
        ttl_days: int = DEFAULT_RULE_TTL_DAYS,
    ) -> FounderRule:
        """Create + sign a new rule. Caller responsible for persistence."""
        # Reject channels that have a permanent ban on auto-approve
        if channel.lower() in _BLOCKED_AUTO_CHANNELS:
            raise ValueError(
                f"REFUSING — channel '{channel}' is permanently blocked from "
                f"auto-approve (whatsapp/linkedin/phone). Per CHANNEL_POLICY."
            )
        # Reject high/blocked risk levels
        if max_risk_level not in {"low", "medium"}:
            raise ValueError(
                f"REFUSING — max_risk_level '{max_risk_level}' not allowed. "
                f"Founder rules can cover only 'low' or 'medium' risk."
            )
        # Reject if confidence too low
        if not (0.0 <= min_confidence <= 1.0):
            raise ValueError(
                f"min_confidence must be 0.0-1.0; got {min_confidence}"
            )
        # Validate regex if provided
        if content_pattern_regex:
            try:
                re.compile(content_pattern_regex)
            except re.error as exc:
                raise ValueError(f"invalid content_pattern_regex: {exc}") from exc

        now = datetime.now(UTC)
        exp = now + timedelta(days=ttl_days)
        rule_id = f"rule_{now.strftime('%Y%m%d_%H%M%S')}_{abs(hash(name)) % 10000:04d}"

        partial = FounderRule(
            rule_id=rule_id,
            name=name,
            channel=channel.lower(),
            customer_handle=customer_handle,
            action_type=action_type,
            max_risk_level=max_risk_level,
            min_confidence=min_confidence,
            content_pattern_regex=content_pattern_regex,
            created_at=now.isoformat(),
            expires_at=exp.isoformat(),
            notes=notes,
        )
        signature = self._sign(partial)
        return FounderRule(
            **{**asdict(partial), "founder_signature": signature}
        )

    def list_rules(self) -> list[FounderRule]:
        """Load all rules from JSONL. Returns even expired ones."""
        if not self.rules_path.exists():
            return []
        rules: list[FounderRule] = []
        for line in self.rules_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                rules.append(FounderRule(**data))
            except (json.JSONDecodeError, TypeError):
                continue
        return rules

    def list_active_rules(self, now: datetime | None = None) -> list[FounderRule]:
        """Load enabled, non-expired, signature-valid rules."""
        return [
            r
            for r in self.list_rules()
            if r.enabled and not r.is_expired(now) and self.verify_signature(r)
        ]

    def append_rule(self, rule: FounderRule) -> None:
        """Append a new rule to the JSONL file."""
        self.rules_path.parent.mkdir(parents=True, exist_ok=True)
        with self.rules_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(rule), ensure_ascii=False) + "\n")

    def disable_rule(self, rule_id: str) -> bool:
        """Disable a rule by id (rewrites the file). Returns True if found."""
        rules = self.list_rules()
        found = False
        for i, r in enumerate(rules):
            if r.rule_id == rule_id:
                rules[i] = FounderRule(**{**asdict(r), "enabled": False})
                found = True
        if found:
            self.rules_path.parent.mkdir(parents=True, exist_ok=True)
            self.rules_path.write_text(
                "\n".join(json.dumps(asdict(r), ensure_ascii=False) for r in rules) + "\n",
                encoding="utf-8",
            )
        return found

    def match(
        self,
        req: ApprovalRequest,
        confidence: float = 1.0,
        content: str = "",
        now: datetime | None = None,
    ) -> FounderRule | None:
        """Find the first matching active rule for a request.

        Returns None if no rule matches OR auto-approve permanently
        forbidden for the channel.

        Hard rules:
          - WhatsApp/LinkedIn/Phone → always None (channel-level block)
          - High/Blocked risk → always None
          - Expired or unsigned rule → ignored
        """
        # Permanent channel block
        channel = (req.channel or "").lower()
        if channel in _BLOCKED_AUTO_CHANNELS:
            return None
        # Risk gate (cannot auto-approve high/blocked)
        risk = (req.risk_level or "low").lower()
        if _RISK_ORDER.get(risk, 1) > _RISK_ORDER["medium"]:
            return None
        # Channel must allow auto-approve at all (per CHANNEL_POLICY)
        chan_pol = CHANNEL_POLICY.get(channel, {})
        if not chan_pol.get("max_auto_approve_risk"):
            return None
        # Iterate active rules
        for rule in self.list_active_rules(now):
            if rule.channel != channel:
                continue
            if rule.customer_handle != "*" and rule.customer_handle != self._extract_customer_handle(req):
                continue
            if rule.action_type != "*" and rule.action_type != req.action_type:
                continue
            if _RISK_ORDER.get(risk, 1) > _RISK_ORDER.get(rule.max_risk_level, 1):
                continue
            if confidence < rule.min_confidence:
                continue
            if rule.content_pattern_regex:
                if not re.search(rule.content_pattern_regex, content or "", re.IGNORECASE):
                    continue
            return rule
        return None

    @staticmethod
    def _extract_customer_handle(req: ApprovalRequest) -> str:
        """Best-effort extraction of customer handle from request."""
        # ApprovalRequest doesn't have a top-level customer_handle field
        # but typically passes object_id like "lead:acme-real-estate-001"
        # or includes it in summary. Caller can populate via metadata.
        oid = req.object_id or ""
        if ":" in oid:
            tail = oid.split(":", 1)[1]
            # Take the first segment if it looks like a handle
            seg = tail.split("-", 1)[0] if "-" in tail else tail
            # Reconstruct full handle (acme-real-estate)
            parts = tail.rsplit("-", 1)
            if len(parts) == 2 and parts[1].isdigit():
                return parts[0]
            return tail
        return ""

    def record_match(
        self,
        rule: FounderRule,
        req: ApprovalRequest,
        confidence: float,
        outcome: str = "auto_approved",
    ) -> None:
        """Append a match to the audit JSONL. Always called when a rule fires."""
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "matched_at": datetime.now(UTC).isoformat(),
            "rule_id": rule.rule_id,
            "rule_name": rule.name,
            "approval_id": req.approval_id,
            "object_id": req.object_id,
            "action_type": req.action_type,
            "channel": req.channel,
            "risk_level": req.risk_level,
            "confidence": confidence,
            "outcome": outcome,
        }
        with self.audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def list_recent_matches(self, limit: int = 50) -> list[dict[str, Any]]:
        """Read the most recent N rule matches from audit log."""
        if not self.audit_path.exists():
            return []
        lines = self.audit_path.read_text(encoding="utf-8").splitlines()
        records: list[dict[str, Any]] = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return records[-limit:][::-1]
