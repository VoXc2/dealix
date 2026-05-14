# Control Mapping

Each non-negotiable in `11_NON_NEGOTIABLES.md` maps to one or more operational controls. Use this as a starting point; adapt to your environment.

| # | Non-Negotiable | Primary Control | Where It Lives |
|---|----------------|-----------------|----------------|
| 1 | No scraping | Data acquisition policy + Source Passport | Data layer |
| 2 | No cold WhatsApp automation | Outreach approval gate + recipient consent registry | Sales / Outreach layer |
| 3 | No LinkedIn automation | Manual outreach policy + audit log | Sales / Outreach layer |
| 4 | No guaranteed sales outcomes | Public claims gate + proof requirement | Marketing layer |
| 5 | No source-less AI output | Source Passport requirement | Data + AI layer |
| 6 | No external action without approval | Approval gate at action boundary | Runtime governance |
| 7 | No agent without identity | Agent identity registry + scope manifest | Runtime governance |
| 8 | No public case study without verified proof | Proof Pack + client approval workflow | Marketing / Trust layer |
| 9 | No autonomous upsell | Pricing / contract change approval gate | Commercial layer |
| 10 | No capital asset without provenance | Capital Asset Library entry with provenance | Capital layer |
| 11 | No unsafe growth | Governance review of growth motions | Governance review |

## Minimum Adoption Checklist
1. Inventory all AI-touching workflows.
2. For each, identify the data source and whether a Source Passport exists.
3. For each, identify whether external action is possible and whether approval is enforced.
4. For each AI agent, record identity, owner, scope, and audit log location.
5. Review public claims and case studies for proof backing.
6. Add a governance review step for any growth proposal that touches outreach, data, or autonomous action.

## What Adoption Does Not Mean
Adopting this doctrine is not certification. It is an operating discipline. Implementation quality matters more than declaration.
