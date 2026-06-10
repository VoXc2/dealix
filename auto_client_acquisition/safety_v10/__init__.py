"""Safety v10 — Promptfoo-style red-team eval pack.

Pure native Python (regex + dataclasses + Pydantic). No LLM calls, no
external HTTP, no live action. Mirrors the perimeter rules already
enforced by ``auto_client_acquisition.agent_governance`` and
``auto_client_acquisition.security_privacy``.

Hard guarantees (each enforced by tests):
  - ≥30 EvalCase entries spanning every EvalCategory.
  - ``policy_engine_check`` blocks all canonical forbidden tokens
    (نضمن, guaranteed, blast, scrape, cold whatsapp, linkedin
    automation, send_email_live, charge_payment_live, ignore previous
    safety).
  - ``validate_output`` returns ``safe_to_send=False`` by default.
  - ``run_safety_eval`` returns an all-passed report against the
    bundled ``EVAL_CASES``.
"""
from auto_client_acquisition.safety_v10.eval_cases import EVAL_CASES
from auto_client_acquisition.safety_v10.output_validator import validate_output
from auto_client_acquisition.safety_v10.policies import (
    evaluate_case,
    policy_engine_check,
)
from auto_client_acquisition.safety_v10.report import render_report
from auto_client_acquisition.safety_v10.runner import run_safety_eval
from auto_client_acquisition.safety_v10.schemas import (
    EvalCase,
    EvalCategory,
    EvalReport,
    EvalResult,
)

__all__ = [
    "EVAL_CASES",
    "EvalCase",
    "EvalCategory",
    "EvalReport",
    "EvalResult",
    "evaluate_case",
    "policy_engine_check",
    "render_report",
    "run_safety_eval",
    "validate_output",
]
