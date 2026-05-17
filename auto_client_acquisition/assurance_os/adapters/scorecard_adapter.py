"""Adapter over per-machine maturity observations.

Machine maturity (0-5) is a founder/operator judgement captured weekly;
it is supplied via ``AssuranceInputs.machine_maturity``. Any machine with
no observation surfaces as UNKNOWN.
"""
from __future__ import annotations

from auto_client_acquisition.assurance_os.adapters.base import BaseAdapter
from auto_client_acquisition.assurance_os.models import AdapterResult, AssuranceInputs


class ScorecardAdapter(BaseAdapter):
    source = "assurance_os (caller-supplied machine_maturity)"

    def maturity(self, machine: str, inputs: AssuranceInputs) -> AdapterResult:
        raw = inputs.machine_maturity.get(machine)
        if raw is None:
            return self.unknown(f"no maturity observation for '{machine}'")
        try:
            level = int(raw)
        except (TypeError, ValueError):
            return self.error(f"non-integer maturity for '{machine}': {raw!r}")
        if not 0 <= level <= 5:
            return self.error(f"maturity for '{machine}' out of range 0-5: {level}")
        return self.ok(level, f"machine_maturity['{machine}']")
