#!/usr/bin/env python3
"""Shared helpers for Dealix report generators (stdlib only)."""

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
REPORTS = REPO / "reports"

SA_TZ = timezone(timedelta(hours=3))  # Saudi time (AST)

SYSTEM_AR = {
    "revenue_os": "Revenue OS — نظام تشغيل الإيرادات",
    "executive_command_os": "Executive Command OS — نظام القيادة التنفيذية",
    "followup_recovery_os": "Follow-up Recovery OS — نظام استرجاع المتابعات",
    "whatsapp_client_os": "WhatsApp Client OS — نظام عملاء واتساب",
    "proposal_proof_os": "Proposal & Proof OS — نظام العروض والإثبات",
}

SYSTEM_SHORT = {
    "revenue_os": "Revenue OS",
    "executive_command_os": "Executive Command OS",
    "followup_recovery_os": "Follow-up Recovery OS",
    "whatsapp_client_os": "WhatsApp Client OS",
    "proposal_proof_os": "Proposal & Proof OS",
}

TOP_QUALITY_THRESHOLD = 75  # Draft Quality Score floor for Top 100


def now_ast():
    return datetime.now(SA_TZ).strftime("%Y-%m-%d %H:%M")


def load_jsonl(rel):
    path = REPO / rel
    rows = []
    if not path.exists():
        return rows
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_report(rel, content):
    path = REPORTS / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote reports/{rel}")
    return path


def md_cell(text):
    """Make a value safe for a one-line markdown table cell."""
    if text is None:
        return ""
    s = str(text).replace("\n", " ").replace("|", "\\|")
    return s.strip()
