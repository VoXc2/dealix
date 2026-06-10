# Dealix Operating Model — الطبقات السبع

كل خدمة تمر عبر هذه الطبقات لتكون **برنامج تشغيل** وليس مهمة عشوائية.

```text
Dealix

1. Strategy Layer
   يحدد المشكلة، القطاع، الأولوية، ROI، والمخاطر.

2. Service Layer
   يحول المشكلة إلى عرض جاهز: Sprint / Pilot / Retainer.

3. Product Layer
   يوفر أدوات داخلية لتسليم الخدمة بسرعة وجودة.

4. Delivery Layer
   يدير تنفيذ المشروع من intake إلى proof pack.

5. Quality Layer
   يراجع كل مخرج قبل التسليم.

6. Governance Layer
   يمنع المخاطر: PII، ادعاءات، إرسال غير مصرح، داتا بلا مصدر.

7. Growth Layer
   يحول المشروع إلى pilot، ثم retainer، ثم enterprise.
```

## الربط بالوثائق

| الطبقة | وثائق |
|--------|--------|
| Strategy | [`docs/strategy/`](../strategy/) |
| Service | [`SERVICE_CATALOG.md`](SERVICE_CATALOG.md)، [`docs/services/`](../services/) |
| Product | [`docs/product/MODULE_MAP.md`](../product/MODULE_MAP.md) |
| Delivery | [`docs/delivery/`](../delivery/) |
| Quality | [`docs/quality/`](../quality/) |
| Governance | [`docs/governance/`](../governance/) |
| Growth | [`docs/sales/`](../sales/) |

## الربط بالكود (ملخص)

- Product + Delivery + Quality + Governance: `data_os`, `revenue_os`, `delivery_os`, `governance_os`, `reporting_os`, `knowledge_os`, واجهات Sprint في `commercial_engagements`.
- Growth: مسودات فقط حتى الموافقة — انظر [`COMPLIANCE_PERIMETER.md`](../governance/COMPLIANCE_PERIMETER.md).
