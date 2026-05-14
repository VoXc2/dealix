#!/usr/bin/env python3
"""Gate: documentation governance files exist and hub links are present.

Exit 0 = PASS, 1 = FAIL.

Run: py -3 scripts/validate_docs_governance.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED_MD = (
    "docs/strategic/HOLDING_DOCS_HUB_AR.md",
    "docs/strategic/DOCS_CANONICAL_REGISTRY_AR.md",
    "docs/strategic/HOLDING_VALUE_REGISTRY_AR.md",
    "docs/strategic/DOCS_ARCHIVE_POLICY_AR.md",
    "docs/strategic/DOCS_ASSET_LIFECYCLE_AR.md",
    "docs/strategic/DOCS_REVIEW_CADENCE_AR.md",
    "docs/strategic/DOCS_READING_PACKS_AR.md",
    "docs/strategic/DOCS_PUBLICATION_BOUNDARY_AR.md",
    "docs/strategic/EXTERNAL_PACK_REGISTRY_AR.md",
    "docs/strategic/ARCHIVE_REVIEW_QUEUE_AR.md",
    "docs/strategic/DOCS_DECISION_RULES_AR.md",
    "docs/strategic/ASSET_USAGE_GOVERNANCE_AR.md",
    "docs/strategic/ASSET_EVIDENCE_LEVELS_AR.md",
    "docs/strategic/OS_ASSET_OPERATING_MODEL_AR.md",
    "docs/strategic/MARKET_SIGNAL_OPERATING_LOOP_AR.md",
    "docs/strategic/FOUNDER_SIGNAL_ROADMAP_AR.md",
    "docs/strategic/FULL_MARKET_PROOF_RUN_AR.md",
    "docs/strategic/MONTHLY_ASSET_COUNCIL_AR.md",
    "docs/strategic/QUARTERLY_PRUNING_POLICY_AR.md",
    "docs/strategic/packs/PARTNER_READING_PACK_AR.md",
    "docs/strategic/packs/INVESTOR_READING_PACK_AR.md",
    "docs/strategic/packs/OPERATOR_READING_PACK_AR.md",
    "docs/strategic/packs/PARTNER_MOTION_PACK_AR.md",
    "docs/strategic/packs/INVESTOR_MOTION_PACK_AR.md",
    "docs/strategic/packs/CLIENT_DEMO_PACK_AR.md",
)

HUB_SUBSTRINGS = (
    "DOCS_CANONICAL_REGISTRY_AR.md",
    "HOLDING_VALUE_REGISTRY_AR.md",
    "DOCS_ARCHIVE_POLICY_AR.md",
    "EXTERNAL_PACK_REGISTRY_AR.md",
    "ARCHIVE_REVIEW_QUEUE_AR.md",
    "DOCS_DECISION_RULES_AR.md",
    "ASSET_USAGE_GOVERNANCE_AR.md",
    "ASSET_EVIDENCE_LEVELS_AR.md",
    "تشغيل الأصول القابضة",
    "PARTNER_MOTION_PACK_AR.md",
    "INVESTOR_MOTION_PACK_AR.md",
    "CLIENT_DEMO_PACK_AR.md",
    "OS_ASSET_OPERATING_MODEL_AR.md",
    "MARKET_SIGNAL_OPERATING_LOOP_AR.md",
    "FOUNDER_SIGNAL_ROADMAP_AR.md",
    "FULL_MARKET_PROOF_RUN_AR.md",
)

SNAPSHOT = "docs/strategic/_generated/docs_top_level_snapshot.json"
SUMMARY = "docs/strategic/_generated/holding_value_summary.json"
PRIORITIES = "docs/strategic/_generated/asset_activation_priorities.json"
EVIDENCE_SUMMARY = "docs/strategic/_generated/asset_evidence_summary.json"
CAPITAL_ALLOCATION = "docs/strategic/_generated/asset_capital_allocation.json"
USAGE_LOG = "data/docs_asset_usage_log.json"

FULL_MARKET_PROOF_RUN_REL = "docs/strategic/FULL_MARKET_PROOF_RUN_AR.md"

# Minimal spine markers — not full-text coverage; prevents accidental truncation.
COMMAND_CENTER_MARKERS = (
    "founder-signal-war-room",
    "Founder Signal War Room",
    "قفل الصدق",
    "follow_up_sent",
    "no_response_after_follow_up",
    "PARTNER-002",
    "No build",
)


def audit_command_center_markers(content: str) -> list[str]:
    """Ensure Command Center doc still carries War Room + L4 + outcomes + build gate."""
    errors: list[str] = []
    for marker in COMMAND_CENTER_MARKERS:
        if marker not in content:
            errors.append(
                f"{FULL_MARKET_PROOF_RUN_REL} missing marker {marker!r}",
            )
    return errors


def _entry_evidence_level_n(entry: object) -> int | None:
    if not isinstance(entry, dict):
        return None
    raw = entry.get("evidence_level_after_use")
    if raw is None:
        return None
    m = re.match(r"^L(\d+)$", str(raw).strip().upper())
    if not m:
        return None
    return int(m.group(1))


def audit_usage_log_entries(entries: object) -> list[str]:
    """L4+ rows must be auditable: real external use, founder_confirmed true."""
    errors: list[str] = []
    if not isinstance(entries, list):
        return ["entries must be a list"]
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entries[{i}] must be an object")
            continue
        n = _entry_evidence_level_n(entry)
        if n is None or n < 4:
            continue
        prefix = f"entries[{i}] (asset={entry.get('asset')!r})"
        if not str(entry.get("date", "")).strip():
            errors.append(f"{prefix}: L4+ requires non-empty date")
        if not str(entry.get("channel", "")).strip():
            errors.append(f"{prefix}: L4+ requires non-empty channel")
        if not str(entry.get("outcome", "")).strip():
            errors.append(f"{prefix}: L4+ requires non-empty outcome")
        aud = str(entry.get("audience", "")).strip()
        aid = str(entry.get("audience_id", "")).strip()
        if not aud and not aid:
            errors.append(f"{prefix}: L4+ requires audience or audience_id")
        if entry.get("founder_confirmed") is not True:
            errors.append(f"{prefix}: L4+ requires founder_confirmed true (else lower evidence / simulation)")
    return errors


def main() -> int:
    failed = False
    for rel in REQUIRED_MD:
        p = REPO / rel
        if not p.is_file():
            print(f"FAIL: missing {rel}", file=sys.stderr)
            failed = True
    if failed:
        return 1

    hub = (REPO / "docs/strategic/HOLDING_DOCS_HUB_AR.md").read_text(encoding="utf-8")
    for sub in HUB_SUBSTRINGS:
        if sub not in hub:
            print(f"FAIL: HOLDING_DOCS_HUB_AR.md must reference {sub}", file=sys.stderr)
            failed = True
    if failed:
        return 1

    fm_text = (REPO / FULL_MARKET_PROOF_RUN_REL).read_text(encoding="utf-8")
    for err in audit_command_center_markers(fm_text):
        print(f"FAIL: {err}", file=sys.stderr)
        failed = True
    if failed:
        return 1

    snap_path = REPO / SNAPSHOT
    if not snap_path.is_file():
        print(f"FAIL: missing {SNAPSHOT}", file=sys.stderr)
        return 1
    data = json.loads(snap_path.read_text(encoding="utf-8"))
    count = int(data.get("docs_top_level_dir_count", 0))
    if count < 80:
        print(f"FAIL: docs_top_level_dir_count {count} < 80", file=sys.stderr)
        return 1

    sum_path = REPO / SUMMARY
    if not sum_path.is_file():
        print(f"FAIL: missing {SUMMARY} (run scripts/generate_holding_value_summary.py)", file=sys.stderr)
        return 1
    summary = json.loads(sum_path.read_text(encoding="utf-8"))
    if summary.get("asset_count", 0) < 5:
        print("FAIL: holding_value_summary asset_count too low", file=sys.stderr)
        return 1
    for key in (
        "top_revenue_assets",
        "top_trust_assets",
        "top_partner_assets",
        "top_investor_assets",
        "top_holding_assets",
        "recommended_for_partner_pack",
        "recommended_for_investor_pack",
        "recommended_for_client_pack",
        "archive_review_candidates",
        "missing_boundary_candidates",
        "assets_missing_status",
        "assets_missing_publication_boundary",
        "assets_recommended_for_partner_pack",
        "assets_recommended_for_archive_review",
    ):
        if key not in summary:
            print(f"FAIL: holding_value_summary.json missing key {key!r}", file=sys.stderr)
            return 1
        if not isinstance(summary[key], list):
            print(f"FAIL: holding_value_summary[{key!r}] must be a list", file=sys.stderr)
            return 1

    pri_path = REPO / PRIORITIES
    if not pri_path.is_file():
        print(
            f"FAIL: missing {PRIORITIES} (run scripts/generate_holding_value_summary.py)",
            file=sys.stderr,
        )
        return 1
    pri = json.loads(pri_path.read_text(encoding="utf-8"))
    for key in ("activation_priorities", "governance_risks", "archive_candidates"):
        if key not in pri:
            print(f"FAIL: asset_activation_priorities.json missing key {key!r}", file=sys.stderr)
            return 1
        if not isinstance(pri[key], list):
            print(f"FAIL: asset_activation_priorities[{key!r}] must be a list", file=sys.stderr)
            return 1

    ev_path = REPO / EVIDENCE_SUMMARY
    if not ev_path.is_file():
        print(
            f"FAIL: missing {EVIDENCE_SUMMARY} (run scripts/generate_holding_value_summary.py)",
            file=sys.stderr,
        )
        return 1
    ev = json.loads(ev_path.read_text(encoding="utf-8"))
    for key in ("counts_by_level", "assets_by_level"):
        if key not in ev:
            print(f"FAIL: asset_evidence_summary.json missing key {key!r}", file=sys.stderr)
            return 1
    if not isinstance(ev["counts_by_level"], dict):
        print("FAIL: asset_evidence_summary counts_by_level must be dict", file=sys.stderr)
        return 1
    if not isinstance(ev["assets_by_level"], dict):
        print("FAIL: asset_evidence_summary assets_by_level must be dict", file=sys.stderr)
        return 1

    cap_path = REPO / CAPITAL_ALLOCATION
    if not cap_path.is_file():
        print(
            f"FAIL: missing {CAPITAL_ALLOCATION} (run scripts/generate_holding_value_summary.py)",
            file=sys.stderr,
        )
        return 1
    cap = json.loads(cap_path.read_text(encoding="utf-8"))
    for key in ("invest", "activate", "maintain", "archive_review"):
        if key not in cap:
            print(f"FAIL: asset_capital_allocation.json missing key {key!r}", file=sys.stderr)
            return 1
        if not isinstance(cap[key], list):
            print(f"FAIL: asset_capital_allocation[{key!r}] must be list", file=sys.stderr)
            return 1

    log_path = REPO / USAGE_LOG
    if not log_path.is_file():
        print(f"FAIL: missing {USAGE_LOG}", file=sys.stderr)
        return 1
    log_data = json.loads(log_path.read_text(encoding="utf-8"))
    uerrs = audit_usage_log_entries(log_data.get("entries"))
    if uerrs:
        for err in uerrs:
            print(f"FAIL: usage log — {err}", file=sys.stderr)
        return 1

    print("Docs governance gate: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
