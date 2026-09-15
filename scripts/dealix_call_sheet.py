#!/usr/bin/env python3
"""Dealix Daily Call Sheet — founder-led phone/WhatsApp-call prioritizer.

Turns the founder's warm contact list (`data/warm_list.csv`) into a
**prioritized daily call sheet**: who to call first, why now, the
qualification decision, the recommended offer rung, three talking points,
and a short bilingual call opener. Built so the founder can literally pick
up the phone and start calling warm contacts — the "able to call the
entities" capability — without ever automating outreach.

Pipeline per contact (all deterministic, no LLM, no external IO):
  1. Build ICP signals from the CSV row.
  2. Score ICP fit (auto_client_acquisition.icp_scorer.score_lead, 0-100).
  3. Pre-qualify (auto_client_acquisition.sales_os.qualification.qualify).
  4. Recommend a rung from the 5-rung ladder.
  5. Rank by (relationship warmth, ICP score) descending.

DOCTRINE (hard rules this script obeys):
  - NEVER sends anything. Output is a markdown file + stdout summary.
  - Warm/known contacts only — this is NOT cold calling and NOT scraping.
  - Every external contact still requires the founder to dial manually.
  - No guaranteed-outcome language. No PII beyond what the founder supplied.

Usage:
    python scripts/dealix_call_sheet.py
    python scripts/dealix_call_sheet.py --csv data/warm_list.csv --out data/call_sheet/2026-06-07.md
    python scripts/dealix_call_sheet.py --top 10        # show only the top N
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

DISCLAIMER = "> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"

# Default Saudi-B2B ICP — the kind of account Dealix serves best.
TARGET_SECTORS = ["real_estate", "b2b_services", "agency", "consulting", "finance", "retail"]
TARGET_REGIONS = ["riyadh", "jeddah", "dammam", "khobar", "mecca", "medina", "saudi", "sa", "ksa"]
TARGET_SIZE_BANDS = ["smb", "mid_market", "11-50", "51-200", "201-500"]

SENIOR_ROLES = {"ceo", "coo", "gm", "founder", "co-founder", "md", "managing director",
                "vp", "owner", "partner", "director", "president", "cmo", "cro"}

# Sector-specific talking points (bilingual). Kept evidence-first, no hype.
SECTOR_TALKING_POINTS: dict[str, list[dict[str, str]]] = {
    "real_estate": [
        {"ar": "ترتيب العملاء المحتملين حسب جدية الشراء قبل صرف وقت المبيعات.",
         "en": "Rank buyers by purchase intent before spending sales time."},
        {"ar": "متابعة التجديدات والعقود بموافقة بشرية — لا رسائل آلية.",
         "en": "Renewal & contract follow-up with human approval — no auto-blasts."},
        {"ar": "Proof Pack يوثّق الفرص المكتشفة والقيمة التقديرية.",
         "en": "A Proof Pack documents surfaced opportunities and estimated value."},
    ],
    "b2b_services": [
        {"ar": "تنظيف وإثراء قاعدة العملاء وترتيبها حسب ICP.",
         "en": "Clean, enrich and ICP-rank your client base."},
        {"ar": "Workflows حتمية للعروض والمتابعة تقلّل التسريب.",
         "en": "Deterministic proposal & follow-up workflows that cut leakage."},
        {"ar": "حوكمة PDPL مدمجة — أدلة لكل قرار.",
         "en": "PDPL governance built in — evidence for every decision."},
    ],
    "agency": [
        {"ar": "خدمة Revenue Ops تبيعها لعملائك تحت علامتك (Proof Pack مشترك).",
         "en": "A Revenue Ops service you resell under your brand (co-branded Proof Pack)."},
        {"ar": "تأهيل leads العملاء قبل تسليمها — جودة أعلى.",
         "en": "Qualify client leads before hand-off — higher quality."},
        {"ar": "لا scraping ولا واتساب بارد — حماية لسمعة وكالتك.",
         "en": "No scraping, no cold WhatsApp — protects your agency's reputation."},
    ],
    "consulting": [
        {"ar": "تحويل توصياتك إلى Workflows قابلة للتنفيذ والقياس.",
         "en": "Turn your recommendations into executable, measurable workflows."},
        {"ar": "Proof Pack يثبت الأثر لعملائك بأدلة موثّقة.",
         "en": "A Proof Pack proves impact to your clients with documented evidence."},
        {"ar": "مراجعة حوكمة AI كخدمة Enterprise بطيئة المسار.",
         "en": "AI Governance Review as a slow-track Enterprise offer."},
    ],
}
GENERIC_TALKING_POINTS = [
    {"ar": "نبدأ بتشخيص مجاني — صورة واضحة لقدرتك التشغيلية بلا التزام.",
     "en": "Start with a free diagnostic — a clear picture of your ops capability, no commitment."},
    {"ar": "كل إجراء خارجي بموافقتك أولاً — لا أتمتة بلا مراجعة.",
     "en": "Every external action needs your approval first — no automation without review."},
    {"ar": "نبدأ بـ discovery، ثم نطاق ومدة ومعايير قبول Revenue Command Pilot خاصة بالعميل وquote موثق.",
     "en": "We start with discovery, then a customer-specific Revenue Command Pilot scope, duration, acceptance criteria, and documented quote."},
]

# 5-rung ladder labels (bilingual).
RUNGS = {
    "diagnostic": {"ar": "تشخيص مجاني (0 ر.س)", "en": "Free Diagnostic (0 SAR)"},
    "sprint": {"ar": "Revenue Command Pilot (مدة ونطاق خاصان بالعميل، quote بعد discovery)", "en": "Revenue Command Pilot (customer-specific duration and scope, quote after discovery)"},
    "data_pack": {"ar": "Data-to-Revenue Pack (quote خاص بالعميل بعد discovery)", "en": "Data-to-Revenue Pack (customer-specific quote after discovery)"},
    "managed": {"ar": "Managed Revenue Ops (quote وشروط خاصة بالعميل بعد discovery)", "en": "Managed Revenue Ops (customer-specific quote and terms after discovery)"},
    "custom": {"ar": "Custom AI Project (quote خاص بالعميل بعد discovery)", "en": "Custom AI Project (customer-specific quote after discovery)"},
}


def _to_signals(row: dict[str, str]):
    from auto_client_acquisition.icp_scorer import LeadSignals

    sector = (row.get("sector") or "").strip().lower()
    city = (row.get("city") or "").strip().lower()
    linkedin = (row.get("linkedin_url") or "").strip()
    notes = (row.get("notes") or "").lower()
    return LeadSignals(
        sector=sector or None,
        region=city or None,
        size_band=None,
        recent_funding_round=("fund" in notes or "raise" in notes or "تمويل" in notes),
        recent_executive_hire=("hire" in notes or "joined" in notes or "تعيين" in notes),
        recent_expansion_announcement=("expand" in notes or "launch" in notes or "توسع" in notes),
        has_email=bool((row.get("email") or "").strip()),
        has_domain=bool((row.get("company") or "").strip()),
        has_linkedin=bool(linkedin),
    )


def _icp_score(row: dict[str, str]) -> dict:
    try:
        from auto_client_acquisition.icp_scorer import ICPFilter, score_lead

        icp = ICPFilter(
            target_sectors=TARGET_SECTORS,
            target_regions=TARGET_REGIONS,
            target_size_bands=TARGET_SIZE_BANDS,
            preferred_tech=[],
        )
        return score_lead(_to_signals(row), icp)
    except Exception:
        return {"score": 0, "band": "unknown", "breakdown": {}}


def _qualify(row: dict[str, str]) -> dict:
    try:
        from auto_client_acquisition.sales_os.qualification import qualify
    except Exception:
        return {"decision": "unknown", "score": 0, "doctrine_violations": []}

    role = (row.get("role") or "").strip().lower()
    sector = (row.get("sector") or "").strip()
    relationship = (row.get("relationship") or "cold").strip().lower()
    notes = (row.get("notes") or "").strip()

    has_owner = role in SENIOR_ROLES
    warm = relationship in ("warm", "active")
    result = qualify(
        pain_clear=warm,
        owner_present=has_owner,
        data_available=warm,
        accepts_governance=True,
        has_budget=warm,
        wants_safe_methods=True,
        proof_path_visible=True,
        retainer_path_visible=warm,
        raw_request_text=(notes + " " + sector),
        sector=sector,
    )
    try:
        return result.to_dict()
    except Exception:
        return {"decision": "unknown", "score": 0, "doctrine_violations": []}


def _recommend_rung(qualification: dict, row: dict[str, str]) -> str:
    """Deterministic, conservative rung recommendation. Default = diagnostic.

    We never jump straight to managed/custom from a cold call — the ladder
    is earned via proof. So the call-sheet recommendation tops out at Sprint.
    """
    decision = qualification.get("decision", "unknown")
    relationship = (row.get("relationship") or "cold").strip().lower()
    role = (row.get("role") or "").strip().lower()

    if decision in ("reject", "refer_out"):
        return "diagnostic"  # still safe to offer the free diagnostic
    if decision == "accept" and relationship in ("warm", "active") and role in SENIOR_ROLES:
        return "sprint"
    if decision in ("accept", "diagnostic_only", "reframe"):
        return "diagnostic"
    return "diagnostic"


def _why_now(row: dict[str, str]) -> dict[str, str]:
    relationship = (row.get("relationship") or "cold").strip().lower()
    notes = (row.get("notes") or "").strip()
    if notes:
        return {"ar": f"سياق العلاقة: {notes}", "en": f"Relationship context: {notes}"}
    mapping = {
        "warm": {"ar": "علاقة دافئة — افتتاحية طبيعية بلا برود.",
                 "en": "Warm relationship — natural, non-cold opener."},
        "active": {"ar": "تعاون قائم — فرصة لعرض مكمّل.",
                   "en": "Active collaboration — chance to offer a complement."},
        "cold": {"ar": "تعارف خفيف — ابدأ بالقيمة لا بالعرض.",
                 "en": "Light acquaintance — lead with value, not the pitch."},
    }
    return mapping.get(relationship, mapping["cold"])


def _talking_points(sector: str) -> list[dict[str, str]]:
    pts = list(SECTOR_TALKING_POINTS.get(sector.strip().lower(), []))
    if not pts:
        pts = list(GENERIC_TALKING_POINTS)
    return pts[:3]


def _call_opener(row: dict[str, str]) -> dict[str, str]:
    name = (row.get("name") or "").strip() or "—"
    relationship = (row.get("relationship") or "cold").strip().lower()
    warm_ar = "كنت أفكر فيك" if relationship in ("warm", "active") else "وصلتني توصية عنك"
    warm_en = "I was thinking of you" if relationship in ("warm", "active") else "you came up as a good person to speak to"
    return {
        "ar": (f"السلام عليكم {name}، معك سامي من Dealix. {warm_ar} — نبني محرك إيرادات "
               f"محكوم بحوكمة AI للشركات السعودية (لا scraping، موافقة قبل أي إرسال). "
               f"عندك 20 دقيقة هالأسبوع لتشخيص مجاني سريع لوضعك التشغيلي؟"),
        "en": (f"Hi {name}, this is Sami from Dealix. {warm_en} — we build a governed AI "
               f"revenue engine for Saudi companies (no scraping, approval before any send). "
               f"Do you have 20 minutes this week for a quick free diagnostic of your ops?"),
    }


def _read_rows(csv_path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not csv_path.exists():
        return rows
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # skip fully-empty template rows
            if not (r.get("name") or "").strip() and not (r.get("company") or "").strip():
                continue
            rows.append({k: (v or "").strip() for k, v in r.items()})
    return rows


def build_call_sheet(rows: list[dict[str, str]]) -> list[dict]:
    """Return enriched, ranked contact dicts."""
    rel_rank = {"active": 3, "warm": 2, "cold": 1, "": 0}
    enriched = []
    for row in rows:
        icp = _icp_score(row)
        qual = _qualify(row)
        rung = _recommend_rung(qual, row)
        enriched.append({
            "row": row,
            "icp": icp,
            "icp_total": int(icp.get("score", 0)),
            "qual": qual,
            "rung": rung,
            "why_now": _why_now(row),
            "talking_points": _talking_points(row.get("sector", "")),
            "opener": _call_opener(row),
            "_rel": rel_rank.get((row.get("relationship") or "").strip().lower(), 0),
        })
    enriched.sort(key=lambda e: (e["_rel"], e["icp_total"]), reverse=True)
    return enriched


def _top_signals(breakdown: dict) -> str:
    if not breakdown:
        return "—"
    items = sorted(breakdown.items(), key=lambda kv: kv[1], reverse=True)[:3]
    return ", ".join(f"{k}={v}" for k, v in items if v)


def render_markdown(enriched: list[dict], today: str) -> str:
    decision_badge = {
        "accept": "✅ accept", "diagnostic_only": "🔵 diagnostic-only",
        "reframe": "🟡 reframe", "reject": "🔴 reject",
        "refer_out": "⚪ refer-out", "unknown": "⚪ unknown",
    }
    lines: list[str] = []
    lines.append(f"# 📞 Dealix Daily Call Sheet · {today}")
    lines.append("")
    lines.append("**قائمة اتصال المؤسس — جهات دافئة فقط. اتصال يدوي. لا أتمتة، لا scraping، لا واتساب بارد.**")
    lines.append("_Founder call sheet — warm contacts only. Manual dialing. No automation, no scraping, no cold WhatsApp._")
    lines.append("")
    lines.append(f"- Contacts ready to call: **{len(enriched)}**")
    if enriched:
        avg = round(sum(e["icp_total"] for e in enriched) / len(enriched), 1)
        lines.append(f"- Average ICP fit: **{avg}/100**")
    lines.append("")

    # Priority summary table
    lines.append("## Priority order")
    lines.append("")
    lines.append("| # | Contact | Company | Sector | ICP | Pre-screen | Recommend |")
    lines.append("|---|---|---|---|---|---|---|")
    for i, e in enumerate(enriched, 1):
        r = e["row"]
        lines.append(
            f"| {i} | {r.get('name','—')} | {r.get('company','—')} | "
            f"`{r.get('sector','—')}` | {e['icp_total']}/100 | "
            f"{decision_badge.get(e['qual'].get('decision','unknown'),'—')} | "
            f"{RUNGS[e['rung']]['en']} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Per-contact call cards
    for i, e in enumerate(enriched, 1):
        r = e["row"]
        q = e["qual"]
        viol = q.get("doctrine_violations") or []
        lines.append(f"## {i}. {r.get('name','—')} — {r.get('role','—')} @ {r.get('company','—')}")
        lines.append(
            f"- Sector: `{r.get('sector','—')}` · City: `{r.get('city','—')}` · "
            f"Relationship: `{r.get('relationship','—')}`"
        )
        lines.append(f"- ICP fit: **{e['icp_total']}/100** (top signals: {_top_signals(e['icp'].get('breakdown', {}))})")
        lines.append(
            f"- Pre-screen: {decision_badge.get(q.get('decision','unknown'),'—')} "
            f"· score={q.get('score',0)}/100"
        )
        lines.append(f"- Recommended next offer: **{RUNGS[e['rung']]['ar']} / {RUNGS[e['rung']]['en']}**")
        if viol:
            lines.append(f"- ⚠ doctrine flags: {', '.join(viol)} → reframe to safe methods before any offer.")
        lines.append("")
        lines.append(f"**لماذا الآن / Why now:** {e['why_now']['ar']} — {e['why_now']['en']}")
        lines.append("")
        lines.append("**نقاط الحديث / Talking points:**")
        for tp in e["talking_points"]:
            lines.append(f"- {tp['ar']} — _{tp['en']}_")
        lines.append("")
        lines.append("**افتتاحية المكالمة / Call opener (DRAFT — adapt live):**")
        lines.append(f"> 🇸🇦 {e['opener']['ar']}")
        lines.append(f"> 🇬🇧 {e['opener']['en']}")
        lines.append("")
        lines.append("**Soft close:** book the free diagnostic → https://dealix.me/ar/dealix-diagnostic")
        lines.append("")
        lines.append("- Called: [ ]  ·  Reached: [ ]  ·  Outcome: ____________  ·  Next action: ____________")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append(DISCLAIMER)
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the founder's daily call sheet.")
    parser.add_argument("--csv", default="data/warm_list.csv",
                        help="warm list CSV (name,role,company,sector,relationship,city,linkedin_url,notes)")
    parser.add_argument("--out", default=None,
                        help="output markdown path (default data/call_sheet/<today>.md)")
    parser.add_argument("--top", type=int, default=0, help="limit to top N contacts (0 = all)")
    args = parser.parse_args()

    today = datetime.now(UTC).strftime("%Y-%m-%d")
    csv_path = (REPO_ROOT / args.csv) if not Path(args.csv).is_absolute() else Path(args.csv)
    out_path = Path(args.out) if args.out else (REPO_ROOT / "data" / "call_sheet" / f"{today}.md")
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path

    rows = _read_rows(csv_path)
    if not rows:
        print("⚠ No warm contacts found.")
        print(f"   Fill {csv_path} with warm contacts (copy data/warm_list.csv.template).")
        print("   Columns: name,role,company,sector,relationship,city,linkedin_url,notes")
        print("   Then re-run: python scripts/dealix_call_sheet.py")
        return 0

    enriched = build_call_sheet(rows)
    if args.top and args.top > 0:
        enriched = enriched[: args.top]

    md = render_markdown(enriched, today)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")

    # stdout summary
    print(f"📞 Dealix Call Sheet · {today} — {len(enriched)} contact(s) ranked")
    print(f"   Written to: {out_path}")
    print("   Top priorities:")
    for i, e in enumerate(enriched[:5], 1):
        r = e["row"]
        print(f"   {i}. {r.get('name','—')} @ {r.get('company','—')} "
              f"({r.get('sector','—')}) — ICP {e['icp_total']}/100 → {RUNGS[e['rung']]['en']}")
    print("   Founder dials manually. No automated sending.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
