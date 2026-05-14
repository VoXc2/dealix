# GCC Governed AI Ops Standard — معيار العمليات المحوكمة لذكاء الخليج

> الـ ١١ غير قابل للتفاوض كمعيار تشغيلي لذكاء اصطناعي تجاري في الخليج. مرجع مفتوح: `/api/v1/doctrine`.

## ١. السياق التنظيمي الخليجي — بالعربية

دول الخليج تعيش لحظة تَكوّن لطبقة الحوكمة:

- **الإمارات** تملك استراتيجية AI 2031 وصندوق MGX؛ التنظيم يتبلور في ADGM و DIFC.
- **السعودية** تملك HUMAIN ورؤية ٢٠٣٠، مع PDPL و NDMO كمرجع PII، و SDAIA كمرجع نموذجي.
- **قطر/البحرين/الكويت/عُمان** أعلنت استراتيجيات AI وطنية، لكن التنظيم التشغيلي ما زال ليناً: الإطار موجود، آلية الإنفاذ غير ناضجة.

النتيجة: فجوة تشغيلية. القوانين تَصِف "ماذا"، لا تَصِف "كيف". Dealix Doctrine يملأ "الكيف": كيف تُصدر مسودة AI مرتبطة بمصدر، كيف تَخزن سجلّاً قابلاً للتدقيق، كيف تَطلب موافقة بشرية قبل فعل خارجي، كيف تَجمّع Proof Pack.

## ٢. الـ ١١ التزاماً كمعيار

| المعرف | العنوان | ما يضمنه تشغيلياً |
|---|---|---|
| `no_scraping` | لا تجريف بيانات | كل جهة اتصال لها Source Passport |
| `no_cold_whatsapp` | لا واتساب بارد | كل إرسال مرتبط بموافقة مسبقة موثّقة |
| `no_linkedin_automation` | لا أتمتة LinkedIn | لا طلبات/رسائل/تجريف عبر LinkedIn |
| `no_unsourced_claims` | لا ادعاءات بلا مصدر | كل رقم/اقتباس له `source_ref` |
| `no_guaranteed_outcomes` | لا ضمانات مبيعات | لغة التزام لا لغة ضَمان |
| `no_pii_in_logs` | لا PII في السجلات | حذف عند حدّ middleware |
| `no_sourceless_ai` | لا إجابة بلا مصدر | "مصدر مطلوب" بدل اختلاق إجابة |
| `no_external_action_without_approval` | لا فعل خارجي بلا موافقة | كل إرسال/دفعة/نشر يتطلّب موافقة بشرية مسجّلة |
| `no_agent_without_identity` | لا عميل ذكي بلا هوية | كل سير عمل مرتبط بهوية مسجّلة |
| `no_project_without_proof_pack` | لا مشروع بلا Proof Pack | ١٤ قسماً موقّعاً قبل الإغلاق |
| `no_project_without_capital_asset` | لا مشروع بلا أصل رأسمالي | إيداع أصل قابل لإعادة الاستخدام |

المصدر الواحد للحقيقة: `auto_client_acquisition/governance_os/non_negotiables.py`.

## ٣. كيف يتبنّاه الشركاء

- **شركات التدقيق الكبرى (Big 4)**: تستخدم Trust Pack كمرفق في تقارير المراجعة.
- **معالجات تقنية مرخّصة**: تُدمج Source Passport في عقود معالجة البيانات.
- **استشارات AI/Cloud**: تَنشر Doctrine كطبقة حوكمة فوق منصّاتها.
- **فِرَق AI المؤسّسية**: تُطبّق Decision Passport على تدفّقاتها الداخلية.

نقطة الوصول الفنية: `GET /api/v1/doctrine` تُرجع الـ ١١ بصياغة EN + AR + ملفّات الإنفاذ.

## ٤. حدود الادّعاء

Dealix لا يدّعي اعتماد أي جهة تنظيمية خليجية للعقيدة. PDPL السعودي، UAE Federal Decree-Law No. 45 of 2021، Qatar PDPPL، Kuwait DPPR، Bahrain Law No. 30 of 2018، و Oman Royal Decree 6/2022 هي قوانين سيادية. Dealix يَخرِط التزاماته على موادها، ولا يطلب اعتماداً منها.

---

## 1. Gulf regulatory context — English

The Gulf is in a formation moment for governance:

- **UAE** has AI Strategy 2031 and MGX; regulation crystallizes inside ADGM and DIFC free zones.
- **Saudi Arabia** has HUMAIN and Vision 2030, with PDPL and NDMO as PII references and SDAIA as the model-governance reference.
- **Qatar, Bahrain, Kuwait, Oman** have announced national AI strategies, but operational regulation remains soft: the framework exists; enforcement machinery is not mature.

The result is an operational gap. Statutes describe "what". They do not describe "how". The Dealix Doctrine fills the "how": how to issue an AI draft bound to a source, how to keep an auditable record, how to require human approval before any external action, how to assemble a Proof Pack.

## 2. The 11 commitments as a standard

| ID | Title | What it enforces operationally |
|---|---|---|
| `no_scraping` | No scraping | Every contact has a Source Passport |
| `no_cold_whatsapp` | No cold WhatsApp | Every send tied to prior recorded consent |
| `no_linkedin_automation` | No LinkedIn automation | No automated requests / messages / scraping |
| `no_unsourced_claims` | No un-sourced claims | Every number/quote carries `source_ref` |
| `no_guaranteed_outcomes` | No guaranteed sales | Commitment language, not guarantee language |
| `no_pii_in_logs` | No PII in logs | Redacted at middleware boundary |
| `no_sourceless_ai` | No source-less answers | "Source required" instead of invention |
| `no_external_action_without_approval` | No external action without approval | Every send/charge/publish requires recorded human approval |
| `no_agent_without_identity` | No agent without identity | Every workflow tied to a registered agent |
| `no_project_without_proof_pack` | No project without a Proof Pack | 14-section signed pack before close |
| `no_project_without_capital_asset` | No project without a Capital Asset | Reusable asset deposited |

Single source of truth: `auto_client_acquisition/governance_os/non_negotiables.py`.

## 3. Adoption path for partners

- **Big 4 / assurance**: attach the Trust Pack to audit reports.
- **Licensed technology processors**: embed Source Passport in data-processing contracts.
- **AI / Cloud consultancies**: deploy the Doctrine as a governance layer above their platforms.
- **Enterprise AI teams**: apply the Decision Passport to internal flows.

Technical entry point: `GET /api/v1/doctrine` returns the 11 with EN + AR text and enforcement file paths.

## 4. Claim boundary

Dealix does not claim regulatory endorsement of the Doctrine by any Gulf authority. Saudi PDPL, UAE Federal Decree-Law No. 45 of 2021, Qatar PDPPL, Kuwait DPPR, Bahrain Law No. 30 of 2018, and Oman Royal Decree 6/2022 are sovereign statutes. Dealix maps its commitments to their articles; it does not seek their endorsement.

The Doctrine is a reference implementation. Dealix is its first deployment. Other implementations are welcome under the same 11 commitments. Endorsement is reserved for sovereign regulators.

---

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
