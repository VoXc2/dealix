# مكدّس الخندق — Dealix Moat Stack
## خمس طبقات لا تَنسخها ربع سنة من الكود — Five layers a quarter of code does not clone

---

## ١. الفرضية · The premise

**AR.** الموديل ليس خندقاً. مزوّدو الموديلات يَنشرون قدرات قابلة للاستنساخ شهرياً. الخندق الفعلي لـ Dealix يَتراكم في خمس طبقات تَتطلّب ثقافة تسليم، لا سطراً من الكود فقط. مَن يَنسخ السطور بلا الثقافة، يَحصل على نَصّ.

**EN.** The model is not the moat. Model vendors release cloneable capabilities monthly. The actual Dealix moat compounds across five layers that require a delivery culture, not lines of code alone. Cloning the text without the culture yields words.

---

## ٢. الطبقة الأولى — العقيدة · Layer 1 — Doctrine

**AR.** ١١ التزاماً غير قابلة للتفاوض، كل التزام مرتبط باختبار CI يُسقط البناء عند الإخلال. هذه الالتزامات معلنة في [`docs/THE_DEALIX_PROMISE.md`](../THE_DEALIX_PROMISE.md) وقابلة للتحقق عَبْر `GET /api/v1/dealix-promise`. أمثلة قابلة للتحقق:

- لا تجريف — `tests/test_no_scraping_engine.py`.
- لا واتساب بارد — `tests/test_no_cold_whatsapp.py`.
- لا أتمتة LinkedIn — `tests/test_no_linkedin_automation.py`.
- لا ادعاء بلا مصدر — `tests/test_no_guaranteed_claims.py`.

ما لا يُنسَخ هنا: ثقافة تَسقُط فيها مَطالب التسليم عند إخلال الالتزام، لا تَسقُط أمامها الالتزامات.

**EN.** Eleven non-negotiables, each backed by a CI test that fails the build on violation. Public at `GET /api/v1/dealix-promise`. Cloning the text is trivial; cloning a culture in which a delivery deadline yields to a violated commitment — not the other way around — is not. CAP-001, CAP-002, CAP-003.

---

## ٣. الطبقة الثانية — الإثبات · Layer 2 — Proof

**AR.** لكل ارتباط مُغلَق:

- **Proof Pack** بـ ١٤ قسماً مع نقاط إثبات محسوبة — `auto_client_acquisition/proof_os/proof_pack.py` (CAP-006).
- **Trust Pack PDF** بـ ١١ قسماً للمراجع التنظيمي — `auto_client_acquisition/trust_os/trust_pack.py` (CAP-007).
- **سلسلة تدقيق + Evidence Graph** — `auto_client_acquisition/auditability_os/audit_event.py` + `evidence_control_plane_os/evidence_graph.py` (CAP-008).

الإثبات مُمَنهَج، لا ارتجاليّ. تَبنّيه يَتطلّب ١٢–١٨ شهراً من تشغيل ارتباطات حقيقية يَمكِن مقابلتها بسلسلة التدقيق.

**EN.** Every closed engagement produces a 14-section Proof Pack (CAP-006), an 11-section Trust Pack PDF (CAP-007), and a cryptographic-quality audit chain plus evidence graph (CAP-008). Proof is systematic, not improvised. Replicating it requires 12–18 months of real engagements that can be replayed against the audit chain. Source files cited in `auto_client_acquisition/capital_os/capital_asset_registry.py`.

---

## ٤. الطبقة الثالثة — المنتج · Layer 3 — Product

**AR.** سلّم تجاري ثلاثي + لوحة قيادة المؤسس:

| العنصر | المصدر | الحالة |
|---|---|---|
| سلّم ٣ عروض (CAP-004) | `auto_client_acquisition/service_catalog/registry.py` | حي، مُختبَر |
| Commercial Map API (CAP-005) | `api/routers/commercial_map.py` | حي، مُختبَر |
| Founder Command Center (CAP-014) | `api/routers/founder_command_center.py` | حي، مُختبَر |

السلّم ليس قائمة أسعار، بل بنية قرار. كل درجة تُؤدّي إلى الدرجة التالية بقاعدة تأهّل صريحة (`retainer-readiness gate`).

**EN.** Three-rung commercial ladder (CAP-004) plus Founder Command Center (CAP-014). The ladder is a decision structure, not a price list. Each rung qualifies into the next via an explicit gate. Replicating the ladder shape is easy; replicating the disciplined "no engagement without a Capital Asset, no engagement without a Proof Pack" enforcement is not.

---

## ٥. الطبقة الرابعة — التجاري · Layer 4 — Commercial

**AR.** قناة الشركاء + Partner Covenant + Anchor Partner Outreach Kit (CAP-009):

- ثلاث أنماط شركاء معرَّفة: Big 4 خليجي، معالج مرخَّص من SAMA، VC سعودي.
- ميثاق شركاء صريح في [`docs/40_partners/PARTNER_COVENANT.md`](../40_partners/PARTNER_COVENANT.md).
- نموذج رِبْحٍ تشاركي موثَّق في `scripts/seed_anchor_partner_pipeline.py`.

التوسّع بقيادة الشركاء يُحوّل تكلفة الاكتساب من مَصْروف تسويق إلى عَلاقة تجاريّة طويلة الأمد.

**EN.** Partner-led channel via the Anchor Partner Outreach Kit (CAP-009): three partner archetypes defined, an explicit Partner Covenant, and a documented rev-share template. Partner-led expansion converts acquisition cost from a marketing expense to a long-term commercial relationship. Replicating a partner network takes years of trust, not a quarter of code.

---

## ٦. الطبقة الخامسة — الرأسمال · Layer 5 — Capital

**AR.** Capital Asset Library: كل ارتباط مُغلَق يُودِع أصلاً واحداً على الأقل في السجل العام. الأصول CAP-001…CAP-015 مُسجَّلون في `auto_client_acquisition/capital_os/capital_asset_registry.py` ومُفعَّلون عَبْر `GET /api/v1/capital-assets/public`. أمثلة:

- CAP-001 — Dealix Promise API (مُختبَر، عام).
- CAP-003 — Open Doctrine (عام، مرجع علَني).
- CAP-006 — Proof Pack Assembler (مُختبَر، داخلي).
- CAP-012 — GCC Standardization Pack (مُختبَر، عام).

الأصول تَتراكم. الارتباط رقم ١٠ يَبدأ متقدّماً على رقم ٩، ورقم ٢٠ يَبدأ متقدّماً على رقم ١٩. هذا تَركيب لا يُنسَخ ربع سنة.

**EN.** Capital Asset Library: every closed engagement deposits at least one asset into the registry. CAP-001 through CAP-015 are registered and exposed via `GET /api/v1/capital-assets/public`. Engagements compound: engagement #10 starts ahead of #9, #20 ahead of #19. This compounding is not cloneable in a quarter. See [`docs/funding/CAPITAL_ASSET_TRACTION.md`](./CAPITAL_ASSET_TRACTION.md).

---

## ٧. مَن يَنسخ ماذا · What competitors can clone

**AR.** يَستطيع مُنافس نسخ:

- نَصّ ١١ التزاماً (إنه عَلَني).
- صورة سلّم ٣ عروض (إنه عَلَني).
- إطار العقيدة المفتوحة (إنه مفتوح).

لا يَستطيع نسخ:

- ثقافة تَسقُط فيها مَطالب التسليم لا الالتزامات.
- ١٢–١٨ شهراً من ارتباطات قابلة لإعادة التشغيل عَبْر سلسلة التدقيق.
- شبكة شركاء مَبنيّة على ميثاق صريح.
- مكتبة أصول رأسمالية مُتراكمة من ارتباطات حقيقية.

**EN.** Clonable: the 11 commitments (they are public), the 3-offer ladder shape (it is public), the Open Doctrine framework (it is open). Not clonable: the delivery culture in which deadlines bend before commitments do; 12–18 months of audit-replay-able engagements; a partner network built on an explicit covenant; a capital asset library compounded from real work. The first three are content; the second four are time and posture.

---

## ٨. سيناريو "ماذا لو نَسخت Big 4" · "What if a Big 4 clones it"

**AR.** سؤال يَتكرّر، الإجابة في [`docs/funding/INVESTOR_QA.md`](./INVESTOR_QA.md). الإجابة المختصرة: Big 4 لا تَبني منصة، تَبني تقريراً. لو حاولت بناء منصة، تَدخل في تعارض مع نموذج عَملها الاستشاري بالساعة.

**EN.** Frequent question. Short answer in [`docs/funding/INVESTOR_QA.md`](./INVESTOR_QA.md): Big 4 firms ship reports, not platforms. A platform competes with billable hours. Detailed answer cites a specific code surface in the QA doc.

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
