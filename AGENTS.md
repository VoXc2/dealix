# AGENTS.md — Dealix Operating System (Acquisition → Delivery → Founder Control)

> دليل التشغيل الموحّد لوكلاء Dealix البشريين والآليين.
> هذا الملف هو **المصدر الوحيد للحقيقة** (single source of truth) لأسماء الأنظمة، حالات الـ pipeline، أدوار التواصل، مستويات الدليل، والقواعد الصارمة.
> أي وثيقة أو schema أو data أو report في هذا الريبو يجب أن تتوافق مع المصطلحات أدناه حرفيًا.

---

## 1. الطبقات الثلاث

```txt
1. Acquisition Engine   → يجلب الشركات ويجهّز لكل شركة Intelligence Pack + Email Draft + Call Brief + Mini Proposal
2. Delivery Engine      → إذا وافق العميل، يحوّل البيع إلى تسليم واضح وشبه آلي
3. Founder Control Engine → كل يوم: ماذا ترسل، من يتصل، ماذا يعرض، ماذا يُسلّم، وما العوائق
```

المسار الكامل من أول استهداف إلى التسليم:

```txt
Company Research → Company Intelligence Pack → Client Need Card → Recommended System
→ Personalized Email Draft → Call Brief → Call Follow-up Script → Mini Proposal
→ Founder Approval → Client Intake → Delivery Pipeline → First Sprint Output
→ Weekly Value Report → Acceptance → Renewal / Upsell
```

كل مرحلة لها: `Input` / `Output` / `Owner` / `Approval gate` / `Report` / `Next action`.

---

## 2. الأنظمة الخمسة (Canonical System IDs)

استخدم `system_id` حرفيًا في كل schema/data. لا تخترع معرّفات جديدة.

| system_id | الاسم (EN) | الاسم (AR) | يستهدف |
|---|---|---|---|
| `revenue_os` | Revenue Operating System | نظام تشغيل الإيرادات | شركات عندها فرص/leads لكن بلا next action واضح |
| `executive_command_os` | Executive Command OS | نظام القيادة التنفيذية | نشاط كثير لكن الإدارة لا ترى القرار اليومي |
| `followup_recovery_os` | Follow-up Recovery OS | نظام استرجاع المتابعات | استفسارات تضيع بعد أول تواصل (تدريب، عقار، عيادات، وكالات، استشارات) |
| `whatsapp_client_os` | WhatsApp Client OS | نظام عملاء واتساب | شركات تعتمد على واتساب في الاستفسارات/الحجوزات/الدعم |
| `proposal_proof_os` | Proposal & Proof OS | نظام العروض والإثبات | خدمات/استشارات/وكالات/B2B تحتاج عروضًا مقنعة بالدليل |

### Outreach Angle لكل نظام (الزاوية الأساسية للإيميل)

| system_id | Email angle (AR) |
|---|---|
| `revenue_os` | أين تضيع الفرص؟ من يحتاج متابعة؟ ما الخطوة التالية؟ |
| `executive_command_os` | التقارير كثيرة، لكن القرار اليومي غير واضح |
| `followup_recovery_os` | آخر متابعة لم تحدث قد تكون أغلى فرصة |
| `whatsapp_client_os` | واتساب ليس فقط محادثات؛ يحتاج flows وaction cards وhandoff آمن |
| `proposal_proof_os` | العرض المقنع يحتاج Proof وليس كلامًا أكثر |

---

## 3. قواعد استهداف جهة الاتصال (Contact Targeting)

`best_contact_role` يجب أن يكون ضمن الأدوار المسموحة لكل نظام (أول دور = الأفضلية):

| system_id | الأدوار المسموحة (best_contact_role / alternate_roles) |
|---|---|
| `revenue_os` | Head of Sales, Founder, GM, Marketing Manager |
| `executive_command_os` | Founder, CEO, GM, Operations Manager |
| `followup_recovery_os` | Sales Manager, Marketing Manager, Founder |
| `whatsapp_client_os` | Operations Manager, Customer Service Manager, Founder |
| `proposal_proof_os` | Founder, Sales Lead, BD Manager, Marketing Manager |

> فحص آلي: كل `recommended_system` في أي pack/contact_target يجب أن يكون له `best_contact_role` ضمن هذه القائمة.

---

## 4. حالات Delivery Pipeline (Canonical, بالترتيب)

```txt
interested
→ qualified
→ mini_proposal_ready
→ proposal_sent
→ payment_handoff
→ won
→ intake_required
→ delivery_started
→ first_output_ready
→ client_review
→ accepted
→ weekly_value_report
→ renewal_candidate
```

حالات نهائية إضافية لإدارة العلاقة: `lost`, `do_not_contact`.

### شروط الانتقال (Transition Gates)

| الانتقال إلى | الشرط |
|---|---|
| `qualified` | ألم واضح + نظام مناسب |
| `mini_proposal_ready` | system + deliverables + starter_price جاهزة |
| `proposal_sent` | **موافقة founder** |
| `won` | اتفاق أو دفع |
| `intake_required` | نحتاج required_inputs |
| `delivery_started` | **استلمنا required_inputs** (لا يبدأ العمل قبلها) |
| `first_output_ready` | خرج أول مخرج |
| `client_review` | أُرسل للمراجعة |
| `accepted` | العميل وافق على المخرج |
| `weekly_value_report` | صدر تقرير قيمة |
| `renewal_candidate` | يوجد دليل قيمة أو توسّع محتمل |

---

## 5. حالات CRM للشركة (company status)

```txt
researched → need_card_ready → draft_ready → approved_to_send → sent
→ follow_up_due → call_brief_ready → called → interested → mini_proposal_ready
→ proposal_sent → won → delivery_started → active → renewal_candidate
```

حالات نهائية: `lost`, `do_not_contact`.

كل إيميل مُرسل يجب أن يُنتج: `follow_up_due_date` + `call_brief` + `next_action` + `owner`.

---

## 6. مستويات الدليل (Evidence Levels)

| level | المعنى |
|---|---|
| `L0` | تخمين قطاعي |
| `L1` | موقع الشركة |
| `L2` | صفحة خدمة/وظيفة/خبر |
| `L3` | عدة مصادر عامة متوافقة |
| `L4` | بيانات مقدّمة من الشركة |

**قاعدة الصياغة:** أي معلومة عند `L0` أو `L1` تُصاغ كاحتمال (`غالبًا`، `قد يكون`، `في هذا النوع من الشركات`) ولا تُصاغ كحقيقة مؤكدة. الحقول التي تبدأ بـ `likely_` احتمالية بطبيعتها.

مصادر مسموحة فقط: website, LinkedIn public page, Google results, directories, job posts, news, public contact page, public social profiles.
مصادر ممنوعة: private data, scraping مخالف, purchased lists, leaked databases, emails غير موثقة.

---

## 7. مستويات المخاطر (risk_level)

`low` | `medium` | `high` — تُستخدم في packs، call briefs، mini proposals، approval queue.

---

## 8. جودة المسودات (Draft Quality Score)

| المكوّن | المدى |
|---|---|
| personalization | 0–25 |
| pain_clarity | 0–20 |
| system_fit | 0–20 |
| cta_clarity | 0–15 |
| risk_safety | 0–10 |
| tone_quality | 0–10 |
| **total** | **0–100** |

- لا يدخل **Top 100** إذا `total < 75`.
- لا يكون **send-ready** إذا: غاب `recommended_system`، أو غاب `client_need_card`، أو غاب `CTA`، أو فيه claim مضمون، أو fake `Re:/Fwd:`، أو معلومات غير مؤكدة مصاغة كحقيقة، أو غاب opt-out حيث يلزم، أو الشركة في suppression list.

---

## 9. القواعد الصارمة (Hard Rules — Red Lines)

```txt
- No external email send by default — كل إيميل يبقى draft حتى موافقة founder.
- No automated calling — Call Briefs لمتصل بشري فقط.
- No cold WhatsApp automation.
- No LinkedIn automation.
- No purchased lists.
- No fake Re:/Fwd:.
- No guaranteed revenue claims (لا "مضمون"/"guarantee"/"نضاعف أرباحك").
- Use only public company information or founder-provided data.
- Respect do-not-contact and suppression list.
- Every mini proposal requires founder approval before sending.
- Every delivery pipeline requires required_inputs before work starts (delivery_started).
- No secrets or PII in prompts/logs/reports (no API keys, no Saudi phone numbers 05XXXXXXXX, no national IDs).
- Evidence levels must distinguish public facts from assumptions; L0/L1 phrased as likely/probable.
```

ما هو **آلي بالكامل**: اختيار الشركات، التحليل العام، توقع الألم، اختيار النظام، كتابة need card/email/call brief/script/follow-up/mini proposal، تجهيز delivery pack وintake وweekly report templates، ترتيب Top 100.

ما يحتاج **موافقة**: إرسال الإيميل فعليًا، إرسال واتساب، إرسال Mini Proposal، إرسال رابط دفع، السعر النهائي خارج السعر الافتتاحي، أي التزام تعاقدي، أي طلب بيانات حساسة/مفاتيح API، نشر Case Study.

> ملاحظة إيصالية (deliverability): متطلبات Google لمراسلة Gmail تشمل إعداد SPF/DKIM (وDMARC للمرسلين الكبار) وone-click unsubscribe للرسائل التسويقية وإبقاء spam rate تحت 0.3%. لذلك التصميم ينتج **حتى 400 draft/day** لكن الإرسال يبقى خلف approval gate.

---

## 10. الأدوار (Who does what)

| الدور | المسؤولية |
|---|---|
| Founder | يوافق على الإرسال/الـ mini proposal/السعر النهائي، يقرر الأولويات، يقفل الصفقات |
| Outreach Operator | يراجع Top 100، يرسل المعتمد، يتابع الردود، يحدّث الحالة |
| Caller / Sales Follow-up | يستخدم Call Brief، يتصل، يسجّل الرد، يطلب diagnostic |
| Delivery Operator | يتابع required_inputs، يشغّل Delivery Pack، يجهّز first output، يرسل weekly report |
| Dealix AI Agents | يحلّل، يكتب، يرتّب، يقترح، يجهّز templates، يطلّع reports — **لا يرسل ولا يسعّر ولا ينفّذ** |

---

## 11. خريطة الريبو (هذا النظام)

```txt
docs/acquisition/    وثائق محرّك الاستحواذ (AR)
docs/delivery/       وثائق محرّك التسليم (AR)
schemas/             تعريفات JSON Schema لكل كيان
data/acquisition/    بيانات الاستحواذ (JSONL — عيّنات تركيبية synthetic)
data/delivery/       بيانات التسليم (JSONL — عيّنات تركيبية)
reports/acquisition/ تقارير الاستحواذ (مولّدة من data)
reports/outreach/    تقارير الإنتاج اليومي وTop 100
reports/delivery/    تقارير حالة التسليم والعوائق
reports/founder/     Daily Super Command + Weekly Board Review
scripts/             مولّدات التقارير + فاحص الجودة (Python)
company_os/          نظام التشغيل الأقدم (revenue/governance/delivery/war_room) — مرجع تاريخي
```

### السكربتات
```txt
scripts/acquisition_delivery_check.py   فاحص الجودة (schemas + data + 8 فحوصات صارمة)
scripts/generate_acquisition_reports.py مولّد تقارير الاستحواذ + outreach
scripts/generate_delivery_reports.py    مولّد تقارير التسليم
scripts/generate_founder_command.py     مولّد Daily Super Command + Weekly Board Review
```

تشغيل: `python3 scripts/acquisition_delivery_check.py` ثم مولّدات التقارير. أو عبر npm: `npm run os:check` و`npm run os:reports`.

---

## 12. ملاحظة على البيانات

كل ملفات `data/**/*.jsonl` في هذا الريبو **عيّنات تركيبية (synthetic samples)** لأغراض القوالب والاختبار — أسماء شركات وهمية بنمط سعودي، بلا أرقام جوال حقيقية ولا أي PII، وبلا مفاتيح أو أسرار. الاستبدال ببيانات حقيقية يتم فقط من مصادر عامة أو بيانات يقدّمها العميل، مع احترام suppression list.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Enforced: YES*
