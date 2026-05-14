"""Canonical Trust OS — composes existing trust evidence into a single
exportable Trust Pack for enterprise procurement.

Pulls from: data_os (Source Passport coverage), governance_os (recent
decisions sample), proof_os (Proof Pack samples), value_os (tier
breakdown), capital_os (asset count), friction_log (resolved-rate),
compliance_os* (PDPL/ZATCA evidence), and the existing docs/security
trilogy.
"""
from auto_client_acquisition.trust_os.trust_pack import (
    TrustPack,
    assemble_trust_pack,
)

__all__ = ["TrustPack", "assemble_trust_pack"]
