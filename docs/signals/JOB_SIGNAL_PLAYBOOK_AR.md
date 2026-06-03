# Dealix — كتيّب إشارات الوظائف (Job Signal Playbook)

> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`
> **المصدر:** لوحات وظائف عامة فقط (`public_job_board` · `public_careers_page`). لا
> scraping مخالف للشروط. أدوار فقط — لا أسماء، لا PII.

إعلان الوظيفة أقوى إشارة شراء متاحة علناً: حين تدفع شركة لتوظيف دور، فهي تعترف
بفجوة عملية تحاول سدّها. نحوّل **الدور المعلَن** إلى **فرضية ألم** (`pain_hypothesis`)
ثم نطابقها بعرض من سلّم Dealix (`offer_match`). الإشارة فرضية لا حكم.

---

## 1. جدول الدور → الألم → العرض (المرجع المعتمد)

| الدور المعلَن (`role_posted`) | `mapped_pain` | `mapped_offer` | المنطق المختصر |
|------------------------------|---------------|----------------|----------------|
| Sales Operations | `weak_reporting` | `DLX-L3` | الحاجة لدور عمليات مبيعات تكشف ضعف القياس والتقارير |
| CRM Manager | `crm_data_disorder` | `DLX-L3` | توظيف مدير CRM يكشف فوضى بيانات تتراكم بلا نظام |
| Marketing Coordinator | `follow_up_chaos` | `DLX-L2` | تنسيق تسويق يدوي = leads تدخل بلا متابعة منظّمة |
| Customer Support | `support_overload` | `DLX-L3` | توظيف دعم مكثّف يكشف ضغط طلبات بلا توجيه ذكي |
| Growth Manager | `sales_team_inconsistency` | `DLX-L3` | دور نمو بلا playbook موحّد = أداء متذبذب |
| Operations Manager | `follow_up_chaos` | `DLX-L1` | عمليات عامة تكشف تسرّباً بين الاستفسار والإغلاق |

> الجدول **مرجعي وثابت**. أي دور خارجه يُربَط بأقرب فئة في `pain_category` المعتمدة،
> ويُسجَّل كـ `evidence_level: assumed` حتى تؤكّده إشارة ثانية.

---

## 2. كيف نقرأ الإعلان (مصادر عامة فقط)

نقرأ علناً: المسمّى، المسؤوليات، الأدوات المذكورة (HubSpot/Salesforce/Zoho)، حجم
الفريق المستهدف. **لا** نسجّل اسم مسؤول التوظيف ولا بريده ولا أي بيانات شخصية —
**الأدوار فقط**. لا نشتري قوائم، ولا نستخرج بيانات تخالف شروط المنصّة.

إشارات داخل الإعلان ترفع الثقة:
- ذكر CRM باسمه صريحاً → يقوّي `crm_data_disorder`.
- "متابعة العملاء" / "إدارة الـ pipeline" → يقوّي `follow_up_chaos`.
- "تقارير" / "dashboards" / "KPIs" → يقوّي `weak_reporting`.
- "حجم تذاكر مرتفع" / "أوقات استجابة" → يقوّي `support_overload`.

---

## 3. كيف نتصرّف (Signal → Action)

1. **تسجيل** الإشارة في `data/signals/job_signals.jsonl` بحقول:
   `signal_id` · `company` · `sector` · `role_posted` · `mapped_pain` ·
   `mapped_offer` · `source` · `observed_at` · `evidence_level`.
2. **التقاطع**: ابحث عن إشارة شركة موازية في `company_signals.jsonl`. تقاطع
   `active_hiring` + دور CRM يرفع `buying_signal` في تقييم العميل المحتمل.
3. **المطابقة**: مرّر `mapped_offer` إلى Prospect Research OS لتأكيد ملاءمة القطاع.
4. **المسودّة**: العرض الناتج يدخل خط المسودّات بفرضية ألم واضحة وزاوية تخصيص ≥ P2.
5. **الموافقة**: لا إرسال. المسودّة تنتظر بوّابات الجودة وطابور المؤسّس.

---

## 4. الثقة والإثبات

- `evidence_level: observed` — رأينا الإعلان منشوراً علناً (الحدّ الأدنى للعمل).
- `evidence_level: assumed` — استنتاج من سياق دون مشاهدة الإعلان مباشرة.
- `evidence_level: verified` — تأكيد الدور من مصدرين عامين مستقلّين.

كل ادّعاء كمّي لاحق في المسودّة يحمل `evidence_level` ولا يتجاوز أعلى مستوى صادق.
لا نرفع `assumed` إلى `verified` بلا مصدر ثانٍ.

---

## 5. أمثلة توضيحية (أسماء placeholder فقط)

> الأسماء التالية placeholder توضيحية، والأرقام **غير حقيقية** — «مثال توضيحي».

- **Nexus IT Solutions** (`local_saas`) ينشر *Sales Operations* →
  `weak_reporting` → `DLX-L3`. تقاطع مع `content_activity` يرفع الأولوية.
- **Horizon Realty Team** (`real_estate_teams`) ينشر *CRM Manager* →
  `crm_data_disorder` → `DLX-L3`. تقاطع مع `new_branch` يقوّي فرضية التشتّت.
- **Digital Rise Agency** (`marketing_agencies`) ينشر *Marketing Coordinator* →
  `follow_up_chaos` → `DLX-L2`.

---

## 6. الحدود غير القابلة للتفاوض

- مصادر عامة فقط · لا scraping مخالف · لا شراء قوائم.
- أدوار لا أشخاص · لا PII في أي سجل أو تقرير.
- الجدول أعلاه مرجع ثابت · كل عرض يُربَط بفرضية ألم صريحة.
- لا ادّعاءات ممنوعة (`نضمن` · `نضاعف الإيرادات` · `نتائج مضمونة` · `بدون مخاطرة` ·
  `10x`) · الأفعال المسموحة فقط: نساعد · نجهّز · نرتّب · نقيس · نكشف فرص التحسين ·
  نقترح · نجهّز مسودّات بموافقة.

---

*المرجع المركزي: `docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md`. النظام الأم:
`docs/signals/SIGNAL_DETECTION_OS_AR.md`. البيانات: `data/signals/job_signals.jsonl`.*
