from __future__ import annotations

from saudi_ai_provider.pricing import get_service_pricing


def render_price_sheet(service_id: str, segment: str) -> dict[str, float | str]:
    pricing = get_service_pricing(service_id, segment)
    return {
        "service_id": pricing["service_id"],
        "segment": pricing["segment"],
        "setup_fee_sar": pricing["setup_fee_sar"],
        "monthly_retainer_sar": pricing["monthly_retainer_sar"],
        "minimum_contract_months": pricing["minimum_contract_months"],
    }
