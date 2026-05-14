# Governed AI Operations Doctrine — دستور تشغيل AI المحوكم

_Version 0.1.0 · Maintained by Dealix · Doctrine: CC BY 4.0 · Code examples: MIT_

## EN — Preamble

This is the canonical text of the Governed AI Operations Doctrine. Eleven commitments define the perimeter inside which any AI operations team can claim to be governed rather than merely "AI-enabled". Each commitment is structured the same way: a name, what we promise, what we refuse, the operating control, the evidence artifact, and the abstract test category an adopter implements. The text is intentionally non-aspirational — every commitment maps to a mechanism, not a slogan. Adopters who skip the mechanism layer have not adopted the doctrine; they have adopted the marketing of it.

## AR — تمهيد

هذا هو النص المرجعي لدستور تشغيل AI المحوكم. أحد عشر التزاماً تُحدّد الحدّ الذي يفصل بين فريق تشغيل AI محوكم وفريق "مُمكَّن بـ AI" فحسب. كل التزام منظّم بنفس الترتيب: الاسم، الوعد، الرفض، الضابط التشغيلي، أثر الإثبات، وفئة الاختبار التجريدية التي يطبّقها المتبنّي. النص ليس طموحاً — كل التزام مربوط بآلية لا بشعار. من تبنّى النص دون الآليات فقد تبنّى تسويقه لا مضمونه.

---

## 1. No scraping — لا تجريف بيانات

- **Promise (EN):** Every contact in use comes from a legitimate source the team can name — a Source Passport the customer provided, a public registry with authorization, or a referral with consent.
- **الوعد (AR):** كل جهة اتصال مصدرها معروف يمكن تسميته — Source Passport قدّمه العميل، أو سجل عام مأذون، أو تحويل برضا صريح.
- **Refusal (EN):** No scraping of websites, social platforms, or third-party UIs. Any data acquired by scraping is quarantined and excluded from drafts and proof.
- **الرفض (AR):** لا تجريف للمواقع أو منصات التواصل أو الواجهات الخارجية. أي بيانات يتم الحصول عليها بالتجريف تُعزل وتُستبعد من المسودات والإثباتات.
- **Control:** Source Passport enforcement at the data-ingestion boundary.
- **Evidence artifact:** Source Passport record per contact.
- **Test category:** source-binding test.

## 2. No cold WhatsApp — لا واتساب بارد

- **Promise (EN):** Every WhatsApp message produced is a draft tied to a consented relationship. The operator approves each send individually; the recipient already opted in.
- **الوعد (AR):** كل رسالة واتساب مسودة مرتبطة بعلاقة موافَق عليها. المشغّل يوافق على كل إرسال على حدة، والمستلم قد وافق مسبقاً.
- **Refusal (EN):** No WhatsApp messages to recipients without explicit, recorded, opt-in consent tied to a Source Passport. Cold sends are blocked at the safe-send gateway.
- **الرفض (AR):** لا إرسال واتساب لمستقبلين دون موافقة صريحة موثّقة مرتبطة بـ Source Passport. الإرسال البارد محجوب عند بوابة الإرسال الآمن.
- **Control:** Channel-policy decision at the send gateway.
- **Evidence artifact:** Channel Policy decision log.
- **Test category:** channel-policy test.

## 3. No LinkedIn automation — لا أتمتة LinkedIn

- **Promise (EN):** LinkedIn data is used only when the customer provides a legitimate export they own. The team helps draft the message; the customer sends it from their own account.
- **الوعد (AR):** بيانات LinkedIn تُستخدم فقط إذا قدّم العميل تصديراً شرعياً يملكه. يساعد الفريق في صياغة الرسالة؛ العميل يرسلها من حسابه الشخصي.
- **Refusal (EN):** No automation of LinkedIn connection requests, messages, scraping, or feed actions. Such integrations are rejected at PR review and at runtime.
- **الرفض (AR):** لا أتمتة لطلبات الاتصال أو الرسائل أو تجريف البيانات أو إجراءات الواجهة. أي تكامل من هذا النوع مرفوض عند مراجعة PR وعند التشغيل.
- **Control:** Channel-policy refusal of LinkedIn automation surfaces.
- **Evidence artifact:** Channel Policy decision log.
- **Test category:** channel-policy test.

## 4. No fake or un-sourced claims — لا ادعاءات بلا مصدر

- **Promise (EN):** Every number, quote, case study, and proof artifact carries a `source_ref` and links to a Source Passport. The source is retrievable in the same minute it is asked for.
- **الوعد (AR):** كل رقم واقتباس ودراسة حالة وإثبات يحمل `source_ref` ويرتبط بـ Source Passport. المصدر قابل للاسترجاع في نفس الدقيقة.
- **Refusal (EN):** No publication of a number, quote, case study, or proof artifact without a source. Content without a source is downgraded to `draft_only` and public proof is blocked.
- **الرفض (AR):** لا نشر لرقم أو اقتباس أو دراسة حالة أو إثبات بدون مصدر. المحتوى بلا مصدر يُخفَّض إلى `draft_only` ويُحجب الإثبات العام.
- **Control:** Claim-review gate on every outbound proof artifact.
- **Evidence artifact:** Claim review log + Source Passport.
- **Test category:** claim-review test.

## 5. No guaranteed sales outcomes — لا ضمانات مبيعات

- **Promise (EN):** Commitments are framed as commitments, not guarantees. A KPI promise reads "we keep working at no extra cost until X is reached", never "we ensure X will close". An estimate is named as an estimate.
- **الوعد (AR):** الالتزامات تُصاغ التزاماتٍ لا ضمانات. وعد KPI يُقال فيه "نواصل دون مقابل إضافي حتى يتحقق X"، لا "نضمن X". التقدير يُسمّى تقديراً.
- **Refusal (EN):** No promise of a fixed revenue, deal count, or conversion rate. Words like "guarantee", "ensure", and "we will close X deals" are redacted from drafts.
- **الرفض (AR):** لا وعد بإيراد ثابت أو عدد صفقات أو معدّل تحويل. كلمات مثل "نضمن" و"سنغلق X صفقة" تُحذف من المسودات.
- **Control:** Customer-safe language redaction middleware.
- **Evidence artifact:** Claim review log.
- **Test category:** customer-safe-language test.

## 6. No PII in logs — لا PII في السجلات

- **Promise (EN):** Personal data (names, phone numbers, national IDs, emails, addresses) is redacted at the middleware boundary before any log writer sees it. PDPL-aligned by construction, not by promise.
- **الوعد (AR):** البيانات الشخصية تُحذف عند حدّ الـ middleware قبل أن يراها أي كاتب سجل. متوافق مع PDPL هندسياً لا وعداً.
- **Refusal (EN):** No raw personal data in application logs, friction logs, or telemetry. A leak is treated as a P0 incident.
- **الرفض (AR):** لا بيانات شخصية خام في سجلات التطبيق أو سجلات الاحتكاك أو القياسات. أي تسريب يُعالَج كحادثة P0.
- **Control:** Redaction middleware on every log path.
- **Evidence artifact:** Redaction middleware log.
- **Test category:** redaction middleware test.

## 7. No source-less knowledge answers — لا إجابة بلا مصدر

- **Promise (EN):** Every AI answer about the customer's business cites a Source Passport. If no source exists, the system returns "source required" rather than inventing an answer.
- **الوعد (AR):** كل إجابة AI عن عمل العميل مستندة إلى Source Passport. عند غياب المصدر، يُعاد "مصدر مطلوب" بدلاً من اختلاق الإجابة.
- **Refusal (EN):** No answer to a knowledge or research question without a Source Passport. AI responses are blocked when no source is bound to the query.
- **الرفض (AR):** لا إجابة لسؤال معرفي أو بحثي بدون Source Passport. ردود AI تُحجب عند عدم ربط مصدر بالطلب.
- **Control:** Source-binding gate on the AI router.
- **Evidence artifact:** Source Passport record per AI call.
- **Test category:** source-binding test.

## 8. No external action without approval — لا فعل خارجي بلا موافقة

- **Promise (EN):** Every external send, charge, publish, or share waits for an explicit human approval logged with an approver identity and a timestamp. The audit chain shows who clicked approve, when, and on what.
- **الوعد (AR):** كل إرسال أو دفعة أو نشر أو مشاركة خارجية ينتظر موافقة بشرية صريحة موثّقة بهوية الموافِق ووقت الموافقة. سلسلة التدقيق تُظهر من ضغط "موافق" ومتى وعلى ماذا.
- **Refusal (EN):** No external send, charge, publish, or share without approval. Bypass attempts are rejected with `REQUIRE_APPROVAL` or `BLOCK`.
- **الرفض (AR):** لا إرسال ولا دفعة ولا نشر ولا مشاركة خارجياً دون موافقة. محاولات الالتفاف تُرفض بـ `REQUIRE_APPROVAL` أو `BLOCK`.
- **Control:** Runtime decision function on every external action.
- **Evidence artifact:** Approval record + Audit Chain.
- **Test category:** approval-gate test.

## 9. No agent without identity — لا عميل ذكي بلا هوية

- **Promise (EN):** Every autonomous workflow ties to a registered agent identity (name, version, owner, governance scope). Every action traces to an identity in the audit chain.
- **الوعد (AR):** كل سير عمل ذاتي مرتبط بهوية عميل ذكي مسجّلة (الاسم، الإصدار، المالك، نطاق الحوكمة). كل إجراء يعود إلى هوية في سلسلة التدقيق.
- **Refusal (EN):** No autonomous workflow without a registered agent identity. Unregistered agents are rejected at the runtime registry.
- **الرفض (AR):** لا سير عمل ذاتي بدون هوية عميل ذكي مسجّلة. الوكلاء غير المسجّلين يُرفضون عند سجل التشغيل.
- **Control:** Agent registry check at workflow start.
- **Evidence artifact:** Agent Card + Agent Registry record.
- **Test category:** agent-identity test.

## 10. No project without a Proof Pack — لا مشروع بلا Proof Pack

- **Promise (EN):** Every closed engagement assembles a 14-section Proof Pack with a computed proof score. The customer receives a signed, exportable PDF before the engagement is invoiced as complete.
- **الوعد (AR):** كل ارتباط مغلق يجمّع Proof Pack من ١٤ قسماً مع نقاط إثبات محسوبة. يستلم العميل PDF موقّعاً قابلاً للتصدير قبل تَسجيل الارتباط كمكتمل.
- **Refusal (EN):** No project closure without an assembled Proof Pack. Such projects cannot be invoiced, referenced in case studies, or trigger retainer eligibility.
- **الرفض (AR):** لا إغلاق لمشروع دون تجميع Proof Pack. هذه المشاريع لا يمكن إصدار فاتورة لها، ولا الاستشهاد بها، ولا تفعّل أهلية الريتينر.
- **Control:** Proof Pack required-gate at engagement closure.
- **Evidence artifact:** Proof Pack PDF (14 sections).
- **Test category:** proof-pack test.

## 11. No project without a Capital Asset — لا مشروع بلا أصل رأسمالي

- **Promise (EN):** Every closed engagement deposits at least one reusable artifact — a scoring rule, draft template, governance rule, sector insight, productization signal, or proof example. The next engagement starts ahead because of the last.
- **الوعد (AR):** كل ارتباط مغلق يودع أصلاً قابلاً لإعادة الاستخدام — قاعدة تسجيل، قالب مسودة، قاعدة حوكمة، insight قطاع، إشارة منتَج، أو نموذج إثبات. الارتباط القادم يبدأ متقدّماً بسبب السابق.
- **Refusal (EN):** No project closure without depositing at least one reusable artifact. Zero-artifact projects are flagged as a productization failure, not a delivery success.
- **الرفض (AR):** لا إغلاق لمشروع دون إيداع أصل واحد على الأقل. مشاريع الصفر تُرفع كإخفاق في الإنتاج، لا كنجاح في التسليم.
- **Control:** Weekly reusable-artifact review at engagement closure.
- **Evidence artifact:** Reusable-artifact ledger record.
- **Test category:** reusable-artifact-ledger test.

---

## How this list changes — كيف يتغيّر هذا النص

The list does not grow casually and does not shrink ever. Adding a commitment requires a doctrinal-amendment PR. Removing a commitment is not allowed; a commitment may only be replaced by a stricter one with the same enforcement coverage.

لا يتوسّع النص بسهولة ولا يُختصر أبداً. الإضافة عبر طلب تعديل دستوري. لا يُسمح بحذف التزام؛ يجوز فقط استبداله بأشد منه بنفس نطاق التنفيذ.

The mapping between each abstract test category and the Dealix reference test paths lives in `CONTROL_MAPPING.md`. Adopters writing their own test suite map the abstract category to their own test path.

ربط فئات الاختبار التجريدية بمسارات اختبار Dealix المرجعية موجود في `CONTROL_MAPPING.md`. المتبنّون الذين يكتبون اختباراتهم يربطون الفئة التجريدية بمسارهم.

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
