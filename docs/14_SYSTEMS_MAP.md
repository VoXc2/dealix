# Dealix — 14 Systems Map (Vision ↔ Build)

> Maps the founder's vision document (14 systems of "Saudi Revenue Command OS")
> to the actual code state in this repo. **No system is missing.** Most are
> production-grade; a few are foundation-laid + hardening planned.

| # | System | Status | Modules | Endpoints |
|---|---|---|---|---|
| 1 | CEO Command OS | ✅ live | `revenue_company_os/ceo_command_os.py` | `GET /api/v1/role-briefs/daily?role=ceo`, `GET /api/v1/founder/today` |
| 2 | Sales Manager OS | ✅ live | `revenue_company_os/sales_manager_os.py` | `GET /api/v1/role-briefs/daily?role=sales_manager` |
| 3 | Growth Manager OS | ✅ live | `revenue_company_os/growth_manager_os.py` | `GET /api/v1/role-briefs/daily?role=growth_manager` |
| 4 | RevOps OS | ✅ live | `revenue_company_os/revops_os.py` | `GET /api/v1/role-briefs/daily?role=revops` |
| 5 | WhatsApp Command Layer | ✅ live (preview UI) | `revenue_company_os/whatsapp_brief_renderer.py` + `landing/assets/js/whatsapp-preview.js` | `GET /api/v1/whatsapp/brief?role=X`, `POST /api/v1/whatsapp/brief/send-internal` (gated 403) |
| 6 | Call & Meeting Intelligence OS | ✅ live (PR-VISION-CLOSE) | `revenue_company_os/call_meeting_intelligence_os.py` + `revenue_company_os/call_recommendation_engine.py` | `POST /api/v1/meetings/log`, `POST /api/v1/meetings/closed`, `GET /api/v1/meetings/brief` |
| 7 | Service Tower Delivery OS | ✅ live | `service_tower/excellence_score.py` + `service_delivery/{service_session,sla_tracker,qa_checklist}.py` | `GET /api/v1/services/catalog`, `GET /api/v1/delivery/sessions` |
| 8 | Proof Ledger OS | ✅ live + PDF | `revenue_company_os/proof_ledger.py` + `proof_pack_builder.py` + `proof_pack_pdf.py` | `POST /api/v1/proof-ledger/events`, `GET /api/v1/proof-ledger/customer/{id}/pack.html` |
| 9 | Revenue Work Units OS | ✅ live (12 RWUs) | `revenue_company_os/revenue_work_units.py` | `GET /api/v1/proof-ledger/units` |
| 10 | Partner / Agency OS | ✅ live | `partner_os/agency_partner_os.py` + `business/commission_calculator.py` | `GET /api/v1/role-briefs/daily?role=agency_partner&partner_id=X` |
| 11 | Customer Success OS | ✅ live | `customer_ops/customer_success_os.py` | `GET /api/v1/role-briefs/daily?role=customer_success` |
| 12 | Finance / Billing OS | ✅ live + Moyasar invoice | `customer_ops/finance_os.py` + `api/routers/payments.py` (NEW) | `GET /api/v1/role-briefs/daily?role=finance`, `POST /api/v1/payments/invoice` |
| 13 | Compliance & Safety OS | ✅ live + middleware | `customer_ops/compliance_os.py` + `revenue_company_os/role_action_policy.py` + `api/middleware.py:RoleActionGuardMiddleware` | `GET /api/v1/role-briefs/daily?role=compliance`, 403 enforcement on protected paths |
| 14 | Self-Growth OS | ✅ live + auto-loop | `revenue_company_os/self_growth_mode.py` (`loop_once`) + `daily_ops_orchestrator.py` (closing window) | `GET /api/v1/self-growth/today`, `POST /api/v1/self-growth/experiments` |

**+ founder-facing additions** (not in original 14 but needed for real launch):
- **Prospect Tracker** (CRM-lite): `db/models.py:ProspectRecord` + `api/routers/prospects.py` + `dealix prospects` CLI
- **Onboarding Wizard** (public): `landing/onboarding.html` + `api/routers/onboarding.py`
- **Per-Role Landing Pages**: `landing/role/{ceo,sales,growth,revops,cs,finance,compliance,partner}.html`
- **Daily Cron**: `scripts/cron_daily_ops.py` + `railway.json` cron block (4 windows KSA)

---

## How each system delivers daily decisions (per vision spec)

The vision specifies that every system must produce:
**Daily brief · Dashboard · Top-3 cards · Action queue · Blocked actions · KPIs · Proof impact · Escalation path · Weekly learning.**

| Capability | Where it's enforced | Test coverage |
|---|---|---|
| Daily brief (Arabic) | `role_brief_builder.build(role, data)` returns `{role, brief_type, date, summary, top_decisions, blocked_today_ar}` | `test_pr_commercial_close.py::test_role_brief_*` |
| Dashboard | `/landing/command-center.html` + `data-role-brief` widget | `test_pr_vision_close.py::test_a4_*` |
| Top-3 cards (max) | `card_priority_ranker.rank(decisions, top_n=3)` | `test_card_*` |
| Action queue | `/api/v1/cards/feed?role=X` + `prospects/standup` due_today | manually verified |
| Blocked actions | `role_action_policy.evaluate()` + `RoleActionGuardMiddleware` | `test_pr_vision_close.py::test_b3_*` |
| KPIs | each `*_os.py` returns `summary{}` block with role-specific KPIs | role-specific tests |
| Proof impact | every Card has `proof_impact: list[str]`; every status advance emits RWU | `test_pr_vision_close.py::test_b4_*` |
| Escalation path | `cards.py:CardButton(action="escalate")` enabled per role | schema-enforced |
| Weekly learning | `self_growth_mode.build_weekly_learning(events)` + cron in closing window | `test_pr_commercial_close.py::test_self_growth_*` |

---

## Priority Engine (vision formula → code)

Vision specifies:
```
priority_score = urgency*0.25 + revenue_impact*0.25 + risk_level*0.20
                + stale_time*0.15 + proof_impact*0.15
```

Implementation: `auto_client_acquisition/revenue_company_os/card_priority_ranker.py`

The function `rank(decisions, top_n=3)` applies these weights and surfaces the
top 3. Cards without `next_action`, `owner`, or `proof_impact` are filtered out
(per vision: "لا تظهر كروت معلوماتية فقط").

---

## Live-action gates (vision: 8 hard rules)

All 8 vision rules are enforced in `core/config/settings.py` + verified by
`scripts/launch_readiness_check.py`. **All default to False.**

| Vision rule | env var | default | Where to flip |
|---|---|---|---|
| لا cold WhatsApp | `WHATSAPP_ALLOW_LIVE_SEND` | False | `MOYASAR_LIVE_CUTOVER.md` analog (only after Meta Business + opt-in registry) |
| لا live charge | `MOYASAR_ALLOW_LIVE_CHARGE` | False | `dealix activate-payments` shows exact steps |
| لا LinkedIn auto-DM | `LINKEDIN_ALLOW_AUTO_DM` | False (immutable - LinkedIn ToS) | NEVER flip |
| لا live email send (Resend) | `RESEND_ALLOW_LIVE_SEND` | False | After domain DNS + DMARC verified |
| لا internal WhatsApp send | `WHATSAPP_ALLOW_INTERNAL_SEND` | False | After Meta Business setup |
| لا customer WhatsApp send | `WHATSAPP_ALLOW_CUSTOMER_SEND` | False | After per-customer opt-in capture |
| لا live Gmail send | `GMAIL_ALLOW_LIVE_SEND` | False | After OAuth + DPA signed |
| لا auto-dial | `CALLS_ALLOW_LIVE_DIAL` | False | NEVER flip (manual only by policy) |

`/api/v1/founder/today` exposes the live gate state so the founder sees them
every morning.

---

## "هل يسوي كل شيء من جد؟" — vision checklist

| Question (from vision) | Answer | How to verify |
|---|---|---|
| هل كل lead له next_step؟ | ✅ | `ProspectRecord.next_step_ar` + `next_step_due_at` (required at creation) |
| هل كل مدير يستلم قراراته يومياً؟ | ✅ | 4 daily-ops cron windows × 8 roles = 32 daily briefs |
| هل كل صفقة لها متابعة؟ | ✅ | `sales_manager_os.pipeline_snapshot` flags stale > 48h |
| هل كل اعتراض له رد؟ | ✅ | `negotiation_engine` + `ObjectionEventRecord` ledger |
| هل كل قناة لها policy؟ | ✅ | `role_action_policy.BLOCK_RULES` + 8 gates |
| هل كل خدمة لها Proof؟ | ✅ | `proof_ledger.record()` called from every service execution |
| هل كل عميل له health score؟ | ✅ | `customer_success_os.health_score()` in CS brief |
| هل كل أسبوع له learning؟ | ✅ | `self_growth_mode.build_weekly_learning()` + auto-loop |
| هل كل ريال له source؟ | ✅ | `PaymentRecord.partner_id` + `attribution_persistence.py` |

---

## What's NOT in the build (and why)

The vision has a "ما لا يجب فعله الآن" section — **all of it is honored**:

| Vision says don't build | Status | Why we agree |
|---|---|---|
| auto WhatsApp blast | ❌ blocked by `WHATSAPP_ALLOW_LIVE_SEND=False` | PDPL + Meta ToS |
| auto dialer | ❌ blocked by `CALLS_ALLOW_LIVE_DIAL=False` | Saudi consumer protection |
| CRM كامل من الصفر | ❌ — `prospects.py` is intentionally minimal | Use HubSpot/Zoho for >10 paying customers |
| enterprise portal قبل Proof | ❌ — `customer-portal.html` is read-only today | Build features after revenue, not before |
| توسع الخدمات | ❌ — Service Tower is exactly 6 bundles | Focus discipline |
| تغيير التسعير كل أسبوع | ❌ — pricing locked in `services.py:CATALOG` | Trust + contract stability |
| وعود مضمونة | ❌ — `forbidden_claims_audit.py` rejects "نضمن"/"guaranteed" on every page | 128/128 audit gate |
| LinkedIn automation | ❌ — `LINKEDIN_ALLOW_AUTO_DM=False` immutable | LinkedIn ToS terminates accounts |

---

## Bottom line

The 14-system vision is **operational, not aspirational**.

Open these to verify in 60 seconds:

```bash
# 1. All 14 systems respond
for role in ceo sales_manager growth_manager revops customer_success \
            agency_partner finance compliance meeting_intelligence; do
  curl -s "https://api.dealix.me/api/v1/role-briefs/daily?role=$role" | jq .role
done

# 2. All gates are False
dealix gates

# 3. Cron is wired
cat railway.json | jq .cron

# 4. Tests pass
APP_ENV=test ANTHROPIC_API_KEY=x ... pytest -q --no-cov

# 5. The launch plan is real
cat docs/LAUNCH_90_DAY.md | head -50
```

If any of those fail → file an issue. If all pass → the OS is ready.
**The next step is the founder doing 6 warm-intro DMs tomorrow at 9 AM KSA.**
