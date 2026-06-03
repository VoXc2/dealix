#!/usr/bin/env python3
"""
Dealix Check: Ultimate Scale Readiness Scorecard

Computes the weighted Ultimate Scale score and maps it to a readiness mode.
Also derives the hard scale gates (deliverability, agent permissions, security
red-team, delivery capacity, learning loop) and reports whether Scale Mode is
unlocked. Exits non-zero only on invalid data or a "Not Ready" (<60) score.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import Reporter, load_json, file_exists  # noqa: E402


def band(score: float) -> str:
    if score >= 90:
        return "Scale Ready"
    if score >= 80:
        return "Controlled Growth"
    if score >= 70:
        return "Launch Only"
    if score >= 60:
        return "Dry Run Only"
    return "Not Ready"


def _deliverability_pass() -> bool:
    d = load_json("company_os/deliverability/deliverability_state.json") or {}
    auth = d.get("authentication", {})
    comp = d.get("compliance", {})
    spam = d.get("spam", {})
    return (
        all(auth.get(k) is True for k in ("spf", "dkim", "dmarc"))
        and comp.get("purchased_lists") is False
        and comp.get("unsubscribe_present") is True
        and spam.get("spam_rate_pct", 1) < spam.get("spam_rate_hard_pct", 0.3)
    )


def _agent_permissions_pass() -> bool:
    reg = load_json("company_os/agents/agent_registry.json") or {}
    caps = ("can_send_external", "can_call", "can_change_price",
            "can_contract", "can_start_delivery")
    for a in reg.get("agents", []):
        if any(a.get(c) is True for c in caps):
            return False
    return True


def _security_pass() -> bool:
    s = load_json("company_os/security/prompt_injection_tests.json") or {}
    results = {r.get("string"): r for r in s.get("results", [])}
    for t in s.get("test_strings", []):
        if not (results.get(t) or {}).get("blocked"):
            return False
    return True


def _delivery_utilization() -> float:
    c = load_json("company_os/delivery/capacity.json") or {}
    total = c.get("total_capacity_hours_per_week", 0)
    committed = c.get("committed_hours_per_week", 0)
    return (committed / total * 100) if total else 100.0


def run() -> bool:
    r = Reporter("DEALIX CHECK — ULTIMATE SCALE READINESS")

    sc = load_json("company_os/scale/ultimate_scorecard.json")
    if sc is None:
        r.fail("ultimate_scorecard.json missing or invalid")
        return r.render()

    weights = sc.get("weights", {})
    scores = sc.get("scores", {})

    total_weight = sum(weights.values())
    r.check(total_weight == 100,
            f"scorecard weights sum to {total_weight}",
            f"scorecard weights must sum to 100 (got {total_weight})")

    missing = [k for k in weights if k not in scores]
    r.check(not missing, "every weighted domain has a score",
            f"missing scores for {missing}")

    total = sum(weights[k] * scores.get(k, 0) / 100 for k in weights)
    total = round(total, 1)
    mode = band(total)

    print()
    print("  ULTIMATE SCALE SCORECARD")
    print("  " + "-" * 60)
    print(f"  {'Domain':<24}{'Weight':>8}{'Score':>8}{'Weighted':>10}")
    for k in weights:
        w = weights[k]
        s = scores.get(k, 0)
        print(f"  {k:<24}{w:>8}{s:>8}{round(w * s / 100, 1):>10}")
    print("  " + "-" * 60)
    print(f"  {'TOTAL':<24}{total_weight:>8}{'':>8}{total:>10}")
    print(f"  Readiness mode: {mode}  ({total}/100)")
    print()

    # Hard scale gates (informational — do not enter Scale Mode unless all true).
    gates = {
        "Launch readiness >= 90": scores.get("launch_readiness", 0) >= 90,
        "Ultimate Scale score >= 90": total >= 90,
        "Deliverability checks pass": _deliverability_pass(),
        "Agent permission audit pass": _agent_permissions_pass(),
        "Security red-team pass": _security_pass(),
        "Delivery utilization < 80%": _delivery_utilization() < 80,
        "Weekly learning report exists": file_exists("reports/scale/WEEKLY_SCALE_REVIEW.md"),
    }
    print("  SCALE-MODE GATES")
    print("  " + "-" * 60)
    for label, ok in gates.items():
        print(f"  [{'OK ' if ok else 'NO '}] {label}")
    scale_unlocked = all(gates.values())
    print(f"  Scale Mode unlocked: {'YES' if scale_unlocked else 'NO'}")
    print()

    if scale_unlocked:
        r.ok(f"Scale Mode unlocked at {total}/100 ({mode})")
    else:
        r.warn(f"current mode: {mode} ({total}/100) — Scale Mode not yet unlocked")

    # The check only fails when data is broken or the score is "Not Ready".
    r.check(total >= 60, f"score {total} is at or above Dry-Run floor (60)",
            f"score {total} below floor — Not Ready")

    r.require_files(["reports/scale/ULTIMATE_SCALE_SCORECARD.md",
                     "reports/scale/SCALE_READINESS_SCORECARD.md"],
                    label="scale report")
    return r.render()


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
