# Account Pack — تكامل ذكاء الاحتياج

كل Account Pack في Dealix يضيف **كتلة ذكاء الاحتياج** و**Need Fit Score**، فيتحول
من بطاقة شركة إلى توصية تنفيذية: ما الاحتياج؟ أي نظام؟ أي تخصيص؟ من نكلّم؟ ماذا
نرسل؟ ماذا نسلّم؟

المخطط: `schemas/account_pack_need_intelligence.schema.json`
مثال مُتحقَّق منه: `data/business_need_intelligence/account_pack_example.yaml`

---

## 1. الحقول الجديدة

```txt
detected_business_need          # أحد الاحتياجات الـ 15
need_confidence                 # ثقة تقديرية بين 0 و 1
recommended_core_system         # أحد الأنظمة العامة الخمسة
recommended_specialized_system  # النظام المتخصص (اسم)
expansion_system                # نظام عام للتوسّع لاحقًا
sector_specific_sprint          # معرّف سبرنت من المكتبة
specialized_delivery_pack[]     # حزمة التسليم
buyer_role_by_need[]            # أدوار وظيفية عامة (لا أسماء)
email_angle_by_need             # زاوية الإيميل
call_angle_by_need              # زاوية الاتصال
upsell_path_by_need[]           # مسار الترقية
need_fit_score                  # 0..100 (انظر أدناه)
```

---

## 2. Need Fit Score (من 100)

| المعيار | الوزن | ما يقيسه |
|---------|------:|----------|
| `sector_need_match` | 25 | مدى مطابقة الاحتياج المكتشف لاحتياجات القطاع |
| `signal_strength` | 20 | قوة الإشارات العلنية المرجِّحة |
| `delivery_readiness` | 20 | جاهزية حزمة التسليم والمدخلات |
| `buyer_clarity` | 15 | وضوح الدور المشتري |
| `first_sprint_clarity` | 10 | وضوح أول سبرنت ومعايير قبوله |
| `upsell_path` | 10 | وضوح مسار التوسّع |
| **total** | **100** | المجموع (يساوي حاصل الجمع) |

يُدمج في ترتيب الأولوية:

```txt
Top 100 = Account Score + Need Fit Score + Cash Priority Score
```

---

## 3. مثال (مجهّل الهوية)

```yaml
company: "Example Training Co (sample)"
sector: training_companies
detected_business_need: follow_up
need_confidence: 0.72
recommended_core_system: followup_recovery_os
recommended_specialized_system: "Admissions / Enrollment OS"
expansion_system: executive_command_os
sector_specific_sprint: enrollment_recovery_sprint
specialized_delivery_pack:
  - "Enrollment Inquiry Queue"
  - "Student Status Model"
  - "Course Inquiry Message Set"
  - "Weekly Registration Recovery Report"
buyer_role_by_need: ["Founder", "Marketing Manager", "Training Manager"]
email_angle_by_need: "آخر متابعة لم تحدث قد تكون سبب ضياع تسجيل جاهز."
call_angle_by_need: "نرتب رحلة الاستفسار حتى التسجيل ونحدد أين تتوقف المتابعة."
upsell_path_by_need: ["executive_command_os", "revenue_os"]
need_fit_score:
  sector_need_match: 25
  signal_strength: 16
  delivery_readiness: 18
  buyer_clarity: 13
  first_sprint_clarity: 10
  upsell_path: 9
  total: 91
```

---

## 4. قواعد التعبئة

- `need_confidence` تقديرية ومبنية على الأدلة، تبقى بين 0 و 1، ولا تُقدَّم كيقين.
- `buyer_role_by_need` أدوار عامة فقط — **لا أسماء ولا جهات اتصال مخترعة**.
- `detected_business_need` و`recommended_core_system` يجب أن يكونا من القوائم
  المعتمدة (يتحقق منهما `scripts/business_need_validate.py`).
- `total` في Need Fit Score يجب أن يساوي مجموع المعايير.
- لا وعود نتائج في أي زاوية إيميل/اتصال.
