# LinkedIn Post 002 — Source Passport

> Bilingual long-form for the founder voice. AR first, EN second. No emojis. No model names. Schema rendered as a code block (the only acceptable code in a marketing post).
>
> Cross-link: [LINKEDIN_POST_001.md](./LINKEDIN_POST_001.md), [LINKEDIN_POST_003.md](./LINKEDIN_POST_003.md), [04_data_os/SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md), [LINKEDIN_CADENCE_PLAN.md](./LINKEDIN_CADENCE_PLAN.md).

---

**Title — العنوان**

Source Passport — لماذا كل بيانات تدخل Dealix تحتاج جواز مصدر / Source Passport — why every dataset entering Dealix needs a provenance card.

---

## العربية أولاً

### القاعدة الواحدة

في ديليكس، لا تدخل بيانات النظام بلا جواز مصدر. لا استثناء، ولا قائمة "نأخذها الآن ونوثّقها لاحقاً". إن لم يكن للبيانات جواز، ترفضها البوابة. هذا ليس بيروقراطية، بل تطبيق مباشر للمادة الخامسة من نظام حماية البيانات الشخصية، التي تشترط أساساً نظامياً لكل معالجة.

### ما هو جواز المصدر

جواز المصدر بطاقة بيانات تُرفَق بكل ملف أو دفعة أو اتصال بنظام عميل. تحوي تسعة حقول إلزامية:

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

كل حقل قرار، لا وصف:

- **source_id** — مُعرّف يُولَّد عند الاستلام. كل أثر لاحق (حساب مُرتَّب، مسوّدة، عنصر إثبات، التزام قيمة، أصل) يحمل هذا المُعرّف مرجعاً لمصدره. لا أثر بلا مصدر.
- **source_type** — واحد من خمسة فقط. أي شيء خارجها — بما في ذلك الكشط، والقوائم "الموجودة"، وبيانات اللينكدإن المُجمَّعة آلياً — مرفوض عند البوابة.
- **owner** — من يملك البيانات قانونياً. في الغالب العميل. حين يكون الشريك، نطلب اتفاق نقل البيانات.
- **allowed_use** — قائمة من أربعة وضعيات. صياغة المسوّدات تتطلب `draft_only`. الترتيب يتطلب `scoring`. التقارير تتطلب `reporting`. لا نُوسّع القائمة لإرضاء عميل.
- **contains_pii** — منطقي. إذا كان صحيحاً، يُفعَّل إخفاء البيانات الشخصية في كل سجل، وكل مسوّدة، وكل لقطة شاشة تُحفظ.
- **sensitivity** — منخفضة، متوسطة، أو عالية. الحساسية العالية تستدعي قرار `REQUIRE_APPROVAL` تلقائياً في طبقة الحوكمة.
- **ai_access_allowed** — هل يُسمح بإرسال البيانات إلى أي نموذج ذكاء اصطناعي. إذا لم يُسمح، تعمل تدفقات حتمية فقط على هذا المصدر، ولا تلمسه أي مسوّدة آلية.
- **external_use_allowed** — هل يُسمح للنتائج المُشتقَّة من هذا المصدر بمغادرة نظامنا. إذا لم يُسمح، تُمنع دراسات الحالة العامة والإحالات الخارجية ومشاركات الشركاء.
- **retention_policy** — موعد الحذف أو الإخفاء. مدة المشروع، مدة الاشتراك، إخفاء بعد الإغلاق، أو حذف بعد الإغلاق.

### مصفوفة القرار

| الحالة | القرار |
|---|---|
| لا جواز مصدر مُرفق | `BLOCK` — لا استيعاب |
| `source_type` غير معروف | `BLOCK` — خمسة أنواع فقط مقبولة |
| `contains_pii = true` و `external_use_allowed = true` | `REQUIRE_APPROVAL` — موافقة بشرية صريحة قبل أي إجراء خارجي |
| `contains_pii = true` و `retention_policy = project_duration` | `ALLOW_WITH_REVIEW` — مع مراجعة احتفاظ عند الإغلاق |
| `ai_access_allowed = false` | تُعطَّل أي مسوّدة آلية على هذا المصدر |
| `external_use_allowed = false` | تُعطَّل المشاركة العامة لأي مُخرَج مُشتق |

الجواز يُحدّد السقف، والطبقات اللاحقة لا تتجاوزه. يمكنها أن تُضيّق القرار، لا أن توسّعه.

### دعوة

ابدأ بتشخيص مجاني خلال 24 ساعة، يُسلَّم باعتماد المؤسس. أوّل ما تراه من ديليكس هو جواز مصدر طلباتك، مُطبَّقاً عليك قبل أن تدفع لنا ريالاً.

---

## English

### The one rule

At Dealix, data does not enter the system without a Source Passport. No exception. No "we will take it now and document it later." If a dataset has no passport, the gate refuses it. This is not bureaucracy; it is a direct application of PDPL Article 5, which requires a lawful basis for every processing activity.

### What a Source Passport is

A Source Passport is a provenance card attached to every file, batch, or live system connection. It carries nine mandatory fields (schema rendered above in the Arabic block).

Each field is a decision, not a description:

- **source_id** — generated on intake. Every downstream artifact (a ranked account, a draft, a proof item, a value entry, a capital asset) carries this `source_id` as `source_ref`. No artifact without a source.
- **source_type** — one of five values. Anything else — including scraping, "found" lists, harvested LinkedIn data — is refused at the gate. This refusal is one of the eleven constitutional non-negotiables.
- **owner** — who legally controls the data. Most often the client. When it is a partner, we require a data transfer agreement on file before intake.
- **allowed_use** — a list of up to four modes. Drafting outreach requires `draft_only`. Ranking requires `scoring`. Reports require `reporting`. We do not expand the list to please a customer.
- **contains_pii** — boolean. When true, PII redaction is enforced on every log line, every draft, and every saved screenshot.
- **sensitivity** — low, medium, or high. High sensitivity auto-promotes downstream actions to `REQUIRE_APPROVAL` in the governance layer.
- **ai_access_allowed** — whether the data may be sent to any AI model. When false, only deterministic workflows touch this source; no AI-generated draft is permitted.
- **external_use_allowed** — whether output derived from this source may leave Dealix systems. When false, public case studies, third-party shares, and partner forwards are disabled for everything derived from this source.
- **retention_policy** — when the data must be deleted, anonymized, or retained. Four standard choices, no custom ones.

### The decision matrix in plain language

| If this is true | Then the decision is |
|---|---|
| No passport attached | `BLOCK` — refuse intake |
| Unknown `source_type` | `BLOCK` — only the five enumerated types are accepted |
| `contains_pii = true` AND `external_use_allowed = true` | `REQUIRE_APPROVAL` — explicit human approval before any external action |
| `contains_pii = true` AND `retention_policy = project_duration` | `ALLOW_WITH_REVIEW` — proceed, with mandatory retention check at close |
| `ai_access_allowed = false` | All AI drafting on this source is disabled |
| `external_use_allowed = false` | All public sharing of derived output is disabled |

The passport sets the ceiling. Downstream layers may narrow the decision (a draft destined for WhatsApp is downgraded to `DRAFT_ONLY` regardless), but never widen it. The ceiling is the contract.

### Why this matters to a Saudi B2B leader

If you cannot answer, today, the question "who owns this dataset and what is it allowed to do," your team is one regulator letter away from a freeze. The cheapest version of governance is to attach a passport at intake. The most expensive version is to reconstruct provenance after a breach, in 72 hours, under PDPL Article 21 reporting obligations.

### CTA — دعوة

Start with the **Free Diagnostic**. Twenty-four hours. Two pages. Founder signature. The first thing you see from Dealix is a Source Passport on your own intake — the methodology applied to you before you pay us a riyal.

Reply with "passport" / "جواز" to begin, or use the email in the company profile.

`#SaudiAI` `#PDPL`

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
