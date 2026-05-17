"""Adapter over evidence completeness.

There is no live evidence-ledger read wired into the Assurance System
yet, so completeness is UNKNOWN unless the caller supplies a measured
percentage. This is deliberate — the doctrine forbids a fabricated
"evidence is complete" signal.
"""
from __future__ import annotations

from auto_client_acquisition.assurance_os.adapters.base import BaseAdapter
from auto_client_acquisition.assurance_os.models import AdapterResult, AssuranceInputs


class EvidenceAdapter(BaseAdapter):
    source = "auto_client_acquisition.evidence_control_plane_os"

    def completeness_pct(self, inputs: AssuranceInputs) -> AdapterResult:
        if inputs.evidence_completeness_pct is None:
            return self.unknown("evidence ledger not wired; no measured % supplied")
        return self.ok(
            float(inputs.evidence_completeness_pct),
            "caller-supplied evidence_completeness_pct",
        )
