"""Adapter over the North-Star / KPI definitions.

Note: ``business/launch_metrics.py`` exposes metric *names*, not live
values. So ``north_star`` is OK (the definitions are real) but ``values``
is UNKNOWN unless the caller supplies measured numbers.
"""
from __future__ import annotations

from auto_client_acquisition.assurance_os.adapters.base import BaseAdapter
from auto_client_acquisition.assurance_os.models import AdapterResult, AssuranceInputs


class KpiAdapter(BaseAdapter):
    source = "auto_client_acquisition.business.launch_metrics"

    def north_star(self) -> AdapterResult:
        try:
            from auto_client_acquisition.business.launch_metrics import (
                north_star_metrics,
            )

            metrics = north_star_metrics()
        except Exception as exc:  # noqa: BLE001
            return self.error(f"launch_metrics unavailable: {exc}")
        return self.ok(metrics, "launch_metrics.north_star_metrics")

    def values(self, inputs: AssuranceInputs) -> AdapterResult:
        """Measured KPI values — UNKNOWN unless supplied by the caller."""
        if not inputs.kpi_values:
            return self.unknown("launch_metrics defines names only; no values supplied")
        return self.ok(dict(inputs.kpi_values), "caller-supplied kpi_values")
