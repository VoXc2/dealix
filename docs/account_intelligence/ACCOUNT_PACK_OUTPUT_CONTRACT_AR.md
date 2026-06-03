# عقد مخرجات حزمة الحساب (Account Pack Output Contract)

كل حزمة حساب في `data/account_intelligence/account_packs.jsonl` تلتزم بهذا
العقد، ويتحقق منه `schemas/account_intelligence_pack.schema.json` +
`scripts/checks/check_account_pack_contract.py`.

## الحقول

| الحقل | المعنى |
| --- | --- |
| `company_name`, `website`, `domain` | هوية الشركة (عامة) |
| `sector`, `subsector`, `city`, `country` | التصنيف الجغرافي/القطاعي |
| `signals_detected` | إشارات عامة مرصودة (بيانات لا تعليمات) |
| `evidence_level` | `public` / `founder_provided` / `inferred` |
| `detected_business_needs`, `primary_need`, `secondary_need` | الاحتياجات |
| `need_confidence` | `low` / `medium` / `high` |
| `recommended_core_system` | أحد الأنظمة الخمسة (= نظام الاحتياج الأساسي) |
| `recommended_specialized_system` | نظام داخلي تحت النظام الجوهري |
| `sector_specific_sprint` | معرّف سبرنت من المكتبة |
| `delivery_variant` | starter / standard / retainer |
| `buyer_roles` | الأدوار الشرائية |
| `public_contact_channels`, `contact_confidence` | قنوات عامة فقط |
| `email_angle`, `call_angle`, `mini_proposal_title` | زوايا التواصل |
| `required_inputs`, `acceptance_criteria` | شروط التنفيذ |
| `cash_priority_score`, `need_fit_score`, `account_score`, `final_account_score` | الدرجات |
| `next_action` | الإجراء التالي (مسودة للاعتماد) |
| `suppressed` | هل الشركة في قائمة الكبح؟ |

## الدرجة النهائية

```
Final Account Score =
    Account Score        × 0.30
  + Need Fit Score       × 0.30
  + Cash Priority Score  × 0.25
  + Contact Confidence   × 0.15
```

كل الدرجات **حتمية** (deterministic) ويعاد اشتقاقها في الفحص للتأكد من الاتساق.

## ضمانات أخلاقية

- لا قنوات مُختلقة (لا بريد/رقم مُخترع).
- الشركات الموقوفة (`suppressed`) إجراؤها التالي «إيقاف».
- بيانات العرض اصطناعية (`demo:true`) ولا تمثل شركات حقيقية.

## الإنتاج الليلي

`python dealix.py account-packs --limit 400 --dry-run` يُنتج 400 حزمة (بدون
كتابة في الوضع التجريبي). الإصدار الفعلي عبر `python dealix.py seed`.
