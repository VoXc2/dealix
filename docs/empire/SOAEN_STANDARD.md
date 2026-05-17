# The SOAEN Standard — معيار سُوأن

<!-- Layer: Empire | Owner: Founder | Date: 2026-05-17 -->
<!-- Arabic primary — العربية أولاً -->

> **قاعدة حاكمة:** أي workflow لا يحتوي العناصر الخمسة — **مصدر، مالك، موافقة، دليل، خطوة تالية** — فهو **غير صالح للأتمتة**. الأتمتة تكبّر ما تؤتمته؛ فإذا كان الـworkflow ناقصاً، الأتمتة تكبّر النقص.

---

## 1. ما هو SOAEN — The Standard

**SOAEN** = العناصر الخمسة التي يجب أن يحتويها أي workflow قبل أن يُعتبر صالحاً للتشغيل أو الأتمتة.

| الرمز | English | العربية | السؤال الذي يجيب عليه |
|-------|---------|---------|------------------------|
| **S** | Source | مصدر | من أين جاءت هذه المعلومة؟ |
| **O** | Owner | مالك | مَن مسؤول عن الإجراء التالي؟ |
| **A** | Approval | موافقة | هل وُوفِق على الفعل الخارجي الحساس؟ |
| **E** | Evidence | دليل | ما الدليل على ما حدث فعلاً؟ |
| **N** | Next Action | خطوة تالية | ما الإجراء القادم، ومتى؟ |

SOAEN هو **المعيار المفاهيمي**. ليس أداة وليس نموذجاً — هو المسطرة التي يُقاس بها أي workflow قبل بنائه.

---

## 2. القاعدة التشغيلية — Operating Lines

الغياب يُترجَم مباشرةً إلى حكم:

| إذا غاب العنصر | فالنتيجة |
|-----------------|----------|
| Lead بلا **مالك** (Owner) | ليس pipeline — مجرد اسم |
| متابعة بلا **دليل** (Evidence) | ليست عمليات — مجرد ادعاء |
| فعل ذكاء اصطناعي بلا **موافقة** (Approval) | مخاطرة، لا تشغيل |
| Dashboard بلا **خطوة تالية** (Next Action) | تقرير فقط، لا قرار |
| معلومة بلا **مصدر** (Source) | لا ثقة — لا تُبنى عليها أتمتة |

> **القاعدة:** workflow ناقص عنصراً واحداً من SOAEN = **لا يُؤتمت**. يُصلَح أولاً، ثم يُؤتمت.

---

## 3. ربط SOAEN بالنظام القائم — Mapping to Artifacts

SOAEN معيار مفاهيمي. أما **الأدوات (Artifacts)** التي تُجسّده فهي موجودة في الكود وموثّقة في الدستور:

| عنصر SOAEN | المعتقد الدستوري | الأداة (Artifact) |
|------------|-------------------|---------------------|
| **Source** | المعتقد 6 — "لا مصدر، لا ثقة" | Source Passport |
| **Owner** | المعتقد 3 — التسليم بلا إثبات ناقص | حقل المالك في Decision Passport |
| **Approval** | المعتقد 7 — "لا موافقة، لا فعل خارجي" | Decision Passport (بوابة الموافقة) |
| **Evidence** | المعتقد 8 — "لا دليل، لا ادعاء" | Proof Pack |
| **Next Action** | المعتقد 1 — "ذكاء بلا workflow ضجيج" | حقل الخطوة التالية في Decision Passport |

### العلاقة بالـDecision Passport

وحدة `decision_passport` تُلزِم القاعدة: **"No Decision Passport = No Action"** — لا جواز قرار، لا فعل. هذا هو التطبيق التنفيذي لعناصر Owner و Approval و Next Action مجتمعةً.

```
[ workflow مقترح ]
        │
        ▼
 هل يحتوي SOAEN الخمسة؟ ──لا──→ يُرفض / يُصلَح أولاً
        │ نعم
        ▼
 Decision Passport يُبنى ──→ يُسجّل: Source, Owner, Approval, Next Action
        │
        ▼
 Proof Pack يُسجّل ──→ Evidence + Truth Label
        │
        ▼
 الآن فقط: الـworkflow صالح للتشغيل والأتمتة
```

### الفصل بين المعيار والأداة

- **SOAEN** = المعيار (ما يجب أن يكون موجوداً).
- **Decision Passport** = الأداة التي تُلزِم Source و Owner و Approval و Next Action.
- **Proof Pack** = الأداة التي تُسجّل Evidence.

لا يوجد تعارض ولا ازدواج: المعيار يصف، والأدوات تُنفّذ.

---

## 4. لماذا SOAEN معيار حوكمة لا قائمة تمنّيات

SOAEN يُترجِم Non-Negotiables الدستور إلى فحص قابل للتطبيق على كل workflow:

- يمنع أتمتة الفوضى — لأن الـworkflow الناقص يُرفض قبل الأتمتة.
- يمنع الفعل الخارجي بلا موافقة — لأن **A** عنصر إلزامي.
- يمنع الادعاء بلا دليل — لأن **E** عنصر إلزامي.
- يمنع المعرفة بلا مصدر — لأن **S** عنصر إلزامي.

---

## المرجع القانوني — Canonical source

- الدستور (المعتقدات 6 و7 و8، وغير القابل للتجاوز): [`../institutional/DEALIX_CONSTITUTION.md`](../institutional/DEALIX_CONSTITUTION.md)
- وحدة جواز القرار (Decision Passport): [`../../auto_client_acquisition/decision_passport/`](../../auto_client_acquisition/decision_passport/)
- وحدة نظام الإثبات (Proof OS): [`../../auto_client_acquisition/proof_os/`](../../auto_client_acquisition/proof_os/)
- الطريقة (الخطوات 3 و5 و7): [`./DEALIX_METHOD.md`](./DEALIX_METHOD.md)
- معيار حزمة الإثبات: [`./PROOF_PACK_STANDARD.md`](./PROOF_PACK_STANDARD.md)
