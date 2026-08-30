#!/usr/bin/env python3
"""Run the read-only Brand & Growth Portfolio V2 compiler.

Input is a bounded snapshot of Market Radar receipts, proof candidates,
allocation candidates and experiment decisions. Output is an internal/draft
snapshot only; this script never sends, publishes, spends, charges, mutates
production or promotes commercial truth.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial.brand_growth_portfolio import (  # noqa: E402
    ZERO_AUTHORITY,
    allocate_portfolio,
    build_content_opportunity,
    evaluate_proof_reuse,
    route_workload,
    validate_experiment,
    validate_source_signal,
)


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _first(values: Any, fallback: str) -> str:
    if isinstance(values, list):
        for value in values:
            if _text(value):
                return _text(value)
    return fallback


def _generated_at(payload: dict[str, Any]) -> str:
    value = _text(payload.get("generated_at"))
    if value:
        return value
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("input must be a JSON object")
    return value


def _content_request(signal: dict[str, Any]) -> dict[str, Any]:
    sector = _text(signal.get("sector_family"))
    archetype = _text(signal.get("business_archetype"))
    audience = " / ".join(part for part in (sector, archetype) if part)
    return {
        "signal_id": _text(signal.get("signal_id")),
        "thesis": _first(
            signal.get("inferences"),
            _first(signal.get("facts"), "Source-bound market observation requires review"),
        ),
        "buyer_question": _first(
            signal.get("unknowns"),
            "What should a buyer verify next before acting?",
        ),
        "audience": audience or "Buyer hypothesis",
        "buying_stage": "PROBLEM_AWARENESS",
        "asset_type": "MASTER_INSIGHT_DRAFT",
        "channels": ["website", "founder_linkedin", "dealix_linkedin_page", "email"],
        "cta": "START_MINI_DIAGNOSTIC_OR_REQUEST_REVIEW",
        "downstream_event": "QUALIFIED_PROBLEM_OR_EXPLICIT_INBOUND",
    }


def compile_portfolio(payload: dict[str, Any]) -> dict[str, Any]:
    generated_at = _generated_at(payload)
    as_of = _text(payload.get("as_of")) or None
    raw_signals = payload.get("signals", [])
    if not isinstance(raw_signals, list):
        raise ValueError("signals must be a list")

    admitted: list[dict[str, Any]] = []
    rejected_signals: list[dict[str, Any]] = []
    for signal in raw_signals:
        if not isinstance(signal, dict):
            rejected_signals.append(
                {"signal_id": "", "status": "BLOCKED", "errors": ["SIGNAL_MUST_BE_OBJECT"]}
            )
            continue
        errors = validate_source_signal(signal, as_of=as_of)
        if errors:
            rejected_signals.append(
                {
                    "signal_id": _text(signal.get("signal_id")),
                    "status": "BLOCKED",
                    "errors": errors,
                }
            )
        else:
            admitted.append(signal)

    by_signal = {_text(signal.get("signal_id")): signal for signal in admitted}
    requests = payload.get("content_requests")
    if requests is None:
        requests = [_content_request(signal) for signal in admitted]
    if not isinstance(requests, list):
        raise ValueError("content_requests must be a list")

    content_opportunities: list[dict[str, Any]] = []
    for request in requests:
        if not isinstance(request, dict):
            content_opportunities.append(
                {
                    "status": "BLOCKED",
                    "errors": ["CONTENT_REQUEST_MUST_BE_OBJECT"],
                    "authority": dict(ZERO_AUTHORITY),
                }
            )
            continue
        signal = by_signal.get(_text(request.get("signal_id")))
        if signal is None:
            content_opportunities.append(
                {
                    "status": "BLOCKED",
                    "errors": ["CONTENT_REQUEST_SIGNAL_NOT_ADMITTED"],
                    "source_signal_id": _text(request.get("signal_id")),
                    "authority": dict(ZERO_AUTHORITY),
                }
            )
            continue
        opportunity = build_content_opportunity(
            signal,
            thesis=_text(request.get("thesis")),
            buyer_question=_text(request.get("buyer_question")),
            audience=_text(request.get("audience")),
            buying_stage=_text(request.get("buying_stage")),
            asset_type=_text(request.get("asset_type")),
            channels=request.get("channels", []),
            cta=_text(request.get("cta")),
            downstream_event=_text(request.get("downstream_event")),
            as_of=as_of,
        )
        content_opportunities.append(opportunity)

    proof_results: list[dict[str, Any]] = []
    raw_proofs = payload.get("proof_candidates", [])
    if not isinstance(raw_proofs, list):
        raise ValueError("proof_candidates must be a list")
    for proof in raw_proofs:
        if not isinstance(proof, dict):
            proof_results.append(
                {
                    "status": "BLOCKED",
                    "errors": ["PROOF_CANDIDATE_MUST_BE_OBJECT"],
                    "authority": dict(ZERO_AUTHORITY),
                }
            )
        else:
            proof_results.append(evaluate_proof_reuse(proof))

    raw_items = payload.get("allocation_items", [])
    if not isinstance(raw_items, list):
        raise ValueError("allocation_items must be a list")
    allocation = allocate_portfolio(
        [item for item in raw_items if isinstance(item, dict)],
        limit=min(int(payload.get("allocation_limit", 5)), 5),
    )

    experiment_results: list[dict[str, Any]] = []
    raw_experiments = payload.get("experiments", [])
    if not isinstance(raw_experiments, list):
        raise ValueError("experiments must be a list")
    for experiment in raw_experiments:
        if not isinstance(experiment, dict):
            experiment_results.append(
                {
                    "status": "BLOCKED",
                    "errors": ["EXPERIMENT_MUST_BE_OBJECT"],
                    "authority": dict(ZERO_AUTHORITY),
                }
            )
            continue
        errors = validate_experiment(experiment)
        experiment_results.append(
            {
                "experiment_id": _text(experiment.get("experiment_id")),
                "decision": _text(experiment.get("decision")).upper(),
                "status": "VALID" if not errors else "BLOCKED",
                "errors": errors,
                "authority": dict(ZERO_AUTHORITY),
            }
        )

    arms = {
        _text(item.get("arm")).upper()
        for item in raw_items
        if isinstance(item, dict) and _text(item.get("arm"))
    }
    if content_opportunities:
        arms.add("SEARCH_SEO_AEO")
    if proof_results:
        arms.add("PROOF_ADVOCACY_REFERRAL")
    workload_routes = [
        route_workload(arm)
        for arm in sorted(arms)
    ]

    has_blocked = bool(
        rejected_signals
        or any(item.get("status") == "BLOCKED" for item in content_opportunities)
        or any(item.get("status") == "BLOCKED" for item in proof_results)
        or allocation["rejected"]
        or any(item.get("status") == "BLOCKED" for item in experiment_results)
    )
    return {
        "schema": "dealix.brand-growth-portfolio-run.v1",
        "generated_at": generated_at,
        "status": "PARTIAL_FAIL_CLOSED" if has_blocked else "PASS",
        "mode": "READ_ONLY_INTERNAL_DRAFT",
        "admitted_signal_count": len(admitted),
        "rejected_signal_count": len(rejected_signals),
        "rejected_signals": rejected_signals,
        "content_opportunities": content_opportunities,
        "proof_reuse": proof_results,
        "allocation": allocation,
        "experiments": experiment_results,
        "workload_routes": workload_routes,
        "summary": {
            "draft_content_opportunities": sum(
                item.get("status") == "DRAFT_REVIEW_ONLY"
                for item in content_opportunities
            ),
            "proof_reuse_ready": sum(
                item.get("status") == "REUSE_READY_PENDING_CHANNEL_APPROVAL"
                for item in proof_results
            ),
            "allocation_items": len(allocation["items"]),
            "valid_experiments": sum(
                item.get("status") == "VALID" for item in experiment_results
            ),
        },
        "truth_firewall": {
            "research_is_relationship": False,
            "attention_is_demand_truth": False,
            "score_is_purchase_probability": False,
            "draft_is_sent_or_published": False,
            "proof_candidate_is_customer_proof": False,
            "proposal_or_invoice_is_payment": False,
            "source_or_tool_may_promote_truth": False,
        },
        "authority": dict(ZERO_AUTHORITY),
        "external_send_or_spend": False,
        "new_scheduler": False,
        "new_permanent_agent": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = compile_portfolio(_load(args.input))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("DEALIX_BRAND_GROWTH_PORTFOLIO_RUN=FAIL")
        print(f"ERROR: {exc}")
        return 2

    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    print(
        "DEALIX_BRAND_GROWTH_PORTFOLIO_RUN="
        + ("PASS" if result["status"] == "PASS" else "PARTIAL_FAIL_CLOSED"),
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
