# Arabic Tone Library

> Pre-approved Arabic tone modes. Every customer-facing AR output must
> declare which mode it is in and pass the corresponding QA check.

## Mode 1 — Executive Formal (فصحى تنفيذية)

**Use for**: CEO reports, board-level summaries, governance documents, procurement responses.

**Style cues**:
- Full sentences, no abbreviations.
- Verb-first or noun-clauses; no informal connectors.
- Numbers spelled or in digits, consistent within the doc.
- Single-paragraph paragraphs (no bullet-heavy formats unless data).

**Openings (examples)**:
- "تتضمن هذه الوثيقة المخرجات والنتائج المرتبطة بـ ..."
- "بناءً على المراجعة المنفذة خلال ..."
- "تشير المؤشرات الواردة في هذا التقرير إلى ..."

**Closings**:
- "نوصي بالخطوات التالية وفق الأولوية الموضحة أعلاه."
- "نحن جاهزون لمناقشة أي توضيح أو خطوة لاحقة."

**Forbidden**:
- لهجة عامية.
- اختصارات (مثل: "وكذا").
- "احنا" / "بنسوي" / "خلصنا".

---

## Mode 2 — Sales Professional (احترافي للمبيعات)

**Use for**: outreach drafts, proposals, follow-ups, sales decks.

**Style cues**:
- Direct, value-first, brief.
- One pain → one benefit → one CTA per message.
- Polite but confident; no apologetic phrasing.
- Bilingual greeting allowed ("السلام عليكم،") but body stays focused.

**Openings**:
- "السلام عليكم {{اسم}}،"
- "تواصلت معكم لأن ..."
- "لاحظت أن {{شركة}} تعمل في ..."

**Closings**:
- "هل لديك ربع ساعة هذا الأسبوع لمناقشة الأمر؟"
- "أرسل لي نعم لمتابعة التفاصيل."
- "إذا التوقيت غير مناسب الآن، أتفهم وسأتوقف هنا."

**Forbidden**:
- "نضمن لك ..." / "100% ..." / "حصري" — any guaranteed-outcome claim.
- مبالغة في الإطراء.
- علامات تعجب متعددة.
- إلحاح زائف (fake urgency).

---

## Mode 3 — Support Friendly (ودي خدمة عملاء)

**Use for**: customer support replies, FAQ entries, help center content.

**Style cues**:
- Warm but professional.
- Short paragraphs.
- Always confirm + clarify before answering.
- End with a question or clear next step.

**Openings**:
- "أهلاً، شكرًا لتواصلك معنا."
- "نعتذر عن الانتظار، خلّيني أوضّح الموقف."

**Closings**:
- "هل هناك شيء آخر أقدر أساعدك فيه؟"
- "أبشر، سنتواصل معك خلال ..."

**Forbidden**:
- لغة بيع (هذه ليست محادثة بيع).
- مبالغة في الاعتذار.
- وعود لا نقدر نلتزم بها.

---

## Mode 4 — Operations Direct (تشغيلي مباشر)

**Use for**: runbooks, SOPs, internal notes, system messages.

**Style cues**:
- Short, declarative, unambiguous.
- Numbered steps preferred.
- Imperative verbs ("نفّذ", "افحص", "احفظ").
- No marketing language.

**Openings**:
- "الخطوات:" / "المتطلبات:" / "النتيجة المتوقعة:"

**Forbidden**:
- جمل طويلة معقدة.
- مصطلحات ترجمة حرفية ("قم بتنفيذ عملية ...").
- صياغة بصيغة المجهول عندما يكون الفاعل مهمًا.

---

## Cross-cutting forbidden list (all modes)

- "نضمن", "نعد بـ", "بالتأكيد ستحقق ...", "أفضل", "الأقوى", "الوحيد", "حصري", "100%", "بدون مخاطر", "ربح مضمون".
- علامات تعجب متعددة (!!!).
- اختصارات عامية في سياق تنفيذي.
- ترجمة حرفية لمصطلحات إنجليزية لها مقابل عربي تجاري شائع (مثل: "اتصل بنا" ≠ "تواصل معنا" حسب السياق).
- استخدام "نحن" بشكل مفرط في الجمل القصيرة.
- "كما تعلم" / "بكل تأكيد" — حشو بلا قيمة.

Auto-checked by `dealix/trust/forbidden_claims.py`.

## Cross-links
- `docs/localization/SAUDI_MENA_LOCALIZATION_SYSTEM.md`
- `docs/quality/ARABIC_QUALITY_GUIDE.md`
- `docs/sales/sales_script.md` — uses Mode 2
- `docs/sales/offer_pages/` — uses Mode 2
- `dealix/reporting/executive_report.py` — uses Mode 1
