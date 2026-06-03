#!/usr/bin/env python3
"""
Dealix Safety Gate
==================

Report-only, dry-run enforcement of Dealix outbound + commercial trust rules.

This gate NEVER sends anything. It inspects drafts and the approval queue and
returns violations. It is importable (so tests can call the checks directly)
and runnable as a CLI that exits non-zero when blocking violations exist.

Hard rules enforced (see company_os/security/OUTBOUND_SAFETY_POLICY.md):
  - No guaranteed revenue / ROI claims (Arabic + English).
  - No misleading subject lines (fake Re:/Fwd: on cold first-touch).
  - No contacting a suppressed recipient.
  - Every outbound item requires approval and must not be pre-approved by AI.
  - Pricing / payment / contract items are high-risk and require approval.
  - No API keys / secrets requested over WhatsApp.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# --- Forbidden guarantee / overclaim patterns (Arabic + English) -------------
GUARANTEE_PATTERNS = [
    r"نضمن\s*(?:لك)?\s*(?:زيادة|مضاعفة|نتائج|المبيعات|الأرباح|الإيراد)",
    r"نتائج\s+مضمونة",
    r"مضمون(?:ة)?\s+(?:النتائج|الأرباح|الزيادة)",
    r"نضاعف\s+(?:مبيعاتك|إيراداتك|أرباحك)",
    r"\bguarantee(?:d)?\s+(?:revenue|results|sales|roi|growth)",
    r"\b10x\b",
    r"\bdouble\s+your\s+(?:revenue|sales|leads)\b",
    r"\brisk[-\s]?free\b",
]

# Subjects that fake a prior thread on a cold first-touch.
FAKE_REPLY_PATTERNS = [r"^\s*re\s*:", r"^\s*fwd\s*:", r"^\s*رد\s*:", r"^\s*تحويل\s*:"]

# Requests for secrets / API keys (must go through the secure portal, never chat).
SECRET_REQUEST_PATTERNS = [
    r"api[\s_-]?key",
    r"secret[\s_-]?key",
    r"access[\s_-]?token",
    r"كلمة\s+المرور",
    r"مفتاح\s+api",
    r"رمز\s+الدخول",
]

SENSITIVE_APPROVAL_TYPES = {"pricing_offer", "payment_handoff", "contract"}


def _load_json(path: Path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def find_guarantee_claims(text: str) -> list[str]:
    """Return the guarantee/overclaim phrases found in `text`."""
    if not text:
        return []
    hits = []
    for pat in GUARANTEE_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            hits.append(pat)
    return hits


def is_fake_reply_subject(subject: str) -> bool:
    """True if a cold subject fakes a reply/forward thread."""
    if not subject:
        return False
    return any(re.search(p, subject, flags=re.IGNORECASE) for p in FAKE_REPLY_PATTERNS)


def requests_secret(text: str) -> bool:
    """True if `text` asks for an API key / secret over a chat channel."""
    if not text:
        return False
    return any(re.search(p, text, flags=re.IGNORECASE) for p in SECRET_REQUEST_PATTERNS)


def load_suppression(path: Path) -> set[str]:
    data = _load_json(path, {"entries": []})
    return {e.get("company", "").strip().lower() for e in data.get("entries", [])}


def check_outbound_items(items: list[dict], suppressed: set[str]) -> list[dict]:
    """Run all outbound safety checks. Returns a list of finding dicts."""
    findings: list[dict] = []

    def add(rule, severity, item, detail):
        findings.append(
            {
                "rule": rule,
                "severity": severity,
                "item_id": item.get("id"),
                "company": item.get("company"),
                "detail": detail,
            }
        )

    for item in items:
        itype = item.get("type", "")
        body = " ".join(
            str(item.get(k, "")) for k in ("draft_subject", "draft_body", "details")
        )
        subject = str(item.get("draft_subject", ""))

        # Only message-like items carry copy to scan.
        is_message = itype in {"outreach_message", "follow_up", "reply", "proposal_intro", "partner_intro"}

        if is_message:
            for hit in find_guarantee_claims(body):
                add("OUT-GUARANTEE", "CRITICAL", item, f"Guaranteed-claim pattern matched: {hit!r}")
            if is_fake_reply_subject(subject):
                add("OUT-FAKE-REPLY", "CRITICAL", item, f"Misleading reply/forward subject: {subject!r}")
            if requests_secret(body):
                add("OUT-SECRET-REQUEST", "CRITICAL", item, "Outbound copy requests a secret/API key over chat")
            if item.get("channel") == "whatsapp_after_consent" and not item.get("consent", False):
                add("WA-CONSENT", "CRITICAL", item, "WhatsApp message without recorded consent")

        # Suppression applies to every outbound item.
        if item.get("company", "").strip().lower() in suppressed:
            add("OUT-SUPPRESSED", "CRITICAL", item, "Recipient is on the suppression list")

        # Approval discipline.
        if is_message or itype in SENSITIVE_APPROVAL_TYPES:
            if item.get("requires_approval") is not True:
                add("OUT-NO-APPROVAL-FLAG", "CRITICAL", item, "Outbound/sensitive item missing requires_approval=true")
            # AI must never mark these approved; only a human reviewer may.
            if item.get("approved") is True and not item.get("reviewed_by"):
                add("OUT-AUTO-APPROVED", "CRITICAL", item, "Item approved without a human reviewer")

        if itype in SENSITIVE_APPROVAL_TYPES and item.get("risk") != "high":
            add("OUT-RISK-LEVEL", "HIGH", item, f"{itype} must be risk=high")

    return findings


def run(base_dir: Path) -> int:
    queue = _load_json(base_dir / "company_os" / "governance" / "approval_queue.json", [])
    suppressed = load_suppression(base_dir / "company_os" / "governance" / "suppression_list.json")

    # Optional dedicated drafts file (not required to exist).
    drafts = _load_json(base_dir / "company_os" / "revenue" / "outreach_queue.json", [])
    if isinstance(drafts, dict):
        drafts = drafts.get("drafts", []) or drafts.get("queue", [])

    items = [i for i in queue if isinstance(i, dict)] + [d for d in drafts if isinstance(d, dict)]
    findings = check_outbound_items(items, suppressed)

    critical = [f for f in findings if f["severity"] == "CRITICAL"]
    high = [f for f in findings if f["severity"] == "HIGH"]

    print("=" * 78)
    print("  DEALIX SAFETY GATE — dry-run, report-only (no sends)")
    print("=" * 78)
    print(f"  Inspected: {len(items)} outbound/approval items, {len(suppressed)} suppressed")
    print(f"  Findings: {len(critical)} critical, {len(high)} high")
    print()
    for f in critical + high:
        flag = "CRITICAL" if f["severity"] == "CRITICAL" else "HIGH"
        print(f"  [{flag}] [{f['rule']}] {f.get('company')}: {f['detail']}")
    if not findings:
        print("  ✅ No safety violations found. (Drafts still require human approval to send.)")
    print()
    print("=" * 78)
    return 1 if critical else 0


if __name__ == "__main__":
    sys.exit(run(Path(__file__).resolve().parent.parent))
