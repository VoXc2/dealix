#!/usr/bin/env python3
"""Wave 6 Phase 4 — 499 SAR Pilot Brief generator.

Generates a markdown brief for the 7-Day Revenue Proof Sprint.

Hard rules:
- No invoice API call
- No live charge
- No fake payment
- No revenue claim
- amount_sar capped at 499 (Sprint tier)
- amount_halalah computed deterministically (1 SAR = 100 halalah)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LIVE_DIR = Path("docs/wave6/live")


def build_brief(*, company: str, sector: str, amount_sar: float,
                diagnostic_summary: str | None = None) -> dict:
    halalah = int(round(amount_sar * 100))
    return {
        "company": company,
        "sector": sector,
        "package": "7-Day Revenue Proof Sprint",
        "amount_sar": amount_sar,
        "amount_halalah": halalah,
        "duration_days": 7,
        "diagnostic_summary": diagnostic_summary or "—",
        "deliverables": [
            "Lead Quality Audit (تقييم آخر ٥٠ lead)",
            "Pipeline Audit (تحديد leakage points)",
            "3 Daily Decisions Briefs (نموذج للقرارات اليوميّة)",
            "1 Sample Outreach Draft (موافقة المؤسس قبل الإرسال)",
            "Initial Proof Pack (٣ proof events موثّقة)",
            "30-Day Plan PDF",
            "Day 7 Review Call (٣٠ دقيقة)",
        ],
        "timeline_days": [
            "Day 1: Lead Quality Audit",
            "Day 2: Pipeline Audit",
            "Day 3: Sample Drafts",
            "Day 4: Daily Decisions Brief",
            "Day 5: Customer Portal setup",
            "Day 6: Initial Proof Pack",
            "Day 7: Review Call + 30-day plan",
        ],
        "required_inputs": [
            "إذن PDPL مكتوب",
            "وصول Read-only لقائمة آخر ٥٠ lead",
            "موافقة على إرسال drafts للمراجعة (لا live send)",
            "تحديد المؤشّر الرئيسي (KPI) للمتابعة",
        ],
        "what_is_excluded": [
            "إرسال WhatsApp/Email/LinkedIn حيّ (manual فقط)",
            "أي اتصال هاتفي بالعملاء (manual فقط)",
            "تكامل CRM مدفوع",
            "أي ميزة تتطلّب أكثر من ٧ أيّام",
        ],
        "payment": {
            "method": "manual_bank_transfer",
            "amount_sar": amount_sar,
            "amount_halalah": halalah,
            "live_charge": False,
            "moyasar_live": False,
            "evidence_required": True,
            "founder_must_confirm_manually": True,
        },
        "kpi_commitment": {
            "type": "commitment_not_guarantee",
            "rule_ar": "لو ما تحقّق +٢٠٪ على المؤشّر المتّفق عليه، أشتغل مجّاناً حتى يتحقّق",
            "rule_en": "If +20% lift on agreed KPI not achieved, founder works free until met",
        },
        "refund_policy": {
            "window_days": 14,
            "rate_pct": 100,
            "questions_required": False,
            "method": "bank_transfer",
        },
        "proof_pack_at_end": True,
        "approval_first_statement_ar": (
            "كل إجراء خارجي خلال الـ Sprint يحتاج موافقتك قبل التنفيذ. "
            "لا live send. لا live charge. لا ادّعاءات بدون دليل. "
            "Proof Pack موثّق يُسلَّم في اليوم ٧."
        ),
        "approval_first_statement_en": (
            "Every external action during the Sprint requires your approval. "
            "No live send. No live charge. No claims without evidence. "
            "Documented Proof Pack delivered on Day 7."
        ),
        "no_revenue_claim": True,
        "no_guaranteed_claim": True,
        "is_template_based": True,
        "source": "wave6_phase4_pilot_brief_generator",
    }


def render_markdown(b: dict) -> str:
    lines = []
    lines.append(f"# {b['package']} — {b['company']}")
    lines.append("")
    lines.append(f"**القطاع:** {b['sector']}  ·  **المدّة:** {b['duration_days']} أيّام  ·  **السعر:** {b['amount_sar']} ريال ({b['amount_halalah']} هللة)")
    lines.append("")
    lines.append("## 🎯 المخرجات")
    for d in b["deliverables"]:
        lines.append(f"- {d}")
    lines.append("")
    lines.append("## 📅 الجدول الزمني")
    for t in b["timeline_days"]:
        lines.append(f"- {t}")
    lines.append("")
    lines.append("## ✅ المدخلات المطلوبة منكم")
    for r in b["required_inputs"]:
        lines.append(f"- {r}")
    lines.append("")
    lines.append("## ❌ ما هو مُستثنى من هذه الباقة")
    for x in b["what_is_excluded"]:
        lines.append(f"- {x}")
    lines.append("")
    lines.append("## 💳 الدفع (يدوي — لا خصم آلي)")
    lines.append(f"- المبلغ: **{b['amount_sar']} ريال** ({b['amount_halalah']} هللة)")
    lines.append(f"- الطريقة: تحويل بنكي يدوي")
    lines.append(f"- المؤسس يؤكّد الاستلام يدوياً")
    lines.append(f"- لا live charge")
    lines.append("")
    lines.append("## 📈 التزام الـ KPI (التزام، لا ضمان)")
    lines.append(f"- {b['kpi_commitment']['rule_ar']}")
    lines.append(f"- _{b['kpi_commitment']['rule_en']}_")
    lines.append("")
    lines.append("## 🔄 سياسة الاسترجاع")
    lines.append(f"- **{b['refund_policy']['rate_pct']}% خلال {b['refund_policy']['window_days']} يوم** بدون أسئلة")
    lines.append("")
    lines.append("## 🛡️ الالتزام بـ Approval-First")
    lines.append(b["approval_first_statement_ar"])
    lines.append("")
    lines.append(f"> {b['approval_first_statement_en']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("**Proof Pack يُسلَّم في اليوم السابع — بدون أرقام مخترعة، بدون ادّعاءات.**")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="Wave 6 Pilot Brief generator")
    p.add_argument("--company", required=True)
    p.add_argument("--sector", required=True)
    p.add_argument("--diagnostic-file", default=None,
                   help="Path to diagnostic.json (optional)")
    p.add_argument("--amount-sar", type=float, default=499.0)
    p.add_argument("--out-md", default=None)
    p.add_argument("--out-json", default=None)
    args = p.parse_args()

    if args.amount_sar > 499.0:
        print(f"REFUSING: amount_sar > 499 (Sprint tier cap)", file=sys.stderr)
        return 2

    diagnostic_summary = None
    if args.diagnostic_file:
        try:
            d = json.loads(Path(args.diagnostic_file).read_text(encoding="utf-8"))
            diagnostic_summary = d.get("executive_summary_ar", "")[:300]
        except Exception as exc:
            print(f"WARNING: could not read diagnostic-file: {exc}", file=sys.stderr)

    brief = build_brief(
        company=args.company,
        sector=args.sector,
        amount_sar=args.amount_sar,
        diagnostic_summary=diagnostic_summary,
    )

    out_md = Path(args.out_md) if args.out_md else LIVE_DIR / "pilot_brief.md"
    out_json = Path(args.out_json) if args.out_json else LIVE_DIR / "pilot_brief.json"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_markdown(brief), encoding="utf-8")
    out_json.write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK: wrote {out_md} + {out_json}")
    print(f"  amount_sar: {brief['amount_sar']}")
    print(f"  amount_halalah: {brief['amount_halalah']}")
    print(f"  live_charge: {brief['payment']['live_charge']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
