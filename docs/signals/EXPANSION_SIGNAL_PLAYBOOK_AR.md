# Dealix — كتيّب إشارات التوسّع (Expansion Signal Playbook)

> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`
> **المصدر:** بيانات عامة فقط (`public_press` · `public_website` · `public_careers_page`).
> لا scraping مخالف. أدوار فقط — لا PII.

التوسّع لحظة ضغط على العملية: فرع جديد، خدمة جديدة، أو توظيف مكثّف كلّها تكشف أن
الطلب ينمو أسرع من قدرة المتابعة والقياس. نحوّل إشارة التوسّع إلى **فرضية ألم**
نطابقها بعرض. الإشارة فرضية لا حكم.

---

## 1. إشارات التوسّع → الألم

| `signal_type` | ما يعنيه التوسّع | `mapped_pain` الافتراضي | العرض المرشّح |
|---------------|------------------|-------------------------|---------------|
| `new_branch` | فرع/موقع جديد = متابعة موزّعة على مواقع | `follow_up_chaos` | `DLX-L2` ثم `DLX-L4` |
| `new_service_launch` | خدمة جديدة = حاجة لتجهيز عروض أسرع | `proposal_delay` | `DLX-L2` |
| `active_hiring` | توظيف مكثّف = فريق ينمو بلا playbook | `sales_team_inconsistency` | `DLX-L3` |

> الخريطة افتراضية وتُرفَع/تُخفَّض حسب القطاع. التوسّع يرفع `confidence` لأنه قرار
> تجاري معلَن لا مجرّد نشاط.

---

## 2. منطق كل إشارة

**`new_branch`:** افتتاح فرع جديد يضاعف نقاط الاستقبال ويوزّع المتابعة على فرق
ومواقع. بلا نظام موحّد، تتسرّب الفرص بين المواقع → `follow_up_chaos`. الفروع
المتعدّدة ترشّح لاحقاً `DLX-L4` (Full Revenue OS).

**`new_service_launch`:** إطلاق خدمة جديدة يولّد استفسارات بمسار جديد بلا قوالب
عروض جاهزة، فيتأخّر تجهيز العروض → `proposal_delay`. زاوية `DLX-L2`.

**`active_hiring`:** توظيف مكثّف (عدّة أدوار مبيعات/تشغيل دفعة واحدة) يعني فريقاً
ينمو أسرع من الـ playbook، فيتفاوت الأداء بين الأفراد → `sales_team_inconsistency`.
زاوية `DLX-L3` (AI Revenue Ops Starter).

---

## 3. كيف نتصرّف

1. **تسجيل** الإشارة في `data/signals/company_signals.jsonl` بمصدرها العام.
2. **التقاطع**: `active_hiring` + `crm_sales_support_role_visible` تقاطع قوي يرفع
   الأولوية و`buying_signal`. `new_branch` + `new_service_launch` يرشّح `DLX-L4`.
3. **المطابقة**: العرض يمرّ إلى Prospect Research OS لتأكيد ملاءمة القطاع والدفع.
4. **المسودّة** بزاوية تخصيص ≥ P2 تشير إلى التوسّع المعلَن (الفرع/الخدمة/التوظيف).
5. لا إرسال — المسودّة تنتظر البوّابات وطابور المؤسّس.

---

## 4. الثقة والإثبات

- `evidence_level: observed` — بيان صحفي أو صفحة رسمية تعلن التوسّع.
- `evidence_level: assumed` — استنتاج من إشارات جانبية دون إعلان صريح.
- `evidence_level: verified` — تأكيد من مصدرين عامين مستقلّين.

التوسّع المعلَن غالباً `observed` لأنه قرار منشور. كل ادّعاء كمّي في المسودّة يحمل
`evidence_level` ولا يتجاوز أعلى مستوى صادق.

---

## 5. أمثلة توضيحية (أسماء placeholder فقط)

> الأسماء placeholder توضيحية والأرقام **غير حقيقية** — «مثال توضيحي».

- **Horizon Realty Team** (`real_estate_teams`): بيان عن فرع جديد →
  `new_branch` → `follow_up_chaos` → `DLX-L2`.
- **TrainMe KSA** (`training_companies`): إطلاق مسار تدريبي جديد →
  `new_service_launch` → `proposal_delay` → `DLX-L2`.
- **Digital Rise Agency** (`marketing_agencies`): توظيف مكثّف لعدّة أدوار →
  `active_hiring` → `sales_team_inconsistency` → `DLX-L3`.

---

## 6. الحدود غير القابلة للتفاوض

- مصادر عامة فقط · لا scraping مخالف · لا شراء قوائم.
- أدوار لا أشخاص · لا PII في أي سجل أو تقرير.
- الإشارة فرضية لا حكم · كل ادّعاء كمّي يحمل `evidence_level`.
- لا ادّعاءات ممنوعة · الأفعال المسموحة فقط: نساعد · نجهّز · نرتّب · نقيس · نكشف
  فرص التحسين · نقترح · نجهّز مسودّات بموافقة.

---

*المرجع المركزي: `docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md`. النظام الأم:
`docs/signals/SIGNAL_DETECTION_OS_AR.md`. البيانات: `data/signals/company_signals.jsonl`.*
