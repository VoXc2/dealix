"""dealix.commercial — Commercial chain engine.

Diagnostic → Warm Intro → Pilot Delivery → Proof Pack → Upsell.
All modules enforce constitutional guardrails:
  NO_LIVE_SEND, NO_LIVE_CHARGE, NO_FAKE_PROOF, NO_UNAPPROVED_TESTIMONIAL.
"""

from dealix.commercial.buyer_outputs import (
    ApprovedAction,
    BaselineMetric,
    BuyerEvidenceSnapshot,
    BuyerOutputsBundle,
    BuyerOutputsEngine,
    DecisionCandidate,
    DeliveryEvidence,
    EvidenceItem,
    HypothesizedLeak,
    Intervention,
    ObservedLeak,
    OutcomeEvent,
    OwnerGap,
    PaymentEvidence,
    ProcessObservation,
    RiskInput,
)
from dealix.commercial.case_study_generator import (
    CaseStudyDocument,
    CaseStudyGenerator,
    CaseStudyRequest,
)
from dealix.commercial.company_brain_sprint import (
    BrainSource,
    CompanyBrainSprintAssessment,
    CompanyBrainSprintPlanner,
    CompanyBrainSprintRequest,
    WorkflowCandidate,
)
from dealix.commercial.diagnostic_engine import (
    DiagnosticEngine,
    DiagnosticReport,
    DiagnosticRequest,
)
from dealix.commercial.pilot_delivery import PilotDeliveryKit, PilotPlan, PilotStartRequest
from dealix.commercial.portfolio_router import (
    DemandSignal,
    EntryPackage,
    PackageRouteDecision,
    PortfolioPackageRouter,
)
from dealix.commercial.proof_builder import ProofBuilder, ProofBuildRequest, ProofPackDocument
from dealix.commercial.upsell_engine import UpsellCheckResult, UpsellEngine
from dealix.commercial.warm_intro_generator import (
    OutreachDraftBundle,
    WarmIntroGenerator,
    WarmIntroRequest,
)

# Economic Cell Model & Registry
from dealix.commercial.economic_cell import (
    Buyer,
    BuyerGroup,
    CellTemplate,
    DEFAULT_TEMPLATES,
    Distribution,
    DistributionRail,
    EconomicCell,
    Economics,
    Evidence,
    EvidenceLevel,
    Execution,
    Geography,
    Identity,
    KillTrigger,
    LifecycleState,
    Market,
    Monetization,
    MonetizationRail,
    Offer,
    OrganizationSize,
    OrganizationType,
    Portfolio,
    Problem,
    ProblemClass,
    Procurement,
    ProcurementRail,
    PromotionGate,
    Proof,
    Risk,
    Sector,
    UNKNOWN,
    Value,
)
from dealix.commercial.economic_cell_registry import (
    EconomicCellRegistry,
    get_default_registry,
    reset_registry_for_tests,
)
from dealix.commercial.economic_dispatcher import (
    BatchDispatcher,
    ConfidenceLevel,
    DispatchDecision,
    EconomicDispatcher,
    EvidenceClass,
    ScoringBreakdown,
    ScoringInput,
)
from dealix.commercial.portfolio_state_machine import (
    KillGateEvaluator,
    PortfolioStateMachine,
    PromotionGateEvaluator,
    StateTransition,
    TransitionReason,
    ValidationExperiment,
)
from dealix.commercial.deep_wip_enforcer import (
    DEEP_WIP_MAX,
    DeepWipEnforcer,
    DeepWipPolicy,
    PresidentWipController,
    WipSlot,
    get_enforcer,
    reset_enforcer_for_tests,
)
from dealix.commercial.president_command import (
    PresidentCommand,
    PresidentCommandOutput,
    Top3Selection,
)
from dealix.commercial.agent_work_packets import (
    AgentPacketBuilder,
    AgentRole,
    AuthorityLevel,
    PacketStatus,
    PacketTracker,
    WorkPacket,
)
from dealix.commercial.business_telemetry import (
    AuthorizationLevel,
    BusinessEventType,
    BusinessTelemetry,
    EconomicReceipt,
    TelemetryEmitter,
    get_emitter,
    get_telemetry,
    reset_telemetry_for_tests,
)

__all__ = [
    # Original commercial chain
    "BrainSource",
    "CompanyBrainSprintAssessment",
    "CompanyBrainSprintPlanner",
    "CompanyBrainSprintRequest",
    "DemandSignal",
    "EntryPackage",
    "PackageRouteDecision",
    "PortfolioPackageRouter",
    "WorkflowCandidate",
    "CaseStudyDocument",
    "CaseStudyGenerator",
    "CaseStudyRequest",
    "ApprovedAction",
    "BaselineMetric",
    "BuyerEvidenceSnapshot",
    "BuyerOutputsBundle",
    "BuyerOutputsEngine",
    "DecisionCandidate",
    "DeliveryEvidence",
    "EvidenceItem",
    "HypothesizedLeak",
    "Intervention",
    "ObservedLeak",
    "OutcomeEvent",
    "OwnerGap",
    "PaymentEvidence",
    "ProcessObservation",
    "RiskInput",
    "DiagnosticEngine",
    "DiagnosticReport",
    "DiagnosticRequest",
    "OutreachDraftBundle",
    "PilotDeliveryKit",
    "PilotPlan",
    "PilotStartRequest",
    "ProofBuildRequest",
    "ProofBuilder",
    "ProofPackDocument",
    "UpsellCheckResult",
    "UpsellEngine",
    "WarmIntroGenerator",
    "WarmIntroRequest",
    # Economic Cell Model
    "Buyer",
    "BuyerGroup",
    "CellTemplate",
    "DEFAULT_TEMPLATES",
    "Distribution",
    "DistributionRail",
    "EconomicCell",
    "Economics",
    "Evidence",
    "EvidenceLevel",
    "Execution",
    "Geography",
    "Identity",
    "KillTrigger",
    "LifecycleState",
    "Market",
    "Monetization",
    "MonetizationRail",
    "Offer",
    "OrganizationSize",
    "OrganizationType",
    "Portfolio",
    "Problem",
    "ProblemClass",
    "Procurement",
    "ProcurementRail",
    "PromotionGate",
    "Proof",
    "Risk",
    "Sector",
    "UNKNOWN",
    "Value",
    # Registry
    "EconomicCellRegistry",
    "get_default_registry",
    "reset_registry_for_tests",
    # Dispatcher
    "BatchDispatcher",
    "ConfidenceLevel",
    "DispatchDecision",
    "EconomicDispatcher",
    "EvidenceClass",
    "ScoringBreakdown",
    "ScoringInput",
    # State Machine
    "KillGateEvaluator",
    "PortfolioStateMachine",
    "PromotionGateEvaluator",
    "StateTransition",
    "TransitionReason",
    "ValidationExperiment",
    # Deep WIP
    "DEEP_WIP_MAX",
    "DeepWipEnforcer",
    "DeepWipPolicy",
    "PresidentWipController",
    "WipSlot",
    "get_enforcer",
    "reset_enforcer_for_tests",
    # President Command
    "PresidentCommand",
    "PresidentCommandOutput",
    "Top3Selection",
    # Agent Packets
    "AgentPacketBuilder",
    "AgentRole",
    "AuthorityLevel",
    "PacketStatus",
    "PacketTracker",
    "WorkPacket",
    # Telemetry
    "AuthorizationLevel",
    "BusinessEventType",
    "BusinessTelemetry",
    "EconomicReceipt",
    "TelemetryEmitter",
    "get_emitter",
    "get_telemetry",
    "reset_telemetry_for_tests",
]
# Financial OS — cash truth, unit economics, forecast
from dealix.commercial.financial_os import (
    CashForecast,
    FinancialCommandView,
    FinancialOS,
    FinancialRecord,
    FinancialState,
    OfferEconomics,
)
# Saudi Market Radar — official watchers
from dealix.commercial.saudi_market_radar import (
    RegulatorySignal,
    SaudiMarketRadar,
    SignalSource,
)
# Phase A — Distribution & Relationship
from dealix.commercial.channel_registry import Channel, ChannelRegistry, ChannelStatus, ChannelType
from dealix.commercial.consent_registry import ConsentRecord, ConsentRegistry, ConsentState
from dealix.commercial.relationship_graph import RelationshipGraph, RelationshipRecord, RelationshipStage

# Phase B — Website Intelligence
from dealix.commercial.ai_concierge import AIConcierge, ConciergeRequest, ConciergeResponse
from dealix.commercial.diagnostic_self_serve import DiagnosticInput, DiagnosticOutput, SelfServeDiagnostic

# Phase C — Income, Open Source, Invariants, Scheduler
from dealix.commercial.low_touch_income import IncomeRail, LowTouchCandidate, LowTouchRegistry
from dealix.commercial.open_source_registry import OpenSourceRegistry, OpenSourceStatus, OpenSourceTool
from dealix.commercial.company_invariants import INVARIANTS, CompanyInvariant, get_invariants
from dealix.commercial.scheduler_inventory import TimerEntry, classify_timers, inventory_timers
# Probability-driven execution & compounding
from dealix.commercial.probability_engine import BetState, EconomicBet, ProbBand, ProbabilityVector
from dealix.commercial.portfolio_bets import PortfolioBets

# Proof → Asset & Delivery
from dealix.commercial.delivery_kit import DeliveryFactory, DeliveryKit, DeliveryStage
from dealix.commercial.proof_asset_factory import AssetType, ProofAsset, ProofAssetFactory
# Universal Diagnostic Factory — 50 families, D0-D5, overlays
from dealix.commercial.universal_diagnostic_factory import DiagnosticDepth, DiagnosticFamily, FAMILIES, UniversalDiagnosticFactory
# Sector Companies & Omnichannel
from dealix.commercial.sector_company_factory import SECTOR_INTEL, SectorCompany, SectorCompanyFactory
from dealix.commercial.omnichannel_orchestrator import ChannelId, OmnichannelMessage, OmnichannelOrchestrator
# Arm Registry — 44+ capability arms, all activated
from dealix.commercial.arm_registry import ALL_ARMS, ArmHealth, CapabilityArm, get_active_arms
# Low-touch products — automated delivery
from dealix.commercial.low_touch_products.diagnostic_product import DiagnosticProductEngine
# Content Factory — proof atomization
from dealix.commercial.content_factory import ContentAtom, ContentFactory
# Partner & Marketplace — expanded launch
from dealix.commercial.partner_economy import PartnerCandidate, PartnerEconomy, PartnerMotion, PartnerType
from dealix.commercial.marketplace_strategy import MarketplaceCandidate, MarketplaceStrategy, MarketplaceType
# SaaS Master — comprehensive SaaS, market control
from dealix.commercial.saas_foundation import BillingRecord, SaaSControlPlane, SaaSEntitlement, Tenant, TenantTier
# SaaS Onboarding — expanded launch
from dealix.commercial.saas_onboarding import OnboardingSession, OnboardingStep, SaaSOnboardingEngine
# Launch Readiness — expanded launch verification
from dealix.commercial.launch_readiness import LaunchReadiness, check as check_launch_readiness
# Expanded Launch — 20 sectors × 44 arms × SaaS comprehensive
from dealix.commercial.expanded_launch_executor import ExpandedLaunchExecutor
# Comprehensive Launch — all sectors, all arms, expanded
from dealix.commercial.comprehensive_launch import ComprehensiveLaunch
# Remaining Plans — comprehensive from all aspects
from dealix.commercial.remaining_plans_executor import RemainingPlansExecutor
# Final Expanded Launch — best thought, all aspects
from dealix.commercial.final_expanded_launch import FinalExpandedLaunch
# Legacy Adapters — best-form integration, One Company
from dealix.commercial.legacy_adapters import LEGACY_PROOF_AVAILABLE, get_proof_ledger
# Next Expansion — continuous, never stops
from dealix.commercial.next_expansion import NextExpansion
# AI Sector Expansion — double coverage via AI
from dealix.commercial.ai_sector_expansion import AI_GENERATED_SECTORS, AISectorExpansion
# Best Free Diagnostic — best in market, all agents operate
from dealix.commercial.best_free_diagnostic import BEST_OFFERS, BestFreeDiagnosticEngine, BestFreeDiagnosticOffer
# Best Offers — best in market, all sectors
from dealix.commercial.best_offers_catalog import BestOfferCatalog
# Realistic Money-Now — real relationships, realistic value
from dealix.commercial.realistic_money_now import RealisticMoneyNowCandidate, RealisticMoneyNowEngine
# Master 15 Plans — best, smart, comprehensive, future, real, launch, money
from dealix.commercial.master_15_plans import PLANS, Master15Executor, MasterPlan
# Execute 15 Plans — comprehensive, no stop
from dealix.commercial.execute_15_plans import Execute15Plans
# Master 20 Plans — best, smart, comprehensive, all aspects, merged 15 + 5
from dealix.commercial.master_20_plans import PLANS_20, Master20Executor
# Slack & Telegram L5 — governed
from dealix.commercial.slack_telegram_l5 import SlackL5Packet, TelegramL5Packet, action_hash
# Sales Automation via Hermes + OpenClaw — real, whole market
from dealix.commercial.sales_automation_hermes_openclaw import SalesAutomationEngine, SalesAutomationTask
# Communication & Social — self, complete, site ready, all platforms
from dealix.commercial.communication_negotiation import CommunicationNegotiationEngine, CommunicationTask, NegotiationState
from dealix.commercial.social_automation import ALL_PLATFORMS, SocialPlatform, get_all_platforms
# Hermes Sector Diagnostic — in every sector Hermes can diagnose and convince
from dealix.commercial.hermes_sector_diagnostic import HermesSectorDiagnostic
# Large-Scale Sector Execution — many people per sector, all channels, no ban, pain targeting
from dealix.commercial.large_scale_sector_execution import LargeScaleExecution, LargeScaleSectorExecutor
# Delix Service Preparation — for each person ready, daily proposal per company, complete profile per sector
from dealix.commercial.delix_service_preparation import CompanyProfile, DelixServicePreparation
# Saudi Sector Targeting — simple picture applied fully to all Saudi sectors
from dealix.commercial.saudi_sector_targeting import SaudiSectorTarget, SaudiSectorTargetingEngine

