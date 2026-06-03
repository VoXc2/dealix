# Dealix — Security, QA & Enterprise Readiness Audit

**Auditor:** Agent #3 (Security + QA + Agent Governance + Enterprise Readiness)
**Date:** 2026-06-03
**Branch:** `claude/compassionate-fermi-gqS6Y`
**Scope:** Full repository hardening after Market, Commercial, Client, Revenue,
Delivery and WhatsApp systems were added.

> **Verdict:** Solid approval-first *business* foundation, but at audit start the
> repo had **no threat model, no untrusted-input policy, no CI workflows, no
> automated tests/evals, and a duplicated governance tree**. This audit + the
> accompanying hardening turn the written policy into an **executable,
> test-enforced safety layer**.

---

## 1. Existing security docs
- ❌ None under `docs/security/` (directory did not exist).
- 🟡 Implicit controls only: `scripts/governance_check.py` (rules G001–G007),
  `company_os/governance/agent_permissions.md` (NEVER/ALWAYS red lines).
- **Action:** created `docs/security/*` threat model, injection boundaries,
  MCP policy, untrusted-input policy, WhatsApp + outbound security models, and
  GitHub Actions policy.

## 2. Existing privacy docs
- 🟢 `company_os/governance/pdpl_checklist.md`, `data_handling_checklist.md`.
- ❌ No retention matrix, data classification, deletion runbook, suppression
  policy, or secret-handling policy under `docs/privacy/`.
- **Action:** created the full `docs/privacy/*` set + `schemas/suppression.schema.json`.

## 3. Existing agent governance docs
- 🟢 `company_os/governance/agent_permissions.md` (Observe/Advise/Draft/Act).
- 🔴 **Conflict:** a *second, divergent* copy exists at
  `company_os/company_os/governance/agent_permissions.md` (different content/levels).
- ❌ No L0–L6 matrix, role catalog, handoff protocol, collision policy, or
  output contract.
- **Action:** created `docs/agents/*` + a code-backed registry
  (`core/safety/permissions.py`, 40 agents) enforced by tests.

## 4. Existing tests / evals
- 🔴 **None.** `npm test` = `vitest run` but there are **zero** test files; no
  Python tests; no evals.
- **Action:** added 22 pytest files (132 tests) + 3 JSONL eval suites + an eval
  runner, all green.

## 5. Existing workflows
- 🔴 **No `.github/` directory at all** — no CI, no security gates.
- **Action:** added 9 least-privilege workflows (`contents: read`, no secrets on
  untrusted triggers, dry-run only).

## 6. Workflows with risky triggers
- N/A at start (none existed). New workflows deliberately avoid
  `pull_request_target` and `issue_comment` tool-execution-with-secrets.

## 7. Workflows with broad permissions
- N/A at start. New workflows pin `permissions: contents: read` (and add
  `pull-requests: write` only where a workflow must comment, with no secrets).

## 8. External-send risk
- 🟢 No code path performs real sends today (drafts only; `outreach_queue.json`
  is `pending_approval`). 🟡 Risk is *latent*: future "send" code must inherit
  the engine gates. Encoded in `core/safety/*` + tests
  (`test_untrusted_input_boundaries.py`, suppression/whatsapp/outreach tests).

## 9. Secrets exposure risk
- 🟢 `.gitignore` ignores `.env*`; `.env.example` holds only placeholder keys
  (`APP_SECRET`, `DATABASE_URL`, Kimi OAuth, `OWNER_UNION_ID`).
- 🟢 `gitleaks`-style scan + GitHub secret-scanning recommended in CI.
- 🟡 No documented secret-handling policy → created
  `docs/privacy/SECRET_HANDLING_POLICY_AR.md` + `docs/infra/SECRETS_MANAGEMENT_POLICY_AR.md`
  and a secret-leak detector in `core/safety/whatsapp.py`.

## 10. Prompt injection risk
- 🔴 No boundary existed. Highest residual risk for an agentic system.
- **Action:** `docs/security/PROMPT_INJECTION_BOUNDARIES.md` +
  `core/safety/untrusted.py` (`treat_as_data_only`, `detect_injection`,
  `can_trigger_external_send`) + tests.

## 11. MCP / tool risk
- 🟡 No MCP server in-repo today, but the session uses GitHub + Notion MCP tools.
- **Action:** `docs/security/MCP_TOOL_RISK_POLICY.md` (allowlist, treat tool
  descriptions as untrusted, no secrets to tools, scope GitHub MCP to `voxc2/dealix`).

## 12. Cold outreach deliverability risk
- 🟡 Templates exist (`scripts/generate_outreach_queue.py`); no SPF/DKIM/DMARC,
  warmup, suppression, or ramp policy.
- **Action:** `docs/outreach/*` readiness checklist + ramp/warmup/bounce policy
  + `reports/outreach/*`; engine enforces unsubscribe + suppression + no purchased lists.

## 13. WhatsApp risk
- 🔴 Templates reference WhatsApp; no consent/secret guardrails.
- **Action:** `docs/whatsapp/*` + `docs/security/WHATSAPP_SECURITY_MODEL.md` +
  `core/safety/whatsapp.py` (post-consent only, no API keys, no key requests) + tests.

## 14. Pricing / payment / legal risk
- 🟢 `approval_queue.json` has `pricing_offer` requiring approval (good).
- 🟡 No code gate. **Action:** `core/safety/commercial.py` (final price needs
  approval, payment handoff needs approval + qualification) + legal handoff
  triggers + tests.

## 15. Missing tests
- Added: claims, personalization threshold, unsubscribe, fake subject,
  suppression, cold-WhatsApp, reply routing, whatsapp secrets/consent, payment,
  proposal mapping/qualification, delivery/CS handoff, renewal, untrusted
  boundaries, agent permissions, schema/data, eval runner.

## 16. Missing schemas
- Added: `suppression`, `vendor`, `legal_review`, `case_study_permission`,
  `productized_service` (+ a dependency-free validator `core/safety/schema_check.py`).

## 17. Duplicate / conflicting agent docs
- 🔴 **`company_os/company_os/`** is a near-complete duplicate of `company_os/`
  with **divergent** governance content and an extra `scripts/` + `payments.csv`.
  This is a real collision/footgun.
- **Action:** documented in `reports/agents/AGENT_GOVERNANCE_REVIEW.md` and
  `docs/agents/AGENT_COLLISION_POLICY_AR.md`. **Not deleted** (manual content I
  didn't author) — flagged for a founder consolidation decision.

## 18. Highest-priority fixes (ranked)
1. **CRITICAL — Unauthenticated approval endpoint.** `api/governance-router.ts`
   `approve` mutation uses `publicQuery` (no auth). Anyone could approve/reject
   AI actions, defeating the entire approval-first model. → make it
   `authedQuery`/`adminQuery`. *(Documented; not changed at runtime — see §19.)*
2. **HIGH — Prompt-injection boundary** (done: engine + docs + tests).
3. **HIGH — No CI safety gates** (done: 9 least-privilege workflows).
4. **HIGH — No tests/evals** (done: 132 tests + evals).
5. **MEDIUM — Duplicate governance tree** (flagged for founder).
6. **MEDIUM — Broken npm scripts:** `package.json` `commercial:*` reference 4
   non-existent `scripts/commercial-*.js`. → create or remove (flagged).
7. **MEDIUM — Deliverability/PDPL/secret policies** (done: docs + schema).

## 19. Files NOT to touch (preserve)
- `api/**`, `db/**`, `src/**` runtime code — **no behavioural changes** in this
  pass (the `publicQuery` auth fix is *recommended* with a ready diff, left for
  founder approval to avoid breaking the running app/frontend).
- `company_os/**` business content — treat as founder-authored data; do not
  delete (including the duplicate tree — flag only).
- `.env*`, any secrets — never edit.
- Existing `scripts/*.py` business generators — left intact.
- Lockfiles / build config (`package-lock.json`, `vite.config.ts`, tsconfig).

## 20. Implementation plan (executed in this pass)
| Phase | Deliverable | Status |
|------|-------------|--------|
| 0 | This audit | ✅ |
| 1 | Agent governance OS (40 agents, registry-as-code) | ✅ |
| 2 | Security threat model + injection/MCP/untrusted/whatsapp/outbound | ✅ |
| 3 | GitHub workflow security review + 9 safe workflows | ✅ |
| 4 | GTM/outreach safety tests + evals | ✅ |
| 5 | WhatsApp/portal/payment/delivery tests + evals | ✅ |
| 6 | Privacy/PDPL guard + suppression schema | ✅ |
| 7 | Deliverability validation docs + reviews | ✅ |
| 8 | Finance / unit-economics QA | ✅ |
| 9 | Enterprise readiness / data room / procurement | ✅ |
| 10 | Infra / reliability review | ✅ |
| 11 | Saudi localization review | ✅ |
| 12 | Productized services review | ✅ |
| 13 | Final super reports | ✅ |
| 14 | Verification (pytest, schema/YAML/JSON, workflow lint) | ✅ |

**Net:** policy → **executable, test-enforced** safety. Residual top risk is the
unauthenticated approval endpoint (founder fix), the duplicate tree, and broken
`commercial:*` npm scripts.
