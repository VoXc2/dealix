# AI Run Ledger

Log **material** AI calls that affect client delivery—move from “we use AI” to “we **operate** AI.” IDs: `AI-###`.

## Rule

Client-facing or governance-sensitive outputs should record where possible:

- **Prompt / template version**  
- **Model** (+ provider)  
- **Inputs redacted** (Y/N)  
- **Output schema** / contract  
- **Cost** estimate  
- **QA** score (if applicable)  
- **Risk** level  

| ID | Project | Task | Model | Prompt Ver. | Inputs redacted | Output schema | Cost | QA | Risk |
|----|---------|------|-------|-------------|-----------------|---------------|------:|---:|------|
| AI-001 | Lead Sprint A | score accounts | *model* | v1.2 | Yes | ScoreBreakdown | 0.40 | 91 | Low |

**Pair with:** [`PROMPT_REGISTRY.md`](PROMPT_REGISTRY.md), [`EVALUATION_REGISTRY.md`](EVALUATION_REGISTRY.md), [`COST_GOVERNANCE.md`](../company/COST_GOVERNANCE.md).
