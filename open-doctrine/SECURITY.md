# Security — الأمان

_How to report a security concern with the doctrine itself — for example, a control that creates a false sense of safety without enforcing the underlying commitment._

## EN — What this page is for

This page is **not** about reporting a vulnerability in the Dealix commercial implementation. The commercial product has its own reporting channel which is not covered here. This page is about the doctrine: the text, the control mapping, the checklist, the adoption guide, and the public framework that adopters are asked to read and follow.

A doctrine can fail in three ways:

1. **A control is named but unenforceable.** The text says "X is blocked" but no realistic mechanism stops X in production.
2. **A control creates a false sense of safety.** The control passes its named test but misses the real-world risk it was meant to address.
3. **A translation drifts.** The Arabic and English versions of a commitment say different things, allowing adopters to claim alignment with one while violating the other.

Reports on any of these three failure modes are in scope for this page.

## AR — ما الغرض من هذه الصفحة

هذه الصفحة **ليست** للإبلاغ عن ثغرة في تطبيق Dealix التجاري. للمنتج التجاري قناة إبلاغ مستقلّة لا تشملها هذه الصفحة. هذه الصفحة للدستور نفسه: نصه، جدول الضوابط، قائمة التبنّي، دليل التبنّي، والإطار العام الذي يُطلَب من المتبنّين قراءته واتّباعه.

يَفشل الدستور بثلاث طُرق:

1. **ضابط مُسمّى لكنه غير قابل للتنفيذ.** النص يقول "X محجوب" بلا آلية واقعية تمنع X في الإنتاج.
2. **ضابط يصنع إحساساً زائفاً بالأمان.** يجتاز الضابط اختباره الاسمي لكنه يُهمل الخطر الواقعي.
3. **انحراف في الترجمة.** العربية والإنجليزية تقولان أشياء مختلفة، فيدّعي المتبنّي توافقاً مع نسخة دون أخرى.

البلاغات على أيٍّ من هذه الإخفاقات الثلاثة داخل نطاق هذه الصفحة.

---

## Reporting channel — قناة الإبلاغ

**Send the report to:** `security@dealix.me`

(This address is a placeholder pending the open-source release. The founder will confirm the active address before this document is published externally. Adopters reading the doctrine before the active address is confirmed should open a private issue on the GitHub repository instead.)

**Include in the report:**

- A short title describing the doctrine concern.
- The specific commitment, control, checklist item, or paragraph the report addresses.
- The failure mode (unenforceable, false sense of safety, translation drift, or other).
- A concrete example showing the failure — a realistic adoption scenario where following the doctrine literally leaves the adopter exposed.
- A proposed remediation if the reporter has one. (Optional.)
- The reporter's name or handle and a preferred contact method for follow-up.

**أرسل البلاغ إلى:** `security@dealix.me` (عنوان مؤقّت إلى حين تأكيد الإصدار العلني).

**يجب أن يحتوي البلاغ على:** عنوان مختصر، والالتزام أو الضابط المعني، ونوع الإخفاق (غير قابل للتنفيذ، إحساس زائف بالأمان، انحراف ترجمة، أو غيرها)، ومثال واقعي يُظهر الإخفاق، ومعالجة مقترحة إن وُجدت، واسم المُبلِّغ وطريقة تواصل مفضّلة.

---

## Response SLA — مدة الاستجابة

**EN.** The Dealix maintainer commits to a **best-effort** acknowledgement within **7 calendar days** of receipt. "Best-effort" is the operative phrase: the doctrine itself states that estimated outcomes are not guaranteed outcomes, and the response SLA is no exception. There is no contractual guarantee of response time, and there is no bug-bounty program in this MVP. Reporters who require a contractual SLA should engage the commercial-review channel described in [`ADOPTION_GUIDE.md`](./ADOPTION_GUIDE.md) tier 4.

**AR.** تلتزم الجهة المُشرفة من Dealix بإقرار **بأفضل جهد** خلال **٧ أيام** من الاستلام. "بأفضل جهد" هو المفتاح: ينصّ الدستور أن النتائج التقديرية ليست نتائج مضمونة، ومدة الاستجابة ليست استثناءً. لا التزام تعاقدي بمدة الاستجابة، ولا برنامج مكافآت ثغرات في المرحلة الأولى. المُبلِّغون الذين يحتاجون SLA تعاقدياً يستخدمون قناة المراجعة التجارية في المرحلة الرابعة من دليل التبنّي.

---

## What happens after a valid report — ما بعد البلاغ

1. **Acknowledgement** — the maintainer confirms receipt and assigns a tracking identifier.
2. **Triage** — the maintainer classifies the failure mode and decides whether it warrants a doctrine amendment, a translation fix, a control-mapping update, or no change.
3. **Remediation** — if the report is accepted, a Pull Request is opened against this repository with the proposed fix. The reporter is credited in `CONTRIBUTORS.md` unless they request anonymity.
4. **Public note** — if the failure mode affected adopters' decisions, a short public note is added to the repository changelog naming the doctrine version that introduced and fixed the issue.

تأكيد الاستلام، ثم التصنيف، ثم المعالجة (PR على المستودع)، ثم ملاحظة عامة في سجل التغييرات إذا كان الإخفاق قد أثّر على قرارات المتبنّين.

---

## What is out of scope — ما هو خارج النطاق

- Vulnerabilities in the Dealix commercial product (separate channel).
- Disagreement on doctrine direction (use [`CONTRIBUTING.md`](./CONTRIBUTING.md) instead).
- Adopter-specific implementation bugs in the adopter's own codebase.
- General security questions; the doctrine is a governance framework, not a security training resource.

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
