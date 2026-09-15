#!/usr/bin/env python3
"""Prepare/verify an OpenClaw config under Dealix NO_DEEPSEEK authority.

This tool never mutates the live OpenClaw config in place. `prepare` reads an
input JSON and writes a separate candidate file for review/cutover. `verify`
is read-only and emits only model/provider policy facts, never secret values.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

LOCAL_MODEL = "ollama/qwen3:4b-instruct-2507-q4_K_M"
LOCAL_ROUTER_MODEL = "dealix-router/dealix-local"


def is_deepseek(value: Any) -> bool:
    return "deepseek" in str(value or "").lower()


def model_refs(model_cfg: Any) -> list[str]:
    if isinstance(model_cfg, str):
        return [model_cfg]
    if not isinstance(model_cfg, dict):
        return []
    refs: list[str] = []
    primary = model_cfg.get("primary")
    if isinstance(primary, str):
        refs.append(primary)
    fallbacks = model_cfg.get("fallbacks") or []
    if isinstance(fallbacks, list):
        refs.extend(str(item) for item in fallbacks)
    return refs


def audit_config(data: dict[str, Any]) -> dict[str, Any]:
    providers = ((data.get("models") or {}).get("providers") or {})
    plugins = ((data.get("plugins") or {}).get("entries") or {})
    auth = ((data.get("auth") or {}).get("profiles") or {})
    agents = ((data.get("agents") or {}).get("list") or [])
    agent_violations: list[dict[str, Any]] = []
    for agent in agents:
        if not isinstance(agent, dict):
            continue
        refs = model_refs(agent.get("model"))
        bad = [ref for ref in refs if is_deepseek(ref) or ref.endswith("/dealix-flash") or ref.endswith("/dealix-think") or ref.endswith("/dealix-pro")]
        if bad:
            agent_violations.append({"agent_id": agent.get("id"), "forbidden_model_refs": bad})
    deepseek_auth = [
        name
        for name, cfg in auth.items()
        if is_deepseek(name) or (isinstance(cfg, dict) and is_deepseek(cfg.get("provider")))
    ]
    deepseek_providers = [name for name in providers if is_deepseek(name)]
    plugin = plugins.get("deepseek") if isinstance(plugins, dict) else None
    deepseek_plugin_enabled = isinstance(plugin, dict) and plugin.get("enabled") is True
    router_models: list[str] = []
    router_cfg = providers.get("dealix-router") if isinstance(providers, dict) else None
    if isinstance(router_cfg, dict):
        raw = router_cfg.get("models")
        if isinstance(raw, list):
            for item in raw:
                if isinstance(item, dict) and item.get("id"):
                    router_models.append(str(item["id"]))
                elif isinstance(item, str):
                    router_models.append(item)
        elif isinstance(raw, dict):
            router_models.extend(str(key) for key in raw)
    forbidden_router_alias = any(item in {"dealix-flash", "dealix-think", "dealix-pro"} for item in router_models)
    ok = not any((agent_violations, deepseek_auth, deepseek_providers, deepseek_plugin_enabled, forbidden_router_alias))
    return {
        "ok": ok,
        "founder_policy": "NO_DEEPSEEK",
        "agent_violations": agent_violations,
        "deepseek_auth_profiles": deepseek_auth,
        "deepseek_model_providers": deepseek_providers,
        "deepseek_plugin_enabled": deepseek_plugin_enabled,
        "dealix_router_models": router_models,
        "forbidden_router_alias_present": forbidden_router_alias,
    }


def migrate(data: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(data)
    auth = ((out.setdefault("auth", {})).setdefault("profiles", {}))
    for name in list(auth):
        cfg = auth[name]
        if is_deepseek(name) or (isinstance(cfg, dict) and is_deepseek(cfg.get("provider"))):
            del auth[name]
    providers = ((out.setdefault("models", {})).setdefault("providers", {}))
    for name in list(providers):
        if is_deepseek(name):
            del providers[name]
    router = providers.get("dealix-router")
    if isinstance(router, dict):
        raw = router.get("models")
        if isinstance(raw, list):
            kept = []
            for item in raw:
                if isinstance(item, dict):
                    clone = copy.deepcopy(item)
                    clone["id"] = "dealix-local"
                    clone["name"] = clone.get("name") or "Dealix Local"
                    kept = [clone]
                    break
                if isinstance(item, str):
                    kept = ["dealix-local"]
                    break
            router["models"] = kept or [{"id": "dealix-local", "name": "Dealix Local"}]
        elif isinstance(raw, dict):
            router["models"] = {"dealix-local": raw.get("dealix-local", {})}
        else:
            router["models"] = [{"id": "dealix-local", "name": "Dealix Local"}]
    plugins = ((out.setdefault("plugins", {})).setdefault("entries", {}))
    if isinstance(plugins.get("deepseek"), dict):
        plugins["deepseek"]["enabled"] = False
    agents = ((out.setdefault("agents", {})).setdefault("list", []))
    for agent in agents:
        if not isinstance(agent, dict):
            continue
        cfg = agent.get("model")
        if isinstance(cfg, str):
            if is_deepseek(cfg) or cfg.endswith(("/dealix-flash", "/dealix-think", "/dealix-pro")):
                agent["model"] = {"primary": LOCAL_MODEL, "fallbacks": []}
            continue
        if not isinstance(cfg, dict):
            continue
        primary = cfg.get("primary")
        if not isinstance(primary, str) or is_deepseek(primary) or primary.endswith(("/dealix-flash", "/dealix-think", "/dealix-pro")):
            cfg["primary"] = LOCAL_MODEL
        fallbacks = cfg.get("fallbacks")
        if isinstance(fallbacks, list):
            cfg["fallbacks"] = [
                ref for ref in fallbacks
                if not is_deepseek(ref) and not str(ref).endswith(("/dealix-flash", "/dealix-think", "/dealix-pro"))
            ]
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--input", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--input", required=True)
    prepare.add_argument("--output", required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if args.command == "verify":
        result = audit_config(data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 3
    candidate = migrate(data)
    result = audit_config(candidate)
    if not result["ok"]:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 4
    output = Path(args.output)
    if output.resolve() == Path(args.input).resolve():
        raise SystemExit("refusing in-place mutation")
    output.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output.chmod(0o600)
    print(json.dumps({"prepared": str(output), "audit": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
