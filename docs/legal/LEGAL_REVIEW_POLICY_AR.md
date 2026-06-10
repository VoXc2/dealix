# سياسة المراجعة القانونية — Dealix Legal Review Policy

> **وثيقة تشغيلية، ليست استشارة قانونية.** كل بند يحتاج توجيهاً
> قانونياً نهائياً يجب أن يُحال إلى محامٍ مرخّص في المملكة العربية
> السعودية، أو إلى المؤسس بعد التحقق من الأساس القانوني.

**الحالة:** مسودة — Phase 1 من Agent #13
**التاريخ:** 2026-06-03

---

## 1. الغرض

تحدد هذه الوثيقة **متى** يجب إيقاف العمل وطلب مراجعة قانونية، ومن
يقرر ذلك، وكيف يُسجَّل القرار. لا يحق لأي agent أو نموذج لغوي إنشاء
التزام قانوني نهائي. كل التزام يمر عبر هذه السياسة.

## 2. قائمة المحفزات (Legal Review Triggers)

| # | المحفز | المستوى | الجهة المراجِعة |
| - | --- | --- | --- |
| 1 | عقد نهائي مع عميل (MSA, SOW, DPA signed) | **Critical** | محامٍ مرخّص + المؤسس |
| 2 | شروط دفع غير قياسية (خصم مرتبط بأداء، revenue share) | **Critical** | محامٍ + المؤسس + Finance |
| 3 | خصم أكبر من 20% على السعر القياسي | **High** | المؤسس |
| 4 | study case باسم عميل (named case study) | **High** | المؤسس + موافقة العميل |
| 5 | التزام معالجة بيانات يتجاوز DPA القياسي | **High** | المؤسس + DPO |
| 6 | مشروع enterprise / custom يتجاوز SAR 250,000 | **Critical** | محامٍ + المؤسس |
| 7 | اتفاقية شريك revenue share أو حصري | **Critical** | محامٍ + المؤسس |
| 8 | ادعاء قانوني عام (e.g. "we are the first", "the only") | **High** | المؤسس |
| 9 | ادعاء يخص قطاع منظَّم (صحة، تعليم، مالي) | **High** | محامٍ قطاع + المؤسس |
| 10 | بنود استرداد / dispute غير قياسية | **High** | المؤسس |
| 11 | التزام SLA بمستوى 99.9%+ | **High** | المؤسس + Ops |
| 12 | معالجة بيانات خارج السعودية (cross-border) | **High** | محامٍ + DPO |
| 13 | sub-processor جديد | **Medium** | DPO + Ops |
| 14 | إقرار ضريبة (ZATCA) غير قياسي | **Medium** | محاسب + المؤسس |
| 15 | ذكر اسم عميل في مادة عامة (blog, social, case study) | **Medium** | المؤسس + موافقة العميل |
| 16 | استخدام علامة تجارية لطرف ثالث | **Medium** | المؤسس |

## 3. مستويات الموافقة (Approval Levels)

| المستوى | من يقرر | زمن الاستجابة |
| --- | --- | --- |
| **Low** | Agent آلي (داخل قواعد محددة) | فوري |
| **Medium** | Operator (Agent #2) أو المؤسس | < 4 ساعات عمل |
| **High** | المؤسس | < 24 ساعة |
| **Critical** | محامٍ مرخّص + المؤسس | < 5 أيام عمل |

## 4. كيف تسجِّل Agent المراجعة

1. **قبل** إنشاء artifact حساس، الـ agent يكتب entry في
   `data/legal/legal_reviews.jsonl` بالحقول:
   ```json
   {
     "review_id": "rev_2026_06_03_001",
     "trigger_id": 4,
     "artifact_kind": "case_study",
     "artifact_ref": "case_study_acme.md",
     "claim": "Acme achieved 3x pipeline in 60 days",
     "evidence_refs": ["proof_event_xyz", "approval_abc"],
     "evidence_tier": "L4_named_with_consent",
     "risk_level": "High",
     "requester_agent": "agent_15",
     "reviewer": "founder",
     "decision": "PENDING|APPROVED|REJECTED|MODIFIED",
     "decision_notes": "...",
     "decided_at": "2026-06-03T10:00:00+03:00"
   }
   ```
2. الـ artifact **لا يُنشر** قبل أن يكون `decision` = `APPROVED`.
3. Decision بدون `decided_at` = لم يُبتّ.

## 5. القواعد غير القابلة للتفاوض

1. **لا agent يضع "APPROVED"** على مراجعة critical. هذا المؤسس فقط
   بعد التحقق.
2. **لا محاكاة قرار مراجعة.** كل decision له timestamp واسم مراجع
   حقيقي.
3. **لا claim بدون evidence_refs.** لو الـ evidence ضعيف أو غائب
   ⇒ `REJECTED` أو `MODIFIED`.
4. **لا ادعاء قابل للقياس** (ROI %, time saved, etc.) بدون baseline
   موثّق.
5. **لا ادعاء "first" / "only" / "best"** بدون مقارنة موثّقة بتاريخ
   المقارنة.
6. **لا ادعاء "compliant"** (PDPL, ZATCA, ISO) بدون شهادة أو تقرير
   تدقيق رسمي مرتبط.
7. **لا named case study** بدون `case_study_permissions.jsonl` entry
   بحالة `APPROVED`.

## 6. ما لا يحتاج مراجعة

- رسائل WhatsApp ضمن قوالب معتمدة (`data/templates/whatsapp_templates_*.md`).
- محتوى تقرير weekly ينتج عن approved proof event.
- عروض أسعار ضمن `pricing.md` المعتمد.
- رسائل outbound لحساب مسجَّل في warm-list (لها قواعد أخرى، ليست
  هنا).
- محتوى marketing ضمن `data/templates/` المعتمد.

## 7. ما يحتاج مراجعة متكررة

- **عند تحديث template:** أي تعديل على قالب WhatsApp/email معتمد
  يحتاج مراجعة Medium.
- **عند تغيير pricing:** أي تعديل على `pricing.md` يحتاج مراجعة High.
- **عند إضافة integration:** أي integration جديد يحتاج مراجعة High
  (data flow + secrets + rollback).

## 8. الأدوار

| الدور | المسؤول |
| --- | --- |
| **Legal Owner** | المؤسس (حالياً) — يراجع كل Critical و High |
| **DPO** | غير معين رسمياً بعد (see `DPO_APPOINTMENT_LETTER.md`) |
| **Legal Counsel** | محامٍ خارجي (لم يُعيَّن بعد) — يراجع Critical |
| **Agent #13 (Legal Guard)** | يبني الـ guardrails ولا يوقّع على أي شيء |

## 9. مخاطر عالية متبقية

1. لا يوجد محامٍ مرخّص رسمي مرتبط بعد.
2. لا يوجد DPO معين رسمياً.
3. لا يوجد audit سنوي لتحديث هذه السياسة.
4. لا يوجد تغطية لازمات AI/ML التوليدي (EU AI Act مثلاً).

## 10. المراجع

- `docs/legal/FOUNDER_RISK_AND_COMPLIANCE_REGISTER_AR.md` — risk register
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — cert status
- `docs/legal/CONTRACT_HANDOFF_CHECKLIST_AR.md` (يُنشأ في Phase 1)
- `docs/legal/CLAIMS_EVIDENCE_MATRIX_AR.md` (يُنشأ في Phase 3)
- `docs/SECURITY_PDPL_CHECKLIST.md` — security+PDPL
- `docs/PRIVACY_PDPL_READINESS.md` — PDPL readiness
