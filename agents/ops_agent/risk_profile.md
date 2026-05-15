# Ops Agent Risk Profile

## Risk Tier

Declared tier: `high`.

## Primary Risks

| Risk ID | Description | Mitigation | Evidence ID |
|---|---|---|---|
| R-AGT-OPS-001 | inaccurate decision suggestion under pressure | require evidence-backed reasoning and confidence output | E-AGT-OPS-040 |
| R-AGT-OPS-002 | unauthorized side-effect proposal | policy check plus approval gate before execution | E-AGT-OPS-041 |
| R-AGT-OPS-003 | drift after prompt or tool changes | run eval suite before release | E-AGT-OPS-042 |
