# Contributing — المساهمة

_How external contributors propose changes to the Governed AI Operations Doctrine._

## EN — Posture

The doctrine is open and maintained by Dealix. Contributions are welcome on the doctrine text, the control mapping, the implementation checklist, the adoption guide, and the contributor-facing documents in this repository. Contributions to the Dealix commercial implementation are out of scope; this repository contains only the open framework.

Every proposed change is reviewed against the 11 commitments. A change that would silently weaken a commitment is rejected. A change that strengthens a commitment, clarifies an ambiguity, fixes a translation, or improves an example is welcomed.

## AR — الموقف

الدستور مفتوح وتُشرف عليه Dealix. المساهمات مرحّب بها على نص الدستور، وجدول الضوابط، وقائمة التبنّي، ودليل التبنّي، ووثائق المساهمين في هذا المستودع. المساهمات في التطبيق التجاري لـ Dealix خارج النطاق؛ هذا المستودع يحتوي على الإطار المفتوح فقط.

كل تعديل مُقترَح يُراجَع وفق الالتزامات الإحدى عشرة. التعديل الذي يُضعف التزاماً بصمت مرفوض. التعديل الذي يُقوّي التزاماً أو يوضّح غموضاً أو يُصحّح ترجمة أو يُحسّن مثالاً مُرحَّب به.

---

## How to propose a change — كيف تُقدّم تعديلاً

1. **Open a Pull Request** to the GitHub repository at the placeholder URL `github.com/dealix/governed-ai-ops-doctrine`. (Repository URL is a placeholder until the open-source release.)
2. **Reference the doctrine commitment** the change touches. If the change crosses multiple commitments, reference each.
3. **State the change rationale** in three lines or fewer. What is the current state, what should it be, and why.
4. **Provide bilingual text.** Any change to the doctrine prose requires both AR and EN. Translations may be improved in a single-language PR, but a new sentence must arrive bilingual.
5. **Run the doctrine-protection checks locally** (see `IMPLEMENTATION_CHECKLIST.md` group rules). A PR that references private Dealix-internal identifiers or implementation paths is rejected automatically.

## Review process — مسار المراجعة

- **First-pass review** by a Dealix maintainer within 7 business days, best-effort.
- **Doctrine alignment review** — does the change strengthen, neutralize, or weaken a commitment? Weakening changes are closed with reasoning.
- **Translation review** — both AR and EN are read by a bilingual reviewer; mismatched length or meaning is flagged.
- **Final approval** — a Dealix maintainer approves and merges. The contributor's name (or chosen handle) is added to `CONTRIBUTORS.md` at first merge.

## Commit rights — حقوق المساهمة المباشرة

No contributor is granted commit rights without **three** reviewed and merged PRs. Commit rights are granted at the discretion of the Dealix maintainer, are scoped to documentation files in this repository, and are revocable. The Dealix commercial implementation is never accessible through doctrine commit rights.

لا يُمنح أي مساهم حقوق commit مباشرة دون **ثلاث** مساهمات مراجَعة ومُدمَجة. حقوق الـ commit تُمنح بتقدير الجهة المُشرفة من Dealix، ومحصورة بملفات الوثائق في هذا المستودع، وقابلة للسحب. التطبيق التجاري لـ Dealix لا يُتاح أبداً عبر حقوق commit الدستور.

## Contributor Licensing — ترخيص المساهمات

**No CLA in MVP.** The first version of this repository does not require a signed Contributor License Agreement. Contributions are accepted under an **Apache 2.0-style implicit grant**: by opening a PR, the contributor grants the project and its users a non-exclusive, perpetual, worldwide, royalty-free license to use, reproduce, modify, distribute, and sublicense the contribution under the project's stated licenses (CC BY 4.0 for doctrine text, MIT for code examples). The contributor warrants they have the right to make the grant.

**لا اتفاقية CLA في المرحلة الأولى.** الإصدار الأول من المستودع لا يشترط توقيع اتفاقية ترخيص مساهم. تُقبل المساهمات وفق **منح ضمني على نمط Apache 2.0**: بفتح PR يمنح المساهم المشروع ومستخدميه ترخيصاً غير حصري ودائماً وعالمياً ومجانياً لاستخدام المساهمة ونسخها وتعديلها وتوزيعها وإعادة ترخيصها وفق ترخيص المشروع (CC BY 4.0 للنص، MIT لأمثلة الشيفرة). يضمن المساهم أن لديه الحق في منح هذا.

The maintainer reserves the right to introduce a formal CLA in a future version of this document. Contributions accepted under the implicit grant remain under that grant.

تحتفظ الجهة المُشرفة بحق إدخال CLA رسمي في إصدار لاحق من هذه الوثيقة. المساهمات المقبولة تحت المنح الضمني تبقى تحت ذلك المنح.

## What we will not accept — ما لا نقبله

- Changes that introduce a guarantee, a fixed-outcome promise, or marketing language that contradicts commitment 5.
- Changes that reference private Dealix-internal identifiers or modules; the open-doctrine repository must reference only public surfaces (`/api/v1/doctrine`, `/api/v1/dealix-promise`, `/api/v1/capital-assets/public`).
- Single-language changes to bilingual prose, unless the change is explicitly labeled as a translation improvement.
- Changes that remove a commitment. Commitments can only be replaced by stricter commitments with equal or broader enforcement coverage.

التعديلات التي تُدخل ضماناً أو وعداً بنتيجة ثابتة أو لغة تسويقية تتعارض مع الالتزام الخامس، أو تشير إلى رموز Dealix الخاصة أو الوحدات الداخلية، أو تكون أحادية اللغة في نص ثنائي، أو تحذف التزاماً — كل هذه مرفوضة.

## Code of conduct — مدوّنة السلوك

Reviewers and contributors interact in writing only. Personal attacks, harassment, and disclosure of private information are grounds for immediate PR closure and contributor block. Disagreement on doctrine substance is welcomed; disagreement on personal terms is not.

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
