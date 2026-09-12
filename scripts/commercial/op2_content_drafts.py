#!/usr/bin/env python3
"""OP2 content drafts — from real market signals, draft-only.

Turns the OP2 fresh market-intelligence wave into bilingual, governed content
drafts. Every draft:

  * cites the underlying market signal (source + URL + observed_at);
  * is tagged ``draft`` with ``approval_required=True`` (publishing is L5);
  * contains no fabricated customer, no fake ROI, no guaranteed outcome;
  * separates fact from inference/invitation.

Nothing is published. No social/LinkedIn/WhatsApp send is performed.

Prints: DEALIX_OP2_CONTENT_DRAFTS=OK plus DRAFT_n machine lines.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

WAVE_PATH = REPO_ROOT / "data" / "commercial" / "op2_market_intelligence_wave_v1.json"
OUT_PATH = REPO_ROOT / "data" / "commercial" / "op2_content_drafts_v1.json"

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"
OWNER_AGENT = "dealix-content"

# Banned positive-claim phrases (mirrors the landing forbidden-claims doctrine).
BANNED = ("نضمن", "مضمون", "guaranteed", "blast", "scrape", "scraping", "cold outreach")

SECTOR_AR = {
    "finance_fintech_insurance": "المال والتأمين",
    "technology_saas_si": "التقنية والبرمجيات",
    "healthcare": "الصحة",
    "real_estate_proptech": "العقار والتقنية العقارية",
    "logistics_supply_chain": "اللوجستيات وسلاسل الإمداد",
    "industrial_manufacturing": "التصنيع",
    "government_b2g": "القطاع الحكومي",
    "education_training": "التعليم والتدريب",
    "retail_commerce_ecommerce": "التجزئة والتجارة الإلكترونية",
}


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def draft_for_signal(signal: dict[str, Any]) -> dict[str, Any]:
    sector = str(signal.get("sector_family", UNKNOWN))
    sector_ar = SECTOR_AR.get(sector, sector)
    problem = str(signal.get("problem", UNKNOWN))
    trigger = str(signal.get("trigger", UNKNOWN))
    deadline = str(signal.get("deadline", UNKNOWN))
    authority = str(signal.get("authority_ref", UNKNOWN))
    facts = signal.get("facts") or []
    refs = signal.get("evidence_refs") or []
    fact_line = facts[0] if facts else UNKNOWN

    title_ar = f"{sector_ar}: ما الذي تغيّر ولماذا يهم الآن؟"
    body_ar = (
        f"السياق: {trigger}. "
        f"المصدر الرسمي: {authority}. "
        f"حقيقة موثّقة: {fact_line} "
        + (f"الموعد: {deadline}. " if deadline not in (UNKNOWN, "", "None") else "")
        + f"السؤال التشغيلي المطروح: {problem}. "
        "الخطوة: تشخيص مجاني يوضّح أين يكمن الفارق لديكم — النتائج تبقى تقديرية حتى الاكتشاف، ولا نُعلن نتائج غير مُتحقَّق منها."
    )
    title_en = f"{sector}: what changed and why it matters now"
    body_en = (
        f"Context: {trigger}. "
        f"Official source: {authority}. "
        f"Documented fact: {fact_line} "
        + (f"Deadline: {deadline}. " if deadline not in (UNKNOWN, "", "None") else "")
        + f"Operating question: {problem}. "
        "Next step: a free diagnostic to locate the gap for your context — outcomes stay estimate-only until discovery, and no unverified number is published."
    )
    founder_post_ar = (
        f"إشارة من {sector_ar}: {fact_line} "
        f"(المصدر: {authority}). لا يعني هذا وجود طلب مؤكد — يعني فقط أن هذه نقطة تستحق تشخيصاً."
    )

    return {
        "draft_id": f"op2-draft-{signal.get('signal_id')}",
        "owner_agent": OWNER_AGENT,
        "channel": "linkedin_article_draft",
        "status": "draft",
        "approval_required": True,
        "published": False,
        "sector_family": sector,
        "signal_id": signal.get("signal_id"),
        "source_ref": signal.get("source_ref"),
        "authority_ref": authority,
        "observed_at": signal.get("observed_at"),
        "fact_from_signal": fact_line,
        "trigger": trigger,
        "deadline": deadline,
        "atoms": [
            {"locale": "ar", "type": "article", "title": title_ar, "body": body_ar},
            {"locale": "en", "type": "article", "title": title_en, "body": body_en},
            {"locale": "ar", "type": "founder_post", "title": title_ar, "body": founder_post_ar},
        ],
        "evidence_refs": refs,
        "truth_class": "DRAFT_FROM_RESEARCH_SIGNAL",
        "allowed_use": ["INTERNAL_DRAFT_ONLY"],
        "counts_as_relationship": False,
        "counts_as_pipeline": False,
    }


def build_drafts() -> dict[str, Any]:
    wave = _read_json(WAVE_PATH)
    warnings: list[str] = []
    if not wave:
        warnings.append(f"market wave unreachable: {WAVE_PATH}")

    drafts = [draft_for_signal(signal) for signal in wave.get("signals", []) or []]
    # Drop any draft that accidentally contains a banned positive claim.
    clean: list[dict[str, Any]] = []
    for draft in drafts:
        text = " ".join(atom["body"] for atom in draft["atoms"]).lower()
        if any(term.lower() in text for term in BANNED):
            warnings.append(f"dropped banned-claim draft: {draft['draft_id']}")
            continue
        clean.append(draft)

    return {
        "schema": "dealix.op2-content-drafts.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "owner_agent": OWNER_AGENT,
        "publish_authority": False,
        "warnings": warnings,
        "draft_count": len(clean),
        "drafts": clean,
    }


def render(result: dict[str, Any]) -> str:
    lines = ["DEALIX_OP2_CONTENT_DRAFTS=OK", f"DRAFTS={result['draft_count']}", f"PUBLISH_AUTHORITY={result['publish_authority']}"]
    for index, draft in enumerate(result["drafts"], start=1):
        lines.append(f"DRAFT_{index} {draft['draft_id']} sector={draft['sector_family']} status={draft['status']}")
    for warning in result["warnings"]:
        lines.append(f"WARN {warning}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="OP2 content drafts from real market signals")
    parser.add_argument("--write", action="store_true", help=f"write {OUT_PATH}")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_drafts()
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render(result))
    if args.write:
        OUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"WROTE {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
