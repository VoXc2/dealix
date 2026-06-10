# Founder Commercial Rhythm — إيقاع المؤسس التجاري اليومي والأسبوعي
**Dealix — Agent #3**

> **الغرض:** روتين ثابت للمؤسس يمنع الفوضى ويجعل القرار التجاري يومياً/أسبوعياً قابلاً للإنجاز. مرتبط بـ `MASTER_COMMERCIAL_OPERATING_PLAN_AR.md` و `FOUNDER_DAILY_ANCHOR_AR.md` و `FOUNDER_REVENUE_DAY_ONE_AR.md`.

---

## 1. الفلسفة

**إيقاع ثابت + بيانات واضحة = قرارات أسرع = تنفيذ أنظف = مؤسس أقل إنهاكاً.**

كل ما في هذا الملف مرتبط بـ:
- **SOAEN** — Source/Owner/Approval/Evidence/Next Action
- **claim_policy.yaml** — لا ادعاء بلا دليل
- **approval_policy.yaml** — كل قرار حرج له approval level
- **agent_permissions.yaml** — لا تجاوز لوكيل

---

## 2. الإيقاع اليومي (Daily Rhythm)

### 2.1 الصباح (08:00 — 09:00) — "5 دقائق"
**الأمر:** `bash scripts/run_founder_commercial_day.sh`

1. افتح `/[locale]/ops/founder` (الـ 90-min cockpit)
2. **Pipeline** — ما الجديد؟ ما الذي يحتاج موافقة؟
3. **War Room** — Top 10 + متابعات
4. **Proposals** — هل يوجد proposal يحتاج موافقة؟
5. **Payments** — هل يوجد payment handoff ينتظر؟
6. **Risks** — هل ظهر risk جديد؟

**المخرج:** قائمة 1-3 مهام اليوم فقط.

### 2.2 منتصف النهار (12:00 — 12:30) — "30 دقيقة"
1. Discovery calls (1-2)
2. Proposal drafts
3. Customer health check (5 دقائق)
4. Channel engagement (LinkedIn/comments — 10 دقائق)

### 2.3 المساء (18:00 — 18:15) — "5 دقائق"
**الأمر:** `python scripts/founder_evening_evidence.py --append`

1. سجّل event واحد على الأقل في `operations/evidence_events_tracker.csv`
2. حدّث tomorrow's draft list
3. أرسل 1 message (warm) — manual فقط
4. حدّث 1 social post (إذا في queue approved)
5. راجع open approvals (1-2 click max)

### 2.4 نهاية اليوم (EOD)
- كل external action → draft (لا send)
- كل approval → marked
- كل risk → flagged

---

## 3. الإيقاع الأسبوعي (Weekly Rhythm)

### 3.1 يوم الأحد — "Weekly Review" (45 دقيقة)

**قبل الجلسة:** `python scripts/founder_weekly_metrics_bundle.py --write`

#### 3.1.1 Pipeline Review (10 دقائق)
- ما الذي أغلق هذا الأسبوع؟ (won/lost)
- ما الذي stagnated > 14 يوم؟ (cleanup)
- ما stage يحتاج cleanup؟
- Conversion rate: lead → qualified → meeting → proposal → won

#### 3.1.2 Channel ROI (5 دقائق)
- ما أفضل channel هذا الأسبوع؟ (ROI/cost per lead/cost per reply)
- هل فيه channel يجب إيقافه؟ (cost > benefit)
- هل فيه channel يجب زيادته؟ (high ROI, low volume)

#### 3.1.3 Best Offer & ICP (5 دقائق)
- أي offer يحوّل أكثر؟ (conversion by offer)
- أي ICP يستجيب؟ (qualified leads by segment)
- أي ICP يرفض؟ (no-fit pattern)

#### 3.1.4 Customer Health (5 دقائق)
- كم عميل في خطر؟ (health score < 50)
- كم client في renewal window؟
- هل في expansion signal؟

#### 3.1.5 Finance (5 دقائق)
- Revenue this week
- Pipeline value change
- Burn rate vs plan
- Margin trend

#### 3.1.6 Risk Register (5 دقائق)
- أي risk جديد؟
- هل أي risk قديم تفاقم؟
- هل في client walk-away candidate؟

#### 3.1.7 Next Week Focus (10 دقائق)
- **القرار الأسبوعي الوحيد** (one decision)
- Top 3 tasks
- Founder time allocation

**المخرج:** Weekly Retro doc + Weekly Scorecard

### 3.2 أيام أخرى — light rhythm
- **الإثنين:** Marketing content week plan (15 دقيقة)
- **الثلاثاء:** Sales deep dive (15 دقيقة)
- **الأربعاء:** Customer success review (15 دقيقة)
- **الخميس:** Partner pipeline (15 دقيقة)
- **الجمعة:** Scorecard finalize + weekend prep
- **السبت:** Off (إلا طوارئ)

---

## 4. الإيقاع الشهري (Monthly Rhythm)

### 4.1 يوم 1 من كل شهر — Monthly Close (2 ساعة)
1. **Revenue close** — actuals من CRM (لا تخمين)
2. **CAC by channel** — last 90 days
3. **LTV estimate** — active retainers
4. **Margin by offer** — delivery cost vs price
5. **Founder time by activity** — sales vs delivery vs ops
6. **Risk register refresh**
7. **ICP refresh** — disqualifiers update
8. **Pricing review** — within range ok
9. **Partner review** — active partners ROI
10. **Strategic bets check** — see `COMMERCIAL_STRATEGY_AR.md` §9

**المخرج:** Monthly Report + 90-day plan update

### 4.2 منتصف الشهر — Mid-month check (30 دقيقة)
- هل نحن في المسار؟
- أي motion يحتاج دعم؟
- أي partner يحتاج attention؟
- أي ICP نشط؟

---

## 5. الإيقاع ربع السنوي (Quarterly)

### 5.1 Quarterly Strategy Review (نصف يوم)
1. هل استراتيجيتنا صحيحة؟ (3 horizons)
2. هل wedge لسه صالح؟
3. هل نوسّع لـ segment جديد؟
4. هل نغيّر pricing؟
5. هل نضيف partner type؟
6. هل نقفل motion؟

### 5.2 Quarterly Team/Advisor Review
- هل نحتاج توظيف؟
- هل نحتاج advisor/board؟
- هل نحتاج partner type جديد؟

---

## 6. Founder Time Allocation (المؤسس — التوزيع)

### 6.1 Default (Stage 1)
- 40% — Sales (calls, proposals, channel engagement)
- 20% — Delivery oversight (not hands-on)
- 20% — Strategic + system building
- 10% — Customer success
- 10% — Admin/finance

### 6.2 When Delivery Burden High (> 50%)
- ⚠️ Hire/contract immediately
- ⚠️ Or raise price
- ⚠️ Or reject low-margin deals

### 6.3 When Sales Pipeline Low (< 4 weeks)
- ⚠️ Increase content output
- ⚠️ Increase warm outreach
- ⚠️ Activate partner network
- ⚠️ Re-evaluate ICP

---

## 7. The 5-Question Daily Filter

كل يوم، قبل أي إجراء، أجِب:

1. **من هو المستهدف؟** (ICP/Persona/Stage)
2. **ما الـ offer المناسب؟** (Pain → Offer match)
3. **ما الـ approval level؟** (Per `approval_policy.yaml`)
4. **ما الـ evidence؟** (Source + L-level)
5. **ما الـ next action؟** (1 شيء واحد، قابل للقياس)

---

## 8. Anti-Patterns (ماذا لا يفعل المؤسس)

### 8.1 لا يفعل ❌
- ❌ يقفز على 5 leads بدون qualification
- ❌ يبعث cold messages بنفسه (وكيل أفضل)
- ❌ يغيّر pricing عشوائياً
- ❌ يقبل discount بدون reason
- ❌ يرسل proposal قبل discovery
- ❌ يضيع ساعتين على TikTok/Instagram يومياً
- ❌ يقبل client spam
- ❌ يعمل custom heavy build بدون scope

### 8.2 يفعل ✅
- ✅ يحترم daily/weekly rhythm
- ✅ يسجّل evidence يومياً
- ✅ يراجع weekly retro
- ✅ يحمي وقت strategic (لا meetings زائدة)
- ✅ يقرأ reports قبل اتخاذ قرار
- ✅ يلتزم approval levels
- ✅ يحتفظ بـ "no" list (bad-fit clients)

---

## 9. Founder Energy Management

### 9.1 High-Energy Tasks (صباح)
- Discovery calls
- Strategic decisions
- Complex proposals
- Partner negotiations

### 9.2 Low-Energy Tasks (مساء)
- Email triage
- CRM updates
- Pipeline cleanup
- Social posts

### 9.3 No-Energy Days (إجازة)
- يوم السبت: off
- آخر يوم من الشهر: half day
- بعد quarterly review: half day

---

## 10. Tools to Run the Rhythm

| الأداة | الاستخدام | الأمر |
|--------|-----------|--------|
| Cockpit | daily | `/[locale]/ops/founder` |
| War Room | daily | `/[locale]/ops/war-room` |
| Sales | daily | `/[locale]/ops/sales` |
| Approvals | daily | `/[locale]/ops/approvals` |
| Evidence | daily | `python scripts/founder_evening_evidence.py` |
| Daily plan | morning | `bash scripts/run_founder_commercial_day.sh` |
| Weekly plan | Sunday | `bash scripts/founder_weekly_loop.sh` |
| Monthly close | 1st of month | `python scripts/founder_weekly_metrics_bundle.py` |
| Quarterly review | quarterly | manual doc |

---

## 11. The Cadence — Visual

```
┌─────────────────────────────────────────────────────────────┐
│  Sunday → Weekly Review (45 min) + plan next week          │
│  Mon-Fri → Morning 5 min + Mid 30 min + Evening 5 min     │
│  Saturday → Off                                            │
│                                                              │
│  Day 1 of month → Monthly Close (2 hr)                     │
│  Mid month → Mid check (30 min)                            │
│                                                              │
│  Quarterly → Strategy Review (half day)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 12. لما تطلع عن المسار (When Off-Track)

### 12.1 Detection
- Weekly review reveals: conversion drop, channel ROI down, churn up
- Daily ops: pipeline stagnant, no events logged
- Energy: founder exhausted by Friday

### 12.2 Recovery
1. **Stop** new lead generation
2. **Triage** open pipeline
3. **Focus** on best 3 opportunities
4. **Cut** low-ROI channels
5. **Reset** rhythm (إجازة قصيرة OK)
6. **Re-plan** next week (only 1 decision)

---

## 13. The One-Page Founder Card (للطباعة)

```
┌────────────────────────────────────────┐
│  DAILY (5+30+5 min)                    │
│  Morning: pipeline + war room + risks  │
│  Mid: calls + proposals                │
│  Evening: 1 event + tomorrow drafts    │
│                                        │
│  WEEKLY (Sunday, 45 min)               │
│  Pipeline + Channel + ICP + Health     │
│  + Finance + Risk + 1 decision         │
│                                        │
│  MONTHLY (1st, 2 hr)                   │
│  Close + CAC + LTV + Margin + Refresh  │
│                                        │
│  NEVER                                 │
│  - send without approval               │
│  - final price without discovery       │
│  - guaranteed claims                   │
│  - skip evidence                       │
└────────────────────────────────────────┘
```

---

**هذا الإيقاع يربط كل يوم بوضوح: أنا أعرف ماذا أفعل، لماذا، ومتى، وبأي موافقة. لا غموض، لا فوضى، لا إنهاك.**
