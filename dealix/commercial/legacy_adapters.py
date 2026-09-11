"""Legacy Adapters — reuse auto_client_acquisition logic without duplication, best thought."""

from __future__ import annotations

from typing import Any

try:
    from auto_client_acquisition.proof_ledger import get_default_ledger as _get_legacy_ledger
    LEGACY_PROOF_AVAILABLE = True
except Exception:
    LEGACY_PROOF_AVAILABLE = False
    _get_legacy_ledger = None

def get_proof_ledger():
    """Canonical adapter — prefers dealix/commercial/proof_asset_factory, falls back to legacy if needed."""
    if LEGACY_PROOF_AVAILABLE and _get_legacy_ledger:
        try:
            return _get_legacy_ledger()
        except Exception:
            pass
    # Fallback to new canonical
    from dealix.commercial.proof_asset_factory import ProofAssetFactory
    return ProofAssetFactory()

__all__ = ["get_proof_ledger", "LEGACY_PROOF_AVAILABLE"]
