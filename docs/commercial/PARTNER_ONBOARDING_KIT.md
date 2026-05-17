# حقيبة تأهيل الشريك / Partner Onboarding Kit

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-17
**وثائق مرافقة / Companion docs:** `../AGENCY_PARTNER_PROGRAM.md` · `../sales-kit/dealix_agency_partnerships.md` · `AFFILIATE_REVIEW_WORKFLOW.md`

---

الهدف من هذه الحقيبة: أن يبدأ الشريك بنظام عمل واضح — رسائل معتمدة، أسئلة تشخيص، عرض تجريبي محدد، ومسار إحالة — لا مجرد توجيه عام بـ«اذهب وابحث عن عملاء».

The purpose of this kit: give a partner a working system — approved messages, discovery questions, a defined pilot offer, and a referral path — not a vague instruction to "go find clients."

---

## 1. جملة تعريف الشريك / Partner one-liner

**عربي:** «Dealix تحوّل بيانات الحسابات والـ leads المبعثرة إلى ترتيب أولويات مُسنَد بأدلة ومسودات تواصل جاهزة للمراجعة — بدون إرسال آلي وبدون قوائم مشتراة.»

**English:** "Dealix turns scattered account and lead data into evidence-backed priority ordering and review-ready outreach drafts — no automated sending, no purchased lists."

استخدم هذه الجملة كما هي. لا تَعِد بأرقام مبيعات. / Use this sentence as-is. Do not promise sales numbers.

---

## 2. مَن تُحيل / Who to refer

أحِل جهة تنطبق عليها واحدة أو أكثر من الحالات التالية:

- وكالة لديها عملاء يصرفون على الإعلانات / an agency with ad clients.
- شركة تفقد leads بسبب ضعف المتابعة / a company with leads being lost.
- استشاري CRM لديه عميل ببيانات فوضوية / a CRM consultant with a chaotic client.
- مؤسس يشتكي من ضياع المتابعات / a founder complaining about follow-up.
- فريق مبيعات بـ pipeline غير موثَّق / a sales team with an undocumented pipeline.

العامل المشترك: توجد بيانات ومالك قرار وميزانية. / The common factor: there is data, an owner, and a budget.

---

## 3. مَن لا تُحيل / Who NOT to refer

لا تُحيل جهة تنطبق عليها أيٌّ من الحالات التالية:

| الحالة / Case | السبب / Reason |
|---|---|
| لا ميزانية / no budget | لا توجد دفعة تُبنى عليها العلاقة. |
| لا مالك قرار / no owner | لا أحد يعتمد المخرجات. |
| لا leads ولا بيانات / no leads | لا مادة خام للتشخيص. |
| يريد رسائل جماعية / wants spam | يخالف `no_cold_whatsapp`. |
| يريد scraping | يخالف `no_scraping`. |
| يريد ROI مضمونًا / wants guaranteed ROI | يخالف `no_unverified_outcomes`. |

إذا انطبقت أي حالة، اعتذر بوضوح ولا تُحيل. / If any case applies, decline clearly and do not refer.

---

## 4. الرسائل المعتمدة / Approved messages

دافئة فقط — مقدمة لجهة تعرفها أو سبق التواصل معها. لا واتساب بارد، لا رسائل جماعية. / Warm only — to a contact you know or have prior contact with. No cold WhatsApp, no bulk messaging.

**رسالة مقدمة (عربي):**
> «لاحظت أن فريقك يعالج leads كثيرة يدويًا. أعرف فريق Dealix — يبنون ترتيب أولويات مُسنَد بأدلة ومسودات تواصل جاهزة للمراجعة. تشخيص أولي مجاني. أوصلك بهم؟»

**Intro message (English):**
> "I noticed your team handles a lot of leads manually. I know the Dealix team — they build evidence-backed priority ordering and review-ready outreach drafts. The first diagnostic is free. Want an introduction?"

**رسالة متابعة (عربي):**
> «إذا حابب، أرسل لك ملخص التشخيص المجاني وتقرر بعدها. لا التزام.»

**Follow-up message (English):**
> "If useful, I can send you the free diagnostic summary and you decide from there. No commitment."

عدّل الاسم والسياق فقط؛ لا تُضِف وعودًا بنتائج. / Adjust only the name and context; do not add outcome promises.

---

## 5. أسئلة التشخيص / Discovery questions

أسئلة قصيرة يطرحها الشريك قبل الإحالة:

- كم عدد الـ leads أو الحسابات النشطة تقريبًا؟ / Roughly how many active leads or accounts?
- أين تُحفظ البيانات الآن — CRM، Excel، أم متفرقة؟ / Where does the data live — CRM, Excel, or scattered?
- مَن يقرر على مَن نتصل أولًا، وكيف؟ / Who decides who to contact first, and how?
- ما أكبر سبب لضياع متابعة؟ / What is the biggest reason a follow-up is missed?
- مَن يعتمد القرار وميزانية التشغيل؟ / Who owns the decision and the operating budget?

---

## 6. العرض التجريبي / The pilot offer

نقطة الدخول دائمًا منخفضة المخاطر، ومرتبطة بعرضين معتمدين فقط:

| العرض / Offer | المُعرّف / Offer ID | السعر / Price |
|---|---|---|
| التشخيص المصغّر المجاني / Free mini diagnostic | `free_mini_diagnostic` | 0 ريال / 0 SAR |
| سبرنت إثبات الإيراد / Revenue proof sprint | `revenue_proof_sprint_499` | 499 ريال / 499 SAR |

ابدأ بـ `free_mini_diagnostic`؛ ومَن يجد قيمة ينتقل إلى `revenue_proof_sprint_499`. لا تَعرض ولا تُسعّر أي مستوى آخر — هذا دور فريق Dealix. الأسعار المعتمدة بالكامل في `../AGENCY_PARTNER_PROGRAM.md` وخريطة العروض.

Start with `free_mini_diagnostic`; anyone who finds value moves to `revenue_proof_sprint_499`. Do not present or price any other tier — that is the Dealix team's role.

---

## 7. قواعد العمولة / Commission rules

النِّسب والمبالغ ومستويات الشركاء محدَّدة حصريًا في `../AGENCY_PARTNER_PROGRAM.md` — وهي المصدر المعتمد الوحيد. لا تُعيد ذكر أي نسبة أو مبلغ في أي مادة تواصل مع العميل.

Commission rates, amounts, and partner tiers are defined exclusively in `../AGENCY_PARTNER_PROGRAM.md` — the single source of truth. Do not restate any percentage or amount in customer-facing material.

القاعدة العامة فقط: لا تُصرف عمولة قبل دفع العميل لفاتورة فعلية. / General rule only: no commission before the client pays an actual invoice.

---

## 8. عيّنة Proof Pack / Proof Pack sample

شارك العيّنة المعتمدة لتوضيح شكل المخرجات: `SAMPLE_PROOF_PACK.md`. وللتفاصيل الكاملة للمخرجات، استخدم `OFFER_LEAD_INTELLIGENCE_SPRINT_AR.md` كمرجع.

Share the approved sample to show what deliverables look like: `SAMPLE_PROOF_PACK.md`. For full deliverable detail, use `OFFER_LEAD_INTELLIGENCE_SPRINT_AR.md` as a reference.

العيّنة آمنة الحالة — لا بيانات عميل حقيقي. / The sample is case-safe — no real customer data.

---

## 9. ادعاءات ممنوعة / Forbidden claims

لا يقول الشريك — كتابةً أو شفهيًا — أيًّا مما يلي:

- «ROI مضمون» أو أي رقم مبيعات أو نسبة تحويل كحقيقة / "guaranteed ROI" or any sales number or conversion rate as fact.
- إثبات أو شهادة عميل غير حقيقية / fabricated proof or testimonial (`no_fake_proof`).
- عرض خدمات scraping أو واتساب بارد / offering scraping or cold WhatsApp (`no_scraping`, `no_cold_whatsapp`).
- إيحاء بأن Dealix تُرسل رسائل بالنيابة عن العميل تلقائيًا / implying Dealix auto-sends messages on the customer's behalf.

Dealix تنتج مسودات للمراجعة فقط؛ الإرسال يبقى قرار العميل بموافقة صريحة. / Dealix produces review-only drafts; sending stays the customer's decision with explicit approval.

---

## 10. مسار تقديم الإحالة / Referral submission flow

1. تأكد من توافق الجهة مع القسم 2 وعدم انطباق القسم 3. / Confirm fit per section 2 and no exclusion per section 3.
2. احصل على موافقة الجهة على المقدمة. / Get the contact's consent for the introduction.
3. أرسل بريدًا إلى `partners@dealix.sa` بعنوان «Referral — [اسم الجهة]» يتضمن: اسم الجهة، جهة الاتصال، القطاع، حجم البيانات التقريبي، وملاحظات التشخيص. / Email `partners@dealix.sa`, subject "Referral — [company]", with company, contact, sector, approximate data size, and discovery notes.
4. يصدر فريق Dealix رابط تتبّع وينسب الإحالة. / Dealix issues a tracking link and attributes the referral.
5. تُسجَّل الإحالة وتمر بمسار التأهيل والمراجعة في `AFFILIATE_REVIEW_WORKFLOW.md`. / The referral is logged and passes through `AFFILIATE_REVIEW_WORKFLOW.md`.

لا تُرسل بيانات شخصية حساسة (هوية وطنية، تفاصيل بنكية) في نموذج الإحالة. / Do not send sensitive personal data (national ID, banking details) in the referral form.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
