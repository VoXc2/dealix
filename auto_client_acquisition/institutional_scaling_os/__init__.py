"""Dealix Institutional Scaling OS.

Companion docs live under ``docs/institutional_scaling/``. Typed surfaces
for the scaling doctrine: institutional metrics (trust + market +
company), monthly control memo with ten sections, the doctrine risk
register with twelve canonical risks, the trust engine component list,
agent identity doctrine, and runtime privacy.
"""

from __future__ import annotations

from auto_client_acquisition.institutional_scaling_os.agent_identity import (
    InstitutionalAgentIdentity,
)
from auto_client_acquisition.institutional_scaling_os.control_memo import (
    CONTROL_MEMO_SECTIONS,
    InstitutionalControlMemo,
    InstitutionalControlMemoSection,
    render_control_memo,
)
from auto_client_acquisition.institutional_scaling_os.institutional_metrics import (
    InstitutionalCompanyMetrics,
    InstitutionalMarketMetrics,
    InstitutionalTrustMetrics,
    is_scaling_safe,
)
from auto_client_acquisition.institutional_scaling_os.privacy_runtime import (
    PrivacyRuntimeChecks,
    evaluate_privacy_runtime,
)
from auto_client_acquisition.institutional_scaling_os.risk_register import (
    DOCTRINE_RISKS,
    DoctrineRisk,
    RiskEntry,
    RiskLevel,
)
from auto_client_acquisition.institutional_scaling_os.trust_engine import (
    TRUST_ENGINE_COMPONENTS,
    TRUST_ENGINE_QUESTIONS,
    TrustEngineCheck,
    evaluate_trust_engine_check,
)

__all__ = [
    "InstitutionalAgentIdentity",
    "CONTROL_MEMO_SECTIONS",
    "InstitutionalControlMemo",
    "InstitutionalControlMemoSection",
    "render_control_memo",
    "InstitutionalCompanyMetrics",
    "InstitutionalMarketMetrics",
    "InstitutionalTrustMetrics",
    "is_scaling_safe",
    "PrivacyRuntimeChecks",
    "evaluate_privacy_runtime",
    "DOCTRINE_RISKS",
    "DoctrineRisk",
    "RiskEntry",
    "RiskLevel",
    "TRUST_ENGINE_COMPONENTS",
    "TRUST_ENGINE_QUESTIONS",
    "TrustEngineCheck",
    "evaluate_trust_engine_check",
]
