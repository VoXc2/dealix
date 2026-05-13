"""Expansion Revenue Map — next step from each offer."""

from __future__ import annotations


EXPANSION_MAP: dict[str, tuple[str, ...]] = {
    "Capability Diagnostic": ("Revenue Intelligence Sprint", "AI Governance Review", "Company Brain Sprint"),
    "Revenue Intelligence Sprint": ("Monthly RevOps OS", "Executive Reporting", "Sales Company Brain"),
    "Company Brain Sprint": ("Monthly Company Brain", "Support Assistant", "Governance Review"),
    "AI Governance Review": ("Monthly Governance", "Governance Runtime", "AI Control Plane"),
    "AI Quick Win Sprint": ("Monthly AI Ops", "Workflow Dashboard", "Reporting Automation"),
    "Monthly RevOps OS": ("Client Workspace", "Dealix Revenue OS"),
    "Monthly Company Brain": ("Enterprise Knowledge OS",),
    "Monthly Governance": ("AI Control Plane", "Enterprise AI OS"),
}


def next_expansion_step(offer: str) -> tuple[str, ...]:
    return EXPANSION_MAP.get(offer, ())
