# Enterprise Pipeline Review — مراجعة خط المبيعات المؤسسي

> **Generated:** 2026-06-03 · v0.1
> **Scope:** الصفقات الثلاث الموضّحة في `data/enterprise_sales/accounts.jsonl`
> **Owner:** Sales Lead

---

## 1. ملخص الـ Pipeline

| الحساب | القطاع | Tier | Stage الحالي | آخر تحديث | أيام في المرحلة |
|--------|--------|------|--------------|-----------|-----------------|
| ACC-ENT-001 (شركة_X_صناعية) | industrial | tier_1 | prospect | 2026-06-03 | 3 (دخلت prospect حديثًا) |
| ACC-ENT-002 (ExampleCo KSA - Healthcare) | healthcare | tier_1 | discovery | 2026-06-03 | 14 (دخلت discovery في 20 مايو) |
| ACC-ENT-003 (شركة_Y_تجزئة) | retail | tier_2 | prospect | 2026-06-03 | 5 |

> **Total:** 3 حسابات نشطة، 2 منها Tier-1، 1 Tier-2. لا حسابات في المراحل المتقدمة بعد (هذا طبيعي لـ design-time).

---

## 2. حالة الحسابات تفصيليًا

### 2.1 ACC-ENT-001 (شركة_X_صناعية)

**الحالة العامة:** في بداية `prospect`، على وشك الدخول في Discovery.

| البُعد | الحالة |
|--------|--------|
| **MAP.current_stage** | لا يوجد MAP بعد (لم تبدأ `discovery`) |
| **Multi-Threading Index** | 0 من 4 stakeholders engaged (3 not_contacted, 1 intro_made) |
| **Open Risks** | 2 — `champion` (medium) و `competitive` (high) |
| **Blocker رئيسي** | منافس سبقنا في 3 عروض |
| **Next Action** | إرسال رسالة تعريفية لـ CRO عبر LinkedIn |

**المرحلة القادمة المتوقعة:** `discovery` (خلال أسبوعين).

**العقبات:**
- CRO لم يستقر في منصبه.
- CFO لم يُقابل بعد.
- لا EB touch حتى الآن.

**7-Day Actions:**
- [ ] Sales Lead: رسالة LinkedIn مخصّصة لـ CRO (STK-001).
- [ ] Sales Lead: طلب إحالة من STK-001 لـ CFO.
- [ ] Sales Lead: Comparison Sheet محايدة للتحضير للأسئلة التنافسية.

---

### 2.2 ACC-ENT-002 (ExampleCo KSA - Healthcare)

**الحالة العامة:** أبعد من ACC-ENT-001. في مرحلة `discovery` وقد بدأ `pilot_scope` يُحدَّد.

| البُعد | الحالة |
|--------|--------|
| **MAP.current_stage** | `problem_confirmation` (مكتمل) — الآن في `pilot_scope` |
| **Multi-Threading Index** | 1 من 5 stakeholders engaged (STK-005 = COO) |
| **Open Risks** | 2 — `economic_buyer` (high) و `security` (high) |
| **Blocker رئيسي** | EB Family approval بطيء + حساسية بيانات المرضى |
| **Next Action** | تسليم Pilot SOW إلى COO |

**المرحلة القادمة المتوقعة:** `pilot_scope` (خلال أسبوع).

**العقبات:**
- CEO/Board Family لا يرد.
- Compliance Lead لم يُقابل بعد.
- لا EB touch.

**7-Day Actions:**
- [ ] Sales Lead: جدولة مكالمة COO + Founder (15 دقيقة) لتفعيل العلاقة.
- [ ] Sales Lead: تقديم Pilot SOW مُحدَّث للـ COO.
- [ ] Founder: رسالة مباشرة لـ CEO (Board Family sponsor).
- [ ] Sales Lead: جدولة مكالمة CISO/Compliance Lead.

---

### 2.3 ACC-ENT-003 (شركة_Y_تجزئة)

**الحالة العامة:** في `prospect`، طلب PoV 4 أسابيع.

| البُعد | الحالة |
|--------|--------|
| **MAP.current_stage** | لا يوجد MAP (لم تبدأ discovery) |
| **Multi-Threading Index** | 1 من 3 stakeholders engaged (STK-010 = Head of E-com) |
| **Open Risks** | 2 — `budget` (medium) و `timeline` (medium) |
| **Blocker رئيسي** | ميزانية Marketing تحت ضغط |
| **Next Action** | إرسال PoV proposal إلى Head of E-com |

**المرحلة القادمة المتوقعة:** `discovery` (خلال أسبوع).

**العقبات:**
- لا اتصال بعد مع CMO أو Daily User.
- 3 مزوّدين منافسين في نفس PoV stage.

**7-Day Actions:**
- [ ] Sales Lead: إرسال PoV proposal محدّث لـ STK-010.
- [ ] Sales Lead: طلب إحالة لـ CMO (STK-011).
- [ ] Sales Lead: Dashboard demo مسبق لـ STK-012 (Daily User).

---

## 3. مقارنة بين الحسابات

| المؤشر | ACC-001 | ACC-002 | ACC-003 |
|--------|---------|---------|---------|
| **Stage** | prospect | discovery (pilot_scope draft) | prospect |
| **Tier** | 1 | 1 | 2 |
| **Multi-threading** | 0/4 | 1/5 | 1/3 |
| **Open Risks (high)** | 1 | 2 | 0 |
| **EB Touch** | ❌ | ❌ | ❌ |
| **Pilot SOW** | ❌ | 🔄 in progress | ❌ |
| **Days in stage** | 3 | 14 | 5 |

> **لا حساب وصل إلى `proposal`. هذا متوقع لـ design-time — لا صفقات حقيقية موجودة.**

---

## 4. التوزيع حسب Stage

| Stage | عدد |
|-------|-----|
| prospect | 2 |
| discovery | 1 |
| problem_confirmation → pilot_scope | 1 (نفس الحساب) |
| security_privacy_review → ... | 0 |
| proposal → ... | 0 |

---

## 5. مخاطر حرجة (هذا الأسبوع)

| الحساب | الفئة | الشدّة | المالك |
|--------|-------|--------|--------|
| ACC-001 | competitive | high | Sales Lead + Founder |
| ACC-002 | economic_buyer | high | Sales Lead + Founder |
| ACC-002 | security | high | Founder + Compliance Lead |

> **3 مخاطر high/4 = 75%. تركيز الأسبوع: ACC-002.**

---

## 6. التوصيات

1. **أولوية قصوى:** فتح قناة EB في ACC-001 و ACC-002 — بدون EB لا صفقة.
2. **دعم ACC-003:** 7-Day Actions يجب أن تنفّذ كاملة هذا الأسبوع لبدء Discovery.
3. **حركة Trust:** Founder يجب أن يحضر ≥ 1 لقاء لكل حساب Tier-1 خلال أسبوعين.
4. **تحديث أسبوعي:** هذا التقرير يُعاد كل يوم اثنين صباحًا.

---

> **آخر تحديث:** 2026-06-03 · v0.1
