# Dealix — Launch Execution Plan

**Owner:** Founder / Revenue Ops
**Last updated:** 2026-04-21
**Scope:** Everything required to move Dealix from "feature-complete repo" to "paid Saudi customers using it daily."
**Status at time of writing:** PR #16 (local AI / Ollama integration) open. Phase Gate (per `CLAUDE.md` §2) NOT green — 0 paying customers.

This document is the single operational plan. Treat every section as a checklist: items are either **DONE**, **IN PROGRESS**, or **TODO**. Track them in `docs/launch-execution-plan.md` itself — do not fork copies.

---

## 0. Guardrails (read before executing anything)

Per `CLAUDE.md` the project is in **Discovery Phase**. Before Phase Gate goes green:

- No Wave A/B/C/D/E roadmap work from `DEALIX_PHASE2_BLUEPRINT.md`.
- Every change ties to a documented customer interview (`docs/customer_learnings/`) or a security finding.
- No bulk outreach without PDPL consent (see §6).

Phase Gate unlocks when **all** are true:
1. 3+ signed, paid pilot agreements.
2. 2+ pilots in active daily use ≥ 30 days.
3. Pentest engagement done; no open Criticals.
4. Truth Registry audit (V005): 100% SUPPORTED.
5. Pilot NPS ≥ 30.
6. 1+ named reference customer.

**This launch plan is optimised for getting those six things done.** It is not a feature plan.

---

## 1. Product Readiness (what must actually work on 2026-04-21)

| Area | Must be true before first paid demo | Verification |
|---|---|---|
| Auth / tenant isolation | Signup, login, tenant-scoped JWT, password reset | `docs/qa-acceptance-checklist.md` §2 |
| Lead intake + scoring | Paste lead → enrichment → score + next action | QA §4 |
| Arabic NLP (AR/EN) | Summarize lead note in AR; classify intent in AR | QA §5 |
| Local AI fallback | If Groq key missing, Ollama answers; if Ollama down, Groq answers | QA §6 |
| Agents (8 roles) | Router assigns event → agent → structured output | QA §7 |
| Dashboard | KPIs load < 2 s, RTL correct, numbers reconcile with DB | QA §8 |
| PDPL consent | No outbound message fires without recorded consent | QA §9 |
| Pricing / checkout | Moyasar sandbox → real SAR charge in production mode | QA §10 |
| Observability | Every request has trace id; errors land in one log stream | Ops runbook §3 |

Anything not in the table is **out of scope for launch** and goes to a post-launch backlog.

### 1.1 Known product gaps (do not hide these from customers)
- Calls integration is stubbed — do not promise call recording.
- Some dashboard widgets read from `data/` seeds, not live DB. Label them "Sample" until wired.
- Arabic speech-to-text is not yet live. Demo transcripts only.

---

## 2. Local AI Rollout (Ubuntu 24.04, 4 vCPU EPYC, 7.6 GiB RAM, no GPU)

Hardware constraint: **7.6 GiB RAM, no GPU**. Per `backend/app/services/local_ai/catalog.py`, this auto-detects as **`small` tier**. Do not force higher.

Plan:

1. **Install** (one-time):
   ```bash
   sudo bash scripts/local-ai/install_local_ai.sh
   ```
   Expect `qwen2.5:0.5b` + `qwen2.5:3b-instruct` to pull (~2.5 GB disk).
2. **Enable opt-in**:
   ```bash
   echo "LOCAL_LLM_ENABLED=1" >> backend/.env
   echo "LOCAL_LLM_FORCE_TIER=small" >> backend/.env
   sudo systemctl restart dealix-backend
   ```
3. **Verify**:
   ```bash
   BASE_URL=http://localhost:8000 bash scripts/qa/smoke_test.sh
   curl -s http://localhost:8000/api/v1/local-ai/status | jq
   ```
4. **Budget guardrail**: keep Groq key provisioned as fallback; local AI is a cost-reducer, not a single point of failure. If p95 latency on `/api/v1/local-ai/chat` > 8 s for Arabic prompts, disable local mode and investigate before a demo.
5. **Memory watch**: `qwen2.5:3b` uses ~3.5 GiB resident. Postgres + Redis + FastAPI together must stay under 3 GiB, or OOM will kill Ollama. Add swap if `free -h` shows < 1 GiB available when idle:
   ```bash
   sudo fallocate -l 4G /swapfile && sudo chmod 600 /swapfile
   sudo mkswap /swapfile && sudo swapon /swapfile
   echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
   ```
6. **Do not** run `qwen2.5:7b` or `14b` on this box. They will OOM.

---

## 3. Infrastructure

Current footprint (single VM):

```
Ubuntu 24.04 → docker compose
  ├─ backend (FastAPI)     :8000
  ├─ frontend (Next.js)    :3000
  ├─ postgres 16           :5432
  ├─ redis 7               :6379
  ├─ ollama (host-level)   :11434
  └─ nginx reverse proxy   :80/:443
```

### 3.1 Launch checklist
- [ ] Domain + TLS via Let's Encrypt (`certbot --nginx`). Renewal cron verified.
- [ ] Cloudflare tunnel or Nginx + UFW. Close 8000/5432/6379 at firewall.
- [ ] DB backups: `pg_dump` nightly to object storage (see Ops runbook §5).
- [ ] Redis persistence: `appendonly yes` in prod compose override.
- [ ] Log rotation: `/var/log/dealix/*.log` via logrotate, 14-day retention.
- [ ] Monitoring: UptimeRobot or Healthchecks.io pinging `/api/v1/health` every 60 s.
- [ ] Alerting: email + WhatsApp to founder on 5xx rate > 1%/5min.

### 3.2 Capacity planning
On the specced box this supports **~3–5 concurrent pilot tenants** with light usage. Hard cap the signup endpoint at 20 tenants until we move to a larger instance.

---

## 4. Security

Per `AGENTS.md` Class C: forbidden actions already enforced by `openclaw/policy.py`. Before launch:

- [ ] `make check` clean (ruff + mypy + bandit + npm audit).
- [ ] `gitleaks detect` clean — no secrets in git history.
- [ ] `pip-audit` + `npm audit --production` with no open HIGH/CRITICAL (PR #15 patched current batch).
- [ ] Rotate all secrets in `.env` from defaults (`JWT_SECRET`, `POSTGRES_PASSWORD`, `DEALIX_INTERNAL_API_TOKEN`, webhook tokens).
- [ ] Enable rate limits on `/auth/*` and public webhook endpoints.
- [ ] PDPL data map published in `docs/legal/`. Documented retention (default 13 months for messages).
- [ ] External pentest engaged (required for Phase Gate).
- [ ] Disaster-recovery drill: restore yesterday's DB backup into a scratch compose and confirm tenant data is intact.

### 4.1 Secrets management
Production `.env` lives on the VM at `/etc/dealix/env`, `chmod 600`, owned by `dealix` user. Never commit. Never copy to laptop for more than one session.

---

## 5. QA

See `docs/qa-acceptance-checklist.md` for the full protocol. Cadence:

- **Daily** during pilots: smoke test (`make smoke-test`) on staging + prod after each deploy.
- **Weekly**: full QA checklist run, results appended to `docs/reality_reviews/`.
- **Per release**: Arabic + English paths signed off, screenshots in PR description.

---

## 6. Sales & Outreach (Saudi B2B)

Full playbook: `docs/sales-launch-kit.md`. Summary of the 30-day motion:

- **ICP**: Saudi SMB owner/operator in real estate, healthcare, retail/e-commerce, contracting, education. 5–150 employees. Using WhatsApp + spreadsheets for sales today.
- **Channel**: Founder-led, direct WhatsApp + in-person meetings in Riyadh/Jeddah/Dammam. Not cold email.
- **Offer**: 30-day paid pilot at discounted rate, personal onboarding. Clear success criteria per §5 of sales kit.
- **PDPL guardrail**: no automated outreach in week 1 of the pilot. Every first message is founder-authored.
- **Conversion target**: 3 paid pilots by Day 45.

---

## 7. Marketing

Keep marketing small until Phase Gate. The goal is credibility, not reach.

- [ ] Landing page (`landing/`) reviewed: Arabic copy, real screenshots, 3 case stubs.
- [ ] LinkedIn founder profile updated with Dealix role + pinned post in Arabic.
- [ ] 1 long-form Arabic article per fortnight on LinkedIn (no blog yet).
- [ ] X/Twitter account optional, low priority.
- [ ] **Do not** run paid ads until 2 pilots are live and you can quote them.

---

## 8. Pricing (SAR)

Repo already has a 3-tier structure (`seeds/pricing_plans.json` per PR #14). Recommended launch pricing — all ranges, not guarantees:

| Tier | Monthly (SAR) | Pilot offer (first 3 months) | Target size |
|---|---|---|---|
| **Starter** | 499 | 249 | 1–10 users |
| **Growth** | 1,499 | 749 | 11–50 users |
| **Scale** | 3,999 | 1,999 | 51–150 users |

Onboarding fee: SAR 1,500 waived for pilots. Month-to-month; no annual lock-in during launch.

Adjust based on first 5 discovery calls. Do not print pricing on the public site until after the 3rd signed pilot.

---

## 9. Onboarding

Target: pilot customer is sending their first enriched lead within **48 hours** of contract signature.

Standard onboarding path (documented in `docs/CUSTOMER_OS_ONBOARDING_AR.md`, summarised here):

1. **Day 0** — Contract signed. Founder provisions tenant, creates admin user, sets pricing tier.
2. **Day 1** — 60-min kickoff call (AR). Walk through dashboard, import first 20 leads, configure WhatsApp Business number, set PDPL consent template.
3. **Day 2** — First real lead processed live on the call. Confirm agent output is usable.
4. **Day 7** — Check-in. First objection handled.
5. **Day 14** — Review KPIs (see `docs/metrics-and-kpis.md`). Adjust.
6. **Day 30** — Pilot review meeting → convert or churn.

Every step has a template in `docs/customer_learnings/templates/`. Do not freestyle.

---

## 10. Metrics

Tracked in `docs/metrics-and-kpis.md`. Top-of-funnel four for launch:

- **Pilot pipeline**: # prospects in discovery.
- **Paid pilots**: # signed + paying.
- **Activation**: % pilots that hit "first real lead enriched" in 48 h.
- **Retention**: % pilots renewing at day 30.

Report in the weekly review (Thursday 18:00 Riyadh, founder).

---

## 11. 30 / 60 / 90 day roadmap

### Days 0–30 — Land 3 paid pilots

- Week 1: Operational readiness. Smoke tests green on prod. `/api/v1/health` + local-ai status monitored. Backups verified.
- Week 2: 10 discovery calls. 5 qualified. 2 demos booked.
- Week 3: First pilot signed and onboarded (Day 3 of week = first real lead in system).
- Week 4: 2nd + 3rd pilots signed.

Exit criteria: 3 signed paid pilots, 1 in daily use.

### Days 31–60 — Prove retention

- Weekly pilot health calls. Every bug fix tied to a customer interview ID.
- Truth Registry audit (V005) run.
- Pentest engagement kicked off (external vendor).
- One reference-worthy case study drafted in Arabic.
- No new features outside of customer-triggered bugs.

Exit criteria: 2 pilots active ≥ 30 days, NPS ≥ 30, 0 critical bugs open > 48 h.

### Days 61–90 — Pass Phase Gate

- Pentest report in; Criticals fixed.
- 1st named reference customer (written permission).
- Truth Registry at 100% SUPPORTED.
- Phase Gate review held; if green, unlock Wave A.
- Pricing page published. Paid ads can start — but only if LTV/CAC model has real pilot numbers.

Exit criteria: Phase Gate = Green per `CLAUDE.md` §2.

---

## 12. Owners & cadence

| Cadence | Meeting | Owner | Output |
|---|---|---|---|
| Daily (10-min) | Ops standup | Founder | Pipeline + incidents |
| Weekly Thu 18:00 | Pilot review | Founder | `docs/reality_reviews/YYYY-MM-DD.md` |
| Fortnightly | Truth Registry audit | Founder | `docs/registry/` update |
| Monthly | Phase Gate check | Founder | Green / Yellow / Red |

No standing meetings beyond these until after Phase Gate.

---

## 13. What is explicitly NOT in this plan

- Mobile app.
- Self-service signup.
- Enterprise contracts (>150 users).
- SSO / SAML.
- Non-Saudi expansion.
- Affiliate / reseller program at scale (the scaffolding in `affiliate-system/` stays dormant).

These re-enter the conversation after Phase Gate — not before.
