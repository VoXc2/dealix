#!/usr/bin/env python3
"""Warm-list outreach generator — governed market motion.

Reads `data/warm_list.csv` (founder fills warm contacts), generates per-
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
    "أنا أبني Dealix كشركة تشغيل ذكاء اصطناعي محكوم تبدأ من السعودية.\n\n"
    "هذا ليس بيع أتمتة AI عامة. زاويتنا تشخيص تشغيلي محكوم للشركات التي تستخدم AI "
    "لكن ينقصها وضوح المصدر وحدود الموافقات ومسار الأدلة وقياس القيمة.\n\n"
    "بالنظر إلى دورك في {company} كـ{role} في قطاع {sector}، {context_line}\n\n"
    "هل لديكم شريحة عميل تعاني من AI بلا حوكمة كافية؟\n\n"
    "تحياتي،\n"
    "Sami"
)


_BASE_MESSAGE_EN = (
    "Hi {name},\n\n"
    "I’m building Dealix, a governed AI operations company starting in Saudi Arabia.\n\n"
    "This is not an AI automation resale motion.\n\n"
    "The angle is a governed AI operations diagnostic for clients already experimenting "
    "with AI but lacking source clarity, approval boundaries, evidence trails, proof "
    "of value, and agent identity controls.\n\n"
    "Given your role at {company} as {role} in {sector}, {context_line}\n\n"
    "Would it be useful to compare this against one client segment you already see "
    "asking about AI governance or AI-driven revenue operations?\n\n"
    "Best,\n"
    "Sami"
)


_CONTEXT_BY_RELATIONSHIP = {
    "warm": {
        "ar": "أثق أن عندك رؤية عملية مباشرة عن هذا النوع من التحدي.",
        "en": "you likely have direct visibility into this kind of challenge.",
    },
    "cold": {
        "ar": "ما زلت أتعلم هذا القطاع وأقدّر توجيهك على شريحة عميل مناسبة.",
        "en": "I am still learning this segment and value your guidance on a fit client profile.",
    },
    "active": {
        "ar": "تعاوننا السابق يجعل رأيك مهمًا جدًا في اختبار هذا الاتجاه.",
        "en": "our prior collaboration makes your view especially valuable for this motion.",
    },
    "": {
        "ar": "أبحث عن رأي واضح حول مدى مناسبة هذا التوجه للسوق.",
        "en": "I am looking for a clear signal on whether this angle is market-relevant.",
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
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="How many contacts to include (default 5 for the first batch)",
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

    selected_rows = rows
    if args.limit and args.limit > 0:
        selected_rows = rows[: args.limit]

    out_path = REPO_ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    drafts: list[str] = []
    drafts.append(f"# Warm-list outreach drafts · مسوّدات التواصل\n")
    drafts.append(f"_Generated: {datetime.now(timezone.utc).isoformat()}_\n")
    drafts.append(f"_Contacts in CSV: {len(rows)}_\n")
    drafts.append(f"_Contacts selected for this batch: {len(selected_rows)}_\n")
    drafts.append("\n")
    drafts.append(
        "**Usage:** send the first batch manually (default 5 contacts). Keep each message "
        "as-is: one personalized line + one question, no deck/PDF/attachments. "
        "Pre-screen decision badge tells you whether to reach out, deprioritize, or refer-out. "
        "Doctrine violations BLOCK the outreach — refuse the contact cleanly.\n\n"
    )
    drafts.append("---\n\n")

    accepted = 0
    deprioritized = 0
    rejected = 0
    for row in selected_rows:
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
        f"- Total contacts in CSV: {len(rows)}\n"
        f"- Contacts in this batch: {len(selected_rows)}\n"
        f"- Accept (reach out now): {accepted}\n"
        f"- Diagnostic-only / reframe: {deprioritized}\n"
        f"- Reject / refer-out: {rejected}\n\n"
        f"_Estimated outcomes are not guaranteed outcomes / "
        f"النتائج التقديرية ليست نتائج مضمونة._\n"
    )
    drafts.append(summary)

    out_path.write_text("".join(drafts), encoding="utf-8")
    print(f"✓ Wrote {len(selected_rows)} drafts to {out_path}")
    print(f"  - source contacts in csv: {len(rows)}")
    print(f"  - accept: {accepted}")
    print(f"  - diagnostic_only/reframe: {deprioritized}")
    print(f"  - reject/refer_out: {rejected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
