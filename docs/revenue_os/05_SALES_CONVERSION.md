# 05 — تحويل المبيعات / Sales Conversion (Layer 5)

عملية بيع مؤسس منضبطة. / A disciplined founder-led sales process.

## العربية

### بنية المكالمة (10 خطوات)

```
1. Context            6. Evidence gap
2. Current workflow   7. AI / CRM risk
3. Pain               8. Demo
4. Source clarity     9. Diagnostic offer
5. Approval boundary  10. Next step
```

### فتح المكالمة

> خليني أوضح Dealix بجملة واحدة: نحن نساعد الفرق التي عندها عمليات إيراد أو
> تجارب AI لكنها غير محكومة بشكل كافٍ — مصادر غير واضحة، موافقات غير محددة،
> أدلة غير موثقة، وصعوبة في ربط العمل بقيمة فعلية.

### أسئلة الاكتشاف

1. ما أكثر workflow يضيع وقت أو فلوس حالياً؟
2. هل عندكم CRM؟ وهل تثقون فيه؟
3. كيف يتم follow-up اليوم؟
4. هل AI مستخدم داخلياً؟
5. من يوافق على الرسائل أو القرارات الخارجية؟
6. كيف تعرفون أن workflow خلق قيمة؟
7. هل عندكم دليل موثق لأي قرار إيرادي؟

### عرض Dealix

> أفضل خطوة ليست مشروعاً كبيراً. نبدأ بتشخيص قصير. نأخذ workflow واحداً
> ونفحصه عبر: source clarity · approval boundaries · evidence trail ·
> proof of value. ثم نعطيكم proof pack وقرارات تشغيلية واضحة.

### الإغلاق

> إذا مناسب، أرسل لك scope مختصراً اليوم. إذا قبلتوه، نصدر invoice ونبدأ
> onboarding.

⚠️ **لا تستخدم لغة ضمان نتائج** («نضمن إغلاق X صفقة») — `no_fake_proof`.

### الربط بالنظام

- توليد المقترحات: `sales_os/proposal_renderer.py` + قوالب Jinja2
  (`templates/PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2`).
- سكربت العرض الكامل في `docs/sales-kit/dealix_demo_script_30min.md`.
- نطاق وأسعار يجب أن تطابق العروض الحية في `service_catalog/registry.py`.

---

## English

### Call structure (10 steps)

```
1. Context            6. Evidence gap
2. Current workflow   7. AI / CRM risk
3. Pain               8. Demo
4. Source clarity     9. Diagnostic offer
5. Approval boundary  10. Next step
```

### Opening the call

> Let me explain Dealix in one sentence: we help teams that have revenue
> operations or AI experiments that are not sufficiently governed — unclear
> sources, undefined approvals, undocumented evidence, and difficulty linking
> work to real value.

### Discovery questions

1. Which workflow wastes the most time or money right now?
2. Do you have a CRM, and do you trust it?
3. How does follow-up happen today?
4. Is AI used internally?
5. Who approves external messages or decisions?
6. How do you know a workflow created value?
7. Do you have documented evidence for any revenue decision?

### The Dealix offer

> The best step is not a big project. We start with a short diagnostic. We take
> one workflow and examine it through: source clarity · approval boundaries ·
> evidence trail · proof of value. Then we give you a proof pack and clear
> operational decisions.

### The close

> If this fits, I'll send you a short scope today. If you accept it, we issue
> an invoice and start onboarding.

⚠️ **No guaranteed-outcome language** ("we will close X deals") — `no_fake_proof`.

### How it connects to the system

- Proposal generation: `sales_os/proposal_renderer.py` + Jinja2 templates
  (`templates/PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2`).
- The full demo script is in `docs/sales-kit/dealix_demo_script_30min.md`.
- Scope and prices must match the live offers in `service_catalog/registry.py`.
