"""Commercial doctrine — SOAEN block and non-negotiables."""

from __future__ import annotations

from dealix.commercial_ops.doctrine import (
    NON_NEGOTIABLE_RULES,
    SOAEN_CHECKLIST_AR,
    build_soaen_daily,
    doctrine_status,
    format_doctrine_markdown,
)
from dealix.commercial_ops.social_queue import SOAEN_CHECKLIST_AR as SOCIAL_SOAEN


def test_doctrine_status_ok() -> None:
    st = doctrine_status()
    assert st["ok"] is True
    assert st["rules_count"] >= 5
    assert st["checklist_count"] == len(SOAEN_CHECKLIST_AR)


def test_soaen_checklist_shared_with_social_queue() -> None:
    assert SOCIAL_SOAEN == SOAEN_CHECKLIST_AR


def test_format_doctrine_markdown_contains_rules() -> None:
    md = format_doctrine_markdown(build_soaen_daily(date_str="2026-05-18"))
    assert "no_cold_whatsapp" in md
    assert "SOAEN" in md
    for rule in NON_NEGOTIABLE_RULES:
        assert rule["id"] in md
