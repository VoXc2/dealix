# Governance Agent Risk Profile

## Risk Tier

Declared tier: `critical`.

## Primary Risks

| Risk ID | Description | Mitigation | Evidence ID |
|---|---|---|---|
| R-AGT-GOV-001 | inaccurate decision suggestion under pressure | require evidence-backed reasoning and confidence output | E-AGT-GOV-040 |
| R-AGT-GOV-002 | unauthorized side-effect proposal | policy check plus approval gate before execution | E-AGT-GOV-041 |
| R-AGT-GOV-003 | drift after prompt or tool changes | run eval suite before release | E-AGT-GOV-042 |
