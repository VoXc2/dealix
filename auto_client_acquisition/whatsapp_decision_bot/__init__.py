"""Internal WhatsApp Decision Layer (Phase 7).

Admin-only. NEVER sends to customers. Provides:
- Brief: "وش الوضع اليوم؟" → today's status
- Command parser: Saudi Arabic commands → structured action
- Approval preview: shows what WOULD be sent if approved
- Policy: blocks every customer-outbound attempt

Reuses whatsapp_safe_send 6 gates as decision-only checks
(never calls send_text()).
"""
from auto_client_acquisition.whatsapp_decision_bot.approval_preview import (
    preview_action,
)
from auto_client_acquisition.whatsapp_decision_bot.brief_builder import (
    build_brief,
)
from auto_client_acquisition.whatsapp_decision_bot.command_parser import (
    SUPPORTED_COMMANDS,
    parse_command,
)

__all__ = [
    "SUPPORTED_COMMANDS",
    "build_brief",
    "parse_command",
    "preview_action",
]
