# Enterprise Controls Matrix

Controls expected when selling **enterprise-grade** AI operations—not all are required day one; **document** what you have vs gap.

| Control | Description | Required for |
|---------|-------------|--------------|
| RBAC | Role-based access control | enterprise multi-team |
| SSO | Single sign-on | enterprise IT standard |
| Audit exports | Exportable decision logs | enterprise procurement |
| Data retention | Retention + deletion procedures | sensitive / regulated |
| Approval workflows | Human approval before external effects | all external channels |
| PII redaction | Protect personal data in logs/reports | all |
| Model run logs | Trace prompts/versions/cost for AI runs | production AI |
| Eval reports | Measurable output quality | production AI at scale |
| Incident response | Documented IR path | enterprise trust ([`../governance/INCIDENT_RESPONSE.md`](../governance/INCIDENT_RESPONSE.md)) |

## Enterprise readiness

Do not enter **enterprise** deals before operational coverage of: audit posture, RBAC model, retention, support, IR, and this matrix (see [`ENTERPRISE_READINESS.md`](ENTERPRISE_READINESS.md), [`ENTERPRISE_DECISION.md`](ENTERPRISE_DECISION.md)).
