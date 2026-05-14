#!/usr/bin/env python3
"""Warm-list outreach generator — Wave 15 (A5).

Reads `data/warm_list.csv` (founder fills 20 contacts), generates per-
contact personalized bilingual messages, writes them to
`data/outreach/warm_list_drafts.md` for founder copy-paste into
LinkedIn / WhatsApp / email.

Each draft is auto-pre-screened through `sales_os.qualification.qualify`
based on the contact's role + sector + relationship_status, so the
founder sees the qualification decision badge before reaching out.

NEVER sends externally. Output is a markdown file the founder reads.

Usage:
    python scripts/warm_list_outreach.py
    python scripts/warm_list_outreach.py --csv data/warm_list.csv --out data/outreach/warm_list_drafts.md
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


_BASE_MESSAGE_AR = (
    "السلام عليكم {name},\n\n"
    "أبني MVP لخدمة Revenue Intelligence لشركات B2B سعودية — تشخيص قدرة "
    "تشغيلية، بيانات نظيفة، فرص مرتبة، رسائل عربية جاهزة، Proof Pack — "
    "كلها محكومة بحوكمة AI واضحة (لا scraping، لا واتساب بارد، لا وعود).\n\n"
    "بالنظر إلى دورك في {company} كـ{role} وقطاع {sector}، {context_line}\n\n"
    "أبحث عن 2-3 شركات تجرّب:\n"
    "  • تشخيص مجاني 24 ساعة (https://dealix.me/diagnostic.html)\n"
    "  • Sprint مدفوع 499 ريال (7 أيام، Proof Pack مضمون، استرداد 14 يوم)\n\n"
    "هل أنت أو أحد من شبكتك يستفيد من هذا؟\n\n"
    "شكرًا — سامي."
)


_BASE_MESSAGE_EN = (
    "Hi {name},\n\n"
    "I'm building Revenue Intelligence MVP for Saudi B2B companies — "
    "operating-capability diagnostic, clean data, ranked opportunities, "
    "Arabic drafts, Proof Pack — all under explicit AI governance "
    "(no scraping, no cold WhatsApp, no guarantees).\n\n"
    "Given your role at {company} as {role} in {sector}, {context_line}\n\n"
    "Looking for 2-3 companies to try:\n"
    "  • Free 24h diagnostic (https://dealix.me/diagnostic.html)\n"
    "  • 499 SAR paid Sprint (7 days, guaranteed Proof Pack, 14-day refund)\n\n"
    "Anyone in your network this might fit?\n\n"
    "Thanks — Sami."
)


_CONTEXT_BY_RELATIONSHIP = {
    "warm": {
        "ar": "أعتقد فيه match لخدمتنا — Sprint 499 ريال يثبت القيمة قبل الالتزام.",
        "en": "I think there's a fit — the 499 SAR Sprint proves value before any commitment.",
    },
    "cold": {
        "ar": "لا أعرف القطاع بعمق — Sprint بسيط 499 ريال يكشف الفرص بسرعة.",
        "en": "I don't know the sector deeply yet — a quick 499 SAR Sprint surfaces opportunities fast.",
    },
    "active": {
        "ar": "نتعاون سابقًا، عرض الـSprint قد يكون مكمل لما تشتغل عليه.",
        "en": "We've collaborated before — the Sprint may complement your current work.",
    },
    "": {
        "ar": "أبحث عن 2-3 شركات تجرب التشخيص المجاني.",
        "en": "Looking for 2-3 companies to try the free diagnostic.",
    },
}


def _qualify_contact(role: str, sector: str, relationship: str, notes: str) -> dict:
    try:
        from auto_client_acquisition.sales_os.qualification import qualify
    except Exception:  # noqa: BLE001
        return {"decision": "unknown", "score": 0, "reasons": [], "doctrine_violations": []}

    # Infer the 8 yes/no flags from the limited intake.
    has_owner = bool(role) and role.upper() in (
        "CEO", "COO", "GM", "FOUNDER", "MD", "VP",
    ) or role.lower() in ("ceo", "coo", "gm", "founder", "md", "vp")
    warm_or_active = relationship in ("warm", "active")
    rel_text = (notes or "") + " " + sector
    result = qualify(
        pain_clear=warm_or_active,
        owner_present=has_owner,
        data_available=warm_or_active,
        accepts_governance=True,
        has_budget=warm_or_active,
        wants_safe_methods=True,
        proof_path_visible=True,
        retainer_path_visible=warm_or_active,
        raw_request_text=rel_text,
        sector=sector,
    )
    return result.to_dict()


def _render_contact(row: dict[str, str], qualification: dict) -> str:
    name = (row.get("name") or "").strip() or "(name?)"
    role = (row.get("role") or "").strip() or "(role?)"
    company = (row.get("company") or "").strip() or "(company?)"
    sector = (row.get("sector") or "").strip() or "(sector?)"
    relationship = (row.get("relationship") or "cold").strip().lower()
    city = (row.get("city") or "").strip()
    linkedin = (row.get("linkedin_url") or "").strip()
    notes = (row.get("notes") or "").strip()

    context = _CONTEXT_BY_RELATIONSHIP.get(relationship) or _CONTEXT_BY_RELATIONSHIP[""]
    ar_msg = _BASE_MESSAGE_AR.format(
        name=name, company=company, role=role, sector=sector,
        context_line=context["ar"],
    )
    en_msg = _BASE_MESSAGE_EN.format(
        name=name, company=company, role=role, sector=sector,
        context_line=context["en"],
    )

    decision = qualification.get("decision", "unknown")
    score = qualification.get("score", 0)
    violations = qualification.get("doctrine_violations", [])

    decision_badge = {
        "accept": "✅ accept",
        "diagnostic_only": "🔵 diagnostic_only",
        "reframe": "🟡 reframe — scope call needed",
        "reject": "🔴 reject",
        "refer_out": "⚪ refer_out",
    }.get(decision, decision)

    violation_block = ""
    if violations:
        violation_block = (
            "**⚠ doctrine violations detected:** " + ", ".join(violations) + "\n\n"
        )

    return (
        f"## {name} — {role} @ {company}\n"
        f"- Sector: `{sector}` · City: `{city}` · Relationship: `{relationship}`\n"
        f"- LinkedIn: {linkedin or '—'}\n"
        f"- Pre-screen: {decision_badge} · score={score}/100\n"
        f"- Notes: {notes or '—'}\n\n"
        f"{violation_block}"
        f"### Arabic message (primary)\n```\n{ar_msg}\n```\n\n"
        f"### English message (secondary)\n```\n{en_msg}\n```\n\n"
        f"- Channel: <choose: LinkedIn DM / WhatsApp / Email>\n"
        f"- Sent: [ ]\n"
        f"- Replied: [ ]\n"
        f"- Next action: [ ]\n\n"
        f"---\n\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv",
        default="data/warm_list.csv",
        help="Input CSV with name,role,company,sector,relationship,city,linkedin_url,notes",
    )
    parser.add_argument(
        "--out",
        default="data/outreach/warm_list_drafts.md",
        help="Output markdown",
    )
    args = parser.parse_args()

    csv_path = REPO_ROOT / args.csv
    if not csv_path.exists():
        print(f"❌ CSV not found at {csv_path}")
        print("Copy the template:")
        print(f"   cp data/warm_list.csv.template {args.csv}")
        return 1

    rows: list[dict[str, str]] = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not (row.get("name") or "").strip():
                continue  # skip empty rows
            rows.append(row)

    if not rows:
        print(f"⚠ CSV is empty — fill {csv_path} with at least 1 contact then re-run.")
        return 1

    out_path = REPO_ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    drafts: list[str] = []
    drafts.append(f"# Warm-list outreach drafts · مسوّدات التواصل\n")
    drafts.append(f"_Generated: {datetime.now(timezone.utc).isoformat()}_\n")
    drafts.append(f"_Contacts in CSV: {len(rows)}_\n")
    drafts.append("\n")
    drafts.append(
        "**Usage:** copy 5/day into LinkedIn / WhatsApp / email. Pre-screen "
        "decision badge tells you whether to reach out, deprioritize, or refer-out. "
        "Doctrine violations BLOCK the outreach — refuse the contact cleanly.\n\n"
    )
    drafts.append("---\n\n")

    accepted = 0
    deprioritized = 0
    rejected = 0
    for row in rows:
        q = _qualify_contact(
            role=row.get("role", ""),
            sector=row.get("sector", ""),
            relationship=row.get("relationship", "cold"),
            notes=row.get("notes", ""),
        )
        decision = q.get("decision", "unknown")
        if decision == "accept":
            accepted += 1
        elif decision in ("reject", "refer_out"):
            rejected += 1
        else:
            deprioritized += 1
        drafts.append(_render_contact(row, q))

    summary = (
        f"## Summary\n\n"
        f"- Total contacts: {len(rows)}\n"
        f"- Accept (reach out today): {accepted}\n"
        f"- Diagnostic-only / reframe: {deprioritized}\n"
        f"- Reject / refer-out: {rejected}\n\n"
        f"_Estimated outcomes are not guaranteed outcomes / "
        f"النتائج التقديرية ليست نتائج مضمونة._\n"
    )
    drafts.append(summary)

    out_path.write_text("".join(drafts), encoding="utf-8")
    print(f"✓ Wrote {len(rows)} drafts to {out_path}")
    print(f"  - accept: {accepted}")
    print(f"  - diagnostic_only/reframe: {deprioritized}")
    print(f"  - reject/refer_out: {rejected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
