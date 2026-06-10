# فهرس غرفة البيانات — Dealix Data Room Index

> **هذا هو الفهرس الرسمي لغرفة بيانات Dealix.** كل investor / partner /
> enterprise / grant جهة تطلب معلومات، يُشار إليها إلى القسم الصحيح.
> لا معلومات في هذا الـ data room بدون مصدر موثّق أو تصنيف "TBD".

**الحالة:** مسودة — Phase 1 من Agent #16
**التاريخ:** 2026-06-03

---

## 1. الأقسام (Sections)

| # | القسم | الملف | الحالة |
| - | --- | --- | --- |
| 1 | Company | `docs/data_room/COMPANY_OVERVIEW_AR.md` | 🟡 TBD |
| 2 | Product | `docs/data_room/PRODUCT_OVERVIEW_AR.md` | 🟡 TBD |
| 3 | Market | `docs/data_room/MARKET_OVERVIEW_AR.md` | 🟡 TBD |
| 4 | GTM | `docs/data_room/GTM_OVERVIEW_AR.md` | 🟡 TBD |
| 5 | Commercial Model | `docs/data_room/COMMERCIAL_MODEL_AR.md` | 🟡 TBD |
| 6 | Technology | `docs/data_room/TECH_ARCHITECTURE_OVERVIEW_AR.md` | 🟡 TBD |
| 7 | Security / Privacy | `docs/data_room/SECURITY_PRIVACY_OVERVIEW_AR.md` | 🟡 TBD |
| 8 | Operations | link → `docs/FOUNDER_OPERATING_SYSTEM_AR.md` | ✅ |
| 9 | Finance | link → `docs/finance/` + `docs/UNIT_ECONOMICS_AND_MARGIN.md` | ✅ |
| 10 | Roadmap | `docs/data_room/ROADMAP_OVERVIEW_AR.md` | 🟡 TBD |
| 11 | Risks | `docs/data_room/RISK_REGISTER_SUMMARY_AR.md` | 🟡 TBD |
| 12 | Traction | `docs/data_room/TRACTION_TEMPLATE_AR.md` | 🟡 TBD |
| 13 | Partnerships | link → `docs/partnerships/` + `docs/PARTNER_LEGAL_AGREEMENT.md` | ✅ |
| 14 | Legal / Compliance | link → `docs/legal/COMPLIANCE_CERTIFICATIONS.md` | ✅ |

## 2. Legend

- ✅ جاهز ومراجع
- 🟡 TBD — needs founder input
- 🔴 placeholder — not yet started

## 3. كيف تستخدم هذا الفهرس

### 3.1 مستثمر (Investor)
1. ابدأ بـ `DEALIX_COMPANY_ONE_PAGER_AR.md` (one-pager).
2. اقرأ `INVESTOR_PARTNER_MEMO_AR.md` (memo).
3. ارجع للأقسام 1–14 حسب السؤال.

### 3.2 شريك استراتيجي (Strategic Partner)
1. ابدأ بـ `DEALIX_BOARD_BRIEF_AR.md`.
2. الأقسام 2 (Product) و 4 (GTM) و 13 (Partnerships).

### 3.3 عميل enterprise (Enterprise Client)
1. `COMPANY_OVERVIEW_AR.md` و `PRODUCT_OVERVIEW_AR.md`.
2. `SECURITY_PRIVACY_OVERVIEW_AR.md` و `docs/ENTERPRISE_MSA_TEMPLATE.md`.
3. `COMPLIANCE_CERTIFICATIONS.md`.

### 3.4 مؤسسة / منحة (Grant / Accelerator)
1. `COMPANY_OVERVIEW_AR.md` و `ROADMAP_OVERVIEW_AR.md`.
2. `TRACTION_TEMPLATE_AR.md` و `RISK_REGISTER_SUMMARY_AR.md`.

## 4. قواعد الحقيقة (Truth Rules)

1. **No fake traction.** أي رقم بدون مصدر ⇒ "TBD — evidence pending".
2. **No fake clients.** أي اسم عميل بدون إذن ⇒ anonymize.
3. **No inflated claims.** أي ادعاء بنسبة/رقم ⇒ baseline موثّق.
4. **No secrets.** لا API keys، لا DB URLs حقيقية، لا internal tokens.
5. **Evidence levels:** L0 (لا دليل) → L5 (تدقيق خارجي).

| Level | الوصف | مثال |
| --- | --- | --- |
| L0 | لا دليل / ادعاء فقط | "we serve 100s of clients" |
| L1 | عدد تقديري بدون قائمة | "we have ~30 SMEs in pipeline" |
| L2 | قائمة مجهولة | "5 paying clients in Riyadh" |
| L3 | قائمة معروفة (بدون إذن) | "3 named logos (with NDA)" |
| L4 | case study + إذن | "Acme case study (signed consent)" |
| L5 | تدقيق خارجي | "audited by Big 4 in 2025" |

## 5. ما يجب ألا يكون في Data Room

- كلمات مرور، API keys، tokens
- DB URLs production
- معلومات عميل بدون إذن (`case_study_permissions.jsonl`)
- ادعاءات غير موثّقة
- معلومات مالية شخصية (راتب المؤسس، حسابات بنكية)
- وثائق قانونية مسودة (use final versions only)

## 6. الصلاحيات

| الإجراء | المطلوب |
| --- | --- |
| إضافة قسم جديد | المؤسس + مراجعة |
| تحديث رقم traction | المؤسس + مصدر موثّق |
| مشاركة data room مع طرف خارجي | المؤسس + NDA/agreement |
| طباعة / export | ممنوع (always review before share) |

## 7. التحديث

- **Quarterly:** مراجعة الأرقام، تحديث TRACTION.
- **عند تغيير جوهري:** تحديث القسم المتأثر + DATA_ROOM_INDEX.
- **CHANGELOG:** كل تحديث في `CHANGELOG.md` (قسم Data Room).

## 8. روابط مفيدة

- `docs/STRATEGIC_MASTER_PLAN_2026.md`
- `docs/BUSINESS_MODEL.md`
- `docs/EXECUTIVE_DECISION_PACK.md`
- `docs/COMMERCIAL_LAUNCH_MASTER_PLAN.md`
- `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md`
- `docs/localization/SAUDI_MENA_LOCALIZATION_SYSTEM.md`
- `docs/agent_definitions/AGENTS_12_TO_17_INDEX.md`

## 9. المراجع

- `reports/data_room/DATA_ROOM_READINESS_REVIEW.md` — gap audit
- `reports/data_room/DATA_ROOM_FINAL_REPORT.md` — final report
- `docs/legal/CASE_STUDY_PERMISSION_POLICY_AR.md` — case study policy
- `docs/legal/CLAIMS_EVIDENCE_MATRIX_AR.md` — claims matrix
