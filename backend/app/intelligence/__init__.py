"""
Dealix Lead Intelligence Engine
================================
محرك استخبارات الـ Leads — يكتشف ويُثري ويُسجّل عملاء B2B في السعودية.

Quick start::

    from app.intelligence import (
        IntelligenceOrchestrator,
        DiscoveryCriteria,
        Sector,
        Region,
    )

    orchestrator = IntelligenceOrchestrator()  # Uses seed data without API keys

    criteria = DiscoveryCriteria(
        sectors=[Sector.ECOMMERCE, Sector.B2B_SAAS],
        regions=[Region.RIYADH],
        min_employees=50,
        limit=10,
    )

    import asyncio
    leads = asyncio.run(orchestrator.run_pipeline(criteria))

    for lead in leads:
        print(f"{lead.company.name}: {lead.dealix_score:.0f}/100 [{lead.priority_tier}]")
"""

from .enrichment import EnrichmentPipeline, EnrichmentResult
from .models import (
    Company,
    Contact,
    DiscoveryCriteria,
    EstablishmentType,
    FundingEvent,
    HiringSignal,
    Lead,
    LeadStatus,
    NewsEvent,
    Region,
    ScoreBreakdown,
    Sector,
    Signal,
    SignalType,
    SocialHandles,
    TenderWin,
)
from .orchestrator import IntelligenceOrchestrator
from .scoring import LeadScorer
from .sources import (
    EtimadSource,
    HiringIntentSource,
    LinkedInSource,
    NewsSource,
    SaudiBusinessRegistrySource,
    TechStackSource,
)

__all__ = [
    # Orchestrator (main entry point)
    "IntelligenceOrchestrator",
    # Pipeline
    "EnrichmentPipeline",
    "EnrichmentResult",
    # Scoring
    "LeadScorer",
    # Models
    "Lead",
    "Company",
    "Contact",
    "Signal",
    "ScoreBreakdown",
    "FundingEvent",
    "HiringSignal",
    "TenderWin",
    "NewsEvent",
    "SocialHandles",
    "DiscoveryCriteria",
    # Enums
    "Sector",
    "Region",
    "LeadStatus",
    "SignalType",
    "EstablishmentType",
    # Sources
    "SaudiBusinessRegistrySource",
    "EtimadSource",
    "LinkedInSource",
    "NewsSource",
    "HiringIntentSource",
    "TechStackSource",
]

__version__ = "1.0.0"
__author__ = "Dealix Engineering"
