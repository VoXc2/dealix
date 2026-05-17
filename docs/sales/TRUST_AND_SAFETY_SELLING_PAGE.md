<!-- Owner: Founder | Date: 2026-05-17 | Arabic primary -->
# صفحة الثقة والأمان — Trust & Safety Selling Page

> صفحة واحدة موجَّهة للمشتري. تجمع شظايا صفحة الثقة في أصل بيعي واحد.
> One buyer-facing page. Consolidates the trust-page fragments into one sales asset.

هذه الصفحة ليست وعداً تسويقياً. كل بند فيها مربوط باختبار يفشل CI لو تغيّر. الثقة هنا قابلة للتحقق.
This page is not a marketing promise. Every clause is wired to a test that fails CI if changed. Trust here is verifiable.

---

## ١. ما لا نفعله — What we do NOT do

**العربية:**
- لا نرسل رسائل WhatsApp باردة، ولا أتمتة WhatsApp.
- لا نقوم بسحب البيانات (scraping) من أي منصة.
- لا نصنع إثباتاً مزيّفاً — كل رقم في تقاريرنا مصدره بيانات العميل الفعلية.
- لا نَعِد بمبيعات مضمونة. النتائج التقديرية ليست نتائج مضمونة.
- لا نرسل أي شيء نيابة عن العميل بدون موافقته الصريحة على كل مسودة.

**English:**
- We do not send cold WhatsApp, and we do not run WhatsApp automation.
- We do not scrape data from any platform.
- We do not manufacture fake proof — every figure in our reports traces to the client's actual data.
- We do not promise guaranteed sales. Estimated outcomes are not guaranteed outcomes.
- We do not send anything on the client's behalf without explicit approval of each draft.

---

## ٢. كيف نتعامل مع بياناتك — How we handle your data

**العربية:**
- نعمل من مصادر بيانات **محدّدة بوضوح** يُصرّح بها العميل — لا أكثر.
- نطبّق تقليل البيانات (data minimization) ونقلّل فترة الاحتفاظ بالبيانات الشخصية.
- البيانات الشخصية (PII) تُحجب أو تُقيَّد في التقارير والمخرجات الخارجية حيث يلزم.

**English:**
- We work from **explicitly scoped** data sources the client authorizes — nothing more.
- We apply data minimization and reduce retention of personal data.
- PII is redacted or restricted in reports and outward-facing outputs where required.

---

## ٣. كيف نستخدم الذكاء الاصطناعي — How we use AI

**العربية:**
- يساعد الذكاء الاصطناعي داخل سير العمل مع **مراجعة بشرية** حيث تستدعي المخاطر ذلك.
- المخرجات الحسّاسة أو الخارجية تكون **مسودة أولاً**، والموافقة مطلوبة قبل أي إرسال.
- الوكلاء (agents) محدودون النطاق — لا وكيل بلا حدود ولا صلاحيات مفتوحة.

**English:**
- AI assists inside workflows with **human review** where risk warrants it.
- Sensitive or external outputs are **draft-first**; approval is required before any send.
- Agents are bounded in scope — no unbounded agents, no open-ended permissions.

---

## ٤. معيار الحوكمة — Governance standard

**العربية:**
- كل إجراء يُسجَّل: ماذا حصل، متى، لماذا، بمعرّف تدقيق (audit_id).
- لا أعطال صامتة — أي خلل يُبلَّغ ويُوثَّق، لا يُخفى.
- مرآة الصلاحيات: الذكاء الاصطناعي والأدوات لا ترى إلا ما يراه المستخدم المسؤول.
- الإجراءات الأعلى خطورة تحتاج موافقة أو تُحظر في النسخة الأولى.

**English:**
- Every action is logged: what happened, when, why, with an audit_id.
- No silent failures — any fault is surfaced and recorded, never hidden.
- Permission mirroring: AI and tools see only what the responsible user may see.
- Higher-risk actions require approval or are blocked in the MVP.

---

## ٥. زاوية نظام حماية البيانات السعودي (PDPL) — The PDPL angle

**العربية:**
معالجة البيانات الشخصية لدينا تقوم على أربعة مبادئ: **أساس نظامي** للمعالجة، **وضوح الغرض**، **التناسب** بين البيانات والغرض، و**انضباط الاحتفاظ**. هذا ليس "نصائح ذكاء اصطناعي" عامة — بل التزام تشغيلي موثَّق في اتفاقية معالجة البيانات.

**English:**
Our processing of personal data rests on four principles: a **lawful basis** for processing, **clarity of purpose**, **proportionality** of data to purpose, and **retention discipline**. This is not generic "AI tips" — it is an operational commitment documented in the data processing agreement.

---

## ٦. حقك في الحذف والتصدير — Your right to delete and export

**العربية:**
لك الحق في طلب نسخة من بياناتك أو تصحيحها أو حذفها أو نقلها. إجراءات التنفيذ والمواعيد النظامية موثّقة في [`PDPL_DATA_SUBJECT_REQUEST_SOP.md`](../PDPL_DATA_SUBJECT_REQUEST_SOP.md).

**English:**
You may request a copy of your data, its correction, deletion, or portability. The procedure and statutory windows are documented in [`PDPL_DATA_SUBJECT_REQUEST_SOP.md`](../PDPL_DATA_SUBJECT_REQUEST_SOP.md).

---

## ٧. مفروض باختبارات — Enforced by tests

**العربية:**
البنود أعلاه ليست سياسة على ورق. القواعد الإحدى عشرة غير القابلة للتفاوض مفروضة في CI — أي تغيير يكسر القاعدة يفشل البناء قبل الدمج. راجع [`NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md) للصياغة الرسمية و[`COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) للربط بالاختبارات.

القواعد: `no_live_send` · `no_live_charge` · `no_cold_whatsapp` · `no_scraping` · `no_fake_proof` · `no_unconsented_data` · `no_unverified_outcomes` · `no_hidden_pricing` · `no_silent_failures` · `no_unbounded_agents` · `no_unaudited_changes`.

**English:**
The clauses above are not policy on paper. The eleven non-negotiables are CI-gated — any change that breaks a rule fails the build before merge. See [`NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md) for the canonical wording and [`COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) for the test wiring.

---

## التالي — Next

- لمساعدة بطلك الداخلي على إقناع الإدارة: [`CHAMPION_ENABLEMENT_PACK.md`](CHAMPION_ENABLEMENT_PACK.md)
- للأسئلة الأمنية التفصيلية: [`dealix_security_faq.md`](../sales-kit/dealix_security_faq.md)

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
