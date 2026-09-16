#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "commercial" / "commercial_launch_control_manifest.json"
RELEASE_GATE = ROOT / "reports" / "startup_release_gate" / "latest.json"
STARTUP = ROOT / "reports" / "startup_command_center" / "latest.json"
BRIEF = ROOT / "reports" / "founder_daily_brief" / "latest.json"
PROOF = ROOT / "reports" / "startup_proof_pack" / "latest.json"
OUT = ROOT / "reports" / "commercial_launch_control"
WEB = ROOT / "apps" / "web" / "lib" / "commercial-launch-control-snapshot.ts"


def load_json(path: Path, fallback: dict) -> dict:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def markdown(payload: dict) -> str:
    lines = [
        "# Dealix Commercial Launch Control",
        "",
        f"Verdict: `{payload['verdict']}`",
        "",
        "## Launch products",
        "",
    ]
    for product in payload["launch_products"]:
        lines.append(f"- {product}")
    lines += ["", "## Sprint packages", ""]
    for package in payload["commercial_sprint_packages"]:
        lines.append(f"- {package['name']} — {package['commercial_terms']} — {package['goal']}")
    lines += ["", "## Operating reports", ""]
    for report in payload["operating_reports"]:
        lines.append(f"- {report['status']}: `{report['path']}`")
    lines += ["", "## Founder next actions", ""]
    for action in payload["founder_next_actions"]:
        lines.append(f"- {action}")
    lines += ["", "## Merge order", ""]
    for item in payload["merge_order"]:
        lines.append(f"- {item}")
    lines += ["", "## Guardrails", ""]
    for item in payload["launch_guardrails"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def report_status(path: Path) -> dict[str, str]:
    return {"path": str(path.relative_to(ROOT)), "status": "PASS" if path.exists() else "MISSING"}


def governed_public_packages(raw: object) -> list[dict[str, str]]:
    """Fail closed if a launch manifest tries to reintroduce fixed public terms."""
    if not isinstance(raw, list):
        raise ValueError("commercial_sprint_packages must be a list")
    packages: list[dict[str, str]] = []
    forbidden = {"price_range_sar", "price_sar", "duration", "duration_days"}
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("commercial_sprint_packages entries must be objects")
        leaked = forbidden.intersection(item)
        if leaked:
            raise ValueError(f"fixed public commercial authority is forbidden: {sorted(leaked)}")
        name = str(item.get("name") or "").strip()
        terms = str(item.get("commercial_terms") or "").strip()
        goal = str(item.get("goal") or "").strip()
        if not name or not terms or not goal:
            raise ValueError("commercial package requires name, commercial_terms and goal")
        packages.append({"name": name, "commercial_terms": terms, "goal": goal})
    return packages


def main() -> int:
    manifest = load_json(MANIFEST, {})
    release_gate = load_json(RELEASE_GATE, {})
    startup = load_json(STARTUP, {})
    brief = load_json(BRIEF, {})
    proof = load_json(PROOF, {})

    reports = [
        report_status(RELEASE_GATE),
        report_status(STARTUP),
        report_status(BRIEF),
        report_status(PROOF),
    ]
    missing = [item for item in reports if item["status"] != "PASS"]
    gate_pass = release_gate.get("verdict") == "PASS"
    has_products = bool(startup.get("products"))
    verdict = manifest.get("launch_verdict_target", "READY_FOR_FOUNDER_LED_COMMERCIAL_SPRINT")
    if missing or not gate_pass or not has_products:
        verdict = "NEEDS_LOCAL_RELEASE_GATE_REVIEW"

    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "company": manifest.get("company", "Dealix"),
        "release_name": manifest.get("release_name", "Commercial Launch Control"),
        "release_mode": manifest.get("release_mode", "founder_led_commercial_launch"),
        "verdict": verdict,
        "launch_products": manifest.get("launch_products", []),
        "commercial_sprint_packages": governed_public_packages(manifest.get("commercial_sprint_packages", [])),
        "public_commercial_authority": manifest.get("public_commercial_authority", {}),
        "operating_reports": reports,
        "targets_loaded": startup.get("targets_loaded", 0),
        "packs_generated": startup.get("packs_generated", 0),
        "founder_actions": brief.get("founder_actions", []),
        "proof_metrics": proof.get("proof_metrics", {}),
        "founder_next_actions": [
            "Finish or merge the database foundation before merging the commercial launch pack.",
            "Run Startup OS Release Gate locally.",
            "Run apps/web verification locally.",
            "Review top P1 accounts and prepare three discovery notes.",
            "Create one scoped diagnostic proposal only after qualification.",
            "Keep every sensitive external action owner-reviewed."
        ],
        "merge_order": manifest.get("merge_order", []),
        "launch_guardrails": manifest.get("launch_guardrails", []),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "latest.md").write_text(markdown(payload), encoding="utf-8")
    WEB.parent.mkdir(parents=True, exist_ok=True)
    web_payload = {
        key: payload[key]
        for key in (
            "generated_at", "company", "release_name", "release_mode", "verdict",
            "launch_products", "commercial_sprint_packages", "public_commercial_authority",
            "targets_loaded", "packs_generated",
        )
    }
    WEB.write_text(
        "export const commercialLaunchControlSnapshot = " + json.dumps(web_payload, ensure_ascii=False, indent=2) + " as const;\n",
        encoding="utf-8",
    )
    print(f"COMMERCIAL_LAUNCH_CONTROL={payload['verdict']}")
    print("COMMERCIAL_LAUNCH_CONTROL_REPORT=reports/commercial_launch_control/latest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
