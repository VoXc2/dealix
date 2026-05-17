"""Layer 5 — KPI / Funnel.

Builds the 10-rung commercial funnel (Attention -> Referral) with per-rung
counts and rung-to-rung conversion. Conversion between two rungs is
computed only when both counts are known; otherwise it is ``None``.
"""
from __future__ import annotations

from auto_client_acquisition.assurance_os.adapters import KpiAdapter, PipelineAdapter
from auto_client_acquisition.assurance_os.models import (
    AssuranceInputs,
    FunnelRung,
    FunnelSnapshot,
)


def build_funnel(inputs: AssuranceInputs) -> FunnelSnapshot:
    """Assemble the funnel snapshot from the ladder config + supplied counts."""
    ladder_res = PipelineAdapter().ladder()
    counts_res = PipelineAdapter().counts(inputs)
    counts: dict[str, int] = counts_res.value if counts_res.is_known else {}

    rungs: list[FunnelRung] = []
    if ladder_res.is_known:
        ladder = ladder_res.value["ladder"]
        mapping = ladder_res.value["rung_to_journey_stage"]
        for rung in ladder:
            key = rung["key"]
            rungs.append(FunnelRung(
                key=key,
                label_en=rung["label_en"],
                label_ar=rung["label_ar"],
                journey_stages=list(mapping.get(key, [])),
                count=counts.get(key),
            ))

    conversion: dict[str, float | None] = {}
    for i in range(len(rungs) - 1):
        a, b = rungs[i], rungs[i + 1]
        if a.count is not None and b.count is not None and a.count > 0:
            conversion[f"{a.key}->{b.key}"] = round(b.count / a.count, 4)
        else:
            conversion[f"{a.key}->{b.key}"] = None

    ns_res = KpiAdapter().north_star()
    north_star = ns_res.value if ns_res.is_known else {}

    return FunnelSnapshot(rungs=rungs, conversion=conversion, north_star=north_star)


def detect_bottleneck(funnel: FunnelSnapshot) -> str:
    """Return the rung transition with the lowest KNOWN conversion."""
    known = {k: v for k, v in funnel.conversion.items() if v is not None}
    if not known:
        return "unknown"
    return min(known, key=lambda k: known[k])
