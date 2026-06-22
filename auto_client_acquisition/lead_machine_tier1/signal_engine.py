from __future__ import annotations

from .schemas import LeadCompany, SignalRecord


SIGNAL_WEIGHTS = {
    "hiring": 10,
    "funding": 15,
    "new_branch": 12,
    "new_website": 8,
    "broken_form": 14,
    "slow_response": 10,
    "whatsapp_button": 6,
    "booking_link": 8,
    "crm_installed": 7,
    "ecommerce_platform": 9,
    "payment_provider": 9,
    "ads_pixel": 6,
    "high_review_volume": 7,
    "bad_review_spike": 13,
    "tender_rfp": 16,
    "expansion": 12,
    "seasonality": 8,
    "ramadan_eid": 11,
}


def detect_signals(lead: LeadCompany) -> list[SignalRecord]:
    metadata = lead.metadata
    signals: list[SignalRecord] = []
    for signal_name, weight in SIGNAL_WEIGHTS.items():
        detected = bool(metadata.get(signal_name))
        signals.append(SignalRecord(signal_name=signal_name, detected=detected, weight=weight if detected else 0, evidence=str(metadata.get(signal_name)) if detected else None))
    return signals