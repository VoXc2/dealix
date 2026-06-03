#!/usr/bin/env python3
"""Smoke checks for AI output / draft guardrails (deterministic)."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))

    from auto_client_acquisition.governance_os.draft_gate import audit_draft_text
    from auto_client_acquisition.governance_os.forbidden_actions import is_channel_forbidden

    bad = audit_draft_text("We will do cold whatsapp blasting for leads")
    if not bad:
        print("expected_audit_issues", file=sys.stderr)
        return 1
    if not is_channel_forbidden("plan: cold whatsapp to everyone"):
        print("expected_channel_forbidden", file=sys.stderr)
        return 1
    print("AI_OUTPUT_QUALITY_PASS=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
