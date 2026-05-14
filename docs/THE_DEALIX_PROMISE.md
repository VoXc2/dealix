# وعد Dealix — The Dealix Promise
## ١١ التزاماً مكتوباً في الكود — 11 commitments written into the code

> **العربية أوّلاً.** هذه الصفحة عقد علني بين Dealix والمراجع لديك — سواء كان CISO شركتك، أو فريق امتثال SAMA، أو مكتب NDMO. كل سطر هنا ليس وعداً تسويقياً، بل اختبار CI ينجح أو يفشل في كل عملية دفع كود. لو سقط أحد هذه الالتزامات، يسقط البناء كله ولا يصل إلى الإنتاج.
>
> **English secondary.** This page is a public contract between Dealix and your reviewer — whether your CISO, the SAMA compliance desk, or the NDMO office. Every line below is not marketing copy; it is a CI test that passes or fails on every push. If any commitment breaks, the build breaks, and nothing reaches production.

---

## 1. No scraping — لا تجريف بيانات

**EN — Promise.** Every contact we use comes from a legitimate source you can name — a Source Passport you provided, a public registry you authorize, a referral with consent. Provenance is recorded on the same row as the contact, and removing the source removes the contact from every downstream draft, report, and proof artifact within the same minute.

**AR — وعد.** كل جهة اتصال نستخدمها مصدرها معروف يمكنك تسميته — Source Passport قدّمته أنت، سجل عام تأذن لنا باستخدامه، أو تحويل برضا صريح. المصدر مسجَّل في نفس صف جهة الاتصال، وحذف المصدر يحذف الجهة من كل مسودة وتقرير وإثبات لاحق خلال الدقيقة نفسها.

**EN — Refusal.** We do not scrape websites, social platforms, or third-party UIs to harvest contacts or content. Any data acquired by scraping is quarantined and excluded from drafts and proof.

**AR — رفض.** لا نقوم بتجريف المواقع أو منصات التواصل أو الواجهات الخارجية لجمع جهات الاتصال أو المحتوى. أي بيانات يتم الحصول عليها بالتجريف تُعزل وتُستبعد من المسودات والإثباتات.

Enforced by: `tests/test_no_scraping_engine.py`, `tests/test_no_linkedin_scraper_string_anywhere.py`

---

## 2. No cold WhatsApp — لا واتساب بارد

**EN — Promise.** Every WhatsApp message Dealix produces is a draft tied to a consented relationship — you (the founder) approve every send individually. The recipient already opted in, and the opt-in record is bound to the Source Passport that produced the contact.

**AR — وعد.** كل رسالة واتساب ينتجها Dealix هي مسودة مرتبطة بعلاقة موافَق عليها — أنت (المؤسس) توافق على كل إرسال على حدة. المستلم وافق مسبقاً، وسجل الموافقة مرتبط بـ Source Passport الذي أنتج جهة الاتصال.

**EN — Refusal.** We do not send WhatsApp messages to recipients without explicit, recorded, opt-in consent tied to a Source Passport. Cold WhatsApp sends are blocked at the safe_send_gateway layer.

**AR — رفض.** لا نرسل رسائل واتساب لمستقبلين بدون موافقة صريحة موثّقة مرتبطة بـ Source Passport. الإرسال البارد محجوب في طبقة safe_send_gateway.

Enforced by: `tests/test_no_cold_whatsapp.py`

---

## 3. No LinkedIn automation — لا أتمتة LinkedIn

**EN — Promise.** Dealix uses LinkedIn data only when you provide a legitimate export you own. We help you write the message; you send it from your own account. The split between drafting and sending is structural — there is no code path inside Dealix that can post to LinkedIn for you.

**AR — وعد.** Dealix يستخدم بيانات LinkedIn فقط عندما تقدّم تصديراً شرعياً تملكه. نساعدك في صياغة الرسالة؛ أنت ترسلها من حسابك الشخصي. الفصل بين الصياغة والإرسال هندسي — لا يوجد مسار كود داخل Dealix يستطيع النشر على LinkedIn نيابةً عنك.

**EN — Refusal.** We do not automate LinkedIn connection requests, messages, scraping, or feed actions. Any integration that automates LinkedIn is rejected at PR review and at runtime.

**AR — رفض.** لا نقوم بأتمتة طلبات الاتصال أو الرسائل أو تجريف بيانات LinkedIn أو إجراءات الواجهة. أي تكامل يقوم بأتمتة LinkedIn مرفوض على مستوى مراجعة PR والتشغيل.

Enforced by: `tests/test_no_linkedin_automation.py`, `tests/test_no_linkedin_scraper_string_anywhere.py`

---

## 4. No fake or un-sourced claims — لا ادعاءات بلا مصدر

**EN — Promise.** Every number, quote, case study, and proof artifact carries a `source_ref` and links to a Source Passport. If you ask where a number came from, we can show you the file in the same minute, with the line range and the timestamp the source was registered.

**AR — وعد.** كل رقم واقتباس ودراسة حالة وإثبات يحمل `source_ref` ويرتبط بـ Source Passport. لو سألت عن مصدر رقم، نرجع لك بالملف خلال نفس الدقيقة، مع نطاق الأسطر ووقت تسجيل المصدر.

**EN — Refusal.** We do not publish a number, quote, case study, or proof artifact without a source. Content without a source is downgraded to `draft_only` and public proof is blocked.

**AR — رفض.** لا ننشر رقماً أو اقتباساً أو دراسة حالة أو إثباتاً بدون مصدر. المحتوى بدون مصدر يُخفّض إلى `draft_only` ويُحجب الإثبات العام.

Enforced by: `tests/test_no_guaranteed_claims.py`

---

## 5. No guaranteed sales outcomes — لا ضمانات مبيعات

**EN — Promise.** We commit to commitments, never guarantees. Our KPI promises read "we keep working at no cost until X is reached", never "we ensure X will close". The estimate is always marked as such, and every customer-facing artifact ends with the bilingual disclaimer that estimated outcomes are not guaranteed outcomes.

**AR — وعد.** نلتزم بالتزامات، لا بضمانات. وعود KPI نقول فيها "نواصل بدون مقابل حتى يتحقق X"، ولا نقول أبداً "نضمن X". التقدير يُسمّى تقديراً، وكل مخرج مواجه للعميل ينتهي بإخلاء مسؤولية ثنائي اللغة بأن النتائج التقديرية ليست نتائج مضمونة.

**EN — Refusal.** We do not promise a fixed revenue, deal count, or conversion rate. Words like "guarantee", "ensure", and "we will close X deals" are redacted from drafts.

**AR — رفض.** لا نَعِد بإيراد ثابت أو عدد صفقات أو معدّل تحويل. كلمات مثل "نضمن" و"سنغلق X صفقة" تُحذف من المسودات.

Enforced by: `tests/test_no_guaranteed_claims.py`, `tests/test_customer_safe_product_language.py`

---

## 6. No PII in logs — لا PII في السجلات

**EN — Promise.** Personal data (names, phone numbers, national IDs, emails, addresses) is redacted at the middleware boundary before any log writer sees it. PDPL-aligned by construction, not by promise. The redaction happens before the log line is formatted, so even a verbose debug build cannot leak personal data.

**AR — وعد.** البيانات الشخصية (الأسماء، الأرقام، الهويات، البريد، العناوين) تُحذف عند حدّ الـ middleware قبل أن يراها أي كاتب سجل. متوافق مع PDPL هندسياً، لا وعداً. الحذف يحصل قبل تنسيق سطر السجل، حتى نسخة التصحيح المفصّلة لا يمكنها تسريب بيانات شخصية.

**EN — Refusal.** We do not write raw personal data into application logs, friction logs, or telemetry. A leak is treated as a P0 incident.

**AR — رفض.** لا نكتب بيانات شخصية خام في سجلات التطبيق أو سجلات الاحتكاك أو القياسات. أي تسريب يُعالَج كحادثة P0.

Enforced by: `api/middleware/bopla_redaction.py`, `auto_client_acquisition/friction_log/sanitizer.py`

---

## 7. No source-less knowledge answers — لا إجابة بلا مصدر

**EN — Promise.** Every AI answer about your business cites a Source Passport. If we lack a source, we return "source required" — we do not invent an answer to look helpful. The empty answer is the honest answer when the source is missing, and you are notified which source is needed to unblock the question.

**AR — وعد.** كل إجابة AI عن عملك مستندة إلى Source Passport. لو ما عندنا مصدر، نرجع "مصدر مطلوب" — لا نختلق جواباً لنبدو مفيدين. الإجابة الفارغة هي الإجابة الصادقة عند غياب المصدر، ويصلك إشعار بالمصدر المطلوب لفك حجب السؤال.

**EN — Refusal.** We do not answer a knowledge or research question without a Source Passport. AI responses are blocked when no source is bound to the query.

**AR — رفض.** لا نجيب على سؤال معرفي أو بحثي بدون Source Passport. ردود AI تُحجب عند عدم ربط مصدر بالطلب.

Enforced by: `tests/test_no_source_passport_no_ai.py`

---

## 8. No external action without approval — لا فعل خارجي بلا موافقة

**EN — Promise.** Every external send, charge, publish, or share waits for an explicit human approval logged with an approver identity and timestamp. The audit chain shows who clicked approve, when, and on what — and the chain is exportable as a PDF for your CISO or SAMA reviewer on demand.

**AR — وعد.** كل إرسال أو دفعة أو نشر أو مشاركة خارجية ينتظر موافقة بشرية صريحة موثّقة بهوية الموافِق ووقت الموافقة. سلسلة التدقيق تُظهر من ضغط "موافق" ومتى وعلى ماذا — والسلسلة قابلة للتصدير كـ PDF لمراجع CISO أو SAMA عند الطلب.

**EN — Refusal.** We do not send, charge, publish, or share externally without approval. Bypass attempts are rejected by `decide(action, context)` with `REQUIRE_APPROVAL` or `BLOCK`.

**AR — رفض.** لا نرسل ولا نَخصم ولا ننشر ولا نشارك خارجياً بدون موافقة. محاولات الالتفاف تُرفض بواسطة `decide(action, context)` بـ `REQUIRE_APPROVAL` أو `BLOCK`.

Enforced by: `tests/test_pii_external_requires_approval.py`, `auto_client_acquisition/governance_os/runtime_decision.py`

---

## 9. No agent without identity — لا عميل ذكي بلا هوية

**EN — Promise.** Every autonomous workflow ties to a registered agent identity (name, version, owner, governance scope). Every action traces to an identity in the audit chain, so a question of the form "which agent did this, on whose behalf, at what version" always has a one-row answer.

**AR — وعد.** كل سير عمل ذاتي مرتبط بهوية عميل ذكي مسجّلة (الاسم، الإصدار، المالك، نطاق الحوكمة). كل إجراء يعود إلى هوية في سلسلة التدقيق، فسؤال من نوع "أي عميل ذكي فعل هذا، نيابةً عن من، بأي إصدار" دائماً له إجابة من صف واحد.

**EN — Refusal.** We do not run an autonomous workflow without a registered agent identity. Unregistered agents are rejected at the runtime registry.

**AR — رفض.** لا نُشغّل أي سير عمل ذاتي بدون هوية عميل ذكي مسجّلة. الوكلاء غير المسجّلين يُرفضون في سجل التشغيل.

Enforced by: `auto_client_acquisition/agent_os/agent_registry.py`, `auto_client_acquisition/secure_agent_runtime_os/four_boundaries.py`

---

## 10. No project without a Proof Pack — لا مشروع بلا Proof Pack

**EN — Promise.** Every closed engagement assembles a 14-section Proof Pack with a computed proof score. You receive a signed, exportable PDF before the engagement is invoiced as complete, and the PDF can be replayed against the audit chain at any later date to confirm nothing was edited after sign-off.

**AR — وعد.** كل ارتباط مغلق يجمّع Proof Pack من ١٤ قسماً مع نقاط إثبات محسوبة. تستلم PDF موقّعاً قابلاً للتصدير قبل تَسجيل الارتباط كمكتمل، ويمكن إعادة تشغيل الـ PDF مقابل سلسلة التدقيق في أي تاريخ لاحق للتأكد من أن شيئاً لم يُعدَّل بعد الاعتماد.

**EN — Refusal.** We do not close a project without assembling a Proof Pack. Projects without a Proof Pack cannot be invoiced, cannot be referenced in case studies, and cannot trigger retainer eligibility.

**AR — رفض.** لا نغلق مشروعاً بدون Proof Pack. المشاريع بدون Proof Pack لا يمكن إصدار فاتورة لها، لا يمكن الاستشهاد بها في حالات، ولا تفعّل أهلية الريتينر.

Enforced by: `tests/test_proof_pack_required.py`, `auto_client_acquisition/proof_os/proof_pack.py`

---

## 11. No project without a Capital Asset — لا مشروع بلا أصل رأسمالي

**EN — Promise.** Every closed engagement deposits at least one reusable Capital Asset — a scoring rule, draft template, governance rule, sector insight, productization signal, or proof example. The next engagement starts ahead because of yours, and the cumulative ledger is reviewed weekly.

**AR — وعد.** كل ارتباط مغلق يودع أصلاً رأسمالياً واحداً على الأقل قابلاً لإعادة الاستخدام — قاعدة تسجيل، قالب مسودة، قاعدة حوكمة، insight قطاع، إشارة منتَج، أو نموذج إثبات. الارتباط القادم يبدأ متقدّماً بسبب ارتباطك، وسجل الأصول التراكمي يُراجَع أسبوعياً.

**EN — Refusal.** We do not close a project without depositing at least one Capital Asset. Zero-capital projects are flagged in the weekly capital review as a productization failure, not a delivery success.

**AR — رفض.** لا نغلق مشروعاً بدون إيداع أصل رأسمالي واحد على الأقل. مشاريع صفر-رأسمال تُرفع في مراجعة الأصول الأسبوعيّة كإخفاق في الإنتاج، لا كنجاح في التسليم.

Enforced by: `auto_client_acquisition/capital_os/capital_ledger.py`

---

## Verify yourself — تحقق بنفسك

The page above is generated from the same Python module the CI tests read. Three public endpoints let any reviewer confirm the manifesto, the audit chain, and the trust pack without contacting Dealix:

```bash
# 1. The 11 commitments as machine-readable JSON
curl https://api.dealix.me/api/v1/dealix-promise | jq .commitments

# 2. The audit chain for a recent action (replace ACTION_ID)
curl https://api.dealix.me/api/v1/audit-chain/ACTION_ID | jq .

# 3. The trust pack for a published engagement (replace PACK_ID)
curl https://api.dealix.me/api/v1/trust-pack/PACK_ID | jq .
```

كل نقطة نهاية أعلاه عامّة وتُرجع JSON. لا حاجة لمفتاح API لقراءة المانيفستو. سلسلة التدقيق وحزمة الثقة تتطلبان معرّف الإجراء أو الحزمة الذي شاركناه معك في تسليم الارتباط.

---

## Cross-links

- Canonical text — النص المرجعي: [`docs/00_constitution/NON_NEGOTIABLES.md`](00_constitution/NON_NEGOTIABLES.md)
- Source-of-truth module — وحدة المصدر: `auto_client_acquisition/governance_os/non_negotiables.py`
- Public landing — صفحة الهبوط: [`landing/promise.html`](../landing/promise.html)
- Partner covenant — ميثاق الشركاء: [`docs/40_partners/PARTNER_COVENANT.md`](40_partners/PARTNER_COVENANT.md)

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
