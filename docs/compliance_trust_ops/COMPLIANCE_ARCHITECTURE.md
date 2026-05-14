# Compliance Architecture

```
compliance_trust_os/
  source_passport_v2
  pii_classifier
  allowed_use_checker
  claim_compliance
  approval_engine
  audit_trail
  incident_response
  compliance_report
  compliance_dashboard
```

Every output passes: Source Passport → PII → Allowed Use → Task Risk → Channel Risk → Claim Safety → Governance Decision → Approval → Audit → QA → Output.
