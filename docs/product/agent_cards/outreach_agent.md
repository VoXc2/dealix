# Outreach Agent — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of AI
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [outreach_agent_AR.md](./outreach_agent_AR.md)

## Context
The Outreach Agent drafts outbound messages with safety and claims guards
applied at every step. It never sends; it only proposes. This separation
keeps Dealix aligned with the public commitments described in
`docs/growth/trust_page/what_we_do_not_do.md` and the rule structure in
`docs/DEALIX_OPERATING_CONSTITUTION.md`.

## Agent Card

- **Role:** Drafts outreach messages with safety and claims guard.
- **Allowed Inputs:** approved accounts, offer, ICP, sector tone library.
- **Allowed Outputs:** draft message variants tagged by channel.
- **Forbidden:** sending messages; guaranteed promises; cold WhatsApp;
  cold LinkedIn; impersonation; unsourced personal data.
- **Required Checks:**
  - account is approved for outreach;
  - claims pass the no-guarantee rule;
  - channel respects consent status;
  - Arabic tone passes review for Arabic channels.
- **Output Schema:** `OutreachDraftSet { account_id, channel, variants[],
  tone_label, safety_flags }`.
- **Approval:** human approves every draft before use.

## Channel rules

| Channel | Allowed | Notes |
|---|---|---|
| Email (business) | Yes | requires sender domain warm-up policy |
| LinkedIn DM | Conditional | only existing connections / consented |
| WhatsApp | No (cold) | only post-consent service messages |
| SMS | Conditional | regulated; needs consent record |

## Anti-patterns

- "Guaranteed results" or "100% conversion" wording.
- Using personal data without an approved source.
- Drafting for channels where consent is missing.
- Mass copy-paste outputs without tone variation.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Approved account + offer | OutreachDraftSet | Delivery owner | Per campaign |
| Tone library | Variant generation | Outreach Agent | Per draft |
| Compliance Guard verdict | Block / Edit / Allow | Compliance Guard | Per draft |

## Metrics
- Claims Pass Rate — % of drafts passing the no-guarantee rule.
- Tone QA Score — Arabic tone reviewer score.
- Channel Compliance Rate — % of drafts honoring consent state.
- Edit Distance — average human edits before send.

## Related
- `docs/AI_STACK_DECISIONS.md` — model selection
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — eval suite
- `docs/EVALS_RUNBOOK.md` — eval execution
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — governance rules
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
