# السبع تفوقات — Dealix

الهدف: التوقف عن التفكير كـ«مزود خدمة AI» وبناء **مدرسة تنفيذ**: منهجية، معايير، منتجات، قياس، أدلة، حالات استخدام، حوكمة، تدريب، ونظام تسليم يتكرر بجودة عالية.

**السياق:** معظم المؤسسات تستخدم AI، لكن قلة منها توسّع على مستوى المؤسسة، ونسبة محدودة ترى أثراً على EBIT على مستوى الشركة — مرجع: [McKinsey — The State of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai/).

---

## 1) Outcome-first

لا تبع features؛ بع **نتيجة تشغيلية** (وقت رد، توحيد جودة، تقرير أسبوعي، تقليل أخطاء، مساعد بمصدر).

المنهجية: [`DEALIX_METHOD_AR.md`](DEALIX_METHOD_AR.md) (ثماني خطوات). الرؤية طويلة المدى: [`DEALIX_AI_OS_LONG_TERM_AR.md`](DEALIX_AI_OS_LONG_TERM_AR.md).

---

## 2) Saudi + Arabic Excellence

ميزة حقيقية: عربي أعمال سعودي، لهجة رسمية مناسبة، سياق منشآت سعودية، مدن وقطاعات، حساسية قنوات مثل واتساب، ثقافة مبيعات محلية، تقارير ثنائية اللغة.

```text
Arabic Quality System
├─ tone library
├─ forbidden phrases
├─ sector templates
├─ bilingual reports
├─ Saudi sales language
└─ executive Arabic summaries
```

---

## 3) Data-first

**قاعدة:** لا تنفيذ AI بدون **Data Readiness** (مصدر، جودة، اكتمال، تكرار، حساسية، غرض، صلاحية استخدام، مخاطر).

مراجع سوقية:

- [Gartner — Lack of AI-ready data puts AI projects at risk](https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk) (63% لا تملك أو لا تعرف ما إذا كانت تمارس إدارة بيانات مناسبة للـAI؛ توقع التخلي عن مشاريع غير المدعومة ببيانات).

---

## 4) Governance-first

كل مشروع يتضمن حيث ينطبق: source attribution، أساس نظامي للمعالجة حيث توجد بيانات شخصية، PII redaction، موافقات، سجلات تدقيق، إجراءات ممنوعة، Proof Pack.

سياق: مع تزايد البيانات غير الموثقة أو المولدة بالـAI، توقعات نحو **zero-trust data governance** — [Gartner — 50% organizations by 2028](https://www.gartner.com/en/newsroom/press-releases/2026-01-21-gartner-predicts-by-2028-50-percent-of-organizations-will-adopt-zero-trust-data-governance-as-unverified-ai-generated-data-grows).

الوثائق: [`../governance/GOVERNANCE_SERVICE_CHECKS_AR.md`](../governance/GOVERNANCE_SERVICE_CHECKS_AR.md)، [`../governance/FORBIDDEN_ACTIONS.md`](../governance/FORBIDDEN_ACTIONS.md).

---

## 5) Proof-backed

كل مشروع ينتهي بإثبات أثر، ليس «تم التنفيذ». هيكل الـProof Pack: [`../templates/proof_pack.md`](../templates/proof_pack.md) وقوالب كل خدمة تحت `docs/services/*/proof_pack_template.md`.

---

## 6) Productized Delivery

أي خدمة رسمية = عرض، نطاق، intake، طلب بيانات، قوائم تسليم وQA، قالب تقرير، Proof Pack، مسار upsell — انظر [`SERVICE_PACK_12_ELEMENTS_AR.md`](SERVICE_PACK_12_ELEMENTS_AR.md).

---

## 7) Learning Loop

بعد كل عميل: ماذا تكرر؟ ماذا أخذ وقتاً؟ ماذا فشل؟ ماذا أعجب العميل؟ ماذا يصبح feature؟ ماذا يصبح template؟ اعتراض مبيعات متكرر؟ KPI أقنع العميل؟

تفاصيل النشر الأسبوعي والمحتوى: [`../strategy/CONTENT_AND_LEARNING_LOOP_AR.md`](../strategy/CONTENT_AND_LEARNING_LOOP_AR.md).

---

## المنافس العربي — نقاط ضعف شائعة

1. يبيع AI عاماً.
2. لا منهجية واضحة.
3. لا قياس أثر.
4. إهمال الحوكمة.
5. لا templates ولا نظام تسليم.

## Dealix Advantage

```text
Dealix Advantage
├─ Dealix Method
├─ Arabic/Saudi quality
├─ Data readiness first
├─ Governance by design
├─ Proof packs
├─ Productized services
├─ Vertical playbooks
└─ Service-assisted platform
```

Playbooks قطاعية: [`../strategy/VERTICAL_PLAYBOOKS.md`](../strategy/VERTICAL_PLAYBOOKS.md) (توسيع تدريجي).

---

## Niche عالمي واضح

**Arabic-first AI Operations for Saudi and MENA businesses** — ثم داخلها: Revenue، Operations، دعم العملاء، Company Brain، Governance. البداية التشغيلية: **ثلاث خدمات** (Revenue sprint، Automation sprint، Company Brain sprint) كما في [`SERVICE_CATALOG.md`](SERVICE_CATALOG.md).

---

## جملة التفوق والعلامة

**إنجليزي (للموقع والعروض الدولية):**

> Dealix turns AI from experiments into operating systems for Saudi companies — with data readiness, workflow design, governance, measurable outputs, and proof of impact.

**عربي:**

> ديلكس يحوّل الذكاء الاصطناعي من أفكار وتجارب إلى أنظمة تشغيل داخل الشركات: بيانات جاهزة، عمليات واضحة، حوكمة، مخرجات قابلة للقياس، وإثبات أثر.

---

## الـMoat (ليس الكود وحده)

1. Dealix Method  
2. Playbooks سعودية/MENA  
3. قوالب ولغة أعمال عربية  
4. Proof packs  
5. نظام حوكمة  
6. قوالب تسليم  
7. مساحات عمل للعميل (تدريجياً)  
8. حلقة تعلّم  
9. دراسات حالة  
10. الثقة  

الكود يُقلّد؛ **المنهجية + القوالب + الأدلة + الثقة** أصعب.
