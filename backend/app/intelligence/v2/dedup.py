"""
Lead Deduplication — Dealix Lead Intelligence Engine V2
=======================================================
Fuzzy deduplication using rapidfuzz.
Priority: domain > phone > company_name_ar > company_name_en
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from rapidfuzz import fuzz, process

from app.intelligence.v2.i18n import normalize_company_name
from app.intelligence.v2.models import NormalizedLead

logger = logging.getLogger(__name__)

# Fuzzy match threshold for company names (0-100)
FUZZY_THRESHOLD = 88


def _exact_dedup(leads: List[NormalizedLead]) -> List[NormalizedLead]:
    """
    First pass: exact dedup by dedup_key (domain > phone > name).
    Merges provenance from duplicates.
    """
    seen: Dict[str, NormalizedLead] = {}

    for lead in leads:
        key = lead.dedup_key
        if not key:
            # Generate one on the fly
            from app.intelligence.v2.normalizer import make_dedup_key
            lead.dedup_key = make_dedup_key(lead)
            key = lead.dedup_key

        if key in seen:
            # Merge: keep existing but add provenance and missing fields
            existing = seen[key]
            for prov in lead.provenances:
                if prov not in existing.provenances:
                    existing.provenances.append(prov)
            existing.raw_lead_ids.extend(lead.raw_lead_ids)

            # Fill missing fields from duplicate
            if not existing.phone_e164 and lead.phone_e164:
                existing.phone_e164 = lead.phone_e164
            if not existing.email and lead.email:
                existing.email = lead.email
                existing.email_mx_valid = lead.email_mx_valid
            if not existing.website and lead.website:
                existing.website = lead.website
            if not existing.company_name_ar and lead.company_name_ar:
                existing.company_name_ar = lead.company_name_ar
            if not existing.linkedin_url and lead.linkedin_url:
                existing.linkedin_url = lead.linkedin_url
            if not existing.is_hiring and lead.is_hiring:
                existing.is_hiring = True
                existing.hiring_roles.extend(
                    r for r in lead.hiring_roles if r not in existing.hiring_roles
                )
        else:
            seen[key] = lead

    return list(seen.values())


def _fuzzy_dedup(leads: List[NormalizedLead]) -> List[NormalizedLead]:
    """
    Second pass: fuzzy company name dedup.
    Groups leads where company names are very similar (≥ FUZZY_THRESHOLD).
    Keeps the lead with the most data (longest name + most fields filled).
    """
    if len(leads) <= 1:
        return leads

    # Normalize names for comparison
    def _norm_en(lead: NormalizedLead) -> str:
        return normalize_company_name(lead.company_name, lang="en")

    def _norm_ar(lead: NormalizedLead) -> str:
        return normalize_company_name(lead.company_name_ar or "", lang="ar")

    # Build comparison list
    normalized_names_en = [_norm_en(l) for l in leads]

    merged_indices: set[int] = set()
    result: List[NormalizedLead] = []

    for i, lead in enumerate(leads):
        if i in merged_indices:
            continue

        duplicates = [i]
        name_en = normalized_names_en[i]
        name_ar = _norm_ar(lead)

        for j in range(i + 1, len(leads)):
            if j in merged_indices:
                continue

            other = leads[j]
            other_name_en = normalized_names_en[j]
            other_name_ar = _norm_ar(other)

            # Check English name similarity
            score_en = fuzz.token_sort_ratio(name_en, other_name_en)

            # Check Arabic name similarity (if both have AR names)
            score_ar = 0
            if name_ar and other_name_ar:
                score_ar = fuzz.token_sort_ratio(name_ar, other_name_ar)

            if score_en >= FUZZY_THRESHOLD or score_ar >= FUZZY_THRESHOLD:
                duplicates.append(j)
                merged_indices.add(j)

        if len(duplicates) == 1:
            result.append(lead)
        else:
            # Merge group: keep the "richest" lead
            group = [leads[k] for k in duplicates]
            primary = _pick_richest(group)

            # Merge all provenances + missing fields
            for other_lead in group:
                if other_lead is primary:
                    continue
                for prov in other_lead.provenances:
                    if prov not in primary.provenances:
                        primary.provenances.append(prov)
                primary.raw_lead_ids.extend(other_lead.raw_lead_ids)
                if not primary.phone_e164 and other_lead.phone_e164:
                    primary.phone_e164 = other_lead.phone_e164
                if not primary.email and other_lead.email:
                    primary.email = other_lead.email
                if not primary.website and other_lead.website:
                    primary.website = other_lead.website
                if not primary.company_name_ar and other_lead.company_name_ar:
                    primary.company_name_ar = other_lead.company_name_ar
                if not primary.linkedin_url and other_lead.linkedin_url:
                    primary.linkedin_url = other_lead.linkedin_url
                if not primary.is_hiring and other_lead.is_hiring:
                    primary.is_hiring = True
                    primary.hiring_roles.extend(
                        r for r in other_lead.hiring_roles if r not in primary.hiring_roles
                    )

            result.append(primary)

    return result


def _pick_richest(leads: List[NormalizedLead]) -> NormalizedLead:
    """Pick the lead with the most filled fields."""

    def _richness(lead: NormalizedLead) -> int:
        score = 0
        if lead.phone_e164:
            score += 10
        if lead.email:
            score += 8
        if lead.website:
            score += 5
        if lead.company_name_ar:
            score += 4
        if lead.linkedin_url:
            score += 3
        if lead.address:
            score += 2
        if lead.is_hiring:
            score += 6
        if lead.industry:
            score += 2
        score += len(lead.provenances)
        return score

    return max(leads, key=_richness)


async def dedup_leads(leads: List[NormalizedLead]) -> List[NormalizedLead]:
    """
    Full deduplication pipeline:
    1. Exact dedup by key (domain/phone/name)
    2. Fuzzy name matching

    Returns deduplicated list sorted by richness desc.
    """
    before = len(leads)

    # Pass 1: Exact
    after_exact = _exact_dedup(leads)
    logger.info(f"[dedup] Exact: {before} → {len(after_exact)}")

    # Pass 2: Fuzzy
    after_fuzzy = _fuzzy_dedup(after_exact)
    logger.info(f"[dedup] Fuzzy: {len(after_exact)} → {len(after_fuzzy)}")

    # Sort by richness (most data first)
    def _richness_score(lead: NormalizedLead) -> int:
        score = 0
        if lead.phone_e164: score += 10
        if lead.email: score += 8
        if lead.website: score += 5
        if lead.company_name_ar: score += 4
        if lead.linkedin_url: score += 3
        if lead.address: score += 2
        if lead.is_hiring: score += 6
        if lead.industry: score += 2
        score += len(lead.provenances)
        return score

    after_fuzzy.sort(key=_richness_score, reverse=True)

    return after_fuzzy
