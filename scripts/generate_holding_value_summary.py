#!/usr/bin/env python3
"""Parse HOLDING_VALUE_REGISTRY_AR.md and emit ranked summary + activation priorities.

Outputs:
- docs/strategic/_generated/holding_value_summary.json
- docs/strategic/_generated/asset_activation_priorities.json
- docs/strategic/_generated/asset_evidence_summary.json
- docs/strategic/_generated/asset_capital_allocation.json

Run: py -3 scripts/generate_holding_value_summary.py
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "docs" / "strategic" / "HOLDING_VALUE_REGISTRY_AR.md"
OUT = REPO / "docs" / "strategic" / "_generated" / "holding_value_summary.json"
PRIORITIES_OUT = REPO / "docs" / "strategic" / "_generated" / "asset_activation_priorities.json"
EVIDENCE_SUMMARY_OUT = REPO / "docs" / "strategic" / "_generated" / "asset_evidence_summary.json"
CAPITAL_ALLOCATION_OUT = REPO / "docs" / "strategic" / "_generated" / "asset_capital_allocation.json"


def _evidence_to_int(level: str) -> int:
    s = str(level).strip().upper()
    m = re.match(r"^L(\d+)$", s)
    if m:
        return int(m.group(1))
    return 0


def _evidence_bucket_label(level: str) -> str:
    n = _evidence_to_int(level)
    return f"L{max(0, min(n, 7))}"


def _evidence_summary_payload(
    rows: list[dict[str, object]],
    ts: str,
    src: str,
) -> dict[str, object]:
    buckets: dict[str, list[dict[str, object]]] = {f"L{i}": [] for i in range(8)}
    for r in rows:
        key = _evidence_bucket_label(str(r.get("evidence_level", "L0")))
        buckets[key].append(
            {
                "asset": r["asset"],
                "holding": int(r["holding"]),
                "last_used": str(r.get("last_used", "")),
            },
        )
    return {
        "generated_at_utc": ts,
        "source": src,
        "counts_by_level": {k: len(v) for k, v in buckets.items()},
        "assets_by_level": buckets,
    }


def _capital_allocation_payload(
    rows: list[dict[str, object]],
    ts: str,
    src: str,
) -> dict[str, object]:
    """2x2: value = max(rev,par,inv,hold) >= 4; evidence high = L5+."""
    invest: list[dict[str, object]] = []
    activate: list[dict[str, object]] = []
    maintain: list[dict[str, object]] = []
    archive_review: list[dict[str, object]] = []
    for r in rows:
        evn = _evidence_to_int(str(r.get("evidence_level", "L0")))
        mx = max(int(r["revenue"]), int(r["partner"]), int(r["investor"]), int(r["holding"]))
        hi_val = mx >= 4
        hi_evi = evn >= 5
        item: dict[str, object] = {
            "asset": r["asset"],
            "max_value_score": mx,
            "evidence_level": str(r.get("evidence_level", "L0")),
        }
        if hi_val and hi_evi:
            invest.append(item)
        elif hi_val and not hi_evi:
            activate.append(item)
        elif (not hi_val) and hi_evi:
            maintain.append(item)
        else:
            archive_review.append(item)
    return {
        "generated_at_utc": ts,
        "source": src,
        "method": "Quadrant: high_value=max(revenue,partner,investor,holding)>=4; high_evidence=L5+",
        "invest": invest,
        "activate": activate,
        "maintain": maintain,
        "archive_review": archive_review,
    }


def _parse_table(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    rows: list[dict[str, object]] = []
    expects_extended = False
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if "| الأصل |" in stripped and "Revenue" in stripped:
            in_table = True
            expects_extended = "EvidenceLevel" in stripped
            continue
        if not in_table:
            continue
        if stripped.startswith("|--") or stripped.startswith("| -"):
            continue
        if not stripped.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in stripped.split("|")[1:-1]]
        if len(cells) < 9:
            continue
        try:
            rec: dict[str, object] = {
                "asset": cells[0],
                "type": cells[1],
                "revenue": int(cells[2]),
                "trust": int(cells[3]),
                "delivery": int(cells[4]),
                "partner": int(cells[5]),
                "investor": int(cells[6]),
                "holding": int(cells[7]),
                "status": cells[8],
            }
            if expects_extended and len(cells) >= 17:
                rec["owner"] = cells[9]
                rec["review_cadence"] = cells[10]
                rec["audience"] = cells[11]
                rec["publication_boundary"] = cells[12]
                rec["last_used"] = cells[13]
                rec["evidence_level"] = cells[14]
                rec["usage_count"] = int(cells[15])
                rec["next_action"] = cells[16]
            elif len(cells) >= 14:
                rec["owner"] = cells[9]
                rec["review_cadence"] = cells[10]
                rec["audience"] = cells[11]
                rec["publication_boundary"] = cells[12]
                rec["last_used"] = cells[13] if len(cells) > 13 else "TBD"
                rec["evidence_level"] = "L2"
                rec["usage_count"] = 0
                rec["next_action"] = ""
            else:
                rec["owner"] = ""
                rec["review_cadence"] = ""
                rec["audience"] = ""
                rec["publication_boundary"] = ""
                rec["last_used"] = ""
                rec["evidence_level"] = "L0"
                rec["usage_count"] = 0
                rec["next_action"] = ""
        except ValueError:
            continue
        rows.append(rec)
    return rows


def _top(rows: list[dict[str, object]], key: str, limit: int = 10) -> list[dict[str, object]]:
    sorted_rows = sorted(rows, key=lambda r: int(r[key]), reverse=True)
    return sorted_rows[:limit]


def _missing_boundary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for r in rows:
        b = str(r.get("publication_boundary", "")).strip()
        if not b or b in {"—", "TBD", "N/A"}:
            out.append({"asset": r["asset"], "reason": "publication_boundary missing or placeholder"})
    return out


def _missing_boundary_asset_names(missing: list[dict[str, object]]) -> list[str]:
    return [str(x["asset"]) for x in missing]


def _missing_status(rows: list[dict[str, object]]) -> list[str]:
    return [str(r["asset"]) for r in rows if not str(r.get("status", "")).strip()]


def _recommend_partner_pack(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    recs: list[dict[str, object]] = []
    for r in rows:
        pub = str(r.get("publication_boundary", "")).strip()
        if int(r["partner"]) >= 4 and pub == "Partner-safe":
            recs.append(
                {
                    "asset": r["asset"],
                    "reason": "Partner >= 4 + Partner-safe boundary",
                },
            )
    return recs


def _recommend_investor_pack(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    recs: list[dict[str, object]] = []
    for r in rows:
        pub = str(r.get("publication_boundary", "")).strip()
        if int(r["investor"]) >= 4 and pub == "Investor-safe":
            recs.append(
                {
                    "asset": r["asset"],
                    "reason": "Investor >= 4 + Investor-safe boundary",
                },
            )
    return recs


def _recommend_client_pack(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    recs: list[dict[str, object]] = []
    for r in rows:
        pub = str(r.get("publication_boundary", "")).strip()
        if int(r["revenue"]) >= 4 and pub == "Client-facing":
            recs.append(
                {
                    "asset": r["asset"],
                    "reason": "Revenue >= 4 + Client-facing boundary",
                },
            )
    return recs


def _archive_review_candidates(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    recs: list[dict[str, object]] = []
    for r in rows:
        st = str(r["status"]).upper()
        if st == "CANONICAL":
            continue
        if int(r["holding"]) <= 2:
            recs.append(
                {
                    "asset": r["asset"],
                    "reason": "Holding <= 2 and not CANONICAL; queue archive review",
                },
            )
    return recs


def _activation_priorities(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """High score + low evidence (L0–L2) -> activate."""
    out: list[dict[str, object]] = []
    for r in rows:
        ev = _evidence_to_int(str(r.get("evidence_level", "L0")))
        hi = max(int(r["revenue"]), int(r["partner"]), int(r["investor"]), int(r["holding"]))
        if hi >= 4 and ev <= 2:
            na = str(r.get("next_action", "")).strip() or "Run motion pack + log usage"
            out.append(
                {
                    "asset": r["asset"],
                    "reason": "High value scores but low evidence (L0–L2); needs market activation",
                    "recommended_action": na,
                },
            )
    return out


def _governance_risks(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    risks: list[dict[str, object]] = []
    for r in rows:
        pub = str(r.get("publication_boundary", "")).strip()
        par, inv, rev = int(r["partner"]), int(r["investor"]), int(r["revenue"])
        if not pub or pub in {"—", "TBD", "N/A"}:
            if max(par, inv, rev) >= 3:
                risks.append(
                    {
                        "asset": r["asset"],
                        "reason": "Meaningful external-facing scores but missing publication boundary",
                    },
                )
            continue
        if pub == "Internal-only" and (par >= 4 or inv >= 4):
            risks.append(
                {
                    "asset": r["asset"],
                    "reason": "High partner/investor scores but Internal-only boundary; review before external motion",
                },
            )
    return risks


def main() -> int:
    if not REGISTRY.is_file():
        print(f"Missing {REGISTRY.relative_to(REPO)}", file=sys.stderr)
        return 1
    rows = _parse_table(REGISTRY)
    if not rows:
        print("No scoring rows parsed from registry.", file=sys.stderr)
        return 1

    top_rev = _top(rows, "revenue")
    top_trust = _top(rows, "trust")
    top_del = _top(rows, "delivery")
    top_par = _top(rows, "partner")
    top_inv = _top(rows, "investor")
    top_hold = _top(rows, "holding")

    missing_b = _missing_boundary(rows)
    partner_recs = _recommend_partner_pack(rows)
    investor_recs = _recommend_investor_pack(rows)
    client_recs = _recommend_client_pack(rows)
    archive_recs = _archive_review_candidates(rows)
    activation = _activation_priorities(rows)
    gov_risks = _governance_risks(rows)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    src = str(REGISTRY.relative_to(REPO)).replace("\\", "/")

    payload = {
        "generated_at_utc": ts,
        "source": src,
        "asset_count": len(rows),
        "top_by_revenue": top_rev,
        "top_by_trust": top_trust,
        "top_by_delivery": top_del,
        "top_by_partner": top_par,
        "top_by_investor": top_inv,
        "top_by_holding": top_hold,
        "top_revenue_assets": top_rev,
        "top_trust_assets": top_trust,
        "top_partner_assets": top_par,
        "top_investor_assets": top_inv,
        "top_holding_assets": top_hold,
        "recommended_for_partner_pack": partner_recs,
        "recommended_for_investor_pack": investor_recs,
        "recommended_for_client_pack": client_recs,
        "archive_review_candidates": archive_recs,
        "missing_boundary_candidates": missing_b,
        "assets_missing_status": _missing_status(rows),
        "assets_missing_publication_boundary": _missing_boundary_asset_names(missing_b),
        "assets_recommended_for_partner_pack": partner_recs,
        "assets_recommended_for_archive_review": archive_recs,
        "all_assets": rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    priorities_payload = {
        "generated_at_utc": ts,
        "source": src,
        "activation_priorities": activation,
        "governance_risks": gov_risks,
        "archive_candidates": list(archive_recs),
    }
    PRIORITIES_OUT.write_text(
        json.dumps(priorities_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    evidence_payload = _evidence_summary_payload(rows, ts, src)
    EVIDENCE_SUMMARY_OUT.write_text(
        json.dumps(evidence_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    capital_payload = _capital_allocation_payload(rows, ts, src)
    CAPITAL_ALLOCATION_OUT.write_text(
        json.dumps(capital_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {OUT.relative_to(REPO)} ({len(rows)} assets)")
    print(f"Wrote {PRIORITIES_OUT.relative_to(REPO)}")
    print(f"Wrote {EVIDENCE_SUMMARY_OUT.relative_to(REPO)}")
    print(f"Wrote {CAPITAL_ALLOCATION_OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
