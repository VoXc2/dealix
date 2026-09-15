"""Production-app fail-closed guard for founder/internal web surfaces."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "apps" / "web"
MIDDLEWARE = WEB / "middleware.ts"
COMPOSE = ROOT / "deploy" / "selfhost" / "compose.yml"


def _array(name: str) -> list[str]:
    text = MIDDLEWARE.read_text(encoding="utf-8")
    match = re.search(rf"const {name} = \[(.*?)\] as const;", text, re.S)
    assert match, f"missing {name}"
    return re.findall(r'"([^\"]+)"', match.group(1))


def _matches(path: str, prefixes: list[str]) -> bool:
    return any(path == p or path.startswith(f"{p}/") for p in prefixes)


def _strip_locale(path: str) -> str:
    parts = path.split("/")
    if len(parts) > 2 and parts[1] in {"ar", "en"}:
        return "/" + "/".join(parts[2:])
    return path


def _guarded(path: str) -> bool:
    path = _strip_locale(path)
    if _matches(path, _array("PUBLIC_EXCEPTIONS")):
        return False
    if _matches(path, _array("INTERNAL_PAGE_PREFIXES")):
        return True
    parts = path.split("/")
    if len(parts) >= 3 and parts[2] in {"dashboard", "hr", "inventory", "projects", "settings"}:
        return True
    return False


def _route(page: Path) -> str:
    rel = page.relative_to(WEB / "app")
    parts = [p for p in rel.parts[:-1] if not (p.startswith("(") and p.endswith(")"))]
    return "/" + "/".join(parts)


def test_selfhost_builds_the_guarded_production_app() -> None:
    compose = COMPOSE.read_text(encoding="utf-8")
    assert "context: ../../apps/web" in compose
    assert MIDDLEWARE.exists()


def test_observed_internal_surfaces_are_fail_closed() -> None:
    for path in ("/crm", "/deals", "/approvals", "/founder/command-room"):
        assert _guarded(path), path
    text = MIDDLEWARE.read_text(encoding="utf-8")
    assert 'status: 404' in text
    assert 'DEALIX_INTERNAL_SURFACE_MODE' in text
    assert 'NODE_ENV' in text and 'production' in text
    assert 'localStorage.getItem' not in text and 'sessionStorage.getItem' not in text


def test_public_buying_and_trust_routes_remain_public() -> None:
    for path in ("/", "/book", "/pricing", "/services", "/cases", "/safety",
                 "/agents", "/products", "/sectors", "/dealix-os", "/saudi-opportunity-radar",
                 "/client-portal/demo"):
        assert not _guarded(path), path

def test_pages_that_read_tracked_commercial_ledgers_are_guarded() -> None:
    markers = (
        "@/lib/crm/crm",
        "@/lib/finance/deals",
        "business/_data",
    )
    exposed: list[str] = []
    for page in (WEB / "app").rglob("page.tsx"):
        text = page.read_text(encoding="utf-8")
        if any(marker in text for marker in markers):
            route = _route(page)
            if not _guarded(route):
                exposed.append(route)
    assert not exposed, f"commercial ledger pages not guarded: {sorted(exposed)}"


def test_founder_operational_contract_is_covered() -> None:
    required = {
        "/crm", "/operator", "/review-queue", "/outreach-lab", "/followups",
        "/command-center", "/war-room", "/pipeline", "/kpi-finance", "/deals",
        "/proof-vault", "/approvals", "/founder",
    }
    prefixes = set(_array("INTERNAL_PAGE_PREFIXES"))
    assert required <= prefixes

def test_public_radar_and_internal_proof_vault_do_not_conflict() -> None:
    assert not _guarded("/saudi-opportunity-radar")
    assert not _guarded("/ar/saudi-opportunity-radar")
    assert _guarded("/proof-vault")
    assert _guarded("/en/proof-vault")


def test_public_surfaces_do_not_link_to_internal_proof_vault() -> None:
    public_files = [
        ROOT / "apps/web/components/landing/InteractiveHome.tsx",
        ROOT / "apps/web/app/dealix-os/page.tsx",
        ROOT / "apps/web/app/ar/case-studies/page.tsx",
        ROOT / "apps/web/app/saudi-opportunity-radar/page.tsx",
    ]
    for path in public_files:
        assert 'href="/proof-vault"' not in path.read_text(encoding="utf-8"), path
