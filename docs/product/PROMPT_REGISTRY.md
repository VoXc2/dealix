# Prompt Registry

No **production** prompt without owner, schema, and eval linkage.

| Prompt ID | Version | Service | Purpose | Owner | Eval hook |
|-----------|---------|---------|---------|-------|-----------|
| lead_scoring_prompt | v1.0 | Lead Intelligence | score account fit | | lead_intelligence_eval |
| outreach_draft_prompt | v1.0 | Lead Intelligence | safe drafts | | outreach_quality_eval |
| citation_answer_prompt | v1.0 | Company Brain | answer with sources | | company_brain_eval |

## Each prompt must define

```text
purpose
input schema
output schema
forbidden behavior
examples
eval tests
version history
```

Implementation: store in repo or prompt DB with **checksum**; reference version in [`AI_RUN_LEDGER.md`](../ledgers/AI_RUN_LEDGER.md).
