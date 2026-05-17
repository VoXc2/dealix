"""Adapter over the funnel ladder + 22-stage customer journey."""
from __future__ import annotations

from auto_client_acquisition.assurance_os.adapters.base import BaseAdapter
from auto_client_acquisition.assurance_os.config_loader import load_config
from auto_client_acquisition.assurance_os.models import AdapterResult, AssuranceInputs


class PipelineAdapter(BaseAdapter):
    source = "assurance_os.config.stage_transitions"

    def ladder(self) -> AdapterResult:
        """The 10-rung commercial ladder + its journey-stage mapping."""
        cfg = load_config()
        ladder = cfg.stage_transitions.get("ladder") or []
        mapping = cfg.stage_transitions.get("rung_to_journey_stage") or {}
        if not ladder:
            return self.unknown("stage_transitions.yaml not loaded")
        return self.ok(
            {"ladder": ladder, "rung_to_journey_stage": mapping},
            "stage_transitions.ladder",
        )

    def journey_stages(self) -> AdapterResult:
        """The canonical 22-stage journey from business_ops.

        Loaded directly from the module file: the ``business_ops`` package
        ``__init__`` pulls in unrelated submodules, so we bypass it and
        execute the self-contained ``stage_definitions.py`` in isolation.
        """
        try:
            import importlib.util
            from pathlib import Path

            import auto_client_acquisition

            path = (
                Path(auto_client_acquisition.__file__).parent
                / "business_ops" / "stage_definitions.py"
            )
            spec = importlib.util.spec_from_file_location(
                "_assurance_stage_definitions", path
            )
            if spec is None or spec.loader is None:
                return self.error(f"cannot load stage_definitions from {path}")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            stages = [s.stage.value for s in module.STAGES]
        except Exception as exc:  # noqa: BLE001
            return self.error(f"stage_definitions unavailable: {exc}")
        return self.ok(stages, "business_ops.stage_definitions.STAGES")

    def counts(self, inputs: AssuranceInputs) -> AdapterResult:
        """Per-rung counts. UNKNOWN unless the caller supplies them —
        the Assurance System has no live pipeline read yet."""
        if not inputs.funnel_counts:
            return self.unknown("no funnel_counts supplied by caller")
        return self.ok(dict(inputs.funnel_counts), "caller-supplied funnel_counts")
