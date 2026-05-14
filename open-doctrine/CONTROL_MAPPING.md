# Control Mapping

Each non-negotiable below maps to a verifiable control. Controls listed
as *test* are automated. Controls listed as *runtime* are enforced by a
policy engine. Controls listed as *operational* are enforced by a
documented procedure with an owner.

| # | Commitment                                  | Control type        | Reference / Mechanism                                           |
|---|---------------------------------------------|---------------------|------------------------------------------------------------------|
| 1 | Source Passport before AI use               | runtime + test      | data-os source passport; locked by source-passport guard test    |
| 2 | Human approval before external action       | runtime + test      | approval policy; locked by external-action approval test         |
| 3 | Governance Runtime before client output     | runtime + test      | runtime decision engine returning ALLOW/DRAFT_ONLY/REQUIRE_APPROVAL/REDACT/BLOCK/ESCALATE; locked by governance-status test |
| 4 | Proof Pack before any claim                 | runtime + test      | proof pack required test; case study requires verified value     |
| 5 | No scraping                                 | test                | no-scraping-engine test                                          |
| 6 | No cold WhatsApp                            | test                | no-cold-whatsapp test                                            |
| 7 | No LinkedIn automation                      | test                | no-linkedin-automation test                                      |
| 8 | No guaranteed sales claims                  | test                | no-guaranteed-claims test                                        |
| 9 | No agent without identity                   | runtime + test      | agent identity card required; agent-no-external-action test      |
| 10 | Capital Asset registration before invoice  | operational + test  | first-invoice unlock runbook; capital asset index validity test  |
| 11 | Verifiable, not merely trusted             | test                | master verifier (`scripts/verify_all_dealix.py`) and per-rule tests |

## What This Document Is NOT

- It is not a marketing document.
- It is not an exhaustive list of every internal Dealix test.
- It is not commercial implementation code.
- It is not a claim of regulatory compliance for any specific
  jurisdiction.

## What This Document IS

A public map from each commitment to a class of verifiable control,
sufficient for a buyer, partner, regulator, or auditor to ask "which
test fails if you violate commitment N?" and get a meaningful answer.

Dealix's commercial implementations of these controls live in private
repositories. The doctrine itself, including this mapping, is public so
that the standard can be checked independently of any vendor — including
Dealix.
