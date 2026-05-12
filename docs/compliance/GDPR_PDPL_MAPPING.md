# GDPR ↔ PDPL ↔ code-path mapping

Every PDPL article + GDPR article that touches our data-processing
behaviour, with the file that enforces it. Auditors copy this into
their evidence pack; engineers use it as a "where do I find the code
for X" map.

| PDPL Art. | GDPR Art. | Topic | Enforcement |
| --- | --- | --- | --- |
| 1–3 | 1–3 | Scope + definitions | `docs/legal/DPA.md` §1, 4 |
| 4 | 5 | Principles (lawful, fair, transparent) | Customer-portal copy + `docs/api/auth.mdx` |
| 5 | 6 | Lawful bases | `auto_client_acquisition/compliance_os/contactability.py` |
| 6 | 7 | Consent | `db/models.ConsentRequestRecord`, `api/routers/pdpl.py` |
| 7–8 | 8, 25 | Children + PbD | Adult-only product; PbD via tenant isolation. |
| 11 | 13–14 | Information to data subject | `docs/legal/DPA.md`, privacy page. |
| 12–16 | 15–17 | Access / correction / erasure | `api/routers/pdpl_dsr.py` |
| 17 | 18 | Restriction | `UserRecord.is_active=False` (soft-delete). |
| 18 | 30 | Records of processing | `AuditLogRecord` + `compliance_os/ropa.py`. |
| 19 | 32 | Security | `api/middleware/*`, `core/llm/guardrails.py`. |
| 20 | 28 | Processor obligations | `docs/legal/DPA.md` §8. |
| 21 | 28(2) | Sub-processors | `docs/compliance/SUB_PROCESSORS.md`. |
| 22 | 33 | Personal-data breach notification | `docs/ops/incident_response.md` §4 (72-h DPO). |
| 23 | 35 | DPIA | `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`. |
| 27 | — | Cross-border transfer | `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`. |
| 29 | — | Transfer registration | Same addendum + sub-processor list. |
| 31 | 37 | DPO | `dpo@ai-company.sa` (designated). |
| — | 24 | Controller accountability | `docs/compliance/CONTROLS.md` (SOC 2 + this table). |
| — | 32 | Encryption + pseudonymisation | `api/middleware/bopla_redaction.py`. |

## Differences worth knowing

- **PDPL Art. 18** explicit audit log → we ship `AuditLogRecord` from
  day one. GDPR Art. 30 ROPA is similar but document-shaped; our
  `compliance_os/ropa.py` generates it on demand.
- **Cross-border transfers**: GDPR uses SCCs / adequacy decisions;
  PDPL Art. 29 requires regulator notification or adequacy. We file
  under the addendum and the Saudi-region runbook
  (`docs/ops/saudi_region.md`) closes the loop for fully-in-Kingdom
  contracts.
- **Right to be forgotten**: GDPR is hard-delete by default; PDPL is
  more permissive on legitimate-business retention. Our default is
  the stricter GDPR shape — `pdpl_dsr.request_delete` queues for DPO
  review with a 14-day grace, then hard-deletes.

## How to add a new article

1. Open a PR adding the row above.
2. Cite the **exact file path** that enforces it.
3. Cross-link from `docs/compliance/CONTROLS.md` if a SOC 2 control
   maps to the same code path.
