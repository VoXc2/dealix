"""Filesystem readiness helpers for platform systems 46-55."""

from __future__ import annotations

from pathlib import Path

from auto_client_acquisition.agentic_economic_os.systems_registry import (
    FINAL_CIVILIZATIONAL_SYSTEMS,
    all_required_platform_paths,
    missing_required_paths,
)


def collect_platform_paths(repo_root: str | Path) -> set[str]:
    """Collect discovered platform path entries from repository."""
    root = Path(repo_root)
    platform_root = root / "platform"
    if not platform_root.exists():
        return set()

    discovered: set[str] = set()
    for path in platform_root.rglob("*"):
        if path.is_dir():
            rel = path.relative_to(root).as_posix()
            discovered.add(rel)
    return discovered


def platform_readiness_snapshot(repo_root: str | Path) -> dict[str, object]:
    """Return coverage and missing paths for the final platform model."""
    discovered = collect_platform_paths(repo_root)
    required = set(all_required_platform_paths())
    missing = missing_required_paths(discovered)
    covered = len(required) - len(missing)
    coverage_pct = round((covered / len(required)) * 100, 2) if required else 0.0

    systems: list[dict[str, object]] = []
    for system in FINAL_CIVILIZATIONAL_SYSTEMS:
        required_paths = set(system.required_platform_paths)
        missing_for_system = sorted(required_paths.difference(discovered))
        systems.append(
            {
                "system_id": system.system_id,
                "key": system.key,
                "title": system.title,
                "covered": len(missing_for_system) == 0,
                "coverage_pct": round(
                    ((len(required_paths) - len(missing_for_system)) / len(required_paths)) * 100,
                    2,
                ),
                "missing_paths": missing_for_system,
            }
        )

    return {
        "required_paths_total": len(required),
        "covered_paths": covered,
        "coverage_pct": coverage_pct,
        "missing_paths": missing,
        "systems": systems,
    }
