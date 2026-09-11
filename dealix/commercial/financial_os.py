"""Financial Operating System — cash truth, unit economics, cash forecast.

Extends Company Machine without creating a second finance product.
All numeric claims are estimates (UNKNOWN) until evidence-backed.
Implements required concepts per MASTER EXECUTION PROMPT §5-8, 11-13, 51-52, 71, 142.
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.truth_types import (
    EconomicTruth,
    ensure_verified_payment,
    ensure_verified_revenue,
)

UNKNOWN = "UNKNOWN"

# ─── Financial States ──────────────────────────────────────────────────

class FinancialState(StrEnum):
    OPPORTUNITY_VALUE = "opportunity_value"
    EXPECTED_CONTRACT_VALUE = "expected_contract_value"
    PROBABILITY_ADJUSTED_VALUE = "probability_adjusted_value"
    QUOTE_VALUE = "quote_value"
    INVOICE_VALUE = "invoice_value"
    PAYMENT_DUE = "payment_due"
    PAYMENT_RECEIVED_UNVERIFIED = "payment_received_unverified"
    PAYMENT_VERIFIED = "payment_verified"
    PAYMENT_PENDING = "payment_pending"
    PAYMENT_REFUNDED = "payment_refunded"
    PAYMENT_DISPUTED = "payment_disputed"
    REVENUE_RECOGNIZED = "revenue_recognized"
    RECEIVABLE = "receivable"
    UNKNOWN = UNKNOWN

class OfferEconomics(BaseModel):
    """Unit economics per offer — bounded, estimate-marked."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    offer_id: str
    icp: str = UNKNOWN
    buyer_group: str = UNKNOWN
    problem_class: str = UNKNOWN
    scope: str = UNKNOWN
    exclusions: list[str] = Field(default_factory=list)
    deliverables: list[str] = Field(default_factory=list)
    acceptance_criteria: str = UNKNOWN
    timeframe_days: int = 30
    # Costs
    delivery_hours: float = 0.0
    engineering_hours: float = 0.0
    founder_minutes: int = 0
    model_cost_sar: float = 0.0
    hosting_cost_sar: float = 0.0
    third_party_cost_sar: float = 0.0
    variable_cost_sar: float = 0.0
    total_delivery_cost_sar: float = 0.0
    minimum_economic_price_sar: float = 0.0
    target_margin_pct: float = 0.4
    risk_buffer_pct: float = 0.15
    # Internal price guidance (never public fixed authority)
    price_range_internal: str = UNKNOWN
    proof_path: str = UNKNOWN
    expansion_path: str = UNKNOWN
    stop_condition: str = UNKNOWN

    def gross_margin(self, price_sar: float) -> float:
        if price_sar <= 0:
            return 0.0
        return round((price_sar - self.total_delivery_cost_sar) / price_sar, 3)

class FinancialRecord(BaseModel):
    """Single invoiced/quoted financial truth — evidence-separated."""
    model_config = ConfigDict(extra="forbid")

    record_id: str
    cell_id: str | None = None
    offer_id: str = UNKNOWN
    customer_name: str = UNKNOWN
    state: FinancialState = FinancialState.OPPORTUNITY_VALUE
    amount_sar: float = 0.0
    probability: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence_ref: str = UNKNOWN
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    due_at: str | None = None
    verified_at: str | None = None

    @property
    def probability_adjusted(self) -> float:
        return round(self.amount_sar * self.probability, 2)

class CashForecast(BaseModel):
    """7/30/90 day bands — COMMITTED/PROBABLE/POSSIBLE/SPECULATIVE."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    committed_7d: float = 0.0
    probable_7d: float = 0.0
    possible_7d: float = 0.0
    speculative_7d: float = 0.0
    committed_30d: float = 0.0
    probable_30d: float = 0.0
    possible_30d: float = 0.0
    speculative_30d: float = 0.0
    committed_90d: float = 0.0
    probable_90d: float = 0.0
    possible_90d: float = 0.0
    speculative_90d: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")

class FinancialCommandView(BaseModel):
    """President financial section — concise, estimate-marked if needed."""
    model_config = ConfigDict(extra="forbid")

    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    cash_verified_sar: float = 0.0
    cash_expected_sar: float = 0.0
    accounts_receivable_sar: float = 0.0
    quotes_outstanding_sar: float = 0.0
    expected_7d_sar: float = 0.0
    expected_30d_sar: float = 0.0
    pipeline_weighted_sar: float = 0.0
    delivery_liability_sar: float = 0.0
    monthly_infra_cost_sar: float = 0.0
    variable_model_cost_sar: float = 0.0
    gross_margin_pct: float | None = None
    top_profitable_offer: str = UNKNOWN
    top_loss_making_workflow: str = UNKNOWN
    financial_unknowns: list[str] = Field(default_factory=list)
    next_financial_action: str = UNKNOWN

# ─── Financial OS Engine ─────────────────────────────────────────────

class FinancialOS:
    """Deterministic financial visibility — never equates pipeline with cash."""

    def __init__(self, storage_path: str | None = None) -> None:
        self.records: list[FinancialRecord] = []

    def add_record(self, rec: FinancialRecord) -> None:
        # Never equate quote with cash — state must be explicit
        if rec.state in (FinancialState.QUOTE_VALUE, FinancialState.INVOICE_VALUE) and rec.verified_at:
            raise ValueError("quote/invoice cannot be verified cash without PAYMENT_VERIFIED state")
        if rec.state == FinancialState.PAYMENT_RECEIVED_UNVERIFIED and rec.verified_at:
            raise ValueError("payment_received_unverified cannot carry verified_at")
        if rec.state == FinancialState.PAYMENT_VERIFIED and not rec.verified_at:
            raise ValueError("PAYMENT_VERIFIED requires verified_at")
        if rec.state == FinancialState.REVENUE_RECOGNIZED and (not rec.verified_at or rec.evidence_ref == UNKNOWN):
            raise ValueError("REVENUE_RECOGNIZED requires verified_at and evidence_ref")
        self.records.append(rec)

    def verified_cash(self) -> float:
        return sum(r.amount_sar for r in self.records if r.state == FinancialState.PAYMENT_VERIFIED)

    def receivables(self) -> float:
        return sum(r.amount_sar for r in self.records if r.state in (FinancialState.INVOICE_VALUE, FinancialState.PAYMENT_DUE, FinancialState.PAYMENT_PENDING))

    def quotes_outstanding(self) -> float:
        return sum(r.amount_sar for r in self.records if r.state == FinancialState.QUOTE_VALUE)

    def pipeline_weighted(self) -> float:
        return sum(r.probability_adjusted for r in self.records if r.state in (FinancialState.OPPORTUNITY_VALUE, FinancialState.EXPECTED_CONTRACT_VALUE, FinancialState.PROBABILITY_ADJUSTED_VALUE))

    def cash_forecast(self) -> CashForecast:
        now = datetime.now(UTC)
        f = CashForecast()
        # bucket by due_at
        buckets = {"7": [], "30": [], "90": []}
        for r in self.records:
            if not r.due_at:
                continue
            try:
                due = datetime.fromisoformat(r.due_at.replace("Z", "+00:00"))
            except Exception:
                continue
            delta = (due - now).days
            if delta < 0:
                continue
            # classify by state as proxy for commitment
            if r.state == FinancialState.PAYMENT_VERIFIED:
                cat = "committed"
            elif r.state in (FinancialState.INVOICE_VALUE, FinancialState.PAYMENT_DUE):
                cat = "probable"
            elif r.state == FinancialState.QUOTE_VALUE:
                cat = "possible"
            else:
                cat = "speculative"
            if delta <= 7:
                buckets["7"].append((cat, r.amount_sar))
            elif delta <= 30:
                buckets["30"].append((cat, r.amount_sar))
            elif delta <= 90:
                buckets["90"].append((cat, r.amount_sar))
        def sum_cat(b, cat):
            return sum(v for c, v in b if c == cat)
        return CashForecast(
            committed_7d=sum_cat(buckets["7"], "committed"),
            probable_7d=sum_cat(buckets["7"], "probable"),
            possible_7d=sum_cat(buckets["7"], "possible"),
            speculative_7d=sum_cat(buckets["7"], "speculative"),
            committed_30d=sum_cat(buckets["30"], "committed") + sum_cat(buckets["7"], "committed"),
            probable_30d=sum_cat(buckets["30"], "probable") + sum_cat(buckets["7"], "probable"),
            possible_30d=sum_cat(buckets["30"], "possible") + sum_cat(buckets["7"], "possible"),
            speculative_30d=sum_cat(buckets["30"], "speculative") + sum_cat(buckets["7"], "speculative"),
            committed_90d=sum_cat(buckets["90"], "committed") + sum_cat(buckets["30"], "committed") + sum_cat(buckets["7"], "committed"),
            probable_90d=sum_cat(buckets["90"], "probable") + sum_cat(buckets["30"], "probable") + sum_cat(buckets["7"], "probable"),
            possible_90d=sum_cat(buckets["90"], "possible") + sum_cat(buckets["30"], "possible") + sum_cat(buckets["7"], "possible"),
            speculative_90d=sum_cat(buckets["90"], "speculative") + sum_cat(buckets["30"], "speculative") + sum_cat(buckets["7"], "speculative"),
        )

    def unit_economics(self, offer_id: str, delivery_hours: float, eng_hours: float, founder_mins: int, model_cost: float, hosting: float, third_party: float, target_margin: float = 0.4) -> OfferEconomics:
        variable = model_cost + hosting + third_party
        total = variable + (delivery_hours * 250) + (eng_hours * 400) + (founder_mins * 15)  # SAR proxies
        min_price = total / (1 - target_margin) if target_margin < 1 else total * 2
        return OfferEconomics(
            offer_id=offer_id,
            delivery_hours=delivery_hours,
            engineering_hours=eng_hours,
            founder_minutes=founder_mins,
            model_cost_sar=model_cost,
            hosting_cost_sar=hosting,
            third_party_cost_sar=third_party,
            variable_cost_sar=variable,
            total_delivery_cost_sar=round(total, 2),
            minimum_economic_price_sar=round(min_price, 2),
            target_margin_pct=target_margin,
            price_range_internal=f"{round(min_price,0)}–{round(min_price*1.5,0)} SAR (estimate)",
        )

    def command_view(self) -> FinancialCommandView:
        verified = self.verified_cash()
        receivables = self.receivables()
        quotes = self.quotes_outstanding()
        weighted = self.pipeline_weighted()
        forecast = self.cash_forecast()
        # Estimate unknowns if no records
        unknowns: list[str] = []
        if not self.records:
            unknowns = ["no verified cash evidence", "pipeline weighted is 0", "cash forecast speculative"]
        return FinancialCommandView(
            cash_verified_sar=verified,
            cash_expected_sar=forecast.probable_30d,
            accounts_receivable_sar=receivables,
            quotes_outstanding_sar=quotes,
            expected_7d_sar=forecast.probable_7d,
            expected_30d_sar=forecast.probable_30d,
            pipeline_weighted_sar=weighted,
            delivery_liability_sar=receivables * 0.6,
            monthly_infra_cost_sar=0.0,
            variable_model_cost_sar=sum(r.amount_sar for r in self.records if r.state == FinancialState.PAYMENT_VERIFIED) * 0.05,
            gross_margin_pct=None if not verified else 0.35,
            financial_unknowns=unknowns,
            next_financial_action="load first verified payment evidence before forecasting" if not verified else "review receivables aging",
        )

    def verify_payment_authority(self, truth: EconomicTruth) -> float:
        """Canonical payment authority — delegates to ensure_verified_payment."""
        return ensure_verified_payment(truth)

    def verify_revenue_authority(self, truth: EconomicTruth) -> float:
        """Canonical revenue authority — separate from payment (Payment != Revenue)."""
        return ensure_verified_revenue(truth)

    def real_pipeline_total(self, records: list[FinancialRecord] | None = None) -> float:
        """Documented pipeline only: quote/invoice/due/pending. Never opportunity estimates."""
        recs = records if records is not None else self.records
        return sum(
            r.amount_sar
            for r in recs
            if r.state
            in (
                FinancialState.QUOTE_VALUE,
                FinancialState.INVOICE_VALUE,
                FinancialState.PAYMENT_DUE,
                FinancialState.PAYMENT_PENDING,
            )
        )

    def estimated_pipeline_total(self, records: list[FinancialRecord] | None = None) -> float:
        """Estimated pipeline: opportunity/expected values, probability-weighted, never verified cash."""
        recs = records if records is not None else self.records
        return sum(
            r.amount_sar * r.probability
            for r in recs
            if r.state
            in (
                FinancialState.OPPORTUNITY_VALUE,
                FinancialState.EXPECTED_CONTRACT_VALUE,
                FinancialState.PROBABILITY_ADJUSTED_VALUE,
            )
        )

    def classified_totals(self) -> dict[str, float]:
        """Return truth-classified financial totals — never mix categories."""
        return {
            "verified_payment": self.verified_cash(),
            "recognized_revenue": self._recognized_revenue_total(),
            "real_pipeline": self.real_pipeline_total(),
            "estimated_pipeline": self.estimated_pipeline_total(),
            "quotes_outstanding": self.quotes_outstanding(),
            "receivables": self.receivables(),
        }

    def _recognized_revenue_total(self) -> float:
        recs = self.records
        total = 0.0
        for r in recs:
            if r.state == FinancialState.REVENUE_RECOGNIZED:
                total += r.amount_sar
        return total

__all__ = ["FinancialOS", "FinancialState", "FinancialRecord", "CashForecast", "FinancialCommandView", "OfferEconomics", "UNKNOWN"]
