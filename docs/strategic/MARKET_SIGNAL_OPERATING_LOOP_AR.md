# حلقة تشغيل إشارات السوق — من L4 إلى قرار

**الغرض:** بعد **Evidence Capital** و**L4**، لا نضيف طبقات حوكمة؛ نُشغّل **حلقة إشارات**: كل حركة خارجية تُنتج قرارًا واحدًا (متابعة، مراجعة رسالة، archetype ثانٍ، أثر مطلوب بسيط، أو إيقاف مؤقت للأصل).

**قاعدة السجل:** *This log is not a motivation tracker. It is an evidence register.* — **هذا السجل ليس سجل حماس؛ إنه سجل أدلة.** (انظر [`../../data/docs_asset_usage_log.json`](../../data/docs_asset_usage_log.json)).

**مرجع:** [ASSET_USAGE_GOVERNANCE_AR.md](ASSET_USAGE_GOVERNANCE_AR.md)، [ASSET_EVIDENCE_LEVELS_AR.md](ASSET_EVIDENCE_LEVELS_AR.md)، [OS_ASSET_OPERATING_MODEL_AR.md](OS_ASSET_OPERATING_MODEL_AR.md). **نسخ ولصق + آلة قرار + رودماب المراحل:** [FULL_MARKET_PROOF_RUN_AR.md](FULL_MARKET_PROOF_RUN_AR.md) · [FOUNDER_SIGNAL_ROADMAP_AR.md](FOUNDER_SIGNAL_ROADMAP_AR.md).

**اللوحة اليومية:** لتشغيل نفس الحلقة بجدول واحد دون تكرار النصوص الطويلة، استخدم قسم **[Founder Signal War Room](FULL_MARKET_PROOF_RUN_AR.md#founder-signal-war-room)** داخل RUN ثم ارجع إلى الأقسام §0–§11 عند الحاجة للتفاصيل.

---

## الأربع حلقات

| الحلقة | المعنى | مخرج |
|--------|--------|------|
| **Follow-up** | متابعة واحدة بعد ~48 ساعة؛ لا ملفات جديدة | `outcome` مثل `follow_up_sent` — يبقى **L4** |
| **Response Classification** | تصنيف الرد أو عدمه | قرار تشغيلي (انظر الجدول أدناه) |
| **Partner Archetype** | ثلاث محاولات مرتبة، لا عشرة دفعة واحدة | محاولة 1 → 2 → 3 بأثر مسجّل لكل محاولة |
| **Conversion / Learning** | من ردّ إلى اجتماع إلى intro إلى فاتورة | **L5** بعد اجتماع فعلي؛ **L6** intro/scope؛ **L7** إيراد موثّق |

---

## تصنيف النتائج (`outcome` — مرشدات)

استخدم قيمًا واضحة في `outcome` (راجع أيضًا `response_outcomes` في سجل الاستخدام):

`follow_up_sent` · `replied_interested` · `meeting_requested` · `meeting_booked` · `used_in_meeting` · `forwarded_internally` · `pilot_intro_requested` · `asks_for_pdf` · `asks_for_english` · `asks_for_case_study` · `asks_for_scope` · `asks_for_pricing` · `not_relevant` · `wrong_timing` · `no_response_after_follow_up` · `objection_no_case_study` …

### جدول قرار سريع

| النتيجة | Evidence (تقريبًا) | قرار |
|---------|-------------------|------|
| follow_up_sent | L4 | انتظر؛ لا ترفع إلى L5 |
| replied_interested | L4 | احرز اجتماعًا — ما زال L4 حتى ينعقد |
| meeting_booked | L4 | جهّز agenda — L5 **بعد** الاجتماع فقط |
| used_in_meeting | L5 | اسأل عن **intro واحد** أو شريحة عميل |
| forwarded_internally | قد يميل L6 | طابِع المستلم التالي |
| asks_for_pdf / english / case / scope / pricing | L4 + تعلم | **بناء بسيط** فقط عند إشارة سوق (PR صغير) |
| no_response_after_follow_up | L4 + learning | archetype ثانٍ؛ لا تعيد بناء المنتج |

---

## قاعدة الإشارة → البناء (Signal → Build)

| إشارة من السوق | البناء المسموح |
|----------------|----------------|
| asks_for_pdf | تصدير PDF للحزمة المعتمدة فقط |
| asks_for_english | One-pager إنجليزي فقط |
| asks_for_case_study | توضيح proof-stage (لا case مزيف) |
| asks_for_scope | قالب نطاق diagnostic |
| asks_for_pricing | صفحة عرض/تسعير قصيرة |
| 3× لا رد من نفس الـarchetype | إعادة صياغة **رسالة**، لا إعادة منتج |
| 3× لا رد من 3 archetypes | مراجعة **positioning** |

**ممنوع بدون إشارة:** dashboard، UI، ترجمة كاملة، إعادة scoring، أرشفة فعلية، نقل مجلدات، موجة منتج جديدة.

---

## حلقة الـPartner Archetype (3 محاولات)

1. **Big 4 / Assurance** — الثلاثية: Offer Matrix + Proof Demo + BU4.  
2. **Regulated technology processor** — زاوية تشغيل محكوم؛ BU4 غالبًا في الصدارة.  
3. **Saudi/GCC VC platform** — جاهزية المحفظة؛ Proof Demo + Offer Matrix.

كل محاولة: سجل **L4** لكل أصل أُرسل فعليًا؛ لا تُعرّف 10 أصول دفعة واحدة لنفس الحركة.

---

## اجتماع الشريك — Agenda ~30 دقيقة

1. ما يرفضه Dealix (no cold automation، claims بلا دليل، إلخ).  
2. المشكلة: تبنّي AI بلا طبقة تشغيل محكومة.  
3. Offer Matrix: ماذا نبيع والسلم.  
4. Proof Demo: أول إثبات → Proof Pack / Value Ledger.  
5. Trust Gate: ثقة كـ**gate** لا كـclaim.  
6. الطلب: **شريحة عميل واحدة** أو **pilot intro واحد**.

**سؤال الإغلاق:** من هي شريحة عميل واحدة عندكم تجرّب AI لكنها ليست آمنة لشراء أداة أتمتة عامة؟

---

## Mini Asset Council (7–14 يومًا بعد أول L4)

أسئلة: L4 صادق؟ المتابعة أُرسلت؟ رد؟ archetype ثانٍ؟ أصل يحتاج تعديل؟ طلب سوق يبرّر PR صغير؟

**مخرج واحد فقط:** `continue` | `follow_up` | `second archetype` | `revise message` | `build requested artifact` | `pause asset`.

---

## قراءة `asset_capital_allocation.json`

- **Activate:** أولوية — استخدم الأصول، لا تبنِ لها.  
- **Invest:** فقط بعد **L5/L6** أو طلب سوق صريح (PDF، EN، …).  
- **Maintain / archive_review:** كما في [MONTHLY_ASSET_COUNCIL_AR.md](MONTHLY_ASSET_COUNCIL_AR.md).

الأصول الثلاثة في **L4 + pending** → قرار تشغيلي: **Activate، ليس Invest**

---

## مقاييس CEO (30 يومًا)

لا تُقاس بعدد الملفات؛ قِس: **محاولات شريك**، **إرسالات خارجية**، **معدل رد**، **اجتماعات**، **intros**، **فواتير**، **اعتراضات متكررة**، **لا رد حسب الـarchetype**، **بناء جديد فقط بعد إشارة**.

---

## Full Market Proof Run — تشغيل في جلسة واحدة (قوالب)

**قبل النسخ:** لا تُدخل في `entries` أي حدث لم يحدث. التواريخ في الأمثلة = عيّن **تاريخ اليوم الفعلي** عند الإرسال. القاعدة: *no fiction register*.

### 0) قائمة تحقق سريعة

1. تأكيد صدق L4 (إرسال فعلي) — وإلا تصحيح إلى `prepared_not_sent` + L2 + `founder_confirmed: false`.  
2. إرسال **متابعة واحدة** (نص أدناه) إن حان وقتها.  
3. عند الرد: صنّف من الجدول الموسّع.  
4. عند الاجتماع: نفّذ المسار 30 دقيقة؛ **L5** فقط بعد انعقاد الاجتماع واستخدام الأصل.  
5. بعد كل حدث حقيقي:  
   `py -3 scripts/generate_holding_value_summary.py` ثم `py -3 scripts/validate_docs_governance.py` ثم حزمة pytest الوثائق.

### 1) جدول تصنيف الردود (مرجع تشغيلي)

| الرد | `outcome` | `outcome_quality` | Evidence | قرار |
|------|-----------|-------------------|:--------:|------|
| متابعة أُرسلت | `follow_up_sent` | pending | L4 | انتظر |
| رد مهتم | `replied_interested` | medium | L4 | احجز اجتماع |
| طلب اجتماع | `meeting_requested` | high | L4 | اقترح أوقاتًا |
| حُجز اجتماع | `meeting_booked` | high | L4 | جهّز agenda — **ليس L5 بعد** |
| اجتماع واستُخدم الأصل | `used_in_meeting` | medium / high | L5 | اطلب pilot intro |
| intro | `pilot_intro_requested` | high | L6 | جهّز نطاق diagnostic |
| طلب نطاق | `scope_requested` | high | L6 | نفس المسار عمليًا |
| PDF | `asks_for_pdf` | learning | L4 | PR صغير: PDF للحزمة المعتمدة فقط |
| English | `asks_for_english` | learning | L4 | PR صغير: one-pager فقط |
| case study | `asks_for_case_study` | learning | L4 | proof-stage positioning (لا case مزيف) |
| لا رد بعد المتابعة | `no_response_after_follow_up` | learning | L4 | archetype ثانٍ |
| غير مناسب | `not_relevant` | low / learning | L4 | غيّر الجمهور لا المنتج |

### 2) متابعة واحدة (بريد — انسخ بعد الإرسال الفعلي)

```text
Hi [Name],

Following up with one concrete angle:

This is not an AI automation resale motion.

The partner angle is a governed AI operations diagnostic for clients already experimenting with AI but lacking source clarity, approval boundaries, evidence trails, proof of value, and agent identity controls.

Would it be useful to compare this against one client segment you already see asking about AI governance or AI-driven revenue operations?

Best,
Sami
```

**سجل واحد فقط** للأصل الذي تناولته المتابعة (غالبًا `HOLDING_OFFER_MATRIX_AR.md`) — مثال حقول: `used_for: partner_follow_up`, `outcome: follow_up_sent`, `evidence_level_after_use: L4`.

### 3) رد مهتم — اقتراح اجتماع 30 دقيقة

```text
Thanks [Name] — glad this is relevant.

A short 30-minute discussion is enough. I'd like to keep it practical:

1. where your clients are already experimenting with AI,
2. where governance / source clarity / approval boundaries are weak,
3. whether a controlled diagnostic or Revenue Intelligence Sprint could be a safe first step.

Would either [Option 1] or [Option 2] work?

Best,
Sami
```

### 4) اعتراض case study — بدون اختراع إثبات

```text
You're right to ask for proof.

We are currently at the controlled proof stage rather than claiming mature case studies.

The first engagement is designed to produce:

* a Proof Pack,
* a Value Ledger entry,
* a governed decision trail,
* and a reusable capital asset,

without unsafe automation, unsupported claims, or external action without approval.

That is exactly why the first motion is a diagnostic or controlled Revenue Intelligence Sprint rather than a broad AI automation deployment.

Best,
Sami
```

### 5) محاولة 2 — معالج تقني خاضع للتنظيم (مثال إرسال)

```text
Hi [Name],

I'm building Dealix, a governed AI operations company starting in Saudi Arabia.

The angle may be relevant for regulated workflows where AI experimentation is happening, but source clarity, human approval, evidence trails, and proof of value are not yet operationalized.

We are not positioning this as generic AI automation. The first motion is a controlled diagnostic or Revenue Intelligence Sprint that produces a Proof Pack, Value Ledger, and governed decision trail.

Would it be useful to compare this against one regulated client segment you already see exploring AI?

Best,
Sami
```

(سجّل L4 لكل أصل **أُرسل فعليًا** فقط.)

### 6) مسار اجتماع 30 دقيقة (L5 prep)

| الدقائق | الموضوع |
|:-------:|---------|
| 0–5 | ما لا نفعله: لا scraping، لا واتساب بارد، لا ادّعاءات بلا دليل، لا إجراء خارجي بدون موافقة. |
| 5–10 | المشكلة: تبنّي AI أسرع من حوكمتها؛ الطبقة الناقصة تشغيلية. |
| 10–15 | العرض: Strategic Diagnostic → Governed Ops Retainer → Revenue Intelligence Sprint. |
| 15–20 | الإثبات: أول إشراك يولّد Proof Pack، Value Ledger، مسار قرار محكوم، أصل قابل لإعادة الاستخدام. |
| 20–25 | Trust gate: BU4 كـ**بوابة** لا كـclaim قبل الجاهزية. |
| 25–30 | السؤال: من شريحة عميل واحدة تجرّب AI لكنها غير آمنة لأداة أتمتة عامة؟ |

### 7) قوالب JSON (تلزم تاريخًا حقيقيًا + `founder_confirmed` صادق)

**L5 — بعد اجتماع فعلي واستخدام الأصل:**

```json
{
  "asset": "HOLDING_OFFER_MATRIX_AR.md",
  "used_for": "partner_meeting",
  "date": "YYYY-MM-DD",
  "audience_id": "PARTNER-001",
  "audience": "Big 4 / Assurance Partner",
  "channel": "video_call",
  "outcome": "used_in_meeting",
  "outcome_quality": "high",
  "evidence_level_after_use": "L5",
  "commercial_next_action": "ask for one pilot intro",
  "founder_confirmed": true
}
```

**L6 — intro أو طلب نطاق:**

```json
{
  "asset": "PROOF_DEMO_PACK_5_CLIENTS_AR.md",
  "used_for": "partner_meeting",
  "date": "YYYY-MM-DD",
  "audience_id": "PARTNER-001",
  "audience": "Big 4 / Assurance Partner",
  "channel": "video_call",
  "outcome": "scope_requested",
  "outcome_quality": "high",
  "evidence_level_after_use": "L6",
  "commercial_next_action": "prepare diagnostic scope for referred client",
  "founder_confirmed": true
}
```

**L7 — مرشّح إيراد (الدفع يؤكد لاحقًا داخليًا):**

```json
{
  "asset": "PROOF_DEMO_PACK_5_CLIENTS_AR.md",
  "used_for": "invoice_motion",
  "date": "YYYY-MM-DD",
  "audience": "Referred client",
  "audience_id": "CLIENT-REF-001",
  "channel": "email",
  "outcome": "invoice_sent",
  "outcome_quality": "revenue_candidate",
  "evidence_level_after_use": "L7",
  "commercial_next_action": "wait for payment and schedule kickoff",
  "founder_confirmed": true
}
```

**محاكاة داخلية فقط (ليس L4):**

```json
{
  "asset": "HOLDING_OFFER_MATRIX_AR.md",
  "used_for": "partner_outreach_template",
  "date": "YYYY-MM-DD",
  "audience_id": "PARTNER-001",
  "audience": "Big 4 / Assurance Partner",
  "channel": "email",
  "outcome": "prepared_not_sent",
  "outcome_quality": "none",
  "evidence_level_after_use": "L2",
  "commercial_next_action": "send to real partner before upgrading to L4",
  "founder_confirmed": false
}
```

### 8) قواعد رفع الدرجات في السجل (لا تغيّر أرقام Revenue في Registry من غير أثر)

- **L4:** تعرض خارجي فقط — لا رفع Revenue score.  
- **L5:** إن ساعد الأصل في وضوح الشراكة، يُراجع Partner usefulness في [MONTHLY_ASSET_COUNCIL_AR.md](MONTHLY_ASSET_COUNCIL_AR.md) لا آليًا.  
- **L6:** سحب سوقي (intro/scope) — يبرر مراجعة Partner/Revenue في المجلس.  
- **L7:** إيراد/ريتينر موثّق — أصل تجاري نواة.

### 9) تجميد البناء

لا PR جديد إلا: PDF، English one-pager، تبسيط matrix، إلخ — **بعد إشارة السوق** وفق قسم **«قاعدة الإشارة → البناء»** أعلاه في هذه الوثيقة.

### الخلاصة القصوى

> **L4 يثبت أن الأصل يخرج بأمان. لا تزوّر الزمن. سجّل بعد الحدث. ادفع L4 → L5 (اجتماع فعلي) → L6 (سحب) → L7 (مال). لا PR قبل إشارة سوق.**

**قاعدة ذهبية:** motion واحدة، ~3 أصول لكل حركة، متابعة واحدة، طلب اجتماع/شريحة واحدة — **No new build until signal.**
