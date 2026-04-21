# Dealix — QA & Acceptance Checklist

**Purpose:** End-to-end, reproducible verification that Dealix is safe to put in front of a paying Saudi customer. Run before every pilot kickoff, and after every non-trivial deploy.

**How to run:**
```bash
# 1. Automated smoke
BASE_URL=https://api.dealix.example  bash scripts/qa/smoke_test.sh

# 2. Manual checklist
# Work through §1–§12 below. Mark each item [x]. Record result in docs/reality_reviews/YYYY-MM-DD.md.
```

Assume a clean staging tenant with seed data (`make seed`).

---

## 1. Environment sanity (30 s)

- [ ] `curl -sf $BASE_URL/api/v1/health` returns `200` and JSON with `status: "ok"`.
- [ ] `curl -sf $BASE_URL/api/v1/health/db` reports DB reachable.
- [ ] `curl -sf $BASE_URL/api/v1/health/redis` reports Redis reachable.
- [ ] Frontend loads at `/` in < 2 s, RTL layout visible (`dir="rtl"`).
- [ ] No console errors on first page load (inspect DevTools).

## 2. Auth & tenant isolation

- [ ] `POST /api/v1/auth/register` creates a new tenant + admin user.
- [ ] `POST /api/v1/auth/login` returns a JWT. Token contains `tenant_id`.
- [ ] Token from Tenant A **cannot** read leads of Tenant B (try `GET /api/v1/leads/{B_lead_id}` → expect 403/404).
- [ ] Expired token is rejected.
- [ ] Password reset flow sends email (sandbox) and accepts new password.
- [ ] Logout invalidates refresh token.

## 3. Data privacy / PDPL

- [ ] New tenant has `pdpl_consent_default = false`.
- [ ] Attempting to send outbound WhatsApp to a contact without consent returns 4xx with PDPL error code.
- [ ] Soft-delete a lead → record remains in DB with `deleted_at` set, is hidden from APIs.
- [ ] No PII (email, phone, national ID) appears in application logs — grep last 1000 lines of backend log.

## 4. Leads & prospect analysis

- [ ] `POST /api/v1/leads/` with minimal payload creates a lead.
- [ ] Lead appears in `GET /api/v1/leads/` for same tenant.
- [ ] `POST /api/v1/lead-prospector/analyze` returns a `LeadScoreCard` with: score (0–100), tier, next_action, reasoning (AR).
- [ ] Score is deterministic for the same input across 2 runs (tolerance ±5 if stochastic LLM used).
- [ ] Arabic name (e.g. `"أحمد الشمري"`) is preserved, not mangled to latin.

## 5. Arabic & English outputs

- [ ] `/api/v1/ai-agents/summarize` with Arabic input returns Arabic output.
- [ ] Same endpoint with English input returns English output.
- [ ] No mixing (AR prompt → unexpected English reply, or vice versa).
- [ ] RTL punctuation correct: Arabic comma `،`, question mark `؟`.
- [ ] Numbers render with Arabic-Indic numerals only where the UI explicitly requests it (Western numerals are the default; confirm in dashboard screens).

## 6. Local AI (Ollama) layer

- [ ] `GET /api/v1/local-ai/status` → `{"enabled": true, "daemon_up": true, "tier": "small"}` on specced server.
- [ ] `GET /api/v1/local-ai/catalog` lists at least `qwen2.5:0.5b` and `qwen2.5:3b-instruct`.
- [ ] `POST /api/v1/local-ai/chat` with `{"task": "arabic_summarization", "prompt": "لخّص النص التالي..."}` returns a non-empty Arabic response in < 10 s.
- [ ] `POST /api/v1/local-ai/health-check` reports each configured model as reachable.
- [ ] `GET /api/v1/local-ai/tasks` returns task routing table.

### 6.1 Fallback behaviour
- [ ] Stop Ollama (`sudo systemctl stop ollama`). `POST /api/v1/ai-agents/summarize` still succeeds using Groq.
- [ ] Remove `GROQ_API_KEY` from env + restart backend. With Ollama running, summarization still succeeds via local.
- [ ] Remove both → endpoint returns a clean 503 with message `"no_llm_available"`. No stack trace leaked.
- [ ] Restore Ollama + Groq key.

## 7. Agent system

- [ ] `POST /api/v1/agent-system/dispatch` with event `"new_lead"` routes to the prospecting agent.
- [ ] Each of the 8 roles (prospector, qualifier, proposer, closer, onboarder, retention, compliance, analytics) responds with a structured output matching its schema.
- [ ] Retry: inject a 500 from downstream (e.g. Arabic NLP). Agent retries ≤ 2x then escalates to `approval_center` queue.
- [ ] `GET /api/v1/approval-center/` shows the escalated item with correct category.

## 8. Dashboards

- [ ] `/dashboard` loads < 2 s on a tenant with 1k leads.
- [ ] KPI cards (pipeline value, MRR, active deals) match raw DB counts within ±1%.
- [ ] "Sample" badge shows on widgets reading from `data/` seeds (per Launch Plan §1.1).
- [ ] Drill-down: click a KPI → filtered list opens, URL is shareable, deep link works on reload.
- [ ] Executive Room (`/api/v1/executive-room/snapshot`) returns 200 with a non-empty snapshot.

## 9. PDPL consent flows

- [ ] Onboarding wizard requires consent-template selection before the first outbound channel is enabled.
- [ ] `POST /api/v1/consents/` records consent with timestamp + source.
- [ ] Revoking consent (`DELETE /api/v1/consents/{id}`) blocks subsequent sends to that contact within 60 s.
- [ ] Audit log entry written for every consent state change.

## 10. Pricing / billing (Moyasar sandbox)

- [ ] Plans load from `/api/v1/pricing` with SAR amounts.
- [ ] Sandbox checkout with Moyasar test card `4111 1111 1111 1111` succeeds.
- [ ] Successful charge creates a `subscription` row and sends a welcome email.
- [ ] Failed card returns localised error (AR) and does not create a subscription.
- [ ] Switch to production keys only after stepping through §10 end-to-end twice in a row without errors.

## 11. Performance

- [ ] Homepage TTFB < 500 ms from Riyadh (test: `curl -o /dev/null -s -w '%{time_starttransfer}\n'`).
- [ ] Backend p95 response < 500 ms for read endpoints, < 2 s for LLM-backed endpoints (Groq), < 10 s for local AI on this server.
- [ ] 100-lead bulk import completes in < 30 s.
- [ ] Memory: `docker stats` shows backend < 1.5 GiB, postgres < 1 GiB, ollama < 4 GiB at rest.

## 12. Error handling & UX

- [ ] 404 page renders in AR with a "العودة للرئيسية" button.
- [ ] 500 surface: shows a generic message, logs contain the trace id, and the same trace id is shown to the user.
- [ ] Slow network (throttle to 3G in DevTools): skeletons / spinners render; no white screen.
- [ ] Form validation errors render under the correct field in Arabic.

---

## 13. Regression matrix (per release)

| Scenario | AR | EN | Mobile | Desktop |
|---|---|---|---|---|
| Login | [ ] | [ ] | [ ] | [ ] |
| Create lead | [ ] | [ ] | [ ] | [ ] |
| Analyze lead | [ ] | [ ] | [ ] | [ ] |
| Dashboard load | [ ] | [ ] | [ ] | [ ] |
| Send WhatsApp (with consent) | [ ] | [ ] | [ ] | [ ] |
| Checkout (sandbox) | [ ] | [ ] | [ ] | [ ] |

One full column ticked per deploy minimum.

---

## 14. Sign-off

```
Release tag:       ____________________
Environment:       ☐ staging  ☐ prod
Smoke script:      ☐ all green
Manual checklist:  ☐ all green  or  ☐ exceptions documented below
Tester:            ____________________
Date (YYYY-MM-DD): ____________________
```

Exceptions / known issues (must be acceptable to the founder before deploy):
- …
- …
