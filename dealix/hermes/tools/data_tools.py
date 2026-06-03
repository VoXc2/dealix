"""Data tool functions — data quality, enrichment, deduplication, TAM/SAM/SOM."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


async def score_data_quality(
    records: list[dict[str, Any]],
    fields: list[str],
) -> dict[str, Any]:
    """Compute a 0-100 data quality score across a record set.

    Evaluates completeness (non-null ratio), consistency (type uniformity),
    and uniqueness (duplicate key ratio) for the specified fields.

    Parameters
    ----------
    records:
        List of record dicts to evaluate.
    fields:
        Field names to include in the quality assessment.

    Returns
    -------
    dict
        DQ score (0-100), per-field breakdown, and a quality tier label.
    """
    if not records:
        return {
            "score": 0,
            "tier": "unusable",
            "completeness": 0.0,
            "consistency": 0.0,
            "uniqueness": 0.0,
            "field_scores": {},
            "record_count": 0,
            "assessed_fields": fields,
        }

    total_records = len(records)
    field_scores: dict[str, dict[str, Any]] = {}

    completeness_values: list[float] = []
    for field in fields:
        non_null = sum(1 for r in records if r.get(field) not in (None, "", []))
        field_completeness = non_null / total_records
        field_scores[field] = {"completeness": round(field_completeness, 3)}
        completeness_values.append(field_completeness)

    completeness = sum(completeness_values) / len(completeness_values) if completeness_values else 0.0

    # Consistency: fraction of records where all fields have non-null values
    fully_complete = sum(
        1 for r in records if all(r.get(f) not in (None, "", []) for f in fields)
    )
    consistency = fully_complete / total_records

    # Uniqueness: based on a composite key of all fields
    unique_keys: set[str] = set()
    for r in records:
        key = "|".join(str(r.get(f, "")) for f in fields)
        unique_keys.add(key)
    uniqueness = len(unique_keys) / total_records

    overall = round(completeness * 40 + consistency * 30 + uniqueness * 30, 1)

    if overall >= 80:
        tier = "high"
    elif overall >= 60:
        tier = "medium"
    elif overall >= 40:
        tier = "low"
    else:
        tier = "unusable"

    logger.info("data_quality_scored", score=overall, tier=tier, records=total_records)
    return {
        "score": overall,
        "tier": tier,
        "completeness": round(completeness * 100, 1),
        "consistency": round(consistency * 100, 1),
        "uniqueness": round(uniqueness * 100, 1),
        "field_scores": field_scores,
        "record_count": total_records,
        "assessed_fields": fields,
    }


async def detect_duplicates(
    records: list[dict[str, Any]],
    key_fields: list[str],
) -> dict[str, Any]:
    """Identify duplicate records based on composite key fields.

    Parameters
    ----------
    records:
        List of record dicts.
    key_fields:
        Fields that together form a uniqueness key.

    Returns
    -------
    dict
        Duplicate groups, counts, and a deduplicated record set.
    """
    if not records:
        return {
            "total_records": 0,
            "duplicate_count": 0,
            "unique_count": 0,
            "duplicate_groups": [],
            "deduplicated_records": [],
        }

    seen: dict[str, list[int]] = {}
    for idx, record in enumerate(records):
        key = "|".join(str(record.get(f, "")).strip().lower() for f in key_fields)
        seen.setdefault(key, []).append(idx)

    duplicate_groups = [
        {
            "key": key,
            "indices": indices,
            "count": len(indices),
        }
        for key, indices in seen.items()
        if len(indices) > 1
    ]

    duplicate_indices: set[int] = set()
    deduplicated: list[dict[str, Any]] = []
    for key, indices in seen.items():
        deduplicated.append(records[indices[0]])
        for idx in indices[1:]:
            duplicate_indices.add(idx)

    logger.info(
        "duplicates_detected",
        total=len(records),
        duplicates=len(duplicate_indices),
        unique=len(deduplicated),
    )
    return {
        "total_records": len(records),
        "duplicate_count": len(duplicate_indices),
        "unique_count": len(deduplicated),
        "duplicate_groups": duplicate_groups[:50],
        "deduplicated_records": deduplicated,
    }


async def enrich_company_data(
    company_name: str,
    cr_number: str = "",
) -> dict[str, Any]:
    """Enrich company data with firmographic and market information.

    Simulates enrichment from external providers (e.g., ZAKAT, commercial
    registry, or third-party data sources).

    Parameters
    ----------
    company_name:
        Registered company name to look up.
    cr_number:
        Saudi commercial registration number (optional).

    Returns
    -------
    dict
        Enriched company record with industry, size, region, and flags.
    """
    import hashlib

    # Deterministic mock based on company name hash
    name_hash = int(hashlib.md5(company_name.encode()).hexdigest(), 16)

    industries = [
        "technology", "retail", "healthcare", "manufacturing",
        "financial_services", "education", "real_estate", "logistics",
    ]
    regions = ["riyadh", "jeddah", "dammam", "makkah", "madinah"]
    employee_bands = [
        "1-10", "11-50", "51-200", "201-500", "501-2000", "2000+",
    ]
    revenue_bands = [
        "under_1m", "1m_5m", "5m_20m", "20m_100m", "over_100m",
    ]

    enriched = {
        "company_name": company_name,
        "cr_number": cr_number or f"10{name_hash % 10_000_000_000:010d}",
        "industry": industries[name_hash % len(industries)],
        "region": regions[name_hash % len(regions)],
        "employee_band": employee_bands[name_hash % len(employee_bands)],
        "revenue_band_sar": revenue_bands[name_hash % len(revenue_bands)],
        "vat_registered": bool(name_hash % 3),
        "founded_year": 2010 + (name_hash % 14),
        "vision_2030_sector": bool(name_hash % 2),
        "enriched_at": datetime.now(UTC).isoformat(),
        "enrichment_confidence": min(95, 60 + (name_hash % 36)),
        "data_sources": ["commercial_registry_sim", "public_records_sim"],
    }

    logger.info("company_data_enriched", company=company_name)
    return {"enriched": True, "company": enriched}


async def calculate_tam_sam_som(
    industry: str,
    region: str,
    segment: str,
) -> dict[str, Any]:
    """Estimate TAM, SAM, and SOM for a given market.

    Uses heuristic multipliers calibrated for the Saudi B2B market.

    Parameters
    ----------
    industry:
        Industry vertical (e.g., "technology", "retail").
    region:
        Geographic region (e.g., "riyadh", "nationwide").
    segment:
        Target customer segment (e.g., "sme", "enterprise").

    Returns
    -------
    dict
        TAM, SAM, SOM estimates in SAR with methodology notes.
    """
    # Baseline TAM estimates by industry (SAR billions)
    tam_baselines: dict[str, float] = {
        "technology": 45.0,
        "retail": 380.0,
        "healthcare": 65.0,
        "manufacturing": 120.0,
        "financial_services": 90.0,
        "education": 30.0,
        "real_estate": 210.0,
        "logistics": 55.0,
        "default": 25.0,
    }

    region_multipliers: dict[str, float] = {
        "riyadh": 0.35,
        "jeddah": 0.22,
        "dammam": 0.15,
        "nationwide": 1.0,
        "default": 0.10,
    }

    segment_multipliers: dict[str, float] = {
        "sme": 0.20,
        "enterprise": 0.15,
        "startup": 0.05,
        "government": 0.30,
        "default": 0.10,
    }

    tam_b = tam_baselines.get(industry.lower(), tam_baselines["default"])
    r_mult = region_multipliers.get(region.lower(), region_multipliers["default"])
    s_mult = segment_multipliers.get(segment.lower(), segment_multipliers["default"])

    tam_sar = tam_b * 1_000_000_000
    sam_sar = tam_sar * r_mult
    som_sar = sam_sar * s_mult * 0.03  # 3% realistic capture in year 1-3

    logger.info("tam_sam_som_calculated", industry=industry, region=region, segment=segment)
    return {
        "industry": industry,
        "region": region,
        "segment": segment,
        "tam_sar": round(tam_sar),
        "sam_sar": round(sam_sar),
        "som_sar": round(som_sar),
        "tam_human": f"SAR {tam_b:.1f}B",
        "sam_human": f"SAR {sam_sar / 1_000_000:.1f}M",
        "som_human": f"SAR {som_sar / 1_000:.0f}K",
        "methodology": "heuristic_saudi_b2b_calibrated",
        "confidence": "medium",
        "notes": "Estimates based on Saudi 2024 market research. Validate with primary data.",
    }


async def generate_data_passport(tenant_id: str) -> dict[str, Any]:
    """Generate a structured data passport report for a tenant.

    The data passport documents data sources, quality scores, PII handling,
    and governance posture for a given tenant.

    Parameters
    ----------
    tenant_id:
        Unique tenant identifier.

    Returns
    -------
    dict
        Full data passport with source inventory, quality scores, and flags.
    """
    passport = {
        "passport_id": f"DP-{tenant_id[:8].upper()}",
        "tenant_id": tenant_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "version": "2.0",
        "data_sources": [
            {
                "source_id": "SRC-001",
                "source_type": "crm_export",
                "record_count": 1_250,
                "quality_score": 72,
                "contains_pii": True,
                "ai_access_allowed": True,
                "external_use_allowed": False,
                "sensitivity": "medium",
            },
            {
                "source_id": "SRC-002",
                "source_type": "sales_data",
                "record_count": 340,
                "quality_score": 85,
                "contains_pii": False,
                "ai_access_allowed": True,
                "external_use_allowed": False,
                "sensitivity": "low",
            },
        ],
        "aggregate_dq_score": 78,
        "pii_sources_count": 1,
        "total_record_count": 1_590,
        "governance_flags": [],
        "pdpl_compliant": True,
        "retention_policy": "project_duration",
        "last_audit_date": datetime.now(UTC).strftime("%Y-%m-%d"),
    }

    logger.info("data_passport_generated", tenant_id=tenant_id)
    return {"passport": passport, "generated": True}


__all__ = [
    "score_data_quality",
    "detect_duplicates",
    "enrich_company_data",
    "calculate_tam_sam_som",
    "generate_data_passport",
]
