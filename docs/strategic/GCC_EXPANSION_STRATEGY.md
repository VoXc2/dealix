# استراتيجية التوسّع الخليجي — GCC Expansion Strategy
## السعودية → الإمارات → قطر → الكويت · KSA → UAE → Qatar → Kuwait

> **Audience / الجمهور:** Founder, anchor partners, prospective investors.
> المؤسس، الشركاء المرتكزون، المستثمرون المحتملون.
> **Status / الحالة:** Saudi beachhead active. UAE pilot-ready post-case-study. Qatar + Kuwait gated on local entity per Article-18 cross-border data transfer requirements.
> **Source of truth / مصدر الحقيقة:** `auto_client_acquisition/governance_os/gcc_markets.py`.

---

## ١. لماذا الخليج، لماذا الآن · Why GCC, why now

### العربية

تلاقت أربعة تحوّلات تنظيمية في نافذة واحدة ضيقة. PDPL السعودي — وتحديدًا المادة ١٨ — قيّد نقل البيانات الشخصية عبر الحدود بشروط قابلة للتنفيذ. مكتب البيانات الإماراتي فعّل تطبيق المرسوم الاتحادي رقم ٤٥ لسنة ٢٠٢١. هيئة الأمن السيبراني القطرية (NCSA) رفعت متطلبات قانون حماية البيانات رقم ١٣ لسنة ٢٠١٦. CITRA الكويتية أصدرت لائحة DPPR رقم ٢٦ لسنة ٢٠٢٤ مع متطلب DPO صارم. كل ذلك على خلفية رؤية ٢٠٣٠ السعودية واستراتيجيات السيادة الرقمية الخليجية الموازية.

الفجوة الناتجة: لا يوجد مزوّد عمليات ذكاء اصطناعي إقليمي واحد يغطي البنود الأساسية في الأنظمة الأربعة بنفس العقيدة الهندسية. الأدوات الأجنبية لا تقرأ اللائحة العربية. الاستشارات الكبرى تبيع وثائق، لا عمليات. عقيدة ديلكس — ١١ بندًا غير قابلة للتفاوض مفروضة باختبارات CI — تُسقَط على كل تشريع من الأربعة بتعديل صف واحد في `gcc_markets.py`.

### English

Four regulatory shifts converged in one tight window. Saudi PDPL — specifically Article 18 — restricted cross-border personal data transfers under enforceable conditions. The UAE Data Office activated enforcement of Federal Decree-Law No. 45 of 2021. Qatar's NCSA stiffened expectations under PDPPL Law No. 13 of 2016. Kuwait's CITRA issued DPPR No. 26 of 2024 with a hard DPO requirement. Vision 2030 and parallel GCC digital-sovereignty agendas sit underneath all four.

The resulting gap: no single regional governed AI operations vendor closes the core articles in all four statutes from one engineered doctrine. Foreign tools do not read the Arabic regulation. Big advisory sells documents, not operations. The Dealix doctrine — 11 non-negotiables enforced by CI tests — maps onto each statute with a one-line edit to `gcc_markets.py`. The window is 24 months before a mature market forms.

---

## ٢. الأسواق الأربعة بترتيب الأولوية · The 4 markets in priority order

### a. المملكة العربية السعودية — Kingdom of Saudi Arabia · `dealix_status = active`

| Field · الحقل | Value · القيمة |
|---|---|
| Regulator · الجهة | NDMO + SDAIA |
| Framework · الإطار | PDPL — Royal Decree M/19 (2021), Implementing Regulation (2023) |
| Articles mapped · المواد | Article 5 (lawful basis), 13 (data subject rights), 14 (consent), 18 (data transfers), 21 (penalties) |
| Local payment · الدفع | Moyasar |
| Invoicing · الفوترة | ZATCA Phase 2 (e-invoicing) |
| Language · اللغة | Khaleeji Arabic (Saudi) primary; MSA + EN secondary |
| Activation gate · بوابة التفعيل | Live. 2026-Q2 reframe targets 50–500-employee B2B services. |

السعودية هي رأس الحربة الحيّ. Moyasar متكامل، ZATCA Phase 2 مُختبَر، Audit Chain + Trust Pack مقبولان من مدراء أمن المعلومات السعوديين.

### b. الإمارات العربية المتحدة — United Arab Emirates · `dealix_status = pilot_ready`

| Field · الحقل | Value · القيمة |
|---|---|
| Regulator · الجهة | UAE Data Office + ADGM + DIFC (free-zone variants) |
| Framework · الإطار | UAE Federal Decree-Law No. 45 of 2021 on the Protection of Personal Data |
| Articles mapped · المواد | Article 5 (controller obligations), 9 (consent), 13 (cross-border transfers), 18 (data subject rights), 22 (penalties) |
| Local payment · الدفع | Telr / Network International / Checkout.com |
| Invoicing · الفوترة | FTA e-invoicing (rollout 2026+) |
| Language · اللغة | Khaleeji Arabic (UAE) primary; English equal weight |
| Activation gate · بوابة التفعيل | Opens after 1 Saudi flagship Sprint case study is published. |

الحزمة الحوكمية تُسقَط ١:١ على المرسوم رقم ٤٥. انحرافات ADGM/DIFC توثَّق لكل ارتباط. لا يوجد ريتينر إماراتي موقَّع بعد.

### c. دولة قطر — State of Qatar · `dealix_status = future_market`

| Field · الحقل | Value · القيمة |
|---|---|
| Regulator · الجهة | National Cyber Security Agency (NCSA) + Ministry of Transport |
| Framework · الإطار | Qatar PDPPL — Law No. 13 of 2016 |
| Articles mapped · المواد | Article 4 (consent), 6 (data minimisation), 7 (purpose limitation), 14 (special categories), 18 (cross-border transfers) |
| Local payment · الدفع | QPay / SkipCash / Doha Bank |
| Invoicing · الفوترة | No mandatory e-invoicing yet (manual + VAT pending) |
| Language · اللغة | Khaleeji Arabic (Qatari) primary; English secondary |
| Activation gate · بوابة التفعيل | Gated on a Qatari B2B services anchor + local legal entity (not Saudi-Article-18 transferable without DPA). |

أقدم PDPL خليجي وأكثرها تسامحًا. ديلكس يتجاوز الحد الأدنى بهامش مريح.

### d. دولة الكويت — State of Kuwait · `dealix_status = future_market`

| Field · الحقل | Value · القيمة |
|---|---|
| Regulator · الجهة | CITRA |
| Framework · الإطار | Data Privacy Protection Regulation (DPPR) No. 26 of 2024 |
| Articles mapped · المواد | Article 4 (consent + lawful basis), 6 (DPO requirement), 9 (data subject rights), 13 (cross-border transfers), 17 (breach notification) |
| Local payment · الدفع | KNET (only domestic processor) |
| Invoicing · الفوترة | No mandatory e-invoicing standard |
| Language · اللغة | Khaleeji Arabic (Kuwaiti) primary; English secondary |
| Activation gate · بوابة التفعيل | Same revenue milestone as Qatar + local entity. |

DPO إلزامي + قيود نقل بيانات صارمة = ملاءمة مرتفعة لحزمة ديلكس الحوكمية.

---

## ٣. تسلسل الـ ١٢ شهرًا · 12-month sequence

### English

**Months 1–3 — Saudi consolidation.** Close 3 Saudi retainers (4,999 SAR/mo × 3-month minimum = 44,991 SAR committed) and 1 flagship Sprint (25,000 SAR). Day-90 decision gate: if committed recurring SAR < 60,000, hold UAE entry until month 4 KPI delivers. Source: `docs/sales-kit/PRICING_REFRAME_2026Q2.md` § 7.

**Months 4–6 — UAE pilot opens.** Publish 1 anonymized flagship Sprint case study. Open UAE pilot via a Saudi anchor-partner referral (Big 4 advisory cross-border practice). Local entity scoping starts; no UAE invoice issued from a Saudi entity. Day-180 gate: 1 signed UAE Diagnostic engagement OR delay UAE retainer pursuit to month 7.

**Months 7–9 — UAE retainer + Qatar scoping.** Sign first UAE retainer (AED equivalent of 4,999 SAR floor at prevailing rate; floor does not drop). Begin Qatar legal entity scope: cost, timeline, DPA requirement for any Saudi → Qatar data flow under PDPPL Article 18. Day-270 gate: UAE retainer collecting on time OR pause Qatar entry.

**Months 10–12 — Qatar pilot OR Kuwait open.** Choose the market with the warmer anchor pipeline. Default: Qatar first (older statute, lighter implementation). Kuwait if a SAMA-licensed cross-border processor or CITRA-savvy partner surfaces earlier. Day-360 gate: 1 signed pilot in market #3 OR roll the 12-month plan forward and double-down on Saudi expansion before opening a third market.

### العربية

**الأشهر ١–٣:** ترسيخ سعودي. ٣ ريتينرات + ١ سبرنت رئيسي. بوابة قرار اليوم ٩٠: إذا الإيراد المتكرر < ٦٠٬٠٠٠ ر.س، نؤجّل دخول الإمارات للشهر ٤.

**الأشهر ٤–٦:** فتح طيار إماراتي بعد نشر دراسة حالة. تحويل عبر شريك سعودي مرتكز. نطاق الكيان القانوني الإماراتي يبدأ. بوابة اليوم ١٨٠: تشخيص إماراتي موقَّع.

**الأشهر ٧–٩:** أول ريتينر إماراتي. نطاق الكيان القطري. بوابة اليوم ٢٧٠: التحصيل الإماراتي منتظم أو إيقاف قطر.

**الأشهر ١٠–١٢:** طيار قطري أو فتح الكويت — أيهما تكون قناة الشريك أدفأ. بوابة اليوم ٣٦٠: ارتباط موقَّع في السوق الثالث، أو تمديد الخطة عامًا وتعميق السعودية.

---

## ٤. ما يتغيّر لكل سوق · What changes per market

### English

- **Dialect:** Saudi Khaleeji vs UAE Khaleeji vs Qatari Khaleeji vs Kuwaiti Khaleeji. Draft Pack templates fork at the dialect layer; the doctrine layer never forks.
- **Payment processor:** Moyasar (SA) → Telr/Network International/Checkout.com (UAE) → QPay/SkipCash/Doha Bank (QA) → KNET (KW). Each is a separate integration; none replaces the others.
- **Invoicing standard:** ZATCA Phase 2 (SA, live) → FTA e-invoicing (UAE, rollout 2026+) → manual + VAT pending (QA) → no mandatory standard (KW).
- **DPO requirements:** explicit + named under Kuwait DPPR Article 6 and UAE Federal Decree-Law 45; implicit under Saudi NDMO maturity model; lightest under Qatar PDPPL.
- **Currency:** SAR / AED / QAR / KWD. Retainer floor remains 4,999 SAR equivalent at prevailing inter-bank rate at contract date; floor never dips below local equivalent.
- **VAT treatment:** 15% SA / 5% UAE / VAT-pending QA / 0% KW (services). Sprint pricing is quoted net of VAT and grossed up on the local invoice.

### العربية

اللهجة والوسيط ومعيار الفوترة والعملة وضريبة القيمة المضافة تتغيّر لكل سوق. كل تغيير منها ينعكس في طبقة المسودات وطبقة الفواتير فقط — لا يلامس طبقة العقيدة، ولا طبقة Capital Asset، ولا Proof Pack. أرضية الريتينر تبقى ما يعادل ٤٬٩٩٩ ر.س محليًا، ولا تنخفض.

---

## ٥. ما لا يتغيّر · What does NOT change

### العربية + English

The doctrine is regional, not Saudi-only. Across all four markets we keep:

- **The 11 non-negotiables** — `auto_client_acquisition/governance_os/non_negotiables.py`.
- **The 3-offer ladder** — Strategic Diagnostic (0) → Governed Ops Retainer (4,999/mo) → Revenue Intelligence Sprint (25,000). Reference: `auto_client_acquisition/service_catalog/registry.py`.
- **The Trust Pack format** — same 14-section structure, signed and exportable, per market.
- **The Audit Chain shape** — same envelope schema with `agent_identity`, `approver_id`, `decision`, `source_ref`, `timestamp`.
- **The qualification scorer** — same weights and the same retainer-readiness gate.

البنود الـ ١١ + سُلَّم العروض الثلاثة + Trust Pack + Audit Chain + qualification scorer ثابتة في الأسواق الأربعة. العقيدة إقليمية، ليست سعودية فقط.

---

## ٦. أنماط مُمنوعة · Anti-pattern catalog

### English + العربية

- **Do NOT enter a market without a local entity.** PDPL Article 18 / UAE Article 13 / PDPPL Article 18 / DPPR Article 13 all bind cross-border data flow. A Saudi entity cannot lawfully invoice or host UAE/QA/KW personal data without a DPA — and a DPA is not a substitute for an entity once retainer-scale relationships form.
- **Do NOT translate the doctrine before launching a market.** Translation follows the first signed pilot, not preceded by it. Translating cold burns founder cycles on hypothetical buyers.
- **Do NOT lower the 4,999 SAR/month floor.** No market discount, no first-customer discount, no FX-rate exception. The floor is a conviction signal, not a price experiment.
- **Do NOT discount for "we are new to this market".** Newness is a buyer's question for the partner, not a price concession from us.

لا دخول بلا كيان محلي. لا ترجمة قبل أول طيار موقَّع. لا تخفيض للأرضية ٤٬٩٩٩. لا خصم لأننا جدد في السوق.

---

## ٧. قناة الشريك عبر الحدود · Cross-border partner channel

### English

The first UAE, Qatar, and Kuwait engagements will not originate from Dealix direct outreach. They originate from a Saudi anchor partner — typically a Big 4 advisory practice or a SAMA-licensed cross-border processor — referring an account they already serve. The partner economics (`docs/40_partners/PARTNER_COVENANT.md`) are identical across markets: 20% of collected revenue, 12-month tenure, 200,000 SAR cap, triggered only on a signed Sprint or Retainer. No referrals sourced via cold outreach. No data sharing without a Source Passport. The founder retains the right to decline any referral without explanation.

Cross-border referrals add one clause: the referring partner confirms in writing that the introduction is consented by the prospect, and that no personal data crosses borders before a Data Processing Agreement is in place. This clause is enforced at intake; an unconsented cross-border lead is rejected by the qualification scorer with reason `cross_border_consent_missing`.

### العربية

أول ارتباطات إماراتية وقطرية وكويتية لن تأتي من outreach مباشر. تأتي من شريك سعودي مرتكز — استشارات Big 4 أو مزوّد دفع مرخّص من ساما — يحوّل حساباً يخدمه أصلًا. اقتصاديات الشراكة في `docs/40_partners/PARTNER_COVENANT.md` ثابتة في الأسواق الأربعة: ٢٠٪ عمولة، ١٢ شهرًا، سقف ٢٠٠٬٠٠٠ ر.س، يُفعَّل عند توقيع سبرنت أو ريتينر. لا إحالات عبر outreach بارد. لا مشاركة بيانات بدون Source Passport. حق المؤسس في رفض الإحالة محفوظ.

الإحالات عبر الحدود تضيف بندًا واحدًا: تأكيد كتابي من الشريك أن التحويل برضا العميل، وأن البيانات الشخصية لا تعبر الحدود قبل توقيع DPA. مخالفة هذا البند ترفضها بوابة التأهيل بسبب `cross_border_consent_missing`.

---

## ٨. لوحة قياس التوسّع · Expansion scoreboard

### English

We measure expansion with three numbers only — anything more is theatre. Targets are estimates and explicitly marked as such; they are not commitments to outcomes.

| Metric · المقياس | Day 90 | Day 180 | Day 270 | Day 360 |
|---|---|---|---|---|
| Markets `active` (per `gcc_markets.py`) | 1 (SA) | 1 (SA) | 1 (SA) + 1 pilot AE | 1 (SA) + 1 (AE) |
| Saudi recurring SAR committed | ≥ 60,000 | ≥ 120,000 | ≥ 200,000 | ≥ 300,000 |
| Published flagship case studies | 0 | 1 | 1 | 2 |
| Cross-border partner referrals signed | 0 | 1 (AE) | 2 (AE) | 3 (AE + 1 QA/KW pilot) |

The `active` status for any market is set in `gcc_markets.py` only after one signed retainer is in production and one Proof Pack has been delivered in that market. The status is not a marketing claim; it is a code-level fact.

### العربية

نقيس التوسّع بثلاثة أرقام فقط. التارجتس تقديرات صريحة، لا التزامات بنتائج. ترقية حالة سوق إلى `active` في `gcc_markets.py` تتم فقط بعد توقيع ريتينر إنتاجي واحد وتسليم Proof Pack واحد في ذلك السوق. الحالة حقيقة برمجية، لا ادعاء تسويقي.

---

## ٩. مخاطر التوسّع · Expansion risks

### English

Three risks dominate. Each has a named mitigation tied to a file in the repo.

- **Risk: Saudi Article 18 cross-border data flow blocks a UAE/QA/KW retainer signing.** Mitigation: no UAE retainer is invoiced from a Saudi entity. Local entity scoping starts at month 4 for UAE. DPA template lives at `docs/40_partners/` (placeholder — founder's lawyer to harden).
- **Risk: A market's local payment processor (KNET in Kuwait) does not support recurring billing.** Mitigation: manual invoice + bank transfer SOP per market, captured in the local-invoicing layer. Recurring billing is a convenience, not a contract requirement.
- **Risk: A flagship case study takes longer than 6 months to publish (PDPL anonymization gate).** Mitigation: case study template is anonymized by default; the publish gate is owner approval + PII redaction pass + 30-day review window. Reference: `docs/case-studies/case_NNN_anonymized.md`.

### العربية

ثلاث مخاطر تهيمن. لكل خطر مخفّف مربوط بملف في المستودع. المادة ١٨ في PDPL، عدم دعم KNET للفوترة المتكررة، وتأخّر نشر دراسة الحالة الرئيسية — كلها مغطّاة بإجراءات SOP محدّدة. الخطر يُسجَّل في Friction Log عند ظهوره؛ لا يُترك في رؤوس الفريق.

---

## ١٠. مراجع · Cross-links

- `auto_client_acquisition/governance_os/gcc_markets.py` — 4 markets registry, single source of truth.
- `auto_client_acquisition/governance_os/non_negotiables.py` — the 11 doctrine entries.
- `docs/THE_DEALIX_PROMISE.md` — 11 non-negotiables (canonical bilingual text).
- `docs/sales-kit/PRICING_REFRAME_2026Q2.md` — pricing reframe + decision log.
- `docs/sales-kit/INVESTOR_ONE_PAGER.md` — anchor-partner positioning.
- `docs/40_partners/PARTNER_COVENANT.md` — partner commercial terms.
- `docs/funding/PRE_SEED_PITCH.md` — investor conversation framing.
- `docs/THE_DEALIX_OS_LICENSE.md` — open-source perimeter of the doctrine.

---

> **Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**
