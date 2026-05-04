#!/usr/bin/env python3
"""
cron_auto_followup.py — autonomous follow-up generator.

Finds prospects with status=messaged where last_message_at > N days,
generates an LLM follow-up draft (or fallback), and adds it to the
Approval Queue as a high-risk, approval_required ProofEvent.

The founder approves → /actions/{id}/approve → auto_executor sends
(if email gate open) or keeps as draft for manual paste.

Usage:
    python scripts/cron_auto_followup.py            # default 3-day stale
    python scripts/cron_auto_followup.py --days 5
    python scripts/cron_auto_followup.py --dry-run

Recommended Railway cron: daily at 10:00 KSA (07:00 UTC).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime, timedelta, timezone

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("cron_auto_followup")


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


async def _run(days_stale: int, dry_run: bool) -> dict:
    from sqlalchemy import select
    from auto_client_acquisition.intelligence.smart_drafter import get_drafter
    from auto_client_acquisition.revenue_company_os.proof_ledger import (
        record as record_proof,
    )
    from db.models import CustomerRecord, ProspectRecord
    from db.session import get_session

    cutoff = _now() - timedelta(days=days_stale)
    drafter = get_drafter()

    findings = {
        "as_of": _now().isoformat(),
        "days_stale": days_stale,
        "scanned": 0,
        "stale_found": 0,
        "drafts_queued": 0,
        "errors": [],
    }

    async with get_session() as session:
        rows = list((await session.execute(
            select(ProspectRecord).where(
                ProspectRecord.status == "messaged",
                ProspectRecord.last_message_at <= cutoff,
            )
            .limit(50)
        )).scalars().all())
        findings["scanned"] = len(rows)
        findings["stale_found"] = len(rows)

        for p in rows:
            # Brain context: most-recent customer or empty (ours-as-default)
            cust = None
            if getattr(p, "customer_id", None):
                cust = (await session.execute(
                    select(CustomerRecord).where(CustomerRecord.id == p.customer_id)
                )).scalar_one_or_none()
            brain = {}
            if cust is not None:
                brain = {
                    "company_name": getattr(cust, "company_name", "") or "",
                    "offer_ar": getattr(cust, "offer_ar", None) or "خدمات الشركة",
                    "ideal_customer_ar": getattr(cust, "ideal_customer_ar", None) or "B2B",
                    "tone_ar": getattr(cust, "tone_ar", "professional_saudi_arabic"),
                    "forbidden_claims": list(getattr(cust, "forbidden_claims", []) or []),
                }

            days = (
                (_now() - p.last_message_at).days
                if p.last_message_at else days_stale
            )

            fallback = (
                f"السلام عليكم {p.name or ''}، تذكير سريع — الأسبوع مزدحم. "
                f"لو ما يناسب، تمام. لو حابب نختصر: 1-page summary أرسله؟ "
                f"(STOP للإلغاء)"
            )

            try:
                r = await drafter.draft_followup(
                    brain, days_since_last=days, fallback=fallback,
                )
                draft_text = r.text or fallback
            except Exception as exc:  # noqa: BLE001
                log.warning("drafter_failed prospect=%s err=%s", p.id, exc)
                findings["errors"].append({"prospect_id": p.id, "error": str(exc)[:200]})
                draft_text = fallback

            if dry_run:
                log.info(
                    "DRY-RUN would queue followup for prospect=%s (days=%d)",
                    p.id, days,
                )
                continue

            try:
                proof = await record_proof(
                    session,
                    unit_type="followup_created",
                    customer_id=p.customer_id or p.id,
                    actor="cron_auto_followup",
                    approval_required=True,
                    approved=False,
                    risk_level="medium",
                    meta={
                        "draft_text": draft_text,
                        "channel": "email_draft",
                        "prospect_id": p.id,
                        "company": p.company,
                        "name": p.name,
                        "to_email": p.contact_email,
                        "subject": f"متابعة — {p.company or ''}",
                        "days_since_last_message": days,
                        "auto_generated_by": "cron_auto_followup",
                    },
                )
                findings["drafts_queued"] += 1
                log.info(
                    "queued_followup prospect=%s event_id=%s used_llm=%s",
                    p.id, proof.id, getattr(r, "used_llm", False),
                )
            except Exception as exc:  # noqa: BLE001
                log.warning("queue_failed prospect=%s err=%s", p.id, exc)
                findings["errors"].append({"prospect_id": p.id, "error": str(exc)[:200]})

        if not dry_run:
            await session.commit()

    return findings


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=3,
                   help="Days since last_message_at to consider stale (default 3)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()
    try:
        result = asyncio.run(_run(args.days, args.dry_run))
    except Exception as exc:  # noqa: BLE001
        log.error("cron_failed err=%s", exc)
        if not args.quiet:
            print(json.dumps({"ok": False, "error": str(exc)[:300]}, ensure_ascii=False))
        return 1
    if not args.quiet:
        print(json.dumps({"ok": True, **result}, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
