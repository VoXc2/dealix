# حوكمة استخدام الأصول الوثائقية

**الغرض:** لا تُحسب قيمة أي وثيقة بناءً على رأي داخلي فقط. تُحدَّث الأدلة عندما يُستخدم الأصل في سياق **حقيقي**: شريك، عميل، مستثمر، تسليم، تدريب، ترخيص.

**سجل أدلة (ليست حماس):** *This log is not a motivation tracker. It is an evidence register.* — **هذا السجل ليس سجل حماس؛ إنه سجل أدلة.**  
**حلقة إشارات السوق:** [MARKET_SIGNAL_OPERATING_LOOP_AR.md](MARKET_SIGNAL_OPERATING_LOOP_AR.md) — من L4 إلى قرار (متابعة، تصنيف رد، archetype، تحويل).

**المرجع:** مستويات الإثبات [ASSET_EVIDENCE_LEVELS_AR.md](ASSET_EVIDENCE_LEVELS_AR.md)؛ السجل التشغيلي [`../../data/docs_asset_usage_log.json`](../../data/docs_asset_usage_log.json).

## مستويات الاستخدام (ملخص)

| المستوى | الوصف | هل يرفع القيمة؟ |
|---------|--------|------------------|
| Internal reference | مرجع داخلي للمؤسس/الفريق | جزئيًا |
| Sent externally | أُرسل لشريك أو عميل أو مستثمر | نعم |
| Used in meeting | استُخدم في اجتماع فعلي | نعم |
| Drove next action | نتج follow-up أو intro أو طلب | نعم بقوة |
| Drove revenue | ساهم في فاتورة أو retainer | أعلى قيمة |
| Drove licensing | ساهم في نقاش ترخيص أو شراكة IP | أعلى قيمة |

## قاعدة التسجيل (Usage Evidence)

لا **Usage Evidence** يُعتمد في تحديث السجلات إلا مع:

- **asset** (اسم الأصل)  
- **audience** أو **audience_id** (مثل `PARTNER-001`) للتدقيق دون كشف اسم الجهة  
- **date**  
- **used_for** أو **usage_type** (قيمة من قائمة `usage_types` في [`../../data/docs_asset_usage_log.json`](../../data/docs_asset_usage_log.json))  
- **outcome**  
- **founder_confirmed** = `true`  

إذا كان الإدخال **تمهيدًا فقط** ولم يُرسل بعد: لا تستخدم **L4** — انظر قسم «قفل L4» في [ASSET_EVIDENCE_LEVELS_AR.md](ASSET_EVIDENCE_LEVELS_AR.md) (`prepared_not_sent`, **L2**, `founder_confirmed: false`).

### حقول اختيارية — Commercial Conversion OS

لربط الأصل بمسار الإغلاق (بعد أول إرسال):

- **outcome_quality**: `pending` | `none` | `low` | `medium` | `high` | `learning` | `revenue_candidate` | `revenue_confirmed`  
- **commercial_next_action**: خطوة تشغيلية صريحة (مثل إرسال نطاق diagnostic)

### قواعد تحويل تجريبية

- وصل **L4** ولا رد خلال **14 يومًا** → راجع الرسالة أو الجمهور.
- وصل **L5** ولا **next action** مؤهل → قد يكون الأصل مناسبًا للشرح أكثر من الإغلاق.
- وصل **L6** → أدرجه في الحزمة الرسمية للشراكة/العميل بعد مراجعة الحدود.
- وصل **L7** → اعتبره **core revenue asset** في المجلس الشهري.

## قاعدة رفع الدرجات في السجل

لا تُرفع درجات **Revenue / Partner / Investor** في [HOLDING_VALUE_REGISTRY_AR.md](HOLDING_VALUE_REGISTRY_AR.md) استنادًا إلى رأي فقط؛ التحديث بعد استخدام **مسجل** في `data/docs_asset_usage_log.json` ومراجعة [MONTHLY_ASSET_COUNCIL_AR.md](MONTHLY_ASSET_COUNCIL_AR.md).

## الحزم المعتمدة

الإرسال الخارجي فقط عبر [EXTERNAL_PACK_REGISTRY_AR.md](EXTERNAL_PACK_REGISTRY_AR.md) وحزم **Motion** تحت [packs/](packs/).
