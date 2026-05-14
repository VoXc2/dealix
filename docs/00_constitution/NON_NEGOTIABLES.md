# Non-Negotiables — الخطوط الحمراء

> Purpose: the eleven rules that define the perimeter Dealix operates inside. Each rule is enforced by a test, middleware, or governance module. Flipping any rule requires a dedicated PR, a founder sign-off, and a safety review. See [DEALIX_CONSTITUTION.md](./DEALIX_CONSTITUTION.md) for context.

These rules are not preferences. They are the conditions that let Dealix sell **Governed AI Operations** instead of "AI tools" or "lead-gen". If even one is silently relaxed, the category claim collapses.

## The eleven rules — القواعد الإحدى عشرة

### 1. No scraping — لا تجريف بيانات

- **Statement:** Dealix never scrapes websites, social platforms, or third-party UIs to harvest contacts or content.
- **Consequence:** any code path that scrapes is treated as a constitutional violation and reverted. Any data acquired by scraping is quarantined and excluded from drafts and proof.
- **Enforced by:** `tests/test_no_scraping_engine.py`.

### 2. No cold WhatsApp automation — لا واتساب بارد

- **Statement:** Dealix never sends WhatsApp messages to recipients without explicit, recorded, opt-in consent tied to a Source Passport.
- **Consequence:** cold WhatsApp sends are blocked at the `safe_send_gateway` layer; attempts produce a governance event of kind `cold_send_blocked`.
- **Enforced by:** `tests/test_no_cold_whatsapp.py`.

### 3. No LinkedIn automation — لا أتمتة LinkedIn

- **Statement:** Dealix never automates LinkedIn connection requests, messages, scraping, or feed actions.
- **Consequence:** any integration that automates LinkedIn is rejected at PR review and at runtime. LinkedIn data may enter Dealix only via legitimate exports owned by the client.
- **Enforced by:** `tests/test_no_linkedin_automation.py`.

### 4. No fake or un-sourced claims — لا ادعاءات بلا مصدر

- **Statement:** Dealix never publishes a number, quote, case study, or proof artifact without a `source_ref` and a Source Passport.
- **Consequence:** content without a source is downgraded to `draft_only`. Public proof is blocked.
- **Enforced by:** `tests/test_no_guaranteed_claims.py`.

### 5. No guaranteed sales outcomes — لا ضمانات مبيعات

- **Statement:** Dealix never promises a fixed revenue, deal count, or conversion rate. Words like "guarantee", "ensure", and "we will close X deals" are redacted.
- **Consequence:** drafts containing guarantee language are returned with decision `REDACT`. Sales decks containing such language are blocked from external use.
- **Enforced by:** `tests/test_no_guaranteed_claims.py`.

### 6. No PII in logs — لا PII في السجلات

- **Statement:** Dealix never writes raw personal data (names, phone numbers, national IDs, emails, addresses) into application logs, friction logs, or telemetry.
- **Consequence:** PII is redacted at the middleware boundary before any log writer sees it. A leak is treated as a P0 incident.
- **Enforced by:** `api/middleware/bopla_redaction.py` and `auto_client_acquisition/friction_log/sanitizer.py`.

### 7. No source-less knowledge answers — لا إجابة بلا مصدر

- **Statement:** Dealix never answers a knowledge or research question without citing a Source Passport. If no passport is available, the system returns "source required" instead of inventing an answer.
- **Consequence:** AI responses are blocked when no source is bound to the query.
- **Enforced by:** `tests/test_no_source_passport_no_ai.py`.

### 8. No external action without approval — لا فعل خارجي بلا موافقة

- **Statement:** Dealix never sends, charges, publishes, or shares a draft externally without an explicit human approval logged with an approver identity and a timestamp.
- **Consequence:** any attempt to bypass approval is rejected by `decide(action, context)` with `REQUIRE_APPROVAL` or `BLOCK`.
- **Enforced by:** `tests/test_pii_external_requires_approval.py`.

### 9. No agent without identity — لا عميل ذكي بلا هوية

- **Statement:** Dealix never runs an autonomous workflow without a registered agent identity (name, version, owner, governance scope).
- **Consequence:** unregistered agents are rejected at the runtime registry. All actions must trace to an identity.
- **Enforced by:** Wave 4 backlog. Documented in `docs/agent-os` and `auto_client_acquisition/agent_governance`.

### 10. No project without a Proof Pack — لا مشروع بلا Proof Pack

- **Statement:** Dealix never closes a project without assembling a 14-section Proof Pack with a computed proof score.
- **Consequence:** projects without a Proof Pack cannot be invoiced, cannot be referenced in case studies, and cannot trigger retainer eligibility.
- **Enforced by:** `tests/test_proof_pack_required.py`.

### 11. No project without a Capital Asset — لا مشروع بلا أصل رأسمالي

- **Statement:** Dealix never closes a project without depositing at least one reusable capital asset (scoring rule, draft template, governance rule, sector insight, productization signal, or proof example).
- **Consequence:** projects that produce zero capital are flagged in the weekly capital review and treated as a productization failure, not a delivery success.
- **Enforced by:** `auto_client_acquisition/capital_os/capital_ledger.py`.

## How this list changes

The list does not grow casually and does not shrink ever. Adding a rule requires a constitutional amendment PR. Removing a rule is not allowed; it can only be replaced by a stricter rule with the same enforcement coverage.
