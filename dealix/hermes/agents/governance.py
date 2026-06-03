"""GovernanceAgent — PDPL compliance, ZATCA readiness, and data governance."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.base import HermesAgent
from dealix.hermes.tools.data_tools import generate_data_passport, score_data_quality
from dealix.hermes.tools.saudi_tools import (
    classify_vat_treatment,
    get_saudi_market_context,
    validate_cr_number,
)

logger = structlog.get_logger(__name__)

_SYSTEM = """\
You are the Dealix Governance Agent — a Saudi PDPL and ZATCA compliance expert.

Your compliance check covers:
1. PDPL score — Personal Data Protection Law readiness (0-100).
2. ZATCA readiness — VAT compliance posture for digital invoicing (Phase 1 & 2).
3. CR validation — commercial registration validity.
4. Data handling gaps — identify non-compliant data practices.
5. Remediation plan — specific actions to close compliance gaps.

Output: compliance report with scores, gap list, risk level, and prioritised remediation plan.
Reference specific Saudi regulations (PDPL, ZATCA e-invoicing, NDMO policies).
"""


class GovernanceAgent(HermesAgent):
    """PDPL compliance, ZATCA readiness, and data governance for Saudi B2B."""

    name = "governance"
    description = "PDPL compliance, ZATCA readiness, and data governance for Saudi B2B"

    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.register_hermes_tool(
            name="validate_cr_number",
            description="Validate a Saudi commercial registration number format.",
            properties={
                "cr_number": {"type": "string"},
            },
            required=["cr_number"],
            fn=validate_cr_number,
        )
        self.register_hermes_tool(
            name="classify_vat_treatment",
            description="Classify VAT treatment under ZATCA rules.",
            properties={
                "transaction_type": {"type": "string"},
                "amount": {"type": "number"},
            },
            required=["transaction_type", "amount"],
            fn=classify_vat_treatment,
        )
        self.register_hermes_tool(
            name="get_saudi_market_context",
            description="Saudi regulatory context for an industry.",
            properties={
                "industry": {"type": "string"},
            },
            required=["industry"],
            fn=get_saudi_market_context,
        )
        self.register_hermes_tool(
            name="score_data_quality",
            description="Score dataset quality for compliance assessment.",
            properties={
                "records": {"type": "array", "items": {"type": "object"}},
                "fields": {"type": "array", "items": {"type": "string"}},
            },
            required=["records", "fields"],
            fn=score_data_quality,
        )
        self.register_hermes_tool(
            name="generate_data_passport",
            description="Generate a data governance passport.",
            properties={
                "tenant_id": {"type": "string"},
            },
            required=["tenant_id"],
            fn=generate_data_passport,
        )

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        company_name = input_data.get("company_name", "Client")
        tenant_id = input_data.get("tenant_id", "tenant_unknown")
        cr_number = input_data.get("cr_number", "")
        industry = input_data.get("industry", "technology")
        records = input_data.get("records", [])
        transaction_sample = input_data.get("transaction_sample", [])

        user_msg = (
            f"Run a full compliance check for: {company_name} (Tenant: {tenant_id})\n"
            f"Industry: {industry} | CR: {cr_number or 'not provided'}\n"
            f"Data records: {len(records)} | Transaction samples: {len(transaction_sample)}\n\n"
            "Produce: PDPL score, ZATCA readiness, CR validation, data handling gaps, "
            "and a prioritised remediation plan. Use all governance tools."
        )

        result = await self.run_with_tools(system=_SYSTEM, user_msg=user_msg, context=input_data)

        logger.info(
            "governance_complete",
            company=company_name,
            tenant_id=tenant_id,
            tokens=result.get("usage", {}).get("total_tokens", 0),
        )
        return {
            "status": "complete",
            "agent": self.name,
            "company_name": company_name,
            "tenant_id": tenant_id,
            "compliance_report": result.get("response", ""),
            "completed_at": datetime.now(UTC).isoformat(),
            "usage": result.get("usage", {}),
        }
