"""
Isolated conftest for local_ai tests.

The top-level `backend/tests/conftest.py` spins up the full FastAPI app
(database, ORM, routers) which requires every runtime dependency. The
local_ai module is pure Python + httpx, so we register a minimal stub
package structure that allows the submodules to import each other via
`app.services.local_ai.*` without pulling in the rest of `app.services`.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import types


def _register_stub_packages() -> None:
    """Create empty parent packages so submodule imports resolve."""
    # If the real `app` package already loaded successfully, leave it alone.
    if "app.services.local_ai" in sys.modules:
        return

    backend_root = pathlib.Path(__file__).resolve().parents[2]
    local_ai_dir = backend_root / "app" / "services" / "local_ai"

    # Register the parent chain as empty namespace packages.
    for pkg_name in ("app", "app.services", "app.services.local_ai"):
        if pkg_name not in sys.modules:
            sys.modules[pkg_name] = types.ModuleType(pkg_name)

    def _load(mod_name: str, filename: str) -> None:
        if mod_name in sys.modules and getattr(sys.modules[mod_name], "__file__", None):
            return
        spec = importlib.util.spec_from_file_location(mod_name, local_ai_dir / filename)
        assert spec and spec.loader, f"cannot build spec for {mod_name}"
        module = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = module
        spec.loader.exec_module(module)

    _load("app.services.local_ai.catalog", "catalog.py")
    _load("app.services.local_ai.client", "client.py")
    _load("app.services.local_ai.router", "router.py")


_register_stub_packages()
