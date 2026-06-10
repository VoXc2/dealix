# سياسة إذن دراسة الحالة — Dealix Case Study Permission Policy

> **وثيقة تشغيلية.** لا دراسة حالة باسم عميل تُنشر بدون إذن مكتوب
> موثَّق في `data/legal/case_study_permissions.jsonl`.

**الحالة:** مسودة — Phase 1 من Agent #13
**التاريخ:** 2026-06-03

---

## 1. مستويات دراسة الحالة

| المستوى | الوصف | الإذن المطلوب |
| --- | --- | --- |
| **L0** | لا دراسة حالة (mention عام بدون عميل) | لا شيء |
| **L1** | دراسة حالة مفترضة / مركّبة (composite) | لازم يُعلَّم صراحةً "سيناريو افتراضي" |
| **L2** | دراسة حالة مجهولة الهوية (sector + نتيجة، بدون اسم) | مراجعة Medium |
| **L3** | دراسة حالة باسم الشركة + علامة تجارية | مراجعة High + إذن العميل |
| **L4** | دراسة حالة مع شعار العميل + اقتباس + رقم | مراجعة High + إذن العميل + DPO |
| **L5** | دراسة حالة enterprise مع KPIs تفصيلية | مراجعة Critical + محامٍ |

## 2. متى يُطلب الإذن

- ذكر اسم العميل في أي artifact عام (blog, social, deck, case_study.md,
  partner pitch).
- عرض شعار العميل.
- استخدام اقتباس مباشر من العميل.
- ذكر رقم محدد (revenue, ROI, time saved) مرتبط بالعميل.
- مشاركة proof pack مع طرف ثالث (partner, investor).

## 3. كيف يُطلب الإذن

1. إرسال `CASE_STUDY_CONSENT_FLOW_AR.md` للعميل عبر email أو توقيع في
   meeting.
2. العميل يوافق / يرفض / يعدّل.
3. تسجيل القرار في `data/legal/case_study_permissions.jsonl`.
4. لا نشر قبل `decision = APPROVED`.

## 4. السجل (JSONL Schema)

```json
{
  "permission_id": "csp_2026_06_03_001",
  "client_id": "acme_sa",
  "client_name": "Acme KSA",
  "client_contact": "cfo@acme.sa",
  "level": "L4",
  "artifact_refs": [
    "docs/case-studies/acme_q2_2026.md",
    "data/proofs/acme_proof_pack_v3.pdf"
  ],
  "claims_in_artifact": [
    "3x pipeline growth in 60 days",
    "saved 14 hours/week on follow-up"
  ],
  "evidence_refs": [
    "proof_event_xyz",
    "approval_abc"
  ],
  "consent_method": "email|signature|verbal_with_followup",
  "consent_date": "2026-06-03",
  "consent_expires": "2027-06-03",
  "revocable": true,
  "decision": "PENDING|APPROVED|REJECTED|MODIFIED",
  "decision_notes": "",
  "decided_by": "founder",
  "decided_at": "2026-06-03T10:00:00+03:00"
}
```

## 5. حق السحب

- العميل يحق له سحب الإذن في أي وقت.
- السحب ⇒ حذف / إخفاء دراسة الحالة خلال 14 يوم عمل.
- تحديث السجل بـ `decision = REJECTED` + `revoked_at`.

## 6. ما لا يحتاج إذن

- mention عام بدون اسم (e.g. "a Riyadh-based logistics company").
- ذكر sector فقط (e.g. "in healthcare").
- ذكر رقم industry benchmark موثّق.
- mention ذاتي (e.g. "we onboarded 12 clients in Q2").

## 7. مخاطر عالية متبقية

1. لا يوجد automated check في CI يمنع نشر case study بدون إذن.
2. لا يوجد expiry check للـ permissions القديمة.
3. لا يوجد reminder للعميل قبل expiry.

## 8. الأدوات

- `tests/test_no_fake_proof.py` — fake proof check
- `tests/test_v7_no_fake_proof.py` — v7 fake proof check
- `docs/PROOF_AND_CASE_STUDY_SYSTEM.md` — proof system

## 9. المراجع

- `docs/legal/LEGAL_REVIEW_POLICY_AR.md` — triggers
- `docs/legal/CASE_STUDY_CONSENT_FLOW_AR.md` (يُنشأ في Phase 3)
- `docs/legal/CLAIMS_EVIDENCE_MATRIX_AR.md` (يُنشأ في Phase 3)
- `docs/PROOF_AND_CASE_STUDY_SYSTEM.md` — proof system
- `docs/PRIVACY_POLICY_v2.md` — privacy
