from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = ROOT / "scripts" / "ops" / "verify_public_truth_seo.py"
SPEC = importlib.util.spec_from_file_location("public_truth_verify", VERIFY_PATH)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def test_current_repository_public_truth_contract_passes():
    assert MOD.verify(ROOT) == []


def test_fourth_internal_sitemap_surface_fails(tmp_path: Path):
    for relative in [
        "apps/web/app/sitemap.ts",
        "apps/web/app/robots.ts",
        "apps/web/app/layout.tsx",
        "apps/web/app/pricing/page.tsx",
        "apps/web/app/book/layout.tsx",
        "apps/web/app/company/layout.tsx",
        "apps/web/app/dealix-os/layout.tsx",
        "apps/web/app/saudi-opportunity-radar/page.tsx",
        "apps/web/next.config.js",
        "landing/pricing.html",
        "landing/academy.html",
    ]:
        source = ROOT / relative
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    sitemap = tmp_path / "apps/web/app/sitemap.ts"
    sitemap.write_text(
        sitemap.read_text(encoding="utf-8").replace(
            "const pages:",
            'const injected = { path: "/control-plane" };\n  const pages:',
        ),
        encoding="utf-8",
    )
    assert any(item.startswith("SITEMAP_ADVERTISES_INTERNAL:/control-plane") for item in MOD.verify(tmp_path))


def test_retired_revenue_os_metadata_fails(tmp_path: Path):
    for relative in [
        "apps/web/app/sitemap.ts",
        "apps/web/app/robots.ts",
        "apps/web/app/layout.tsx",
        "apps/web/app/pricing/page.tsx",
        "apps/web/app/book/layout.tsx",
        "apps/web/app/company/layout.tsx",
        "apps/web/app/dealix-os/layout.tsx",
        "apps/web/app/saudi-opportunity-radar/page.tsx",
        "apps/web/next.config.js",
        "landing/pricing.html",
        "landing/academy.html",
    ]:
        source = ROOT / relative
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    layout = tmp_path / "apps/web/app/layout.tsx"
    layout.write_text(layout.read_text(encoding="utf-8") + "\n// خلال أسبوع واحد\n", encoding="utf-8")
    assert "RETIRED_METADATA:خلال أسبوع واحد" in MOD.verify(tmp_path)
