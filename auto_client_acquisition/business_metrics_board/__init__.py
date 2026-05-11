"""Business Metrics Board (Wave 13 Phase 11).

Per-customer + portfolio-level metrics composite. Replaces ad-hoc
grep across 5 modules.

Hard rule (Article 8): every numeric field carries `is_estimate=True`.
`confirmed_revenue_sar` reads ONLY from payment_state=payment_confirmed.
"""

from auto_client_acquisition.business_metrics_board.computer import (
    compute_customer_metrics,
)
from auto_client_acquisition.business_metrics_board.portfolio_view import (
    compute_portfolio_metrics,
)
from auto_client_acquisition.business_metrics_board.schemas import (
    CustomerMetrics,
    PortfolioMetrics,
)

__all__ = [
    "CustomerMetrics",
    "PortfolioMetrics",
    "compute_customer_metrics",
    "compute_portfolio_metrics",
]
