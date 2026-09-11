#!/usr/bin/env python3
"""Generate Dealix's daily governed multi-channel content draft pack.

No external publishing occurs here. This runner is intentionally safe for the
Company Brain loop: it composes current corporate messaging, current-authority
social drafts and review metadata into local report artifacts only.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from zoneinfo import ZoneInfo

from dealix.commercial_ops.social_queue import get_post_for_date
from dealix.marketing_factory.weekly_pack import generate_weekly_pack

ROOT = Path(__file__).resolve().parents[1]
RIYADH = ZoneInfo("Asia/Riyadh")
GTM_CONFIG = ROOT / "config" / "growth" / "dealix_gtm_social_engine_v1.json"
OUT = ROOT / "reports" / "company_os" / "daily"


def _load_gtm() -> dict:
    return json.loads(GTM_CONFIG.read_text(encoding="utf-8"))


def _markdown(pack: dict) -> str:
    lines = [
        "# Dealix Content Drafts Today",
        "",
        f"Date (Asia/Riyadh): {pack['date']}",
        f"Brand: {pack['parent_brand']} · Flagship product: {pack['flagship_product']}",
        "",
        "> Draft-only. No external publish/send was executed by this runner.",
        "",
        "## Daily thesis",
        "",
        pack["daily_thesis"],
        "",
        "## Channel-native draft pack",
        "",
    ]
    for item in pack["drafts"]:
        lines.extend(
            [
                f"### {item['channel']} — {item['title_ar']}",
                "",
                item["body_draft_ar"],
                "",
                f"CTA: {item['cta_label_ar']} ({item['cta_path']})",
                f"Campaign: {item['utm_campaign']}",
                f"Status: {item['status']}",
                "",
            ]
        )

    if pack.get("canonical_social_today"):
        row = pack["canonical_social_today"]
        lines.extend(
            [
                "## Canonical social queue candidate",
                "",
                f"Surface: {row.get('surface') or 'linkedin'}",
                f"Title: {row.get('title_ar') or ''}",
                "",
                str(row.get("body_ar") or ""),
                "",
                f"CTA: {row.get('cta_ar') or ''}",
                f"Authority: {row.get('launch_authority') or ''}",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "## Canonical social queue candidate",
                "",
                "HOLD: no selectable corporate_brand_gtm_v1 row is currently available. Regenerate the canonical queue; do not resurrect legacy content.",
                "",
            ]
        )

    lines.extend(
        [
            "## Review gates",
            "",
            "- Source/evidence class is known for any market or proof claim.",
            "- Research is not represented as a relationship or buyer intent.",
            "- Demo/synthetic evidence is not represented as Customer Proof.",
            "- External publish remains approval/action-bound.",
            "- Paid amplification remains disabled without separate spend authority.",
            "",
            "## Measurement",
            "",
            ", ".join(pack["primary_metrics"]),
            "",
        ]
    )
    return "\n".join(lines)


def main(*, on_date: date | None = None) -> int:
    # Import datetime locally so the runner remains easy to monkeypatch/test.
    from datetime import datetime

    today = on_date or datetime.now(RIYADH).date()
    gtm = _load_gtm()
    weekly = generate_weekly_pack(week_start=today)
    canonical_today = get_post_for_date(today)

    drafts = [
        {
            "scheduled_date": row["scheduled_date"],
            "channel": row["channel"],
            "title_ar": row["title_ar"],
            "body_draft_ar": row["body_draft_ar"],
            "cta_label_ar": row["cta_label_ar"],
            "cta_path": row["cta_path"],
            "utm_campaign": row["utm_campaign"],
            "status": "draft",
        }
        for row in weekly["slots"]
    ]

    pack = {
        "date": today.isoformat(),
        "timezone": "Asia/Riyadh",
        "parent_brand": "Dealix",
        "flagship_product": "Dealix OS",
        "daily_thesis": (
            "Turn one verified signal or first-party operating lesson into a clear B2B consequence, "
            "a recognizable Dealix point of view, and a measurable next action."
        ),
        "drafts": drafts,
        "canonical_social_today": canonical_today,
        "content_pillars": [p["name"] for p in gtm["content_pillars"]],
        "primary_metrics": list(gtm["measurement"]["primary"]),
        "external_publish_executed": False,
        "customer_send_executed": False,
        "paid_spend_executed": False,
        "governance": "DRAFT_ONLY_APPROVAL_FIRST",
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "CONTENT_DRAFTS_TODAY.md").write_text(_markdown(pack), encoding="utf-8")
    (OUT / f"content_drafts_{today.isoformat()}.json").write_text(
        json.dumps(pack, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("DEALIX_CONTENT_FACTORY_DAILY=PASS")
    print(f"DATE={today.isoformat()}")
    print(f"DRAFT_COUNT={len(drafts)}")
    print(f"CANONICAL_SOCIAL_AVAILABLE={str(canonical_today is not None).lower()}")
    print("EXTERNAL_PUBLISH_EXECUTED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
