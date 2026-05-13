# دماغ الشركة في 21 يومًا / Company Brain Sprint
## Company Brain Sprint — Customer-Facing Offer Page

---

## المشكلة / The Problem

**AR:** المعرفة المؤسسية موزّعة عبر مئات الملفات في SharePoint وGoogle Drive وOneDrive وإيميل. الموظف الجديد يصرف 15-20 دقيقة بحثًا عن سياسة بسيطة، ويتصل بـ 3 زملاء قبل أن يجد إجابة. مديرو الأقسام يقاطَعون كل ساعة بأسئلة موظفين. AI شات بوت العام لا يعرف وثائقك، ولا يستشهد بالمصدر، ويعطي إجابات قد تخالف سياستك الفعلية.

**EN:** Your institutional knowledge is scattered across hundreds of files in SharePoint, Google Drive, OneDrive, and email. New employees spend 15-20 minutes searching for a basic policy. Department heads are interrupted hourly. Generic AI chat doesn't know your documents, doesn't cite sources, and can give answers that contradict your actual policy.

---

## الوعد / The Promise

**AR:** خلال **21 يوم عمل**، نحوّل ملفاتك إلى مساعد ذكي يعطي **إجابات مُستشهَدة بالمصدر**، يرفض الإجابة إذا لم يجد دليلًا، ويحترم صلاحيات الوصول. القاعدة الذهبية: **لا مصدر = لا إجابة**.

**EN:** In **21 business days**, we turn your files into an internal AI assistant that gives **cited answers**, refuses to answer without evidence, and respects access rules. The hard rule: **no source = no answer**.

---

## ما تستلمه / What You Receive

| البند | التفاصيل |
|---|---|
| 1. استيعاب حتى 500 وثيقة | PDF، Word، Excel، PowerPoint، نصوص، صور (OCR) |
| 2. كشف PII آلي + تنقيح | قبل الفهرسة، حسب `pii_detector.py` |
| 3. RAG مع استشهاد كل إجابة | كل إجابة تأتي بـ [DOC-ID §section] قابل للنقر |
| 4. واجهة استعلام للموظفين | Web + Slack أو Teams (حتى 20 مقعدًا) |
| 5. 3 شخصيات وصول (RBAC) | عام / إداري / سرّي |
| 6. تتبع الحداثة | تنبيه آلي على وثائق > 90 يومًا |
| 7. تدريب فريقك 2 ساعة (مسجّل) | مع scenarios عملية |
| 8. تقرير تنفيذي + حزمة إثبات | شامل eval results |

---

## القاعدة المنتجة الصارمة / Hard Product Rule

**AR:** "لا مصدر = لا إجابة." المساعد **يرفض الإجابة** إذا لم يجد chunk مرجعي معتمد. هذا قرار تصميمي مُتعمَّد، يحمي من الادعاءات المُختلَقة.

**EN:** "No source = no answer." The assistant **refuses to answer** when no qualifying source exists. This is an intentional design choice, protecting you from hallucinated claims.

---

## السعر والشروط / Price & Terms

| البند | القيمة |
|---|---|
| **السعر الثابت / Fixed price** | **SAR 20,000** (ضريبة قيمة مضافة 15% خارج السعر) |
| **المدة / Timeline** | 21 يوم عمل |
| **الدفع / Payment** | 50% عند التوقيع + 50% عند التسليم |
| **عقد / Contract** | SOW جاهز للتوقيع — 6 صفحات |
| **ضمان / Guarantee** | تغطية استشهاد ≥ 95% أو نُعيد المعالجة بدون رسوم إضافية |

---

## غير مشمول (Not Included)

- **لا نستوعب بيانات مرضى/سريرية فردية** (PDPL Art. 27 — البيانات الصحية الحساسة).
- **لا نشغّل** المساعد بدون موافقة على Data Processing Record (PDPL Art. 31).
- لا نضمن إجابة لكل سؤال — نضمن أن **كل إجابة** ستكون مدعومة بمصدر.
- لا استيعاب لأكثر من 500 وثيقة في هذا Sprint (السقف).
- لا نتعامل مع وثائق غير مملوكة لك أو غير مرخصة.
- لا تكامل ERP/CRM داخل Sprint (خارج النطاق، يُتاح في مشروع منفصل).
- لا نقدم استشارات قانونية أو طبية — المساعد يجيب فقط من سياساتك المرفوعة.

---

## مناسب لـ / Best For

- فرق غنية بالوثائق: المبيعات، الموارد البشرية، الدعم، العمليات، الجودة.
- شركات تعاني من نقطة الألم "وين ذاك الـ PDF؟".
- مؤسسات تستعد لشهادة CBAHI / ISO / JCI وتحتاج تتبّع الحداثة.
- مدارس/جامعات/مستشفيات/مؤسسات قطاع حكومي مع corpus ثابت كبير.

---

## كيف تبدو النتيجة / What the Output Looks Like

> "زمن البحث عن سياسة انخفض من 14 دقيقة إلى < 12 ثانية، مع 96.7% تغطية استشهاد و0% تسريب PII."

شاهد نموذج تقرير تنفيذي حقيقي (بيانات اصطناعية لشبكة صحية): `docs/services/company_brain_sprint/sample_output.md`

---

## ضمانات الجودة / Quality Guarantees

| البند | القيمة |
|---|---|
| تغطية الاستشهاد / Citation coverage | ≥ 95% |
| سلوك "لا مصدر = لا إجابة" | 100% على out-of-corpus |
| PII surfacing في إجابات | 0% |
| دقة تحكم الوصول / Access control accuracy | 100% (3 شخصيات اختبار) |
| متوسط زمن الإجابة | ≤ 3 ثوان |
| تتبع الحداثة | آلي > 90 يومًا |
| Prompt-injection robustness | 0/5 محاولات تنجح |
| تغطية audit log | 100% من الاستعلامات |
| PDPL Art. 31 DPIA | مُجهَّز ومُسلَّم |

---

## مسار الترقية / Upgrade Path

بعد Sprint، تختار:

1. **Sales Knowledge Assistant** بسعر SAR 18,000 — مساعد منفصل لفريق المبيعات (عروض، خدمات، شركاء).
2. **Policy Assistant Premium** بسعر SAR 28,000 — توسيع إلى 900 وثيقة + 7 شخصيات + Teams + WhatsApp.
3. **Monthly Knowledge Ops Retainer** بسعر **SAR 7,500/شهريًا** — صيانة فهرس + 20 وثيقة شهريًا + eval refresh + QBR.

---

## خطوة البدء / Call to Action

**AR:** جلسة 45 دقيقة لمراجعة وثائقك مع DPO من Dealix، وتحديد المسار الأنسب. لا التزام. رد بكلمة **"ابدأ"** على أي بريد من Dealix، أو احجز موعدًا مباشرًا.

**EN:** A 45-minute call with a Dealix DPO to review your documents and confirm scope. No commitment. Reply **"start"** to any Dealix email, or book directly.

> **احجز جلستك / Book your slot:** [calendly.com/dealix/company-brain-sprint](#)
> **أو راسلنا / Or email:** sales@dealix.me

---

## روابط ذات صلة / Related links

- [نموذج تقرير تنفيذي / Sample executive report](../../services/company_brain_sprint/sample_output.md)
- [نطاق الخدمة / Scope](../../services/company_brain_sprint/scope.md)
- [قائمة التحقق التشغيلي / QA checklist](../../services/company_brain_sprint/qa_checklist.md)
- [حزمة الإثبات / Proof pack template](../../services/company_brain_sprint/proof_pack_template.md)
- [سيناريو المبيعات / Sales script](../sales_script.md)
- [إجابات الاعتراضات / Objection handling](../objection_handling.md)

---

*Dealix · sales@dealix.me · `service_id: company_brain_sprint` · SAR 20,000 · 21 يوم عمل*
