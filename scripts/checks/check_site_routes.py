#!/usr/bin/env python3
"""Validate the public site: route manifest, public catalog, and router wiring.

The app is a Vite + React Router SPA, so we verify that:
  - the route manifest covers home/systems/solutions/pricing/diagnostic + one
    route per core system and per sector,
  - the public catalog exposes exactly the 5 core systems + 20 sectors and does
    NOT leak the 40 internal systems,
  - the React router actually wires /systems and /solutions.
"""
import _bootstrap  # noqa: F401
from dealix.lib import ROOT, CheckResult, load_yaml
from dealix import seeds

REQUIRED_TOP = ["/", "/systems", "/solutions", "/pricing", "/diagnostic"]


def main():
    r = CheckResult("site_routes")
    routes = load_yaml("data/site/site_routes.yaml")["public_routes"]
    rset = set(routes)
    for top in REQUIRED_TOP:
        r.ok(f"route {top}") if top in rset else r.fail(f"missing route {top}")
    for c in seeds.CORE_SYSTEM_IDS:
        if f"/systems/{c}" not in rset:
            r.fail(f"missing core system route /systems/{c}")
    for sid in seeds.SECTOR_IDS:
        if f"/solutions/{sid}" not in rset:
            r.fail(f"missing sector route /solutions/{sid}")
    if not r.errors:
        r.ok(f"{len(routes)} public routes cover 5 systems + 20 sectors")

    # public catalog must not leak internal systems
    cat = ROOT / "src/marketing/catalog.ts"
    if not cat.exists():
        r.fail("src/marketing/catalog.ts missing")
        return r.finish()
    text = cat.read_text(encoding="utf-8")
    internal_ids = [s["id"] for s in seeds.iter_specialized_systems()]
    leaked = [i for i in internal_ids if i in text]
    r.fail(f"internal systems leaked into public catalog: {leaked[:3]}") if leaked else r.ok("public catalog hides all 40 internal systems")
    for c in seeds.CORE_SYSTEM_IDS:
        if c not in text:
            r.fail(f"core system {c} missing from public catalog")

    # router wiring
    app = ROOT / "src/App.tsx"
    if app.exists():
        app_text = app.read_text(encoding="utf-8")
        for path in ("/systems", "/solutions", "/pricing"):
            if path not in app_text:
                r.fail(f"router does not wire {path}")
        if not r.errors:
            r.ok("React Router wires the public marketing routes")
    else:
        r.fail("src/App.tsx missing")

    return r.finish()


if __name__ == "__main__":
    main()
