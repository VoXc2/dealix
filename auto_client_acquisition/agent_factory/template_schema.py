"""Design-time agent template schema.

The Agent Factory is the design-time layer above ``ai_workforce``: it
defines reusable, governed agent templates that compile down to a
runtime ``AgentSpec``. Every template must declare bounded escalation
and a risk class (honors ``no_unbounded_agents``).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from auto_client_acquisition.ai_workforce.schemas import AutonomyLevel, RiskLevel

# The 5 action modes the Operating Constitution (Article 5) permits.
ACTION_MODES: frozenset[str] = frozenset(
    {"suggest_only", "draft_only", "approval_required", "approved_manual", "blocked"}
)

# Tool tokens that may never appear in a template's allowed_tools.
FORBIDDEN_TOOL_TOKENS: frozenset[str] = frozenset(
    {
        "cold_whatsapp",
        "linkedin_automation",
        "scrape_web",
        "send_email_live",
        "send_whatsapp_live",
        "charge_payment_live",
    }
)


@dataclass(frozen=True, slots=True)
class EscalationRule:
    """When an agent must hand off to a human, and to whom."""

    trigger: str
    escalate_to: str
    action_mode: str


@dataclass(frozen=True, slots=True)
class MemoryPolicy:
    """What an agent template is allowed to remember.

    ``cross_customer`` must always be False — tenant isolation is a
    non-negotiable.
    """

    episodic: bool
    semantic: bool
    cross_customer: bool
    ttl_hours: int


@dataclass(frozen=True, slots=True)
class AgentTemplate:
    """A reusable, governed agent definition."""

    template_id: str
    role_en: str
    role_ar: str
    goals: tuple[str, ...]
    allowed_tools: tuple[str, ...]
    forbidden_tools: tuple[str, ...]
    permissions: tuple[str, ...]
    autonomy_level: AutonomyLevel
    memory_policy: MemoryPolicy
    escalation_rules: tuple[EscalationRule, ...]
    eval_metrics: tuple[str, ...]
    risk_class: RiskLevel
    cost_budget_usd: float
    default_action_mode: str = "draft_only"
    evidence_required: bool = True

    def to_dict(self) -> dict[str, object]:
        return {
            "template_id": self.template_id,
            "role_en": self.role_en,
            "role_ar": self.role_ar,
            "goals": list(self.goals),
            "allowed_tools": list(self.allowed_tools),
            "forbidden_tools": list(self.forbidden_tools),
            "permissions": list(self.permissions),
            "autonomy_level": str(self.autonomy_level),
            "memory_policy": {
                "episodic": self.memory_policy.episodic,
                "semantic": self.memory_policy.semantic,
                "cross_customer": self.memory_policy.cross_customer,
                "ttl_hours": self.memory_policy.ttl_hours,
            },
            "escalation_rules": [
                {
                    "trigger": e.trigger,
                    "escalate_to": e.escalate_to,
                    "action_mode": e.action_mode,
                }
                for e in self.escalation_rules
            ],
            "eval_metrics": list(self.eval_metrics),
            "risk_class": str(self.risk_class),
            "cost_budget_usd": self.cost_budget_usd,
            "default_action_mode": self.default_action_mode,
            "evidence_required": self.evidence_required,
        }
