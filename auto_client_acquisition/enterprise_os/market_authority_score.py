"""Enterprise facade — market authority composite (Command OS)."""

from __future__ import annotations

from auto_client_acquisition.command_os.market_authority_score import (
    MarketAuthorityInputs,
    compute_market_authority_score,
)

__all__ = ["MarketAuthorityInputs", "compute_market_authority_score"]
