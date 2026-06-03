#!/usr/bin/env python3
"""Fail if any required Dealix file is missing."""
import _bootstrap  # noqa: F401
from dealix.lib import ROOT, CheckResult

REQUIRED = [
    # docs — policies & contracts
    "docs/site/SITE_ARCHITECTURE_AR.md",
    "docs/commercial/FOCUS_5_SYSTEMS_MARKET_ENTRY_AR.md",
    "docs/business_os_catalog/BUSINESS_OS_CATALOG_AR.md",
    "docs/business_need_intelligence/NEED_TAXONOMY_25_AR.md",
    "docs/business_need_intelligence/BUSINESS_NEED_INTELLIGENCE_ENGINE_AR.md",
    "docs/account_intelligence/ACCOUNT_PACK_OUTPUT_CONTRACT_AR.md",
    "docs/contacts/CONTACT_DISCOVERY_POLICY_AR.md",
    "docs/outreach/DAILY_400_SYSTEM_DRAFT_FACTORY_AR.md",
    "docs/acquisition/CALL_BRIEF_SYSTEM_AR.md",
    "docs/proposals/MINI_PROPOSAL_FACTORY_AR.md",
    "docs/delivery/AUTOMATED_DELIVERY_PIPELINE_AR.md",
    "docs/finance/CASH_PRIORITY_SCORE_AR.md",
    "docs/quality/EMAIL_QUALITY_GATE_AR.md",
    "docs/security/EXTERNAL_CONTENT_UNTRUSTED_DATA_POLICY.md",
    "docs/privacy/DO_NOT_CONTACT_AND_SUPPRESSION_POLICY_AR.md",
    "docs/founder_control/DAILY_SUPER_COMMAND_SYSTEM_AR.md",
    "docs/operating_factory/READY_TO_LAUNCH_CHECKLIST_AR.md",
    # schemas
    "schemas/account_intelligence_pack.schema.json",
    "schemas/business_system.schema.json",
    "schemas/need_taxonomy.schema.json",
    "schemas/specialized_sprint.schema.json",
    "schemas/email_draft.schema.json",
    "schemas/mini_proposal.schema.json",
    "schemas/delivery_pipeline.schema.json",
    # data
    "data/business_os_catalog/systems.yaml",
    "data/business_need_intelligence/need_taxonomy_25.yaml",
    "data/business_need_intelligence/sector_need_matrix_20.yaml",
    "data/business_need_intelligence/specialized_sprint_library_50.yaml",
    "data/account_intelligence/account_packs.jsonl",
    "data/contacts/contact_discovery.jsonl",
    "data/outreach/email_drafts.jsonl",
    "data/acquisition/call_briefs.jsonl",
    "data/proposals/mini_proposals.jsonl",
    "data/delivery/pipelines.jsonl",
    "data/finance/cash_priority_scores.jsonl",
    "data/suppression/do_not_contact.jsonl",
    "data/site/site_routes.yaml",
    # site catalog (public)
    "src/marketing/catalog.ts",
    # reports
    "reports/operating_factory/READY_TO_LAUNCH_SCORECARD.md",
    "reports/founder/DAILY_SUPER_COMMAND.md",
]


def main():
    r = CheckResult("file_manifest")
    for rel in REQUIRED:
        if (ROOT / rel).exists():
            r.ok(rel)
        else:
            r.fail(f"missing required file: {rel}")
    return r.finish()


if __name__ == "__main__":
    main()
