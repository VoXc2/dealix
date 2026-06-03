# Incident Response

Even small teams need a **written** path for AI/data incidents—confidence scales with clarity.

## Incident types

- PII exposure or unlawful processing  
- Wrong / harmful AI output **delivered** to client  
- Unsupported claim in client-facing asset  
- Unauthorized access or credential issue  
- Client data mishandling (wrong tenant, wrong export)  
- Automation misfire (wrong recipient, wrong document)  

## Response steps

1. **Stop** affected workflow / revoke tokens if needed  
2. **Preserve** evidence (logs, versions, prompts—per policy)  
3. **Assess** impact (who, what data, external blast radius)  
4. **Notify** internal owner; client notification per contract/law **if required**  
5. **Correct** output, data, or configuration  
6. Document **root cause** (RCA lite)  
7. **Update** controls (runtime checks, prompts, evals)  
8. **Update** playbook / [`../ledgers/LEARNING_LEDGER.md`](../ledgers/LEARNING_LEDGER.md)  

Log material events in [`../ledgers/GOVERNANCE_LEDGER.md`](../ledgers/GOVERNANCE_LEDGER.md) and client `governance_events.md` when client-specific.

See [`../enterprise/CONTROLS_MATRIX.md`](../enterprise/CONTROLS_MATRIX.md) for enterprise expectations.
