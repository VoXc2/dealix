#!/usr/bin/env python3
"""Dealix eval harness — deterministic, offline, CI-gateable.

Proves the parts of "AI quality" that must never regress: governance
discipline (the product moat), value-tier discipline, and Arabic output
safety. Runs the real engines in-process — no LLM keys, no network.

Probe packs live in ``evals/probes/*.jsonl``. Each probe declares a
``kind`` dispatched to a handler below.

Usage:
  python evals/runner.py            # print report, exit non-zero on failure
  python evals/runner.py --json     # machine-readable report
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

_PROBE_DIR = _REPO / "evals" / "probes"

# Governance pass rate below this fails CI; ANY governance violation fails CI.
_MIN_PASS_RATE = 0.90

_CATEGORY_BY_KIND = {
    "governance_qualify": "governance",
    "governance_decide": "governance",
    "value_discipline": "value_discipline",
    "arabic_text": "arabic_quality",
}


@dataclass
class ProbeResult:
    probe_id: str
    kind: str
    category: str
    passed: bool
    reason: str = ""


@dataclass
class EvalReport:
    results: list[ProbeResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed(self) -> int:
        return self.total - self.passed

    @property
    def governance_violations(self) -> int:
        return sum(
            1 for r in self.results if r.category == "governance" and not r.passed
        )

    @property
    def pass_rate(self) -> float:
        return round(self.passed / self.total, 4) if self.total else 0.0

    @property
    def ai_quality_score(self) -> int:
        return round(100 * self.pass_rate)

    def by_category(self) -> dict[str, dict[str, int]]:
        out: dict[str, dict[str, int]] = {}
        for r in self.results:
            bucket = out.setdefault(r.category, {"passed": 0, "total": 0})
            bucket["total"] += 1
            bucket["passed"] += int(r.passed)
        return out

    def ok(self) -> bool:
        return self.governance_violations == 0 and self.pass_rate >= _MIN_PASS_RATE

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "pass_rate": self.pass_rate,
            "ai_quality_score": self.ai_quality_score,
            "governance_violations": self.governance_violations,
            "by_category": self.by_category(),
            "ok": self.ok(),
            "failures": [
                {"id": r.probe_id, "kind": r.kind, "reason": r.reason}
                for r in self.results
                if not r.passed
            ],
        }

    def to_markdown(self) -> str:
        lines = ["# Dealix Eval Report", ""]
        lines.append(f"- **AI quality score:** {self.ai_quality_score}/100")
        lines.append(f"- **Pass rate:** {self.passed}/{self.total} ({self.pass_rate})")
        lines.append(f"- **Governance violations:** {self.governance_violations}")
        lines.append(f"- **Verdict:** {'PASS' if self.ok() else 'FAIL'}")
        lines.append("")
        lines.append("## By category")
        for cat, b in sorted(self.by_category().items()):
            lines.append(f"- {cat}: {b['passed']}/{b['total']}")
        if self.failed:
            lines.append("")
            lines.append("## Failures")
            for r in self.results:
                if not r.passed:
                    lines.append(f"- [{r.category}] {r.probe_id}: {r.reason}")
        return "\n".join(lines)


def _load_probes() -> list[dict[str, Any]]:
    probes: list[dict[str, Any]] = []
    for path in sorted(_PROBE_DIR.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                probes.append(json.loads(line))
    return probes


# ── Probe handlers ───────────────────────────────────────────────────


def _handle_governance_qualify(probe: dict[str, Any]) -> tuple[bool, str]:
    from auto_client_acquisition.sales_os.qualification import qualify

    result = qualify(**probe["input"])
    expect = probe["expect"]
    decision = result.decision.value
    if decision != expect["decision"]:
        return False, f"decision={decision!r} expected {expect['decision']!r}"
    needle = expect.get("violation_contains")
    if needle and not any(needle in v for v in result.doctrine_violations):
        return False, f"no doctrine violation containing {needle!r}"
    return True, ""


def _handle_governance_decide(probe: dict[str, Any]) -> tuple[bool, str]:
    from auto_client_acquisition.governance_os.runtime_decision import decide
    from auto_client_acquisition.sovereignty_os.source_passport_standard import (
        SourcePassport,
    )

    inp = probe["input"]
    raw = inp.get("passport")
    passport = None
    if raw:
        passport = SourcePassport(
            source_id=raw["source_id"],
            source_type=raw["source_type"],
            owner=raw["owner"],
            allowed_use=frozenset(raw["allowed_use"]),
            contains_pii=raw["contains_pii"],
            sensitivity=raw["sensitivity"],
            retention_policy=raw["retention_policy"],
            ai_access_allowed=raw["ai_access_allowed"],
            external_use_allowed=raw["external_use_allowed"],
        )
    result = decide(
        action=inp["action"],
        context={
            "source_passport": passport,
            "contains_pii": inp.get("contains_pii", False),
            "external_use": inp.get("external_use", False),
        },
    )
    expect = probe["expect"]
    decision = result.decision.value
    if "decision" in expect and decision != expect["decision"]:
        return False, f"decision={decision!r} expected {expect['decision']!r}"
    if "decision_not" in expect and decision == expect["decision_not"]:
        return False, f"decision={decision!r} must not equal {expect['decision_not']!r}"
    return True, ""


def _handle_value_discipline(probe: dict[str, Any]) -> tuple[bool, str]:
    from auto_client_acquisition.value_os.value_ledger import (
        ValueDisciplineError,
        add_event,
    )

    expect = probe["expect"]
    try:
        event = add_event(**probe["input"])
    except ValueDisciplineError as exc:
        if expect.get("raises"):
            return True, ""
        return False, f"unexpected ValueDisciplineError: {exc}"
    if expect.get("raises"):
        return False, "expected ValueDisciplineError but event was accepted"
    if "tier" in expect and event.tier != expect["tier"]:
        return False, f"tier={event.tier!r} expected {expect['tier']!r}"
    return True, ""


def _arabic_ratio(text: str) -> float:
    if not text:
        return 0.0
    arabic = sum(1 for ch in text if "؀" <= ch <= "ۿ")
    letters = sum(1 for ch in text if ch.isalpha())
    return arabic / letters if letters else 0.0


def _arabic_source_text(source: str) -> str:
    if source == "value_os_disclaimer":
        from auto_client_acquisition.value_os.monthly_report import BILINGUAL_DISCLAIMER

        return BILINGUAL_DISCLAIMER
    if source == "monthly_report_markdown":
        from auto_client_acquisition.value_os.monthly_report import generate

        return generate(customer_id="eval_tenant").to_markdown()
    if source == "trust_pack_markdown":
        from auto_client_acquisition.trust_os.trust_pack import assemble_trust_pack

        return assemble_trust_pack("eval_tenant").to_markdown()
    raise KeyError(f"unknown arabic source: {source}")


def _handle_arabic_text(probe: dict[str, Any]) -> tuple[bool, str]:
    text = _arabic_source_text(probe["source"])
    expect = probe["expect"]
    if expect.get("no_replacement_char") and "�" in text:
        return False, "contains U+FFFD replacement character (mojibake)"
    ratio = _arabic_ratio(text)
    min_ratio = float(expect.get("min_arabic_ratio", 0.0))
    if ratio < min_ratio:
        return False, f"arabic ratio {ratio:.2f} < min {min_ratio}"
    must = expect.get("must_contain")
    if must and must not in text:
        return False, f"missing required substring {must!r}"
    return True, ""


_HANDLERS = {
    "governance_qualify": _handle_governance_qualify,
    "governance_decide": _handle_governance_decide,
    "value_discipline": _handle_value_discipline,
    "arabic_text": _handle_arabic_text,
}


def run_evals() -> EvalReport:
    """Run every probe pack and return a scored report."""
    report = EvalReport()
    # Isolate the value ledger so probes never touch a real ledger file.
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["DEALIX_VALUE_LEDGER_PATH"] = str(Path(tmp) / "value.jsonl")
        os.environ.setdefault("DEALIX_FRICTION_LOG_PATH", str(Path(tmp) / "fr.jsonl"))
        for probe in _load_probes():
            kind = probe["kind"]
            category = _CATEGORY_BY_KIND.get(kind, "other")
            handler = _HANDLERS.get(kind)
            if handler is None:
                report.results.append(
                    ProbeResult(probe["id"], kind, category, False, "unknown kind")
                )
                continue
            try:
                ok, reason = handler(probe)
            except Exception as exc:  # noqa: BLE001
                ok, reason = False, f"{type(exc).__name__}: {exc}"
            report.results.append(
                ProbeResult(probe["id"], kind, category, ok, reason)
            )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix eval harness")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    report = run_evals()
    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(report.to_markdown())
    return 0 if report.ok() else 1


if __name__ == "__main__":
    raise SystemExit(main())
