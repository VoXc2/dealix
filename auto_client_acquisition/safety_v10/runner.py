"""Runner — execute the EvalCase pack and produce an EvalReport."""
from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from auto_client_acquisition.safety_v10.eval_cases import EVAL_CASES
from auto_client_acquisition.safety_v10.policies import evaluate_case
from auto_client_acquisition.safety_v10.schemas import (
    EvalCase,
    EvalReport,
    EvalResult,
)


def run_safety_eval(cases: Iterable[EvalCase] | None = None) -> EvalReport:
    """Run every case through ``policy_engine_check`` and aggregate results.

    Each EvalCase has both ``input_ar`` and ``input_en``. We treat the
    case as PASSING if either the Arabic OR the English input matches
    the expected action — both should match for a well-formed case, but
    we only require one to flag a forbidden token.
    """
    chosen = list(cases) if cases is not None else list(EVAL_CASES)
    results: list[EvalResult] = []
    by_cat: dict[str, dict[str, int]] = defaultdict(
        lambda: {"total": 0, "passed": 0, "failed": 0}
    )

    for case in chosen:
        ar_result = evaluate_case(case.id, case.input_ar, case.expected_action)
        en_result = evaluate_case(case.id, case.input_en, case.expected_action)
        # A case passes if BOTH bilingual inputs reach the expected action.
        passed = ar_result.passed and en_result.passed
        # Use the most informative reason (the one that mentions the match).
        chosen_result = ar_result if ar_result.passed else en_result
        if not passed:
            # Fall through to whichever side failed for clearer reporting.
            chosen_result = ar_result if not ar_result.passed else en_result
        result = EvalResult(
            case_id=case.id,
            category=case.category,
            actual_action=chosen_result.actual_action,
            passed=passed,
            reason=chosen_result.reason,
        )
        results.append(result)
        cat_key = (
            case.category.value
            if hasattr(case.category, "value")
            else str(case.category)
        )
        by_cat[cat_key]["total"] += 1
        if passed:
            by_cat[cat_key]["passed"] += 1
        else:
            by_cat[cat_key]["failed"] += 1

    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    return EvalReport(
        total=total,
        passed=passed,
        failed=failed,
        by_category=dict(by_cat),
        results=results,
    )
