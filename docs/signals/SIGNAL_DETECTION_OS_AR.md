# Dealix — نظام كشف الإشارات (Signal Detection OS)

> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`
> **المصدر:** بيانات عامة فقط. لا scraping مخالف للشروط. لا PII (أدوار فقط).

نظام كشف الإشارات يحوّل ما تنشره الشركات علناً إلى **فرضية ألم** (`pain_hypothesis`)
قابلة للتقييم والمطابقة مع عرض من سلّم Dealix. الإشارة ليست دليلاً مؤكَّداً؛ هي
**مؤشّر شراء** نربطه بمستوى ثقة (`confidence`) ومستوى إثبات (`evidence_level`).

---

## 1. القاعدة الأولى: مصادر عامة فقط

نقرأ فقط ما نشرته الشركة أو طرف ثالث علناً ودون مخالفة شروط الاستخدام:

- `public_website` — الموقع الرسمي وصفحات الخدمات والنماذج.
- `public_careers_page` — صفحة التوظيف الرسمية.
- `public_job_board` — لوحات الوظائف العامة (يُعالَج في كتيّب إشارات الوظائف).
- `public_press` — بيانات صحفية وأخبار منشورة.
- `public_social` — منشورات عامة على حسابات الشركة.

**ممنوع:** أي scraping يخالف شروط المنصّة، شراء قوائم، أو استخراج بيانات شخصية.
نسجّل **الأدوار** (Head of Sales) لا **الأشخاص**. لا بريد شخصي، لا جوّال، لا اسم فرد.

---

## 2. أنواع الإشارات العشرة (`signal_type`)

| # | `signal_type` | ماذا يعني | المصدر النموذجي |
|---|---------------|-----------|-----------------|
| 1 | `job_posting` | إعلان وظيفة يكشف فجوة عملية | `public_job_board` |
| 2 | `new_branch` | فرع/موقع جديد = توسّع وتشتّت متابعة | `public_press` |
| 3 | `new_service_launch` | خدمة جديدة = حاجة لتجهيز عروض أسرع | `public_website` |
| 4 | `marketing_campaign` | حملة تسويق = تدفّق leads بلا نظام متابعة | `public_social` |
| 5 | `active_hiring` | توظيف مكثّف = نمو فريق بلا اتّساق | `public_careers_page` |
| 6 | `multi_forms` | الموقع فيه نماذج/خدمات متعدّدة = تسرّب leads | `public_website` |
| 7 | `crm_sales_support_role_visible` | دور CRM/مبيعات/دعم ظاهر = فوضى بيانات | `public_careers_page` |
| 8 | `recent_press` | تغطية صحفية حديثة = لحظة انتباه وتوسّع | `public_press` |
| 9 | `content_activity` | نشاط محتوى مكثّف = توليد طلب بلا قمع | `public_social` |
| 10 | `partner_ecosystem` | شراكات/قنوات معلنة = تعقيد مسار البيع | `public_website` |

---

## 3. خريطة الإشارة → الألم (`mapped_pain`)

كل إشارة تُترجَم إلى **فرضية ألم** من قائمة `pain_category` المعتمدة:

| `signal_type` | `mapped_pain` الافتراضي | المنطق |
|---------------|-------------------------|--------|
| `job_posting` | حسب الدور (انظر `JOB_SIGNAL_PLAYBOOK_AR.md`) | الدور يكشف الفجوة |
| `new_branch` | `follow_up_chaos` | فرع جديد يضاعف المتابعة اليدوية |
| `new_service_launch` | `proposal_delay` | خدمة جديدة تحتاج تجهيز عروض منظّم |
| `marketing_campaign` | `lead_leakage` | حملة تجلب leads أسرع من قدرة المتابعة |
| `active_hiring` | `sales_team_inconsistency` | فريق ينمو بلا playbook موحّد |
| `multi_forms` | `lead_leakage` | نماذج متفرّقة بلا قمع موحّد |
| `crm_sales_support_role_visible` | `crm_data_disorder` | الحاجة للدور تكشف فوضى بيانات |
| `recent_press` | `weak_reporting` | لحظة توسّع تكشف ضعف القياس |
| `content_activity` | `no_proof_case_study_system` | محتوى بلا نظام إثبات يحوّل |
| `partner_ecosystem` | `sales_team_inconsistency` | قنوات متعدّدة تشتّت رسالة البيع |

> الخريطة **افتراضية**؛ تُرفَع أو تُخفَّض حسب القطاع والإشارات المتقاطعة.

---

## 4. الثقة والإثبات

كل إشارة تحمل حقلين منفصلين:

- **`confidence`** (0.0–1.0): قوة الرابط بين الإشارة والألم. إشارة وظيفة مباشرة
  (`crm_sales_support_role_visible`) ثقتها أعلى من إشارة سياقية (`recent_press`).
- **`evidence_level`**: `none` · `assumed` · `observed` · `verified`.
  - `observed`: رأينا الإشارة منشورة علناً (الحدّ الأدنى للعمل).
  - `assumed`: استنتاج منطقي من سياق عام دون مشاهدة مباشرة للإشارة.
  - `verified`: تأكيد من أكثر من مصدر عام مستقل.

**قاعدة:** كل ادّعاء كمّي لاحق في المسودّة يجب أن يحمل `evidence_level`، ولا يتجاوز
أعلى مستوى صادق. لا نرفع `assumed` إلى `verified` بلا مصدر ثانٍ.

---

## 5. إشارات متقاطعة = أولوية أعلى

اجتماع إشارتين على نفس الشركة (مثال: `active_hiring` + `crm_sales_support_role_visible`)
يرفع الأولوية ويقوّي فرضية الألم. هذا التقاطع يغذّي `buying_signal` في تقييم العميل
المحتمل (انظر `docs/outreach/PROSPECT_RESEARCH_OS_AR.md`).

---

## 6. حقول سجل الإشارة

| الحقل | المثال |
|-------|--------|
| `signal_id` | `SIG-C-004` (شركة) · `SIG-J-001` (وظيفة) |
| `company` | `Nexus IT Solutions` *(اسم placeholder توضيحي)* |
| `sector` | `local_saas` |
| `signal_type` | من القائمة العشرة |
| `source` | مصدر عام فقط |
| `observed_at` | تاريخ المشاهدة |
| `evidence_level` | `observed` غالباً |
| `mapped_pain` | فرضية الألم |
| `confidence` | 0.0–1.0 |

البيانات الحيّة: `data/signals/company_signals.jsonl` · `data/signals/job_signals.jsonl`.

---

## 7. الحدود غير القابلة للتفاوض

- مصادر عامة فقط · لا scraping مخالف · لا شراء قوائم.
- أدوار لا أشخاص · لا PII في أي سجل أو تقرير.
- الإشارة فرضية لا حكم · كل ادّعاء كمّي يحمل `evidence_level`.
- أسماء الأمثلة placeholder توضيحية فقط، مع وسم «مثال توضيحي» عند الاقتضاء.

---

*المرجع المركزي: `docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md`. التقرير اليومي:
`reports/signals/SIGNAL_REPORT.md`.*
