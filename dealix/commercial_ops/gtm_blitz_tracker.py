"""GTM Blitz 90d progress vs targets in gtm_blitz_90d.yaml."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.evidence_csv import count_evidence_events
from dealix.commercial_ops.paths import REPO_ROOT

GTM_BLITZ = REPO_ROOT / "dealix/config/gtm_blitz_90d.yaml"
ICP_CSV = REPO_ROOT / "docs/commercial/operations/targeting/agency_accounts_seed.csv"
CONV_CSV = REPO_ROOT / "docs/commercial/operations/gtm_conversation_tracker.csv"


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _count_csv_rows(path: Path, *, min_filled_company: bool = False) -> int:
    if not path.is_file():
        return 0
    n = 0
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if min_filled_company:
                company = (row.get("company") or row.get("company_name") or "").strip()
                if not company or company.lower().startswith("template"):
                    continue
            n += 1
    return n


def build_gtm_blitz_snapshot() -> dict[str, Any]:
    cfg = _load_yaml(GTM_BLITZ)
    targets = cfg.get("targets") or {}
    evidence = count_evidence_events(exclude_placeholders=True)
    by_type = evidence.get("all_time_by_type") or evidence.get("by_type") or {}
    paid = by_type.get("payment_received", 0)
    proof = by_type.get("proof_pack_delivered", 0)
    icp_rows = _count_csv_rows(ICP_CSV, min_filled_company=True)
    conv_rows = _count_csv_rows(CONV_CSV, min_filled_company=True)

    checks = {
        "icp_accounts_min": icp_rows >= int(targets.get("icp_accounts_min", 75)),
        "paid_diagnostics": paid >= int(targets.get("paid_diagnostics", 1)),
        "proof_packs_delivered": proof >= int(targets.get("proof_packs_delivered", 1)),
        "qualified_conversations": conv_rows >= int(targets.get("qualified_conversations", 30)),
    }
    done = sum(1 for v in checks.values() if v)
    total = len(checks) or 1
    pct = round(100 * done / total)

    return {
        "motion": cfg.get("motion"),
        "window": {"start": cfg.get("start_iso"), "end": cfg.get("end_iso")},
        "targets": targets,
        "actuals": {
            "icp_filled_rows": icp_rows,
            "conversation_rows": conv_rows,
            "payment_received": paid,
            "proof_pack_delivered": proof,
        },
        "checks": checks,
        "pct": pct,
        "verdict": "PASS" if all(checks.values()) else "IN_PROGRESS",
    }
