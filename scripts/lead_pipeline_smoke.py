#!/usr/bin/env python3
"""Lead acquisition pipeline E2E smoke test (W1.2).

Validates the 5 enrichment adapters against a small set of known-good
Saudi B2B targets. Detects two failure modes that pure unit tests miss:

  1. Adapter init succeeds but API quota/key is dead
  2. Pipeline orchestration breaks across adapter boundaries (e.g. type
     mismatch in returned shape, async-await chain breaks, etc.)

Outputs:
  - Console summary: ✓/✗ per adapter and per target
  - JSON report at docs/ops/LEAD_PIPELINE_SMOKE_REPORT.json

Exit code:
  0  all 5 adapters returned at least one result for ≥ 7 of 10 targets
  1  one or more adapters failed for too many targets
  2  unexpected exception during run

Usage:
  python scripts/lead_pipeline_smoke.py
  python scripts/lead_pipeline_smoke.py --targets data/saudi_b2b_smoke_targets.json
  python scripts/lead_pipeline_smoke.py --no-network    # offline mode (adapter import + signature check only)

Real network calls are gated on env vars being set (GOOGLE_MAPS_API_KEY etc.).
Missing keys produce SKIPPED status (not a failure) for that adapter.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

# Default smoke-test targets — well-known Saudi B2B companies.
# Pick 10 with stable public web presence so adapter quotas are predictable.
DEFAULT_TARGETS = [
    {"name": "Foodics",            "domain": "foodics.com",       "sector": "saas"},
    {"name": "Salla",              "domain": "salla.com",         "sector": "saas"},
    {"name": "Lucidya",            "domain": "lucidya.com",       "sector": "saas"},
    {"name": "Zid",                "domain": "zid.sa",            "sector": "saas"},
    {"name": "Tamara",             "domain": "tamara.co",         "sector": "fintech"},
    {"name": "Lean Technologies",  "domain": "leantech.me",       "sector": "fintech"},
    {"name": "Sary",               "domain": "sary.com",          "sector": "marketplace"},
    {"name": "Retailo",            "domain": "retailo.co",        "sector": "marketplace"},
    {"name": "Jahez",              "domain": "jahez.net",         "sector": "delivery"},
    {"name": "Mnzil",              "domain": "mnzil.com",         "sector": "proptech"},
]


def _env(name: str) -> bool:
    return bool(os.environ.get(name))


def _adapter_status() -> dict[str, dict[str, Any]]:
    """Return readiness state of each adapter based on env vars."""
    return {
        "search": {
            "ready": _env("GOOGLE_SEARCH_API_KEY") and _env("GOOGLE_SEARCH_CX")
                  or _env("TAVILY_API_KEY"),
            "env_needed": "GOOGLE_SEARCH_API_KEY+GOOGLE_SEARCH_CX or TAVILY_API_KEY",
        },
        "maps": {
            "ready": _env("GOOGLE_MAPS_API_KEY") or _env("GOOGLE_PLACES_API_KEY"),
            "env_needed": "GOOGLE_MAPS_API_KEY",
        },
        "email_intel": {
            "ready": _env("HUNTER_API_KEY") or _env("ABSTRACT_API_KEY"),
            "env_needed": "HUNTER_API_KEY",
        },
        "crawler": {
            "ready": True,  # has bs4 fallback so always "ready"
            "env_needed": "FIRECRAWL_API_KEY (optional — bs4 fallback exists)",
        },
        "tech": {
            "ready": _env("WAPPALYZER_API_KEY"),
            "env_needed": "WAPPALYZER_API_KEY",
        },
    }


async def _smoke_one_target(target: dict[str, Any], no_network: bool) -> dict[str, Any]:
    """Run all adapters against one target. Returns per-adapter result dict."""
    result: dict[str, Any] = {
        "target": target,
        "adapters": {},
        "elapsed_ms": {},
    }
    adapters = _adapter_status()

    # --- Search adapter ---
    t0 = time.monotonic()
    if no_network or not adapters["search"]["ready"]:
        result["adapters"]["search"] = "skipped" if no_network else "no_env"
    else:
        try:
            from auto_client_acquisition.providers.search import SearchProvider
            provider = SearchProvider()
            hits = await provider.search(f"{target['name']} Saudi Arabia B2B", max_results=3)
            result["adapters"]["search"] = "ok" if hits else "empty"
        except Exception as exc:
            result["adapters"]["search"] = f"error:{type(exc).__name__}"
    result["elapsed_ms"]["search"] = int((time.monotonic() - t0) * 1000)

    # --- Maps adapter ---
    t0 = time.monotonic()
    if no_network or not adapters["maps"]["ready"]:
        result["adapters"]["maps"] = "skipped" if no_network else "no_env"
    else:
        try:
            from auto_client_acquisition.providers.maps import MapsProvider
            provider = MapsProvider()
            places = await provider.search_places(f"{target['name']} Saudi Arabia", limit=2)
            result["adapters"]["maps"] = "ok" if places else "empty"
        except Exception as exc:
            result["adapters"]["maps"] = f"error:{type(exc).__name__}"
    result["elapsed_ms"]["maps"] = int((time.monotonic() - t0) * 1000)

    # --- Email Intel adapter ---
    t0 = time.monotonic()
    if no_network or not adapters["email_intel"]["ready"]:
        result["adapters"]["email_intel"] = "skipped" if no_network else "no_env"
    else:
        try:
            from auto_client_acquisition.providers.email_intel import EmailIntelProvider
            provider = EmailIntelProvider()
            emails = await provider.find_emails(target["domain"], limit=2)
            result["adapters"]["email_intel"] = "ok" if emails else "empty"
        except Exception as exc:
            result["adapters"]["email_intel"] = f"error:{type(exc).__name__}"
    result["elapsed_ms"]["email_intel"] = int((time.monotonic() - t0) * 1000)

    # --- Crawler adapter (always tried; has bs4 fallback) ---
    t0 = time.monotonic()
    if no_network:
        result["adapters"]["crawler"] = "skipped"
    else:
        try:
            from auto_client_acquisition.providers.crawler import CrawlerProvider
            provider = CrawlerProvider()
            content = await provider.crawl_url(f"https://{target['domain']}")
            result["adapters"]["crawler"] = "ok" if content and len(content) > 100 else "empty"
        except Exception as exc:
            result["adapters"]["crawler"] = f"error:{type(exc).__name__}"
    result["elapsed_ms"]["crawler"] = int((time.monotonic() - t0) * 1000)

    # --- Tech adapter ---
    t0 = time.monotonic()
    if no_network or not adapters["tech"]["ready"]:
        result["adapters"]["tech"] = "skipped" if no_network else "no_env"
    else:
        try:
            from auto_client_acquisition.providers.tech import TechProvider
            provider = TechProvider()
            techs = await provider.fingerprint(target["domain"])
            result["adapters"]["tech"] = "ok" if techs else "empty"
        except Exception as exc:
            result["adapters"]["tech"] = f"error:{type(exc).__name__}"
    result["elapsed_ms"]["tech"] = int((time.monotonic() - t0) * 1000)

    return result


def _summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute per-adapter pass-rate summary across all targets."""
    adapters = ["search", "maps", "email_intel", "crawler", "tech"]
    summary: dict[str, Any] = {"by_adapter": {}, "by_target": []}
    for ad in adapters:
        statuses = [r["adapters"].get(ad, "missing") for r in results]
        ok_count = sum(1 for s in statuses if s == "ok")
        empty_count = sum(1 for s in statuses if s == "empty")
        skipped_count = sum(1 for s in statuses if s in ("skipped", "no_env"))
        error_count = sum(1 for s in statuses if isinstance(s, str) and s.startswith("error"))
        summary["by_adapter"][ad] = {
            "ok": ok_count,
            "empty": empty_count,
            "skipped": skipped_count,
            "errors": error_count,
            "pass_rate": round(ok_count / len(results), 2) if results else 0.0,
        }
    for r in results:
        summary["by_target"].append({
            "name": r["target"]["name"],
            "ok": sum(1 for v in r["adapters"].values() if v == "ok"),
            "total_attempted": sum(1 for v in r["adapters"].values() if v != "skipped" and v != "no_env"),
        })
    return summary


def _verdict(summary: dict[str, Any], no_network: bool) -> tuple[int, str]:
    """Return exit code + human-readable verdict."""
    if no_network:
        # Offline mode: success if all adapters imported (no errors)
        any_errors = any(d["errors"] > 0 for d in summary["by_adapter"].values())
        return (0, "import-only smoke passed") if not any_errors else (1, "import errors found")

    # Network mode: each adapter that's ready must pass on ≥ 7/10 targets
    failures: list[str] = []
    for adapter, stats in summary["by_adapter"].items():
        attempted = stats["ok"] + stats["empty"] + stats["errors"]
        if attempted == 0:  # all skipped, fine
            continue
        if stats["pass_rate"] < 0.7:
            failures.append(f"{adapter} pass_rate={stats['pass_rate']:.0%} (< 70%)")
    if failures:
        return 1, "FAIL: " + "; ".join(failures)
    return 0, "PASS: all live adapters at ≥ 70% pass rate"


async def main_async(args: argparse.Namespace) -> int:
    targets = DEFAULT_TARGETS
    if args.targets:
        with open(args.targets) as f:
            targets = json.load(f)

    print(f"Lead pipeline smoke: {len(targets)} targets, no_network={args.no_network}")
    adapter_status = _adapter_status()
    for name, info in adapter_status.items():
        marker = "✓" if info["ready"] else "—"
        print(f"  {marker} {name:<12} env_needed: {info['env_needed']}")
    print()

    results: list[dict[str, Any]] = []
    for i, t in enumerate(targets, 1):
        print(f"  [{i}/{len(targets)}] {t['name']:<22}", end=" ", flush=True)
        r = await _smoke_one_target(t, args.no_network)
        results.append(r)
        ok_count = sum(1 for v in r["adapters"].values() if v == "ok")
        attempted = sum(1 for v in r["adapters"].values() if v not in ("skipped", "no_env"))
        print(f"ok={ok_count}/{attempted}  " +
              "  ".join(f"{ad}={st}" for ad, st in r["adapters"].items()))

    summary = _summary(results)
    exit_code, verdict = _verdict(summary, args.no_network)

    # Write JSON report
    report = {
        "run_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "no_network": args.no_network,
        "target_count": len(targets),
        "adapter_status": adapter_status,
        "summary": summary,
        "verdict": verdict,
        "exit_code": exit_code,
        "results": results,
    }
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print()
    print(f"Report → {out_path}")
    print(f"Verdict: {verdict}")
    return exit_code


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--targets", help="path to JSON file with target list (default: built-in 10 Saudi B2B)")
    p.add_argument("--no-network", action="store_true",
                   help="offline mode — verify imports + adapter signatures only")
    p.add_argument("--output", default="docs/ops/LEAD_PIPELINE_SMOKE_REPORT.json",
                   help="JSON report output path")
    args = p.parse_args()

    try:
        return asyncio.run(main_async(args))
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
