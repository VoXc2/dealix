# Saudi Legal Classification Matrix — Draft for Counsel

الغرض: منع استخدام عقد واحد لكل الناس. قبل التفعيل يصنف النظام العلاقة أولًا.

| Scenario | Default Classification | Required Gate | Notes |
|---|---|---|---|
| سعودي يقدم إحالات/تسويق كعمل مستقل | Independent Referral/Marketing Partner | identity + lawful activity status + terms + tax profile | وثيقة العمل الحر قد تكون مسارًا مناسبًا بحسب النشاط المتاح فعليًا؛ لا نفترضها تلقائيًا. |
| سعودي يعمل بأجر بالساعة وتحت تنظيم عمل Dealix | Flexible Worker | HR/legal + HRSD flexible work contract | العمل المرن للسعوديين ويجب توثيق العقد في المنصة المحددة. |
| سعودي بوظيفة عن بعد منظمة | Remote Employee | HR/Qiwa/remote work path | لا نستخدم عقد شريك لإخفاء علاقة عمل فعلية. |
| وكالة/شركة سعودية | B2B Channel Partner | CR/activity + authorized signatory + VAT/tax + contract | يمكنها co-sell ضمن صلاحيات محددة. |
| غير سعودي مقيم يريد ممارسة خدمة تسويق/مبيعات لحسابه | HOLD | legal/work authorization check | لا تمكين لنشاط اقتصادي غير مرخص؛ Anti-Concealment hard gate. |
| جهة/فرد يدّعي صفة “وكيل تجاري” | HOLD | Commercial Agency legal review | لا نستخدم هذه الصفة كاسم عام للبرنامج. |
| وسيط/مسوق عقاري | OUT-OF-SCOPE unless licensed | sector license review | الوساطة العقارية نشاط منظم مستقل. |
| فرصة حكومة/B2G | Compliance Controlled | anti-bribery + procurement + conflict review | لا success fee على نفوذ/وصول لمسؤول عام. |
| Creator/Affiliate ينشر محتوى عام | Referral/Media Partner | disclosure + claims approval + campaign tracking | الإعلان يجب أن يكون واضحًا وغير مضلل. |

## Employment Misclassification Signals
إذا اجتمعت عناصر مثل ساعات مفروضة، إشراف يومي، حصرية، أهداف/حضور كموظف، أدوات وعمل مستمر تحت إدارة Dealix، فالنظام يرفع `POSSIBLE_EMPLOYMENT_RELATIONSHIP=HOLD` بدل تمرير Independent Partner تلقائيًا.

## Non-Saudi Guard
`NON_SAUDI_INDEPENDENT_ECONOMIC_ACTIVITY = HOLD_UNTIL_AUTHORIZATION_PROVEN`
لا يكفي وجود إقامة أو حساب بنكي. يجب أن يحدد المستشار القانوني/العمالي المسار النظامي المناسب للحالة الفعلية.

## Tax/VAT Profile
- partner_type: individual / sole proprietor / company.
- VAT registered? yes/no/unknown.
- VAT number if applicable.
- Annual economic revenue declaration is partner responsibility; ZATCA currently states mandatory individual VAT registration above SAR 375,000 annual revenue and optional registration from SAR 187,500 to SAR 375,000.
- Dealix accounting determines required invoice/tax document per status; portal never fabricates tax treatment.