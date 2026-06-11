"""Master verification for Dealix Ultimate Commercial OS.

Usage:
    python3 scripts/verify_dealix_ultimate_os.py
"""
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    # Brand
    "business/brand/DEALIX_BRAND_SYSTEM.md",
    "business/brand/DEALIX_LOGO_AND_IDENTITY_SYSTEM.md",
    "business/brand/DEALIX_COPY_BANK_AR.md",
    "business/brand/DEALIX_COPY_BANK_EN.md",
    "apps/web/public/dealix-logo.svg",
    "apps/web/public/dealix-mark.svg",
    "apps/web/public/dealix-og.svg",
    # Website pages
    "apps/web/app/brand/page.tsx",
    "apps/web/app/offers/page.tsx",
    "apps/web/app/pricing/page.tsx",
    "apps/web/app/cases/page.tsx",
    "apps/web/app/revenue-machine/page.tsx",
    "apps/web/app/sales-assets/page.tsx",
    "apps/web/app/lead-engine/page.tsx",
    "apps/web/app/persuasion-room/page.tsx",
    "apps/web/app/command-center/page.tsx",
    "apps/web/app/war-room/page.tsx",
    "apps/web/app/pipeline/page.tsx",
    "apps/web/app/delivery-os/page.tsx",
    "apps/web/app/partner-room/page.tsx",
    "apps/web/app/daily-draft/page.tsx",
    "apps/web/app/kpi-finance/page.tsx",
    "apps/web/app/client-acquisition/page.tsx",
    "apps/web/app/automated-sales/page.tsx",
    # APIs
    "apps/web/app/api/company-os/ceo-brief/route.ts",
    "apps/web/app/api/company-os/founder-dashboard/route.ts",
    "apps/web/app/api/sales-machine/ultimate-pack/route.ts",
    "apps/web/app/api/sales-machine/daily-pack/route.ts",
    # Libraries
    "apps/web/lib/company-os/company-os.ts",
    "apps/web/lib/company-os/pipeline.ts",
    "apps/web/lib/sales-machine/ultimate-sales-os.ts",
    "apps/web/lib/sales-automation/lead-sources.ts",
    "apps/web/lib/generated/founder-dashboard.ts",
    # Sales machine docs
    "business/sales-machine/DEALIX_MASTER_SALES_FILE_AR.md",
    "business/sales-machine/DEALIX_MASTER_SALES_FILE_EN.md",
    "business/sales-machine/OBJECTION_HANDLING_LIBRARY.md",
    "business/sales-machine/PERSUASION_ANGLE_MATRIX.md",
    "business/sales-machine/LEAD_SOURCE_CONNECTORS_SPEC.md",
    "business/sales-machine/SALES_DAILY_OPERATING_SYSTEM.md",
    "business/sales-machine/INDUSTRY_WEAKNESS_TAXONOMY.md",
    "business/sales-machine/OFFER_MATCHING_RULES.md",
    "business/sales-machine/HUMAN_REVIEW_POLICY.md",
    # CRM
    "business/crm/schema.md",
    "business/crm/prospects.seed.json",
    "business/crm/README.md",
    # Proposals
    "business/proposals/PROPOSAL_TEMPLATE_AR.md",
    "business/proposals/PROPOSAL_TEMPLATE_EN.md",
    "business/proposals/PROPOSAL_SECTIONS_LIBRARY.md",
    # Delivery
    "business/delivery/CLIENT_DELIVERY_SOP.md",
    "business/delivery/CLIENT_ONBOARDING_CHECKLIST.md",
    "business/delivery/PROOF_REPORT_TEMPLATE.md",
    "business/delivery/WEEKLY_COMMAND_REPORT_TEMPLATE.md",
    "business/delivery/CHANGE_REQUEST_POLICY.md",
    "business/delivery/DELIVERY_AUTOMATION_BLUEPRINT.md",
    # Governance
    "business/governance/AI_HUMAN_REVIEW_POLICY.md",
    "business/governance/PDPL_AWARE_DATA_BOUNDARIES.md",
    "business/governance/OUTREACH_COMPLIANCE_POLICY.md",
    "business/governance/NO_SPAM_POLICY.md",
    "business/governance/SOURCE_AND_DATA_USAGE_REGISTER.md",
    "business/legal-lite/CLIENT_BOUNDARIES.md",
    # Pricing/Finance
    "business/pricing/OFFER_LADDER.md",
    "business/pricing/PRICING_STRATEGY_AR.md",
    "business/pricing/PRICING_STRATEGY_EN.md",
    "business/pricing/QUOTE_RULES.md",
    "business/finance/UNIT_ECONOMICS_MODEL.md",
    "business/finance/KPI_FINANCE_CONTROL.md",
    # CEO
    "business/ceo/FOUNDER_WAR_ROOM.md",
    "business/reports/DAILY_CEO_BRIEF_TEMPLATE.md",
    "business/reports/WEEKLY_OPERATING_REVIEW.md",
    # AI
    "business/ai/AI_TASK_ROUTING.md",
    "docs/ai/AI_MODEL_ROUTER_PLAN.md",
    "docs/integrations/INTEGRATION_ARCHITECTURE.md",
    "docs/integrations/GOOGLE_PLACES_CONNECTOR_PLAN.md",
    "docs/integrations/WHATSAPP_BUSINESS_CONNECTOR_PLAN.md",
    "docs/integrations/HUBSPOT_OR_CRM_CONNECTOR_PLAN.md",
    "docs/integrations/OPEN_DATA_CONNECTOR_PLAN.md",
    "docs/integrations/EMAIL_OUTREACH_CONNECTOR_PLAN.md",
    "docs/security/SALES_AUTOMATION_SECURITY_MODEL.md",
    "docs/security/DATA_MINIMIZATION.md",
    "docs/security/AUDIT_LOGGING_PLAN.md",
    # Scripts
    "scripts/import_leads_csv.py",
    "scripts/score_leads.py",
    "scripts/generate_outreach_drafts.py",
    "scripts/approve_outreach_draft.py",
    "scripts/reject_outreach_draft.py",
    "scripts/generate_prospect_pack.py",
    "scripts/generate_followup_queue.py",
    "scripts/generate_proposal.py",
    "scripts/generate_client_brief.py",
    "scripts/generate_workflow_review_agenda.py",
    "scripts/generate_delivery_plan.py",
    "scripts/generate_weekly_command_report.py",
    "scripts/generate_daily_ceo_brief.py",
    "scripts/generate_weekly_operating_review.py",
    "scripts/generate_ultimate_sales_os_pack.py",
    "scripts/generate_sales_machine_pack.py",
    "scripts/verify_dealix_ultimate_os.py",
    "scripts/verify_ultimate_sales_os.py",
    "scripts/verify_sales_machine.py",
    "scripts/verify_client_acquisition_delivery_os.py",
]


def main() -> int:
    missing = [r for r in REQUIRED if not (REPO_ROOT / r).exists()]
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  - {m}")
        return 1
    print("Dealix Ultimate Commercial OS verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
