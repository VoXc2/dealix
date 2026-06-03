# Account Pack — Output Contract (عقد المخرجات)

> العقد الكامل لحقول الـ Account Pack. المصدر الرسمي للحقيقة هو المخطط:
> `schemas/account_intelligence_pack.schema.json`. هذا المستند شرحٌ عربيّ له.

---

## 1. الحقول (40 حقلاً)

### الهوية والقطاع
| الحقل | النوع | إلزامي | ملاحظات |
|------|------|:-----:|---------|
| `id` | string | ✅ | `ACC-001` |
| `company_name` | string | ✅ | |
| `website` | string\|null | — | عام أو null |
| `country` | string | ✅ | `SA` |
| `city` | string\|null | — | |
| `sector` | string | ✅ | |
| `subsector` | string\|null | — | |
| `services_detected` | string[] | — | خدمات ظاهرة علنًا فقط |
| `business_model_hint` | string\|null | — | |

### التواصل (عام فقط — لا اختراع)
| الحقل | النوع | إلزامي | ملاحظات |
|------|------|:-----:|---------|
| `public_contact_channels` | enum[] | — | website/contact_page/linkedin… |
| `phone_if_public` | string\|null | — | فقط إن نُشر علنًا، وإلا null |
| `email_if_public` | string\|null | — | فقط عنوان عام منشور، لا تخمين |
| `contact_page_url` | string\|null | — | |
| `social_links` | string[] | — | روابط عامة |
| `google_business_hint` | string\|null | — | |
| `likely_decision_maker_role` | string | ✅ | **دور** لا اسم مخترع |
| `secondary_contact_role` | string\|null | — | |
| `best_contact_route` | enum | ✅ | كيف نصل عبر قنوات عامة |
| `contact_confidence` | C0–C4 | ✅ | راجع `docs/contacts/CONTACT_CONFIDENCE_LEVELS_AR.md` |

### الإشارة والألم والنظام
| الحقل | النوع | إلزامي | ملاحظات |
|------|------|:-----:|---------|
| `buying_signal` | string\|null | — | إشارة عامة مؤرّخة أو null |
| `signal_source` | string\|null | — | المصدر العام للإشارة |
| `likely_pain` | string | ✅ | احتمالية لـ L0/L1 |
| `recommended_system` | enum(5) | ✅ | نظام واحد فقط |
| `why_this_system` | string | ✅ | بلا ادعاء مضمون |
| `first_sprint_offer` | string | ✅ | |
| `proof_angle` | string\|null | — | |

### الرسائل والاتصال
| الحقل | النوع | إلزامي | ملاحظات |
|------|------|:-----:|---------|
| `email_subject` | string | ✅ | |
| `email_body` | string | ✅ | لا Re:/Fwd: مزيفة، لا ادعاء مضمون |
| `call_opener` | string\|null | — | |
| `call_questions` | string[] | — | |
| `expected_objections` | string[] | — | |

### العرض والتسليم
| الحقل | النوع | إلزامي | ملاحظات |
|------|------|:-----:|---------|
| `mini_proposal_title` | string\|null | — | |
| `mini_proposal_angle` | string\|null | — | |
| `delivery_pack` | string[] | — | ما يُسلَّم في أول Sprint |
| `required_inputs` | string[] | — | مدخلات العميل المطلوبة |

### التصنيف والحوكمة
| الحقل | النوع | إلزامي | ملاحظات |
|------|------|:-----:|---------|
| `risk_level` | low/medium/high | ✅ | |
| `evidence_level` | L0–L4 | ✅ | |
| `cash_priority_score` | int 0–100 | ✅ | |
| `next_action` | string | ✅ | |
| `owner` | string | ✅ | مالك بشري للخطوة |
| `status` | enum | ✅ | يبدأ `draft` — لا إرسال آلي |

---

## 2. الثوابت (Enums)

```
recommended_system ∈ {
  "Revenue Operating System",
  "Executive Command OS",
  "Follow-up Recovery OS",
  "WhatsApp Client OS",
  "Proposal & Proof OS"
}
evidence_level    ∈ { L0, L1, L2, L3, L4 }
contact_confidence∈ { C0, C1, C2, C3, C4 }
risk_level        ∈ { low, medium, high }
status            ∈ { draft, approval_queue, approved, sent, rejected, nurture, won, lost }
```

---

## 3. قواعد لا تتفاوض (مفروضة آليًا)

1. `recommended_system` نظام **واحد** من الخمسة.
2. `likely_decision_maker_role` يجب أن يكون **دورًا صالحًا** للنظام (راجع Role Targeting Matrix).
3. إذا `evidence_level` ∈ {L0, L1} → النص يحتوي لغة احتمالية.
4. لا ادعاءات مضمونة في `email_body` أو `why_this_system`.
5. `status` يبدأ `draft`؛ لا إرسال بدون اعتماد بشري.
6. لا اختراع جهات اتصال: `phone_if_public`/`email_if_public` = null إن لم تُنشر.

> هذه القواعد يفرضها `scripts/account-factory-check.mjs` (`npm run factory:check`).

---

## 4. مثال مختصر

```json
{
  "id": "ACC-001",
  "company_name": "Madar Marketing Agency",
  "recommended_system": "Revenue Operating System",
  "likely_decision_maker_role": "Head of Sales",
  "best_contact_route": "official_contact_page",
  "contact_confidence": "C2",
  "evidence_level": "L2",
  "risk_level": "low",
  "cash_priority_score": 74,
  "status": "draft"
}
```

المثال الكامل (40 حقلاً) في `data/account_intelligence/account_packs.jsonl`.

---

*Account Pack Output Contract | الإصدار 1.0 | آخر تحديث: 2026-06-03*
