"""Revenue Pipeline — in-memory store + summary."""
from __future__ import annotations

from collections.abc import Iterable
from threading import RLock

from auto_client_acquisition.revenue_pipeline.lead import Lead
from auto_client_acquisition.revenue_pipeline.stage_policy import (
    PipelineStage,
    advance_stage,
    counts_as_commitment,
    counts_as_revenue,
)


class RevenuePipeline:
    """Append-only-by-default lead store with idempotent insert by id."""

    def __init__(self) -> None:
        self._leads: dict[str, Lead] = {}
        self._lock = RLock()

    def add(self, lead: Lead) -> Lead:
        with self._lock:
            self._leads[lead.id] = lead
        return lead

    def add_many(self, leads: Iterable[Lead]) -> int:
        n = 0
        for lead in leads:
            self.add(lead)
            n += 1
        return n

    def get(self, lead_id: str) -> Lead | None:
        return self._leads.get(lead_id)

    def list_all(self) -> list[Lead]:
        with self._lock:
            return list(self._leads.values())

    def list_by_stage(self, stage: PipelineStage) -> list[Lead]:
        return [lead for lead in self.list_all() if lead.stage == stage]

    def advance(
        self,
        lead_id: str,
        target: PipelineStage,
        *,
        commitment_evidence: str = "",
        payment_evidence: str = "",
        actual_amount_sar: int | None = None,
    ) -> Lead:
        """Advance a lead. Enforces evidence requirements for revenue stages.

        - To advance to ``commitment_received``, ``commitment_evidence``
          must be non-empty (e.g. "email_2026-MM-DD_signed_intent.png").
        - To advance to ``payment_received``, ``payment_evidence`` must
          be non-empty AND ``actual_amount_sar`` must be > 0.
        """
        with self._lock:
            lead = self._leads.get(lead_id)
            if lead is None:
                raise KeyError(f"unknown lead: {lead_id}")
            new_stage = advance_stage(current=lead.stage, target=target)
            if new_stage == "commitment_received" and not commitment_evidence:
                raise ValueError(
                    "commitment_evidence is required to advance to "
                    "'commitment_received' (e.g. signed-intent email "
                    "screenshot reference). Verbal yes is NOT enough."
                )
            if new_stage == "payment_received":
                if not payment_evidence:
                    raise ValueError(
                        "payment_evidence is required to advance to "
                        "'payment_received' (e.g. moyasar_dashboard_screenshot "
                        "or bank_statement_reference). A draft invoice is "
                        "NOT payment."
                    )
                if not actual_amount_sar or actual_amount_sar <= 0:
                    raise ValueError(
                        "actual_amount_sar must be > 0 for payment_received."
                    )
            updated = lead.model_copy(update={
                "stage": new_stage,
                "commitment_evidence": commitment_evidence or lead.commitment_evidence,
                "payment_evidence": payment_evidence or lead.payment_evidence,
                "actual_amount_sar": actual_amount_sar or lead.actual_amount_sar,
            })
            self._leads[lead_id] = updated
            return updated

    def summary(self) -> dict[str, int]:
        all_leads = self.list_all()
        commitments = [lead for lead in all_leads if counts_as_commitment(lead.stage)]
        revenue = [lead for lead in all_leads if counts_as_revenue(lead.stage)]
        total_revenue_sar = sum(
            (lead.actual_amount_sar or 0) for lead in revenue
        )
        return {
            "total_leads": len(all_leads),
            "commitments": len(commitments),
            "paid": len(revenue),
            "total_revenue_sar": total_revenue_sar,
        }

    def reset(self) -> None:
        """Test-only — wipe all leads."""
        with self._lock:
            self._leads.clear()


_DEFAULT = RevenuePipeline()


def get_default_pipeline() -> RevenuePipeline:
    return _DEFAULT
