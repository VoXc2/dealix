"""
Self-Ops Runner — Dealix uses Dealix on itself.

Daily loop:
  1. Ensure Dealix's own CustomerRecord exists (with DEALIX_BRAIN populated)
  2. Generate today's segment + 3-5 LLM-drafted intros for that segment
  3. Add the intros to the Approval Queue (so the founder reviews + sends)
  4. Snapshot the day's plan into a DealixSelfOpsRunRecord-equivalent
     (we use a ProofEvent with unit_type=target_ranked + meta to track)

Pure orchestration. Calls existing primitives:
  - SmartDrafter.draft_outreach_message
  - proof_ledger.record (for queueing)
  - intelligence.channel_orchestrator (for channel pick)

Returns SelfOpsResult with: prospects_seeded, drafts_generated, errors.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

log = logging.getLogger(__name__)


@dataclass
class SelfOpsResult:
    customer_id: str | None = None
    prospects_seeded: int = 0
    drafts_generated: int = 0
    drafts_used_llm: int = 0
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:14]}"


async def _ensure_dealix_customer(session) -> Any:
    """Idempotent: ensure Dealix's own CustomerRecord exists with Brain seeded."""
    from sqlalchemy import select
    from auto_client_acquisition.self_ops.dealix_brain import DEALIX_BRAIN
    from db.models import CustomerRecord

    cust = (await session.execute(
        select(CustomerRecord).where(CustomerRecord.id == "cus_dealix_self")
    )).scalar_one_or_none()
    if cust is not None:
        return cust

    cust = CustomerRecord(
        id="cus_dealix_self",
        plan="growth",
        onboarding_status="active",
        churn_risk="low",
        company_name=DEALIX_BRAIN["company_name"],
        website=DEALIX_BRAIN["website"],
        sector=DEALIX_BRAIN["sector"],
        city=DEALIX_BRAIN["city"],
        offer_ar=DEALIX_BRAIN["offer_ar"],
        ideal_customer_ar=DEALIX_BRAIN["ideal_customer_ar"],
        average_deal_value_sar=float(DEALIX_BRAIN["average_deal_value_sar"]),
        approved_channels=list(DEALIX_BRAIN["approved_channels"]),
        blocked_channels=list(DEALIX_BRAIN["blocked_channels"]),
        tone_ar=DEALIX_BRAIN["tone_ar"],
        forbidden_claims=list(DEALIX_BRAIN["forbidden_claims"]),
        current_service_id=DEALIX_BRAIN["current_service_id"],
    )
    session.add(cust)
    await session.commit()
    return cust


async def _seed_prospects(session, count: int = 6) -> int:
    """Seed N synthetic ICP-fit prospects if Dealix has < count active prospects."""
    from sqlalchemy import select
    from auto_client_acquisition.self_ops.dealix_brain import expand_seed_prospects
    from db.models import ProspectRecord

    existing = list((await session.execute(
        select(ProspectRecord).where(
            ProspectRecord.actor == "self_ops",
            ProspectRecord.status == "new",
        )
    )).scalars().all())

    if len(existing) >= count:
        return 0  # already enough seeded

    needed = count - len(existing)
    seeds = expand_seed_prospects(start_n=len(existing) + 1, count=needed)
    for s in seeds:
        prospect = ProspectRecord(
            id=_new_id("prs"),
            name=s["name"],
            company=s["company"],
            sector=s.get("sector"),
            city=s.get("city"),
            relationship_type=s["relationship_type"],
            status="new",
            next_step_ar=s["next_step_ar"],
            next_step_due_at=_now(),
            expected_value_sar=float(s["expected_value_sar"]),
            source_type=s["source_type"],
            consent_status="none",
            allowed_channels=["linkedin_manual"],
            blocked_channels=["whatsapp_outbound"],
            human_approval_required=True,
            actor="self_ops",
            customer_id="cus_dealix_self",
        )
        session.add(prospect)
    await session.commit()
    return needed


async def _queue_intros(session, customer_id: str, prospects: list, max_intros: int = 5) -> tuple[int, int]:
    """Generate LLM intros for the first N prospects + add to approval queue.
    Returns (drafts_total, drafts_used_llm)."""
    from auto_client_acquisition.intelligence.smart_drafter import get_drafter
    from auto_client_acquisition.revenue_company_os.proof_ledger import (
        record as record_proof,
    )
    from auto_client_acquisition.self_ops.dealix_brain import DEALIX_BRAIN

    drafter = get_drafter()
    drafts_total = 0
    drafts_used_llm = 0

    for p in prospects[:max_intros]:
        fallback = (
            f"السلام عليكم، اسمي [اسم founder] من Dealix. "
            f"شفت أنكم من {p.sector or 'B2B'} في {p.city or 'السعودية'}. "
            f"عندي نظام عربي للنمو مع PDPL compliance. "
            f"١٥ دقيقة هذا الأسبوع لأشاركك Diagnostic مجاني؟ (STOP للإلغاء)"
        )
        try:
            r = await drafter.draft_outreach_message(
                DEALIX_BRAIN,
                prospect_hint=f"{p.name} في {p.sector or 'B2B'}، {p.city or 'السعودية'}",
                fallback=fallback,
            )
            draft_text = r.text
            if r.used_llm:
                drafts_used_llm += 1
        except Exception as exc:  # noqa: BLE001
            log.warning("self_ops_draft_failed prospect=%s err=%s", p.id, exc)
            draft_text = fallback

        try:
            await record_proof(
                session,
                unit_type="draft_created",
                customer_id=customer_id,
                actor="self_ops",
                approval_required=True,
                approved=False,
                risk_level="low",
                meta={
                    "draft_text": draft_text,
                    "channel": "linkedin_manual",
                    "prospect_id": p.id,
                    "company": p.company,
                    "name": p.name,
                    "auto_generated_by": "self_ops_runner",
                },
            )
            drafts_total += 1
        except Exception as exc:  # noqa: BLE001
            log.warning("self_ops_queue_failed prospect=%s err=%s", p.id, exc)

    await session.commit()
    return drafts_total, drafts_used_llm


async def daily_self_ops(*, prospect_target: int = 6, intro_count: int = 5) -> SelfOpsResult:
    """Run Dealix's own daily-ops on itself.

    1. Ensure Dealix's CustomerRecord (Brain seeded)
    2. Seed prospects if needed
    3. Generate LLM intros for top N prospects
    4. Add to Approval Queue
    """
    from sqlalchemy import select
    from db.models import ProspectRecord
    from db.session import get_session

    result = SelfOpsResult()

    try:
        async with get_session() as session:
            cust = await _ensure_dealix_customer(session)
            result.customer_id = cust.id

            seeded = await _seed_prospects(session, count=prospect_target)
            result.prospects_seeded = seeded

            # Pull active 'new' prospects to generate intros for
            rows = list((await session.execute(
                select(ProspectRecord).where(
                    ProspectRecord.customer_id == cust.id,
                    ProspectRecord.status == "new",
                )
                .limit(intro_count)
            )).scalars().all())

            total, llm_count = await _queue_intros(session, cust.id, rows, max_intros=intro_count)
            result.drafts_generated = total
            result.drafts_used_llm = llm_count
            result.notes.append(
                f"Dealix self-ops: seeded {seeded} prospects, generated {total} intros "
                f"({llm_count} via LLM, {total - llm_count} fallback)."
            )
    except Exception as exc:  # noqa: BLE001
        log.exception("self_ops_failed")
        result.errors.append(f"{type(exc).__name__}: {str(exc)[:200]}")

    return result
