#!/usr/bin/env python3
"""WhatsApp draft generator — Wave 16 (A11).

Companion to `scripts/warm_list_outreach.py`. Same input
(`data/warm_list.csv`) but produces WhatsApp-formatted drafts:
- Shorter (≤ 250 chars per message)
- Voice-note-friendly (one ask per message)
- No URL spam (one link maximum)
- Bilingual: AR primary, EN optional in separate message

NEVER sends. Output is a markdown file the founder copies into the
WhatsApp Web composer (per `docs/content/WHATSAPP_TEMPLATES.md`).

Each draft is auto-pre-screened through `sales_os.qualification.qualify`
— founder sees the decision badge before reaching out.

Usage:
    python scripts/whatsapp_draft.py
    python scripts/whatsapp_draft.py --csv data/warm_list.csv --out data/outreach/whatsapp_drafts.md
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


_AR_MESSAGE = (
    "السلام عليكم {name}،\n\n"
    "أبني MVP لـRevenue Intelligence لشركات B2B سعودية. "
    "أبحث عن شركتين يجربون تشخيصاً مجانياً + Sprint 499 ر.س. "
    "تعرف من في {company} يفيده هذا؟\n\n"
    "tinyurl.com/dealix-diag\n\n"
    "(يمكنك الرد STOP في أي وقت)"
)


_EN_VOICE_NOTE_SCRIPT = (
    "Hi {name}, quick voice note — I'm building Revenue Intelligence "
    "for Saudi B2B; looking for 2 founders to try free diagnostic + "
    "499 SAR Sprint. Anyone at {company} this might fit?"
)


def _qualify(role: str, sector: str, relationship: str, notes: str) -> dict:
    try:
        from auto_client_acquisition.sales_os.qualification import qualify
    except Exception:  # noqa: BLE001
        return {"decision": "unknown", "score": 0, "doctrine_violations": []}
    has_owner = bool(role) and role.upper() in (
        "CEO", "COO", "GM", "FOUNDER", "MD", "VP",
    ) or role.lower() in ("ceo", "coo", "gm", "founder", "md", "vp")
    warm_or_active = relationship in ("warm", "active")
    result = qualify(
        pain_clear=warm_or_active,
        owner_present=has_owner,
        data_available=warm_or_active,
        accepts_governance=True,
        has_budget=warm_or_active,
        wants_safe_methods=True,
        proof_path_visible=True,
        retainer_path_visible=warm_or_active,
        raw_request_text=(notes or "") + " " + sector,
        sector=sector,
    )
    return result.to_dict()


def _render(row: dict[str, str], qualification: dict) -> str:
    name = (row.get("name") or "").strip() or "(name?)"
    company = (row.get("company") or "").strip() or "(company?)"
    role = (row.get("role") or "").strip() or "(role?)"
    relationship = (row.get("relationship") or "cold").strip().lower()
    decision = qualification.get("decision", "unknown")
    score = qualification.get("score", 0)
    violations = qualification.get("doctrine_violations", [])

    badges = {
        "accept": "✅ accept",
        "diagnostic_only": "🔵 diagnostic_only",
        "reframe": "🟡 reframe",
        "reject": "🔴 reject (DO NOT SEND)",
        "refer_out": "⚪ refer_out",
    }
    badge = badges.get(decision, decision)

    ar_msg = _AR_MESSAGE.format(name=name, company=company)
    en_voice = _EN_VOICE_NOTE_SCRIPT.format(name=name, company=company)

    violation_block = ""
    if violations:
        violation_block = (
            "**⚠ doctrine violations detected — DO NOT SEND:** "
            + ", ".join(violations) + "\n\n"
        )

    return (
        f"## {name} — {role} @ {company}\n"
        f"- Relationship: `{relationship}` · Pre-screen: {badge} (score {score}/100)\n\n"
        f"{violation_block}"
        f"### Arabic WhatsApp message ({len(ar_msg)} chars)\n```\n{ar_msg}\n```\n\n"
        f"### English voice-note script (~30 sec)\n```\n{en_voice}\n```\n\n"
        f"- Channel: [ ] LinkedIn DM   [ ] WhatsApp text   [ ] WhatsApp voice note\n"
        f"- Sent: [ ]\n"
        f"- Replied: [ ]\n"
        f"- Next action: [ ]\n\n"
        f"---\n\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/warm_list.csv")
    parser.add_argument("--out", default="data/outreach/whatsapp_drafts.md")
    args = parser.parse_args()

    csv_path = REPO_ROOT / args.csv
    if not csv_path.exists():
        print(f"❌ CSV not found at {csv_path}")
        print(f"Copy the template: cp data/warm_list.csv.template {args.csv}")
        return 1

    rows: list[dict[str, str]] = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not (row.get("name") or "").strip():
                continue
            rows.append(row)

    if not rows:
        print(f"⚠ CSV is empty — fill {csv_path} with at least 1 contact then re-run.")
        return 1

    out_path = REPO_ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("# WhatsApp drafts · مسوّدات واتساب\n")
    lines.append(f"_Generated: {datetime.now(timezone.utc).isoformat()}_\n")
    lines.append(f"_Contacts: {len(rows)}_\n\n")
    lines.append(
        "**Channel rules (PDPL Article 5 + Dealix non-negotiables):**\n\n"
        "- WhatsApp NEVER sent autonomously. Founder approval per message.\n"
        "- Consent or warm intro required. NO cold blasts.\n"
        "- Quiet hours: 21:00–08:00 KSA. Drafts not sent overnight.\n"
        "- 'reject' or doctrine-violation rows MUST NOT be sent.\n\n"
        "See `docs/content/WHATSAPP_TEMPLATES.md` for the canonical journey "
        "(10 templates from warm-intro → retainer offer).\n\n"
        "---\n\n"
    )

    accepted = deprioritized = rejected = 0
    for row in rows:
        q = _qualify(
            role=row.get("role", ""),
            sector=row.get("sector", ""),
            relationship=row.get("relationship", "cold"),
            notes=row.get("notes", ""),
        )
        if q["decision"] == "accept":
            accepted += 1
        elif q["decision"] in ("reject", "refer_out"):
            rejected += 1
        else:
            deprioritized += 1
        lines.append(_render(row, q))

    lines.append(
        f"## Summary\n\n"
        f"- Total: {len(rows)} contacts\n"
        f"- ✅ Accept (send today): {accepted}\n"
        f"- 🔵 Diagnostic_only / reframe: {deprioritized}\n"
        f"- 🔴 Reject / refer_out (DO NOT SEND): {rejected}\n\n"
        f"_Estimated outcomes are not guaranteed outcomes / "
        f"النتائج التقديرية ليست نتائج مضمونة._\n"
    )

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"✓ Wrote {len(rows)} WhatsApp drafts to {out_path}")
    print(f"  - accept: {accepted}")
    print(f"  - diagnostic_only/reframe: {deprioritized}")
    print(f"  - reject/refer_out (DO NOT SEND): {rejected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
