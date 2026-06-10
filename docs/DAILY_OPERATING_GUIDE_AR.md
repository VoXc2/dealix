# دليل التشغيل اليومي — DAILY_OPERATING_GUIDE_AR

> **الإيقاع اليومي** لمؤسس Dealix. قائمة فحص (checklist) في 3 أوقات: صباحي، مسائي، شهري. bullet-heavy + link-heavy.
>
> **آخر تحديث:** 2026-06-03 — المالك: Founder — الإصدار: v1.0

---

## 1) الفهرس السريع

- ☀️ Morning check (10 min)
- 🌙 End-of-day wrap (5 min)
- 📅 Weekly review trigger (Sunday 9 AM)
- 📊 Monthly governance review (1st of month)

> **الوقت الإجمالي اليومي:** 15 دقيقة. **انظر:** [`WEEKLY_OPERATING_GUIDE_AR.md`](WEEKLY_OPERATING_GUIDE_AR.md) للأسبوعي.

---

## 2) ☀️ Morning Check (10 دقائق)

### 2.1 الأوامر (الترتيب مهم)

```bash
# 1) 5 metrics — 2 دقيقة
python scripts/founder_daily_five_metrics.py

# 2) State of day — 3 دقيقة
python scripts/run_dealix_daily_ops.py --api-only

# 3) Check inbox — 2 دقيقة
# (3 أشياء: incident + approvals + leads warm)

# 4) Read founder brief — 3 دقيقة
cat data/founder_briefs/$(date +%Y-%m-%d).md 2>/dev/null || echo "no brief today"
```

### 2.2 Checklist

- [ ] **P1 incident في `data/ai_governance/agent_incidents.jsonl`؟** → ارجع لـ `AGENT_INCIDENT_RESPONSE_AR.md`
- [ ] **P0 approval في `/api/v1/ops-autopilot/approvals/pending`؟** → وافق أو ارفض
- [ ] **3+ warm leads جديدة من الأمس؟** → ارجع لـ `ENTERPRISE_PIPELINE_REVIEW.md`
- [ ] **Deal Risk HIGH؟** → Schedule call مع Sales Lead
- [ ] **Moyasar payment failed؟** → `BILLING_MOYASAR_RUNBOOK.md`

### 2.3 KPIs المراقبة (5 metrics)

| Metric | Threshold | Action |
|--------|-----------|--------|
| **Conversion lead → SQL** | < 8% | راجع `MESSAGE_PERFORMANCE_LIBRARY_AR.md` |
| **Active deals in pipeline** | < 5 | راجع ABM list (`accounts.jsonl`) |
| **Critical incidents open** | > 0 | Incident Response |
| **Approval queue** | > 3 | راجع `HUMAN_APPROVAL_BOUNDARIES_AR.md` |
| **MRR** | declining 7 days | راجع `CHURN_RISK.md` (إن وجد) |

---

## 3) 🌙 End-of-Day Wrap (5 دقائق)

### 3.1 Checklist

- [ ] **سجّل 3 أشياء حدثت اليوم** (in `docs/ops/FOUNDER_DAILY_ANCHOR_AR.md` → "Today's log")
- [ ] **افتح 3 approvals معلقة** (القرارات الصغيرة)
- [ ] **Schedule 3 first-touch follow-ups** للغد (Calendar block)
- [ ] **سجّل أي ملاحظة** في `docs/memory/` (الـ memory/ folder)
- [ ] **شغّل** `python scripts/run_dealix_daily_ops.py --skip-api` (offline log)

### 3.2 Output يومي

- **3 logs** → `docs/ops/FOUNDER_DAILY_ANCHOR_AR.md`
- **3 approvals** → /api/v1/ops-autopilot/approvals/decided
- **3 follow-ups** → Calendar
- **1 weekly trigger** (إن كان Sunday)

---

## 4) 📅 Weekly Review Trigger (Sunday 9 AM)

> **راجع:** [`WEEKLY_OPERATING_GUIDE_AR.md`](WEEKLY_OPERATING_GUIDE_AR.md) للقائمة الكاملة.

### 4.1 Triggers

- **كل أحد 9 صباحاً** → افتح Weekly Operating Meeting template
- **شغّل:** `bash scripts/founder_weekly_loop.sh` (Sunday gates)

### 4.2 5 دقائق قبل الاجتماع

- [ ] اقرأ `reports/enterprise_sales/ACCOUNT_PLAN_REVIEW.md`
- [ ] اقرأ `reports/ai_governance/AGENT_GOVERNANCE_REVIEW.md`
- [ ] اقرأ `reports/data_products/LEARNING_LOOP_REVIEW.md`

---

## 5) 📊 Monthly Governance Review (1st of month)

### 5.1 الأوامر

```bash
# 1) Audit trail
cat reports/ai_governance/AGENT_PERMISSION_REVIEW.md

# 2) Risk register
cat docs/risk_resilience/RISK_REGISTER.md

# 3) Schema drift check
ls -la schemas/ | wc -l  # must be 51 (no drift)

# 4) Compliance review
cat docs/responsible_ai/RESPONSIBLE_AI_SCORE.md
```

### 5.2 Checklist

- [ ] راجع **A0-A5 distribution** في `data/ai_governance/agent_registry.jsonl` — هل ظهر A5؟ (ممنوع)
- [ ] راجع **incident summary** — هل closed vs open في تحسّن؟
- [ ] راجع **vendor DD queue** (`docs/enterprise/VENDOR_DUE_DILIGENCE_QUEUE.md`)
- [ ] راجع **PDPL logs** — هل أي data export جديد للسوق السعودي؟
- [ ] راجع **data quality** — هل `data_quality_issues.jsonl` ينخفض؟

### 5.3 Output شهري

- **1 board memo** → `reports/company_os/board_memo_<YYYY-MM>.md`
- **1 risk register update** → `docs/risk_resilience/RISK_REGISTER.md`
- **1 quarterly OKR review** (إن كان 1st of Q1/Q2/Q3/Q4)

---

## 6) قواعد ذهبية (Hard Rules)

- 🚫 **لا ترسل WhatsApp/email/LinkedIn** بدون موافقة (Default-Deny).
- 🚫 **لا تنشر landing page** بدون founder sign-off.
- 🚫 **لا تسجّل agent جديد** في registry بدون `evidence_level=validated`.
- ✅ **سجّل كل قرار** في الـ daily anchor.
- ✅ **استخدم only scripts/ المفعّلة** — لا run ad-hoc commands.

---

## 7) See Also

- [`FOUNDER_START_HERE_AR.md`](FOUNDER_START_HERE_AR.md)
- [`WEEKLY_OPERATING_GUIDE_AR.md`](WEEKLY_OPERATING_GUIDE_AR.md)
- [`DEALIX_COMPANY_OS_INDEX_AR.md`](DEALIX_COMPANY_OS_INDEX_AR.md)
- [`PRIORITY_ROADMAP_AR.md`](PRIORITY_ROADMAP_AR.md)
- [`SYSTEM_BOUNDARIES.md`](SYSTEM_BOUNDARIES.md)
- [`FILE_OWNERSHIP_MAP.md`](FILE_OWNERSHIP_MAP.md)

---

## Open Questions for Founder

1. هل 15 دقيقة/يوم (10 morning + 5 evening) معقولة، أم تحتاج تخفيض؟
2. هل تريد **daily Slack/WhatsApp digest** تلقائي، أم تكتفي بالـ scripts؟
3. هل الـ Monthly Governance Review في اليوم 1 من الشهر، أم في اليوم 5 (بعد تجميع البيانات)؟
