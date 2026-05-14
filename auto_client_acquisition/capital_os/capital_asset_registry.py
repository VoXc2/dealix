"""Capital Asset Registry — Wave 19.

The canonical list of strategic Capital Assets Dealix has built across
Waves 14-19. This registry is the single source of truth for:
  - /api/v1/capital-assets (admin: all assets)
  - /api/v1/capital-assets/public (public: only assets marked public=True)
  - scripts/generate_capital_asset_index.py (writes capital-assets/CAPITAL_ASSET_INDEX.json)
  - scripts/validate_capital_assets.py (schema integrity check)

Add a new entry every time a wave ships a strategic asset. Doctrine guard:
every entry MUST cite real file paths (the validator enforces this).
"""
from __future__ import annotations

from auto_client_acquisition.capital_os.capital_asset import CapitalAsset


CAPITAL_ASSETS: tuple[CapitalAsset, ...] = (
    # ── Trust + Doctrine assets (public-safe) ────────────────────────
    CapitalAsset(
        asset_id="CAP-001",
        name="Dealix Promise API",
        type="trust_asset",
        strategic_role="public doctrine verification surface — any CISO can curl-verify the 11 commitments against the test files that enforce each",
        file_paths=(
            "api/routers/dealix_promise.py",
            "auto_client_acquisition/governance_os/non_negotiables.py",
            "tests/test_dealix_promise.py",
            "landing/promise.html",
        ),
        buyer_relevance=("CISO", "DPO", "regulated buyer", "Big 4 advisory", "VC due diligence"),
        commercial_use=("trust proof", "partner diligence", "investor evidence", "procurement bypass"),
        maturity="live",
        linked_non_negotiables=(
            "no_scraping", "no_cold_whatsapp", "no_linkedin_automation",
            "no_unsourced_claims", "no_guaranteed_outcomes", "no_pii_in_logs",
            "no_sourceless_ai", "no_external_action_without_approval",
            "no_agent_without_identity", "no_project_without_proof_pack",
            "no_project_without_capital_asset",
        ),
        proof_level="test-backed",
        last_reviewed="2026-05-14",
        public=True,
    ),
    CapitalAsset(
        asset_id="CAP-002",
        name="The Dealix Promise (Public Manifesto)",
        type="doctrine_asset",
        strategic_role="canonical bilingual manifesto — the doctrine that becomes the brand",
        file_paths=(
            "docs/THE_DEALIX_PROMISE.md",
            "docs/00_constitution/NON_NEGOTIABLES.md",
        ),
        buyer_relevance=("CISO", "DPO", "regulated buyer", "partner due diligence"),
        commercial_use=("trust proof", "category creation", "standard setting"),
        maturity="live",
        linked_non_negotiables=(
            "no_scraping", "no_cold_whatsapp", "no_linkedin_automation",
            "no_unsourced_claims", "no_guaranteed_outcomes", "no_pii_in_logs",
            "no_sourceless_ai", "no_external_action_without_approval",
            "no_agent_without_identity", "no_project_without_proof_pack",
            "no_project_without_capital_asset",
        ),
        proof_level="doc-backed",
        last_reviewed="2026-05-14",
        public=True,
    ),
    CapitalAsset(
        asset_id="CAP-003",
        name="Governed AI Operations Doctrine (Open Framework)",
        type="doctrine_asset",
        strategic_role="open-source framework — Dealix becomes de-facto GCC standard by publishing the doctrine",
        file_paths=(
            "open-doctrine/README.md",
            "open-doctrine/GOVERNED_AI_OPS_DOCTRINE.md",
            "open-doctrine/11_NON_NEGOTIABLES.md",
            "open-doctrine/CONTROL_MAPPING.md",
            "open-doctrine/LICENSE.md",
        ),
        buyer_relevance=("partner consultancy", "AI ops shop", "regulated buyer", "standards body"),
        commercial_use=("category creation", "partner standardization", "reference implementation positioning"),
        maturity="live",
        linked_non_negotiables=(
            "no_scraping", "no_cold_whatsapp", "no_linkedin_automation",
            "no_unsourced_claims", "no_guaranteed_outcomes", "no_pii_in_logs",
            "no_sourceless_ai", "no_external_action_without_approval",
            "no_agent_without_identity", "no_project_without_proof_pack",
            "no_project_without_capital_asset",
        ),
        proof_level="doc-backed",
        last_reviewed="2026-05-14",
        public=True,
    ),

    # ── Sales + Product assets (public-safe) ─────────────────────────
    CapitalAsset(
        asset_id="CAP-004",
        name="3-Offer Commercial Ladder",
        type="sales_asset",
        strategic_role="2026-Q2 reframe — Free Diagnostic / 4,999 SAR Retainer / 25,000 SAR Sprint",
        file_paths=(
            "auto_client_acquisition/service_catalog/registry.py",
            "api/routers/commercial_map.py",
            "docs/OFFER_LADDER_AND_PRICING.md",
            "docs/COMMERCIAL_WIRING_MAP.md",
            "docs/sales-kit/PRICING_REFRAME_2026Q2.md",
            "landing/pricing.html",
        ),
        buyer_relevance=("Saudi B2B services founder", "Saudi B2B services COO", "CFO"),
        commercial_use=("pricing anchor", "proposal generation", "qualification engine"),
        maturity="live",
        linked_non_negotiables=("no_guaranteed_outcomes", "no_unsourced_claims"),
        proof_level="test-backed",
        last_reviewed="2026-05-14",
        public=True,
    ),
    CapitalAsset(
        asset_id="CAP-005",
        name="Commercial Map API",
        type="sales_asset",
        strategic_role="public commercial wiring map — every offer to landing/endpoint/delivery surface",
        file_paths=(
            "api/routers/commercial_map.py",
            "tests/test_commercial_map.py",
            "docs/COMMERCIAL_WIRING_MAP.md",
        ),
        buyer_relevance=("partner", "procurement", "Big 4 advisory"),
        commercial_use=("partner diligence", "operational transparency"),
        maturity="live",
        linked_non_negotiables=("no_unsourced_claims",),
        proof_level="test-backed",
        last_reviewed="2026-05-14",
        public=True,
    ),

    # ── Proof + Product assets (mixed exposure) ─────────────────────
    CapitalAsset(
        asset_id="CAP-006",
        name="Proof Pack Assembler",
        type="proof_asset",
        strategic_role="14-section signed Proof Pack per closed engagement — non-negotiable #10",
        file_paths=(
            "auto_client_acquisition/proof_os/proof_pack.py",
            "tests/test_proof_pack_required.py",
        ),
        buyer_relevance=("customer", "Big 4 advisory", "regulator"),
        commercial_use=("delivery proof", "case study source", "renewal trigger"),
        maturity="live",
        linked_non_negotiables=("no_project_without_proof_pack", "no_unsourced_claims"),
        proof_level="test-backed",
        last_reviewed="2026-05-14",
        public=False,
    ),
    CapitalAsset(
        asset_id="CAP-007",
        name="Trust Pack PDF Renderer",
        type="trust_asset",
        strategic_role="11-section enterprise trust pack PDF per customer — for CISO/SAMA review",
        file_paths=(
            "auto_client_acquisition/trust_os/trust_pack.py",
        ),
        buyer_relevance=("CISO", "DPO", "regulator", "Big 4 advisory"),
        commercial_use=("enterprise sales unlock", "compliance evidence"),
        maturity="live",
        linked_non_negotiables=("no_unsourced_claims", "no_project_without_proof_pack"),
        proof_level="code-backed",
        last_reviewed="2026-05-14",
        public=False,
    ),
    CapitalAsset(
        asset_id="CAP-008",
        name="Audit Chain + Evidence Control Plane",
        type="trust_asset",
        strategic_role="cryptographic-quality audit trail of every external action + decision",
        file_paths=(
            "auto_client_acquisition/auditability_os/audit_event.py",
            "auto_client_acquisition/evidence_control_plane_os/evidence_graph.py",
        ),
        buyer_relevance=("CISO", "DPO", "regulator", "internal audit"),
        commercial_use=("regulator response", "incident retrospective", "non-negotiable #8 proof"),
        maturity="live",
        linked_non_negotiables=("no_external_action_without_approval",),
        proof_level="code-backed",
        last_reviewed="2026-05-14",
        public=False,
    ),

    # ── Partner + Investor assets (mostly internal) ─────────────────
    CapitalAsset(
        asset_id="CAP-009",
        name="Anchor Partner Outreach Kit",
        type="partner_asset",
        strategic_role="3-archetype bilingual outreach drafts + 60-min agenda + rev-share term sheet",
        file_paths=(
            "docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md",
            "docs/40_partners/PARTNER_COVENANT.md",
            "scripts/seed_anchor_partner_pipeline.py",
        ),
        buyer_relevance=("Big 4 advisory", "SAMA-licensed processor", "Saudi VC"),
        commercial_use=("partner channel activation", "rev-share contract template"),
        maturity="live",
        linked_non_negotiables=("no_cold_whatsapp", "no_external_action_without_approval"),
        proof_level="doc-backed",
        last_reviewed="2026-05-14",
        public=False,
    ),
    CapitalAsset(
        asset_id="CAP-010",
        name="Investor One-Pager + Funding Memo",
        type="investor_asset",
        strategic_role="bilingual single-page investor narrative + funding memo + use-of-funds",
        file_paths=(
            "docs/sales-kit/INVESTOR_ONE_PAGER.md",
            "docs/funding/FUNDING_MEMO.md",
            "docs/funding/USE_OF_FUNDS.md",
            "docs/funding/WHY_NOW_GCC_AI_OPS.md",
        ),
        buyer_relevance=("Sanabil", "STV", "Wa'ed Ventures", "Raed Ventures", "Saudi angel"),
        commercial_use=("pre-seed conversation starter", "advisor recruitment"),
        maturity="draft",
        linked_non_negotiables=("no_guaranteed_outcomes", "no_unsourced_claims"),
        proof_level="doc-backed",
        last_reviewed="2026-05-14",
        public=False,
    ),

    # ── Hiring + Standard assets ────────────────────────────────────
    CapitalAsset(
        asset_id="CAP-011",
        name="First 3 Hires + Hiring Scorecards",
        type="hiring_asset",
        strategic_role="revenue-gated hiring playbook: AI Ops Engineer, Delivery Operator, Partnerships",
        file_paths=(
            "docs/funding/FIRST_3_HIRES.md",
            "docs/funding/HIRING_SCORECARDS.md",
            "docs/funding/HIRING_PLAN.md",
        ),
        buyer_relevance=("founder", "advisor"),
        commercial_use=("hiring gates", "founder discipline"),
        maturity="draft",
        linked_non_negotiables=("no_project_without_capital_asset",),
        proof_level="doc-backed",
        last_reviewed="2026-05-14",
        public=False,
    ),
    CapitalAsset(
        asset_id="CAP-012",
        name="GCC Standardization Pack",
        type="standard_asset",
        strategic_role="Saudi-first commercialization + GCC-ready doctrine positioning",
        file_paths=(
            "docs/gcc-expansion/GCC_EXPANSION_THESIS.md",
            "docs/gcc-expansion/GCC_GOVERNED_AI_OPS_STANDARD.md",
            "docs/gcc-expansion/GCC_COUNTRY_PRIORITY_MAP.md",
            "docs/gcc-expansion/GCC_PARTNER_ARCHETYPES.md",
            "docs/gcc-expansion/GCC_LOCALIZATION_MATRIX.md",
            "auto_client_acquisition/governance_os/gcc_markets.py",
            "api/routers/gcc_market_intel.py",
        ),
        buyer_relevance=("GCC partner", "regional VC", "Big 4 GCC practice"),
        commercial_use=("category positioning", "partner-led expansion narrative"),
        maturity="live",
        linked_non_negotiables=("no_unsourced_claims",),
        proof_level="test-backed",
        last_reviewed="2026-05-14",
        public=True,
    ),

    # ── Revenue Ops asset (Wave 18) ────────────────────────────────
    CapitalAsset(
        asset_id="CAP-013",
        name="First Invoice Unlock Runbook",
        type="revenue_ops_asset",
        strategic_role="8-action cascade when Invoice #1 lands — Capital Asset registration is action 1",
        file_paths=(
            "docs/ops/FIRST_INVOICE_UNLOCK.md",
            "scripts/moyasar_live_cutover.py",
            "scripts/zatca_preflight.py",
        ),
        buyer_relevance=("founder", "advisor"),
        commercial_use=("invoice #1 readiness", "operational discipline"),
        maturity="live",
        linked_non_negotiables=("no_external_action_without_approval", "no_project_without_capital_asset"),
        proof_level="doc-backed",
        last_reviewed="2026-05-14",
        public=False,
    ),

    # ── Product asset (Wave 18) ────────────────────────────────────
    CapitalAsset(
        asset_id="CAP-014",
        name="Founder Command Center",
        type="product_asset",
        strategic_role="single-pane-of-glass: deploy + doctrine + ladder + routine + ARR + capital",
        file_paths=(
            "api/routers/founder_command_center.py",
            "landing/founder-command-center.html",
            "tests/test_founder_command_center.py",
        ),
        buyer_relevance=("founder", "advisor"),
        commercial_use=("founder operational discipline", "advisor demo surface"),
        maturity="live",
        linked_non_negotiables=("no_unsourced_claims",),
        proof_level="test-backed",
        last_reviewed="2026-05-14",
        public=False,
    ),

    # ── Market asset (Wave 19) ─────────────────────────────────────
    CapitalAsset(
        asset_id="CAP-015",
        name="GCC Market Intel Public API",
        type="market_asset",
        strategic_role="public Saudi/UAE/Qatar/Kuwait posture + PDPL-equivalent framework mapping",
        file_paths=(
            "api/routers/gcc_market_intel.py",
            "auto_client_acquisition/governance_os/gcc_markets.py",
            "tests/test_gcc_markets.py",
        ),
        buyer_relevance=("regional partner", "GCC enterprise buyer", "regional VC"),
        commercial_use=("regional credibility", "partner conversation opener"),
        maturity="live",
        linked_non_negotiables=("no_unsourced_claims",),
        proof_level="test-backed",
        last_reviewed="2026-05-14",
        public=True,
    ),
)


def list_capital_assets() -> tuple[CapitalAsset, ...]:
    """All registered Capital Assets in canonical order."""
    return CAPITAL_ASSETS


def list_public_capital_assets() -> tuple[CapitalAsset, ...]:
    """Only assets explicitly marked public=True. Used by /api/v1/capital-assets/public."""
    return tuple(a for a in CAPITAL_ASSETS if a.public)


def get_capital_asset(asset_id: str) -> CapitalAsset | None:
    for a in CAPITAL_ASSETS:
        if a.asset_id == asset_id:
            return a
    return None


def assets_by_type(t: str) -> tuple[CapitalAsset, ...]:
    return tuple(a for a in CAPITAL_ASSETS if a.type == t)


__all__ = [
    "CAPITAL_ASSETS",
    "list_capital_assets",
    "list_public_capital_assets",
    "get_capital_asset",
    "assets_by_type",
]
