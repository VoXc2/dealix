# Dealix Role Ownership — من يملك ماذا (RACI)

> *آخر تحديث: 2026-06-03*
> يمتد من `company_os/governance/agent_permissions.md` ويربط الأدوار بالحلقة اليومية.

---

## الأدوار

| الدور | الطبيعة | الصلاحية القصوى |
|-------|---------|------------------|
| **Founder (المؤسس)** | إنسان | يوافق على كل شيء حسّاس؛ القرار النهائي |
| **Operator (المشغّل)** | إنسان | يشغّل الحلقة، يرسل/يتصل بعد الموافقة |
| **Research Agent** | AI | Observe / Advise / Draft — بحث وترتيب وصياغة |
| **Drafting Agent** | AI | Draft — مسودات إيميل/Brief فقط |
| **Proposal Agent** | AI | Draft — Mini Proposals فقط |
| **Delivery Agent** | AI | Observe / Draft — مخرجات تسليم على بيانات مجهّلة |
| **Finance Agent** | AI | Observe / Advise — حساب Score والهامش |
| **Governance Agent** | AI | Observe / Advise — تدقيق وامتثال |

> مستويات الصلاحية (Observe / Advise / Draft / Act-with-Approval / Autonomous)
> معرّفة في `agent_permissions.md`. **مستوى Autonomous ممنوع لكل الوكلاء.**

---

## مصفوفة RACI للحلقة اليومية

> R = ينفّذ · A = مسؤول/يوافق · C = يُستشار · I = يُبلَّغ

| الخطوة | Research | Drafting | Proposal | Delivery | Finance | Operator | **Founder** |
|--------|:-------:|:--------:|:--------:|:--------:|:-------:|:--------:|:-----------:|
| Account Discovery | R | – | – | – | C | A/I | I |
| Account Packs | R | – | – | – | C | A | I |
| Contact Discovery | R | – | – | – | – | A | I |
| Email + Call Brief | C | R | – | – | C | A | I |
| Quality Gate + Top 100 | C | C | – | – | C | **R/A** | I |
| Review & Approve | I | I | I | I | I | C | **R/A** |
| Send / Call | – | – | – | – | – | **R** | A |
| Reply / Classify | C | – | – | – | – | **R/A** | I |
| Mini Proposal | – | C | **R** | – | C | A | A |
| Delivery Review | – | – | – | **R** | C | A | A |
| Founder Command | I | I | I | I | C | C | **R/A** |

**القاعدة الذهبية:** أي عمود فيه إرسال خارجي أو سعر أو بدء تسليم → العمود الأخير
(Founder) فيه **A**، والتنفيذ (R) بيد **إنسان** (Operator)، لا بيد وكيل.

---

## الخطوط الحمراء (مكرّرة للتأكيد من agent_permissions.md)

```txt
1. الوكيل لا يرسل رسائل خارجية بدون موافقة.
2. الوكيل لا يعالج PII خام في أدوات عامة.
3. الوكيل لا يتخذ قرارات تسعير.
4. الوكيل لا يحذف بيانات.
5. الوكيل لا يعدّل أسرار الإنتاج.
6. الوكيل لا يقدّم استشارة قانونية/امتثال مباشرة للعميل.
7. الوكيل لا يعمل بشكل مستقل على حسابات العملاء.
```

---

## سلسلة الموافقات (Escalation)

| نوع القرار | المعتمِد |
|-----------|---------|
| رسائل التواصل | المؤسس |
| تسعير ≤ 5,000 ريال | المؤسس |
| تسعير > 5,000 ريال | المؤسس + تهدئة 24 ساعة |
| معالجة بيانات عميل | المؤسس + فحص امتثال |
| تسليم مخرجات | مراجعة المؤسس |
| بدء التسليم | موافقة المؤسس |
| تغييرات النظام | المؤسس |

كل موافقة تُسجَّل في `company_os/governance/approval_queue.json`، وكل إجراء AI
يُسجَّل في `company_os/governance/ai_action_ledger.jsonl`.

---

*Dealix Role Ownership (RACI) | Version 1.0 | 2026-06-03*
