"""GTM agent mesh — six governed agents (draft-only, no external sends)."""

from __future__ import annotations

from typing import Any

import yaml

from auto_client_acquisition.proof_ledger.pack_assembly import assemble_proof_pack
from auto_client_acquisition.sales_os.qualification import qualify
from dealix.commercial_ops.gtm_stack import score_abm_wave1_row
from dealix.commercial_ops.outreach_drafts import attach_outreach_drafts, build_outreach_draft_ar
from dealix.commercial_ops.paths import ICP_AGENCY_YAML
from dealix.commercial_ops.targeting_csv import build_war_room_today, load_targets


def _agent_envelope(
    *,
    agent: str,
    autonomy_level: str,
    draft_only: bool,
    payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "agent": agent,
        "autonomy_level": autonomy_level,
        "draft_only": draft_only,
        "external_send": False,
        **payload,
    }


def _load_icp() -> dict[str, Any]:
    if not ICP_AGENCY_YAML.is_file():
        return {}
    data = yaml.safe_load(ICP_AGENCY_YAML.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


class TargetingAgent:
    """Rank warm ABM targets from CSV seed (no scraping)."""

    @staticmethod
    def run(context: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = context or {}
        top_n = int(ctx.get("top_n") or 5)
        rows = load_targets()
        war_room = build_war_room_today(rows, top_n=top_n)
        scored = []
        for row in war_room.get("items") or []:
            if isinstance(row, dict):
                scored.append({**row, "abm_score": score_abm_wave1_row(row)})
        return _agent_envelope(
            agent="targeting",
            autonomy_level="suggest",
            draft_only=True,
            payload={
                "targets": scored,
                "count": len(scored),
                "policy_ar": "استهداف warm فقط — لا cold WhatsApp/LinkedIn آلي.",
            },
        )


class EnrichmentAgent:
    """Light enrichment from row fields + source passport hints (no external fetch)."""

    @staticmethod
    def run(context: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = context or {}
        row = dict(ctx.get("target") or {})
        company = (row.get("company") or "").strip()
        enriched = {
            **row,
            "enriched_fields": {
                "company": company,
                "segment": (row.get("segment") or "").strip(),
                "pain_hypothesis": (row.get("pain_hypothesis") or "").strip(),
                "channel": (row.get("channel") or "linkedin_manual").strip(),
            },
            "source_passport_hint": {
                "source_type": "founder_csv_seed",
                "contains_pii": bool(row.get("contact")),
                "ai_access_allowed": True,
                "external_use_allowed": False,
            },
        }
        return _agent_envelope(
            agent="enrichment",
            autonomy_level="assist",
            draft_only=True,
            payload={"enriched": enriched},
        )


class OutreachDraftAgent:
    """First-touch Arabic draft — approval required before any send."""

    @staticmethod
    def run(context: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = context or {}
        row = dict(ctx.get("target") or ctx.get("enriched") or {})
        icp = _load_icp()
        payload = attach_outreach_drafts({"targets": {"items": [row]}})
        item = (payload.get("targets") or {}).get("items") or [{}]
        draft = (item[0] if item else {}).get("outreach_draft_ar") or build_outreach_draft_ar(
            row, icp=icp, objection_snippet=""
        )
        return _agent_envelope(
            agent="outreach_draft",
            autonomy_level="draft",
            draft_only=True,
            payload={
                "draft_ar": draft,
                "channel": row.get("channel") or "linkedin_manual",
                "governance": "requires_founder_approval_before_send",
            },
        )


class QualificationAgent:
    """Discovery-call qualification via sales_os (deterministic)."""

    @staticmethod
    def run(context: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = context or {}
        text = str(ctx.get("raw_request_text") or ctx.get("notes") or "")
        result = qualify(
            pain_clear=bool(ctx.get("pain_clear", True)),
            owner_present=bool(ctx.get("owner_present", False)),
            data_available=bool(ctx.get("data_available", True)),
            accepts_governance=bool(ctx.get("accepts_governance", True)),
            has_budget=bool(ctx.get("has_budget", False)),
            wants_safe_methods=bool(ctx.get("wants_safe_methods", True)),
            proof_path_visible=bool(ctx.get("proof_path_visible", True)),
            retainer_path_visible=bool(ctx.get("retainer_path_visible", False)),
            raw_request_text=text,
            sector=str(ctx.get("sector") or ""),
            city=str(ctx.get("city") or ""),
        )
        return _agent_envelope(
            agent="qualification",
            autonomy_level="recommend",
            draft_only=True,
            payload={"qualification": result.to_dict()},
        )


class ProofPackAgent:
    """Assemble internal proof pack skeleton (no publish)."""

    @staticmethod
    def run(context: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = context or {}
        customer = str(ctx.get("customer_handle") or ctx.get("company") or "prospect")
        events = list(ctx.get("proof_events") or [])
        if not events:
            events = [
                {
                    "event_id": "evt_sample",
                    "event_type": "discovery_completed",
                    "summary_ar": "اكتشاف — مسودة",
                    "summary_en": "Discovery — draft",
                    "evidence_level": "internal",
                    "approval_status": "pending",
                    "consent_for_publication": False,
                }
            ]
        pack = assemble_proof_pack(
            customer_handle=customer,
            events=events,
            audience="internal_only",
        )
        return _agent_envelope(
            agent="proof_pack",
            autonomy_level="assemble",
            draft_only=True,
            payload={"proof_pack": pack},
        )


class LearningAgent:
    """Weekly learning template — friction notes only, no outbound."""

    @staticmethod
    def run(context: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = context or {}
        observations = list(ctx.get("observations") or [])
        template = {
            "week_id": ctx.get("week_id"),
            "wins": observations[:3],
            "losses": [],
            "experiments_next": ["refine ICP wedge", "review approval latency"],
            "doctrine_ok": True,
        }
        return _agent_envelope(
            agent="learning",
            autonomy_level="reflect",
            draft_only=True,
            payload={"learning_report": template},
        )


AGENT_MESH: dict[str, type] = {
    "targeting": TargetingAgent,
    "enrichment": EnrichmentAgent,
    "outreach_draft": OutreachDraftAgent,
    "qualification": QualificationAgent,
    "proof_pack": ProofPackAgent,
    "learning": LearningAgent,
}


def run_agent(agent_name: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Dispatch a named mesh agent."""
    cls = AGENT_MESH.get(agent_name)
    if cls is None:
        raise ValueError(f"unknown agent: {agent_name}")
    return cls.run(context)


__all__ = [
    "AGENT_MESH",
    "EnrichmentAgent",
    "LearningAgent",
    "OutreachDraftAgent",
    "ProofPackAgent",
    "QualificationAgent",
    "TargetingAgent",
    "run_agent",
]
