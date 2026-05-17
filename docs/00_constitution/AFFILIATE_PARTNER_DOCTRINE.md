# عقيدة الشركاء والمسوّقين بالعمولة — Affiliate & Partner Doctrine

## الدور — Role

حدّ ثقة لقناتي الإحالة: الشركاء (Partners) والمسوّقين بالعمولة (Affiliates).
A trust boundary for the two referral channels: partners and affiliates.

هذه الوثيقة **امتداد** لـ [NON_NEGOTIABLES.md](./NON_NEGOTIABLES.md) — لا تنسخها ولا
تستبدلها. كل بند هنا يخضع لنفس البنود الإحدى عشر غير القابلة للتفاوض، ويضيف بوّابات
خاصة بدخْل قناتي الإحالة (money-touching channels).

This document **extends** [NON_NEGOTIABLES.md](./NON_NEGOTIABLES.md). It does not
replace it. Every clause here inherits the 11 non-negotiables and adds gates
specific to the money-touching referral channels.

## لماذا — Why

برنامج العمولة يلمس الإيراد والادعاءات والبيانات. بدون عقيدة صريحة، أي مسوّق قد
يَعِد بنتائج، أو يرسل رسائل باردة، أو يطالب بعمولة قبل الدفع. هذه الوثيقة تجعل
الانضباط شرطًا تقنيًا، لا توصية.

## البوّابات — Gates

كل بوّابة أدناه هي مرشّح لاختبار `tests/test_no_*.py` في مرحلة البناء (V2/V3).
لا يُبنى أي اختبار في هذه المرحلة — هذه وثيقة عقيدة فقط.

1. **لا عمولة قبل الدفع — No commission before payment.**
   لا تُحتسب عمولة الشريك/المسوّق إلا بعد وجود حدث `invoice_paid` في سجل الأدلة.
   يرث البند رقم 2 (no live charge): صرف العمولة يتطلب موافقة المؤسس.
   Gate candidate: `test_no_affiliate_payout_before_paid`.

2. **الإفصاح إلزامي وقابل للفحص آليًا — Mandatory, machine-checkable disclosure.**
   كل محتوى ترويجي يجب أن يحمل إفصاحًا ظاهرًا قبل أي دعوة لإجراء (CTA).
   النصّ المعتمد في [`data/config/affiliate_rules.yaml`](../../data/config/affiliate_rules.yaml).
   Gate candidate: `test_affiliate_disclosure_required`.

3. **رسائل معتمدة فقط — Approved messaging only.**
   يستخدم المسوّق قوالب معتمدة من المؤسس فقط. قائمة الادعاءات الممنوعة
   (أرباح/ROI/أمن/امتثال مضمونة، إرسال ذاتي، نتائج عملاء غير موثّقة، دراسات حالة غير
   معتمدة) في `affiliate_rules.yaml`.
   Gate candidate: `test_no_affiliate_unapproved_message`.

4. **لا تواصل بارد — No cold outreach.**
   ممنوع WhatsApp البارد، وأتمتة LinkedIn، والقوائم المسحوبة (scraped). هذا يرث
   البندين 1 و3 من غير القابل للتفاوض مباشرة.

5. **مخالفة الامتثال تُجمّد الصرف — A compliance flag freezes payout.**
   أي علم امتثال مفتوح (إفصاح ناقص، ادعاء غير معتمد، تواصل بارد، مخالفة معالجة
   بيانات) يوقف صرف العمولة ويوقف استلام الإحالات حتى الإغلاق.

6. **مسار مال واحد — One money path.**
   تركب العمولة على **سجل الإحالة القائم** ولا تنشئ مسارًا موازيًا:
   - `auto_client_acquisition/value_os/value_ledger.py` — سجل القيمة/الإيراد.
   - `auto_client_acquisition/partnership_os/referral_tracker.py` — تتبّع الإحالة.
   - `auto_client_acquisition/partnership_os/referral_store.py` — تخزين الإحالة.
   لا يُنشأ محرّك صرف (payout engine) مستقل.

## التطبيق — Where this lives

| الطبقة | المسار |
| --- | --- |
| العقيدة | هذه الوثيقة + سطر مرجعي في `NON_NEGOTIABLES.md` |
| القواعد القابلة للضبط | [`data/config/affiliate_rules.yaml`](../../data/config/affiliate_rules.yaml), [`data/config/partner_rules.yaml`](../../data/config/partner_rules.yaml) |
| منطق التشغيل (مرحلة بناء لاحقة) | `auto_client_acquisition/partnership_os/` |
| سجل المال | `auto_client_acquisition/value_os/` |
| الوثائق القائمة (لا تُعاد كتابتها) | `docs/partners/`, `docs/40_partners/`, `docs/AGENCY_PARTNER_PROGRAM.md`, `docs/sales-kit/dealix_referral_program.md` |

## خارج النطاق — Out of scope (هذه المرحلة)

- بناء اختبارات البوّابات `tests/test_no_*.py` — مرشّحة، لا مبنية.
- بوّابة الشركاء/المسوّقين في الواجهة (Partner/Affiliate Portal) — مرحلة V3.
- ربط ملفات YAML بالكود.
