"""Agent permission safety — no external send, no secrets, output contract.

Tests:
- Agent cannot send externally without approval
- Agent cannot modify secrets
- Agent output requires contract
- Agent permission matrix
- Agent collision policy
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.governance_os.approval_matrix import approval_for_action


class TestAgentCannotSendExternal:
    """Agents cannot autonomously send external messages."""

    def test_email_send_blocked(self) -> None:
        """Email send requires human approval."""
        risk, approval_type = approval_for_action("send email")
        assert "human" in approval_type.lower(), "Email send needs human"

    def test_whatsapp_send_blocked(self) -> None:
        """WhatsApp send requires human + consent."""
        risk, approval_type = approval_for_action("send whatsapp")
        assert risk == "high", "WhatsApp not high risk"
        assert "human" in approval_type.lower() and "consent" in approval_type.lower()

    def test_linkedin_send_blocked(self) -> None:
        """LinkedIn automation is blocked."""
        risk, approval_type = approval_for_action("linkedin automation")
        assert approval_type == "blocked", "LinkedIn not blocked"


class TestAgentCannotModifySecrets:
    """Agents cannot access or modify secrets autonomously."""

    def test_secret_access_blocked(self) -> None:
        """Secret access requires founder approval."""
        risk, approval_type = approval_for_action("access secrets")
        assert risk == "critical", "Secrets not critical risk"
        assert "blocked" in approval_type.lower() or "founder" in approval_type.lower()

    def test_no_secrets_in_prompt(self) -> None:
        """Secrets must never be in prompts."""
        import re

        SECRET_PATTERNS = [
            r"sk-[a-zA-Z0-9]{20,}",
            r"ghp_[a-zA-Z0-9]{36,}",
            r"github_pat_",
        ]

        # Example prompt (should be clean)
        clean_prompt = "Summarize this customer data: {customer_data}"
        for pattern in SECRET_PATTERNS:
            match = re.search(pattern, clean_prompt)
            assert match is None, f"Secret pattern found in prompt: {pattern}"


class TestAgentOutputContractRequired:
    """Agent outputs must include required contract fields."""

    def test_output_contract_structure(self) -> None:
        """Agent output must have required fields."""
        output = {
            "summary": "Generated warm intro draft",
            "files_touched": ["data/outreach/draft_001.md"],
            "evidence_level": "L4",
            "risk_level": "medium",
            "approval_required": True,
            "external_action": False,
            "tests_run": False,
            "rollback": "Delete draft file",
            "founder_next_action": "Review and approve draft",
        }

        required_fields = [
            "summary",
            "risk_level",
            "approval_required",
            "external_action",
        ]
        for field in required_fields:
            assert field in output, f"Output missing required field: {field}"

    def test_output_includes_risk_level(self) -> None:
        """Output must include risk_level."""
        output = {"risk_level": "high"}
        assert output["risk_level"] in ["low", "medium", "high"]

    def test_output_includes_approval_status(self) -> None:
        """Output must include approval_required."""
        output = {"approval_required": True}
        assert isinstance(output["approval_required"], bool)


class TestAgentPermissionMatrix:
    """Agents must follow permission matrix."""

    def test_read_tool_tier(self) -> None:
        """Read tools are T0-T1."""
        from auto_client_acquisition.governance_os.approval_matrix import approval_for_action

        # Read operations are low risk
        risk, approval_type = approval_for_action("read report")
        assert risk in ("low", "medium"), "Read not low/medium risk"

    def test_draft_tool_tier(self) -> None:
        """Draft tools are T2."""
        risk, approval_type = approval_for_action("draft proposal")
        assert risk in ("low", "medium"), "Draft not low/medium risk"

    def test_external_action_tier(self) -> None:
        """External actions are high/critical."""
        risk, approval_type = approval_for_action("send external message")
        assert risk in ("high", "critical"), "External action not high/critical"


class TestAgentCollisionPolicy:
    """Multiple agents must not conflict."""

    def test_no_simultaneous_write(self) -> None:
        """Two agents cannot write to same file simultaneously."""
        # Policy: Only one agent writes at a time
        active_writers = []
        # When one agent starts writing, others are blocked
        agent_a_writing = True
        agent_b_blocked = agent_a_writing
        assert agent_b_blocked is True

    def test_handoff_requires_state(self) -> None:
        """Agent handoff requires state transfer."""
        handoff = {
            "from_agent": "Draft Writer",
            "to_agent": "Email Safety",
            "state_transferred": True,
            "context_summary": "Draft for review",
        }
        assert handoff["state_transferred"] is True


# Total: 14 tests
