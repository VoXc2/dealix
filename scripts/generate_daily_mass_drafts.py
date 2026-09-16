"""
Standalone script — generates 100+ bilingual outreach drafts daily.

Usage:
    python3 scripts/generate_daily_mass_drafts.py [options]

Options:
    --sectors   all|sector1,sector2,...   default: all
    --count     N                         default: 120  (min: 100)
    --date      YYYY-MM-DD                default: today
    --dry-run                             print to stdout, no file writes
    --gmail-push                          create Gmail drafts via API (drafts.create only)
    --limit     N                         max Gmail drafts to create, default: 50
    --targets   PATH                      CSV path, default: data/targets/saudi_sector_targets.csv
    --lang      ar|en|both                default: both

All outputs are DRAFT_ONLY. Nothing is sent automatically.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

# Optional internal imports — degrade gracefully if unavailable.
try:
    import yaml as _yaml  # type: ignore
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False

# ---------------------------------------------------------------------------
# Repo root resolution
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = _SCRIPT_DIR.parent

# ---------------------------------------------------------------------------
# Sector catalogue
# ---------------------------------------------------------------------------

SECTORS: list[str] = [
    "real_estate",
    "clinics",
    "training_centers",
    "agencies",
    "restaurants",
    "logistics",
    "b2b_services",
    "construction",
    "hospitality",
    "saas",
    "retail",
    "law_accounting",
]

SECTOR_LABELS_AR: dict[str, str] = {
    "real_estate": "العقار والتطوير",
    "clinics": "العيادات والرعاية الصحية",
    "training_centers": "مراكز التدريب",
    "agencies": "وكالات التسويق",
    "restaurants": "المطاعم والضيافة",
    "logistics": "الخدمات اللوجستية",
    "b2b_services": "الخدمات المهنية B2B",
    "construction": "المقاولات والإنشاء",
    "hospitality": "الفنادق والسياحة",
    "saas": "تقنية المعلومات والبرمجيات",
    "retail": "التجزئة والتجارة",
    "law_accounting": "القانون والمحاسبة",
}

ANGLES_AR: dict[str, str] = {
    "real_estate": (
        "leads العقارية الواردة عبر واتساب تضيع بدون نظام متابعة. "
        "Dealix يبني لكم Revenue OS يحوّل كل استفسار إلى pipeline مرئي يومياً."
    ),
    "clinics": (
        "حجوزات العيادة تأتي من واتساب وتليفون وإنستغرام — بدون نظام. "
        "Dealix يربط الاستقبال والتقييمات والحجوزات في مسار واحد."
    ),
    "training_centers": (
        "التسجيل في الدورات يتم يدوياً، والـ leads تضيع. "
        "Dealix يبني لكم Growth Engine يتابع كل مسجل من أول استفسار حتى الشهادة."
    ),
    "agencies": (
        "تقارير العملاء تُكتب يدوياً كل أسبوع. "
        "Dealix يبني Command Center للوكالة — كل عميل، كل مهمة، كل نتيجة في مكان واحد."
    ),
    "restaurants": (
        "تقييمات جوجل تتراكم بدون ردود منظمة. "
        "Dealix يبني Review Intelligence OS يحوّل كل تقييم إلى فرصة تحسين مع ردود جاهزة للمراجعة."
    ),
    "logistics": (
        "طلبات الشحن والتسعير تتضيع في الواتساب. "
        "Dealix يبني Sales Pipeline يجمع كل RFQ ويفرز الجاد منها للمتابعة الفورية."
    ),
    "b2b_services": (
        "عروض الأسعار تُكتب يدوياً وبطيئة، والعملاء المحتملون يرحلون. "
        "Dealix يبني Proposal Builder يُصدر عروضاً احترافية خلال دقائق."
    ),
    "construction": (
        "طلبات تسعير المشاريع تتضيع. "
        "Dealix يبني نظام استقبال RFQ يجمع المواصفات والميزانية ويفرز الجاد للفريق."
    ),
    "hospitality": (
        "حجوزات الفعاليات والقاعات تحتاج رداً فورياً. "
        "Dealix يبني Event Booking OS يرد خلال ثوانٍ ويحجز المواعيد آلياً."
    ),
    "saas": (
        "inbound leads من السوق السعودي تحتاج رداً بالعربي الخليجي. "
        "Dealix يبني لكم Sales AI Rep يرد فورياً ويؤهل العميل."
    ),
    "retail": (
        "شكاوى العملاء وتقييمات المنتجات تتراكم. "
        "Dealix يبني Customer Success OS يحوّل الشكاوى إلى فرص احتفاظ."
    ),
    "law_accounting": (
        "استفسارات العملاء الجدد تضيع. "
        "Dealix يبني Inquiry Management System يرتب الاستفسارات ويُصدر عروض أسعار فورية."
    ),
}

ANGLES_EN: dict[str, str] = {
    "real_estate": (
        "Real estate leads coming through WhatsApp and calls are lost without a structured follow-up system. "
        "Dealix builds you a Revenue OS that turns every inquiry into a visible daily pipeline."
    ),
    "clinics": (
        "Clinic bookings arrive through WhatsApp, phone, and Instagram — no system connecting them. "
        "Dealix builds a unified intake to booking to review management OS."
    ),
    "training_centers": (
        "Course registrations are manual and slow, leads fall through. "
        "Dealix builds a Growth Engine that tracks every prospect from first inquiry to certificate."
    ),
    "agencies": (
        "Client reports are written manually each week. "
        "Dealix builds an Agency Command Center — every client, every task, every result in one dashboard."
    ),
    "restaurants": (
        "Google reviews pile up without organized responses. "
        "Dealix builds a Review Intelligence OS that turns every review into an improvement opportunity."
    ),
    "logistics": (
        "Shipping RFQs get lost in WhatsApp. "
        "Dealix builds a Sales Pipeline that captures every RFQ and surfaces the serious ones for immediate follow-up."
    ),
    "b2b_services": (
        "Proposals are written manually and slowly — prospects leave for competitors. "
        "Dealix builds a Proposal Builder that generates professional bilingual proposals in minutes."
    ),
    "construction": (
        "Project pricing requests get lost. "
        "Dealix builds an RFQ intake system that collects specs, budgets, and timelines — sorted by priority for your team."
    ),
    "hospitality": (
        "Event and venue bookings need immediate responses. "
        "Dealix builds an Event Booking OS that responds instantly and manages your calendar automatically."
    ),
    "saas": (
        "Saudi inbound leads need a response in Gulf Arabic, not generic English. "
        "Dealix builds you a bilingual Sales AI Rep that responds in seconds."
    ),
    "retail": (
        "Customer complaints and product reviews accumulate. "
        "Dealix builds a Customer Success OS that turns complaints into retention opportunities."
    ),
    "law_accounting": (
        "New client inquiries get lost. "
        "Dealix builds an Inquiry Management System that organizes leads and issues instant professional proposals."
    ),
}

SUBJECT_AR_TEMPLATE = "Dealix — نظام تشغيل ذكي لـ {company}"
SUBJECT_EN_TEMPLATE = "Dealix — AI Operating System for {company}"

BODY_AR_TEMPLATE = (
    "السلام عليكم {company}،\n\n"
    "{angle}\n\n"
    "نبدأ بتشخيص مختصر. بعد discovery نجهّز نطاق Revenue Command Pilot بمدة ومعايير قبول خاصة بالعميل وquote موثقًا للمراجعة.\n"
    "تناسبكم 20 دقيقة هذا الأسبوع؟\n\n"
    "سامي\n"
    "Dealix — https://dealix.me\n"
    "العرض: {presentation_link}\n"
    "حجز موعد: https://calendly.com/sami-assiri11/dealix-demo\n\n"
    "[DRAFT_ONLY — يتطلب موافقة قبل الإرسال]"
)

BODY_EN_TEMPLATE = (
    "Hello {company},\n\n"
    "{angle}\n\n"
    "We start with a bounded diagnostic. After discovery, we prepare a customer-specific Revenue Command Pilot scope and documented quote for review.\n"
    "Would 20 minutes this week work for you?\n\n"
    "Sami\n"
    "Dealix — https://dealix.me\n"
    "Proposal: {presentation_link}\n"
    "Book a call: https://calendly.com/sami-assiri11/dealix-demo\n\n"
    "[DRAFT_ONLY — requires approval before sending]"
)

PRESENTATION_LINK = "https://dealix.me/proposal"


# ---------------------------------------------------------------------------
# Optional YAML loader
# ---------------------------------------------------------------------------


def _load_yaml_templates(path: Path) -> dict[str, Any] | None:
    """Load outreach templates from YAML. Returns None if unavailable."""
    if not _YAML_AVAILABLE:
        return None
    if not path.exists():
        return None
    try:
        with path.open(encoding="utf-8") as fh:
            return _yaml.safe_load(fh)
    except Exception:  # YAML unavailable or malformed — caller falls back to ANGLES_* dicts
        return None


# ---------------------------------------------------------------------------
# CSV target loader
# ---------------------------------------------------------------------------


def load_targets(csv_path: Path) -> list[dict[str, str]]:
    """
    Load companies from a CSV file.

    Expected columns (any extras are ignored):
        company, sector, city, email, contact_name

    Returns a list of dicts — empty list if file is absent.
    """
    if not csv_path.exists():
        return []
    rows: list[dict[str, str]] = []
    with csv_path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append({k.strip().lower(): (v or "").strip() for k, v in row.items()})
    return rows


# ---------------------------------------------------------------------------
# Draft rendering
# ---------------------------------------------------------------------------


def _angle_ar(sector: str, yaml_data: dict[str, Any] | None) -> str:
    if yaml_data:
        try:
            tmpl = yaml_data.get("email", {}).get("body_ar", "")
            if tmpl and "{angle}" not in tmpl:
                # yaml provides a full body — extract angle-like content
                pass
        except Exception:  # angle extraction is best-effort; fall back to ANGLES_AR dict
            pass
    return ANGLES_AR.get(sector, ANGLES_AR["b2b_services"])


def _angle_en(sector: str, yaml_data: dict[str, Any] | None) -> str:
    return ANGLES_EN.get(sector, ANGLES_EN["b2b_services"])


def render_draft(
    company: dict[str, str],
    language: str,
    yaml_data: dict[str, Any] | None,
    draft_index: int,
) -> dict[str, Any]:
    """
    Render a single draft for one company in one language.

    Returns a flat dict suitable for CSV row + gmail_queue entry.
    """
    sector = company.get("sector", "b2b_services").strip() or "b2b_services"
    company_name = company.get("company", company.get("company_name", "الشركة")).strip() or "الشركة"
    city = company.get("city", "").strip()
    contact_name = company.get("contact_name", "").strip()
    email_addr = company.get("email", "").strip()

    now_iso = datetime.now(UTC).isoformat(timespec="seconds")

    if language == "ar":
        subject = SUBJECT_AR_TEMPLATE.format(company=company_name)
        angle = _angle_ar(sector, yaml_data)
        body = BODY_AR_TEMPLATE.format(
            company=company_name,
            angle=angle,
            presentation_link=PRESENTATION_LINK,
        )
    else:
        subject = SUBJECT_EN_TEMPLATE.format(company=company_name)
        angle = _angle_en(sector, yaml_data)
        body = BODY_EN_TEMPLATE.format(
            company=company_name,
            angle=angle,
            presentation_link=PRESENTATION_LINK,
        )

    draft_id = f"draft_{draft_index:04d}"

    return {
        "id": draft_id,
        "company": company_name,
        "sector": sector,
        "city": city,
        "contact_name": contact_name,
        "email": email_addr,
        "language": language,
        "subject": subject,
        "body": body,
        "channel": "email",
        "status": "draft_only",
        "approval_required": True,
        "created_at": now_iso,
    }


# ---------------------------------------------------------------------------
# Synthetic target generation (fallback when CSV is absent or small)
# ---------------------------------------------------------------------------


def _synthetic_targets(sectors: list[str], count: int) -> list[dict[str, str]]:
    """
    Produce synthetic target rows so the script always generates >= count drafts
    even without a real CSV file.
    """
    cities = ["الرياض", "جدة", "الدمام", "مكة المكرمة", "المدينة المنورة", "الخبر", "أبها"]
    rows: list[dict[str, str]] = []
    per_sector = max(1, (count // len(sectors)) + 1)
    idx = 0
    for sector in sectors:
        label = SECTOR_LABELS_AR.get(sector, sector)
        for i in range(per_sector):
            idx += 1
            rows.append(
                {
                    "company": f"شركة {label} {idx}",
                    "sector": sector,
                    "city": cities[idx % len(cities)],
                    "email": "",
                    "contact_name": "",
                }
            )
    return rows


# ---------------------------------------------------------------------------
# Core generation logic
# ---------------------------------------------------------------------------


def generate_drafts(
    sectors: list[str],
    count: int,
    target_date: str,
    targets_path: Path,
    lang: str,
    yaml_data: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    """
    Generate at least `count` draft records across the requested sectors and languages.

    Returns a flat list of draft dicts.
    """
    raw_targets = load_targets(targets_path)

    # Filter to requested sectors
    if raw_targets:
        filtered = [r for r in raw_targets if r.get("sector", "") in sectors]
        if not filtered:
            filtered = raw_targets  # fallback: use all if no sector match
    else:
        filtered = []

    # Determine how many languages we need
    languages: list[str]
    if lang == "ar":
        languages = ["ar"]
    elif lang == "en":
        languages = ["en"]
    else:
        languages = ["ar", "en"]

    # We need enough target rows to reach `count` total drafts across all languages.
    target_rows_needed = max(1, (count + len(languages) - 1) // len(languages))

    # Interleave sectors so coverage is spread evenly across all 12 sectors
    import random
    from collections import defaultdict
    by_sector: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in filtered:
        by_sector[row.get("sector", "unknown")].append(row)

    interleaved: list[dict[str, str]] = []
    sector_lists = list(by_sector.values())
    max_len = max((len(s) for s in sector_lists), default=0)
    for i in range(max_len):
        for sl in sector_lists:
            if i < len(sl):
                interleaved.append(sl[i])

    # Pad with synthetic rows if real data is short
    if len(interleaved) < target_rows_needed:
        synthetic = _synthetic_targets(sectors, target_rows_needed - len(interleaved))
        interleaved = interleaved + synthetic

    # Trim / cycle to exact need
    combined: list[dict[str, str]] = []
    while len(combined) < target_rows_needed:
        combined.extend(interleaved)
    combined = combined[:target_rows_needed]

    drafts: list[dict[str, Any]] = []
    idx = 1
    for company in combined:
        for language in languages:
            if len(drafts) >= count:
                break
            draft = render_draft(company, language, yaml_data, idx)
            drafts.append(draft)
            idx += 1
        if len(drafts) >= count:
            break

    return drafts


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------


def write_markdown_drafts(
    drafts: list[dict[str, Any]],
    language: str,
    out_path: Path,
) -> None:
    """Write drafts for one language to a numbered markdown file."""
    lang_drafts = [d for d in drafts if d["language"] == language]
    lines: list[str] = [
        f"# مسودات يومية — {language.upper()}\n",
        f"**المجموع:** {len(lang_drafts)}\n\n---\n",
    ]
    for i, d in enumerate(lang_drafts, start=1):
        lines.append(f"## [{i}] {d['company']} — {d['sector']}")
        lines.append(f"**ID:** {d['id']}  ")
        lines.append(f"**Subject:** {d['subject']}  ")
        lines.append(f"**Status:** {d['status']} | approval_required: {d['approval_required']}")
        lines.append("")
        lines.append(d["body"])
        lines.append("\n---\n")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def write_csv_drafts(drafts: list[dict[str, Any]], out_path: Path) -> None:
    """Write all drafts to a CSV file."""
    fieldnames = ["id", "company", "sector", "city", "language", "subject", "body", "channel", "status"]
    with out_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for d in drafts:
            writer.writerow(d)


def write_gmail_queue(drafts: list[dict[str, Any]], out_path: Path, limit: int) -> None:
    """Write the Gmail-ready queue JSON (capped at limit entries)."""
    queue = []
    for d in drafts[:limit]:
        queue.append(
            {
                "id": d["id"],
                "company": d["company"],
                "sector": d["sector"],
                "language": d["language"],
                "subject": d["subject"],
                "body": d["body"],
                "status": "draft_only",
                "approval_required": True,
                "created_at": d["created_at"],
            }
        )
    out_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")


def write_summary(
    drafts: list[dict[str, Any]],
    target_date: str,
    out_path: Path,
) -> None:
    """Write a human-readable daily summary in Arabic."""
    ar_count = sum(1 for d in drafts if d["language"] == "ar")
    en_count = sum(1 for d in drafts if d["language"] == "en")
    companies = len({d["company"] for d in drafts})
    sector_counts: dict[str, int] = {}
    for d in drafts:
        sector_counts[d["sector"]] = sector_counts.get(d["sector"], 0) + 1

    sector_table_rows = "\n".join(
        f"| {SECTOR_LABELS_AR.get(s, s)} | {c} |"
        for s, c in sorted(sector_counts.items(), key=lambda x: -x[1])
    )

    summary = f"""# تقرير المسودات اليومية — {target_date}

## الملخص
- إجمالي المسودات: {len(drafts)}
- مسودات عربية: {ar_count}
- مسودات إنجليزية: {en_count}
- القطاعات: {len(sector_counts)}
- الشركات المستهدفة: {companies}

## توزيع القطاعات
| القطاع | عدد المسودات |
|--------|-------------|
{sector_table_rows}

## القاعدة الذهبية
[DRAFT_ONLY] جميع المسودات للمراجعة فقط — لا إرسال تلقائي.
يجب الحصول على موافقة صريحة قبل إرسال أي مسودة.
"""
    out_path.write_text(summary, encoding="utf-8")


# ---------------------------------------------------------------------------
# Optional Gmail push
# ---------------------------------------------------------------------------


def push_gmail_drafts(queue: list[dict[str, Any]], limit: int) -> int:
    """
    Create Gmail drafts using the Gmail API (drafts.create — never messages.send).

    Returns the number of drafts successfully created. Gracefully skips if
    credentials are not configured.
    """
    try:
        from google.oauth2.credentials import Credentials  # type: ignore
        from googleapiclient.discovery import build  # type: ignore
    except ImportError:
        print("  [gmail-push] google-api-python-client not installed — skipping.")
        return 0

    token_path = Path(os.getenv("GMAIL_TOKEN_PATH", str(REPO_ROOT / "token.json")))
    if not token_path.exists():
        print("  [gmail-push] No Gmail token found — skipping.")
        return 0

    import base64
    from email.mime.text import MIMEText

    try:
        creds = Credentials.from_authorized_user_file(str(token_path))
        service = build("gmail", "v1", credentials=creds, cache_discovery=False)
    except Exception as exc:
        print(f"  [gmail-push] Gmail auth failed: {exc}")
        return 0

    created = 0
    for item in queue[:limit]:
        try:
            mime = MIMEText(item["body"], "plain", "utf-8")
            mime["To"] = ""
            mime["Subject"] = item["subject"]
            raw = base64.urlsafe_b64encode(mime.as_bytes()).decode()
            service.users().drafts().create(  # type: ignore[attr-defined]
                userId="me",
                body={"message": {"raw": raw}},
            ).execute()
            created += 1
        except Exception as exc:
            print(f"  [gmail-push] Failed to create draft {item['id']}: {exc}")
    return created


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate daily bilingual outreach drafts (DRAFT_ONLY).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--sectors",
        default="all",
        help="Comma-separated sector keys, or 'all'. Default: all",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=120,
        help="Number of drafts to generate (min: 100). Default: 120",
    )
    parser.add_argument(
        "--date",
        default=str(date.today()),
        help="Target date YYYY-MM-DD. Default: today",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print drafts to stdout; do not write files.",
    )
    parser.add_argument(
        "--gmail-push",
        action="store_true",
        help="Create Gmail drafts via API (drafts.create only — never send).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Max Gmail drafts to create. Default: 50",
    )
    parser.add_argument(
        "--targets",
        default=str(REPO_ROOT / "data" / "targets" / "saudi_sector_targets.csv"),
        help="Path to targets CSV. Default: data/targets/saudi_sector_targets.csv",
    )
    parser.add_argument(
        "--lang",
        choices=["ar", "en", "both"],
        default="both",
        help="Language(s) to generate. Default: both",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    count = max(100, args.count)
    target_date = args.date
    targets_path = Path(args.targets)
    lang = args.lang

    # Resolve sectors
    if args.sectors.strip().lower() == "all":
        sectors = SECTORS
    else:
        requested = [s.strip() for s in args.sectors.split(",") if s.strip()]
        sectors = [s for s in requested if s in SECTORS]
        if not sectors:
            print(f"[warn] No valid sectors in '{args.sectors}' — using all.", file=sys.stderr)
            sectors = SECTORS

    # Load optional YAML templates
    yaml_path = REPO_ROOT / "business_autopilot" / "templates" / "outreach_templates_v2.yaml"
    yaml_data = _load_yaml_templates(yaml_path)
    if yaml_data:
        print(f"[info] Loaded YAML templates from {yaml_path}")
    else:
        print("[info] YAML templates not found — using built-in angle strings.")

    # Generate
    print(f"[info] Generating {count}+ drafts for {len(sectors)} sectors (lang={lang}) ...")
    drafts = generate_drafts(sectors, count, target_date, targets_path, lang, yaml_data)
    print(f"[info] Generated {len(drafts)} drafts.")

    if args.dry_run:
        for d in drafts:
            print(json.dumps(d, ensure_ascii=False))
        return 0

    # Create output directory
    out_dir = REPO_ROOT / "data" / "daily_drafts" / target_date
    out_dir.mkdir(parents=True, exist_ok=True)

    # Write files
    write_markdown_drafts(drafts, "ar", out_dir / "drafts_ar.md")
    write_markdown_drafts(drafts, "en", out_dir / "drafts_en.md")
    write_csv_drafts(drafts, out_dir / "drafts_all.csv")
    write_gmail_queue(drafts, out_dir / "gmail_queue.json", limit=args.limit)
    write_summary(drafts, target_date, out_dir / "summary.md")

    print(f"[info] Output written to {out_dir}/")

    if args.gmail_push:
        queue_path = out_dir / "gmail_queue.json"
        queue = json.loads(queue_path.read_text(encoding="utf-8"))
        print(f"[info] Pushing up to {args.limit} Gmail drafts (drafts.create only) ...")
        created = push_gmail_drafts(queue, args.limit)
        print(f"[info] Gmail drafts created: {created}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
