# Company Intelligence Pack — دليل النظام

**الهدف:** لكل شركة مستهدفة يُولّد ملف ذكاء واحد يجيب عن: مَن نكلّم؟ وش ألمه؟ وش نرسل؟ وش نسأل؟ وش نعرض؟ وش الخطوة التالية؟ — بحيث يقدر أي شخص في الفريق يفتح الملف ويتحرك بلا أن يفهم Dealix من الصفر.

- **المصدر (Schema):** [`schemas/company_intelligence_pack.schema.json`](../../schemas/company_intelligence_pack.schema.json)
- **البيانات:** [`data/acquisition/company_intelligence_packs.jsonl`](../../data/acquisition/company_intelligence_packs.jsonl)
- **المولّد:** [`scripts/generate_acquisition_packs.py`](../../scripts/generate_acquisition_packs.py)
- **التقرير اليومي:** [`reports/acquisition/DAILY_COMPANY_INTELLIGENCE_PACKS.md`](../../reports/acquisition/DAILY_COMPANY_INTELLIGENCE_PACKS.md)

---

## 1. كيف يُولّد؟

```txt
prospects.csv  ──►  pick_system(pain)  ──►  resolve_contact_role(system, sector)  ──►  Company Intelligence Pack
                     (pain → نظام)          (contact_targets.jsonl)
```

النظام المقترح يُختار من **ألم الشركة** عبر خريطة ثابتة (`PAIN_TO_SYSTEM`) مع fallback بالكلمات المفتاحية، ثم يُحَل **أول شخص نتواصل معه** من جدول الاستهداف حسب النظام والقطاع.

تشغيل:

```bash
python3 scripts/generate_acquisition_packs.py
python3 scripts/generate_acquisition_reports.py
```

---

## 2. الحقول

| الحقل | المعنى |
|------|--------|
| `pack_id` | معرّف الملف (CIP-001 …) |
| `company`, `website`, `country`, `city`, `sector` | تعريف الشركة |
| `public_contact_channels` | قنوات تواصل عامة فقط (website / email / whatsapp) |
| `likely_decision_maker` | صاحب القرار المرجّح |
| `best_contact_role` | أفضل **دور** نتواصل معه أولاً (ليس اسم شخص) |
| `signal` | الإشارة التي رجّحت النظام |
| `likely_pain` | الألم المرجّح (فرضية) |
| `recommended_system` | واحد من الأنظمة الخمسة |
| `why_this_system` | لماذا هذا النظام تحديدًا |
| `first_mission` | أول مهمة قيمة في السبرنت |
| `proof_angle` | زاوية الدليل المتوقعة |
| `email_subject`, `email_draft` | مسودة البريد — **تبقى مسودة حتى موافقة المؤسس** |
| `call_opener`, `call_questions`, `expected_objections` | مادة المكالمة |
| `mini_proposal_angle` | زاوية العرض المصغّر |
| `next_action` | الخطوة التالية |
| `risk_level` | low / medium / high |
| `evidence_level` | public_only / founder_provided / inferred |
| `approval_required` | **true دائمًا** — لا إرسال بلا موافقة |
| `do_not_contact` | احترام قائمة عدم التواصل |

---

## 3. مثال (مولّد فعليًا)

```txt
Company: TrainMe KSA
Sector: Training Company
Signal: واتساب قناة رئيسية لكن الطلبات غير مصنفة وبلا تصعيد واضح
Likely pain: ضياع جزء من استفسارات واتساب قبل أن تتحول إلى عملاء
Recommended system: WhatsApp Client OS
Best contact role: Operations Manager
Email subject: TrainMe KSA: سبرنت 7 أيام لترتيب محادثات واتساب وبناء سياسة تصعيد.
Next action: إرسال المسودة لقائمة موافقة المؤسس قبل أي تواصل خارجي.
Approval required: true
```

---

## 4. قواعد صارمة

- معلومات **عامة** أو مقدّمة من المؤسس فقط — لا قوائم مشتراة، لا كشط بيانات خاصة.
- **أدوار** فقط في `best_contact_role` — لا أسماء أشخاص (حماية للخصوصية و PDPL).
- البريد يبقى **مسودة** حتى موافقة المؤسس (`approval_required = true`).
- لا عناوين Re:/Fwd: مزيّفة، ولا وعود عائد مضمونة.
- يُفحَص كل هذا آليًا في [`scripts/acquisition_delivery_check.py`](../../scripts/acquisition_delivery_check.py) (الفحوص C01, C06, C08, C09).
