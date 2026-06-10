# Procurement Sales Playbook — دليل البيع للمشتريات

> **Status:** READY (structure) / PARTIAL (placeholders فقط في البنود التجارية)
> **Evidence Level:** assumption (design-time playbook)
> **Owner:** Founder (Primary) · Sales Lead (Secondary)
> **الاستخدام:** من مرحلة `procurement` في MAP فصاعدًا.

---

## 1. نظرة عامة على المشتريات السعودية

### 1.1 كيف تعمل المشتريات في المؤسسات السعودية الكبيرة؟

| القطاع | خصوصية Procurement |
|--------|---------------------|
| **حكومي / شبه حكومي** | يمرّ عبر منصة اعتماد أو شبيه، RFP إلزامي، Vendor registration مسبق |
| **صناعي (مدرجة)** | Procurement Department مركزي، Vendor list معتمد، عطاءات محدودة |
| **صناعي (خاصة عائلية)** | قرار مركزي عند المالك، Procurement role إداري |
| **رعاية صحية** | Procurement متخصص، اعتمادات SFDA/NHIC، Vendor risk review |
| **خدمات مالية** | SAMA/BAFILT compliance، Risk Management يشارك، Vendor due-diligence مكثّف |
| **اتصالات** | Vendor Risk Register، SLA صارم، PII handling |

### 1.2 أطراف داخلية يمرّ بهم الطلب
1. **Champion / Business Owner** — يروّج داخليًا.
2. **Procurement Manager** — يجمع عروض، يفاوض، يضيف بنودًا.
3. **Legal Counsel** — يراجع MSA، DPA، SOW.
4. **CFO / Finance** — يعتمد الميزانية.
5. **CISO / DPO** — يعتمد Security/Privacy.
6. **المالك / Board** — يعتمد إن كان المبلغ فوق عتبة.

> **القاعدة: لا تتجاوز Procurement. اعمل معه، لا حوله.**

---

## 2. الفرق بين RFP / RFI / RFQ

| | **RFI (Request for Information)** | **RFP (Request for Proposal)** | **RFQ (Request for Quotation)** |
|---|---|---|---|
| **الهدف** | جمع معلومات عن السوق والمزوّدين | تقييم عروض كاملة (حل + سعر + شروط) | مقارنة أسعار لشراء محدد |
| **الإجابة** | معلومات عامة عن الشركة والقدرات | عرض كامل (Approach + Team + Pricing) | عرض سعر مفصّل |
| **الـ Output** | Vendor shortlist | Vendor selection | PO جاهز |
| **متى نتلقاه** | بداية التأهيل | منتصف عملية الاختيار | بعد اختيار المزوّد |

### كيف نردّ على كلٍّ منها
- **RFI:** أرسل Vendor Profile + Capability Statement.
- **RFP:** رد بـ Proposal كامل + Security Pack + Reference.
- **RFQ:** ردّ بسعر مفصّل (placeholder حتى تأكيد Founder).

---

## 3. المتطلبات (Required Artifacts)

| الوثيقة | الغرض | المكان |
|---------|------|--------|
| **Vendor Profile** | تعريف الشركة، التراخيص، الخبرة | `docs/enterprise/VENDOR_PROFILE_AR.md` |
| **Security Overview** | كيف نحمي البيانات | `docs/enterprise/SECURITY_OVERVIEW_AR.md` |
| **Privacy Overview (PDPL)** | التزامات PDPL | `docs/enterprise/PRIVACY_OVERVIEW_AR.md` |
| **DPA (Data Processing Agreement)** | اتفاقية معالجة البيانات | `docs/enterprise/DPA_DEALIX_FULL.md` |
| **SLA / SLO** | مستوى الخدمة | `docs/enterprise/SLA_SLO_DRAFT_AR.md` |
| **MSA (Master Service Agreement)** | الإطار التعاقدي | يُسحب من `docs/legal/` |
| **SOW (Statement of Work)** | نطاق العمل | يُسحب من Pilot SOW |
| **Security Questionnaire** | استبيان أمني | يُولَّد من `data/enterprise/questionnaires.jsonl` |
| **Insurance Certificates** | تأمين (Cyber, Professional Indemnity) | placeholder — يُحدّد مع Founder |
| **Banking Reference / Tax Certificate** | ملاءة مالية | placeholder |

> **القاعدة: جهّز 9 من 10 قبل أن يُطلب منك. المفاجأة = تأخير.**

---

## 4. اعتراض «لدينا مزوّد حالي»

### 4.1 أنماط الردود
| الردّ | التحليل | الاستجابة |
|------|---------|----------|
| «نحن راضون عن المزوّد الحالي» | لا مشكلة حقيقية | «أقدّر ذلك. أعرض عليكم Pilot محدود لـ [Use Case] يكمل ما عندكم، لا يستبدله.» |
| «مزوّدنا أرخص» | سباق سعر | «السعر جزء من المعادلة. الـ TCO الحقيقي يشمل وقت الفريق، الـ Opportunity Cost، وسرعة التوسّع.» |
| «مزوّدنا أكبر» | ثقلي أسماء | «الحجم ليس ميزة بحد ذاته. اسأل: هل يستخدمون هذا الحجم لخدمتكم بشكل مخصّص؟» |
| «لا نغيّر بسهولة» | Inertia | «أتفهّم. نبدأ بـ Pilot 6–8 أسابيع لا يستبدل شيئًا. يضيف رؤية.» |
| «مزوّدنا متكامل معنا» | Switching cost | «لا تغيير في البنية. نعمل فوق [Stack]. الـ integration في أسبوعين.» |

### 4.2 سكريبت عربي مقترح
> «أقدّر قراركم بالبقاء مع مزوّدكم الحالي. أنا لا أعرض استبدالًا. أعرض Pilot يضيف طبقة [AI Governance / Revenue Visibility / Lead Recovery] فوق ما لديكم، مع نجاح قابل للقياس في 8 أسابيع. إذا لم يُضف قيمة، نخرج. هل تودّ رؤية التصميم المقترح؟»

---

## 5. البنود التجارية (Placeholders فقط)

> **لا توجد أرقام نهائية. كل ما يلي placeholders بانتظار تأكيد Founder.**

### 5.1 شروط الدفع (Payment Terms)
- **نموذج A:** 50% مقدّم + 50% عند التسليم.
- **نموذج B:** دفعات ربع سنوية متساوية.
- **نموذج C:** شهري + Setup Fee.
- **العملة:** SAR افتراضي؛ USD اختياري للمشتريات الدولية.
- **تأخّر الدفع:** [...placeholder...]

### 5.2 حقوق الملكية الفكرية (IP Terms)
- **Pre-existing IP:** ملك لكل طرف.
- **Work Product:** ملك العميل بعد السداد الكامل.
- **AI Model Outputs:** ملك العميل، Dealix يحتفظ بـ tooling IP.
- **Background IP:** Dealix يحتفظ بـ underlying platform IP.
- **ترخيص الاستخدام:** non-exclusive, non-transferable.

### 5.3 تحديد المسؤولية (Liability Terms)
- **Liability Cap:** [نطاق placeholder — founder-confirmed].
- **Carve-outs:** Indemnification لـ IP infringement + Data breach.
- **Force Majeure:** بنود معيارية.
- **Termination for Cause:** 30 days notice + cure period.

> **كل ما سبق placeholders. لا يجوز لـ Sales Lead تعديلها منفردًا — تتطلب مراجعة Founder + Legal.**

---

## 6. المدة الزمنية المتوقعة لـ Procurement

| القطاع | المدة المتوقعة (من Proposal إلى التوقيع) |
|--------|------------------------------------------|
| حكومي | 90–180 يومًا |
| صناعي عام | 45–90 يومًا |
| مالي | 60–120 يومًا |
| صحي | 60–120 يومًا |
| اتصالات | 45–75 يومًا |

> **ضع `timeline risk` في `deal_risks.jsonl` من اليوم الأول.**

---

## 7. مسار التصعيد (Escalation Path)

```
مشكل في Procurement
        ↓
Sales Lead → Procurement Manager
        ↓ (إن فشل)
Founder → Procurement Director
        ↓ (إن فشل)
Founder → EB (Economic Buyer)
        ↓ (إن فشل)
تجميد الصفقة أو إعادة تصميم
```

### متى نصعّد؟
- تأخّر > 30 يومًا من الموعد المتفق.
- طلب بنود خارج MSA template (مثال: Liability Cap = 0).
- طلب تعديلات على DPA.
- تجاهل لرسائل (3 متتالية بدون رد).

### كيف نصعّد بأدب؟
> «أقدّر جهودكم. للعلم، المشروع في انتظار هذا البند منذ [N] يومًا، وأودّ تأكيد استمراريته من جانبنا. هل يمكنني التحدث مع [الاسم] لمدّ الجدول الزمني؟»

---

## 8. Anti-Patterns (تجنّبها)

- ❌ التعامل مع Procurement كـ "gatekeeper". هو شريك.
- ❌ إرسال عرض أسعار بدون SOW.
- ❌ تجاهل بنود قسرية في MSA (مثال: "no liability cap").
- ❌ محاولة إضعاف Procurement Manager أمام زملائه.
- ❌ الوعد ببنود لم يوافق عليها Founder.
- ❌ اختلاق "previous customers" أو "we have a deal with X".

---

## 9. Checklist قبل MSA

- [ ] DPA موقّع مسبقًا (مسودة نظيفة).
- [ ] Security Overview محدّث.
- [ ] Privacy Overview (PDPL) محدّث.
- [ ] SLA SLO متفق عليه.
- [ ] SOW موقّع من العميل.
- [ ] Price band مُؤكَّد من Founder.
- [ ] Insurance Certificates (إن لزم).
- [ ] Tax Certificate (ZATCA).
- [ ] Vendor Registration (اعتماد).
- [ ] Champion sign-off نهائي.

---

## 10. الربط

- [`MUTUAL_ACTION_PLAN_AR.md`](MUTUAL_ACTION_PLAN_AR.md) — المرحلة 6 و 7.
- [`ENTERPRISE_DEAL_RISK_REVIEW_AR.md`](ENTERPRISE_DEAL_RISK_REVIEW_AR.md) — `procurement` و `timeline` risks.
- `docs/enterprise/PROCUREMENT_FAQ_AR.md` — إجابات جاهزة للأسئلة الشائعة.
- `docs/enterprise/DPA_DEALIX_FULL.md` — مرجع DPA.
- `docs/legal/LEGAL_FOUNDER_SELF_EXECUTION.md` — حدود ما يمكن للمؤسس تنفيذه.

---

> **آخر تحديث:** 2026-06-03 · v0.1
