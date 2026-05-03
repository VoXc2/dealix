# Dealix Operations Runbook

**جمهور الوثيقة:** الـ Founder + first hires (Sales / CS / Support).
**التحديث الأخير:** يُربط بآخر commit على `claude/launch-command-center-6P4N0`.

هذا runbook عملي يومي/أسبوعي/شهري + incident playbook + rollback.
يفترض أن النظام مُنشَر على staging أو production (يقابل `STAGING_BASE_URL`
أو `PRODUCTION_BASE_URL`).

---

## 1) Daily Operating Rhythm — 4 windows

النظام يعرف 4 نوافذ في `auto_client_acquisition/revenue_company_os/daily_ops_orchestrator.py`. شغّلها يدوياً أو عبر cron.

### 08:30 KSA — Morning brief
```bash
curl -s -X POST "$BASE_URL/api/v1/daily-ops/run" \
  -H "Content-Type: application/json" \
  -d '{"window":"morning"}' | jq .
```
ينتج briefs لـ: `ceo`, `sales_manager`, `growth_manager`, `customer_success`, `compliance`.

**ماذا يفعل الـ Founder:**
1. يقرأ CEO brief (3 قرارات).
2. يفتح Approval queue ويعتمد ما لا يحتاج نقاش.
3. ما يحتاج نقاش → يحدد اجتماع 10 دقائق مع الـ owner.

### 12:30 KSA — Midday execution check
```bash
curl -s -X POST "$BASE_URL/api/v1/daily-ops/run" -d '{"window":"midday"}'
```
Sales + Growth deltas. **هدف:** تأكد ما في pipeline stuck > 4 ساعات.

### 16:30 KSA — Closing window
```bash
curl -s -X POST "$BASE_URL/api/v1/daily-ops/run" -d '{"window":"closing"}'
```
Sales + Finance: invoices ready، follow-ups جاهزة لإرسال صباحاً.

### 18:00 KSA — End-of-day scorecard
```bash
curl -s -X POST "$BASE_URL/api/v1/daily-ops/run" -d '{"window":"scorecard"}'
```
CEO + RevOps + Compliance: scorecard اليوم + خطة بكرة + التزام السلامة (refusals).

### Cron template (Railway/Linux)
```cron
# KSA = UTC+3
30 5 * * *  curl -X POST $BASE_URL/api/v1/daily-ops/run -d '{"window":"morning"}'
30 9 * * *  curl -X POST $BASE_URL/api/v1/daily-ops/run -d '{"window":"midday"}'
30 13 * * * curl -X POST $BASE_URL/api/v1/daily-ops/run -d '{"window":"closing"}'
0  15 * * * curl -X POST $BASE_URL/api/v1/daily-ops/run -d '{"window":"scorecard"}'
```

---

## 2) Weekly Rituals (يوم خميس صباحاً)

| Ritual | المسؤول | الإنتاج |
|---|---|---|
| **Weekly Proof Pack** لكل عميل | CS | PDF موقّع + حصري للعميل |
| **Cost Review** (`/observability/costs/summary?days=7`) | Founder | تأكد ما في agent يصرف > 100 SAR/يوم |
| **Refusals Audit** (`/observability/unsafe/summary?days=7`) | Compliance | يجب أن يبقى `no_unsafe_action_executed=true` |
| **Quality KPIs** (`/observability/quality?days=7`) | RevOps | acceptance_rate ≥ 60%، complaint_rate ≤ 5% |
| **Pipeline Review** | Sales | review كل deal في `pilot` أو `needs_approval` |
| **Self-Growth Experiment** | Founder | اختر 1 segment + 1 channel + 1 message للتجربة الجديدة |

---

## 3) Monthly Rituals (أول 3 أيام من كل شهر)

- **MRR audit** (`/api/v1/partners/{id}/dashboard` لكل شريك).
- **Subscription churn check** (`SubscriptionRecord` بـ `status=canceled` آخر 30 يوم).
- **Service Excellence rescore** (`auto_client_acquisition/service_tower/excellence_score.py`) — كل خدمة يجب أن تبقى ≥ 80.
- **Live-action gates audit** — نفّذ:
  ```bash
  python -c "from core.config.settings import get_settings; s=get_settings(); \
    print({g: getattr(s,g) for g in ['whatsapp_allow_live_send','gmail_allow_live_send','moyasar_allow_live_charge','linkedin_allow_auto_dm','resend_allow_live_send','whatsapp_allow_internal_send','whatsapp_allow_customer_send','calls_allow_live_dial']})"
  ```
  يجب أن يكون كل المتغيرات `False` إلا ما اعتمدته صراحة بـ commit موقَّع.

---

## 4) Incident Playbook

### P0 — أمان / إرسال خاطئ / تعطل كامل (≤ 1 ساعة)

**Triggers:**
- `/healthz` returns non-200 لأكثر من 5 دقائق.
- شكوى عميل عن "وصلت رسالة لم يطلبها".
- `unsafe_action_executed=true` في أي endpoint.

**Actions (في الترتيب):**
1. **Stop the bleeding:** اقلب live-action gate ذو الصلة إلى `false` فوراً.
   ```bash
   railway variables set WHATSAPP_ALLOW_LIVE_SEND=false  # مثلاً
   railway redeploy
   ```
2. اقفل الـ outbound queue إذا موجود (`/api/v1/admin/outbound/pause`).
3. أرسل bulletin داخلي للـ team.
4. خلال ساعة: شارك update مع العملاء المتأثرين.
5. خلال 24 ساعة: post-mortem (متى/لماذا/الإصلاح/الـ guardrail الجديد).

### P1 — خدمة مهمة لا تعمل (نفس اليوم)
- `/api/v1/cards/feed`, `/role-briefs/daily`, `/proof-ledger` — أي endpoint صار 5xx > 5 دقائق.
- شغّل: `python scripts/launch_readiness_check.py` → ابحث عن السبب.
- Rollback إذا الـ commit الأخير هو السبب (انظر §6).

### P2 — connector / Proof Pack متأخر (≤ 24 ساعة)
- Connector failure: راجع `webhook_deliveries` table، أعد إرسال يدوياً.
- Proof Pack متأخر: ابحث عن `service_sessions` بـ `breach_flag=true`، أرسل update للعميل.

### P3 — سؤال / تحسين (≤ 48 ساعة)
- ضع التذكرة في backlog، رد بـ ack خلال ساعة.

---

## 5) Escalation Matrix

| الحدث | يصعّد إلى | كيف |
|---|---|---|
| P0 / breach / unsafe execution | Founder + Compliance | WhatsApp business + email |
| Payment dispute (Moyasar) | Founder | Moyasar dashboard + email |
| Privacy / PDPL request | Founder + Legal | Email رسمي خلال 48 ساعة |
| Negative review / public complaint | Founder | Direct DM في 4 ساعات |
| Customer cancel intent | CS lead | Save call خلال يوم |

---

## 6) Rollback Procedure

عند فشل deploy جديد:
```bash
# 1. Identify last good commit
git log --oneline -10

# 2. Revert (لا تستخدم --hard على main)
git revert <BAD_COMMIT_SHA>

# 3. Push (Railway will redeploy automatically)
git push origin claude/launch-command-center-6P4N0

# 4. Verify
sleep 90
python scripts/staging_smoke.py --base-url "$STAGING_BASE_URL"
```

في حالة الطوارئ القصوى فقط:
```bash
# يحتاج صلاحية explicit من الـ Founder
git push --force origin <LAST_GOOD_SHA>:claude/launch-command-center-6P4N0
```

---

## 7) قواعد ذهبية لا تكسرها

1. **لا تفعّل أي live-action gate قبل أول Proof Pack مُسلَّم.**
2. **لا توقّع white-label قبل 3 paid pilots.**
3. **لا تُعدِّل `_HIGH` في unsafe_action_monitor دون موافقة Compliance.**
4. **لا تكتب `print(...)` في production paths** — `repo_architecture_audit` يفرض.
5. **لا تنشر "نضمن" أو "guaranteed"** — `forbidden_claims_audit` يفرض.
6. **لا تضع secrets في الـ repo** — `gitleaks` يجب أن يبقى أخضر.
7. **كل secret في Railway env**، لا في `.env` ملف committed.

---

## 8) Daily Founder Routine (أول 30 يوم بعد التدشين)

```
07:00 افتح WhatsApp business inbox + Email
08:30 morning daily-ops + قراءة CEO brief
09:00 5 LinkedIn outreach manual (انظر OUTREACH_PLAYBOOK)
10:00 Diagnostic calls / Pilot intake (إذا متاح)
12:30 midday daily-ops + sales pipeline check
14:00 وقت إنتاجي: writing case studies / improving service
16:30 closing daily-ops + invoice list
17:00 الرد على customer support tickets
18:00 scorecard daily-ops + خطة بكرة
19:00 إغلاق
```

---

## 9) ربط الوثائق الأخرى

- **`docs/OUTREACH_PLAYBOOK.md`** — السكربتات بالعربي للوكالات.
- **`docs/LAUNCH_DAY_CHECKLIST.md`** — الخطوة بخطوة لليوم 0.
- **`docs/FIRST_PILOT_INTAKE.md`** — نموذج intake لأول عميل.
- **`docs/RAILWAY_DEPLOY_GUIDE_AR.md`** — تفاصيل الـ deployment.
- **`docs/PRIVATE_BETA_RUNBOOK.md`** — مزيد من العمق التشغيلي.
- **`scripts/staging_smoke.py`** — verify staging URL بعد deploy.
- **`scripts/launch_checklist.py`** — gate نهائي قبل التدشين.
