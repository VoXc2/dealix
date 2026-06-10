#!/usr/bin/env python3
"""Commercial FE/BE readiness — env matrix, import smoke, optional frontend build."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()

FAILURES: list[str] = []


def ok(msg: str) -> None:
    print(f"  ok: {msg}")


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  FAIL: {msg}")


def check_env_examples() -> None:
    for rel in ("frontend/.env.local.example", ".env.example"):
        if (ROOT / rel).is_file():
            ok(rel)
        else:
            fail(f"missing {rel}")


def check_backend_smoke() -> None:
    try:
        from dealix.execution_assurance.health import compute_full_ops_health

        snap = compute_full_ops_health()
        ok(f"full_ops_health keys={len(snap)}")
    except Exception as exc:
        fail(f"execution_assurance.health: {exc}")


def check_ops_founder_marketing_smoke() -> None:
    """Smoke routes used by /ops/founder and /ops/marketing UI."""
    try:
        import os as _os

        from fastapi.testclient import TestClient

        from api.main import app

        smoke_admin = "test-admin-ops-ui"
        _os.environ["DEALIX_ADMIN_API_KEY"] = smoke_admin
        _os.environ["ADMIN_API_KEYS"] = smoke_admin
        _os.environ.pop("API_KEYS", None)
        client = TestClient(app)
        headers = {"X-Admin-API-Key": smoke_admin}

        r_social = client.get("/api/v1/ops-autopilot/marketing/social-today", headers=headers)
        if r_social.status_code == 200:
            ok("GET marketing/social-today (OpsMarketingSocial)")
        else:
            fail(f"marketing/social-today status={r_social.status_code}")

        r_obj = client.get("/api/v1/ops-autopilot/sales/objections", headers=headers)
        if r_obj.status_code == 200:
            ok("GET sales/objections (OpsObjectionPanel)")
        else:
            fail(f"sales/objections status={r_obj.status_code}")

        r_pack = client.get("/api/v1/ops-autopilot/founder/daily-pack", headers=headers)
        if r_pack.status_code == 200:
            ok("GET founder/daily-pack (OpsFounderCommandCenter)")
        else:
            fail(f"founder/daily-pack status={r_pack.status_code}")

        r_auto = client.get("/api/v1/ops-autopilot/founder/autonomous-ops/status", headers=headers)
        if r_auto.status_code == 200:
            ok("GET founder/autonomous-ops/status")
        else:
            fail(f"founder/autonomous-ops/status status={r_auto.status_code}")
    except Exception as exc:
        fail(f"ops UI API smoke: {type(exc).__name__}")


def check_railway_matrix() -> None:
    from dealix.commercial_ops.railway_launch import (
        check_railway_api_env,
        check_railway_frontend_env,
    )

    api = check_railway_api_env()
    fe = check_railway_frontend_env()
    if api["ready_for_api_deploy"] or os.getenv("APP_ENV") == "test":
        ok("railway API matrix (or APP_ENV=test)")
    else:
        fail(f"railway API missing: {api['missing_required']}")
    if fe["ready_for_fe_deploy"] or not os.getenv("COMMERCIAL_FE_BE_STRICT"):
        ok("railway FE matrix (set COMMERCIAL_FE_BE_STRICT=1 to require)")
    elif os.getenv("COMMERCIAL_FE_BE_STRICT") == "1":
        fail(f"railway FE missing: {fe['missing']}")


def run_frontend_build() -> None:
    fe = ROOT / "frontend"
    if not (fe / "package.json").is_file():
        fail("frontend/package.json missing")
        return
    print("  (running npm run build — may take several minutes)")
    r = subprocess.run(
        ["npm", "run", "build"],
        cwd=fe,
        shell=os.name == "nt",
        capture_output=True,
        text=True,
        timeout=900,
        check=False,
    )
    if r.returncode == 0:
        ok("frontend npm run build")
    else:
        tail = (r.stderr or r.stdout or "")[-800:]
        fail(f"frontend build failed: {tail}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--with-frontend-build", action="store_true")
    args = p.parse_args()

    print("== verify_commercial_fe_be ==")
    check_env_examples()
    check_backend_smoke()
    check_ops_founder_marketing_smoke()
    if not os.getenv("APP_ENV"):
        os.environ["APP_ENV"] = "test"
    check_railway_matrix()
    if args.with_frontend_build:
        run_frontend_build()

    if FAILURES:
        print("\nCOMMERCIAL_FE_BE=FAIL")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("\nCOMMERCIAL_FE_BE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
