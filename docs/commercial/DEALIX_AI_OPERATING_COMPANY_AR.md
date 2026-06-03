# Dealix — شركة تشغيل AI (المرجع الشامل)

**الموقف:** Dealix ليست «أداة leads» وحدها؛ الهدف التنظيمي هو **AI Operating Partner للشركات السعودية**: كل خط خدمة = نظام داخل المنتج + خدمة مدفوعة + تسليم موحّد + مقياس نجاح. التسعير التفصيلي للإيراد يبقى في [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md).

**مراجع سوق (اتجاهات، لا تُنسَخ كأسعار):**

- McKinsey — The State of AI (انتشار التجارب مقابل التوسع):  
  https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai  
- SPA — سجلات تجارية Q4 2025 (سياق حجم السوق):  
  https://www.spa.gov.sa/en/N2484191  
- Saudi Gazette — تغطية إعلامية موازية لنمو السجلات:  
  https://saudigazette.com.sa/article/658036  
- Gartner — بيانات غير جاهزة للـ AI تعرّض المشاريع للخطر:  
  https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk  
- Gartner — نضج AI والحوكمة والهندسة:  
  https://www.gartner.com/en/newsroom/press-releases/2025-06-30-gartner-survey-finds-forty-five-percent-of-organizations-with-high-artificial-intelligence-maturity-keep-artificial-intelligence-projects-operational-for-at-least-three-years  
- IT Pro — فشل مشاريع AI مع استمرار الإنفاق (سياق الحذر التشغيلي):  
  https://www.itpro.com/business/business-strategy/ai-adoption-projects-keep-failing-but-enterprise-fomo-means-investment-is-still-rising  
- أسس قانونية لمعالجة البيانات (PDPL — مرجع عام):  
  https://istitlaa.ncc.gov.sa/en/Transportation/NDMO/IMPLEMENTINGPDPL/Pages/Article_003.aspx  

---

## أين الكود؟

لربط **أسماء الأنظمة التسعة** بالحزم والراوترات والمشغّلات الفعلية (بما فيها مسارات curl للـ Sprint)، راجع: **[CODE_MAP_OS_TO_MODULES_AR.md](CODE_MAP_OS_TO_MODULES_AR.md)**.

---

## القاعدة الذهبية لكل خدمة (السبعة)

1. وعد واضح  
2. نطاق واضح  
3. مدخلات مطلوبة من العميل  
4. عملية تنفيذ ثابتة  
5. مخرجات ملموسة  
6. مقياس نجاح  
7. ترقية طبيعية للخدمة التالية  

---

## التسعة أنظمة (OS) — تعريف، خدمات، مقاييس

### 1) Strategy OS

**الغرض:** أين تستخدم الشركة الـ AI ولِمَ، وبأي ترتيب.

**وحدات كود أولية:** [`auto_client_acquisition/strategy_os/`](../../auto_client_acquisition/strategy_os/) — scoring لحالات استخدام وترتيب أولويات (قابل للتوسيع).

**خدمة مدفوعة:** AI Strategy & Readiness Assessment — **7,500–25,000** ريال، 5–10 أيام.

**مخرجات:** تقرير جاهزية، portfolio use cases، risk map، quick wins، roadmap 30/60/90، توصية بأي Sprint من Dealix يبدأ به العميل.

**مقياس نجاح:** العميل يعرف أول 3 خطوات؛ ≥50% ينتقلون إلى Sprint (هدف داخلي).

---

### 2) Revenue OS

**الغرض:** تحويل داتا مبعثرة إلى مبيعات قابلة للتنفيذ.

**الكود الحالي:** [`auto_client_acquisition/revenue_os/`](../../auto_client_acquisition/revenue_os/) — سجل مصادر، dedupe، anti-waste، توسعة، تعلم؛ ومسارات API في [`api/routers/leads.py`](../../api/routers/leads.py).

**خدمات:** Diagnostic، Lead Intelligence Sprint، Pilot Conversion، Monthly RevOps — كما في [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md).

**مقياس نجاح:** صفوف معالجة، qualified accounts، مسودات، اجتماعات، قيمة pipeline، تحويل Sprint → Retainer.

---

### 3) Customer OS

**الغرض:** دعم عملاء أسرع بمساعدة + موافقة بشرية (لا إرسال تلقائي في البداية).

**الكود:** خارطة طريق — إعادة استخدام سياسات القنوات والمسودات من Revenue OS + بوابات الموافقة؛ وحدات مستقلة لاحقاً: تصنيف، FAQ، SLA.

**خدمات:** AI Support Desk Sprint (12k–30k)، Feedback Intelligence (7.5k–25k)، Retainer دعم (8k–25k/شهر).

**مقياس نجاح:** زمن رد، رسائل معلّقة، توحيد جودة، أعلى 10 مشاكل متكررة.

---

### 4) Marketing OS

**الغرض:** محتوى وحملات مربوطة بالعرض والإيراد (ليس وكالة منفصلة).

**الكود:** خارطة طريق — ربط لاحق بـ ICP و`signal_normalizer` وقوالب المحتوى.

**خدمات:** AI Content Engine (5k–18k/شهر)، Campaign Intelligence Pack (8k–25k)، Brand Voice System (7.5k–20k).

**مقياس نجاح:** حملات جاهزة، سرعة إنتاج، التزام نبرة، leads ناتجة (حيث يُقاس).

---

### 5) Operations OS

**الغرض:** أتمتة عملية متكررة مع مراجعة بشرية وتدقيق.

**الكود:** خارطة طريق — تكامل لاحق مع سكربتات التقارير والـ workflows الداخلية.

**خدمات:** AI Quick Win Sprint (7.5k–15k)، Workflow Automation Sprint (15k–50k)، Executive Reporting Automation (setup + شهري).

**مقياس نجاح:** ساعات موفّرة، أخطاء أقل، workflows نشطة.

---

### 6) Knowledge OS

**الغرض:** Company Brain — إجابات بمصادر (**No source = no answer**).

**الكود:** خارطة طريق — ربط لاحق بـ RAG/Project Intelligence في المستودع حيث يتوفر.

**خدمات:** Company Brain Sprint (20k–60k)، Sales Knowledge Assistant، Policy Assistant.

**مقياس نجاح:** نسبة إجابات موثّقة، تقليل وقت البحث، جودة حسب مراجعة العميل.

---

### 7) Data OS

**الغرض:** جودة بيانات وقرار.

**وحدات كود أولية:** [`auto_client_acquisition/data_os/`](../../auto_client_acquisition/data_os/) — درجة جودة بسيطة على جداول (قابل للتوسيع).

**خدمات:** Data Cleanup & Unification (8k–50k)، AI Business Dashboard، Forecasting & Scoring.

**مقياس نجاح:** رفع درجة الجودة، تقليل تكرار، وضوح KPIs.

---

### 8) Governance OS

**الغرض:** سياسات، موافقات، PDPL، audit.

**وحدات كود أولية:** [`auto_client_acquisition/governance_os/`](../../auto_client_acquisition/governance_os/) — بوابة مسودات تستدعي قواعد anti-waste الموجودة.

**الكود الحالي:** `validate_pipeline_step`، `source_registry`، قنوات الموافقة في المنتج.

**خدمات:** AI Readiness & Risk Review، AI Usage Policy، PDPL-Aware Data Review.

**مقياس نجاح:** مصادر موثّقة، مسارات موافقة للإرسال الحساس، سجلات تدقيق.

---

### 9) Delivery OS

**الغرض:** تسليم متكرر بنفس الجودة (تحويل freelancer → شركة).

**وحدات كود أولية:** [`auto_client_acquisition/delivery_os/`](../../auto_client_acquisition/delivery_os/) — مراحل معيارية وقوائم تحقق (لا يتعارض مع [`api/routers/delivery_os.py`](../../api/routers/delivery_os.py) — ذلك API تشغيلي؛ هذا **إطار تسليم خدمة**).

**مخرجات لكل خدمة:** intake، scope، checklist، تقرير، QA، handoff، upsell — أنظر [checklists/DELIVERY_LEAD_INTELLIGENCE_SPRINT.md](checklists/DELIVERY_LEAD_INTELLIGENCE_SPRINT.md).

**مقياس نجاح:** الالتزام بالوقت، هامش، upsell، رضا، إعادة استخدام القوالب.

---

## معيار التسليم — Dealix Delivery Standard (ثابت لكل مشروع)

```text
Discover → Diagnose → Design → Build → Validate → Deliver → Prove → Expand
```

| المرحلة | سؤال مركزي |
|---------|------------|
| Discover | ما المشكلة، الداتا، الفريق، الأدوات، أين الضياع؟ |
| Diagnose | جاهزية بيانات، نضج عمليات، مخاطر، ROI سريع؟ |
| Design | workflow، موافقات، مخرجات، مقاييس؟ |
| Build | أقل تعقيد، human-in-the-loop، سجلات؟ |
| Validate | جودة، أمان، لغة، حالات حافة؟ |
| Deliver | تقارير، SOP، تدريب، handoff؟ |
| Prove | قبل/بعد، أرقام، دليل؟ |
| Expand | retainer، workflow إضافي، حوكمة؟ |

---

## إطار QA (قبل التسليم)

- **Business QA:** أثر إداري، KPI، next action، upsell؟  
- **Data QA:** مصدر، تكرار، فراغات، PII، lawful basis؟  
- **AI QA:** دقة، مصادر، عربي، edge cases؟  
- **Compliance QA:** ادعاءات، إرسال بارد، موافقة، audit؟  
- **Delivery QA:** اكتمال المخرجات، وضوح التقرير، renewal؟  

---

## درجة جودة المشروع الداخلية (0–100)

| المعيار | الوزن |
|---------|------:|
| وضوح أثر الأعمال | 20 |
| جودة البيانات | 15 |
| جودة المخرجات لغوياً | 15 |
| سهولة استخدام العميل | 10 |
| الأمان والامتثال | 15 |
| قابلية التكرار كمنتج | 15 |
| قابلية الترقية لـ retainer | 10 |

**قاعدة:** أي مشروع بدرجة أقل من 80 لا يُسلّم كـ«ممتاز» دون تحسين.

---

## الأبواب الخمسة للعميل (عرض مبسّط)

1. **Grow Revenue** — فرص من البيانات إلى pipeline — صفحات الواجهة: `/ar/services`، عرض Sprint: `/ar/offer/lead-intelligence-sprint`.  
2. **Serve Customers** — دعم أسرع بمساعد + موافقة.  
3. **Automate Operations** — workflow واحد واضح.  
4. **Build Company Brain** — إجابات بمصادر.  
5. **Govern AI** — سياسات وموافقات وaudit.  

---

## كتالوج خدمات مختصر (ريال سعودي)

| الخط | الخدمة | السعر (من–إلى) |
|------|--------|-----------------|
| Strategy | AI Readiness Assessment | 7,500–25,000 |
| Revenue | Revenue Diagnostic | 3,500–7,500 |
| Revenue | Lead Intelligence Sprint | 9,500–18,000 |
| Revenue | Pilot Conversion Sprint | 22,000–45,000 |
| Customer | AI Support Desk Sprint | 12,000–30,000 |
| Marketing | Campaign Intelligence Pack | 8,000–25,000 |
| Ops | AI Quick Win Sprint | 7,500–15,000 |
| Ops | Workflow Automation Sprint | 15,000–50,000 |
| Knowledge | Company Brain Sprint | 20,000–60,000 |
| Data | Data Cleanup & Unification | 8,000–50,000 |
| Governance | AI Usage Policy | 10,000–35,000 |
| Retainer | Monthly AI Ops / RevOps | 15,000–60,000/شهر |
| Enterprise | AI Operating System | 85,000–300,000+ |

---

## خارطة بناء الكود (مراحل)

### المرحلة 1 — Sellable Core (الآن + ما أُضيف)

- Data OS: جودة بيانات أولية ([`data_os`](../../auto_client_acquisition/data_os/)).  
- Revenue OS: موجود — استمرار التوسيع.  
- Governance OS: بوابة مسودات ([`governance_os`](../../auto_client_acquisition/governance_os/)).  
- Reporting: سكربتات التقارير الحالية في `scripts/dealix_*`.  
- Delivery: إطار مراحل ([`delivery_os`](../../auto_client_acquisition/delivery_os/)).  
- Strategy OS: ترتيب use cases ([`strategy_os`](../../auto_client_acquisition/strategy_os/)).  

### المرحلة 2 — توسيع AI Ops

Operations عميق، Customer OS، Knowledge RAG، تقارير تنفيذية أوتوماتيكية أكثر.

### المرحلة 3 — Retainer Machine

لوحات شهرية، CRM hygiene، مراقبة workflows.

### المرحلة 4 — Enterprise

صلاحيات، تعدد مستأجرين، تكاملات، SLA، تصدير audit.

---

## التفوق التنافسي (ملخّص تنفيذي)

1. **Outcome-first** — كل خدمة بنتيجة قابلة للقياس.  
2. **Saudi-localized** — عربي أعمال، قطاعات، مدن.  
3. **Proof-backed** — Proof ledger وتقارير قبل/بعد.  
4. **Governed AI** — مصادر، موافقة، عدم إرسال بارد.  
5. **Productized delivery** — نفس القوالب لكل عميل.  

**الجملة القيادية:** Dealix لا تقدم أدوات AI عشوائية؛ تبني **وظائف تشغيلية** داخل الشركة — مبيعات، دعم، أتمتة، معرفة، وحوكمة — بمخرجات واضحة وجودة قابلة للقياس.

---

## روابط داخلية

- [Playbooks قطاعية (مسودات)](playbooks/README_AR.md)  
- [حزم الإيراد والأسعار](DEALIX_REVOPS_PACKAGES_AR.md)  
- [نموذج التشغيل الأعظم](../strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md)  
- [مكينة ليدز سعودية](../ops/SAUDI_LEAD_MACHINE_AR.md)  
