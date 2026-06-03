# Daily 400-Draft Factory — مصنع الـ 400 مسودة يومياً

> **القاعدة الحاكمة:**
> ```txt
> 400 drafts/day  = إنتاج مسودات مخصّصة وجاهزة للمراجعة  ✅ مسموح
> 400 sends/day   = إرسال 400 رسالة يومياً               ❌ غير مفعّل افتراضياً
> ```
> الإرسال يتطلب جاهزية تسليم + suppression list + unsubscribe + موافقة بشرية + صحة دومين.
>
> **مبني على:** بنية المسودات الحالية في `company_os/revenue/outreach_queue.json` و`company_os/revenue/followups.json`، وحوكمة `company_os/governance/agent_permissions.md` (prospect_research: Draft فقط، الإرسال بشري).

---

## 1. لماذا نفصل Draft عن Send؟

`agent_permissions.md` صريح: وكيل `prospect_research` صلاحيته **Draft** للرسائل، و**"Send messages = NOT ALLOWED / Human only"**، والخط الأحمر #1: "AI never sends external messages without approval."

إذن المصنع ينتج **مسودات** بكميّة، والإنسان يوافق على **دفعات إرسال صغيرة وآمنة**.

---

## 2. التوزيع اليومي لـ 400 مسودة

| النوع                         | العدد |
| ----------------------------- | ----: |
| First-touch drafts            |   150 |
| Follow-up 1                   |   100 |
| Follow-up 2                   |    75 |
| Proposal / Proof intros       |    35 |
| Close-loop / nurture          |    20 |
| Partner / press / referral    |    20 |
| **الإجمالي**                  | **400** |

> الـ follow-ups تتبع إيقاع الريبو الحالي **3 / 7 / 14 يوم** (من `revenue/followups.json` → `rules.follow_up_sequence`).

---

## 3. حقول كل مسودة (Draft Schema)

كل مسودة يجب أن تحتوي الحقول التالية (امتداد لبنية `outreach_queue.json` الحالية):

```txt
company                 سطر الشركة
sector                  القطاع
country                 الدولة (Saudi-first)
city                    المدينة
decision_maker_role     دور صاحب القرار (لا اسم شخصي/PII في اللوقات)
signal                  الإشارة التي بُنيت عليها الرسالة
pain_hypothesis         فرضية الألم
likely_need             ما يحتاجه العميل غالباً
recommended_mission     المهمة المقترحة (M1..M8)
draft_subject           عنوان الرسالة
draft_body              نص الرسالة
cta                     الخطوة التالية الصغيرة
personalization_score   0–100
evidence_level          low / medium / high
risk_level              low / medium / high
approval_status         pending_approval / approved / rejected
send_readiness          not_ready / ready_when_domain_healthy
```

> **حماية البيانات:** لا أسماء أشخاص خام ولا PII في اللوقات/المسودات المخزّنة؛ نكتفي بالدور الوظيفي (مطابق لـ `governance/data_handling_checklist.md` و`pdpl_checklist.md`).

---

## 4. بوابات الجودة (Quality Gates)

تُرفض المسودة آلياً قبل وصولها لقائمة المراجعة إذا:

- `personalization_score < 60`، أو
- لا توجد `signal` حقيقية (تخصيص وهمي)، أو
- `risk_level = high` بلا مبرر، أو
- تحتوي وعداً/ضماناً ("نضمن"، "مؤكّد +X%") — **No guaranteed claims**، أو
- تستخدم Re:/Fwd: مزيّفة، أو
- المصدر قائمة مشتراة، أو
- تستهدف من لم يبدِ اهتماماً مشروعاً (legitimate interest غير واضح).

KPI الجودة اليومي:
```txt
drafts_generated = 400
drafts_passed_quality
drafts_rejected
avg_personalization_score
top_missions / top_sectors / top_cities / top_signals
```

---

## 5. ترتيب Top-100 (لا نراجع 400 يدوياً)

النظام يرتّب أفضل 100 مسودة للمراجعة البشرية حسب:

```txt
Top 100 by:
  - prospect score        (من revenue/prospects.csv)
  - buying signal strength
  - personalization score
  - offer/mission fit
  - low risk
  - sector priority (Saudi-first)
```

ثم المؤسس يوافق على **20–80** للإرسال حسب جاهزية الدومين.

---

## 6. دفعات الإرسال الآمن (Safe-Send Batches)

الأمر النموذجي لوكيل المسودات:
```txt
Generate 400 drafts/day.
Do not send by default.
Rank top 80.
Prepare safe send batches (size = حسب صحة الدومين).
```

ثم القرار البشري:
```txt
Approve 20–80 sends  ← حسب SPF/DKIM/DMARC + bounce + spam-rate.
```

---

## 7. جدول رفع الإرسال التدريجي (Ramp)

| المرحلة         | Drafts/day | Sends/day |
| --------------- | ---------: | --------: |
| Day 1–7         |        400 |     20–40 |
| Week 2          |        400 |    50–100 |
| Week 3          |        400 |   100–200 |
| Week 4          |        400 |   200–300 |
| بعد الاستقرار   |    400–800 |   300–400 |

**شرط الانتقال بين المراحل** (راجع `docs/outreach/GCC_OUTREACH_POLICY_AR.md`):
```txt
SPF/DKIM/DMARC جاهزة · one-click unsubscribe · suppression list شغّالة
bounce handling شغّال · spam rate < 0.3% · domain health جيد (Postmaster Tools)
no fake Re/Fwd · no purchased lists
```

> الرفع تدريجي ومراقب — لا bursts. أي ارتفاع في الـ spam rate أو الـ bounces يوقف الرفع ويعيدنا مرحلة للخلف.

---

## 8. التدفّق الكامل

```txt
prospects.csv + signals
        │
        ▼
Need Router ─▶ Client Need Card  (docs/outreach/CLIENT_NEED_CARD_SYSTEM_AR.md)
        │
        ▼
400 Drafts (بالتوزيع أعلاه) ─▶ Quality Gates ─▶ Top-100 Queue
        │
        ▼
Founder approves 20–80  ─▶  Human sends (داخل حدود الـ Ramp)  ─▶  ai_action_ledger
        │
        ▼
Replies ─▶ Follow-ups (3/7/14) ─▶ Proof ─▶ Mission upgrade
```

---

## 9. الربط

- التقرير اليومي: `reports/outreach/DAILY_400_DRAFT_PRODUCTION.md`
- بطاقات الاحتياج: `docs/outreach/CLIENT_NEED_CARD_SYSTEM_AR.md`
- سياسة القنوات والإرسال: `docs/outreach/GCC_OUTREACH_POLICY_AR.md`

*ملاحظة مصدر: متطلبات المرسلين (SPF/DKIM/DMARC، spam rate < 0.3%، one-click unsubscribe، الرفع التدريجي) مبنية على "Google Workspace — Email sender guidelines". الإرسال قرار مؤسس.*
