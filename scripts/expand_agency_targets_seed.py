#!/usr/bin/env python3
"""Ensure agency_accounts_seed.csv has at least N strategic rows (idempotent).

Default N=120 (soft). Use --wave2 for 150 rows · --wave3 for 200 (ABM prep, gtm_abm_wave1.yaml).
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.paths import AGENCY_TARGETS_CSV
from dealix.commercial_ops.targeting_csv import TARGET_FIELDS

DEFAULT_MIN_ROWS = 120
WAVE2_TARGET_ROWS = 150
WAVE3_TARGET_ROWS = 200
WAVE4_TARGET_ROWS = 250

_PROFILES: list[tuple[str, str, str, str, str]] = [
    ("agency_wedge", "العميل يسأل عن ROI بعد الحملة", "linkedin_manual", "A", "ten_lead_audit"),
    ("agency_wedge", "لا proof أسبوعي للعميل", "email_warm", "A", "agency_proof_pack"),
    ("direct_b2b", "متابعة أولى بطيئة", "email_warm", "B", "governed_diagnostic"),
    ("saas", "توسع AI بدون حوكمة", "linkedin_manual", "D", "executive_diagnostic"),
    ("crm_partner", "تنفيذ CRM قبل التشخيص", "email_warm", "C", "diagnostic_layer"),
    ("consulting_firm", "عملاء يطلبون أتمتة بلا أدلة", "email_warm", "A", "agency_proof_pack"),
    ("hospitality", "استفسارات MICE بلا owner", "phone_task", "B", "ten_lead_audit"),
    ("real_estate_developer", "جودة leads inbound", "email_warm", "B", "ten_lead_audit"),
    ("agency_partner", "co-sell عميل واحد", "partner_intro", "A", "partner_sprint"),
    ("marketing_agency", "ضغط inbound", "linkedin_manual", "A", "ten_lead_audit"),
    ("executive_governance", "مخاطر توسع AI", "partner_intro", "D", "executive_diagnostic"),
    ("fintech", "leads مالية بلا تسليم Proof", "email_warm", "B", "governed_diagnostic"),
    ("healthcare", "متابعة مريض/عميل بلا owner", "phone_task", "B", "ten_lead_audit"),
    ("retail", "حملات موسمية بلا إغلاق", "linkedin_manual", "A", "agency_proof_pack"),
    ("education", "تسجيل inbound بلا متابعة", "inbound", "B", "ten_lead_audit"),
    ("logistics", "عروض B2B بلا evidence", "email_warm", "C", "diagnostic_layer"),
    ("media_buying", "تقارير media بلا post-lead ops", "linkedin_manual", "A", "ten_lead_audit"),
    ("ecommerce", "سلة متروكة بلا قرار إيراد", "email_warm", "B", "governed_diagnostic"),
    ("government_vendor", "مناقصات بلا owner متابعة", "partner_intro", "D", "executive_diagnostic"),
    ("insurance", "وثائق leads بلا إغلاق", "email_warm", "B", "ten_lead_audit"),
    ("telecom_b2b", "حسابات enterprise بلا proof", "linkedin_manual", "D", "executive_diagnostic"),
    ("construction", "عروض مشاريع بلا متابعة", "phone_task", "B", "governed_diagnostic"),
    ("automotive_dealer", "استفسارات showrooms", "inbound", "B", "ten_lead_audit"),
]


def _existing_companies(rows: list[dict[str, str]]) -> set[str]:
    return {(r.get("company") or "").strip().lower() for r in rows}


def _append_rows(
    rows: list[dict[str, str]], *, need: int, min_rows: int
) -> list[dict[str, str]]:
    companies = _existing_companies(rows)
    n = len(rows)
    slot = n + 1
    statuses = ["not_contacted", "message_drafted", "sent_manual", "replied", "meeting_booked"]
    priorities = ["high", "medium", "low"]
    channels_extra = ["inbound", "phone_task"]
    added = 0
    while len(rows) < min_rows and added < need + 20:
        seg, pain, channel, motion, offer = _PROFILES[(slot - 1) % len(_PROFILES)]
        if slot % 5 == 0:
            channel = channels_extra[slot % len(channels_extra)]
        company = f"هدف استراتيجي {slot}"
        key = company.lower()
        if key in companies:
            slot += 1
            continue
        rows.append(
            {
                "company": company,
                "contact": f"مدير حسابات {slot}",
                "segment": seg,
                "pain_hypothesis": pain,
                "channel": channel,
                "motion": motion,
                "offer_id": offer,
                "status": statuses[slot % len(statuses)],
                "next_action": "مسودة — موافقة قبل الإرسال",
                "next_action_date": "",
                "priority": priorities[slot % len(priorities)],
                "notes": f"seed strategic slot {slot}",
            }
        )
        companies.add(key)
        slot += 1
        added += 1
    return rows


def expand_targets(*, min_rows: int = DEFAULT_MIN_ROWS) -> tuple[int, int]:
    """Return (before_count, after_count)."""
    path = AGENCY_TARGETS_CSV
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    before = len(rows)
    if before >= min_rows:
        return before, before
    rows = _append_rows(rows, need=min_rows - before, min_rows=min_rows)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=TARGET_FIELDS)
        w.writeheader()
        w.writerows(rows)
    return before, len(rows)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--min-rows",
        "--target",
        type=int,
        default=DEFAULT_MIN_ROWS,
        dest="min_rows",
        help=f"Minimum rows (default {DEFAULT_MIN_ROWS}; wave2={WAVE2_TARGET_ROWS})",
    )
    p.add_argument(
        "--wave2",
        action="store_true",
        help=f"Expand to ABM wave-2 pool ({WAVE2_TARGET_ROWS} rows)",
    )
    p.add_argument(
        "--wave3",
        action="store_true",
        help=f"Expand to wave-3 prep pool ({WAVE3_TARGET_ROWS} rows, inbound/AEO gate)",
    )
    p.add_argument(
        "--wave4",
        action="store_true",
        help=f"Inbound/AEO prep pool ({WAVE4_TARGET_ROWS} rows — after paid proof gate)",
    )
    args = p.parse_args()
    if args.wave4:
        min_rows = WAVE4_TARGET_ROWS
    elif args.wave3:
        min_rows = WAVE3_TARGET_ROWS
    elif args.wave2:
        min_rows = WAVE2_TARGET_ROWS
    else:
        min_rows = max(80, args.min_rows)

    path = AGENCY_TARGETS_CSV
    if not path.is_file():
        print(f"FAIL: missing {path}")
        return 1
    before, after = expand_targets(min_rows=min_rows)
    if before >= min_rows:
        print(f"OK: rows={before} (already >= {min_rows})")
        return 0
    print(f"OK: expanded {before} -> {after} rows at {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
