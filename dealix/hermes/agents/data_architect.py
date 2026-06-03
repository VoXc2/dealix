"""DataArchitectAgent — builds the 1,500 SAR Data Pack."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.base import HermesAgent
from dealix.hermes.tools.data_tools import (
    calculate_tam_sam_som,
    detect_duplicates,
    enrich_company_data,
    generate_data_passport,
    score_data_quality,
)

logger = structlog.get_logger(__name__)

_SYSTEM = """\
You are the Dealix Data Architect Agent — you build the 1,500 SAR Data Pack deliverable.

The Data Pack includes:
1. Data Quality Report — DQ score across all fields.
2. Deduplication Report — identified duplicate records and deduplicated output.
3. Enrichment Report — enriched company profiles with Saudi firmographic data.
4. TAM/SAM/SOM Analysis — addressable market sizing.
5. Data Passport — formal governance and lineage document.

For each component, use the relevant tools, summarise findings, and assemble
the complete data pack report. Flag any data governance risks.
"""


class DataArchitectAgent(HermesAgent):
    """Builds the 1,500 SAR Data Pack — unified data model and quality report."""

    name = "data_architect"
    description = "Builds the 1,500 SAR Data Pack — unified data model and quality report"

    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.register_hermes_tool(
            name="score_data_quality",
            description="Score dataset quality across completeness, consistency, and uniqueness.",
            properties={
                "records": {"type": "array", "items": {"type": "object"}},
                "fields": {"type": "array", "items": {"type": "string"}},
            },
            required=["records", "fields"],
            fn=score_data_quality,
        )
        self.register_hermes_tool(
            name="detect_duplicates",
            description="Identify duplicate records based on key fields.",
            properties={
                "records": {"type": "array", "items": {"type": "object"}},
                "key_fields": {"type": "array", "items": {"type": "string"}},
            },
            required=["records", "key_fields"],
            fn=detect_duplicates,
        )
        self.register_hermes_tool(
            name="enrich_company_data",
            description="Enrich company profile with Saudi firmographic data.",
            properties={
                "company_name": {"type": "string"},
                "cr_number": {"type": "string"},
            },
            required=["company_name"],
            fn=enrich_company_data,
        )
        self.register_hermes_tool(
            name="calculate_tam_sam_som",
            description="Estimate TAM, SAM, and SOM for a Saudi market segment.",
            properties={
                "industry": {"type": "string"},
                "region": {"type": "string"},
                "segment": {"type": "string"},
            },
            required=["industry", "region", "segment"],
            fn=calculate_tam_sam_som,
        )
        self.register_hermes_tool(
            name="generate_data_passport",
            description="Generate a formal data governance passport.",
            properties={
                "tenant_id": {"type": "string"},
            },
            required=["tenant_id"],
            fn=generate_data_passport,
        )

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        tenant_id = input_data.get("tenant_id", "tenant_unknown")
        company_name = input_data.get("company_name", "Client")
        records = input_data.get("records", [])
        industry = input_data.get("industry", "technology")
        region = input_data.get("region", "riyadh")
        segment = input_data.get("segment", "sme")

        user_msg = (
            f"Build the complete Data Pack for: {company_name} (Tenant: {tenant_id})\n"
            f"Industry: {industry} | Region: {region} | Segment: {segment}\n"
            f"Records to process: {len(records)}\n\n"
            "Run DQ scoring, deduplication, enrichment, TAM/SAM/SOM, and data passport. "
            "Assemble a complete data pack report with all five components."
        )

        result = await self.run_with_tools(system=_SYSTEM, user_msg=user_msg, context=input_data)

        logger.info(
            "data_architect_complete",
            tenant_id=tenant_id,
            company=company_name,
            tokens=result.get("usage", {}).get("total_tokens", 0),
        )
        return {
            "status": "complete",
            "agent": self.name,
            "tenant_id": tenant_id,
            "company_name": company_name,
            "data_pack_report": result.get("response", ""),
            "completed_at": datetime.now(UTC).isoformat(),
            "usage": result.get("usage", {}),
        }
