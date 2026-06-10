# قائمة تسليم العقد — Dealix Contract Handoff Checklist

> **وثيقة تشغيلية.** كل عقد جديد (MSA, SOW, DPA) يُسلَّم إلى المراجعة
> القانونية بهذه القائمة. لا agent يُنهي العقد — المراجعة القانونية هي
> التي تُنهي.

**الحالة:** مسودة — Phase 1 من Agent #13
**التاريخ:** 2026-06-03

---

## 1. معلومات العقد الأساسية

| الحقل | القيمة | ملاحظات |
| --- | --- | --- |
| Contract ID | `con_2026_06_03_001` | فريد |
| Client name | | |
| Client entity (CR) | | |
| Signer name + role | | |
| Signer email | | |
| Product / Service | | اختر من `data/productized_services/services.yaml` |
| Contract type | MSA / SOW / DPA / Pilot | |
| Effective date | | |
| End date | | |
| Auto-renew? | | |

## 2. النطاق (Scope)

- **In scope:** (قائمة deliverables ملموسة)
- **Out of scope:** (ما لا يشمله العقد)
- **Assumptions:** (افتراضات تشغيلية)

## 3. التسعير والدفع

| البند | القيمة |
| --- | --- |
| Total contract value (SAR) | |
| Payment schedule (مقدم / عند التسليم / شهري) | |
| Currency | SAR فقط |
| Late payment terms | |
| Discount (if any) | |
| Performance-tied discount? | **إذا نعم ⇒ مراجعة Critical** |

## 4. الوصول للبيانات

- **Data accessed:** (قائمة أنواع البيانات)
- **Data source:** (أي DB / API)
- **PDPL class:** (Personal / Sensitive / Anonymous)
- **Cross-border?** | **إذا نعم ⇒ مراجعة High**
- **Data deletion at contract end:** (خطة)

## 5. حساسية الخصوصية

- **يحتاج DPA signed?** | **إذا نعم ⇒ وثيقة DPA_DEALIX_FULL.md موقّعة**
- **Sub-processors involved:** (قائمة)
- **DSAR response obligation:** (yes/no + من)

## 6. المخاطر

| المخاطرة | المستوى | Mitigation |
| --- | --- | --- |
| | | |

## 7. شروط غير قياسية (Non-Standard Terms)

- [ ] revenue share
- [ ] performance guarantee
- [ ] exclusivity
- [ ] indemnity > standard
- [ ] liability cap < standard
- [ ] SLA > 99.9%
- [ ] custom refund clause
- [ ] termination for convenience
- [ ] other: ____

**أي بند مختار ⇒ مراجعة Critical.**

## 8. الموافقات

| البند | المطلوب |
| --- | --- |
| Founder approval | ☐ |
| DPO approval (لو PDPL personal data) | ☐ |
| Legal counsel approval (لو Critical) | ☐ |
| Finance approval (لو غير standard payment) | ☐ |
| Risk register entry added? | ☐ |

## 9. التتبع

```json
{
  "contract_id": "con_2026_06_03_001",
  "status": "DRAFT|LEGAL_REVIEW|FOUNDER_REVIEW|APPROVED|SIGNED|ACTIVE|CLOSED",
  "client": "",
  "product": "",
  "scope": "",
  "out_of_scope": "",
  "price_sar": 0,
  "payment_terms": "",
  "delivery_timeline": "",
  "data_access": "",
  "privacy_sensitivity": "low|medium|high",
  "risk_level": "low|medium|high|critical",
  "non_standard_terms": [],
  "founder_approval": false,
  "legal_review_needed": true,
  "legal_review_id": null,
  "status_updated_at": "2026-06-03T10:00:00+03:00"
}
```

يُحفظ في `data/legal/contract_handoffs.jsonl`.

## 10. ما بعد التوقيع

1. أرشفة العقد الموقّع في 1Password vault `Dealix Contracts`.
2. تحديث `risk_register` بأي مخاطر جديدة.
3. إضافة العميل إلى قائمة العملاء النشطين في
   `data/clients/active.jsonl`.
4. تحديث `services_active.yaml` (قادم من Agent #15).
5. تسجيل review ID في `data/legal/legal_reviews.jsonl`.

## 11. المراجع

- `docs/legal/LEGAL_REVIEW_POLICY_AR.md` — triggers
- `docs/legal/ENTERPRISE_MSA_TEMPLATE.md` — MSA template
- `docs/legal/DPA_DEALIX_FULL.md` — DPA template
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — compliance status
- `docs/PRIVACY_POLICY_v2.md` — privacy policy
- `docs/TERMS_OF_SERVICE_v2.md` — ToS
- `docs/REFUND_POLICY.md` — refund policy
