#!/usr/bin/env python3
"""
Seed Commercial Demo — populate the new Saudi Revenue OS tables.

Complements the older `seed_demo_data.py` (which seeds Accounts/Contacts).
This script seeds the *commercial* layer added in PR-BE-Attribution +
PR-COMMERCIAL-CLOSE + PR-8 + PR-LAUNCH-FINAL:

  - 1 PartnerRecord    "Riyadh Growth Agency"
  - 3 CustomerRecord   (paying / pilot / churned)
  - 1 SubscriptionRecord + 2 PaymentRecord
  - 3 ServiceSessionRecord across delivery states
  - 30 ProofEventRecord (10 RWU types)
  - 6 FunnelEventRecord (lead → renewed)
  - 4 SupportTicketRecord (P0/P1/P2/P3)
  - 5 UnsafeActionRecord (proves safety gates fire)
  - 1 ObjectionEventRecord + 1 GrowthExperimentRecord

Idempotent (deterministic IDs prefixed `demo_*`).

Usage:
    DATABASE_URL=... APP_SECRET_KEY=... python scripts/seed_commercial_demo.py
"""

from __future__ import annotations

import asyncio
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


def _now() -> datetime:
    return datetime.now(timezone.utc)


PARTNER_ID = "demo_partner_riyadh"
CUSTOMERS = [
    {"id": "demo_cust_training_co",  "stage": "paying",  "company": "أكاديمية التدريب التنفيذي"},
    {"id": "demo_cust_logistics",    "stage": "pilot",   "company": "شركة لوجستيات الخليج"},
    {"id": "demo_cust_real_estate",  "stage": "churned", "company": "العقار المتميز"},
]


async def seed() -> dict[str, int]:
    # Force test env defaults so settings load cleanly
    os.environ.setdefault("APP_ENV", "test")
    os.environ.setdefault("ANTHROPIC_API_KEY", "x")
    os.environ.setdefault("DEEPSEEK_API_KEY", "x")
    os.environ.setdefault("GROQ_API_KEY", "x")
    os.environ.setdefault("GLM_API_KEY", "x")
    os.environ.setdefault("GOOGLE_API_KEY", "x")
    os.environ.setdefault("APP_SECRET_KEY", "demo-launch-secret")
    os.environ.setdefault(
        "DATABASE_URL",
        "sqlite+aiosqlite:///file:dealix_demo?mode=memory&cache=shared&uri=true",
    )

    from db.models import (
        CustomerRecord, FunnelEventRecord, GrowthExperimentRecord,
        ObjectionEventRecord, PartnerRecord, PaymentRecord, ProofEventRecord,
        ServiceSessionRecord, SubscriptionRecord, SupportTicketRecord,
        UnsafeActionRecord,
    )
    from db.session import get_session, init_db
    from sqlalchemy import select

    await init_db()
    counts: dict[str, int] = {
        "partners": 0, "customers": 0, "subscriptions": 0, "payments": 0,
        "sessions": 0, "proof_events": 0, "funnel_events": 0, "tickets": 0,
        "unsafe_actions": 0, "objections": 0, "experiments": 0,
    }

    async def _add_if_missing(s, model, pk_col, pk_value, factory):
        ex = (await s.execute(select(model).where(pk_col == pk_value))).scalar_one_or_none()
        if ex is None:
            s.add(factory())
            return 1
        return 0

    async with get_session() as s:
        # Partner
        counts["partners"] += await _add_if_missing(
            s, PartnerRecord, PartnerRecord.id, PARTNER_ID,
            lambda: PartnerRecord(
                id=PARTNER_ID, company_name="Riyadh Growth Agency",
                partner_type="AGENCY", contact_name="Founder",
                contact_email="founder@demo-agency.sa", status="active",
                commission_terms="MRR 15% + Setup 0", setup_fee_sar=0.0,
                mrr_share_pct=15.0, clients_signed=3,
            ),
        )

        # Customers
        for c in CUSTOMERS:
            counts["customers"] += await _add_if_missing(
                s, CustomerRecord, CustomerRecord.id, c["id"],
                lambda c=c: CustomerRecord(
                    id=c["id"], company_id=None, deal_id=None,
                    plan="growth_os" if c["stage"] == "paying" else "pilot",
                    onboarding_status="kickoff_complete" if c["stage"] != "churned" else "churned",
                    churn_risk={"paying": "low", "pilot": "medium", "churned": "high"}[c["stage"]],
                    nps_score=9 if c["stage"] == "paying" else (7 if c["stage"] == "pilot" else None),
                ),
            )

        # Subscription + 2 payments for paying customer
        sub_id = "demo_sub_training"
        counts["subscriptions"] += await _add_if_missing(
            s, SubscriptionRecord, SubscriptionRecord.id, sub_id,
            lambda: SubscriptionRecord(
                id=sub_id, customer_id="demo_cust_training_co", partner_id=PARTNER_ID,
                plan_id="executive_growth_os", status="active",
                started_at=_now() - timedelta(days=45),
                current_period_start=_now() - timedelta(days=15),
                current_period_end=_now() + timedelta(days=15),
                mrr_sar=2999.0, moyasar_subscription_id="demo_moyasar_sub_001",
            ),
        )
        for i, days_ago in enumerate([45, 15]):
            counts["payments"] += await _add_if_missing(
                s, PaymentRecord, PaymentRecord.id, f"demo_pay_training_{i}",
                lambda i=i, days_ago=days_ago: PaymentRecord(
                    id=f"demo_pay_training_{i}", subscription_id=sub_id,
                    customer_id="demo_cust_training_co", partner_id=PARTNER_ID,
                    amount_sar=2999.0, status="paid",
                    moyasar_payment_id=f"demo_moyasar_pay_{i:03d}",
                    moyasar_event_id=f"demo_moyasar_evt_{i:03d}",
                    paid_at=_now() - timedelta(days=days_ago),
                ),
            )

        # ServiceSessions
        sessions_def = [
            ("demo_sess_training_001",   "executive_growth_os", "demo_cust_training_co",   "proof_generated"),
            ("demo_sess_logistics_001",  "growth_starter",      "demo_cust_logistics",     "in_progress"),
            ("demo_sess_realestate_001", "growth_starter",      "demo_cust_real_estate",   "closed"),
        ]
        for sid, svc, cust, status in sessions_def:
            counts["sessions"] += await _add_if_missing(
                s, ServiceSessionRecord, ServiceSessionRecord.id, sid,
                lambda sid=sid, svc=svc, cust=cust, status=status: ServiceSessionRecord(
                    id=sid, service_id=svc, customer_id=cust, partner_id=PARTNER_ID,
                    status=status, owner="founder@dealix.me",
                    started_at=_now() - timedelta(days=10),
                    deadline_at=_now() + timedelta(days=4),
                    sla_target_hours=168,
                    next_step="weekly_proof_pack" if status == "proof_generated" else "draft_messages",
                    inputs_json={"company_name": cust, "sector": "training"},
                    deliverables_json=[
                        {"type": "proof_pack_pdf", "url": "https://demo.dealix.me/proof.pdf"}
                    ] if status in ("proof_generated", "closed") else [],
                ),
            )

        # ProofEvents
        rwu_distribution = [
            ("opportunity_created", 10, 500.0),
            ("draft_created",        8, 100.0),
            ("approval_collected",   6,   0.0),
            ("meeting_drafted",      2, 1000.0),
            ("followup_created",     5,  75.0),
            ("risk_blocked",         3, 300.0),
            ("partner_suggested",    1, 500.0),
            ("proof_generated",      1,   0.0),
            ("target_ranked",        4,  50.0),
            ("payment_link_drafted", 1,   0.0),
        ]
        for unit_type, n, impact in rwu_distribution:
            for j in range(n):
                pid = f"demo_prf_{unit_type}_{j:02d}"
                counts["proof_events"] += await _add_if_missing(
                    s, ProofEventRecord, ProofEventRecord.id, pid,
                    lambda pid=pid, ut=unit_type, im=impact, j=j: ProofEventRecord(
                        id=pid, customer_id="demo_cust_training_co",
                        partner_id=PARTNER_ID, service_id="executive_growth_os",
                        session_id="demo_sess_training_001",
                        unit_type=ut, revenue_impact_sar=im, weight=1.0,
                        actor="customer" if ut == "approval_collected" else "system",
                        approval_required=(ut == "draft_created"),
                        approved=(ut == "approval_collected"),
                        risk_level="high" if ut == "risk_blocked" else "low",
                        occurred_at=_now() - timedelta(days=5, hours=j),
                    ),
                )

        # FunnelEvents
        for i, stage in enumerate(["lead", "mql", "sql", "pilot", "paying", "renewed"]):
            counts["funnel_events"] += await _add_if_missing(
                s, FunnelEventRecord, FunnelEventRecord.id, f"demo_funnel_{stage}_001",
                lambda i=i, stage=stage: FunnelEventRecord(
                    id=f"demo_funnel_{stage}_001",
                    customer_id="demo_cust_training_co", partner_id=PARTNER_ID,
                    stage=stage, reason=f"demo seed: {stage}", actor="system",
                    occurred_at=_now() - timedelta(days=60 - i * 10),
                ),
            )

        # Support tickets
        tickets_def = [
            ("demo_tkt_p0", "P0", "security",    "أمان: استفسار عن الـ encryption", 1),
            ("demo_tkt_p1", "P1", "service_down", "Proof Pack لم يصل",              8),
            ("demo_tkt_p2", "P2", "connector",   "HubSpot connector معطّل",        24),
            ("demo_tkt_p3", "P3", "question",    "سؤال عن خطة الترقية",            48),
        ]
        for tid, prio, cat, subj, sla in tickets_def:
            counts["tickets"] += await _add_if_missing(
                s, SupportTicketRecord, SupportTicketRecord.id, tid,
                lambda tid=tid, prio=prio, cat=cat, subj=subj, sla=sla: SupportTicketRecord(
                    id=tid, subject=subj, message=f"تذكرة تجريبية {prio}",
                    name="عميل تجريبي", email=f"customer{prio.lower()}@demo.sa",
                    priority=prio, category=cat, partner_id=PARTNER_ID,
                    status="open", sla_target_hours=sla,
                    escalated=(prio in ("P0", "P1")),
                ),
            )

        # UnsafeAction blocks (5 — proves safety works)
        unsafe_def = [
            ("demo_uns_001", "cold_whatsapp",     "high",   "no_opt_in_for_target"),
            ("demo_uns_002", "linkedin_auto_dm",  "high",   "ToS_violation_detected"),
            ("demo_uns_003", "scrape_linkedin",   "high",   "scraping_endpoint_blocked"),
            ("demo_uns_004", "mass_send",         "medium", "missing_consent_audit"),
            ("demo_uns_005", "guaranteed_claim",  "high",   "blocked_in_draft_review"),
        ]
        for uid, pat, sev, reason in unsafe_def:
            counts["unsafe_actions"] += await _add_if_missing(
                s, UnsafeActionRecord, UnsafeActionRecord.id, uid,
                lambda uid=uid, pat=pat, sev=sev, reason=reason: UnsafeActionRecord(
                    id=uid, actor="operator", pattern=pat, severity=sev,
                    source_module="api.routers.operator",
                    customer_id="demo_cust_training_co", partner_id=PARTNER_ID,
                    blocked_reason=reason,
                ),
            )

        # Objection + Experiment
        counts["objections"] += await _add_if_missing(
            s, ObjectionEventRecord, ObjectionEventRecord.id, "demo_obj_001",
            lambda: ObjectionEventRecord(
                id="demo_obj_001", customer_id="demo_cust_training_co",
                objection_class="price", raw_text="السعر مرتفع بدون proof",
                response_variant="pilot_499_offer", outcome="won",
            ),
        )
        counts["experiments"] += await _add_if_missing(
            s, GrowthExperimentRecord, GrowthExperimentRecord.id, "demo_exp_001",
            lambda: GrowthExperimentRecord(
                id="demo_exp_001", week_iso="2026-W18",
                hypothesis_ar="LinkedIn manual للوكالات في الرياض > Email B2B services",
                segment="riyadh_b2b_agencies", channel="linkedin_manual",
                status="running", n_targets_planned=30, n_drafts_created=12,
                n_approvals_collected=10, n_replies=4, n_meetings=2,
                n_pilots_offered=1, n_pilots_paid=0,
            ),
        )

    return counts


def main() -> int:
    counts = asyncio.run(seed())
    total = sum(counts.values())
    print("DEALIX_SEED_COMMERCIAL_DEMO v1.0")
    print("=" * 40)
    for k, v in counts.items():
        print(f"  + {k:18s} = {v}")
    print("=" * 40)
    print(f"TOTAL ROWS INSERTED: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
