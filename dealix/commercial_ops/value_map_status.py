"""Consolidated commercial value-map status (docs + pipeline + artifacts)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.paths import (
    FOUNDER_BRIEFS_DIR,
    REPO_ROOT,
    WAR_ROOM_TODAY_JSON,
    display_path,
)
from dealix.commercial_ops.value_map_catalog import get_value_map_catalog

# Do not route founder decisions through the historical COMMERCIAL_VALUE_MAP_AR
# price/package ladder. The first-launch gate names DEALIX_BUSINESS_MODEL.md as
# canonical business-model authority and COMMERCIAL_IDENTITY.md defines the
# current one-product wedge.
VALUE_MAP_DOC = REPO_ROOT / "docs/DEALIX_BUSINESS_MODEL.md"
COMMERCIAL_IDENTITY_DOC = REPO_ROOT / "COMMERCIAL_IDENTITY.md"
FIRST_LAUNCH_GATE = REPO_ROOT / "dealix/config/first_launch_offer_gate.yaml"
BRIEFS_INDEX = FOUNDER_BRIEFS_DIR / "index.json"
AGENCY_CSV = REPO_ROOT / "docs/commercial/operations/targeting/agency_accounts_seed.csv"


def _count_csv_rows(path: Path) -> int:
    if not path.is_file():
        return 0
    text = path.read_text(encoding="utf-8")
    lines = [ln for ln in text.strip().splitlines() if ln.strip()]
    return max(0, len(lines) - 1) if lines else 0


def _latest_brief_date() -> str | None:
    if not BRIEFS_INDEX.is_file():
        return None
    import json

    try:
        data = json.loads(BRIEFS_INDEX.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if isinstance(data, dict):
        if data.get("latest_date"):
            return str(data["latest_date"])
        if data.get("date"):
            return str(data["date"])
    if isinstance(data, list) and data:
        last = data[-1]
        if isinstance(last, dict):
            return str(last.get("date") or last.get("brief_date") or "")
    return None


def build_value_map_status() -> dict[str, Any]:
    """Snapshot for founder commercial status from current launch authority."""
    pipeline = analyze_first_paid_diagnostic()
    agency_rows = _count_csv_rows(AGENCY_CSV)
    brief_date = _latest_brief_date()

    artifacts: dict[str, bool] = {
        "value_map_doc": VALUE_MAP_DOC.is_file(),
        "commercial_identity_doc": COMMERCIAL_IDENTITY_DOC.is_file(),
        "first_launch_gate": FIRST_LAUNCH_GATE.is_file(),
        "agency_seed_csv": AGENCY_CSV.is_file(),
        "founder_briefs_index": BRIEFS_INDEX.is_file(),
        "war_room_today": WAR_ROOM_TODAY_JSON.is_file(),
    }

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "brief_latest_date": brief_date,
        "agency_seed_rows": agency_rows,
        "agency_seed_strict_ok": agency_rows >= 80,
        "first_paid": pipeline,
        "artifacts": artifacts,
        # Compatibility key retained. The value is the current launch path,
        # not a public price/package ladder.
        "revenue_ladder_ar": pipeline.get("revenue_ladder_ar"),
        "founder_action": [
            "Qualify one real company for a customer-specific 30-day Revenue Command Pilot",
            "Sync kpi_founder_commercial_import.yaml from CRM when ready",
            "Complete FOUNDER_ACTION in verify_paid_launch_readiness before any live payment provider activation",
        ],
        "doc_path": display_path(VALUE_MAP_DOC),
        "commercial_identity_path": display_path(COMMERCIAL_IDENTITY_DOC),
        "first_launch_gate_path": display_path(FIRST_LAUNCH_GATE),
        "market_intel_index": "docs/commercial/MARKET_INTELLIGENCE_MASTER_INDEX_AR.md",
    }


def build_commercial_value_map(
    *,
    include_value_plan: bool = True,
    motion_top_n: int = 5,
) -> dict[str, Any]:
    """Full payload for API / JSON export — status + catalog + optional value_plan."""
    status = build_value_map_status()
    out: dict[str, Any] = {
        "schema_version": "1.0",
        "generated_at": status["generated_at"],
        "status": status,
        "catalog": get_value_map_catalog(),
    }
    if include_value_plan:
        from dealix.commercial_ops.value_plan import build_value_plan_snapshot

        out["value_plan"] = build_value_plan_snapshot(motion_top_n=motion_top_n)
    return out


def render_commercial_value_map_markdown(blob: dict[str, Any]) -> str:
    """Founder-readable markdown from build_commercial_value_map()."""
    st = blob.get("status") or {}
    fp = st.get("first_paid") or {}
    vp = blob.get("value_plan") or {}
    lines = [
        f"# Commercial Value Map · {vp.get('date') or st.get('generated_at', '')[:10]}",
        "",
        f"_{vp.get('policy_ar') or 'لا توسعة قبل Pilot مدفوع + Proof موثق.'}_",
        "",
        "## North Star",
        f"- First paid Pilot: `{fp.get('verdict', '—')}`",
        f"- Payment (real): **{fp.get('payment_received_real', 0)}**",
        f"- Proof delivered (real): **{fp.get('proof_pack_delivered_real', 0)}**",
        f"- Agency seed rows: **{st.get('agency_seed_rows', 0)}**",
        "",
        "## Evidence",
    ]
    ev = vp.get("evidence") or {}
    lines.append(f"- Today: **{ev.get('today_total', 0)}** · Week: **{ev.get('week_total', 0)}**")
    lines.extend(["", "## Motion A (top)", ""])
    for t in (vp.get("motion_a") or {}).get("targets") or []:
        lines.append(f"- **{t.get('company')}** · `{t.get('status')}` — {t.get('next_action_ar', '')}")
    gtm = vp.get("gtm_stack") or {}
    if gtm:
        lines.extend(["", "## GTM / ABM", ""])
        for item in gtm.get("focus_ar") or []:
            lines.append(f"- {item}")
    lines.extend(["", "## Warnings", ""])
    for w in vp.get("warnings_ar") or []:
        lines.append(f"- {w}")
    for w in st.get("founder_action") or []:
        lines.append(f"- FOUNDER_ACTION: {w}")
    lines.extend(
        [
            "",
            "## Current authority",
            f"- {st.get('doc_path') or 'docs/DEALIX_BUSINESS_MODEL.md'}",
            f"- {st.get('commercial_identity_path') or 'COMMERCIAL_IDENTITY.md'}",
            f"- {st.get('first_launch_gate_path') or 'dealix/config/first_launch_offer_gate.yaml'}",
            "",
            f"_Generated: {blob.get('generated_at')}_",
        ]
    )
    return "\n".join(lines)


def write_value_map_artifacts(*, day: str | None = None, motion_top_n: int = 5) -> dict[str, str]:
    """Write JSON + MD under the governed founder-briefs root."""
    import json

    day = day or datetime.now(UTC).strftime("%Y-%m-%d")
    FOUNDER_BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    blob = build_commercial_value_map(include_value_plan=True, motion_top_n=motion_top_n)
    json_path = FOUNDER_BRIEFS_DIR / f"commercial_value_map_{day}.json"
    md_path = FOUNDER_BRIEFS_DIR / f"commercial_value_map_{day}.md"
    json_path.write_text(json.dumps(blob, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_commercial_value_map_markdown(blob) + "\n", encoding="utf-8")
    return {
        "json": display_path(json_path),
        "md": display_path(md_path),
    }