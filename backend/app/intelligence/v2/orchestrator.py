"""
Discovery Orchestrator — Dealix Lead Intelligence Engine V2
===========================================================
Runs search plans in parallel via asyncio.gather.
Collects RawLeads and streams them via async generator.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import AsyncGenerator, Dict, List, Optional, Type

from app.intelligence.v2.models import (
    DiscoveryJob,
    DiscoveryQuery,
    JobStatus,
    RawLead,
    SearchPlan,
    ScoredLead,
)
from app.intelligence.v2.planner import plan_queries
from app.intelligence.v2.sources.base import BaseSource

# Import all source adapters
from app.intelligence.v2.sources.search.google_custom import GoogleCustomSearchSource
from app.intelligence.v2.sources.search.duckduckgo import DuckDuckGoSource
from app.intelligence.v2.sources.search.brave import BraveSearchSource
from app.intelligence.v2.sources.maps.google_places import GooglePlacesSource
from app.intelligence.v2.sources.maps.osm_nominatim import OSMNominatimSource
from app.intelligence.v2.sources.social.linkedin_public import LinkedInPublicSource
from app.intelligence.v2.sources.registries.sa_mc_gov import SaudiMCGovSource
from app.intelligence.v2.sources.directories.bayt import BaytJobsSource

logger = logging.getLogger(__name__)

# Registry: source_name → source class
SOURCE_REGISTRY: Dict[str, Type[BaseSource]] = {
    "google_custom_search": GoogleCustomSearchSource,
    "duckduckgo": DuckDuckGoSource,
    "brave_search": BraveSearchSource,
    "google_places": GooglePlacesSource,
    "osm_nominatim": OSMNominatimSource,
    "linkedin_public": LinkedInPublicSource,
    "sa_mc_gov": SaudiMCGovSource,
    "bayt_jobs": BaytJobsSource,
}


async def _run_single_plan(
    source: BaseSource,
    query: DiscoveryQuery,
    plan: SearchPlan,
) -> List[RawLead]:
    """Execute a single search plan and return raw leads."""
    try:
        logger.info(
            f"[orchestrator] Running {plan.source_name}: {plan.query_string[:60]}"
        )
        leads = await source.discover(query, plan)
        logger.info(
            f"[orchestrator] {plan.source_name} returned {len(leads)} leads"
        )
        return leads
    except Exception as e:
        logger.error(f"[orchestrator] {plan.source_name} failed: {e}")
        return []


async def discover_raw(
    query: DiscoveryQuery,
    job: Optional[DiscoveryJob] = None,
) -> AsyncGenerator[RawLead, None]:
    """
    Core discovery generator.
    Plans queries via LLM, runs sources in parallel, yields RawLeads as they arrive.
    """
    # 1. Generate search plans
    logger.info(f"[orchestrator] Planning queries for job {query.id}")
    plans = await plan_queries(query)

    if job:
        job.sources_total = len(plans)

    # 2. Instantiate sources
    source_instances: Dict[str, BaseSource] = {}
    for plan in plans:
        source_name = plan.source_name
        if source_name not in source_instances:
            cls = SOURCE_REGISTRY.get(source_name)
            if cls:
                source_instances[source_name] = cls()
            else:
                logger.warning(f"[orchestrator] Unknown source: {source_name}")

    # 3. Run plans in batches (group by priority)
    priority_groups: Dict[int, List[SearchPlan]] = {}
    for plan in plans:
        priority_groups.setdefault(plan.priority, []).append(plan)

    all_raw_leads: List[RawLead] = []
    completed_sources: set[str] = set()

    for priority in sorted(priority_groups.keys()):
        group = priority_groups[priority]

        # Run this priority group in parallel
        tasks = []
        task_plans = []
        for plan in group:
            source = source_instances.get(plan.source_name)
            if source:
                tasks.append(_run_single_plan(source, query, plan))
                task_plans.append(plan)

        if not tasks:
            continue

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for plan, result in zip(task_plans, results):
            if isinstance(result, Exception):
                logger.error(f"[orchestrator] {plan.source_name} raised: {result}")
                continue

            completed_sources.add(plan.source_name)
            if job:
                if plan.source_name not in job.sources_completed:
                    job.sources_completed.append(plan.source_name)
                job.progress = min(
                    99.0,
                    len(job.sources_completed) / max(job.sources_total, 1) * 100
                )
                job.leads_found += len(result)

            for lead in result:
                all_raw_leads.append(lead)
                yield lead

        # Respect limit
        if len(all_raw_leads) >= query.limit * 3:  # 3x buffer for dedup
            logger.info(f"[orchestrator] Reached lead buffer limit ({len(all_raw_leads)})")
            break

    # Close source HTTP clients
    for source in source_instances.values():
        try:
            await source.close()
        except Exception:
            pass


async def run_full_pipeline(
    query: DiscoveryQuery,
    job: DiscoveryJob,
) -> List[ScoredLead]:
    """
    Run the full discovery pipeline:
    discover → normalize → dedup → enrich → score

    Updates job status throughout.
    """
    from app.intelligence.v2.normalizer import normalize_leads
    from app.intelligence.v2.dedup import dedup_leads
    from app.intelligence.v2.enrichment import enrich_leads
    from app.intelligence.v2.scoring import score_leads

    job.status = JobStatus.RUNNING
    job.started_at = datetime.utcnow()

    try:
        # 1. Discover raw leads
        logger.info(f"[orchestrator] Starting discovery for job {job.id}")
        raw_leads: List[RawLead] = []
        async for lead in discover_raw(query, job):
            raw_leads.append(lead)
            if len(raw_leads) >= query.limit * 5:
                break

        logger.info(f"[orchestrator] Collected {len(raw_leads)} raw leads")

        # 2. Normalize
        job.progress = 40.0
        normalized = await normalize_leads(raw_leads)
        logger.info(f"[orchestrator] Normalized to {len(normalized)} leads")

        # 3. Dedup
        job.progress = 50.0
        deduped = await dedup_leads(normalized)
        logger.info(f"[orchestrator] After dedup: {len(deduped)} leads")

        # 4. Enrich (up to limit)
        job.progress = 60.0
        to_enrich = deduped[:query.limit]
        enriched = await enrich_leads(to_enrich)
        logger.info(f"[orchestrator] Enriched {len(enriched)} leads")

        # 5. Score
        job.progress = 80.0
        scored = await score_leads(enriched, query)
        logger.info(f"[orchestrator] Scored {len(scored)} leads")

        # Sort by score desc
        scored.sort(key=lambda x: x.total_score, reverse=True)

        # Update job
        job.scored_leads = scored
        job.leads_scored = len(scored)
        job.status = JobStatus.COMPLETED
        job.progress = 100.0
        job.completed_at = datetime.utcnow()

        logger.info(f"[orchestrator] Job {job.id} complete — {len(scored)} leads ready")
        return scored

    except Exception as e:
        logger.error(f"[orchestrator] Job {job.id} failed: {e}", exc_info=True)
        job.status = JobStatus.FAILED
        job.error = str(e)
        job.completed_at = datetime.utcnow()
        return []
