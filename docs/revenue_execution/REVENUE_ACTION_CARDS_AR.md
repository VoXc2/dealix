# بطاقات إجراء الإيراد (Revenue Action Cards)

> **نظام Dealix — Saudi B2B Revenue Operating System**
> الإصدار: 1.0 | التاريخ: 2026-06-03 | المالك: Agent #2
> السكيمة المرجعية: `schemas/revenue_action_card.schema.json`
> بيانات الأمثلة: `data/revenue/action_cards.jsonl`

---

## 1. ما هي بطاقة الإجراء؟

بطاقة إجراء الإيراد (`revenue_action_card`) هي **الأداة الرئيسية** لعرض توصية على المؤسس واستصدار موافقته. الذكاء **يُحضّر** الكارت، المؤسس **يُقرر**. لا إجراء بدون بطاقة، ولا بطاقة بدون `evidence_level`.

---

## 2. الحقول الأساسية (revenue_action_card.schema.json)

| الحقل | الإلزامية | الوصف |
|---|---|---|
| `id` | إلزامي | `RAC-XXXX` |
| `type` | **إلزامي** | نوع الإجراء — من 7 أنواع فقط |
| `company` | إلزامي | الشركة المعنية |
| `linked_proposal_id` | اختياري | ربط بعرض إن وجد |
| `product_id` | اختياري | يجب أن يكون في الكتالوج إن حُدِّد |
| `title` | إلزامي | عنوان واضح للكارت |
| `summary` | إلزامي | ملخص الموقف والتوصية |
| `reason` | إلزامي | لماذا هذا الإجراء الآن؟ |
| `risk_level` | إلزامي | `low / medium / high / critical` |
| `evidence_level` | **إلزامي** | مستوى الدليل الداعم |
| `options` | إلزامي | خيارات للمؤسس (مصفوفة) |
| `approval_required` | إلزامي | دائمًا حسب نوع الإجراء |
| `approved` | إلزامي | `false` حتى قرار المؤسس |
| `expires_at` | اختياري | انتهاء صلاحية الكارت |
| `owner` | إلزامي | من يتابع التنفيذ |
| `status` | إلزامي | `proposed → approved / rejected / done / expired` |

---

## 3. أنواع البطاقات السبعة

### 3.1 `generate_proposal` — توليد عرض تجاري

| الحقل | القيمة المعتادة |
|---|---|
| `risk_level` | `medium` |
| `approval_required` | `true` |
| الخيارات | اعتمد / عدّل / ارفض |
| ما يتبعه | إرسال `PROP-XXXX` لمراجعة المؤسس |

**قاعدة:** لا سعر نهائي حتى موافقة المؤسس على الكارت **وعلى العرض** لاحقًا.

**مثال (RAC-1001):** توليد عرض لـ TrainMe KSA — `product_id=revenue_leakage_diagnostic`، `evidence_level=client_reported`، ينتظر موافقة المؤسس.

---

### 3.2 `generate_proof_pack` — توليد حزمة إثبات

| الحقل | القيمة المعتادة |
|---|---|
| `risk_level` | `low` |
| `approval_required` | `true` |
| الخيارات | اعتمد / عدّل |
| ما يتبعه | نشر `PRF-XXXX` في `/client/proof-pack` |

**قاعدة:** `guaranteed_roi=false` دائمًا. كل رقم له `evidence_level`.

**مثال (RAC-1003):** توليد Proof Pack لـ Digital Rise Agency — `evidence_level=client_data`، بيانات CRM متاحة.

---

### 3.3 `prepare_payment_handoff` — تحضير تسليم الدفع

| الحقل | القيمة المعتادة |
|---|---|
| `risk_level` | `high` |
| `approval_required` | `true` |
| الخيارات | حضّر للمراجعة / ارفض |
| ما يتبعه | إنشاء `PAY-XXXX` (status=pending_approval) |

**ثوابت:** `send_enabled=false`، لا إرسال تلقائي. العرض المُرتبط يجب أن يكون `founder_approved=true`.

**مثال (RAC-1002):** تحضير دفع لـ Digital Rise Agency — `linked_proposal_id=PROP-1002` (معتمد)، المبلغ 1,250 SAR.

---

### 3.4 `request_contract_handoff` — طلب تسليم بشري للعقد

| الحقل | القيمة المعتادة |
|---|---|
| `risk_level` | `critical` |
| `approval_required` | `true` |
| الخيارات | تولَّ بنفسك / فوّض محاميًا / أرجئ |
| ما يتبعه | تسليم بشري كامل — خارج نطاق الذكاء |

**قاعدة:** الذكاء يُحضّر مسودة فقط. المؤسس/المحامي يُكمل. لا وعود قانونية.

---

### 3.5 `move_to_nurture` — نقل لقائمة التغذية

| الحقل | القيمة المعتادة |
|---|---|
| `risk_level` | `low` |
| `approval_required` | `true` (تغيير حالة العميل) |
| الخيارات | انقل لـ Nurture / استمر في المتابعة |
| ما يتبعه | إزالة من Pipeline النشط + جدولة متابعة مؤجلة |

**متى يُستخدم:** العميل مهتم لكن التوقيت غير مناسب. لا حذف — بل تأجيل منظّم.

---

### 3.6 `do_not_contact` — لا تواصل

| الحقل | القيمة المعتادة |
|---|---|
| `risk_level` | `medium` |
| `approval_required` | `true` |
| الخيارات | أكّد لا تواصل / راجع سبب الطلب |
| ما يتبعه | تسجيل في النظام، إيقاف كل الرسائل فورًا |

**قاعدة:** طلب `opt_out` يُنفَّذ فورًا بدون تأخير. أي رسالة بعد `do_not_contact` = انتهاك PDPL.

---

### 3.7 `request_human_handoff` — طلب تسليم بشري عام

| الحقل | القيمة المعتادة |
|---|---|
| `risk_level` | `high` أو `critical` |
| `approval_required` | `true` |
| الخيارات | تولَّ بنفسك / عيّن مندوبًا / أرجئ |
| ما يتبعه | المؤسس يتولى التواصل المباشر |

**متى يُستخدم:** أي موقف يتجاوز صلاحية L3 ولا ينطبق عليه نوع أكثر تحديدًا.

---

## 4. مصفوفة الخطورة والموافقة

| type | risk_level | approval_required | من يُنفّذ |
|---|---|---|---|
| `generate_proposal` | medium | نعم | المؤسس يعتمد، الذكاء يُعدّ |
| `generate_proof_pack` | low | نعم | المؤسس يعتمد، الذكاء يُعدّ |
| `prepare_payment_handoff` | high | نعم | المؤسس يعتمد + تسليم بشري |
| `request_contract_handoff` | critical | نعم | تسليم بشري كامل |
| `move_to_nurture` | low | نعم | المؤسس يُقرر |
| `do_not_contact` | medium | نعم | فوري بعد تأكيد |
| `request_human_handoff` | high/critical | نعم | المؤسس مباشرةً |

---

## 5. دورة حياة الكارت

```
proposed
  ↓ مراجعة المؤسس
approved → تنفيذ الإجراء → done
rejected → توثيق السبب
expired  ← انتهاء expires_at بدون قرار
```

---

## 6. قواعد الجودة الإلزامية

- كل كارت يجب أن يحمل `evidence_level` — بدونه الكارت غير صالح.
- `product_id` إن ذُكر يجب أن يكون في `data/catalog/product_catalog.json`.
- الكارت المنتهي لا يُعاد تفعيله — يُنشأ كارت جديد.
- كل قرار مؤسس يُسجَّل في `ai_action_ledger` + `reports/founder/DECISION_LOG.md`.

---

## الروابط المرجعية

- سكيمة بطاقة الإجراء: `schemas/revenue_action_card.schema.json`
- بيانات الأمثلة: `data/revenue/action_cards.jsonl`
- مصنع العروض: [`PROPOSAL_FACTORY_AR.md`](PROPOSAL_FACTORY_AR.md)
- مصنع Proof Pack: [`PROOF_PACK_FACTORY_AR.md`](PROOF_PACK_FACTORY_AR.md)
- تسليم الدفع: [`PAYMENT_HANDOFF_AR.md`](PAYMENT_HANDOFF_AR.md)
- تسليم العقود: [`CONTRACT_HANDOFF_POLICY_AR.md`](CONTRACT_HANDOFF_POLICY_AR.md)
- الحوكمة الموحّدة: [`AGENTS.md`](../../AGENTS.md)

---

*ينبغي قراءة هذا المستند مع [AGENTS.md](../../AGENTS.md) — عقد الحوكمة الموحّد لكل وكيل/سكربت/مستند في Dealix.*
