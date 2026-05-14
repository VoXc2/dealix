# نموذج التشغيل القابض للأصول — Dealix كـ Asset Operating Company

**الغرض:** بعد [Holding Memory Activation](HOLDING_DOCS_HUB_AR.md)، لا تُدار Dealix كمجلدات؛ تُدار كـ **رأس مال معرفي مُحكَم** يتحرك في السوق عبر حزم وحوكمة وأدلة.

**القاعدة:** **No usage, no commercial evidence** — انظر [ASSET_USAGE_GOVERNANCE_AR.md](ASSET_USAGE_GOVERNANCE_AR.md).

## الخمس أنظمة فوق الذاكرة

كل نظام يجيب سؤالًا واحدًا على مستوى CEO:

| النظام | السؤال | الملفات / المخرجات المرجعية |
|--------|--------|-------------------------------|
| **Asset Evidence OS** | أي أصل أثبت نفسه في السوق؟ | [ASSET_EVIDENCE_LEVELS_AR.md](ASSET_EVIDENCE_LEVELS_AR.md)، [_generated/asset_evidence_summary.json](_generated/asset_evidence_summary.json) |
| **External Motion OS** | أي أصل خرج، لمن، وماذا حدث؟ | [EXTERNAL_PACK_REGISTRY_AR.md](EXTERNAL_PACK_REGISTRY_AR.md)، [packs/](packs/)، [data/docs_asset_usage_log.json](../../data/docs_asset_usage_log.json) |
| **Commercial Conversion OS** | أي أصل حرّك اجتماعًا أو فاتورة؟ | [ASSET_USAGE_GOVERNANCE_AR.md](ASSET_USAGE_GOVERNANCE_AR.md) (حقول التحويل)، [HOLDING_VALUE_REGISTRY_AR.md](HOLDING_VALUE_REGISTRY_AR.md) |
| **Trust & Diligence OS** | أي أصل آمن للخروج؟ | [DOCS_PUBLICATION_BOUNDARY_AR.md](DOCS_PUBLICATION_BOUNDARY_AR.md)، اختبار [tests/test_external_pack_safety.py](../../tests/test_external_pack_safety.py) |
| **Pruning & Capital Allocation OS** | أين الوقت والتركيز؟ | [QUARTERLY_PRUNING_POLICY_AR.md](QUARTERLY_PRUNING_POLICY_AR.md)، [ARCHIVE_REVIEW_QUEUE_AR.md](ARCHIVE_REVIEW_QUEUE_AR.md)، [_generated/asset_capital_allocation.json](_generated/asset_capital_allocation.json) |

## مسارات الحركة الخارجية (Motion)

لكل مسار يجب أن يتوفر: **Pack** + **رسالة** + **تسجيل في usage log** + **نتيجة** + **إجراء تالي** + **Evidence Level** — راجع حزم الحركة تحت [packs/](packs/).

| المسار | حزمة مرجعية |
|--------|-------------|
| Partner | [packs/PARTNER_MOTION_PACK_AR.md](packs/PARTNER_MOTION_PACK_AR.md) |
| Client / Proof | [packs/CLIENT_DEMO_PACK_AR.md](packs/CLIENT_DEMO_PACK_AR.md) |
| Investor (خفيف) | [packs/INVESTOR_MOTION_PACK_AR.md](packs/INVESTOR_MOTION_PACK_AR.md) |

## لوحة CEO (جدول شهري — لا واجهة)

يُبنى يدويًا من [HOLDING_VALUE_REGISTRY_AR.md](HOLDING_VALUE_REGISTRY_AR.md) + السجل:

- **Asset, Type, Audience, Boundary, Value scores, Evidence, LastUsed, UsageCount, Best outcome, Next action**
- **قرار:** Invest / Activate / Package / Revise / Archive review / Do not send

المخرجات الآلية تساعد: [_generated/holding_value_summary.json](_generated/holding_value_summary.json)، [_generated/asset_activation_priorities.json](_generated/asset_activation_priorities.json)، [_generated/asset_capital_allocation.json](_generated/asset_capital_allocation.json).

## ما لا تفعله

لا توسيع فهرسة لـ195 مجلدًا يدويًا؛ لا dashboard قبل أدلة استخدام؛ لا حذف جماعي — انظر [DOCS_DECISION_RULES_AR.md](DOCS_DECISION_RULES_AR.md).

**الإيقاع:** [DOCS_REVIEW_CADENCE_AR.md](DOCS_REVIEW_CADENCE_AR.md) و [MONTHLY_ASSET_COUNCIL_AR.md](MONTHLY_ASSET_COUNCIL_AR.md).
