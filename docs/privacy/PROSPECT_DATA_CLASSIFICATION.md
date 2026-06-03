# Prospect Data Classification

| Class | Examples | Handling |
|-------|----------|----------|
| **Public business** | company name, website, sector, public role | OK to store/use; minimize |
| **Business-personal** | named decision-maker, work email/phone | minimize; prefer role; PDPL rights apply |
| **Sensitive (PII)** | national ID, personal financial, health, religion | ❌ do not collect |
| **Secret/credential** | API keys, passwords, tokens | ❌ never; detectors block |
| **Derived** | score, intent, leak hypothesis | internal; evidence-level tagged |

## Rules
- Default to the lowest class that achieves the purpose.
- Business-personal triggers PDPL data-subject rights (`OUTREACH_DATA_RIGHTS_AR.md`).
- Sensitive/secret classes are blocked by policy and by `core/safety` detectors.
- `scripts/governance_check.py` flags probable personal names in `prospects.csv`.
