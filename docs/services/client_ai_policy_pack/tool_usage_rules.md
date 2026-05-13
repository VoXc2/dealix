# Client AI Policy Pack — Tool Usage Rules

**Layer:** L5 · Enterprise Governance
**Owner:** Governance Lead + IT Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [tool_usage_rules_AR.md](./tool_usage_rules_AR.md)

## Context
The fastest data leaks happen at the tool boundary. A free chatbot, a browser extension, or a "trial" automation product can quietly send sensitive data outside the company. This file states the rules for tool usage that flow out of the policy in `./policy_template.md`, the matrix in `./approval_matrix.md`, and the employee guide in `./employee_guide.md`. It aligns with the data terms in `docs/DPA_DEALIX_FULL.md`, the retention model in `docs/DATA_RETENTION_POLICY.md`, and the PDPL alignment in `docs/ops/PDPL_RETENTION_POLICY.md`.

## Tool categories
- **Public chatbots** — consumer-grade AI chat products with no enterprise data terms.
- **Approved enterprise AI tools** — vetted vendor products with enterprise data terms, data residency commitments, and contractual safeguards.
- **Internal Dealix-managed AI** — agents and workflows built or operated by Dealix inside the client workspace.

## Rule 1 — Public chatbots: no sensitive data
- Public chatbots may be used for **public information only** — generic drafting, brainstorming, explanations.
- Customer data, employee data, financial data, deal data, PII, regulated data, and any internal document classified higher than "Public" must never be pasted, uploaded, or referenced in a public chatbot.
- Public chatbots may not be used as the means of producing client-facing communications, unless the resulting text is reviewed for confidentiality before sending.

## Rule 2 — Approved enterprise tools: within RBAC
- Use only with company credentials and within Role-Based Access Control.
- The user's role must be sufficient for the data the user requests through the tool.
- No personal accounts; no shared logins; no bypass of single sign-on.
- The tool's data residency and retention settings must match the policy.

## Rule 3 — Logs are required for outputs used outside the team
- Any AI-generated output that leaves the immediate working team — sent to a client, posted publicly, used in a board pack, included in a regulatory filing — must be logged.
- The log includes: user, tool, prompt summary or input class, output reference, reviewer, and timestamp.
- Logs are retained per the data retention policy.

## Rule 4 — Browser extensions and plugins
- AI browser extensions may not be installed on company devices without IT and Governance approval.
- "Free" AI plugins that access page content, mailboxes, or calendars are prohibited unless explicitly approved.

## Rule 5 — Vendor approval is required for new tools
- No new AI tool — paid or free, consumer or enterprise — may be used for company work without going through the vendor approval process.
- Approval depends on data residency, contract terms, sub-processor list, vendor security posture, and policy alignment.
- The approved list is maintained by IT and Governance and published in the client workspace.

## Approved tools list (template)
| Tool | Category | Allowed Data Classes | Approver | Renewal Date |
|---|---|---|---|---|
| [Vendor X] | Enterprise AI | Internal, Confidential | Governance | YYYY-MM-DD |
| [Vendor Y] | Public chatbot | Public only | Manager | n/a |
| [Dealix Agent] | Internal Dealix-managed AI | Internal, Confidential | Governance | YYYY-MM-DD |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| New tool requests | Approved list updates | IT + Governance | As needed |
| Data classification map | Tool-by-tool allowed data classes | Governance + Data Owner | Quarterly |
| Audit findings | Policy / list adjustments | Governance | Quarterly |

## Metrics
- Approved-Tool Compliance — % of measured AI use that happened in an approved tool.
- Unapproved-Tool Detection — count of unapproved tool incidents per quarter.
- Log Coverage — % of "outside-team" outputs with a complete log entry.
- Renewal Hygiene — % of approved tools reviewed before renewal date.

## Related
- `docs/DPA_DEALIX_FULL.md` — DPA framing the data terms
- `docs/DATA_RETENTION_POLICY.md` — retention rules for logs
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL alignment
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — certifications context
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
