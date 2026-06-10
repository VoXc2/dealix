# Enterprise Deal Risk Review — مراجعة مخاطر الصفقات

> **Status:** READY (structure) / PARTIAL (signals — تحتاج calibration من أول 5 صفقات)
> **Evidence Level:** assumption (design-time framework)
> **Owner:** Sales Lead (Primary) · Founder (Secondary)
> **الاستخدام:** مراجعة أسبوعية لكل صفقة مؤسسية نشطة.

---

## 1. الهدف

**Enterprise Deal Risk Review** اجتماع أسبوعي (30–45 دقيقة) لـ:
1. رصد المخاطر في 9 فئات معيارية.
2. تعيين مالك التصعيد لكل خطر.
3. تحديث `deal_risks.jsonl`.
4. اتخاذ قرار: متابعة / تجميد / تفكيك / تصعيد.

> **القاعدة: لا تنتظر أن تسقط الصفقة لتكتشف الخطر. الرصد المبكر = الإنقاذ.**

---

## 2. الفئات التسعة للمخاطر

### 2.1 Champion Risk (خطر البطل)

| البُعد | التفصيل |
|--------|---------|
| **إشارات الرصد** | صمت > 14 يوم، تغيير الدور/الإدارة، تسرّب في رسائله للزملاء، EB يستقبلنا بدون علمه |
| **التخفيف** | تنشيط العلاقة، مكالمة مخصّصة، إعطاؤه Quick Win، جلسة 1:1 مع Founder |
| **مالك التصعيد** | Sales Lead → Founder |

### 2.2 Economic Buyer Risk (خطر صانع القرار الاقتصادي)

| البُعد | التفصيل |
|--------|---------|
| **إشارات الرصد** | لم يُقابل بعد، أو مُقابل ولكن لا يرد على رسائل، أو يطلب تأجيلًا متكررًا |
| **التخفيف** | طلب إدخال EB مبكرًا، تحضير Business Case مخصّص، ربط المشروع بأهدافه الشخصية |
| **مالك التصعيد** | Sales Lead → Founder |

### 2.3 Technical Risk (خطر تقني)

| البُعد | التفصيل |
|--------|---------|
| **إشارات الرصد** | Technical Reviewer يطلب مراجعة طويلة، قائمة استثناءات API، اختبارات أداء |
| **التخفيف** | تقديم Architecture Overview، Sandbox demo، ضمان عدم تغيير Stack |
| **مالك التصعيد** | Sales Lead + Solutions Architect |

### 2.4 Security Risk (خطر أمني/خصوصية)

| البُعد | التفصيل |
|--------|---------|
| **إشارات الرصد** | Security questionnaire طويل جدًا، CISO بطيء في الرد، طلبات DPA غير معتادة |
| **التخفيف** | Security pack مُسبّق، DPA موقّع مسبقًا، مكالمة CISO مباشرة، عرض Data Residency |
| **مالك التصعيد** | Founder + CISO العميل |

### 2.5 Procurement Risk (خطر المشتريات)

| البُعد | التفصيل |
|--------|---------|
| **إشارات الرصد** | طلب بنود خارج MSA، طلبات T&C جديدة، تجمد الجدول الزمني |
| **التخفيف** | إرسال MSA + SOW مُسبّقًا، عرض Liability Cap placeholders، تصعيد Procurement Director |
| **مالك التصعيد** | Founder |

### 2.6 Timeline Risk (خطر الجدول الزمني)

| البُعد | التفصيل |
|--------|---------|
| **إشارات الرصد** | أي مرحلة في MAP لم تتقدم > 14 يومًا، إعادة جدولة متكررة، مواعيد مفقودة |
| **التخفيف** | إعادة تصميم MAP، ضغط المراحل، تقسيم Pilot لنسخة أصغر |
| **مالك التصعيد** | Sales Lead → Founder |

### 2.7 Budget Risk (خطر الميزانية)

| البُعد | التفصيل |
|--------|---------|
| **إشارات الرصد** | العميل يقول "ميزانيتنا ضاقت"، أوضاع Economy، تغيير في أولويات |
| **التخفيف** | إعادة تسعير (placeholder، تتطلب Founder approval)، نموذج دفع مرن، تقصير Pilot |
| **مالك التصعيد** | Founder + EB |

### 2.8 Competitive Risk (خطر تنافسي)

| البُعد | التفصيل |
|--------|---------|
| **إشارات الرصد** | العميل يُقارنك بمزوّد آخر، قائمة shortlist، تواصل مفاجئ من مزوّد منافس |
| **التخفيف** | تمييز العرض (TCO، Security، Speed)، Reference calls، جلسة Q&A مع Blocker |
| **مالك التصعيد** | Sales Lead + Founder |

### 2.9 Internal Change Risk (خطر تغيير داخلي)

| البُعد | التفصيل |
|--------|---------|
| **إشارات الرصد** | تغيير في EB/Champion/Business Owner، Reorg، M&A، تغيير في الـ OKRs |
| **التخفيف** | إعادة رسم Stakeholder Map، عقد جلسة تعريفية مع الوافدين الجدد، إعادة بناء Coalition |
| **مالك التصعيد** | Founder |

---

## 3. قالب المراجعة الأسبوعية (Weekly Review)

> **يُعقد يوم الإثنين صباحًا (أو يوم حدّدته المؤسسة). 30–45 دقيقة.**

### Agenda
| الوقت | النشاط |
|------|--------|
| 00–05 | مراجعة المؤشرات الإجمالية (عدد الصفقات النشطة، توزيع Severity) |
| 05–30 | مراجعة كل صفقة نشطة (≤ 6 صفقات) — 4 دقائق لكل صفقة |
| 30–40 | اتخاذ قرارات (تجميد، تفكيك، تصعيد، تخصيص مالك جديد) |
| 40–45 | Tasks للأسبوع (تحديث JSONL، تواصل مع Champions) |

### قالب الاجتماع لصفقة واحدة (4 دقائق)

```markdown
## [Account Placeholder] — Stage: [Stage]

### Health
- آخر تواصل: [Date]
- Multi-Threading Index: [N] stakeholders
- أيام في المرحلة الحالية: [N]

### Risks (مأخوذة من JSONL)
| Category | Severity | Status | Owner |
|----------|----------|--------|-------|
| champion | high | mitigating | Sales Lead |
| procurement | medium | open | Founder |

### Decisions
- [Continue / Freeze / Deconstruct / Escalate]

### Next 7 Days
- [ ] [Action 1] — [Owner] — [Date]
- [ ] [Action 2] — [Owner] — [Date]
```

---

## 4. Severity Levels

| Severity | الوصف | الاستجابة |
|----------|------|----------|
| **low** | يمكن معالجته ضمن الـ Cadence العادي | لا إجراء خاص |
| **medium** | يحتاج تركيز هذا الأسبوع | تدخل Sales Lead |
| **high** | يهدّد الصفقة | تدخل Founder خلال 48 ساعة |

---

## 5. KPIs

| المؤشر | الهدف placeholder |
|--------|-------------------|
| عدد المخاطر المفتوحة / الصفقة النشطة | tracked |
| متوسط زمن إغلاق المخاطرة (بالأيام) | tracked |
| نسبة الصفقات المتأثرة بمخاطر high | tracked |
| توزيع Severity عبر الـ Pipeline | tracked (يُعرض في التقرير) |

---

## 6. ربط بالـ Systems الأخرى

- **TAP** — `account.risks[]` (نفس الفئات).
- **MAP** — `stages[].risk` (مرتبط).
- **Schema:** `schemas/enterprise_deal_risk.schema.json` و `data/enterprise_sales/deal_risks.jsonl`.

---

## 7. القواعد الصارمة (Non-Negotiable)

1. **كل صفقة نشطة** يجب أن يكون لها ≥ 1 risk item على الأقل (افتراضي: `timeline`).
2. **كل risk item عالي (high)** يجب أن يكون له `escalation_owner` ≠ null.
3. **مراجعة أسبوعية** بدون استثناء (حتى لو 0 مخاطر).
4. **لا تُغلق مخاطرة** بدون توثيق السبب في `notes`.

---

> **آخر تحديث:** 2026-06-03 · v0.1
