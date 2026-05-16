# Dealix — Governed Revenue & AI Operations (Enterprise Positioning)

**الغرض:** تثبيت تموضع Dealix كشركة تشغيل إيراد وذكاء اصطناعي محكومة، لا كوكالة AI عامة ولا CRM تقليدية.

## الصياغة الرسمية

**EN:** Dealix — Governed Revenue & AI Operations  
**AR:** Dealix — تشغيل الإيراد والذكاء الاصطناعي بحوكمة، أدلة، وموافقات.

## السلسلة التشغيلية الحاكمة

```text
Signal → Source → Approval → Action → Evidence → Decision → Value → Asset
```

أي عمل لا يمر بهذه السلسلة يعدّ تشتيتًا، أو مخاطرة حوكمة، أو قيمة غير قابلة للإثبات.

## North Star

**Governed Value Decisions Created**

التعريف: عدد القرارات الإيرادية/التشغيلية التي صُنعت بمصدر واضح، موافقة واضحة، أثر قابل للقياس، وسجل أدلة كامل.

أمثلة قرار محسوب:
- متابعة حسابات عالية القيمة.
- إيقاف workflow خطر.
- منع إرسال خارجي بلا موافقة.
- تحويل Diagnostic إلى Sprint.
- إصدار فاتورة ثم تأكيد الإيراد بعد الدفع.

## الطبقات الثلاث للعرض المؤسسي

| الطبقة | القيمة | كيف تظهر في الريبو |
|--------|--------|---------------------|
| **Revenue Ops** | تحسين pipeline والفرص والقرارات | `revenue_os/` + `decision_passport/` + `api/v1/leads` |
| **Governance Ops** | ضبط حدود الموافقات والأفعال المسموحة | `approval_center` + `revenue_os/action_catalog.py` + Trust Plane |
| **Evidence Ops** | تحويل التنفيذ إلى Proof قابل للتدقيق والقياس | `proof_ledger/` + `proof_engine/` + `ProofEventCanonical` |

## الوعود التجارية المسموحة

- مسودات وإجراءات داخلية بسرعة أعلى.
- قرار أوضح، مخاطر أقل، وإيقاع تنفيذ أعلى.
- ربط AI بقيمة تشغيلية وإيرادية قابلة للإثبات.

## الوعود التجارية الممنوعة

- لا إرسال خارجي تلقائي بدون approval.
- لا ادعاء revenue قبل `invoice_paid`.
- لا claim امتثال كامل بدون مرجع موثق وموافقات.
- لا cold WhatsApp ولا LinkedIn automation ولا scraping إنتاجي.

## مراجع واجهات API

- `GET /api/v1/decision-passport/golden-chain`
- `GET /api/v1/decision-passport/evidence-levels`
- `GET /api/v1/revenue-os/catalog`
- `POST /api/v1/revenue-os/signals/normalize`
- `POST /api/v1/revenue-os/anti-waste/check`
- `POST /api/v1/leads` (يرجع `decision_passport` + `customer_readiness`)

## مراجع

- [DEALIX_MASTER_OPERATING_MODEL_AR.md](DEALIX_MASTER_OPERATING_MODEL_AR.md)
- [DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md)
- [DEALIX_MARKET_DIFFERENTIATION_AR.md](DEALIX_MARKET_DIFFERENTIATION_AR.md)
- [ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md](ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md)
- [dealix/registers/no_overclaim.yaml](../../dealix/registers/no_overclaim.yaml)
