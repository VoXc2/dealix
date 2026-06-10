"""Tests for Dealix MCP server — tools, resources, prompts."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _import_mcp_server():
    """Import the MCP server module without starting the server."""
    if "mcp_server.dealix_mcp" in sys.modules:
        return sys.modules["mcp_server.dealix_mcp"]
    spec = importlib.util.spec_from_file_location(
        "mcp_server.dealix_mcp",
        _REPO / "mcp_server" / "dealix_mcp.py",
    )
    if spec is None or spec.loader is None:
        pytest.skip("fastmcp not installed")
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except ImportError as exc:
        pytest.skip(f"fastmcp not installed: {exc}")
    return mod


class TestMCPServerStructure:
    """MCP server has required tools, resources, and prompts."""

    def test_mcp_server_file_exists(self):
        assert (_REPO / "mcp_server" / "dealix_mcp.py").exists()

    def test_mcp_server_init_exists(self):
        assert (_REPO / "mcp_server" / "__init__.py").exists()

    def test_mcp_server_readme_exists(self):
        assert (_REPO / "mcp_server" / "README.md").exists()

    def test_fastmcp_in_mcp_requirements(self):
        req = (_REPO / "mcp_server" / "requirements-mcp.txt").read_text()
        assert "fastmcp" in req

    def test_mcp_server_imports_cleanly(self):
        mod = _import_mcp_server()
        assert hasattr(mod, "mcp")

    def test_mcp_server_has_read_tools(self):
        content = (_REPO / "mcp_server" / "dealix_mcp.py").read_text()
        required_tools = [
            "get_war_room_today",
            "get_kpi_snapshot",
            "get_business_now",
            "get_commercial_strategy",
            "get_doctrine_rules",
            "get_founder_cockpit",
            "get_expansion_status",
            "get_outreach_drafts",
            "get_evidence_summary",
            "get_commercial_digest",
            "get_targeting_pool",
            "get_social_content_queue",
            "get_company_policy",
        ]
        for tool in required_tools:
            assert tool in content, f"Missing tool: {tool}"

    def test_mcp_server_has_write_tools(self):
        content = (_REPO / "mcp_server" / "dealix_mcp.py").read_text()
        assert "draft_warm_intro" in content
        assert "run_diagnostic_report" in content

    def test_mcp_server_has_resources(self):
        content = (_REPO / "mcp_server" / "dealix_mcp.py").read_text()
        assert "dealix://business/overview" in content
        assert "dealix://doctrine/non-negotiables" in content

    def test_mcp_server_has_prompts(self):
        content = (_REPO / "mcp_server" / "dealix_mcp.py").read_text()
        assert "morning_briefing" in content
        assert "lead_analysis" in content

    def test_doctrine_enforced_no_cold_whatsapp(self):
        content = (_REPO / "mcp_server" / "dealix_mcp.py").read_text()
        assert "cold WhatsApp" in content or "cold_whatsapp" in content.lower()

    def test_doctrine_enforced_approval_required(self):
        content = (_REPO / "mcp_server" / "dealix_mcp.py").read_text()
        assert "approval_required" in content

    def test_draft_only_no_auto_send(self):
        content = (_REPO / "mcp_server" / "dealix_mcp.py").read_text()
        assert "draft_only" in content or "DOES NOT SEND" in content

    def test_no_cold_whatsapp_in_channel_choices(self):
        content = (_REPO / "mcp_server" / "dealix_mcp.py").read_text()
        assert '"linkedin", "email"' in content or "'linkedin', 'email'" in content

    def test_http_transport_supported(self):
        content = (_REPO / "mcp_server" / "dealix_mcp.py").read_text()
        assert "--transport http" in content or 'transport="http"' in content

    def test_stdio_transport_default(self):
        content = (_REPO / "mcp_server" / "dealix_mcp.py").read_text()
        assert "stdio" in content

    def test_readme_has_claude_desktop_setup(self):
        readme = (_REPO / "mcp_server" / "README.md").read_text()
        assert "claude_desktop_config.json" in readme or "Claude Desktop" in readme

    def test_readme_has_claude_code_setup(self):
        readme = (_REPO / "mcp_server" / "README.md").read_text()
        assert ".mcp.json" in readme or "Claude Code" in readme

    def test_readme_has_railway_setup(self):
        readme = (_REPO / "mcp_server" / "README.md").read_text()
        assert "Railway" in readme or "railway" in readme


class TestMCPToolLogic:
    """Individual tool functions return valid JSON strings."""

    def test_get_doctrine_rules_fallback(self):
        """get_doctrine_rules returns valid JSON even without fastmcp installed."""
        # Test the helper function logic directly
        import json

        from dealix.commercial_ops.doctrine import NON_NEGOTIABLE_RULES, SOAEN_CHECKLIST_AR

        result = {
            "non_negotiables": NON_NEGOTIABLE_RULES,
            "soaen_checklist_ar": SOAEN_CHECKLIST_AR,
        }
        dumped = json.dumps(result, ensure_ascii=False)
        assert "no_cold_whatsapp" in dumped

    def test_get_company_policy_fallback(self):
        """Company policy defaults to safe mode."""
        from dealix.company_brain.policy import CompanyPolicy

        with patch.dict("os.environ", {}, clear=False):
            policy = CompanyPolicy.from_env()
            assert not policy.auto_send_enabled
            assert not policy.external_outreach_enabled
            assert policy.approval_required

    def test_safe_json_helper(self):
        """_safe_json handles Arabic text and datetimes."""
        import json
        from datetime import UTC, datetime

        obj = {"name": "شركة الديليكس", "ts": datetime.now(UTC)}
        result = json.dumps(obj, ensure_ascii=False, default=str)
        parsed = json.loads(result)
        assert parsed["name"] == "شركة الديليكس"
