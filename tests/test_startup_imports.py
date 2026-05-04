"""
Static guard: every module reachable from `api.main` must import cleanly.

If a top-level `import x` lands in any module that uvicorn loads at boot
(directly or transitively), and `x` isn't in requirements.txt, the
production container crashes on `import api.main` before the
healthcheck can ever return — Railway times out and shows
"Network → Healthcheck failed" with no useful traceback in the user-facing
deployment view.

This test catches that class of regression in CI: it imports the FastAPI
factory and every router. Any missing third-party dep produces a clean
ModuleNotFoundError here, not a Railway healthcheck timeout.
"""

from __future__ import annotations

import importlib

# Modules that uvicorn loads at boot via `api.main:app`.
# Adding a new router → add it here. If a router can't import cleanly
# in CI, do not ship it: production will fail healthcheck.
_BOOT_MODULES = (
    "api.main",
    "api.routers.health",
    "api.routers.operator",
    "api.routers.services",
    "api.routers.prospects",
    "api.routers.proof_ledger",
    "api.routers.role_briefs",
    "api.routers.whatsapp_briefs",
    "api.routers.payments",
    "api.routers.support",
    "auto_client_acquisition.safety",
    "auto_client_acquisition.customer_ops",
    "auto_client_acquisition.revenue_company_os.proof_pack_pdf",  # imports jinja2
    "scripts.migrate_add_hubspot_deal_id",
)


def test_all_boot_modules_import_cleanly() -> None:
    """Production-image-equivalent import smoke."""
    failures: list[str] = []
    for name in _BOOT_MODULES:
        try:
            importlib.import_module(name)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{name}: {type(exc).__name__}: {exc}")
    assert not failures, (
        "Modules failed to import — production container would crash at boot:\n  - "
        + "\n  - ".join(failures)
    )


def test_jinja2_is_importable() -> None:
    """Pin jinja2 specifically — proof_pack_pdf depends on it at module level."""
    import jinja2  # noqa: F401
