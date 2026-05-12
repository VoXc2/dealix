# Contract Analyst (AR + EN redlining)

Reads a contract PDF/Markdown/DOCX and produces (a) a clause-by-clause
summary, (b) suggested redlines, and (c) risk flags. Built for Saudi
commercial contracts (LLC service agreements, NDAs, partner deals).

## Output

```yaml
clauses:
  - id: int
    title: string
    summary_ar: string
    summary_en: string
    risk: low | medium | high
    suggested_redline: string | null
contract_type: nda | msa | order_form | partnership | other
governing_law: string
overall_risk: low | medium | high
```
