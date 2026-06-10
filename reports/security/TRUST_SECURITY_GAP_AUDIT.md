# Dealix Trust & Security Gap Audit
**Agent #5 — Security Red Team**
**Date:** 2026-06-03
**Repository:** https://github.com/Dealix-sa/dealix

---

## Executive Summary

This audit establishes the current state of Dealix's trust, safety, and security posture. The repository has a solid foundation in several areas (WhatsApp consent, governance OS, SSRF guard, deliverability checks, no-cold-whatsapp rule), but has critical gaps in prompt injection defense, GitHub Actions permissions, MCP tooling security, and comprehensive eval datasets.

**Overall Posture:** FOUNDATION PRESENT — HARDENING NEEDED

---

## 1. Existing Security Docs

| Doc | Status | Notes |
|-----|--------|-------|
| `docs/SECURITY_RUNBOOK.md` | Basic | Incident response for secret exposure, P1/P2 escalation. Needs expansion. |
| `docs/security/key_rotation_log.md` | Basic | Key rotation tracking template. |
| `docs/security/KEY_ROTATION.md` | Basic | Rotation procedures. |
| `docs/security/RATE_LIMITS.md` | Basic | Rate limit doc. |
| `docs/security/CORS_POLICY.md` | Basic | CORS policy. |
| `docs/security/OWASP_API_SECURITY_ACTION_PLAN_AR.md` | Basic | Arabic OWASP alignment. |
| `docs/security/` (dedicated dir) | Sparse | Needs comprehensive TRUSST_SAFETY_OS_AR.md |

**Gaps:** No comprehensive TRUST_SAFETY_OS_AR.md, no AGENTIC_WORKFLOW_THREAT_MODEL, no PROMPT_INJECTION_BOUNDARIES doc.

---

## 2. Existing Privacy Docs

| Doc | Status | Notes |
|-----|--------|-------|
| `docs/wave8/DPA_CHECKLIST_AR_EN.md` | Draft | Pre-signing DPA checklist, lawyer review required. |
| `docs/wave8/WHATSAPP_CONSENT_CHECKLIST_AR_EN.md` | Basic | Consent checklist. |
| `docs/wave8/DSR_REQUEST_TEMPLATE.md` | Basic | Data subject request template. |
| `docs/wave8/CONSENT_RECORD_TEMPLATE.json` | Basic | Consent record schema. |
| `docs/privacy/` (dedicated dir) | **MISSING** | Needs comprehensive PRIVACY_GUARD_OS_AR.md |

**Gaps:** No dedicated privacy directory. No PDPL operational guard. No data minimization policy. No retention/deletion policy. No PII redaction policy doc.

---

## 3. Existing Agent Governance Docs

| Doc | Status | Notes |
|-----|--------|-------|
| `os/02_AGENTS.md` | Good | 16 agents defined with purpose, inputs, outputs, approval requirements. Interaction rules. |
| `AGENTS.md` | Good | Primary repo guidance. Security runbook link. |

**Gaps:** No AGENT_PERMISSION_SECURITY_AR.md. No AGENT_COLLISION_SECURITY_POLICY_AR.md. No agent output contract spec. No permission matrix.

---

## 4. Existing Trust Gates

### 4.1 Governance OS (auto_client_acquisition/governance_os/)

| Gate | Implementation | Status |
|------|---------------|--------|
| No cold WhatsApp | `forbidden_actions.py`, `rules/no_cold_whatsapp.py`, `draft_gate.py` | ✅ Present |
| No LinkedIn automation | `forbidden_actions.py`, `rules/no_linkedin_automation.py` | ✅ Present |
| No scraping | `rules/no_scraping.py` | ✅ Present |
| Claim safety | `claim_safety.py` | ✅ Present |
| Approval matrix | `approval_matrix.py` | ✅ Present |
| Draft gate | `draft_gate.py` | ✅ Present |
| Workflow control | `workflow_control_registry.py` | ✅ Present |
| Channel policy | `channel_policy.py` | ✅ Present |
| External action requires approval | `rules/external_action_requires_approval.py` | ✅ Present |
| PII requires review | `rules/pii_requires_review.py` | ✅ Present |
| No guaranteed claims | `rules/no_guaranteed_claims.py` | ✅ Present |

**Assessment:** Solid governance OS foundation. Evidence: `governance/__init__.py` exposes all gates via clean API.

### 4.2 Security Tests

| Test | Coverage | Status |
|------|----------|--------|
| `test_engine12_security_v1.py` | SSRF guard (8 tests) + Email deliverability (8 tests) | ✅ Strong |
| `test_v7_prompt_injection_resistance.py` | WorkforceGoal injection block, redact_text, apply_policy | ✅ Present |
| `test_no_cold_whatsapp.py` | Cold WhatsApp policy check | ✅ Basic |
| `test_billing_moyasar_safety.py` | No secrets in pricing module | ✅ Present |
| `test_whatsapp_*` (multiple) | WhatsApp signature, safe send, policy, decision layer | ✅ Present |
| WhatsApp consent tests | N/A | ✅ In docs |

**Gaps:** No tests for outbound unsubscribe enforcement, suppression blocking, guaranteed claims, cold WhatsApp automation, approval requirement, prompt injection in email/GitHub/com CRM.

### 4.3 API Security

| Component | Status | Notes |
|-----------|--------|-------|
| SSRF Guard | ✅ `api/security/ssrf_guard.py` | Blocks 8 internal-IP patterns + cloud metadata + non-approved domains |
| Moyasar payment safety | ✅ `test_billing_moyasar_safety.py` | No secrets in module |
| WhatsApp webhook signature | ✅ `test_whatsapp_signature.py` | Signature verification |
| `WHATSAPP_ALLOW_LIVE_SEND=false` | ✅ Default | Production default is dry-run |

**Gaps:** No dedicated secrets handling policy. No API key in WhatsApp test. No prompt injection firewall.

---

## 5. Existing Tests

**Existing test coverage areas:**
- WhatsApp: signature, safe send, policy, decision layer, full ops, cards, webhook
- Security: SSRF guard, email deliverability, prompt injection resistance, Moyasar safety
- Cold WhatsApp: governance check
- No dedicated: outbound unsubscribe, suppression, guaranteed claims, pricing approval, contract terms, PII redaction

---

## 6. Existing GitHub Workflows and Permissions

### 6.1 Workflow Inventory (55+ workflows)

| Workflow | Permissions | Classification |
|----------|-------------|----------------|
| `security.yml` | `contents: read`, `security-events: write`, `pull-requests: read` | ✅ SAFE |
| `repository-hardening.yml` | `contents: read`, `security-events: write` | ✅ SAFE |
| `founder_commercial_daily.yml` | `contents: read` | ✅ SAFE |
| `governed-full-ops-daily.yml` | `contents: read` | ✅ SAFE |
| `hermes-revenue-growth-os.yml` | `contents: read` | ✅ SAFE |
| `railway_deploy.yml` | ? | ⚠️ NEEDS_REVIEW |
| `railway_deploy_frontend.yml` | ? | ⚠️ NEEDS_REVIEW |
| `deploy.yml` | ? | ⚠️ HIGH_RISK |
| `release.yml` | ? | ⚠️ NEEDS_REVIEW |
| `production-smoke.yml` | ? | ⚠️ NEEDS_REVIEW |
| `production_api_trust_smoke.yml` | ? | ⚠️ NEEDS_REVIEW |
| `release-please.yml` | ? | ⚠️ NEEDS_REVIEW |
| `codeql.yml` | `contents: read`, `security-events: write` | ✅ SAFE |
| `local_stack_verify.yml` | ? | ✅ Likely SAFE |
| `staging-smoke.yml` | ? | ⚠️ NEEDS_REVIEW |

**Critical findings:**
1. Many workflows have undocumented permissions — full audit needed.
2. No `agentic-security-gate.yml` exists.
3. No workflow that checks for `pull_request_target`, `issue_comment` triggers, or broad permissions.
4. No gate that blocks production deploy from PRs.
5. No workflow that flags untrusted event text being passed to AI agents.
6. `repository-hardening.yml` runs gitleaks + trivy — good.
7. `security.yml` has CodeQL + dependency review — good.

---

## 7. Existing MCP/Tooling Surfaces

### 7.1 MCP Server

| Tool | Write? | External Send? | Approval Required? |
|------|--------|---------------|-------------------|
| `get_war_room_today` | No | No | No |
| `get_kpi_snapshot` | No | No | No |
| `get_business_now` | No | No | No |
| `get_commercial_strategy` | No | No | No |
| `get_doctrine_rules` | No | No | No |
| `get_founder_cockpit` | No | No | No |
| `get_expansion_status` | No | No | No |
| `get_outreach_drafts` | No | No | No |
| `get_evidence_summary` | No | No | No |
| `get_commercial_digest` | No | No | No |
| `get_ceo_master_plan_status` | No | No | No |
| `get_platform_kpi_baselines` | No | No | No |
| `get_todo_registry` | No | No | No |
| `get_risk_register` | No | No | No |
| `get_targeting_pool` | No | No | No |
| `get_social_content_queue` | No | No | No |
| `get_company_policy` | No | No | No |
| `get_war_room_lead_stages` | No | No | No |
| `draft_warm_intro` | Draft only | No | Yes |
| `run_diagnostic_report` | Draft only | No | Yes |

**Assessment:** MCP server is well-designed. Read tools are safe. Write tools produce drafts only. Doctrine enforced. No external send tools exposed.

**Gaps:** No documented tool permission matrix. No tool poisoning threat model. No tool input/output firewall spec. No policy against using tool descriptions as instructions.

---

## 8. Existing WhatsApp/Webhook Surfaces

### 8.1 WhatsApp OS

| Component | Status |
|-----------|--------|
| `docs/whatsapp/WHATSAPP_CLIENT_OS_AR.md` | ✅ Comprehensive — consent, safety rules, human handoff, card types |
| `docs/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md` | ✅ Post-reply decision tree, consent request |
| `docs/whatsapp/WHATSAPP_OPERATOR_FLOW.md` | ✅ Design for buttons, no cold WhatsApp |
| `docs/wave8/WHATSAPP_CONSENT_CHECKLIST_AR_EN.md` | ✅ Consent checklist |
| `WHATSAPP_ALLOW_LIVE_SEND=false` | ✅ Default |
| Human handoff triggers | ✅ Defined (pricing, legal, complaints, deletion, etc.) |
| No API keys in WhatsApp | ✅ Rule stated |
| Action cards with risk/evidence | ✅ Card structure defined |

**Gaps:** No dedicated WHATSAPP_SAFETY_POLICY_AR.md doc. No WhatsApp secret handling policy doc. No WhatsApp human handoff safety doc. No test for API key in WhatsApp text. No test for WhatsApp action card risk requirement.

---

## 9. Existing Outreach/Cold Email Surfaces

| Component | Status |
|-----------|--------|
| `draft_gate.py` | ✅ Blocks scraping, purchased list, cold WhatsApp, LinkedIn automation, auto-send |
| `claim_safety.py` | ✅ Blocks guaranteed claims, fake proof |
| `approval_matrix.py` | ✅ Routes WhatsApp/LinkedIn to high-risk |
| Email deliverability check | ✅ SPF, DKIM, DMARC, unsubscribe check |
| No fake Re:/Fwd: | Not explicitly tested |
| Unsubscribe in cold email | ⚠️ Only checked via deliverability, not in draft gate |
| Suppression enforcement | ⚠️ No dedicated suppression enforcement doc |

**Gaps:** No OUTBOUND_SAFETY_POLICY_AR.md. No COLD_EMAIL_TRUST_GATE_AR.md. No DELIVERABILITY_SAFETY_GATE_AR.md. No SUPPRESSION_ENFORCEMENT_POLICY_AR.md. No tests for missing unsubscribe, suppression blocking, fake reply subject, guaranteed claims.

---

## 10. Existing Secret-Handling Patterns

| Pattern | Status |
|---------|--------|
| `.env` only | ✅ Documented |
| `SecretStr` usage | ✅ Documented |
| gitleaks pre-commit | ✅ In repository-hardening.yml |
| detect-secrets | ✅ In security target |
| No PAT in pricing module | ✅ `test_billing_moyasar_safety.py` |
| OIDC for cloud | ⚠️ Not documented |
| No secrets in logs | ⚠️ Not enforced in code |
| No secrets in prompts | ⚠️ No dedicated policy |
| No secrets in reports | ⚠️ No dedicated policy |

**Gaps:** No SECRETS_HANDLING_POLICY.md. No policy on secrets in prompts/logs/reports/JSONL.

---

## 11. Prompt Injection Risks

### 11.1 Known Injection Paths

| Path | Risk Level | Current Defense |
|------|------------|----------------|
| Website content scraped by agents | HIGH | None — data, not instructions policy needed |
| Email body in agent context | HIGH | None — need INPUT FIREWALL |
| GitHub issue/PR comment text | HIGH | None — UNTRUSTED_GITHUB_EVENT_POLICY needed |
| CRM notes/fields | HIGH | None |
| Uploaded files (CSV, JSON, etc.) | HIGH | `test_v7_prompt_injection_resistance.py` tests redact_text |
| WhatsApp user messages | MEDIUM | None in agent context |
| Tool output from external sources | HIGH | None |
| Tool descriptions | LOW | Implicit — not trusted as instructions |

### 11.2 Existing Prompt Injection Tests

- `test_v7_prompt_injection_resistance.py`: 3 tests covering WorkforceGoal injection, redact_text phone redaction, apply_policy block
- **Assessment:** Good start but incomplete. No tests for website, email, GitHub comment, WhatsApp message, CRM note, uploaded file injection.

### 11.3 Missing Defenses

| Defense | Status |
|---------|--------|
| Prompt boundary template | ❌ Missing |
| Context sanitization policy | ❌ Missing |
| Tool input firewall | ❌ Missing |
| Tool output firewall | ❌ Missing |
| Untrusted content summarization | ❌ Missing |
| Indirect prompt injection runbook | ❌ Missing |
| PROMPT_INJECTION_DEFENSE_AR.md | ❌ Missing |

---

## 12. Untrusted Input Paths

| Input Source | Classification | Current Handling |
|--------------|---------------|------------------|
| Website content | UNTRUSTED | None — needs summarization as data |
| Email bodies | UNTRUSTED | None — needs INPUT FIREWALL |
| GitHub issues | UNTRUSTED | None |
| GitHub PR descriptions | UNTRUSTED | None |
| GitHub comments | UNTRUSTED | None |
| CRM notes | UNTRUSTED | None |
| Uploaded files | UNTRUSTED | Partially (redact_text) |
| WhatsApp messages | UNTRUSTED | None in agent context |
| Search results | UNTRUSTED | None |
| Customer reviews | UNTRUSTED | None |
| Scraped pages | UNTRUSTED | Forbidden (no_scraping.py) |

**Missing:** UNTRUSTED_INPUT_POLICY.md, TOOL_INPUT_OUTPUT_FIREWALL_POLICY.md, UNTRUSTED_CONTENT_SUMMARIZATION_POLICY.md

---

## 13. PII Leakage Risks

| Risk | Status |
|------|--------|
| `redact_text` in PII redaction | ✅ Covered by test |
| No PII in prompts without approval | ⚠️ Not enforced |
| PII redaction in reports | ⚠️ No policy |
| Consent records | ✅ `CONSENT_RECORD_TEMPLATE.json` |
| DSR template | ✅ `DSR_REQUEST_TEMPLATE.md` |

**Missing:** PII_REDACTION_POLICY_AR.md, tests for no_secrets_in_reports, privacy_event schema, data_subject_request schema.

---

## 14. External Action Risks

| Action | Current Gate | Status |
|--------|-------------|--------|
| External email send | Approval matrix | ✅ Present |
| WhatsApp send | No cold + consent + WHATSAPP_ALLOW_LIVE_SEND=false | ✅ Present |
| LinkedIn automation | Forbidden | ✅ Present |
| Scraping | Forbidden | ✅ Present |
| External API calls | SSRF guard | ✅ Present |
| Production deploy | ⚠️ No gate in CI | ❌ Missing |
| Workflow write (PR) | ⚠️ No gate | ❌ Missing |
| Payment link generation | ⚠️ No approval gate in workflow | ❌ Missing |

**Missing:** EXTERNAL_ACTION_APPROVAL_POLICY.md, agentic-security-gate.yml

---

## 15. Missing Tests

| Test | Priority |
|------|----------|
| `test_outbound_no_fake_reply_subject.py` | HIGH |
| `test_outbound_unsubscribe_required.py` | HIGH |
| `test_outbound_suppression_blocks_send.py` | HIGH |
| `test_outbound_no_guaranteed_claims.py` | HIGH |
| `test_outbound_no_cold_whatsapp.py` | HIGH |
| `test_outbound_requires_approval.py` | HIGH |
| `test_whatsapp_post_consent_only.py` | HIGH |
| `test_whatsapp_no_api_keys_in_text.py` | HIGH |
| `test_whatsapp_handoff_for_sensitive_topics.py` | HIGH |
| `test_whatsapp_action_card_requires_risk.py` | HIGH |
| `test_no_secrets_in_reports.py` | HIGH |
| `test_privacy_event_schema.py` | MEDIUM |
| `test_data_subject_request_required_fields.py` | MEDIUM |
| `test_pii_redaction_policy.py` | MEDIUM |
| `test_no_guaranteed_revenue_claims.py` | HIGH |
| `test_case_study_requires_truth_label.py` | MEDIUM |
| `test_commercial_claim_requires_evidence.py` | MEDIUM |
| `test_pricing_commitment_requires_approval.py` | HIGH |
| `test_payment_handoff_requires_approval.py` | HIGH |
| `test_pricing_requires_founder_approval.py` | HIGH |
| `test_contract_terms_require_handoff.py` | HIGH |
| `test_discount_guardrails.py` | MEDIUM |
| `test_agent_cannot_send_external.py` | HIGH |
| `test_agent_cannot_modify_secrets.py` | HIGH |
| `test_agent_output_contract_required.py` | MEDIUM |
| `test_agent_permission_matrix.py` | MEDIUM |
| `test_agent_collision_policy.py` | MEDIUM |

---

## 16. Missing Gates

| Gate | Priority |
|------|----------|
| Prompt injection boundary template in all agent prompts | HIGH |
| Tool input firewall (block untrusted instructions) | HIGH |
| Tool output firewall (mark external content as untrusted) | HIGH |
| GitHub Actions security gate workflow | HIGH |
| Production deploy requires approval | HIGH |
| No `pull_request_target` with write token | HIGH |
| No `issue_comment` tool execution | HIGH |
| WhatsApp action card requires risk_level | HIGH |
| External send requires dry_run=true | HIGH |
| Approval gate for pricing/payment/legal | HIGH |
| No secrets in prompts/logs/reports | HIGH |
| Suppression enforcement gate | MEDIUM |
| Agent output contract enforcement | MEDIUM |

---

## 17. Highest-Priority Fixes

### Tier 1 — CRITICAL (Do First)

1. **Create `agentic-security-gate.yml`** — Block production deploy, broad permissions, unsafe triggers
2. **Create `PROMPT_INJECTION_DEFENSE_AR.md`** — Document boundary rules
3. **Create `UNTRUSTED_INPUT_POLICY.md`** — Classify all input sources
4. **Create `TOOL_INPUT_OUTPUT_FIREWALL_POLICY.md`** — Block injection via tools
5. **Create `GITHUB_WORKFLOW_PERMISSION_POLICY.md`** — Audit all workflows
6. **Add outbound safety tests** — Unsubscribe, suppression, no guaranteed claims, approval required
7. **Create `WHATSAPP_SAFETY_POLICY_AR.md`** — Consolidate WhatsApp safety rules
8. **Create `PRIVACY_GUARD_OS_AR.md`** — Saudi PDPL operational guard

### Tier 2 — HIGH (Do Second)

9. Create `SECRETS_HANDLING_POLICY.md`
10. Create `BUSINESS_CLAIMS_SAFETY_POLICY_AR.md`
11. Create `PAYMENT_HANDOFF_SECURITY_POLICY.md`
12. Create `AGENT_PERMISSION_SECURITY_AR.md`
13. Add WhatsApp safety tests (API key in text, handoff, consent)
14. Create security eval datasets
15. Create incident response runbooks

### Tier 3 — MEDIUM (Do Third)

16. Create `MCP_SECURITY_POLICY.md`
17. Create `INDIRECT_PROMPT_INJECTION_RUNBOOK.md`
18. Create `OUTBOUND_INCIDENT_RESPONSE_AR.md`
19. Create daily/weekly security report templates
20. Add agent permission/collision tests

---

## 18. Implementation Order

### Phase 1: Trust & Safety Architecture
1. `TRUST_SECURITY_GAP_AUDIT.md` ← This document
2. `docs/security/TRUST_SAFETY_OS_AR.md`
3. `docs/security/AGENTIC_WORKFLOW_THREAT_MODEL.md`
4. `docs/security/PROMPT_INJECTION_BOUNDARIES.md`
5. `docs/security/UNTRUSTED_INPUT_POLICY.md`
6. `docs/security/TOOL_USE_SECURITY_POLICY.md`
7. `docs/security/MCP_TOOL_RISK_POLICY.md`
8. `docs/security/EXTERNAL_ACTION_APPROVAL_POLICY.md`
9. `docs/security/SECRETS_HANDLING_POLICY.md`
10. `docs/security/SECURITY_ESCALATION_MATRIX.md`
11. `reports/security/TRUST_SAFETY_ARCHITECTURE_MAP.md`

### Phase 2: Prompt Injection Defense
12. `docs/security/PROMPT_INJECTION_DEFENSE_AR.md`
13. `docs/security/INDIRECT_PROMPT_INJECTION_RUNBOOK.md`
14. `docs/security/CONTEXT_SANITIZATION_POLICY.md`
15. `docs/security/TOOL_INPUT_OUTPUT_FIREWALL_POLICY.md`
16. `docs/security/UNTRUSTED_CONTENT_SUMMARIZATION_POLICY.md`
17. `schemas/security_event.schema.json`
18. `schemas/prompt_injection_case.schema.json`
19. `data/security/prompt_injection_cases.jsonl`
20. `reports/security/PROMPT_INJECTION_RISK_REVIEW.md`

### Phase 3: GitHub Actions Security
21. `docs/security/GITHUB_ACTIONS_SECURITY_POLICY.md`
22. `docs/security/GITHUB_WORKFLOW_PERMISSION_POLICY.md`
23. `docs/security/UNTRUSTED_GITHUB_EVENT_POLICY.md`
24. `docs/security/OIDC_AND_SECRET_POLICY.md`
25. `reports/security/GITHUB_ACTIONS_SECURITY_REVIEW.md`
26. `.github/workflows/agentic-security-gate.yml`

### Phase 4-15: (See detailed phases in main task)
→ See full implementation plan in mission document

---

## Summary Findings

**Existing strengths:**
- Solid governance OS with 11 rule modules
- WhatsApp safety well-documented (consent, no cold, human handoff, cards)
- SSRF guard + email deliverability check (tested)
- Prompt injection resistance tests (partial)
- No-cold-whatsapp enforcement
- MCP server doctrine enforcement
- `WHATSAPP_ALLOW_LIVE_SEND=false` default
- GitHub Actions: `security.yml`, `repository-hardening.yml` with gitleaks/trivy

**Critical gaps:**
- No agentic-security-gate.yml workflow
- No comprehensive prompt injection boundary template
- No tool input/output firewall policy
- No GitHub workflow permission policy/audit
- No outbound safety gate tests (unsubscribe, suppression, approval)
- No WhatsApp API key test
- No pricing/payment/contract approval gate tests
- No comprehensive privacy/PDPL guard docs
- No security eval datasets
- No incident response runbooks

**Non-negotiables confirmed enforced:**
✅ No cold WhatsApp automation
✅ No LinkedIn automation
✅ No scraping that violates terms
✅ No purchased lists in governance
✅ No auto-send without approval
✅ No guaranteed revenue claims (partial)
✅ SSRF guard on external URLs
✅ MCP write tools = draft only
✅ WhatsApp default = dry run

**Non-negotiables needing enforcement:**
❌ Missing unsubscribe in cold email (needs test + gate)
❌ No production deploy gate
❌ No GitHub Actions permission audit
❌ No prompt injection boundary in agent prompts
❌ No tool input firewall
❌ No suppression enforcement gate

---

*Audit completed by Agent #5 — Dealix Security Red Team*
*Next action: Proceed to Phase 1 implementation*
