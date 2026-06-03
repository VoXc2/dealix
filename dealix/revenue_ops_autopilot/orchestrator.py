"""Lightweight orchestration — deterministic side-effects + approval queue."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from dealix.revenue_ops_autopilot.outreach_templates import build_outreach_draft
from dealix.revenue_ops_autopilot.schemas import EvidenceEvent, FunnelLeadRecord
from dealix.revenue_ops_autopilot.scoring import compute_lead_score, suggested_stage_from_score
from dealix.revenue_ops_autopilot.store import AutopilotJSONStore, get_autopilot_store, uid


class RevenueAutopilotOrchestrator:
    def __init__(self, store: AutopilotJSONStore | None = None) -> None:
        self.store = store or get_autopilot_store()

    def _log(self, *, event_type: str, summary: str, entity_type: str, entity_id: str) -> EvidenceEvent:
        ev = EvidenceEvent(
            id=uid("ev"),
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            source="RevenueAutopilotOrchestrator",
            summary=summary,
        )
        return self.store.append_evidence(ev)

    def capture_lead(self, payload: dict[str, Any]) -> FunnelLeadRecord:
        raw_for_score = dict(payload)
        raw_for_score["role"] = str(payload.get("role") or payload.get("title") or "")

        src_lc = str(payload.get("source") or "").lower()
        partner_hit = any(x in src_lc for x in ("partner", "referral", "consultant")) or str(
            payload.get("stage_hint") or "",
        ).lower() in {"partner", "partner_candidate"}

        score, bd = compute_lead_score(raw_for_score)
        stage = suggested_stage_from_score(score=score, is_partner_candidate=partner_hit)

        hold_stage = bool(payload.get("hold_stage"))
        if hold_stage:
            stage = "new_lead"

        segment = str(payload.get("segment") or payload.get("industry") or "").strip()
        if not segment and any(x in src_lc for x in ("partner", "referral", "agency")):
            segment = "agency_partner"
        outreach = build_outreach_draft(
            company=str(payload.get("company") or ""),
            contact=str(payload.get("name") or payload.get("contact") or ""),
            segment=segment,
            pain=str(payload.get("pain") or payload.get("message") or ""),
        )

        hint_ar = "راجع مركز الموافقات قبل أول رسالة خارجية؛ الإرسال دائماً بعد موافقة يدوية."

        preset_id = str(payload.get("id") or payload.get("external_lead_id") or "").strip()
        if preset_id:
            hit = self.store.get_lead(preset_id)
            if hit:
                return hit
            lead_id = preset_id
        else:
            lead_id = uid("lea")

        lead = FunnelLeadRecord(
            id=lead_id,
            name=str(payload.get("name") or "").strip(),
            email=str(payload.get("email") or "").strip(),
            phone=str(payload.get("phone") or "").strip(),
            company=str(payload.get("company") or "").strip(),
            role=str(payload.get("role") or payload.get("title") or "").strip(),
            industry=str(payload.get("industry") or "").strip(),
            country=str(payload.get("country") or payload.get("region") or "").strip(),
            source=str(payload.get("source") or "dealix_diagnostic").strip(),
            pain=str(payload.get("pain") or payload.get("message") or "").strip(),
            ai_usage=str(payload.get("ai_usage") or "").strip(),
            budget_range=str(payload.get("budget_range") or "").strip(),
            urgency=str(payload.get("urgency") or "").strip(),
            consent_marketing=bool(payload.get("consent_marketing")),
            consent_proof_pack=bool(payload.get("consent_proof_pack")),
            lead_score=score,
            score_breakdown=bd,
            stage=stage,
            war_room_status="not_contacted" if hold_stage else "message_drafted",
            segment=segment,
            pain_hypothesis=str(
                payload.get("pain_hypothesis")
                or payload.get("pain")
                or payload.get("message")
                or "",
            ).strip(),
            offer_id=str(payload.get("offer_id") or "revenue_diagnostic_3500").strip(),
            next_action_hint_ar=hint_ar,
            next_action=hint_ar,
            outreach_draft_snippet_ar=outreach,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        self.store.upsert_lead(lead)
        self._log(
            event_type="lead_captured",
            summary=f"score={score} stage={lead.stage}",
            entity_type="funnel_lead",
            entity_id=lead.id,
        )

        try:
            if score >= 15 and not hold_stage:
                apr = ApprovalRequest(
                    object_type="funnel_lead",
                    object_id=lead.id,
                    action_type="draft_email",
                    action_mode="approval_required",
                    channel="linkedin_or_email_manual",
                    summary_ar="مسودة تواصل شخصي — بحاجة موافقة قبل الإرسال اليدوي.",
                    summary_en="Personal outreach draft; manual send after approval.",
                    risk_level="medium",
                    proof_impact="first_touch_outreach_guarded",
                    lead_id=lead.id,
                )
                get_default_approval_store().create(apr)
        except Exception:
            pass

        try:
            from auto_client_acquisition import lead_inbox as _lb

            _lb.append(
                {
                    "name": lead.name,
                    "company": lead.company or "dealix-diagnostic",
                    "email": lead.email,
                    "phone": lead.phone,
                    "sector": lead.industry,
                    "message": lead.pain,
                    "source": f"funnel::{lead.source}",
                    "lead_score": lead.lead_score,
                    "dealix_lead_id": lead.id,
                },
            )
        except Exception:
            pass

        try:
            from dealix.revenue_ops_autopilot.crm_bridge import sync_lead_to_hubspot

            sync_lead_to_hubspot(lead, store=self.store)
        except Exception:
            pass

        return lead


def get_default_orchestrator(store: AutopilotJSONStore | None = None) -> RevenueAutopilotOrchestrator:
    return RevenueAutopilotOrchestrator(store=store)
