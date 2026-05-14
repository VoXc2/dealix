# Dealix Pricing Reframe — 2026-Q2
## إعادة هيكلة التسعير — الربع الثاني ٢٠٢٦

_Audience: founder + commercial team (internal).  
الجمهور: المؤسس + فريق المبيعات (داخلي)._

> **One-line CEO summary:** The 2025 five-rung ladder optimized for funnel
> volume. The 2026 three-rung ladder optimizes for first-paid-invoice
> conviction. Saudi B2B services with the technical depth Dealix carries
> do not buy at 499 SAR — that price signals "I don't believe my own
> work yet". The new paid floor is 4,999 SAR / month.

> **سطر واحد للقرار:** سلّم ٢٠٢٥ بخمس درجات حسّن مدخل القمع. سلّم ٢٠٢٦
> بثلاث درجات يحسّن قناعة أول فاتورة مدفوعة. شركات خدمات B2B السعودية
> بهذا العمق التقني لا تشتري عند ٤٩٩ ر.س. الأرضية الجديدة ٤٬٩٩٩ ر.س / شهر.

---

## 1. The reframe in one table · إعادة الهيكلة في جدول واحد

| Stage · المرحلة | 2025 ladder (7 rungs) | 2026-Q2 ladder (3 rungs) | Action |
|---|---|---|---|
| Discovery · اكتشاف | Free Mini Diagnostic (0 SAR, 24h) | **Strategic Diagnostic** (0 SAR, 1 working day) | upgraded — anchored on PDPL/NDMO audit |
| First paid · أول دفعة | 499 SAR Sprint (one-time, 7d) | _archived_ | **kill** — below founder conviction |
| Expansion · توسّع | 1,500 SAR Data Pack (one-time, 14d) | _folded into flagship sprint_ | merge |
| Monthly · شهري | 2,999 SAR / mo Growth Ops (4-mo min) | **Governed Ops Retainer** (4,999 SAR / mo, 3-mo min) | **raise floor** by 2,000 SAR |
| Add-on · إضافة | 1,500 SAR / mo Support OS | _folded into retainer_ | merge |
| Executive · تنفيذي | 7,500 SAR / mo ECC (4-mo min) | _reshaped_ | replaced by flagship sprint outcome |
| Flagship · رئيسي | — | **Revenue Intelligence Sprint** (25,000 SAR / 30d fixed) | **new** — Capital Asset producer |
| Channel · قناة | Agency Partner OS (custom) | _moved out of customer ladder_ | partnership_os contract only |

---

## 2. Why these three and not five · لماذا ثلاث وليس خمس

### a. **Conviction floor (4,999 SAR / month)**
- Saudi B2B services mid-market (50–500 employees) commands engagement budgets
  of 30–80K SAR / quarter for operations consulting. Charging 499 SAR for a
  Sprint signals doubt in our own depth.
- Below 5,000 SAR / month, the buyer treats the engagement as a side-project.
  At 5,000+, it goes on the CFO's recurring-OpEx review — which is where
  renewals actually live.
- **أرضية القناعة:** أقل من ٥٬٠٠٠ ر.س / شهر تبقى صفقة جانبية في رأس المشتري.
  عند ٥٬٠٠٠+ تدخل قائمة مراجعة المالي الشهرية — مكان التجديدات الفعلية.

### b. **Outcome floor (25,000 SAR flagship)**
- A 30-day Sprint that merges three sources of truth, builds an audit-ready
  governance pack, and ships a Capital Asset is worth 25,000 SAR to any
  Saudi B2B services CFO with revenue forecast pain.
- The 25K Sprint is the proof-of-conviction sale. After one, the retainer
  becomes the obvious renewal. Without a flagship outcome, there is no
  case study to convert the next prospect.
- **أرضية المخرَج:** سبرنت ٣٠ يومًا يدمج ٣ مصادر حقيقة + يبني حزمة حوكمة
  قابلة للتدقيق + يسلّم أصلًا رأسماليًا — قيمته الحقيقية ٢٥٬٠٠٠ ر.س لأي
  CFO B2B سعودي عنده ألم في توقّع الإيرادات.

### c. **Funnel simplicity**
- 7 rungs forced 7 different intake forms, 7 checkout paths, 7 proposal
  templates, 7 doctrine variations. Founder time was the binding constraint.
- 3 rungs collapse this to 1 funnel form (the Diagnostic) + 2 paid paths
  (Retainer or Sprint). Time saved per qualified lead: ~45 minutes.
- **بساطة القمع:** ٧ درجات فرضت ٧ نماذج، ٧ مسارات دفع، ٧ قوالب اقتراح.
  ٣ درجات تختصرها إلى نموذج واحد + مسارَين مدفوعَين فقط.

---

## 3. Saudi B2B services as sole beachhead · القطاع المختار وحده

The 2025 homepage promised banking + energy + healthcare + government +
SaaS. The 2026 reframe drops all of them from the customer-facing ladder
for the next 90 days.

**Why B2B services first:**

| Reason · السبب | Detail · التفاصيل |
|---|---|
| Decision speed | B2B services founders/COOs sign in days, not quarters. Banks/government sign in quarters. |
| Budget shape | 50–500 employee companies routinely run 30–80K SAR / quarter operations consulting budgets. |
| PDPL / NDMO surface | These companies have exposure but lack in-house DPO + governance maturity → exactly the gap Dealix closes. |
| Network density | Saudi B2B services is a dense referral network — one happy CFO referral converts in <30 days. |
| Capital Asset replay | Revenue intelligence templates port across B2B-services companies almost 1:1 → margin compounds. |

Banking, energy, healthcare, government, and SaaS continue to be served
**only** as Custom AI engagements (≥ 50,000 SAR) negotiated directly with
the founder — they are NOT on the public ladder until 90 days post-pivot.

---

## 4. Migration · هجرة العملاء الحاليّين

There are no paying customers on legacy SKUs at the date of this reframe.
Internal tooling treats legacy IDs via the alias map in
`auto_client_acquisition/service_catalog/registry.py::_LEGACY_ID_ALIASES`:

| Legacy ID (2025) | Resolves to (2026) |
|---|---|
| `free_mini_diagnostic` | `strategic_diagnostic` |
| `revenue_proof_sprint_499` | `revenue_intelligence_sprint_25k` |
| `data_to_revenue_pack_1500` | `revenue_intelligence_sprint_25k` |
| `growth_ops_monthly_2999` | `governed_ops_retainer_4999` |
| `support_os_addon_1500` | `governed_ops_retainer_4999` |
| `executive_command_center_7500` | `governed_ops_retainer_4999` |

If a legacy proposal goes out by accident, qualification will auto-resolve
to the 2026 successor — no broken contract surface.

---

## 5. Objection handling · معالجة الاعتراضات

### Objection 1: "4,999 SAR / month is too high — we started at 499."
**EN:** "499 was a pilot price for the first five founding partners. The
production retainer reflects what a 3-source merge + monthly Value Report
+ governance pack actually costs to deliver. If 4,999/mo is a stretch,
we recommend completing the free Strategic Diagnostic first — three out
of five clients use the diagnostic alone to unlock budget internally."

**AR:** "كان ٤٩٩ سعراً تجريبياً لأول خمسة شركاء تأسيسيين. ريتينر الإنتاج
يعكس التكلفة الحقيقية لدمج ثلاثة مصادر + تقرير قيمة شهري + حزمة حوكمة.
لو ٤٬٩٩٩ صعب الآن، نوصي بإكمال التشخيص الاستراتيجي المجاني أولاً —
ثلاثة من كل خمسة عملاء يستخدمون التشخيص لوحده ليفتحوا الميزانية داخلياً."

### Objection 2: "25,000 SAR is more than we wanted to commit."
**EN:** "The flagship Sprint is for companies who already know they need
revenue forecast accuracy + audit-ready governance. If you're earlier than
that — exploring whether Dealix fits at all — start with the free
diagnostic. We won't quote the 25K Sprint until the diagnostic confirms
the fit."

**AR:** "السبرنت الرئيسي للشركات اللي تعرف إنها تحتاج دقة تنبؤ إيرادات
+ حوكمة قابلة للتدقيق. لو أنت أبكر من ذلك، ابدأ بالتشخيص المجاني.
ما نقدّم عرض السبرنت ٢٥ك إلا بعد ما التشخيص يأكّد المناسبة."

### Objection 3: "Why drop banking / energy from your offers?"
**EN:** "For the next 90 days. Saudi B2B services is our beachhead — once
we ship three flagship Sprints with documented Capital Assets, we'll
reopen Custom AI engagements for regulated sectors. Banking and energy
will pay more, but the cycle is longer; we need to compound 3 proof
points first."

**AR:** "خلال التسعين يوم القادمة فقط. خدمات B2B السعودية هي قاعدتنا.
بعد ما نسلّم ٣ سبرنتات رئيسية مع Capital Assets موثّقة، نفتح Custom AI
للقطاعات المنظّمة. البنوك والطاقة يدفعون أكثر، لكن الدورة أطول؛ نحتاج
نراكم ٣ نقاط إثبات أولاً."

### Objection 4: "How do we know 4,999/mo is the right floor — what's the data?"
**EN:** "It's a strategic choice, not a market study. The math: a 4,999/mo
retainer with a 3-month minimum is 15,000 SAR of committed revenue, which
exceeds the legacy 7-day 499 Sprint by 30× and creates the recurring base
we need to fund delivery infrastructure. If the floor is wrong, we'll
learn within two months and adjust — but we will not lower it below 4,999
this year."

**AR:** "قرار استراتيجي، ليس دراسة سوق. الحساب: ريتينر ٤٬٩٩٩ مع التزام
٣ أشهر = ١٥٬٠٠٠ ر.س إيراد ملتزَم به، أعلى من سبرنت ٤٩٩ القديم بـ٣٠ مرة،
ويوفّر القاعدة المتكررة اللازمة لتمويل البنية التحتية للتسليم. لو الأرضية
خطأ، نتعلّم خلال شهرين ونعدّل — لكن لن ننزل تحت ٤٬٩٩٩ هذه السنة."

---

## 6. Internal commitments · التزامات داخليّة

- **Founder calendar surgery:** 4h/day SELL, 2h/day DELIVER, 0h/day CODE.
  Claude does the code. Every founder hour spent coding is a non-event.
- **Doctrine guards remain non-negotiable:** the 11 non-negotiables apply
  to every offer; no exceptions for higher-priced engagements.
- **No live charge / no live send:** even at 25,000 SAR Sprint, payment
  capture is `intent_only` until founder flips the live cutover flag.
- **Every engagement produces ≥ 1 Capital Asset:** registered in
  `capital_os.add_asset` before the engagement closes. No exceptions.
- **Trust Pack + Audit Chain on every paid engagement:** PDF + control
  graph exported and shared with the customer.

---

## 7. KPIs to watch · مؤشرات للمتابعة

| KPI · المؤشر | 30 days · ٣٠ يوم | 60 days · ٦٠ يوم | 90 days · ٩٠ يوم |
|---|---|---|---|
| Diagnostics delivered · تشخيصات مسلّمة | 8 | 18 | 30 |
| Diagnostic → Retainer conversion · تحويل إلى ريتينر | ≥ 1 | ≥ 3 | ≥ 6 |
| Diagnostic → Flagship Sprint · تحويل إلى سبرنت رئيسي | 0 | ≥ 1 | ≥ 3 |
| Recurring SAR committed · إيراد ملتزَم متكرر | 15,000 | 60,000 | 150,000 |
| Capital Assets registered · أصول رأسماليّة مسجّلة | ≥ 1 | ≥ 4 | ≥ 8 |
| Friction-log high-severity events · أحداث احتكاك حرجة | ≤ 2 | ≤ 3 | ≤ 5 |

If the 90-day recurring SAR target slips below 100,000, we re-open this
doc and revisit the 4,999 floor downward — but never below 2,999.

---

## 8. Decision log · سجل القرارات

| Date · التاريخ | Decision · القرار | Owner · المسؤول |
|---|---|---|
| 2026-05-14 | Collapse 7-offer ladder → 3-offer ladder | Founder |
| 2026-05-14 | Raise paid floor 499 → 4,999 SAR/month | Founder |
| 2026-05-14 | Pick Saudi B2B services as sole beachhead for 90 days | Founder |
| 2026-05-14 | Archive Agency Partner OS from customer ladder; keep as channel contract via partnership_os | Founder |
| 2026-08-12 | Review gate — open if recurring SAR ≥ 100,000 or revisit floor | Founder |

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
