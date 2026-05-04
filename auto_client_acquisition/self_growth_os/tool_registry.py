"""Lightweight optional-tooling registry.

Introspects which optional packages the Self-Growth OS *can* use,
without forcing them as dependencies. Returns a list of
``ToolCapability`` records. Useful for the
``/api/v1/self-growth/tooling`` endpoint and for deciding which
phases can be built next without provisioning anything new.

This module never installs anything. It only inspects.
"""
from __future__ import annotations

import importlib
from dataclasses import dataclass

from auto_client_acquisition.self_growth_os.schemas import ToolCapability


@dataclass(frozen=True)
class _ToolSpec:
    name: str
    module: str
    required_for_core: bool
    install_hint: str
    safe_usage_notes: str


# Curated registry — each tool maps to a concrete capability the
# Self-Growth OS would use IF installed. This list is short and
# intentional; we do not try to enumerate every package on PyPI.
TOOL_SPECS: tuple[_ToolSpec, ...] = (
    _ToolSpec(
        name="pyyaml",
        module="yaml",
        required_for_core=True,
        install_hint="pip install pyyaml>=6.0",
        safe_usage_notes="Loads docs/registry/SERVICE_READINESS_MATRIX.yaml.",
    ),
    _ToolSpec(
        name="pydantic",
        module="pydantic",
        required_for_core=True,
        install_hint="pip install 'pydantic>=2.9'",
        safe_usage_notes="Schemas for typed self-growth records.",
    ),
    _ToolSpec(
        name="fastapi",
        module="fastapi",
        required_for_core=True,
        install_hint="pip install 'fastapi>=0.115'",
        safe_usage_notes="Hosts /api/v1/self-growth/* read-only endpoints.",
    ),
    _ToolSpec(
        name="httpx",
        module="httpx",
        required_for_core=True,
        install_hint="pip install 'httpx>=0.27'",
        safe_usage_notes="Outbound HTTP. Never used for scraping.",
    ),
    _ToolSpec(
        name="anthropic",
        module="anthropic",
        required_for_core=False,
        install_hint="pip install 'anthropic>=0.40'",
        safe_usage_notes="Quality LLM provider; multi-provider router falls back.",
    ),
    _ToolSpec(
        name="openai",
        module="openai",
        required_for_core=False,
        install_hint="pip install 'openai>=1.54'",
        safe_usage_notes="Optional LLM provider.",
    ),
    _ToolSpec(
        name="google-generativeai",
        module="google.generativeai",
        required_for_core=False,
        install_hint="pip install 'google-generativeai>=0.8'",
        safe_usage_notes="Optional Gemini provider.",
    ),
    _ToolSpec(
        name="beautifulsoup4",
        module="bs4",
        required_for_core=False,
        install_hint="pip install beautifulsoup4 lxml",
        safe_usage_notes=(
            "Allowed only for parsing OUR OWN landing/*.html during seo_audit. "
            "Never used to crawl third-party sites."
        ),
    ),
    _ToolSpec(
        name="lxml",
        module="lxml",
        required_for_core=False,
        install_hint="pip install lxml",
        safe_usage_notes="Faster HTML parsing for seo_audit.",
    ),
    _ToolSpec(
        name="markdown",
        module="markdown",
        required_for_core=False,
        install_hint="pip install markdown",
        safe_usage_notes="Render brief drafts to HTML for preview.",
    ),
    _ToolSpec(
        name="defusedxml",
        module="defusedxml",
        required_for_core=False,
        install_hint="pip install defusedxml",
        safe_usage_notes="Safer XML/sitemap parsing.",
    ),
    _ToolSpec(
        name="opentelemetry-api",
        module="opentelemetry",
        required_for_core=False,
        install_hint="pip install 'opentelemetry-api>=1.41'",
        safe_usage_notes="Optional traces; NEVER log PII.",
    ),
    _ToolSpec(
        name="redis",
        module="redis",
        required_for_core=True,
        install_hint="pip install 'redis[hiredis]>=5.1'",
        safe_usage_notes="Backs the existing ApprovalGate for draft approvals.",
    ),
    _ToolSpec(
        name="sqlalchemy",
        module="sqlalchemy",
        required_for_core=True,
        install_hint="pip install 'sqlalchemy>=2.0'",
        safe_usage_notes="Persists self-growth records (when wired).",
    ),
    _ToolSpec(
        name="structlog",
        module="structlog",
        required_for_core=True,
        install_hint="pip install structlog",
        safe_usage_notes="Structured logging for evidence_collector.",
    ),
)


def _is_installed(module_name: str) -> bool:
    """Check if a module is importable.

    Catches *any* exception (including BaseException-derived panics
    from C extensions) — some optional packages have native import
    paths that can panic on incomplete sandbox environments. We
    treat any failure as "not installed" rather than letting it
    propagate. Production deploys install the full requirements set
    from a clean image and do not hit these paths.
    """
    try:
        importlib.import_module(module_name)
        return True
    except BaseException:  # noqa: BLE001 — intentional broad catch for panics
        return False


def audit() -> list[ToolCapability]:
    """Return one ToolCapability per registered tool."""
    out: list[ToolCapability] = []
    for spec in TOOL_SPECS:
        out.append(
            ToolCapability.new(
                source="self_growth_os.tool_registry",
                tool_name=spec.name,
                installed=_is_installed(spec.module),
                required_for_core=spec.required_for_core,
                install_hint=spec.install_hint,
                safe_usage_notes=spec.safe_usage_notes,
                recommended_action=(
                    "ok"
                    if _is_installed(spec.module)
                    else f"install: {spec.install_hint}"
                ),
            )
        )
    return out


def core_required_missing() -> list[str]:
    """Return tool names where required_for_core=True but installed=False."""
    return [t.tool_name for t in audit() if t.required_for_core and not t.installed]
