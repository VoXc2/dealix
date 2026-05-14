# Governed AI Operations Doctrine — دستور تشغيل AI المحوكم

_Version 0.1.0 · Maintained by Dealix · Doctrine: CC BY 4.0 · Code examples: MIT_

## EN — Opener

The **Governed AI Operations Doctrine** is an open framework for teams building responsible, evidence-backed AI operations. It is designed for AI consultancies, enterprise AI teams, regulated operators, GCC + MENA digital transformation teams, and founders building AI-enabled services. The doctrine names eleven non-negotiables — the rules that distinguish governed AI operations from "AI tools" or "lead-gen". Each rule pairs a promise with a refusal, a control with an evidence artifact, and a test category any adopter can implement in their own codebase. The framework is open. The Dealix commercial implementation is not.

## AR — افتتاحية

**دستور تشغيل AI المحوكم** هو إطار مفتوح للفِرق التي تبني عمليات ذكاء اصطناعي مسؤولة ومستندة إلى الأدلة. صُمِّم لاستشاريي AI، وفِرق AI المؤسسية، والمشغّلين الخاضعين للتنظيم، وفِرق التحول الرقمي في الخليج والشرق الأوسط، والمؤسسين الذين يبنون خدمات قائمة على AI. يحدّد الدستور أحد عشر التزاماً غير قابل للتفاوض — القواعد التي تميّز عمليات AI المحوكمة عن "أدوات AI" أو "توليد العملاء". كل قاعدة تَقرن وعداً برفض، وضابطاً بأثر يُثبت الامتثال، وفئة اختبار يستطيع أي متبنٍّ تطبيقها على قاعدته البرمجية. الإطار مفتوح. أما تطبيق Dealix التجاري فليس كذلك.

---

## What this repository IS — ما هذا المستودع

- The canonical text of the 11 commitments (EN + AR).
- The control mapping that ties each commitment to an evidence artifact and a test category.
- A 30-item adoption checklist any team can run on its own codebase.
- A four-tier adoption guide (awareness → alignment → compliance → certified-by-Dealix).
- Licensing posture, contribution rules, and a security-reporting channel for the doctrine itself.

النص المرجعي للالتزامات الإحدى عشرة، وجدول الضوابط الذي يربط كل التزام بأثر إثبات وفئة اختبار، وقائمة تبنٍّ من ٣٠ بنداً يمكن لأي فريق تطبيقها على قاعدته البرمجية، ودليل تبنٍّ بأربع مراحل، وموقف الترخيص وقواعد المساهمة وقناة الإبلاغ الأمني.

## What this repository is NOT — ما ليس عليه

This repository does **NOT** provide commercial Dealix implementation code. It does not contain Dealix's scoring engines, agent runtimes, proof-pack assembly logic, capital ledger, or any internal operating module. Adopting the doctrine does not grant access to the Dealix commercial product. It does not grant use of the "Dealix" name or logo. It is not a compliance certification, not legal advice, and not a substitute for jurisdictional law (PDPL, GDPR, NDMO, sector regulators).

هذا المستودع **لا** يوفّر شيفرة التطبيق التجاري لـ Dealix. لا يحتوي على محرّكات التسجيل، أو زمن تشغيل العملاء الأذكياء، أو منطق تجميع Proof Pack، أو دفتر الأصول الرأسمالية، أو أي وحدة تشغيل داخلية. تبنّي الدستور لا يمنح الوصول إلى منتج Dealix التجاري، ولا يمنح حق استخدام اسم "Dealix" أو شعارها. ليس شهادة امتثال، ولا رأياً قانونياً، ولا بديلاً عن القانون الواجب التطبيق (PDPL، GDPR، NDMO، الجهات القطاعية).

## How to adopt — كيف تتبنّى

1. Read `GOVERNED_AI_OPS_DOCTRINE.md` (the canonical 11 commitments).
2. Read `11_NON_NEGOTIABLES.md` (the 5-minute condensed reference).
3. Read `CONTROL_MAPPING.md` (each commitment → control → evidence → test).
4. Run `IMPLEMENTATION_CHECKLIST.md` against your own codebase.
5. Choose your tier in `ADOPTION_GUIDE.md` (awareness, alignment, compliance, or certified-by-Dealix).
6. If contributing changes, see `CONTRIBUTING.md` before opening a PR.

اقرأ الوثيقة المرجعية، ثم المرجع المختصر، ثم جدول الضوابط، ثم نفّذ قائمة التبنّي على قاعدتك البرمجية، ثم اختر مرحلتك من دليل التبنّي. للمساهمة في تطوير النص، راجع `CONTRIBUTING.md`.

## Maintainer — الجهة المُشرفة

The doctrine is maintained by **Dealix** as a public good. Dealix is the reference commercial implementation. Every change to the doctrine is reviewed against the 11 commitments. The maintainer reserves the right to reject a proposed change that would silently weaken a commitment.

تُشرف **Dealix** على الدستور كمنفعة عامة. Dealix هي التطبيق المرجعي التجاري. كل تعديل على نص الدستور يُراجَع وفق الالتزامات الإحدى عشرة. تحتفظ الجهة المُشرفة بحق رفض أي تعديل يُضعف التزاماً بصمت.

## License — الترخيص

- **Doctrine text** (every prose paragraph, table, and checklist) → **CC BY 4.0** (Creative Commons Attribution 4.0). Attribution required.
- **Code examples** (any inline code block, JSON schema, API signature) → **MIT**.
- **Trademark** → The names "Dealix", "Dealix Doctrine", "Governed AI Operations Doctrine", and the Dealix logo are **reserved**. You may state that your product follows the doctrine; you may not brand your product with the Dealix marks.

نص الدستور تحت **CC BY 4.0**؛ أمثلة الشيفرة تحت **MIT**؛ أسماء "Dealix" و"Governed AI Operations Doctrine" والشعار **محفوظة** ولا يجوز استخدامها كعلامة لمنتجاتك.

See `LICENSE.md` for full terms. لتفاصيل الترخيص الكاملة راجع `LICENSE.md`.

## Public surfaces — الواجهات العامة

The machine-readable surfaces of the doctrine:

- `/api/v1/doctrine` — JSON of the open framework + control rows.
- `/api/v1/doctrine/controls` — JSON of the control mapping only.
- `/api/v1/dealix-promise` — Dealix's commitment to its own customers (distinct from the doctrine).
- `/api/v1/capital-assets/public` — the public catalog of reusable artifacts.

These endpoints are the canonical public surface. Adopters MAY hit them; they MUST NOT depend on private endpoints.

## Security — الأمان

To report a doctrine-level security concern (e.g., a control that creates a false sense of safety), see `SECURITY.md`.

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
