# Dealix — مصنع مسودّات البريد البارد (Cold Email Draft Factory)

> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`
> **قاعدة المصنع:** هذا الخط ينتج **مسودّات فقط**. الإرسال نشاط منفصل مُعطَّل ومُبوَّب.

المصنع يحوّل العملاء المقيَّمين إلى **250 مسودّة/يوم** جاهزة للمراجعة. كل مسودّة
تمرّ سبع بوّابات وتحمل حقولاً إلزامية. **إنتاج المسودّة ليس إرسالاً** — 250
مسودّة/يوم مسموحة ومطلوبة؛ 250 إرسالة/يوم ممنوعة حتى تجتاز بوّابات قابلية التسليم
وطابور المؤسّس.

---

## 1. الخلطة اليومية (Daily Mix = 250)

| `draft_type` | الهدف اليومي | الدور |
|--------------|--------------|-------|
| `first_touch` | 100 | اللمسة الأولى — فرضية ألم + سؤال خفيف |
| `follow_up_1` | 75 | متابعة أولى — زاوية مختلفة لنفس الألم |
| `follow_up_2` | 50 | متابعة ثانية — قيمة/إثبات مختصر |
| `proposal_intro` | 15 | تمهيد عرض لمن أبدى اهتماماً |
| `close_loop` | 10 | إغلاق مهذّب يفتح الباب لاحقاً |
| **الإجمالي** | **250** | إنتاج مسودّات فقط |

> المصدر المرجعي للأرقام: `scripts/_lib/dealix.js` (`DRAFT_MIX_TARGET`) و
> `docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md`.

---

## 2. البوّابات السبع (كل مسودّة تمرّ بها)

| # | البوّابة | تتحقّق من | الفشل = |
|---|----------|-----------|---------|
| 1 | **brand gate** | الصوت والأفعال المسموحة، لا ادّعاءات ممنوعة | `forbidden_claim` |
| 2 | **offer match gate** | `offer_match` يطابق `pain_hypothesis` ضمن السلّم | رفض المطابقة |
| 3 | **personalization gate** | `personalization_score` ≥ P1 | `below_p1` |
| 4 | **compliance gate** | opt-out موجود، لا `Re:/Fwd:` وهمي | `missing_unsubscribe` / `fake_thread` |
| 5 | **evidence gate** | كل ادّعاء كمّي يحمل `evidence_level` صادق | رفض الإثبات |
| 6 | **deliverability gate** | المستلِم ليس على قائمة الإيقاف؛ الإرسال مُعطَّل | `suppressed` |
| 7 | **security gate** | لا PII، لا أسرار، أدوار فقط | رفض الأمان |

التفصيل التنفيذي (pass/fail) في `docs/outreach/OUTBOUND_RISK_GATES_AR.md`، مربوط بـ
`scripts/draft-quality-gate.js` واختبارات `tests/`.

---

## 3. حقول المسودّة الإلزامية

كل مسودّة تحمل (مطابقةً لـ `schemas/outreach_draft.schema.json`):

`prospect_id` · `company` · `sector` · `pain_hypothesis` · `offer_match` ·
`personalization_score` · `evidence_level` · `risk_level` · حالة opt-out
(`opt_out.included`) · `approval_status` · `send_status`.

إضافةً إلى: `draft_id` · `draft_type` · `subject` · `body`.

**الافتراضات:** `approval_status: pending` · `send_status: not_sent`.

---

## 4. قاعدة "إنتاج مسودّات فقط" (Draft-Production-Only)

- المصنع **لا يرسل**. ينتج إلى `data/outreach/drafts.jsonl` فقط.
- لا مسودّة دون P1 تدخل طابور الموافقة (انظر `PERSONALIZATION_RULES_AR.md`).
- لا مسودّة تُرسَل قبل: موافقة المؤسّس + حكم قابلية تسليم ≥ `LIMITED_SEND_READY` +
  عدم وجود المستلِم على قائمة الإيقاف.
- الافتراضات في كل خطوة: `dry_run=true` · `approval_required=true` · `send_enabled=false`.

---

## 5. الإيقاع

| الوقت | المرحلة | المخرج |
|------|---------|--------|
| 08:30 | توليد 250 مسودّة | `data/outreach/drafts.jsonl` |
| 09:00 | البوّابات السبع | `reports/outreach/DRAFT_GATE_REVIEW.md` |
| 10:00 | طابور موافقة المؤسّس | `reports/outreach/APPROVAL_QUEUE.md` |
| أسبوعياً | إيقاف أسوأ 20% من المسودّات | `docs/outreach/DRAFT_REJECTION_REASONS_AR.md` |

---

## 6. الحدود غير القابلة للتفاوض

- إنتاج مسودّات فقط · لا إرسال خارجي · لا تفعيل إرسال حقيقي.
- لا ادّعاءات ممنوعة (`نضمن` · `نضاعف الإيرادات` · `نتائج مضمونة` · `بدون مخاطرة` ·
  `10x` · `guaranteed revenue` · `no risk`).
- الأفعال المسموحة فقط: نساعد · نجهّز · نرتّب · نقيس · نكشف فرص التحسين · نقترح ·
  نجهّز مسودّات بموافقة.
- لا عملاء مخترَعين، لا أرقام ملفّقة (أمثلة «مثال توضيحي»، أسماء placeholder فقط).
- لا PII (أدوار فقط) · لا عناوين `Re:/Fwd:` وهمية · كل مسودّة باردة تحمل سطر
  «للإلغاء: ردّ «إيقاف».».

---

*المرجع المركزي: `docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md`. التخصيص:
`docs/outreach/PERSONALIZATION_RULES_AR.md`. البوّابات:
`docs/outreach/OUTBOUND_RISK_GATES_AR.md`.*
