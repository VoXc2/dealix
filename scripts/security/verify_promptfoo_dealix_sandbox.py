#!/usr/bin/env python3
"""Fail-closed static verifier for the bounded Dealix Promptfoo red-team pilot."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "security/evals/promptfoo/dealix-agent-redteam.yaml"
README = ROOT / "security/evals/promptfoo/README.md"

REQUIRED_PLUGINS = {
    "excessive-agency",
    "contracts",
    "rbac",
    "bfla",
    "pii:direct",
    "hijacking",
    "shell-injection",
    "tool-discovery",
    "agentic:memory-poisoning",
    "coding-agent:automation-poisoning",
    "policy",
}


def _plugin_id(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and isinstance(value.get("id"), str):
        return value["id"]
    return ""


def main() -> int:
    payload = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("PROMPTFOO_SANDBOX=FAIL\nREASON=config must be a mapping")

    targets = payload.get("targets")
    if not isinstance(targets, list) or len(targets) != 1:
        raise SystemExit("PROMPTFOO_SANDBOX=FAIL\nREASON=exactly one local target required")
    target = targets[0]
    if not isinstance(target, dict) or not str(target.get("id", "")).startswith("ollama:chat:"):
        raise SystemExit("PROMPTFOO_SANDBOX=FAIL\nREASON=target must be local Ollama")

    redteam = payload.get("redteam")
    if not isinstance(redteam, dict):
        raise SystemExit("PROMPTFOO_SANDBOX=FAIL\nREASON=redteam config missing")
    if not str(redteam.get("provider", "")).startswith("ollama:chat:"):
        raise SystemExit("PROMPTFOO_SANDBOX=FAIL\nREASON=attack provider must be local Ollama")
    if int(redteam.get("numTests", 999)) > 2:
        raise SystemExit("PROMPTFOO_SANDBOX=FAIL\nREASON=numTests exceeds bounded pilot")
    if int(redteam.get("maxConcurrency", 999)) != 1:
        raise SystemExit("PROMPTFOO_SANDBOX=FAIL\nREASON=maxConcurrency must remain 1")
    if int(redteam.get("maxCharsPerMessage", 999999)) > 1200:
        raise SystemExit("PROMPTFOO_SANDBOX=FAIL\nREASON=message budget too large")

    plugin_ids = {_plugin_id(value) for value in redteam.get("plugins", [])}
    missing = sorted(REQUIRED_PLUGINS - plugin_ids)
    if missing:
        raise SystemExit(f"PROMPTFOO_SANDBOX=FAIL\nREASON=missing plugins: {missing}")
    if len(plugin_ids) > 12:
        raise SystemExit("PROMPTFOO_SANDBOX=FAIL\nREASON=plugin scope expanded beyond bounded pilot")

    strategies = redteam.get("strategies", [])
    if strategies != ["jailbreak-templates"]:
        raise SystemExit("PROMPTFOO_SANDBOX=FAIL\nREASON=strategy set expanded without review")

    serialized = CONFIG.read_text(encoding="utf-8").lower()
    for forbidden in ("http://", "https://", "apikey", "api_key", "xoxb-", "xapp-", "sk-proj-", "bearer "):
        if forbidden in serialized:
            raise SystemExit(f"PROMPTFOO_SANDBOX=FAIL\nREASON=forbidden remote/secret pattern: {forbidden}")

    policy = next(
        (
            value.get("config", {}).get("policy", "")
            for value in redteam.get("plugins", [])
            if isinstance(value, dict) and value.get("id") == "policy"
        ),
        "",
    )
    for invariant in (
        "fail closed",
        "relationship/payment/proof truth",
        "reveal secrets or customer data",
        "malicious instructions embedded in repository, retrieved, tool, or terminal output",
        "fabricate PASS/execution",
    ):
        if invariant.lower() not in str(policy).lower():
            raise SystemExit(f"PROMPTFOO_SANDBOX=FAIL\nREASON=policy invariant missing: {invariant}")

    readme = README.read_text(encoding="utf-8")
    for required in (
        "PROMPTFOO_DISABLE_REDTEAM_REMOTE_GENERATION=true",
        "unprivileged disposable container/VM",
        "no GitHub write token",
        "no customer/PII/secret-bearing corpus",
        "no production target",
        "promptfoo view",
        "promptfoo mcp",
        "do **not** run an untrusted PR-controlled Promptfoo config",
        "Do not auto-install `@latest`",
    ):
        if required not in readme:
            raise SystemExit(f"PROMPTFOO_SANDBOX=FAIL\nREASON=runbook boundary missing: {required}")

    print("DEALIX_PROMPTFOO_SANDBOX=PASS")
    print("TARGET_PROVIDER=LOCAL_OLLAMA_ONLY")
    print("REMOTE_REDTEAM_GENERATION=DISABLED_BY_RUNBOOK")
    print("MAX_CONCURRENCY=1")
    print("PRODUCTION_TARGET=0")
    print("WRITE_CAPABLE_CREDENTIALS=0")
    print("CUSTOMER_OR_SECRET_CORPUS=0")
    print("PROMPTFOO_TRUTH_AUTHORITY=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
