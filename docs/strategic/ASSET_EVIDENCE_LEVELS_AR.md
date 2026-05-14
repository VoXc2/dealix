# مستويات إثبات الأصول القابضة

**الغرض:** منع تضخيم قيمة وثيقة قبل **إثبات استخدام**؛ كل أصل له مستوى من L0 إلى L7.

| المستوى | الاسم | المعنى |
|---------|-------|--------|
| L0 | Created | الأصل موجود فقط |
| L1 | Classified | له تصنيف وقيمة في السجل |
| L2 | Packaged | داخل حزمة قراءة أو حزمة خارجية / motion معتمدة |
| L3 | Used internally | استُخدم داخليًا (اجتماع داخلي، تشغيل) |
| L4 | Sent externally | أُرسل خارجيًا ضمن حزمة معتمدة **إلى جهة خارجية فعلية** عبر قناة محددة (بريد، اجتماع، رابط مُوَقَّع، …) |
| L5 | Used in meeting | استُخدم في **اجتماع منعقد** مع طرف خارجي (لا تُرفع إلى L5 عند مجرد حجز الموعد) |
| L6 | Drove follow-up | أدى إلى متابعة أو طلب مؤهل |
| L7 | Drove revenue | ساهم في فاتورة أو retainer أو intro مؤهل قابل للقياس |

## قفل L4 (L4 Verification Lock)

- **L4 لا يُمنح** إلا إذا **خرج الأصل إلى جهة خارجية حقيقية** عبر قناة محدّدة (وليس مسودة داخلية فقط).
- **لا يُحسب** مجرد sample أو template أو `prepared_not_sent` كـ **L4**؛ في تلك الحالة استخدم **L2** (Packaged) أو **L3** (داخلي) حتى الإرسال الفعلي.
- كل إدخال L4+ في [`../../data/docs_asset_usage_log.json`](../../data/docs_asset_usage_log.json) يجب أن يمرّ بفحص آلي: `date`, `channel`, `outcome`, `audience` **أو** `audience_id`, و`founder_confirmed: true` (انظر `scripts/validate_docs_governance.py`).
- عند **حجز** اجتماع دون انعقاده بعد: ابقَ على **L4** مع `outcome` يصف الحجز؛ حدّث إلى **L5** بعد الاجتماع واستخدام الأصل فيه.

## قواعد صارمة (Claim discipline)

- **لا ادّعاء «تجاري» بلا L4** (إثبات إرسال خارجي معتمد).
- **لا ادّعاء «شراكة قوية» بلا L5** (استخدام في اجتماع مع طرف خارجي).
- **لا ادّعاء «قابض عالي أثر» بلا L6** (متابعة / intro / طلب مؤهل).
- **لا ادّعاء revenue-grade بلا L7** (فاتورة أو retainer أو صفقة شريك قابلة للقياس، مع سجل).

**التمييز:** درجة القيمة في السجل = رأي استراتيجي؛ **Evidence level** = إثبات سوقي — انظر [_generated/asset_evidence_summary.json](_generated/asset_evidence_summary.json) (يُولَّد آليًا).

- لا أصل يُعتبر **holding-grade** في العرض الخارجي إلا إذا وصل **L4** على الأقل (إرسال معتمد).
- لا أصل يُعتبر **commercial-grade** في ادّعاء الإيراد إلا إذا وصل **L6** أو **L7** (مع سجل في `docs_asset_usage_log.json`).
- الانتقال بين المستويات **يدويًا + مسجل** بعد [ASSET_USAGE_GOVERNANCE_AR.md](ASSET_USAGE_GOVERNANCE_AR.md).

## الربط بالسجل

عمود **EvidenceLevel** في [HOLDING_VALUE_REGISTRY_AR.md](HOLDING_VALUE_REGISTRY_AR.md) يعكس المستوى الحالي (مثل `L2`).
