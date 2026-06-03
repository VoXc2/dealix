# Governance as Code

Governance rules should be executable.

## Rule Examples

RULE: no_cold_whatsapp  
IF channel = whatsapp AND relationship_status != consented_or_existing  
THEN block  

RULE: no_guaranteed_claims  
IF output contains guaranteed sales language  
THEN rewrite_or_block  

RULE: no_source_no_answer  
IF answer has no source  
THEN insufficient_evidence  

RULE: pii_redaction_required  
IF output contains phone/email/person_name AND destination = report/public  
THEN redact_or_require_basis  

## Packaged YAML (v0)

Rule documents live in `auto_client_acquisition/governance_os/rules/` and are loaded by `rules.loader` (see tests). Runtime engine may evolve beyond draft-string audits.

## Later technical layout

```text
governance_os/
  rules/
    *.yaml
  engine.py  # future: structured evaluation
```

(Previously listed example filenames — now see repo folder.)

## Why

Paper governance is not enough when AI runs inside workflows.
