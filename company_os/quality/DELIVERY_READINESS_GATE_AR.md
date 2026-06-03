# بوابة جاهزية التسليم — Delivery Readiness Gate

لا تبِع نظامًا إلا وهو جاهز للتسليم. المنطق: `deliveryGate` في
`scripts/lib/commercial.js`. يُفرض في `npm run commercial:check`.

---

## جاهزية كل نظام

| النظام | جاهزية التسليم المطلوبة |
|--------|--------------------------|
| نظام تشغيل الإيرادات | Leakage Map + Workflow + Report Template |
| نظام القيادة التنفيذية | KPI Map + Daily Report + Decision Log |
| نظام استرجاع المتابعات | Queue + Status Model + Message Set |
| نظام عملاء واتساب | Flow Map + Action Cards + Handoff Policy |
| نظام العروض والإثبات | Proposal Template + Proof Pack + Scope Block |

(المصدر: `company_os/commercial/systems.json` حقل `delivery_readiness`.)

---

## لا يبدأ التسليم إذا نقص أي من

```
client / selected_system / scope / required_inputs /
starter_price / delivery_pack / success_metric / acceptance_criteria
```

## تفشل البوابة إذا

| السبب | الوصف |
|------|-------|
| `no_scope` | لا يوجد نطاق |
| `no_required_inputs` | لا توجد مدخلات مطلوبة |
| `no_success_metric` | لا يوجد مؤشر نجاح |
| `no_acceptance_criteria` | لا توجد معايير قبول |

إذا نقص شيء، الحالة: `delivery_blocked`.

---

## فرض حرج

أي فرصة في `won/delivery_started/active/renewal_candidate` لا تجتاز هذه البوابة
تُعتبر **مخالفة حرجة (CRITICAL)** في `commercial:check` ويتوقف المصنع — لأن التسليم
بدون نطاق ومعايير قبول أكبر مخاطر السمعة.
