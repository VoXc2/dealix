# Governance Decision

Any action involving **data**, **outreach**, **claims**, or **external communication** must pass this gate before execution or client delivery.

## Questions

1. Is the **source** known and documented?
2. Does it contain **PII**? What fields?
3. Is there **lawful basis** (consent, contract, legitimate interest, public, etc.) per policy?
4. Is the action **internal** or **external** (customer-visible / third-party)?
5. Does it require **approval** per [`APPROVAL_MATRIX.md`](APPROVAL_MATRIX.md)?
6. Does it include a **risky claim** (ROI guarantee, medical/legal certainty)?
7. Does it need **redaction** before sharing?
8. Is it **logged** when material ([`AUDIT_LOG_POLICY.md`](AUDIT_LOG_POLICY.md))?

**PDPL / handling:** lawful basis and minimization are non-optional for personal data. Industry context: AI success depends on **AI-ready data** and disciplined use ([Gartner press release on AI-ready data](https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk)).

## Decision outcomes

| Outcome | When |
|---------|------|
| **Allow** | Low risk; policy-clear; internal draft |
| **Allow with approval** | External send, client-identifiable report, sensitive channel |
| **Redact then allow** | PII or excess detail removable |
| **Research-only** | Missing source; not valid for client-facing certainty |
| **Block** | Forbidden action, unlawful basis, or unapproved cold outreach |

## Examples

| Client ask | Decision |
|------------|----------|
| “Write an email draft” | Allow (draft) |
| “Send WhatsApp to everyone on the list” cold | **Block** |
| “Prepare WhatsApp drafts for opted-in / relationship accounts” | Allow **with approval** per message |
| “Use mobile numbers with no source” | Research-only or **Block** |
| “Write we guarantee sales” | **Block** / rewrite to operational outputs |

Log in `clients/<client>/governance_events.md`.
