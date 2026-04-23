# Dealix — Customer Onboarding Playbook

## دليل الـ 14 يوم للعميل الأول: من التوقيع إلى التبنّي الكامل

**المبدأ:** العميل اللي يوصل لـ first value خلال أسبوع — retention rate عنده 90%+. اللي ما يوصل — يُلغي خلال 60 يوم.

---

## قبل Day 1: التحضير

### لك (Sami):
- [ ] العقد موقّع ومستلم
- [ ] أول دفعة نجحت في Moyasar
- [ ] حساب admin أُنشئ في Dealix
- [ ] رسالة ترحيب مُجدولة للإرسال Day 1 8:00 ص
- [ ] Calendly kickoff call مؤكد (Day 1 10:00 ص)

### للعميل:
- [ ] قائمة المستخدمين (أسماء + إيميلات + أدوار)
- [ ] CRM حالي (اسمه + وصول للتصدير)
- [ ] 5-10 leads نموذجية جاهزة للاستيراد
- [ ] صلاحيات IT (SSO إن طُلب)

---

## اليوم 1 — Kickoff

### 8:00 ص — Email ترحيب

**Subject:** `أهلاً [اسم العميل] — رحلتك مع Dealix بدأت`

```
السلام عليكم [الاسم]،

مرحباً بك في عائلة Dealix.

اليوم يبدأ الـ 14 يوم الأهم — هدفنا: أن يكون فريقك منتج بالكامل
على المنصة بنهاية أسبوعين.

مرفق:
1. Welcome kit PDF
2. روابط الوصول (SSO/username)
3. جدول الـ onboarding

لقاء اليوم 10:00 ص عبر Google Meet: [الرابط]

في حال أي سؤال: أنا شخصياً مسؤول عن رحلتك الأولى.
رقمي المباشر: [WhatsApp]

أهلاً،
سامي العسيري
Founder & (مؤقتاً) CS Lead
Dealix
```

### 10:00 ص — Kickoff Call (60 دقيقة)

**Agenda:**
1. (5د) تعارف الفريق
2. (10د) إعادة تأكيد الأهداف (من discovery call)
3. (15د) جولة سريعة على dashboard
4. (10د) جدول الـ 14 يوم
5. (10د) تخصيص success metrics
6. (5د) Q&A
7. (5د) Next steps

**تُنتج من الجلسة:**
- Shared doc: `[Company]_Dealix_Success_Plan.md`
- 3 success metrics متفق عليها
- قائمة المستخدمين النهائية
- موعد تدريب الفريق (Day 3)

### 4:00 م — رسالة متابعة

```
شكراً [الاسم] على الوقت اليوم.

الملخص:
- أهدافك: [A، B، C]
- Success metrics: [1، 2، 3]
- اجتماعاتنا التالية: [Day 3، Day 7، Day 14]

اليوم 2 — سنشتغل على data migration.
جهز export من [CRM القديم] بصيغة CSV.

شكراً،
سامي
```

---

## اليوم 2 — Data Migration

### الصباح
- [ ] استلام CSV من العميل
- [ ] Map الأعمدة لـ Dealix schema
- [ ] Import dry-run على sandbox
- [ ] تأكد لا توجد duplicates أو missing required fields
- [ ] Import على production (مع backup قبل)

### بعد الظهر
- [ ] إرسال تقرير import:
  - X leads مُستوردة
  - Y duplicates مُدمجة
  - Z مشاكل (مع حل لكل مشكلة)

```
[الاسم]، Data migration اكتمل:

✅ 847 lead مُستورد
✅ 23 duplicate مدمج
⚠️  12 lead ناقصها email — راجعها هنا: [رابط]

بكرة Day 3 — تدريب الفريق.
Agenda مرفق.
```

---

## اليوم 3 — تدريب الفريق

### الجلسة 1 (45 دقيقة): للمستخدمين العاديين
- تسجيل الدخول
- إضافة lead جديد
- تحديث stage
- إضافة ملاحظة
- البحث والفلترة
- Mobile app

### الجلسة 2 (30 دقيقة): للـ managers
- Pipeline view
- التقارير الأساسية
- Assignment & routing
- Alerts & notifications

### الجلسة 3 (30 دقيقة): للـ admins
- User management
- Custom fields
- Workflow automation
- Integrations
- Audit log

### بعد التدريب:
- [ ] إرسال recording لمن لم يحضر
- [ ] cheat sheet PDF للمستخدمين
- [ ] دعوة لـ Slack/WhatsApp group

---

## اليوم 4-6 — Soft Launch

### اليوم 4: فريق محدود (3-5 مستخدمين)
- استخدام فعلي لـ نصف يوم
- جمع feedback في اليوم التالي
- إصلاح أي مشكلة عاجلة

### اليوم 5: Check-in (15 دقيقة)
أسئلة مُحددة:
1. ما أعظم تحدي واجهك اليوم؟
2. ما الشي اللي اشتغل بسلاسة؟
3. هل اكتشفت ميزة ما تعرفها؟
4. هل فيه شي تبينا نضيفه/نعدله؟

### اليوم 6: إطلاق كامل الفريق
- Go/no-go call 9:00 ص
- إن go: notification لكل الفريق
- مراقبة live للـ 4 ساعات أولى

---

## اليوم 7 — Week 1 Review

### KPIs الـ 7 أيام (مقارنة بالـ baseline)
| Metric | قبل | بعد | التغيير |
|--------|-----|-----|---------|
| Active users | - | - | - |
| Leads created | - | - | - |
| Stage transitions | - | - | - |
| Time per lead | - | - | - |

### الجلسة (30 دقيقة)
1. استعراض KPIs
2. ما الذي اشتغل؟
3. ما التحديات؟
4. تعديلات للأسبوع الثاني
5. Quick wins للأسبوع الجاي

**Output:** Week 2 action plan مُوقّع من الطرفين.

---

## اليوم 8-12 — Deepen Usage

### التركيز على Advanced Features
- Day 8: Workflow automations (أول 3)
- Day 9: Custom reports (أول 2)
- Day 10: Email/WhatsApp templates
- Day 11: Integration مع CRM ثاني (إن موجود)
- Day 12: Mobile app adoption

### Daily check-in (5 دقائق كل يوم)
عبر Slack/WhatsApp:
```
Good morning. Dealix pulse:
- Active users أمس: X من Y
- Leads added: Z
- Any blockers?
```

---

## اليوم 13 — Deep Dive

### Quarterly Business Review (60 دقيقة)
مع: decision maker (CEO/CRO) + Sami

**Agenda:**
1. (15د) نتائج الـ 14 يوم vs الأهداف
2. (15د) ROI الفعلي المحقق
3. (15د) رحلة الـ 90 يوم القادمة
4. (10د) طلبات features
5. (5د) references + referrals

**Output:**
- Success scorecard
- 90-day roadmap
- NPS survey
- طلب case study (إن النتائج قوية)

---

## اليوم 14 — Handoff

### Formal Handoff للـ CSM الدائم (عند scaling)
- توثيق كامل في shared doc
- Introduction للـ CSM الجديد
- Weekly → Monthly check-in cadence
- Escalation path واضح

### رسالة ختامية
```
[الاسم]، مبروك — اكتملت رحلة onboarding الرسمية.

النتائج:
- [KPI 1]: +X%
- [KPI 2]: Y عدد
- [KPI 3]: Z ريال

من اليوم:
- Monthly check-in: [الموعد]
- Support SLA العادي مفعّل
- My direct line لا يزال متاح لأي escalation

أفتخر بثقتك، ومتحمس للمرحلة التالية.

سامي
```

---

## متابعة ما بعد Day 14

### Week 3-4: استقرار
- Weekly KPI report آلي عبر Email
- Monthly check-in (30 دقيقة)

### Month 2-3: التوسيع
- Quarterly Business Review
- Feature adoption tracker
- Expansion opportunities (upgrade tier)

### Month 4+: Advocacy
- طلب case study
- طلب referrals
- دعوة لـ customer advisory board
- Beta testing للميزات الجديدة

---

## إشارات الخطر (Red Flags)

| الإشارة | الإجراء الفوري |
|--------|----------------|
| DAU ينخفض 30%+ لأسبوع | Call من Sami في 24 ساعة |
| لا توجد leads مُضافة لـ 5 أيام | Check-in عاجل |
| تذكرة P1 بدون حل | escalation لـ Sami مباشرة |
| عدم حضور check-ins × 2 | Email من Sami شخصياً |
| payment failure | call خلال ساعتين |

---

## قوالب سريعة

### Day 1 Welcome Email — `/templates/welcome.md`
### Data Migration Report — `/templates/migration_report.md`
### Weekly KPI Report — `/templates/weekly_kpi.md`
### QBR Deck — `/templates/qbr_deck.pptx`
### Success Scorecard — `/templates/scorecard.md`

---

## مقاييس نجاح الـ Onboarding

| Metric | Target | Red |
|--------|--------|-----|
| Time to First Value | < 3 أيام | > 7 أيام |
| Week 1 Active Users % | > 80% | < 50% |
| Day 14 Full Adoption | > 90% | < 70% |
| NPS Day 14 | > 50 | < 30 |
| Day 30 Retention | > 95% | < 85% |

**Target الأعلى:** NPS > 70 ويشير العميل لعميل جديد خلال 90 يوم.

---

*آخر تحديث: 2026-04-23*
