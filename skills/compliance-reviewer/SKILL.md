# Compliance Reviewer (PDPL + GDPR + CITC ad-rules)

Reviews any outbound message (email, WhatsApp, SMS, voice script)
against Saudi PDPL, GDPR (when EU recipients in scope), and Saudi
CITC ad-content rules. Outputs a verdict + redlines.

## Output

```yaml
verdict: pass | warn | block
violations:
  - rule_id: string
    severity: low | medium | high
    excerpt: string
    suggested_fix: string
```
