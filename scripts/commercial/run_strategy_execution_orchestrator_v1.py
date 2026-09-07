#!/usr/bin/env python3
"""Dealix Strategy Execution Orchestrator V1.

Internal planning/orchestration only. It ranks the canonical TRUST / MONEY_NOW /
COMPOUNDING strategies, selects at most three actions, selects at most two
venture-validation experiments, and admits at most one OSS benchmark candidate.
It does not send, publish, merge, deploy, mutate production, charge, sign, or bid.
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "company" / "strategy_execution_orchestrator_v1.json"
OUT_ROOT = ROOT / "reports" / "strategy_execution_orchestrator"

FORBIDDEN_TRUE = {
    "DEALIX_EXTERNAL_SEND",
    "DEALIX_EMAIL_LIVE_SEND",
    "DEALIX_WHATSAPP_OUTBOUND",
    "DEALIX_PUBLIC_PUBLISH",
    "DEALIX_PAID_SPEND",
    "DEALIX_PAYMENT_EXECUTION",
    "DEALIX_PRODUCTION_MUTATION",
    "DEALIX_DNS_MUTATION",
    "DEALIX_DB_MUTATION",
    "DEALIX_SECRET_MUTATION",
    "DEALIX_IDENTITY_MUTATION",
    "DEALIX_AGENT_SELF_AUTHORITY",
}


def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def date_stamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_state(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    if not path.is_file():
        raise SystemExit(f"STRATEGY_ORCHESTRATOR=BLOCKED_STATE_FILE_MISSING:{path}")
    data = load_json(path)
    if not isinstance(data, dict):
        raise SystemExit("STRATEGY_ORCHESTRATOR=BLOCKED_STATE_NOT_OBJECT")
    return data


def env_tripwire() -> list[str]:
    return sorted(key for key in FORBIDDEN_TRUE if truthy(os.getenv(key)))


def trust_green(state: dict[str, Any]) -> bool:
    value = str(state.get("production_trust", "UNKNOWN_NOT_EVIDENCE_BACKED")).upper()
    return value in {"PASS", "GREEN", "VERIFIED_GREEN"}


def portfolio_multiplier(portfolio: str, state: dict[str, Any]) -> float:
    if trust_green(state):
        return {"TRUST": 0.80, "MONEY_NOW": 1.35, "COMPOUNDING": 1.00}[portfolio]
    return {"TRUST": 1.10, "MONEY_NOW": 1.20, "COMPOUNDING": 0.90}[portfolio]


def evidence_available(requirement: str, state: dict[str, Any]) -> bool:
    evidence = state.get("evidence") or {}
    if isinstance(evidence, dict):
        return bool(evidence.get(requirement))
    return False


def score_strategy(item: dict[str, Any], state: dict[str, Any]) -> tuple[int, list[str]]:
    base = int(item.get("priority", 0))
    portfolio = str(item.get("portfolio"))
    score = round(base * portfolio_multiplier(portfolio, state))
    missing = [
        req for req in item.get("requires", [])
        if not evidence_available(str(req), state)
    ]
    if missing:
        score -= min(25, 5 * len(missing))
    if item.get("id") == "daily_market_advantage_top3" and int(state.get("verified_cash_sar", 0) or 0) <= 0:
        score += 8
    if item.get("id") == "market_to_delivery_diagnostic" and int(state.get("qualified_problem_count", 0) or 0) > 0:
        score += 15
    if item.get("id") == "d4_procurement_bid_no_bid" and bool(state.get("active_d4_procurement")):
        score += 18
    return max(0, score), missing


def false_authority() -> dict[str, bool]:
    return {
        "send": False,
        "publish": False,
        "bid": False,
        "contract": False,
        "payment": False,
        "merge": False,
        "deploy": False,
        "dns": False,
        "db": False,
        "secret": False,
    }


def choose_actions(config: dict[str, Any], state: dict[str, Any]) -> list[dict[str, Any]]:
    limit = int((config.get("wip_limits") or {}).get("top_actions_per_cycle", 3))
    ranked: list[dict[str, Any]] = []
    for item in config.get("strategies", []):
        score, missing = score_strategy(item, state)
        ranked.append({
            "id": item["id"],
            "portfolio": item["portfolio"],
            "owner": item["owner"],
            "score": score,
            "action": item["action"],
            "missing_evidence": missing,
            "status": "READY_INTERNAL" if not missing else "EVIDENCE_GAP",
            "material_authority": false_authority(),
        })
    ranked.sort(key=lambda x: (-x["score"], x["id"]))
    return ranked[:limit]


def choose_ventures(config: dict[str, Any], state: dict[str, Any]) -> list[dict[str, Any]]:
    limit = int((config.get("wip_limits") or {}).get("active_venture_experiments", 2))
    already = set(str(x) for x in state.get("active_venture_experiments", []) if x)
    candidates = []
    for item in config.get("venture_candidates", []):
        score = int(item.get("priority", 0))
        if item["id"] in already:
            score += 10
        candidates.append({
            "id": item["id"],
            "score": score,
            "stage": item["stage"],
            "next_validation": item["next_validation"],
            "build_allowed": False,
            "evidence": item.get("evidence", []),
        })
    candidates.sort(key=lambda x: (-x["score"], x["id"]))
    return candidates[:limit]


def choose_oss(config: dict[str, Any], state: dict[str, Any]) -> list[dict[str, Any]]:
    limit = int((config.get("wip_limits") or {}).get("capability_benchmarks", 1))
    gap = str(state.get("named_capability_gap", "")).strip()
    if not gap:
        return []
    allowed = []
    for item in config.get("oss_admission", []):
        decision = str(item.get("decision", ""))
        if decision.startswith("KEEP_EXISTING") or decision == "ADOPT_SPEC_NOW":
            continue
        allowed.append({
            "id": item["id"],
            "decision": decision,
            "purpose": item["purpose"],
            "source": item["source"],
            "named_gap": gap,
            "automatic_install": False,
            "status": "BENCHMARK_CANDIDATE_ONLY",
        })
    return allowed[:limit]


def write_outputs(config: dict[str, Any], state: dict[str, Any], actions: list[dict[str, Any]], ventures: list[dict[str, Any]], oss: list[dict[str, Any]], tripwire: list[str]) -> Path:
    out = OUT_ROOT / date_stamp()
    out.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "dealix.strategy-execution-orchestrator.v1",
        "generated_at": utc_stamp(),
        "mode": "draft-only",
        "north_star": config["north_star"],
        "source_sha": os.getenv("DEALIX_SOURCE_SHA", "UNKNOWN_NOT_EVIDENCE_BACKED"),
        "tripwire_violations": tripwire,
        "state": state,
        "top_actions": actions,
        "venture_experiments": ventures,
        "oss_benchmark_candidates": oss,
        "material_authority": config["material_authority"],
        "truth_firewall": config["truth_firewall"],
    }
    (out / "strategy_execution_plan.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out / "venture_experiments.json").write_text(
        json.dumps(ventures, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out / "oss_admission.json").write_text(
        json.dumps(oss, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        f"# Dealix Strategy Execution Orchestrator — {date_stamp()}",
        "",
        f"Verdict: {'HALTED_BY_ENV_TRIPWIRE' if tripwire else 'SAFE_INTERNAL_EXECUTION'}",
        "",
        "## MONEY / TRUST / COMPOUNDING — Top 3",
    ]
    for item in actions:
        lines.append(f"- **{item['portfolio']} / {item['id']}** score={item['score']} — {item['action']} [{item['status']}]")
    lines.extend(["", "## Venture validation WIP"])
    for item in ventures:
        lines.append(f"- **{item['id']}** — {item['next_validation']} (build_allowed=false)")
    if not ventures:
        lines.append("- none")
    lines.extend(["", "## OSS benchmark WIP"])
    if oss:
        for item in oss:
            lines.append(f"- **{item['id']}** — {item['status']} for gap: {item['named_gap']}")
    else:
        lines.append("- none; no named capability gap, so no new OSS benchmark is admitted")
    lines.extend([
        "",
        "## Authority",
        "- external send/public publish/payment/contract/tender/merge/deploy/DNS/DB/secret authority: FALSE",
        "- one material approval packet maximum; this runner creates no executable L5 action",
        "",
        "## Truth firewall",
        "- Research != Relationship; Signal != Opportunity; Draft != Sent; Quote != Payment; Synthetic != Customer Proof.",
    ])
    if tripwire:
        lines.extend(["", "## Tripwire violations", *[f"- {x}" for x in tripwire]])
    (out / "president_brief.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    parser.add_argument("--state-file", type=Path)
    args = parser.parse_args()

    config = load_json(CONFIG)
    state = load_state(args.state_file)
    tripwire = env_tripwire()
    actions = choose_actions(config, state)
    ventures = choose_ventures(config, state)
    oss = choose_oss(config, state)
    out = write_outputs(config, state, actions, ventures, oss, tripwire)
    summary = {
        "ok": not tripwire,
        "output": str(out.relative_to(ROOT)),
        "top_actions": len(actions),
        "venture_experiments": len(ventures),
        "oss_benchmarks": len(oss),
        "tripwire_violations": tripwire,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not tripwire else 2


if __name__ == "__main__":
    raise SystemExit(main())
