"""Generate bilingual outreach drafts for the top scored leads.

Usage:
    python3 scripts/generate_outreach_drafts.py --top 10 --language both --channel whatsapp
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCORED_PATH = REPO_ROOT / "business" / "_data" / "scored_leads.json"
QUEUE_PATH = REPO_ROOT / "business" / "_data" / "outreach_review_queue.json"


AR_OPENERS = {
    "marketing_agency": "مرحبًا، شفت إن وكالتكم تنشر حملات قوية، بس الاستجابة على الليدز الواردة تتأخر. Dealix يحلّه — مسوّدات مولّدة + مراجعة بشرية.",
    "training": "السلام عليكم، لاحظت إن دوراتكم قوية، بس المتابعة بعد الكورس ضعيفة. Dealix يبني نظام متابعة قابل للقياس.",
    "clinic": "السلام عليكم، لاحظت إن تقييماتكم على Google ما عليها متابعة. Dealix يبني نظام ردود بموافقة بشرية + تقرير شهري.",
    "real_estate": "السلام عليكم، شفت إنكم تعلنون عن عقارات بشكل مستمر، بس المتابعة على الليدز مو منتظمة. Dealix ينسّق المتابعة على مستوى المكتب.",
    "logistics": "السلام عليكم، أعرف إن تحديثات الشحنات عندكم يدوية. Dealix يبني غرفة قيادة بخمسة مؤشرات فقط.",
    "consulting": "السلام عليكم، شفت إن Pipeline عندكم ما عنده إيقاع أسبوعي. Dealix يركّب الإيقاع + تقرير إثبات أسبوعي.",
    "b2b_services": "السلام عليكم، شفت إن فريقكم يستقبل ليدز لكن المتابعة تأخذ وقت. Dealix يقفل نافذة الرد.",
    "retail": "السلام عليكم، شفت إن عندكم فروع لكن التقارير مو موحّدة. Dealix يبني Command Center بسيط.",
}

EN_OPENERS = {
    "marketing_agency": "Hi, I noticed your agency ships strong campaigns but inbound response is slow. Dealix closes that window with drafts + human review.",
    "training": "Hello, your courses are strong but post-course follow-up is light. Dealix builds a measurable retention flow.",
    "clinic": "Hello, your Google reviews need a steady response system. Dealix installs human-approved replies + a monthly report.",
    "real_estate": "Hello, listings change fast but follow-up isn't consistent. Dealix coordinates follow-up across the office.",
    "logistics": "Hello, shipment updates are manual. Dealix builds a command center with five KPIs only.",
    "consulting": "Hello, your pipeline doesn't have a weekly cadence. Dealix installs the cadence + a weekly proof report.",
    "b2b_services": "Hello, your team takes inbound leads but follow-up is slow. Dealix closes the response window.",
    "retail": "Hello, your multi-branch reporting isn't unified. Dealix builds a simple Command Center.",
}


def load_queue() -> list[dict]:
    if not QUEUE_PATH.exists():
        return []
    try:
        data = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
        return data.get("drafts", [])
    except json.JSONDecodeError:
        return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--language", choices=["ar", "en", "both"], default="both")
    parser.add_argument("--channel", default="whatsapp")
    args = parser.parse_args()

    if not SCORED_PATH.exists():
        print(f"missing: {SCORED_PATH}")
        return 1
    data = json.loads(SCORED_PATH.read_text(encoding="utf-8"))
    accounts = data.get("accounts", [])[: args.top]

    queue = load_queue()
    queue_ids = {d["draftId"] for d in queue}
    added = 0

    for a in accounts:
        seg = a.get("segment", "")
        for lang in (["ar", "en"] if args.language == "both" else [args.language]):
            draft_id = f"draft-{a['id']}-{lang}"
            if draft_id in queue_ids:
                continue
            opener = (AR_OPENERS if lang == "ar" else EN_OPENERS).get(seg, "")
            if not opener:
                continue
            queue.append(
                {
                    "draftId": draft_id,
                    "accountId": a["id"],
                    "language": lang,
                    "channel": args.channel,
                    "tone": "executive",
                    "opener": opener,
                    "followUp1": "لو تبغى مكالمة 20 دقيقة بدون التزام، اختر الوقت اللي يناسبك." if lang == "ar" else "Open to a 20-min diagnostic call?",
                    "followUp2": "أقدر أرسل one-pager للفريق." if lang == "ar" else "I can send a one-pager to your team.",
                    "reviewStatus": "draft_pending_human_review",
                    "generatedAt": "2026-06-11",
                    "reviewer": None,
                    "reviewedAt": None,
                    "rejectionReason": None,
                    "safetyFlags": ["no_roi_claim", "no_fake_testimonial", "no_pressure"],
                }
            )
            added += 1

    QUEUE_PATH.write_text(
        json.dumps({"drafts": queue, "version": "1.0"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"added {added} drafts to {QUEUE_PATH} (total in queue: {len(queue)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
