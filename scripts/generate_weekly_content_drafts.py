#!/usr/bin/env python3
"""Generate 5 LinkedIn draft posts (AR) from AEO calendar + objection registry.

Draft-only — never publishes. Output: var/content_drafts/YYYY-Www.json

Usage:
    python scripts/generate_weekly_content_drafts.py
    python scripts/generate_weekly_content_drafts.py --week 3
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

AEO_PATH = REPO_ROOT / "docs/commercial/operations/AEO_CONTENT_CALENDAR_AR.md"
OBJ_PATH = REPO_ROOT / "docs/commercial/operations/objection_engine_registry.yaml"
OUT_DIR = REPO_ROOT / "var" / "content_drafts"

BANNED_PHRASES = (
    "cold blast",
    "واتساب بارد",
    "guaranteed roi",
    "ضمان إيراد",
    "auto dm",
    "إرسال تلقائي",
)

_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)\|\s*([^|]+)\|",
    re.MULTILINE,
)


def _iso_week_label(when: datetime | None = None) -> str:
    dt = when or datetime.now(UTC)
    y, w, _ = dt.isocalendar()
    return f"{y}-W{w:02d}"


def parse_aeo_weeks(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    rows: list[dict[str, str]] = []
    for m in _ROW_RE.finditer(text):
        rows.append(
            {
                "week": m.group(1).strip(),
                "slug": m.group(2).strip(),
                "title_ar": m.group(3).strip(),
                "aeo_question": m.group(4).strip(),
            }
        )
    return rows


def load_objections(path: Path) -> list[dict[str, str]]:
    try:
        import yaml  # type: ignore
    except ImportError:
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    items = data.get("objections") or []
    out: list[dict[str, str]] = []
    for ob in items:
        if not isinstance(ob, dict):
            continue
        out.append(
            {
                "id": str(ob.get("id") or ""),
                "response_draft_ar": str(ob.get("response_draft_ar") or "").strip(),
                "content_asset_slug": str(ob.get("content_asset_slug") or ""),
            }
        )
    return out


def _linkedin_body(
    *,
    title_ar: str,
    aeo_question: str,
    slug: str,
    objection_snippet: str,
) -> str:
    cta = "Risk Score مجاني أو Sample Proof Pack — راسلني إن أردت نسخة على 10 leads عندكم."
    lines = [
        f"سؤال يتكرر: {aeo_question}",
        "",
        title_ar,
        "",
        "بعد الحملة، السؤال ليس «كم lead» بل: من رد؟ من تابع؟ ما next action؟ وهل عندكم دليل؟",
        "",
        "Dealix = Post-Lead Revenue Operations محكوم:",
        "Source → Owner → Approval → Evidence → Next Action",
        "",
    ]
    if objection_snippet:
        lines.extend([f"💬 {objection_snippet[:280]}", ""])
    lines.extend(
        [
            f"تعلّم أكثر: /ar/learn/{slug} (عند النشر)",
            "",
            cta,
            "",
            "#RevenueOps #B2B #Saudi #Agency #AIgovernance",
        ]
    )
    return "\n".join(lines)


def build_drafts(*, week_num: int | None = None, count: int = 5) -> list[dict[str, object]]:
    weeks = parse_aeo_weeks(AEO_PATH)
    if not weeks:
        raise RuntimeError(f"No AEO rows parsed from {AEO_PATH}")

    objections = load_objections(OBJ_PATH)
    primary_ob = objections[0] if objections else {}
    ob_snip = primary_ob.get("response_draft_ar", "").replace("\n", " ").strip()

    if week_num is not None:
        selected = [w for w in weeks if w["week"] == str(week_num)]
        if not selected:
            raise ValueError(f"Week {week_num} not in AEO calendar")
        pool = selected * count
    else:
        pool = weeks

    drafts: list[dict[str, object]] = []
    for i, row in enumerate(pool[:count]):
        body = _linkedin_body(
            title_ar=row["title_ar"],
            aeo_question=row["aeo_question"],
            slug=row["slug"],
            objection_snippet=ob_snip if i == 0 else "",
        )
        lower = body.lower()
        for banned in BANNED_PHRASES:
            if banned.lower() in lower:
                raise ValueError(f"Banned phrase in draft: {banned}")
        drafts.append(
            {
                "id": f"linkedin_{row['slug']}_{i + 1}",
                "channel": "linkedin",
                "language": "ar",
                "aeo_week": row["week"],
                "slug": row["slug"],
                "title_ar": row["title_ar"],
                "status": "draft_pending_approval",
                "body": body,
            }
        )
    return drafts


def main(argv: list[str] | None = None) -> int:
    ensure_stdout_utf8()
    parser = argparse.ArgumentParser(description="Weekly LinkedIn content drafts (no publish)")
    parser.add_argument("--week", type=int, default=None, help="AEO calendar week number (1-12)")
    parser.add_argument("--count", type=int, default=5, help="Number of drafts (default 5)")
    args = parser.parse_args(argv)

    drafts = build_drafts(week_num=args.week, count=max(1, min(args.count, 12)))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    label = _iso_week_label()
    out_path = OUT_DIR / f"{label}.json"
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "iso_week": label,
        "draft_count": len(drafts),
        "policy": "draft_only_no_auto_publish",
        "drafts": drafts,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"CONTENT_DRAFTS: wrote {len(drafts)} drafts -> {out_path}")
    for d in drafts:
        print(f"  - [{d['aeo_week']}] {d['title_ar'][:60]}...")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"CONTENT_DRAFTS: FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
