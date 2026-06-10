# Privacy Policy v2 — Dealix

**Version:** 2.0 (founder-self-execution per `LEGAL_FOUNDER_SELF_EXECUTION.md`)
**Effective:** 2026-05-07
**Replaces:** `landing/privacy.html` v1 ("under review")
**Companion:** `landing/privacy.html` (mirror) · `docs/DPA_DEALIX_FULL.md` · `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`

> **Founder note:** Aligned with Saudi PDPL principles + GDPR-derived best practice. NOT lawyer-attested. Lawyer review scheduled within 90 days of customer #1.

---

# سياسة الخصوصيّة — Dealix

**آخر تحديث:** ٢٠٢٦-٠٥-٠٧
**الإصدار:** ٢.٠

---

## ١. من نحن · Who we are

Dealix هي منصّة Saudi-PDPL-compliant AI Operating Team للشركات الصغيرة والمتوسّطة في المملكة العربيّة السعوديّة.

- **اسم الكيان القانوني:** [يُحدَّث عند تسجيل CR]
- **العنوان الرسمي:** [Sami's registered address — TBD]
- **مسؤول حماية البيانات (Acting DPO):** Sami [last name]
- **بريد التواصل لشؤون الخصوصيّة:** privacy@dealix.me
- **بريد الدعم العام:** support@dealix.me

---

## ٢. نطاق هذه السياسة · Scope

هذه السياسة تنطبق على:

1. **زوّار dealix.me** — البيانات التي نجمعها عند زيارة موقعنا
2. **العملاء المحتملون (prospects)** — الذين يتواصلون معنا عبر diagnostic / Calendly / WhatsApp warm-intro
3. **العملاء الدافعون** — الشركات التي وقّعت Sprint أو Partner contract
4. **الأفراد المستهدفون من خدمات عملائنا** — حيث Dealix يتصرّف كـ Processor (المتحكّم = العميل الدافع)

**لا تنطبق على:** المواقع الخارجيّة المرتبطة من dealix.me (لكلّ موقع سياسته).

---

## ٣. ما البيانات التي نجمعها · What data we collect

### ٣.١ بيانات تُقدَّم منك مباشرة

عند تعبئة diagnostic أو طلب Sprint:

- **بيانات تعريف:** اسم، عنوان وظيفي، شركة، قطاع، مدينة
- **بيانات اتّصال:** بريد إلكتروني، جوّال (E.164)، LinkedIn URL (إن قدّمته)
- **بيانات الشركة:** حجم الفريق، الـ ICP، problem statement
- **محتوى الرسائل:** نسخ من المحادثات (مع redaction للأسرار)
- **مدفوعات:** مرجع التحويل، تاريخ، مبلغ — **لا نخزّن أرقام بطاقات** (تمرّ عبر Moyasar)

### ٣.٢ بيانات تُجمع تلقائيّاً

عند زيارة dealix.me أو api.dealix.me:

- **معلومات تقنيّة:** IP، User-Agent، نوع المتصفّح، نظام التشغيل
- **سجلّ الزيارات:** الصفحات التي زرتها، التوقيت، المدّة
- **Cookies:** session cookies (لتسجيل الدخول)، tracking cookies (PostHog إن فُعّل، اختياري)

نحن **لا نستخدم** advertising tracking (Google Ads / Facebook Pixel / TikTok Pixel).

### ٣.٣ بيانات نستلمها من أطراف ثالثة (sub-processors)

عند استخدام خدمات Dealix، قد نستلم بيانات إضافيّة من:

- **Hunter.io** (إن فُعّل) — context إثرائي للشركات (industry, employee count band)
- **Meta WhatsApp Business** (إن فُعّل) — رسائل واردة من العملاء الذين يتواصلون مع شركتك
- **Calendly** (إن فُعّل) — تفاصيل الـ bookings للـ demo

كل sub-processor مذكور في `landing/subprocessors.html` مع غرض المعالجة.

---

## ٤. لماذا نجمع هذه البيانات · Why we collect

### ٤.١ الأساس القانوني (Legal basis)

| النشاط | الأساس |
|---|---|
| تنفيذ عقد Sprint / Partner | تنفيذ عقد |
| إرسال إيميل ترحيب بعد diagnostic | الموافقة الصريحة + المصلحة المشروعة |
| اتّصال WhatsApp بعد warm-intro | الموافقة الصريحة (verbal + موثّقة في consent ledger) |
| الاحتفاظ بالفواتير ٦-١٠ سنوات | التزام قانوني (نظام ZATCA السعودي) |
| سجلّ التدقيق (audit log) | التزام قانوني + المصلحة المشروعة في الأمن |
| Sub-processor enrichment | تنفيذ العقد + المصلحة المشروعة |

### ٤.٢ الأغراض المحدّدة

نستخدم البيانات لـ:

1. تقديم خدمات Dealix (Sprint / Partner / Diagnostic)
2. توليد مسودّات ردود (مع موافقتك قبل أيّ إرسال)
3. إصدار الفواتير وتسجيل المدفوعات
4. الردّ على استفساراتك ودعم العملاء
5. تحسين خدماتنا (analytics) — مع redaction للـ PII
6. الالتزام بمتطلّبات PDPL + ZATCA + قوانين أخرى

**نحن لا نستخدم بياناتك لـ:**

- ❌ بيع البيانات أو تأجيرها لأطراف ثالثة
- ❌ تدريب نماذج LLM ذاتيّة لـ Dealix
- ❌ إرسال محتوى تسويقي بدون موافقتك
- ❌ مشاركتها مع منافسيك أو شركات إعلان

---

## ٥. كيف نحمي البيانات · How we protect

### ٥.١ الإجراءات الأمنيّة التقنيّة

- **التشفير في النقل:** TLS 1.3 على كل API + landing endpoint
- **التشفير في التخزين:** Postgres encryption-at-rest (Railway managed)
- **سجلّ تدقيق immutable:** كل عمليّة لها correlation_id
- **٨ بوّابات أمان مفروضة في الكود:** NO_LIVE_SEND · NO_LIVE_CHARGE · NO_COLD_WHATSAPP · NO_LINKEDIN_AUTO · NO_SCRAPING · NO_FAKE_PROOF · NO_FAKE_REVENUE · NO_BLAST
- **PII redaction** قبل تخزين أيّ نسخة في observability traces
- **Rate limiting** على endpoints حسّاسة
- **WhatsApp signature verification** على كل webhook وارد

### ٥.٢ الإجراءات الأمنيّة التنظيميّة

- وصول الـ admin محدود بـ Sami فقط (Wave 7)
- جميع الموظّفين / المتعاقدين الذين يصلون للبيانات يلتزمون بـ NDA
- التدريب على PDPL مسؤوليّة Dealix لكل من يصل للبيانات
- نسخ احتياطي يومي (Railway managed) + اختبار استرجاع كل ٣ شهور

### ٥.٣ في حالة خرق أمني

نلتزم بـ:
- إخطار SDAIA خلال **٧٢ ساعة** من اكتشاف الخرق
- إخطار الأفراد المتأثّرين خلال **٧٢ ساعة** عند تأثير عالي
- نشر بيان عام إن كان الخرق يمسّ عدداً كبيراً
- التفاصيل في `docs/PDPL_BREACH_RESPONSE_PLAN.md`

---

## ٦. مدّة الاحتفاظ بالبيانات · Retention

| نوع البيانات | مدّة الاحتفاظ |
|---|---|
| بيانات اتّصال نشطة (عميل دافع) | طوال مدّة العقد + ٣٠ يوم بعد الانتهاء |
| نسخ من المحادثات | طوال مدّة العقد + ٣٠ يوم |
| سجلّ التدقيق (audit log) | ٥ سنوات (التزام قانوني) |
| الفواتير + سجلّات المدفوعات | ٦-١٠ سنوات (نظام ZATCA) |
| Cookies (tracking — اختياري) | ١٢ شهر بحد أقصى |
| عناوين IP في log files | ٩٠ يوم ثمّ تُحذف أو تُقصّر |
| Diagnostic submissions (لم يصبحوا عملاء) | ١٢ شهر ثمّ تُحذف |

بعد انقضاء مدّة الاحتفاظ، البيانات تحذف بشكل آمن (overwrite + verification).

---

## ٧. حقوقك · Your rights

وفق نظام حماية البيانات الشخصيّة في المملكة العربيّة السعوديّة (PDPL)، لديك الحقوق التالية:

| الحق | الوصف | كيفيّة الممارسة |
|---|---|---|
| **حقّ الاطّلاع** | معرفة البيانات التي نمتلكها عنك | privacy@dealix.me — نرد خلال ٣٠ يوم |
| **حقّ الحصول على نسخة** | استلام نسخة structured (JSON / CSV) | كذلك |
| **حقّ التصحيح** | تصحيح البيانات الخاطئة | كذلك |
| **حقّ الحذف** | حذف بياناتك (مع استثناء الالتزامات القانونيّة) | كذلك |
| **حقّ تقييد المعالجة** | إيقاف معالجة بياناتك مؤقّتاً | كذلك |
| **حقّ النقل (Portability)** | استلام بياناتك بشكل machine-readable | كذلك |
| **حقّ الاعتراض** | الاعتراض على معالجة معيّنة (تسويق) | privacy@dealix.me — يتمّ الإيقاف فوراً |
| **حقّ سحب الموافقة** | سحب أيّ موافقة أعطيتها سابقاً | كذلك — السحب لا يؤثّر على المعالجة السابقة |
| **حقّ عدم الخضوع لقرار آلي** | طلب مراجعة بشريّة لأيّ قرار آلي يؤثّر عليك | كذلك |

التفاصيل الكاملة في `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`.

---

## ٨. النقل عبر الحدود · Cross-border transfer

بعض الـ subprocessors نستخدمهم يعالجون البيانات خارج المملكة:

- **Anthropic** (US) — معالجة LLM
- **Groq** (US) — معالجة LLM
- **Google** (US) — Gemini API
- **OpenAI** (US) — fallback
- **Hunter.io** (FR) — enrichment
- **Railway** (US) — استضافة backend
- **Cloudflare** (US) — DNS + CDN

نطبّق ضمانات تعاقديّة (Standard Contractual Clauses أو معادلها) مع كل واحد منهم. التفاصيل في `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.

إن كنت لا تقبل هذا النقل، تواصل معنا قبل التوقيع.

---

## ٩. Cookies والتتبّع · Cookies &amp; tracking

نستخدم cookies في الحالات التالية:

| النوع | الغرض | افتراضي |
|---|---|---|
| Session cookies | تسجيل الدخول لـ Customer Portal | مفعّل (ضروري) |
| PostHog (إن فُعّل) | analytics مجمّعة (لا PII) | معطّل افتراضاً — opt-in |
| LocalStorage | حفظ Customer Portal token | مفعّل بعد الـ access |

**لا نستخدم:** Google Ads pixel · Facebook Pixel · TikTok Pixel · أيّ cross-site tracking.

يمكنك تعطيل cookies من إعدادات متصفّحك (لكن قد تتأثّر تجربة Customer Portal).

---

## ١٠. الأطفال · Children

خدمات Dealix موجّهة للشركات (B2B) فقط. لا نجمع عمداً بيانات الأطفال (تحت ١٨ سنة). إن اكتشفنا أنّنا جمعنا بيانات طفل دون قصد، نحذفها فوراً.

---

## ١١. التغييرات على هذه السياسة · Changes to this policy

- نُخطر عن أيّ تغيير جوهري عبر:
  - بريد إلكتروني للعملاء الدافعين
  - بانر على dealix.me
  - تحديث "آخر تحديث" في أعلى هذه الصفحة
- التغييرات تسري بعد ٣٠ يوم من الإخطار

---

## ١٢. التواصل · Contact

لأيّ سؤال حول هذه السياسة أو لممارسة حقوقك:

- **بريد الخصوصيّة:** privacy@dealix.me
- **WhatsApp المؤسس:** [يُملأ عند تفعيل WBA]
- **العنوان البريدي:** [Sami's registered address]

نرد على جميع طلبات الخصوصيّة خلال **٧ أيّام عمل** كأقصى حد، ونقدّم استجابة كاملة لطلبات DSAR خلال **٣٠ يوم**.

---

## ١٣. السلطة الرقابيّة · Supervisory authority

إذا كنت ترى أنّنا أخللنا بحقوقك، يمكنك تقديم شكوى إلى:

**الهيئة السعوديّة للبيانات والذكاء الاصطناعي (SDAIA)**
- الموقع: sdaia.gov.sa
- نوصي بمحاولة حلّ المسألة معنا أوّلاً قبل التصعيد

---

## English summary

This Privacy Policy applies to all visitors, prospects, paying customers, and the individuals targeted by our customers' B2B services. We collect identification data, contact data, business context, message content (with PII redaction), and payment references (no card numbers stored). We use the data only to deliver Dealix services, never to sell data, never to train our own LLM models, and never for marketing without explicit consent.

We protect data with TLS encryption, encrypted-at-rest storage, immutable audit logs, 8 hard gates immutable in code (NO_LIVE_SEND, NO_LIVE_CHARGE, NO_COLD_WHATSAPP, NO_LINKEDIN_AUTO, NO_SCRAPING, NO_FAKE_PROOF, NO_FAKE_REVENUE, NO_BLAST), PII redaction before observability storage, and per-event correlation IDs.

Retention: active customer data for contract duration + 30 days; audit logs for 5 years; invoices for 6-10 years (ZATCA requirement); diagnostics that don't convert deleted after 12 months.

Saudi PDPL data subject rights: access, copy, correction, deletion, restriction, portability, objection, consent withdrawal, and human review of automated decisions. All rights exercised at privacy@dealix.me — 30-day response window.

Cross-border transfers (Anthropic, Groq, Gemini, OpenAI, Hunter, Railway, Cloudflare — all US/EU based) governed by standard contractual clauses or equivalent. Full details in `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.

We use only essential cookies + opt-in analytics. No advertising trackers. Children's data not collected (B2B only).

Supervisory authority: SDAIA (sdaia.gov.sa). Try resolving with us first at privacy@dealix.me.

---

## Appendix — Mapping to PDPL principles

| PDPL principle | This Policy section |
|---|---|
| Notice/transparency | §1, §2, §3, §4 |
| Consent + lawful basis | §4.1 |
| Data minimization | §3 (limited list) |
| Purpose limitation | §4.2 (specific purposes) |
| Retention | §6 |
| Security | §5 |
| Subject rights | §7 |
| Cross-border | §8 |
| Children | §10 |
| Supervisory authority | §13 |
