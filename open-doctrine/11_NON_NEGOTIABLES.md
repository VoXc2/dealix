# The 11 Non-Negotiables — الالتزامات الإحدى عشرة

_The 5-minute reference. For full canonical text see [`GOVERNED_AI_OPS_DOCTRINE.md`](./GOVERNED_AI_OPS_DOCTRINE.md). For machine-readable form see `/api/v1/doctrine/controls`._

## EN — How to read this page

Eleven rules. Each rule has: a one-line English statement, a parallel Arabic statement, a one-line rationale (why the rule exists), and a one-line operational mechanism (what stops the violation in production). If a team cannot answer "what stops this in production" with a mechanism — not a policy — the rule is not in force.

## AR — كيف تقرأ هذه الصفحة

أحد عشر التزاماً. كل التزام: عبارة إنجليزية، وعبارة عربية مقابلة، وسطر مبرر، وسطر آلية تشغيلية. إن لم يُجب الفريق على "ما الذي يمنع المخالفة في الإنتاج" بآلية لا بسياسة، فالقاعدة ليست نافذة.

---

### 1. No scraping — لا تجريف بيانات

- **EN:** No scraping of websites, social platforms, or third-party UIs to harvest contacts or content.
- **AR:** لا تجريف للمواقع أو منصات التواصل أو الواجهات الخارجية لجمع جهات الاتصال أو المحتوى.
- **Rationale:** Scraped data has no consent chain; using it pollutes every downstream proof artifact.
- **Mechanism:** Source-binding test at the data-ingestion boundary; unsourced records are quarantined.

### 2. No cold WhatsApp — لا واتساب بارد

- **EN:** No WhatsApp messages to recipients without explicit, recorded, opt-in consent tied to a Source Passport.
- **AR:** لا إرسال واتساب لمستقبلين دون موافقة صريحة موثّقة مرتبطة بـ Source Passport.
- **Rationale:** Cold WhatsApp is a regulatory liability and a relationship liability.
- **Mechanism:** Channel-policy gate at the send layer; cold sends produce a blocked governance event.

### 3. No LinkedIn automation — لا أتمتة LinkedIn

- **EN:** No automation of LinkedIn connection requests, messages, scraping, or feed actions.
- **AR:** لا أتمتة لطلبات الاتصال أو الرسائل أو تجريف البيانات أو إجراءات الواجهة على LinkedIn.
- **Rationale:** Platform-policy violation creates account loss and breaks the chain of consent.
- **Mechanism:** Channel-policy gate rejects LinkedIn automation at PR review and at runtime.

### 4. No fake or un-sourced claims — لا ادعاءات بلا مصدر

- **EN:** No publication of a number, quote, case study, or proof artifact without a `source_ref` and a Source Passport.
- **AR:** لا نشر لرقم أو اقتباس أو دراسة حالة أو إثبات دون `source_ref` و Source Passport.
- **Rationale:** Un-sourced claims survive only until the first audit; the cost of the audit is the cost of the firm.
- **Mechanism:** Claim-review gate downgrades sourceless content to `draft_only` and blocks public proof.

### 5. No guaranteed sales outcomes — لا ضمانات مبيعات

- **EN:** No promise of a fixed revenue, deal count, or conversion rate. The doctrine itself states: estimated outcomes are not guaranteed outcomes.
- **AR:** لا وعد بإيراد ثابت أو عدد صفقات أو معدّل تحويل. النتائج التقديرية ليست نتائج مضمونة.
- **Rationale:** Outcome language that misrepresents probability is a deceptive-marketing risk and an internal-culture risk.
- **Mechanism:** Customer-safe-language redaction middleware rewrites or rejects outcome-promise phrasing.

### 6. No PII in logs — لا PII في السجلات

- **EN:** No raw personal data (names, phone numbers, national IDs, emails, addresses) written to application logs, friction logs, or telemetry.
- **AR:** لا بيانات شخصية خام في سجلات التطبيق أو سجلات الاحتكاك أو القياسات.
- **Rationale:** A log leak is the most common PDPL breach vector; redact before, not after.
- **Mechanism:** Redaction middleware on every log path; leaks are P0 incidents.

### 7. No source-less knowledge answers — لا إجابة بلا مصدر

- **EN:** No AI answer to a business question without a Source Passport. If no source exists, return "source required".
- **AR:** لا إجابة AI لسؤال يخصّ العمل دون Source Passport. عند الغياب تُعاد "مصدر مطلوب".
- **Rationale:** An AI that invents to look helpful is an AI that erases the audit chain.
- **Mechanism:** Source-binding gate at the AI router; the call is blocked if no source is bound.

### 8. No external action without approval — لا فعل خارجي بلا موافقة

- **EN:** No external send, charge, publish, or share without a logged human approval (approver identity + timestamp).
- **AR:** لا إرسال أو دفعة أو نشر أو مشاركة خارجية دون موافقة بشرية موثّقة (هوية + وقت).
- **Rationale:** External actions are the only actions a customer or regulator can see; they need a human approver.
- **Mechanism:** Approval-gate test on every external surface; bypass returns `REQUIRE_APPROVAL` or `BLOCK`.

### 9. No agent without identity — لا عميل ذكي بلا هوية

- **EN:** No autonomous workflow without a registered agent identity (name, version, owner, governance scope).
- **AR:** لا سير عمل ذاتي دون هوية عميل ذكي مسجّلة (الاسم، الإصدار، المالك، النطاق).
- **Rationale:** "An AI did it" is not an audit answer; an identity is.
- **Mechanism:** Agent-identity test at the registry; unregistered agents are rejected at workflow start.

### 10. No project without a Proof Pack — لا مشروع بلا Proof Pack

- **EN:** No engagement closes without a 14-section Proof Pack and a computed proof score, delivered as a signed PDF.
- **AR:** لا إغلاق لارتباط دون Proof Pack من ١٤ قسماً ونقاط إثبات محسوبة، يُسلَّم PDF موقّعاً.
- **Rationale:** Without a Proof Pack the engagement is a memory, not an asset; memories do not compound.
- **Mechanism:** Proof-pack test gates invoice eligibility; no Proof Pack means no closure.

### 11. No project without a Capital Asset — لا مشروع بلا أصل رأسمالي

- **EN:** No engagement closes without depositing at least one reusable artifact (rule, template, insight, signal, or example).
- **AR:** لا إغلاق لارتباط دون إيداع أصل قابل لإعادة الاستخدام (قاعدة، قالب، insight، إشارة، أو نموذج).
- **Rationale:** Without a deposit, every engagement starts from zero; the firm has no capital, only labor.
- **Mechanism:** Reusable-artifact-ledger test gates closure; zero-artifact projects are flagged as productization failures.

---

## Cross-link — روابط

- Canonical text → [`GOVERNED_AI_OPS_DOCTRINE.md`](./GOVERNED_AI_OPS_DOCTRINE.md)
- Control mapping → [`CONTROL_MAPPING.md`](./CONTROL_MAPPING.md)
- Adoption checklist → [`IMPLEMENTATION_CHECKLIST.md`](./IMPLEMENTATION_CHECKLIST.md)
- Machine-readable → `/api/v1/doctrine/controls`

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
