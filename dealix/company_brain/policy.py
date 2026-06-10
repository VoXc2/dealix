import os
from dataclasses import dataclass


@dataclass(frozen=True)
class CompanyPolicy:
    auto_send_enabled: bool = False
    external_outreach_enabled: bool = False
    approval_required: bool = True

    @classmethod
    def from_env(cls):
        return cls(
            auto_send_enabled=os.getenv("AUTO_SEND_ENABLED", "false").lower() == "true",
            external_outreach_enabled=os.getenv("EXTERNAL_OUTREACH_ENABLED", "false").lower() == "true",
            approval_required=os.getenv("AGENT_APPROVAL_MODE", "required").lower() != "off",
        )

    def assert_safe(self):
        if self.auto_send_enabled:
            raise RuntimeError("AUTO_SEND_ENABLED must stay false.")
        if self.external_outreach_enabled:
            raise RuntimeError("EXTERNAL_OUTREACH_ENABLED must stay false.")
        if not self.approval_required:
            raise RuntimeError("AGENT_APPROVAL_MODE must stay required.")
