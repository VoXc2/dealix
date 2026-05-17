# Dealix — Execution Roadmap
> 24h / 7d / 30d. Each item: deliverable • owner • dependency • DoD • metric • risk.

## Next 24 Hours (by end of 2026-04-24)

### R1. CI green
- **Deliverable**: all CI jobs pass on main
- **Owner**: Dealix agent (in this PR)
- **Dependency**: none
- **DoD**: `gh run list --branch main --limit 1` shows success
- **Metric**: 0 CI failures for 24h
- **Risk**: new commit introduces regression → mitigated by PR gate

### R2. Marketers/Pricing/Partners pages live
- **Deliverable**: 3 HTML pages accessible from main landing
- **Owner**: Dealix agent (in this PR) + Sami (Railway deploy verify)
- **Dependency**: Railway auto-deploy from main
- **DoD**: curl 200 on all 3 URLs post-deploy
- **Metric**: each page has ≥10 visits in first 48h
- **Risk**: Railway cache → manual purge

### R3. Sentry → Slack alerts wired
- **Deliverable**: real error reaches Slack within 60s
- **Owner**: Sami (15 min manual)
- **Dependency**: Slack workspace
- **DoD**: test error delivered
- **Metric**: 100% of new Sentry issues reach channel
- **Risk**: Slack webhook expiry → alert on it

### R4. UptimeRobot on /healthz
- **Deliverable**: external monitor active
- **Owner**: Sami (10 min)
- **Dependency**: UptimeRobot free account
- **DoD**: monitor shows "up", alert tested by stopping Railway
- **Metric**: uptime ≥99.5% this week
- **Risk**: free tier 5-min interval → acceptable

### R5. PostHog key set in landing
- **Deliverable**: `window.POSTHOG_KEY` defined, events firing
- **Owner**: Sami (5 min)
- **DoD**: Live events in PostHog show `*_viewed` events
- **Metric**: ≥5 distinct sessions tracked
- **Risk**: adblock → acceptable noise

---

## Next 7 Days (by 2026-04-30)

### W1. 1 SAR payment E2E test
- **Deliverable**: real invoice → real payment → DB update → alerts
- **Owner**: Sami
- **Dependency**: Moyasar secret rotated (W2)
- **DoD**: row in leads where status='paid' exists
- **Metric**: end-to-end latency <30s
- **Risk**: webhook signature fail → signature fix via W2

### W2. Moyasar secret rotated
- **Owner**: Sami (5 min)
- **DoD**: old secret fails, new passes
- **Risk**: briefly, window where webhook may fail mid-rotation → acceptable

### W3. First 30 outreach messages sent
- **Owner**: Sami (90 min/day × 5 days)
- **Deliverable**: 30 SME DMs + 5 agencies + 2 VCs
- **DoD**: tracker has 37+ rows
- **Metric**: ≥7 replies (20%)
- **Risk**: LinkedIn rate limit → spread across platforms

### W4. Calendly webhook → CRM
- **Owner**: Dealix agent (new PR)
- **Deliverable**: `/api/webhooks/calendly` route + lead status update
- **DoD**: booking changes lead.stage to demo_booked in <10s
- **Metric**: 100% of Calendly bookings synced

### W5. Backup & restore drill documented
- **Owner**: Sami
- **Deliverable**: `docs/runbooks/restore_drill.md` + first drill run
- **DoD**: staged restore verified
- **Risk**: Railway snapshot format changes → acceptable risk

### W6. Partner form data collection live
- **Deliverable**: Formspree or Airtable form alive, submissions landing in inbox
- **Owner**: Sami (replace `YOUR_ID` in partners.html with real Formspree ID)
- **DoD**: test submission reaches email
- **Metric**: ≥1 real partner application by day 14

---

## Next 30 Days (by 2026-05-23)

### M1. First paying customer (even 1 SAR pilot)
- **Deliverable**: signed + paid + onboarded
- **Owner**: Sami
- **DoD**: customer using product actively for 7+ days
- **Metric**: 1 active pilot
- **Risk**: 0 conversions → pivot messaging, increase volume

### M2. 2 partners signed (Certified tier)
- **Owner**: Sami
- **DoD**: 2 signed partner agreements
- **Metric**: each has ≥1 prospect passed

### M3. ZATCA e-invoice readiness assessment
- **Owner**: Sami + accountant
- **Deliverable**: 1-page memo: do we need it now? when? cost?
- **DoD**: decision documented

### M4. Content: 4 Arabic articles published
- **Topics**: "كيف تقفل مواعيد من WhatsApp"، "أتمتة المبيعات للSMEs"، "دليل الوكالات للشراكة"، "حساب ROI لنظام AI"
- **Owner**: Sami
- **Channel**: LinkedIn + blog on Dealix site (P2 blog)

### M5. Case study #1 (even placeholder)
- **Deliverable**: one real case (can be pilot) written up
- **Metric**: visitor → case study page → CTA click ≥ 5%

### M6. Financial model updated with real data
- **Deliverable**: update `dealix_financial_model.md` with actual funnel metrics
- **Owner**: Sami
- **DoD**: real CAC, conversion, churn numbers from first 30 days

---

## Critical Path Dependencies
```
CI green  →  deploy landing pages  →  PostHog tracking
                                  →  Sentry alerts
                                  →  UptimeRobot
Moyasar rotation  →  1 SAR test  →  first real invoice
Outreach volume  →  demos  →  pilots  →  first paid
```

## Non-negotiables
- No feature work before first paid customer
- No automation of partner commissions before 3 real partners
- No ZATCA integration before legal threshold reached
- No new AI features before funnel measured

## Weekly review cadence
Every Sunday 8:00 AM KSA:
- Review tracker
- Update metrics
- Adjust priorities
- Reset daily cadence for the week

---

## 30-day wedge-proof plan — خطة إثبات الإسفين في 30 يوماً

The 30-day milestones above set the outcomes. This plan sets the founder's weekly
execution rhythm to reach them — one wedge, proven, then scaled. معالم الـ 30 يوماً
أعلاه تحدّد النتائج؛ هذه الخطة تحدّد إيقاع التنفيذ الأسبوعي للمؤسس للوصول إليها —
إسفين واحد، يُثبَت، ثم يُوسَّع.

### Week 1 — Wedge Proof / الأسبوع 1 — إثبات الإسفين

- 20 agency targets / 20 هدفاً من الوكالات.
- 50 manual touches / 50 تواصلاً يدوياً.
- 10 follow-ups / 10 متابعات.
- 2 demos / عرضان.
- 1 pilot offer / عرض Pilot واحد.

### Week 2 — First Proof / الأسبوع 2 — أول إثبات

- 1 pilot or written commitment / Pilot واحد أو التزام مكتوب.
- Delivery within 48h / تسليم خلال 48 ساعة.
- Proof Pack v1 / حزمة إثبات النسخة 1.
- Referral ask / طلب إحالة.
- First anonymized insight / أول رؤية مجهّلة.

### Week 3 — Partner Loop / الأسبوع 3 — حلقة الشركاء

- 10 partner conversations / 10 محادثات مع شركاء.
- 2 co-selling opportunities / فرصتا بيع مشترك.
- 1 mini workshop / ورشة مصغّرة واحدة.
- 5 partner / affiliate applications / 5 طلبات شراكة أو إحالة.

### Week 4 — Scale / الأسبوع 4 — التوسّع

- Double the best message / ضاعِف أفضل رسالة.
- Stop the weak channel / أوقِف القناة الضعيفة.
- Offer Sprint on the first proof / اعرض Sprint بناءً على أول إثبات.
- Prepare the first case-style post / جهّز أول منشور بأسلوب دراسة الحالة.
- Start small retargeting **only if there is traffic** / ابدأ إعادة استهداف صغيرة
  **فقط إذا وُجدت زيارات**.

Scaling never invents a price or an outcome claim. Any Sprint offer in Week 4
draws its figures from the canonical offer registry in
[`../../COMMERCIAL_WIRING_MAP.md`](../../COMMERCIAL_WIRING_MAP.md), and the
case-style post reports patterns only — no guaranteed revenue, ROI, or compliance.
التوسّع لا يخترع سعراً ولا ادعاء نتيجة؛ المنشور يعرض أنماطاً فقط دون ضمان.
