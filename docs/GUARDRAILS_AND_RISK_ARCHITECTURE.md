# Dealix Guardrails & Risk Architecture

> NIST AI RMF–shaped: every external action passes through nine checks.
> The default for unknown is BLOCKED; the default for known-safe is
> APPROVAL_REQUIRED. APPROVED_EXECUTE is reachable only after a human
> approves the specific action in writing (or via an approvals endpoint).

## Action modes (canonical)

| Mode | Meaning | Examples |
| --- | --- | --- |
| `suggest_only` | Internal idea; no draft yet | "consider running a Saudi clinics campaign next week" |
| `draft_only` | Concrete artifact created, not sent | a saved Arabic message draft |
| `approval_required` | Draft + human approval pending | message queued for Sami's approval |
| `approved_execute` | Sent after human approval | only after explicit approval log |
| `blocked` | Refused by a guardrail | cold WhatsApp on purchased numbers |

## The 9-step gate

1. **Identity / context check** — `RequestIDMiddleware` + caller identity.
2. **Consent check** — `compliance/check-outreach` reads `SuppressionRecord` + `contact_opt_out`.
3. **Channel policy check** — `channels/policy` + `revenue-os/compliance/contactability`.
4. **Claim safety check** — `tests/test_no_guaranteed_claims.py` sweep + classifier reasons never include "guaranteed".
5. **Role permission check** — role brief routing (deploy branch's `role-briefs`).
6. **Approval state check** — `approvals/pending`, `approvals/{id}/decide`.
7. **Tool availability check** — `WHATSAPP_ALLOW_LIVE_SEND`, `gmail_configured()`, `MOYASAR_SECRET_KEY`.
8. **Audit log write** — `request_completed` structured log + `observability/unsafe/record`.
9. **Proof event mapping** — `proof-ledger/events` for revenue-impacting outcomes.

## Always-blocked actions (floor)

```
cold_whatsapp
purchased_list_whatsapp
scraped_lists_whatsapp
linkedin_automation
live_gmail_without_approval
moyasar_live_charge_without_flag
auto_call_without_permission
guaranteed_revenue_claim
post_opt_out_contact
missing_consent_direct_marketing
```

These are enforced in two places so a single edit cannot reopen the floor:
1. `auto_client_acquisition/safety/intent_classifier.py` — blocks at intent.
2. `auto_client_acquisition/customer_ops/company_brain.py` — `_ALWAYS_BLOCKED_CHANNELS` floor in every brain payload.

## Blocked-decision response shape

Every blocked decision returns:

```
{
  "intent": "cold_or_blast_outreach_request",
  "action_mode": "blocked",
  "blocked": true,
  "language": "ar|en|mixed",
  "recommended_bundle": null,
  "blocked_reasons": ["cold_or_blast_whatsapp", ...],
  "safe_alternatives": [
    "linkedin_manual_warm_intro",
    "inbound_wa_me_link",
    "opt_in_form",
    "email_draft_with_approval",
    "customer_initiated_whatsapp"
  ],
  "reason_ar": "هذا الطلب غير آمن: ...",
  "reason_en": "This request is not safe: ...",
  "requires_intake": false
}
```

## Risk classes covered

| Risk | Class | Test |
| --- | --- | --- |
| Saudi PDPL — direct marketing without consent | unauthorized contact | `test_whatsapp_policy.py` |
| Meta WhatsApp policy — cold/bulk send | platform violation | same |
| Hallucinated guaranteed outcomes | misrepresentation | `test_no_guaranteed_claims.py` |
| Live charge before customer agreed | financial harm | `test_live_gates_default_false.py` |
| Auto-DM bot on customers | privacy + platform violation | `test_operator_saudi_safety.py` |
| Forgetting opt-out | re-contact harm | `compliance/check-outreach` integration test |
| Unsigned webhook acceptance | impersonation | live 401 verified on prod |

## Enforcement responsibility

| Owner | Action |
| --- | --- |
| Developer | Run pytest before push; never bypass `BLOCKED` decisions in code. |
| Founder | Never set `WHATSAPP_ALLOW_LIVE_SEND=true` on prod without a documented opt-in registry. |
| Founder | Never share Moyasar live key into Railway prod env until paid-beta gates have a written policy. |
| Reviewer | Reject PRs that add a public route bypassing `compliance/check-outreach` for outbound. |
