# Contact Targeting Matrix — مصفوفة استهداف الدور

*أي دور نخاطب لكل نظام. المدقّق يفرض أن دور كل باقة يطابق نظامها.*
*آخر تحديث: 2026-06-03*

---

## المصفوفة

| النظام | الشخص الأول | البديل | سبب الاستهداف |
|--------|-------------|--------|----------------|
| Revenue OS (`revenue_os`) | Head of Sales / Founder | Marketing Manager / GM | مسؤول عن الفرص والإيراد |
| Executive Command OS (`executive_command_os`) | Founder / CEO / GM | Operations Manager | يملك قرار الإدارة والتقارير |
| Follow-up Recovery OS (`followup_recovery_os`) | Sales Manager / Marketing Manager | Founder | يملك المتابعة والحملات |
| WhatsApp Client OS (`whatsapp_client_os`) | Operations / Customer Service Manager | Founder / Clinic Manager | يملك تجربة العميل والواتساب |
| Proposal & Proof OS (`proposal_proof_os`) | Founder / BD / Sales Lead | Marketing Manager | يملك العروض والإقناع |

---

## التحقق الآلي (Enforced)

`scripts/validate_account_intelligence.py` يطابق `likely_decision_maker_role`
(و `target_role` في الاكتشاف) مع قائمة الأدوار المسموحة لكل نظام عبر مطابقة
رموز نصية (case-insensitive substring). أمثلة الرموز:

```txt
revenue_os            → head of sales, sales, founder, ceo, gm, marketing manager …
executive_command_os  → founder, ceo, gm, operations, coo, partner …
followup_recovery_os  → sales manager, sales, marketing manager, founder …
whatsapp_client_os    → operations, customer service, support, clinic manager …
proposal_proof_os     → founder, bd, business development, sales lead, partner …
```

> إذا استهدفت باقة دورًا لا ينتمي للنظام (مثل استهداف «Warehouse Clerk» لـ Revenue OS)
> يفشل الفحص فورًا.

---

## إذا لم نجد اسم شخص

نخاطب الدور/الفريق:

```txt
إلى فريق الإدارة / فريق المبيعات / فريق التسويق / فريق العمليات / فريق خدمة العملاء
```

ولا نخترع اسمًا. (راجع `CONTACT_DISCOVERY_POLICY_AR.md`.)

---

## أمثلة من التشغيل الحالي

| Company | System | Targeted role | Secondary |
|---------|--------|---------------|-----------|
| Digital Rise Agency | revenue_os | Head of Sales | Founder / CEO |
| Growth Labs SA | followup_recovery_os | Marketing Manager | Founder |
| TrainMe KSA | whatsapp_client_os | Customer Service Manager | Operations Manager |
| TechVenture Partners | executive_command_os | Founder | Operations Manager |
| LegalEdge SA | proposal_proof_os | Managing Partner | BD Manager |
