#!/usr/bin/env python3
"""Generate dealix/transformation/strategic_initiatives_registry.yaml (100 initiatives)."""

from __future__ import annotations

from pathlib import Path

import yaml

# (id, title_en, wave, owner_os, raci_R, deliverable_slug, verification)
_INITIATIVES: list[tuple[int, str, int, str, str, str, str]] = [
    (1, "Unified North Star across layers", 0, "strategy", "CEO", "north_star_manifest.yaml", "verify_global_ai_transformation.py --check-initiatives"),
    (2, "Constitution to Policy-as-Code", 1, "trust", "CTO", "governance_os/constitution_policy_map.yaml", "pytest tests/test_constitution_policy_map.py -q"),
    (3, "API domain ownership reorganization", 2, "platform", "CTO", "docs/architecture/API_DOMAIN_OWNERSHIP.md", "pytest tests/test_api_domain_ownership.py -q"),
    (4, "Product Evidence Review Board weekly", 4, "product", "CEO", "docs/transformation/PRODUCT_EVIDENCE_REVIEW_BOARD_AR.md", "grep PERB weekly_proof"),
    (5, "KPI Registry SSOT", 0, "strategy", "CEO", "dealix/transformation/kpi_registry.yaml", "verify_global_ai_transformation.py"),
    (6, "Revenue attribution per commercial path", 3, "value", "Revenue", "value_os/attribution_paths.yaml", "pytest tests/test_value_attribution.py -q"),
    (7, "Fast Lane vs Governed Lane", 1, "trust", "CTO", "dealix/transformation/lane_policy.yaml", "pytest tests/test_lane_policy.py -q"),
    (8, "Productized offers from capabilities", 3, "gtm", "Revenue", "commercial_os/productized_offers.yaml", "bash scripts/revenue_os_master_verify.sh"),
    (9, "Upsell engine evidence-level gating", 3, "sales", "Revenue", "revenue_os upsell rules", "pytest tests/test_revenue_os_catalog.py -q"),
    (10, "Saudi vertical GTM framework", 3, "gtm", "Revenue", "gtm_os/saudi_vertical_playbook.yaml", "pytest tests/test_saudi_targeting_profile.py -q"),
    (11, "Data Quality Operating System", 5, "data", "Operations", "data_os DQ cadence", "pytest tests/test_data_os_quality.py -q"),
    (12, "Error budget SLO per API domain", 2, "reliability", "CTO", "dealix/transformation/slo_by_domain.yaml", "python3 scripts/reliability_drills_scorecard.py"),
    (13, "Deal Desk operating layer", 3, "sales", "Revenue", "commercial_engagements/deal_desk_os.py", "pytest tests/test_deal_desk_os.py -q"),
    (14, "First 14 days onboarding program", 6, "delivery", "Operations", "adoption_os/first_14_days_playbook.yaml", "pytest tests/test_delivery_os_framework.py -q"),
    (15, "Live risk register linked to execution", 1, "trust", "CEO", "dealix/transformation/risk_register.yaml", "verify_global_ai_transformation.py"),
    (16, "Incident command via security runbook", 1, "reliability", "CTO", "docs/SECURITY_RUNBOOK.md", "verify_global_ai_transformation.py --check-reliability"),
    (17, "Value-based pricing engine", 3, "finance", "Revenue", "value_os/pricing_engine.py", "pytest tests/test_pricing_engine.py -q"),
    (18, "Customer value narrative framework", 6, "delivery", "Operations", "proof pack monthly narrative template", "pytest tests/test_proof_pack.py -q"),
    (19, "Dealix capability map", 4, "product", "CEO", "dealix/transformation/capability_map.yaml", "python3 scripts/generate_capability_map_md.py"),
    (20, "Quarterly strategic bets portfolio", 8, "strategy", "CEO", "strategic_initiatives_registry portfolio_status", "verify_global_ai_transformation.py --check-initiatives"),
    (21, "Proof pack productization for sales", 3, "sales", "Revenue", "commercial proof pack playbook", "bash scripts/revenue_os_master_verify.sh"),
    (22, "Pipeline decay alerts", 3, "sales", "Revenue", "revenue_os pipeline decay signals", "pytest tests/test_revenue_os_catalog.py -q"),
    (23, "Decision postmortem loop", 4, "strategy", "CEO", "docs/transformation/decision_postmortem_template.md", "weekly proof DQI section"),
    (24, "Saudi compliance control plane", 1, "trust", "CTO", "compliance PDPL + contracts", "pytest tests/unit/test_compliance_os.py -q"),
    (25, "Partner strategy execution layer", 3, "gtm", "Revenue", "market_power_os partner gates", "pytest tests/test_market_power_os.py -q"),
    (26, "Executive daily weekly rhythm 2.0", 0, "strategy", "CEO", "docs/transformation/EXECUTIVE_RHYTHM_2_AR.md", "bash scripts/run_executive_weekly_checklist.sh"),
    (27, "Time to first value acceleration", 6, "delivery", "Operations", "adoption_os TTFV checkpoints", "pytest tests/test_adoption_os.py -q"),
    (28, "AI workforce governance unified", 1, "trust", "CTO", "workflow_control_registry AI paths", "pytest tests/test_governance_os_draft_gate.py -q"),
    (29, "Margin expansion OS", 8, "finance", "CEO", "09_unit_economics_governance.md", "verify_global_ai_transformation.py --check unit-economics"),
    (30, "Script lifecycle governance", 2, "platform", "CTO", "scripts/script_inventory.yaml", "verify_global_ai_transformation.py --check-initiatives"),
    (31, "Launch war room protocol", 7, "reliability", "CTO", "docs/ops/LAUNCH_WAR_ROOM_AR.md", "file exists LAUNCH_WAR_ROOM_AR.md"),
    (32, "Strategy to execution traceability", 0, "strategy", "CEO", "strategic_initiatives_registry.yaml", "verify_global_ai_transformation.py --check-initiatives"),
    (33, "Dealix Method Academy", 10, "people_ops", "CEO", "docs/academy/README.md", "verify_global_ai_transformation.py --check-initiatives"),
    (34, "Objection intelligence system", 3, "sales", "Revenue", "commercial_engagements objection templates", "pytest tests/test_deal_desk_os.py -q"),
    (35, "Unified readiness Go No-Go API", 1, "platform", "CTO", "api/routers/unified_readiness.py", "pytest tests/test_unified_readiness.py -q"),
    (36, "Executive knowledge graph", 5, "platform", "CTO", "dealix/execution/executive_knowledge_index.py", "pytest tests/test_executive_knowledge_index.py -q"),
    (37, "BU level scorecards", 4, "finance", "CEO", "kpi_registry BU extensions", "generate_weekly_operating_proof_pack.py"),
    (38, "Enterprise sales motion hardening", 3, "gtm", "Revenue", "docs/strategic/ENTERPRISE_OFFER_POSITIONING_AR.md", "verify_global_ai_transformation.py --check enterprise-package"),
    (39, "Growth critical tech debt program", 2, "platform", "CTO", "docs/transformation/growth_tech_debt_register.yaml", "verify_global_ai_transformation.py --check-initiatives"),
    (40, "Service readiness standardization", 4, "delivery", "Operations", "delivery_os service_readiness", "pytest tests/test_service_readiness_score.py -q"),
    (41, "Decision quality index leadership", 4, "strategy", "CEO", "kpi_registry guardrails DQI", "generate_weekly_operating_proof_pack.py"),
    (42, "Institution mode beyond founder", 10, "people_ops", "CEO", "ownership_matrix institutionalization", "verify_global_ai_transformation.py"),
    (43, "Customer facing API documentation", 2, "product", "CTO", "docs/product/API_SPEC.md", "file exists API_SPEC.md"),
    (44, "Lead scoring calibration program", 5, "data", "Operations", "scripts/calibrate_lead_scoring.py", "pytest tests/test_strategy_os_scoring.py -q"),
    (45, "Global transformation program office", 0, "strategy", "CEO", "docs/transformation/README.md", "verify_global_ai_transformation.py"),
    (46, "Decision brief standard for reports", 4, "strategy", "CEO", "docs/transformation/decision_brief_template.md", "weekly proof decision brief section"),
    (47, "Revenue OS monetization blueprint", 3, "sales", "Revenue", "docs/transformation/revenue_os_monetization.md", "bash scripts/revenue_os_master_verify.sh"),
    (48, "Trust and assurance client dashboard", 4, "trust", "CTO", "api/routers/trust_dashboard.py", "pytest tests/test_trust_dashboard.py -q"),
    (49, "Experimentation OS with guardrails", 1, "product", "CTO", "lane_policy experimentation flags", "pytest tests/test_lane_policy.py -q"),
    (50, "12 month platform first roadmap", 9, "strategy", "CEO", "docs/transformation/PLATFORM_FIRST_12M_ROADMAP_AR.md", "verify_global_ai_transformation.py --check-initiatives"),
    (51, "Unified operating calendar", 0, "strategy", "CEO", "dealix/transformation/operating_calendar.yaml", "verify_global_ai_transformation.py --check-initiatives"),
    (52, "Priority arbitration framework", 0, "strategy", "CEO", "dealix/transformation/priority_arbitration.yaml", "verify_global_ai_transformation.py --check-initiatives"),
    (53, "Unified executive command center", 4, "product", "CEO", "v3 command center + founder dashboard", "pytest tests/test_v5_layers.py -q"),
    (54, "Voice of customer institutional", 4, "product", "CEO", "friction_log + NPS routers", "pytest tests/test_commercial_engagements_support_desk.py -q"),
    (55, "Definition of done unified", 4, "delivery", "Operations", "docs/transformation/definition_of_done.yaml", "verify_global_ai_transformation.py --check-initiatives"),
    (56, "Strategic dependency graph", 4, "strategy", "CEO", "dealix/transformation/strategic_dependency_graph.yaml", "verify_global_ai_transformation.py --check-initiatives"),
    (57, "Commercial translation L0-L5", 3, "sales", "Revenue", "commercial_os/evidence_level_sales_ar.yaml", "bash scripts/revenue_os_master_verify.sh"),
    (58, "Land and expand motion", 3, "sales", "Revenue", "expansion_engine readiness", "pytest tests/test_commercial_engagements_quick_win_ops.py -q"),
    (59, "Standardized QBRs", 6, "delivery", "Operations", "docs/transformation/qbr_template_ar.md", "verify_global_ai_transformation.py --check-initiatives"),
    (60, "Commercial forecast accuracy program", 3, "finance", "Revenue", "revenue_pipeline forecasting", "pytest tests/test_revenue_pipeline.py -q"),
    (61, "Strategic PMO lightweight", 10, "strategy", "CEO", "strategic_initiatives_registry.yaml", "verify_global_ai_transformation.py --check-initiatives"),
    (62, "Zero blind spots observability", 2, "observability", "CTO", "observability_v10 contracts", "verify_global_ai_transformation.py --check-observability"),
    (63, "Cost to serve per customer", 8, "finance", "CEO", "09_unit_economics cost_to_serve", "verify_global_ai_transformation.py --check unit-economics"),
    (64, "Contract intelligence tracking", 8, "finance", "CEO", "dealix/registers/contracts_register.yaml", "verify_global_ai_transformation.py --check-initiatives"),
    (65, "Business glossary unified", 5, "data", "Operations", "dealix/registers/business_glossary.yaml", "verify_global_ai_transformation.py --check-initiatives"),
    (66, "Regional expansion readiness", 9, "strategy", "CEO", "category_expansion_gates.yaml", "bash scripts/verify_category_expansion_before_scale.sh"),
    (67, "PMF signal engine", 4, "product", "CEO", "growth_v10 PMF signals", "pytest tests/test_growth_v10.py -q"),
    (68, "Customer health intelligence", 5, "delivery", "Operations", "customer_success_scores router", "pytest tests/test_customer_success_scores.py -q"),
    (69, "Execution quality score per team", 7, "delivery", "Operations", "delivery control tower metrics", "pytest tests/test_delivery_os_framework.py -q"),
    (70, "Enterprise anti-waste framework", 4, "trust", "CTO", "revenue_os anti-waste extended", "bash scripts/revenue_os_master_verify.sh"),
    (71, "Trust by design product wide", 1, "trust", "CTO", "governance_os + compliance", "pytest tests/test_enterprise_control_plane_e2e.py -q"),
    (72, "Executive simulation drills", 7, "strategy", "CEO", "reliability_drills executive tier", "python3 scripts/reliability_drills_scorecard.py"),
    (73, "Revenue assurance program", 3, "finance", "Revenue", "payment_ops + revenue assurance", "pytest tests/test_payment_ops.py -q"),
    (74, "Buy build partner map", 8, "platform", "CTO", "dealix/transformation/buy_build_partner_log.yaml", "verify_global_ai_transformation.py --check-initiatives"),
    (75, "Strategic narrative consistency", 4, "strategy", "CEO", "docs/strategic narrative index", "verify_global_ai_transformation.py --check-initiatives"),
    (76, "Delivery excellence framework", 6, "delivery", "Operations", "delivery_factory blueprints", "pytest tests/test_delivery_os_framework.py -q"),
    (77, "Meeting operating system", 0, "strategy", "CEO", "docs/transformation/meeting_os_ar.md", "verify_global_ai_transformation.py --check-initiatives"),
    (78, "Talent density critical teams", 10, "people_ops", "CEO", "11_org_operating_system.md", "verify_global_ai_transformation.py --check org-operating-system"),
    (79, "Knowledge retention program", 10, "people_ops", "CEO", "knowledge_v10 + academy", "pytest tests/test_knowledge_v10.py -q"),
    (80, "Governed innovation pipeline", 1, "product", "CTO", "lane_policy innovation lane", "pytest tests/test_lane_policy.py -q"),
    (81, "Enterprise audit readiness kit", 9, "trust", "CTO", "enterprise_package trust pack", "verify_global_ai_transformation.py --check-enterprise-package"),
    (82, "API product tiering", 2, "platform", "CTO", "platform_foundation API tiers", "pytest tests/test_platform_foundation.py -q"),
    (83, "Customer segment strategy map", 3, "gtm", "Revenue", "docs/strategic segment map", "verify_global_ai_transformation.py --check-initiatives"),
    (84, "Strategic risk heatmap quarterly", 8, "strategy", "CEO", "risk_register heatmap section", "verify_global_ai_transformation.py"),
    (85, "Renewal expansion intelligence", 3, "sales", "Revenue", "referral_program + renewal", "pytest tests/test_referral_program.py -q"),
    (86, "Service blueprint library", 6, "delivery", "Operations", "delivery_factory/blueprints/", "verify_global_ai_transformation.py --check-initiatives"),
    (87, "Internal benchmarking program", 7, "strategy", "CEO", "weekly_cross_os_snapshot", "python3 -c from dealix.execution.weekly_cross_os_snapshot"),
    (88, "Escalation clarity unified", 7, "strategy", "CEO", "ownership_matrix escalation", "verify_global_ai_transformation.py"),
    (89, "Strategic automation map", 7, "platform", "CTO", "dealix/transformation/automation_map.yaml", "verify_global_ai_transformation.py --check-initiatives"),
    (90, "Executive KPI narratives", 4, "finance", "CEO", "weekly proof narrative section", "generate_weekly_operating_proof_pack.py"),
    (91, "Multi product readiness", 9, "product", "CTO", "platform_core multi product flags", "pytest tests/test_platform_foundation.py -q"),
    (92, "Strategic customer council", 6, "gtm", "CEO", "docs/transformation/customer_council_ar.md", "verify_global_ai_transformation.py --check-initiatives"),
    (93, "Quality of revenue indicator", 8, "finance", "CEO", "kpi_registry QoR guardrail", "verify_global_ai_transformation.py"),
    (94, "Strategic scenario planning 12-24m", 8, "strategy", "CEO", "docs/transformation/scenario_planning_ar.md", "verify_global_ai_transformation.py --check-initiatives"),
    (95, "Board ready operating system", 9, "strategy", "CEO", "scripts/generate_board_ready_pack.py", "python3 scripts/generate_board_ready_pack.py"),
    (96, "Internal strategic SLAs", 7, "operations", "CEO", "ownership_matrix internal_sla", "verify_global_ai_transformation.py --check-initiatives"),
    (97, "Dealix operating playbook single", 0, "strategy", "CEO", "docs/transformation/DEALIX_OPERATING_PLAYBOOK_AR.md", "verify_global_ai_transformation.py --check-initiatives"),
    (98, "Strategic API governance council", 2, "platform", "CTO", "docs/architecture/API_GOVERNANCE_COUNCIL_AR.md", "verify_global_ai_transformation.py --check-initiatives"),
    (99, "Capital efficiency growth plan", 8, "finance", "CEO", "09_unit_economics capital efficiency", "verify_global_ai_transformation.py --check unit-economics"),
    (100, "Dealix 2030 strategic endgame", 0, "strategy", "CEO", "docs/transformation/DEALIX_2030_ENDGAME_AR.md", "verify_global_ai_transformation.py --check-initiatives"),
]

_RACI_ACCOUNTABLE = {
    "CEO": "founder",
    "CTO": "enterprise_control_plane_owner",
    "Revenue": "founder_sales_owner",
    "Operations": "delivery_factory_owner",
}


def _build() -> dict:
    initiatives = []
    for row in _INITIATIVES:
        iid, title, wave, owner_os, raci_r, deliverable, verification = row
        initiatives.append(
            {
                "id": iid,
                "key": f"initiative_{iid:03d}",
                "title_en": title,
                "title_ar": title,
                "wave": wave,
                "owner_os": owner_os,
                "status": "active" if iid in {1, 5, 13, 35, 100} else "proposed",
                "raci": {
                    "R": raci_r,
                    "A": _RACI_ACCOUNTABLE.get(raci_r, "founder"),
                    "C": "product,trust",
                    "I": "finance,delivery",
                },
                "deliverable": deliverable,
                "verification": verification,
            }
        )
    return {
        "version": 1,
        "program": "dealix_100_strategic_initiatives",
        "north_star_program_link": "dealix/transformation/north_star_manifest.yaml",
        "initiatives": initiatives,
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    out = root / "dealix/transformation/strategic_initiatives_registry.yaml"
    out.write_text(
        yaml.safe_dump(_build(), sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"Wrote {out} ({len(_INITIATIVES)} initiatives)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
