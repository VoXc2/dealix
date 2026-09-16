#!/usr/bin/env python3
"""Verify self-host measurement source wiring without exposing config values."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCKERFILE = ROOT / "apps/web/Dockerfile"
COMPOSE = ROOT / "deploy/selfhost/compose.yml"
POSTHOG = ROOT / "apps/web/lib/analytics/posthog.tsx"
ENV_EXAMPLE = ROOT / "apps/web/.env.example"
CSP = ROOT / "apps/web/next.config.js"
APPROVED_HOST = "https://us.i.posthog.com"


def env_names(path: Path) -> dict[str, bool]:
    result: dict[str, bool] = {}
    if not path.is_file():
        return result
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = bool(value.strip())
    return result


def source_errors() -> list[str]:
    errors: list[str] = []
    dockerfile = DOCKERFILE.read_text(encoding="utf-8")
    compose = COMPOSE.read_text(encoding="utf-8")
    posthog = POSTHOG.read_text(encoding="utf-8")
    example = ENV_EXAMPLE.read_text(encoding="utf-8")
    csp = CSP.read_text(encoding="utf-8")
    required = {
        "Dockerfile build key arg": (dockerfile, 'ARG NEXT_PUBLIC_POSTHOG_KEY=""'),
        "Dockerfile build host arg": (dockerfile, f'ARG NEXT_PUBLIC_POSTHOG_HOST="{APPROVED_HOST}"'),
        "Compose build key arg": (compose, "NEXT_PUBLIC_POSTHOG_KEY: ${NEXT_PUBLIC_POSTHOG_KEY:-}"),
        "Compose build host arg": (compose, f"NEXT_PUBLIC_POSTHOG_HOST: ${{NEXT_PUBLIC_POSTHOG_HOST:-{APPROVED_HOST}}}"),
        "PostHog host default": (posthog, APPROVED_HOST),
        "Example host default": (example, f"NEXT_PUBLIC_POSTHOG_HOST={APPROVED_HOST}"),
        "CSP ingest host": (csp, APPROVED_HOST),
        "Explicit opt-in": (posthog, 'consent !== "granted"'),
        "Autocapture disabled": (posthog, "autocapture: false"),
        "Pageview disabled": (posthog, "capture_pageview: false"),
        "Pageleave disabled": (posthog, "capture_pageleave: false"),
        "Replay disabled": (posthog, "disable_session_recording: true"),
        "Identified-only profiles": (posthog, 'person_profiles: "identified_only"'),
    }
    for label, (text, token) in required.items():
        if token not in text:
            errors.append(label)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path, default=ROOT / ".env.prod")
    args = parser.parse_args()
    errors = source_errors()
    if errors:
        print("MEASUREMENT_SOURCE_WIRING=FAIL")
        for error in errors:
            print(f"ERROR={error}")
        return 1
    names = env_names(args.env_file)
    key_present = names.get("NEXT_PUBLIC_POSTHOG_KEY", False)
    host_present = names.get("NEXT_PUBLIC_POSTHOG_HOST", False)
    print("MEASUREMENT_SOURCE_WIRING=PASS")
    print(f"POSTHOG_KEY_CONFIGURED={'YES' if key_present else 'NO'}")
    print(f"POSTHOG_HOST_EXPLICIT={'YES' if host_present else 'NO_DEFAULT_APPROVED'}")
    if not key_present:
        print("MEASUREMENT_STATE=MEASUREMENT_NOT_PROVEN")
    else:
        print("MEASUREMENT_STATE=CONFIGURED_NOT_EVENT_PROOF")
    print("TRAFFIC_OR_DEMAND_INFERENCE=PROHIBITED_WITHOUT_EVENTS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
