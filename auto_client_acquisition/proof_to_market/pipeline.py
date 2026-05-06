"""End-to-end proof → market plan from internal proof events list."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.proof_to_market.approval_gate import gate_for_public_use
from auto_client_acquisition.proof_to_market.case_study_candidate import case_study_candidate
from auto_client_acquisition.proof_to_market.content_snippet import build_snippet_ar
from auto_client_acquisition.proof_to_market.proof_selector import select_proof_themes
from auto_client_acquisition.proof_to_market.sector_learning import sector_learning


def build_proof_to_market_plan(
    proof_events: list[dict[str, Any]],
    *,
    sector: str = "general",
    has_written_approval: bool = False,
) -> dict[str, Any]:
    themes = select_proof_themes(proof_events)
    gate = gate_for_public_use(has_written_approval=has_written_approval)
    snippet = build_snippet_ar(themes[0])
    candidate = case_study_candidate(sector=sector, proof_theme=themes[0])
    learning = sector_learning(themes)

    return {
        "schema_version": 1,
        "themes": themes,
        "approval_gate": gate,
        "content_snippet": snippet,
        "case_study_candidate": candidate,
        "sector_learning": learning,
        "forbidden": [
            "logo_without_consent",
            "testimonial_without_consent",
            "revenue_claim_without_payment_or_commitment_record",
        ],
        "action_mode": "approval_required",
    }
