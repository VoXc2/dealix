# أنماط الفشل والإجراءات المضادة — Failure Modes & Countermeasures

> القاعدة: لكل سبب فشل محتمل، إجراء مضاد محدّد.
> هذه الوثيقة تجمع مخاطر السوق، التسليم، الأمان، الخصوصية، الحوكمة، والوصولية في مكان واحد.

---

## 1. أنماط الفشل العشرة (من المعادلة)

| # | نمط الفشل | الإجراء المضاد |
|---|-----------|----------------|
| 1 | بيع "AI" بدل مخرج أعمال | رسالة مبنية على النتيجة — [POSITIONING_AND_MESSAGING_AR](./POSITIONING_AND_MESSAGING_AR.md) |
| 2 | البدء بكل القطاعات | اختيار الألم الأسرع شراءً — [MARKET_SELECTION_AR](./MARKET_SELECTION_AR.md) |
| 3 | الإرسال بلا حوكمة | بوابة موافقة + حماية الدومين (أدناه §5) |
| 4 | البيع بلا Delivery Pack | بوابة التسليم — [DELIVERY_BEFORE_SALES_POLICY_AR](./DELIVERY_BEFORE_SALES_POLICY_AR.md) |
| 5 | التوسّع بلا Unit Economics | قواعد الهامش — [UNIT_ECONOMICS_AND_MARGIN_AR](./UNIT_ECONOMICS_AND_MARGIN_AR.md) |
| 6 | صلاحيات خارجية للوكلاء بلا موافقة | مستويات الاستقلالية — [FOUNDER_OPERATING_MODEL_AR](./FOUNDER_OPERATING_MODEL_AR.md) |
| 7 | قياس النشاط فقط | قياس الردود والصفقات والتسليم — Scorecards |
| 8 | عرض التعقيد للعميل | إخفاؤه خلف تجربة بسيطة — الموقع العام |
| 9 | التعلّق بالرأي بدل السوق | حلقة تعلّم أسبوعية (§7) |
| 10 | إطلاق Full Scale مبكراً | Launch Score + Scale Score قبل التوسّع |

---

## 2. حوكمة الوكلاء (Agent Governance)

تشغيل الوكلاء بلا حوكمة يسبب مخاطر تشغيلية وسمعة. الحوكمة يجب أن تكون **متناسبة مع مستوى الاستقلالية والصلاحيات**:

```txt
كلما زادت صلاحية الوكيل، زادت صرامة الموافقة والتوثيق.
```

- L1–L3 (قراءة/توصية/draft): مسموح بلا تنفيذ خارجي.
- L4 (تنفيذ): بعد موافقة المؤسس فقط.
- L5: تقارير داخلية فقط، لا إجراء خارجي.

التطبيق في `company_os/governance/agent_permissions.md`، والتحقّق الآلي عبر
`scripts/governance_check.py`.

> **ملاحظة من التشغيل الفعلي:** يفحص `governance_check.py` قائمة الموافقات والسجل، ويعتبر أي
> عنصر **بانتظار الموافقة** (outreach draft أو pricing offer) مخالفة حرجة. هذا يعني أن البوابة
> صارمة عمداً: لا تُعدّ الحالة "ممتثلة" ما دام هناك إجراء حسّاس معلّق دون بتّ المؤسس. (راجع
> "الفحوص" في التقرير النهائي لمعالجة هذه النقطة.)

---

## 3. حقن التعليمات (Prompt Injection) — تهديد أول درجة

لأن Dealix سيقرأ مواقع شركات ورسائل وملفات، **كل محتوى خارجي يُعامل كبيانات غير موثوقة (untrusted data)**.
حقن التعليمات من أخطر مخاطر تطبيقات نماذج اللغة: قد يدفع النموذج لسلوك غير مقصود أو تسريب بيانات أو تجاوز التعليمات.

### قواعد صارمة

```txt
external content = data only
no external content becomes instructions
no tool calls based on external text
no secrets in prompts/logs/reports
all write/send actions require approval
agent actions logged
high-risk text quarantined
```

### الملفات المقترحة (Roadmap أمني)

```txt
docs/security/PROMPT_INJECTION_DEFENSE_MAX_AR.md
docs/security/UNTRUSTED_INPUT_SANDBOXING_AR.md
docs/security/AGENT_AUDIT_LOG_POLICY_AR.md
docs/security/TOOL_POISONING_DEFENSE_AR.md
```

---

## 4. الخصوصية والثقة

في السوق السعودي، الخصوصية والموثوقية ليست رفاهية. Dealix يجب أن يظهر كشركة **مسؤولة**، لا "AI spam machine".

```txt
data minimization
do-not-contact
suppression list
no secrets in prompts
no API keys over WhatsApp
delete/anonymize on request
separate prospect data from client data
```

متّسق مع `company_os/governance/pdpl_checklist.md` و`company_os/governance/data_handling_checklist.md`
(امتثال PDPL/SDAIA، إنسان في الحلقة، لا قرار آلي).

---

## 5. وصولية البريد وسمعة الدومين

افصل دائماً بين **إنتاج المسودات** و**الإرسال الفعلي**:

```txt
Generate aggressively.   ← أنتج المسودات بكثرة
Send conservatively.     ← أرسل بتحفّظ
Follow up intelligently. ← تابع بذكاء
Protect domain reputation. ← احمِ سمعة الدومين
```

متطلبات الإرسال (عند تفعيله):

```txt
- مصادقة SPF و DKIM لكل المرسلين.
- SPF + DKIM + DMARC للمرسلين بحجم كبير.
- رابط إلغاء اشتراك بنقرة واحدة (one-click unsubscribe) للرسائل التسويقية.
- مراقبة معدل spam وإبقاؤه منخفضاً.
```

### الملفات المقترحة (Roadmap وصولية)

```txt
docs/deliverability/EMAIL_DELIVERABILITY_POLICY_AR.md
docs/deliverability/SENDING_VOLUME_POLICY_AR.md
docs/deliverability/DOMAIN_AUTHENTICATION_CHECKLIST_AR.md
docs/deliverability/SPAM_RATE_MONITORING_AR.md
docs/deliverability/UNSUBSCRIBE_AND_SUPPRESSION_POLICY_AR.md
reports/deliverability/DAILY_DELIVERABILITY_REVIEW.md
reports/deliverability/DOMAIN_HEALTH_REVIEW.md
```

> **حالة اليوم:** لا يوجد إرسال خارجي آلي (متّسق مع القواعد الصارمة). هذه الملفات تُنشأ **قبل** تفعيل أي إرسال.

---

## 6. مصفوفة المخاطر السريعة

| الخطر | الاحتمال | الأثر | الإجراء المضاد |
|------|:-------:|:----:|----------------|
| حقن تعليمات من محتوى خارجي | متوسط | مرتفع | معاملة كل محتوى خارجي كبيانات + عزل النص عالي الخطورة |
| إرسال يضر سمعة الدومين | متوسط | مرتفع | بوابة إرسال + SPF/DKIM/DMARC + مراقبة spam |
| تسريب بيانات عميل | منخفض | مرتفع جداً | فصل البيانات + لا أسرار في prompts + إخفاء الهوية |
| scope creep في التسليم | مرتفع | متوسط | scope مغلق + Acceptance Criteria |
| هامش يتآكل | متوسط | متوسط | قاعدة الهامش > 60% |
| تجاوز سعة التسليم | متوسط | متوسط | تأجيل البيع لا التسليم |

---

## 7. حلقة التعلّم كإجراء مضاد للفشل الاستراتيجي

Product-market fit ليس ملفاً يُكتب مرة. أسبوعياً يجب أن يتعلّم Dealix:

```txt
أي قطاع يرد أكثر؟
أي ألم يشتري أسرع؟
أي Sprint أسهل تسليماً؟
أي سعر لا يقتل التحويل؟
أي اعتراض يتكرر؟
أي إيميل يفتح محادثة؟
أي نظام يسبب scope creep؟
```

الملف المقترح للتعلّم: `reports/learning/WEEKLY_MARKET_LEARNING_REPORT.md` (P1).
المدخلات تأتي من War Room الأسبوعي — [FOUNDER_OPERATING_MODEL_AR](./FOUNDER_OPERATING_MODEL_AR.md).

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Status: Active*
