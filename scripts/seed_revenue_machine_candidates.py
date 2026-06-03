#!/usr/bin/env python3
"""Seed Postgres accounts for revenue-machine (allowed_use + business contacts).

Idempotent — IDs prefixed gtm_seed_. Safe alongside demo_acc_* rows.
See docs/ops/DATA_LAKE_PLAYBOOK.md.

  python scripts/seed_revenue_machine_candidates.py
  DEALIX_GTM_SEED_PURGE=true python scripts/seed_revenue_machine_candidates.py
"""

from __future__ import annotations

import asyncio
import os
import sys
from datetime import UTC, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from sqlalchemy import select

    from db.models import AccountRecord, ContactRecord, LeadScoreRecord
    from db.session import async_session_factory, init_db
except ImportError as exc:
    print(f"ERROR: {exc}")
    sys.exit(2)

_PREFIX = "gtm_seed_"


def _utcnow() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


# (id_suffix, company, domain, city, sector, dq, email_local, priority)
GTM_ACCOUNTS = [
    ("001", "وكالة نبض الرقمية", "nabdigital.sa", "Riyadh", "marketing_agency", 82, "ceo", "P1"),
    ("002", "وكالة إبداع الخليج", "ibdaa-gulf.sa", "Jeddah", "marketing_agency", 78, "growth", "P1"),
    ("003", "استوديو محتوى الرياض", "content-riyadh.sa", "Riyadh", "marketing_agency", 74, "ops", "P2"),
    ("004", "مختبر SaaS السعودي", "saudi-saas-lab.sa", "Riyadh", "saas", 80, "founder", "P1"),
    ("005", "منصة تدفق B2B", "tadflow.sa", "Riyadh", "saas", 76, "sales", "P1"),
    ("006", "حلول سحابة الخليج", "gulf-cloud.sa", "Dammam", "saas", 72, "ceo", "P2"),
    ("007", "استشارات نمو الأعمال", "ngrowth.sa", "Riyadh", "consulting_firm", 77, "partner", "P1"),
    ("008", "مجموعة استشارات المركز", "center-consult.sa", "Jeddah", "consulting_firm", 73, "director", "P2"),
    ("009", "أكاديمية قادة المستقبل", "future-leaders.sa", "Riyadh", "training_center", 70, "director", "P2"),
    ("010", "مركز مهارات الشركات", "corp-skills.sa", "Riyadh", "training_center", 68, "sales", "P2"),
    ("011", "تطوير أفق العقاري", "ofuq-re.sa", "Riyadh", "real_estate_developer", 84, "sales", "P1"),
    ("012", "مشاريع الواحة", "oasis-projects.sa", "Jeddah", "real_estate_developer", 79, "marketing", "P1"),
    ("013", "فندق قمة الرياض", "qimah-hotel.sa", "Riyadh", "hospitality", 75, "gm", "P2"),
    ("014", "قاعة ليالي جدة", "layali-events.sa", "Jeddah", "hospitality", 71, "events", "P2"),
    ("015", "شحن الخليج السريع", "gulf-fast-log.sa", "Dammam", "logistics", 74, "ops", "P2"),
    ("016", "لوجستيات نجد", "najd-logistics.sa", "Riyadh", "logistics", 70, "commercial", "P2"),
    ("017", "وكالة Rafal للإبداع", "rafal-creative.sa", "Jeddah", "marketing_agency", 81, "ceo", "P1"),
    ("018", "وكالة فعل التسويق", "fail-marketing.sa", "Riyadh", "marketing_agency", 79, "yousef", "P1"),
    ("019", "تقنية مكدس", "makdstack.sa", "Riyadh", "saas", 77, "cto", "P1"),
    ("020", "شركة حوكمة AI", "ai-gov.sa", "Riyadh", "consulting_firm", 75, "founder", "P1"),
]


async def _purge() -> int:
    count = 0
    async with async_session_factory() as session:
        for model in (LeadScoreRecord, ContactRecord, AccountRecord):
            rows = (await session.execute(
                select(model).where(model.id.like(f"{_PREFIX}%"))
            )).scalars().all()
            for row in rows:
                await session.delete(row)
                count += 1
        await session.commit()
    return count


async def main() -> int:
    if not os.getenv("DATABASE_URL"):
        print("ERROR: set DATABASE_URL")
        return 2

    await init_db()
    if os.getenv("DEALIX_GTM_SEED_PURGE", "").lower() in {"1", "true", "yes"}:
        n = await _purge()
        print(f"purged {n} gtm_seed_* rows")

    now = _utcnow()
    async with async_session_factory() as session:
        for suffix, name, domain, city, sector, dq, local, priority in GTM_ACCOUNTS:
            aid = f"{_PREFIX}acc_{suffix}"
            cid = f"{_PREFIX}ct_{suffix}"
            lid = f"{_PREFIX}ls_{suffix}"
            email = f"{local}@{domain}"

            if not (await session.execute(
                select(AccountRecord).where(AccountRecord.id == aid)
            )).scalar_one_or_none():
                session.add(
                    AccountRecord(
                        id=aid,
                        company_name=name,
                        normalized_name=name.lower().replace(" ", "")[:120],
                        domain=domain,
                        website=f"https://{domain}",
                        city=city,
                        country="SA",
                        sector=sector,
                        google_place_id=f"ChIJ_gtm_{suffix}",
                        source_count=1,
                        best_source="gtm_seed",
                        risk_level="low" if dq >= 78 else "medium",
                        status="enriched",
                        data_quality_score=float(dq),
                        extra={
                            "allowed_use": "business_contact_research_only",
                            "consent_status": "legitimate_interest_business_directory",
                            "source_type": "public",
                            "gtm_seed": True,
                            "warm_outreach_eligible": False,
                        },
                    )
                )

            if not (await session.execute(
                select(ContactRecord).where(ContactRecord.id == cid)
            )).scalar_one_or_none():
                session.add(
                    ContactRecord(
                        id=cid,
                        account_id=aid,
                        name=f"مسؤول {name[:40]}",
                        role="Director",
                        email=email,
                        phone=f"+96650{suffix.zfill(7)}",
                        source="gtm_seed",
                        consent_status="legitimate_interest",
                        opt_out=False,
                        risk_level="low",
                    )
                )

            if not (await session.execute(
                select(LeadScoreRecord).where(LeadScoreRecord.id == lid)
            )).scalar_one_or_none():
                fit = 22 + (int(suffix) % 8)
                intent = 18 + (int(suffix) % 5)
                urgency = 14 + (int(suffix) % 6)
                total = fit + intent + urgency + 10
                session.add(
                    LeadScoreRecord(
                        id=lid,
                        account_id=aid,
                        fit_score=float(fit),
                        intent_score=float(intent),
                        urgency_score=float(urgency),
                        risk_score=8.0,
                        total_score=float(total),
                        priority=priority,
                        recommended_channel="email_warm"
                        if sector in {"saas", "marketing_agency", "consulting_firm"}
                        else "phone_task",
                        reason=f"gtm_seed: {sector} → {priority}",
                        created_at=now,
                    )
                )

        await session.commit()

    print(f"OK · {len(GTM_ACCOUNTS)} gtm_seed accounts (enriched + contacts + scores)")
    print("Next: POST /api/v1/automation/revenue-machine/run with approval_mode=draft_only")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
