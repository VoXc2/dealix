"""
Revenue Work Units (RWUs) — the atomic unit of value Dealix produces.

Each unit is a small, verifiable thing Dealix did on behalf of a customer:
  - opportunity_created      — one new qualified prospect
  - target_ranked            — one prospect scored + prioritized
  - draft_created            — one Arabic outbound draft prepared
  - approval_collected       — one human approval recorded
  - meeting_drafted          — one meeting brief / scheduling draft
  - meeting_held             — one customer meeting held (logged outcome)
  - meeting_closed           — one meeting that closed a deal
  - followup_created         — one follow-up scheduled
  - risk_blocked             — one unsafe outbound blocked / channel protected
  - partner_suggested        — one partner shortlist entry
  - proof_generated          — one Proof Pack assembled (deliverable)
  - payment_link_drafted     — one Moyasar invoice draft prepared (no live charge)

Each RWU has:
  - a deterministic weight (used by Excellence Score)
  - an Arabic label
  - an estimated revenue impact (SAR) used in Proof Pack totals
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RWUDef:
    unit_type: str
    label_ar: str
    weight: float
    base_revenue_impact_sar: float


RWU_CATALOG: tuple[RWUDef, ...] = (
    RWUDef("opportunity_created",   "فرصة جديدة",                 1.0,  500.0),
    RWUDef("target_ranked",         "هدف مُرتَّب بحسب الأولوية",  0.5,   50.0),
    RWUDef("draft_created",         "مسودة رسالة جاهزة",          0.7,  100.0),
    RWUDef("approval_collected",    "موافقة بشرية مُسجَّلة",       0.6,    0.0),
    RWUDef("meeting_drafted",       "اجتماع مُجهَّز",              1.2, 1000.0),
    RWUDef("meeting_held",          "اجتماع تم عقده",             1.5,  800.0),
    RWUDef("meeting_closed",        "اجتماع أغلق صفقة",           3.0, 5000.0),
    RWUDef("followup_created",      "متابعة مُجدوَلَة",            0.4,   75.0),
    RWUDef("risk_blocked",          "مخاطرة تم منعها",            1.0,  300.0),  # protecting future revenue
    RWUDef("partner_suggested",     "شريك مُقترَح",               0.8,  500.0),
    RWUDef("proof_generated",       "Proof Pack صدر",              2.0,    0.0),
    RWUDef("payment_link_drafted",  "رابط دفع مُجهَّز",            1.5,    0.0),
)


_BY_TYPE: dict[str, RWUDef] = {r.unit_type: r for r in RWU_CATALOG}


def known_unit_types() -> tuple[str, ...]:
    return tuple(_BY_TYPE.keys())


def is_valid_unit(unit_type: str) -> bool:
    return unit_type in _BY_TYPE


def label_for(unit_type: str) -> str:
    rwu = _BY_TYPE.get(unit_type)
    return rwu.label_ar if rwu else unit_type


def weight_for(unit_type: str) -> float:
    rwu = _BY_TYPE.get(unit_type)
    return rwu.weight if rwu else 0.0


def base_revenue_impact(unit_type: str) -> float:
    rwu = _BY_TYPE.get(unit_type)
    return rwu.base_revenue_impact_sar if rwu else 0.0
