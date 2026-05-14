# رخصة Dealix OS — Governed AI Ops Framework
## فَتح مَصدر العَقيدة · Open-sourcing the doctrine

> **Audience / الجمهور:** Saudi VC, anchor partners, the next AI ops shop in the region, and any CISO doing supply-chain diligence.
> صناديق رأس المال السعودي، الشركاء المرتكزون، أي شركة عَمليّات ذكاء اصطناعي قادمة في المِنطقة، وأي CISO يُجري فَحص سلسلة التَوريد.
> **Status / الحالة:** Positioning doctrine. Final license selection (Apache 2.0 vs MIT) deferred to counsel.
> وثيقة تَموضع. اختيار الرخصة النهائي (Apache 2.0 مُقابل MIT) مُحال إلى المُستشار القانوني.

---

## ١. لماذا نَفتح مَصدر العَقيدة · Why open-source the doctrine

### العربية

السؤال البَديهي: إذا كانت العَقيدة هي الخَندق، أَلا يَضيع الخَندق إذا فَتحناها؟ الجواب: لا. الخَندق ليس النَصّ — الخَندق هو الالتزام العَلَني المَفروض بـ CI. النَصّ يُنشَر بَالفِعل في `docs/00_constitution/NON_NEGOTIABLES.md` وعلى نقطة النِهاية العامّة `/api/v1/dealix-promise/markdown`. الفَتح الرَسمي تَحت رخصة مَفتوحة لا يُغيِّر سَطرًا في تَعرُّضنا — لكنه يُغيِّر مَوقعنا.

عندما تَتبنّى شركة عَمليّات أُخرى في الرياض / دبي / الدوحة / الكويت "Dealix OS — Governed AI Ops Framework" كَطَبَقَة حَوكَمَتِها، تَصبح كل عَمليّة تَسليم لها تَأييدًا ضِمنيًّا لمنهج ديلكس. ديلكس يَفوز بِكَونه التَطبيق المَرجعي — لا أَسرع تَطبيق، ليس أَرخصه، بل المَرجعي. هذا مَركز سوق لا يَنتقل بسهولة.

ثانيًا: المَعركة التَنظيميّة في المِنطقة لن يَفوز بها مَن يَملك العَقيدة، بل مَن يَكتب اللُّغة المُشتَركة. مَن يَكتب اللُّغة يَتحدَّث في غُرَف NDMO / UAE Data Office / NCSA / CITRA باعتباره مَرجِعًا، لا بائعًا.

### English

The intuitive objection: if doctrine is the moat, doesn't opening it lose the moat? The answer is no. The moat is not the text — the moat is the public commitment enforced by CI. The text is already published in `docs/00_constitution/NON_NEGOTIABLES.md` and at the public endpoint `/api/v1/dealix-promise/markdown`. Formal release under an open license does not change a line of our exposure — it changes our position.

When another ops shop in Riyadh / Dubai / Doha / Kuwait adopts "Dealix OS — Governed AI Ops Framework" as its governance layer, every delivery they ship becomes implicit endorsement of the Dealix approach. Dealix wins by being the reference implementation — not the fastest, not the cheapest, but the canonical one. That is a market position that does not move easily.

Second order: the regional regulatory conversation will be won not by whoever owns the doctrine, but by whoever writes the common vocabulary. Whoever writes the vocabulary sits in NDMO / UAE Data Office / NCSA / CITRA rooms as a reference, not a vendor.

---

## ٢. ما في Dealix OS · What's in Dealix OS

### العربية

النِطاق الدَقيق لما يُنشَر تَحت الرخصة المَفتوحة:

- **البُنود الـ ١١ غير القابلة للتَفاوض** — النص القانوني من `docs/00_constitution/NON_NEGOTIABLES.md` ومرآته البَرمجيّة `auto_client_acquisition/governance_os/non_negotiables.py`. ١١ مُدخَل دَقيقًا: `no_scraping`, `no_cold_whatsapp`, `no_linkedin_automation`, `no_unsourced_claims`, `no_guaranteed_outcomes`, `no_pii_in_logs`, `no_sourceless_ai`, `no_external_action_without_approval`, `no_agent_without_identity`, `no_project_without_proof_pack`, `no_project_without_capital_asset`.
- **اختبارات حِراسة العَقيدة** — `tests/test_no_scraping_engine.py`, `tests/test_no_cold_whatsapp.py`, `tests/test_no_linkedin_automation.py`, `tests/test_no_guaranteed_claims.py`, `tests/test_no_source_passport_no_ai.py`, `tests/test_pii_external_requires_approval.py`, `tests/test_proof_pack_required.py`. هذه الاختبارات هي الالتزام العَلَني المَنفُوذ. مَن يَنسخ النَص دون الاختبارات لا يَنسخ العَقيدة.
- **وحدة `governance_os/`** — Decision envelope (`decide(action, context)`), channel policy، claim safety، Source Passport schema. مُحايد للقِطاع، قابل للنَشر لأي شركة عَمليّات تَتبنّى الإطار.
- **هَيكل سِلسِلَة التَدقيق (audit chain skeleton)** — مَخطّط الـ JSON envelope مع `agent_identity` و `approver_id` و `decision` و `source_ref` و `timestamp`. بدون المُحرّك الذي يُشغِّله، لكن مع المَخطَّط الكامل.

### English

Precise scope of what is released under the open license:

- **The 11 non-negotiables** — the canonical text from `docs/00_constitution/NON_NEGOTIABLES.md` and its code mirror `auto_client_acquisition/governance_os/non_negotiables.py`. Exactly 11 entries: `no_scraping`, `no_cold_whatsapp`, `no_linkedin_automation`, `no_unsourced_claims`, `no_guaranteed_outcomes`, `no_pii_in_logs`, `no_sourceless_ai`, `no_external_action_without_approval`, `no_agent_without_identity`, `no_project_without_proof_pack`, `no_project_without_capital_asset`.
- **The doctrine guard tests** — `tests/test_no_scraping_engine.py`, `tests/test_no_cold_whatsapp.py`, `tests/test_no_linkedin_automation.py`, `tests/test_no_guaranteed_claims.py`, `tests/test_no_source_passport_no_ai.py`, `tests/test_pii_external_requires_approval.py`, `tests/test_proof_pack_required.py`. These tests ARE the public commitment in enforced form. Copying the text without the tests is not copying the doctrine.
- **The `governance_os/` module** — decision envelope (`decide(action, context)`), channel policy, claim safety, Source Passport schema. Sector-neutral, deployable by any ops shop adopting the framework.
- **Audit chain skeleton** — JSON envelope schema with `agent_identity`, `approver_id`, `decision`, `source_ref`, `timestamp`. Without the engine that runs it, but with the full schema.

---

## ٣. ما ليس في Dealix OS · What's NOT in Dealix OS

### العربية

المُحيط مَفتوح؛ المُحرِّك داخل المُحيط مَملوك. التَالي يَبقى مُغلَقًا:

- **سُلَّم العُروض** (`auto_client_acquisition/service_catalog/registry.py`) — الـ ٣ عُروض، السِعر، الـ KPIs، الـ refund policy.
- **مُنسِّق السبرنت** (Sprint orchestrator) — مَنطق الـ ٣٠ يومًا، تَسلسل المَهام، مَنطق Capital Asset.
- **مُجمِّع Proof Pack** (proof-pack assembler) — مَنطق احتساب نَقاط الإثبات، قَوالب الأَقسام الـ ١٤.
- **مُولِّد Trust Pack PDF** — التَصميم، الخَطّ العربي، تَوقيع PDF.
- **بَوّابة العَميل** (customer portal) — UI، تَدفُّق المُوافَقة، إدارة الجَلسات.
- **مُسجِّل التَأهيل** (qualification scorer) — الأَوزان المُحَدَّدة لمَيدان السوق السعودي، الفِئات، عَتَبَة `retainer_ready`.
- **كُتُب اللَّعب الخاصة بالتَسليم** (delivery playbooks) — `docs/ops/*` الكامل.

### English

The perimeter is open; the engine inside the perimeter is proprietary. The following stays closed:

- **The service catalog** (`auto_client_acquisition/service_catalog/registry.py`) — the 3 offerings, pricing, KPIs, refund policy.
- **The Sprint orchestrator** — the 30-day logic, task sequencing, Capital Asset gating.
- **The Proof Pack assembler** — proof-score computation, the 14-section templates.
- **The Trust Pack PDF renderer** — layout, Arabic typography, PDF signing.
- **The customer portal** — UI, approval flow, session management.
- **The qualification scorer** — Saudi-market-specific weights, tiers, the `retainer_ready` threshold.
- **The delivery playbooks** — the full `docs/ops/*` set.

The OS is the perimeter; the engine inside is what we sell.

---

## ٤. اختيار الرخصة · License choice

### العربية + English

**Recommended default: Apache License 2.0.** The Apache 2.0 patent grant matters in the AI era: it gives downstream adopters explicit protection against patent claims by contributors. With AI patent troll activity intensifying in the GCC tech corridor, the Apache patent clause is real risk mitigation for everyone who adopts Dealix OS.

**Acceptable alternative: MIT.** MIT maximizes adoption velocity (shortest, most permissive, no patent clause to read). If counsel determines the patent grant is unnecessary or creates downstream complications, MIT is the fallback.

**Final call: founder's lawyer.** No public release until counsel has reviewed:
- Apache 2.0 vs MIT against Saudi software-protection norms.
- Compatibility with any open-source dependencies in `governance_os/`.
- Trademark posture for "Dealix" and "Dealix OS" as separate marks (the framework is open, the brand is not).

التَوصية: Apache 2.0 بسبب مَنحَة بَراءَة الاختراع — مُهمَّة في عَصر الذكاء الاصطناعي. البَديل المَقبول: MIT لِسرعة التَبنّي. القرار النهائي للمُحامي.

---

## ٥. مَراجع + تَحقُّق · Cross-links + verify

### العربية + English

A public `/api/v1/license` endpoint will surface the chosen license terms in the same way `/api/v1/dealix-promise/markdown` surfaces the doctrine today. Public GitHub repo to be created at `github.com/dealix/governed-ai-ops-framework` once the founder commits the release. The repo will contain only the perimeter described in section ٢ — proprietary modules stay in the private monorepo.

نقطة نِهاية عامّة `/api/v1/license` تَكشف الرُّخصة المُختارة كَما تَكشف `/api/v1/dealix-promise/markdown` العَقيدة اليوم. مُستودَع GitHub عام يُنشأ على `github.com/dealix/governed-ai-ops-framework` عندما يَلتزم المؤسس بالإصدار.

Cross-links:
- `docs/THE_DEALIX_PROMISE.md` — canonical bilingual manifesto.
- `docs/00_constitution/NON_NEGOTIABLES.md` — the 11 entries (text source of truth).
- `auto_client_acquisition/governance_os/non_negotiables.py` — code mirror.
- `auto_client_acquisition/governance_os/gcc_markets.py` — regional surface the OS is designed for.
- `docs/strategic/GCC_EXPANSION_STRATEGY.md` — how the OS positions Dealix regionally.

---

> **Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**
