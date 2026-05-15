# LinkedIn Post 005 — Source Passport 101

> Bilingual long-form for the founder voice. AR first, EN second. No emojis. No model names. JSON schema is the only code block.
>
> Cross-link: [LINKEDIN_POST_002.md](./LINKEDIN_POST_002.md), [04_data_os/SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md), [23_standards/SOURCE_PASSPORT_STANDARD.md](../23_standards/SOURCE_PASSPORT_STANDARD.md), [LINKEDIN_CADENCE_PLAN.md](./LINKEDIN_CADENCE_PLAN.md).

---

**Title — العنوان**

Source Passport 101 — لماذا كل dataset يحتاج جواز مصدر / Source Passport 101 — why every dataset needs a provenance card.

---

## القاعدة — The Rule

**لا جواز مصدر = لا استخدام للذكاء الاصطناعي. لا استثناء.**

**No Source Passport = no AI use. No exceptions.**

---

## العربية أولاً

### لماذا قاعدة واحدة، لا قائمة قواعد

كل خرق بيانات في الخليج بدأ بدفعة بيانات دخلت دون توثيق. المصدر مجهول، الإذن مفترَض، والمسؤول غير معروف وقت الحادث. جواز المصدر يُغلق هذه الفجوة قبل أن تُفتَح.

### الحقول التسعة الإلزامية

لكل ملف، كل دفعة، كل اتصال نظامي يدخل ديليكس، نُرفِق جواز مصدر بتسعة حقول:

```json
{
  "source_id": "<auto>",
  "source_type": "client_upload | crm_export | manual_entry | partner_data | licensed_dataset",
  "owner": "client | dealix | partner",
  "allowed_use": ["internal_analysis", "draft_only", "reporting", "scoring"],
  "contains_pii": true,
  "sensitivity": "low | medium | high",
  "ai_access_allowed": true,
  "external_use_allowed": false,
  "retention_policy": "project_duration | retainer_duration | anonymize_after_close | delete_after_close"
}
```

كل حقل قرار، لا وصف. الفرق بين قرار وصف: القرار يُلزم البوابة، الوصف يُلزم الذاكرة.

### مصفوفة القرار

البوابة لا تستشير المؤسس في كل دفعة. تطبّق مصفوفة قرار صارمة:

| الحالة | القرار |
|---|---|
| لا جواز مصدر | **BLOCK** |
| جواز مصدر غير صالح (حقل مفقود) | **BLOCK** |
| `contains_pii = true` و `external_use_allowed = true` | **REQUIRE_APPROVAL** |
| `sensitivity = high` | **REQUIRE_APPROVAL** |
| جواز سليم بقيود | **ALLOW** ضمن `allowed_use` |

لا "نناقش لاحقاً". لا "سنوثّق غداً". إن أردتَ أن يلمس النظام البيانات، تكتب الجواز أولاً.

### لماذا هذا مهم لـ B2B السعودي

ثلاث ركائز:

1. **المادة الخامسة من نظام حماية البيانات الشخصية (PDPL):** تشترط أساساً نظامياً لكل معالجة. جواز المصدر يُسجِّل هذا الأساس.
2. **المادة الثامنة عشرة (مسار التدقيق):** كل عملية معالجة يجب أن تترك أثراً مرجعياً. الجواز هو الأثر.
3. **مشتريات المؤسسات السعودية:** كل بنك، كل جهة حكومية، كل شركة كبرى تسأل قبل التوقيع: "من أين جاءت هذه البيانات؟" الجواب الجاهز يختصر شهراً من المراجعة.

### ثلاثة أنماط ترفضها ديليكس

كل واحد منها لا يستطيع إنتاج جواز صالح، فيُرفَض من البوابة لا من المؤسس:

1. **الكشط (Scraping):** لا مالك معروف، لا إذن استخدام، لا سياسة احتفاظ. لا جواز ممكن.
2. **القوائم المشتراة:** "الموزّع" ليس مالكاً قانونياً للبيانات. لا جواز ممكن.
3. **بيانات الاعتماد المشتركة (shared credentials):** لا مالك مفرد، فلا توقيع موثوق. لا جواز ممكن.

هذه ليست تحفّظات تجارية — هذه قراءة مباشرة لنظام حماية البيانات وقواعد الحوكمة.

### دعوة

تشخيص مجاني، 24 ساعة، عبر `/diagnostic.html`. سنُريك أي بياناتك تمتلك جوازاً صالحاً، وأي منها يحتاج معالجة قبل أن تلمسه أيّ أداة ذكاء اصطناعي.

---

## English

### Why one rule, not a list

Every data breach in the Gulf started with an undocumented data batch entering a system. The source was unknown, permission was assumed, and the data owner could not be reached when the incident happened. The Source Passport closes that gap before it opens.

### The 9 required fields

For every file, batch, or system connection that enters Dealix, we attach a Source Passport with nine mandatory fields. The schema is in the JSON block above. Each field is a **decision**, not a description. A decision binds the gate; a description binds only memory.

### The decision matrix

The gate does not consult the founder per batch. It applies a strict matrix:

| Condition | Gate decision |
|---|---|
| No Source Passport | **BLOCK** |
| Invalid Passport (missing field) | **BLOCK** |
| `contains_pii = true` AND `external_use_allowed = true` | **REQUIRE_APPROVAL** |
| `sensitivity = high` | **REQUIRE_APPROVAL** |
| Valid Passport within bounds | **ALLOW**, within `allowed_use` |

No "we'll discuss later". No "we'll document tomorrow". If you want the system to touch the data, write the Passport first.

### Why this matters for Saudi B2B

Three pillars:

1. **PDPL Article 5 (lawful basis):** every processing activity requires a documented legal basis. The Source Passport records that basis at the moment of intake.
2. **PDPL Article 18 (audit trail):** every processing event must leave a referenceable record. The Passport is the record.
3. **Saudi enterprise procurement:** every bank, every government entity, every large corporate asks one question before signing: "Where did the data come from?" A ready answer saves a month of review.

### Three anti-patterns Dealix refuses

Each one cannot produce a valid Passport, so the gate rejects them — not the founder:

1. **Scraping:** no known owner, no use permission, no retention policy. No Passport possible.
2. **Purchased lists:** the "broker" is not the legal data owner. No Passport possible.
3. **Shared credentials:** no single owner, so no trusted signature. No Passport possible.

These are not commercial preferences — they are direct readings of PDPL and governance norms.

### CTA

Free 24-hour diagnostic at `/diagnostic.html`. We will show you which of your datasets carry a valid Passport, and which need work before any AI tool touches them.

Read more: [SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md) and the formal standard at [SOURCE_PASSPORT_STANDARD.md](../23_standards/SOURCE_PASSPORT_STANDARD.md).

---

`#SaudiAI` `#PDPL` `#DataGovernance` `#B2B`

---

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**
