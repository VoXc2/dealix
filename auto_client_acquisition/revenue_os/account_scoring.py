"""Account scoring entrypoint (delegates to deterministic Revenue OS scorer)."""

from __future__ import annotations

from auto_client_acquisition.revenue_os.scoring import score_account_row

__all__ = ["score_account_row"]
