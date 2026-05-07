# Dealix — Real Demo Runbook (Wave 6 Phase 1)

**Date:** 2026-05-07
**Audience:** founder running the first warm-intro demos
**Duration:** 15 minutes
**Language:** Arabic primary, English helper

> **⚠️ Hard rules during the demo (every minute):**
> No live WhatsApp send · No live charge · No fake metrics · No guaranteed revenue · No internal terms (v11/v12/v13/v14/beast/growth_beast/stacktrace).
> All claims backed by evidence. All external actions stay manual.

---

## 0:00 — Opening (1 min)

**EN helper:** "Thanks for the time. I'll show you Dealix in 15 minutes — no slides, just the live system."

**AR (Saudi dialect):**
> "السلام عليكم. شكراً على الوقت. خلّني أوريك Dealix شغّال على الهواء — ١٥ دقيقة، بدون شرايح، بس النظام مباشرة."

**What you SHOW:**
- Open `https://dealix.me/` in browser
- Show the hero: "أوّل AI Operating Team للشركات السعوديّة"
- Note: "كل شي تشوفه هذي ١٥ دقيقة شغّال فعلاً، ليس prototype"

---

## 1:00 — What Dealix is (1 min)

**AR:**
> "Dealix طبقة AI تشغّل المبيعات + النمو + الدعم لشركتك قبل ما توظّف فريق كامل. ميزتي: كل قرار خارجي بموافقتك. لا إرسال آلي. لا اتصال آلي. لا ادعاءات بدون دليل."

**EN:** "Dealix is the AI operating layer that runs sales + growth + support for your company before you hire a full team. Every external action requires your approval. No auto-send. No auto-call. No claims without proof."

**What you SHOW:** `/launchpad.html` — the closed-package strategic depth (Sprint + Partner)

---

## 2:00 — Executive Command Center (2 min)

**AR:**
> "هذا مركز القيادة التنفيذي — كل ما تحتاجه الإدارة في صفحة واحدة. ١٥ قسم، بدون ما تفتح ١٠ تابات."

**EN:** "Executive Command Center — everything leadership needs in one screen. 15 sections, no tab-switching."

**What you SHOW:**
- Open `https://dealix.me/executive-command-center.html`
- DEMO mode is loud (purple "DEMO MODE" pill)
- Walk through the 15 sections in 30 seconds: executive_summary → full_ops_score → today_3_decisions → revenue_radar → sales_pipeline → growth_radar → partnership_radar → support_inbox → delivery_operations → finance_state → proof_ledger → risks_compliance → approval_center → whatsapp_decision_preview

**Talking point:** "كل كرت قرار يحتوي على ٨ حقول ثابتة: signal · why_now · recommended_action · risk · impact · owner · action_mode · proof_link. مو عشوائي."

---

## 4:00 — Full-Ops Score (1 min)

**AR:**
> "الـ Full-Ops Score رقم واحد يفهمه المدير. بين صفر و١٠٠. كل طبقة لها وزن محدّد. النقاط لا تظهر إذا الطبقة ناقصة."

**EN:** "The Full-Ops Score is a single number leadership reads. 0-100. Each layer has a fixed weight. No points awarded if a layer is missing."

**What you SHOW:**
- Hit `https://api.dealix.me/api/v1/full-ops-radar/score` (live endpoint)
- Show the breakdown: LeadOps 15 · Customer Brain 10 · Service Sessions 10 · Approval Center 10 · Payment Ops 10 · Support 10 · Proof Ledger 10 · Customer Portal 10 · Executive Dashboard 10 · Safety/Compliance 5 = **100**
- Readiness label: 90+ = "Full Ops Ready"

**Talking point:** "ما نزوّر النقاط. لو طبقة ناقصة، النقاط صفر. هذا الفرق بين Dealix و dashboard فاضي."

---

## 5:00 — Today's 3 Decisions (2 min)

**AR:**
> "هذا الجزء الأهم لك — أهم ٣ قرارات اليوم. كل قرار: من الإشارة، ليش الآن، الإجراء المقترح، الخطر، الأثر، صاحبه، طريقة التنفيذ، رابط الدليل."

**EN:** "Most important part for you — top 3 decisions today. Each: signal · why_now · recommended_action · risk · impact · owner · action_mode · proof_link."

**What you SHOW:**
- Show 3 demo decision cards (visible in DEMO state)
- Highlight: every action_mode is `approval_required` (NOT `live_send`)
- Click into one card to show how the founder would approve it manually

**Talking point:** "ما يطلع شي للعميل بدون موافقتك — حتى لو AI كتب الرد كاملاً."

---

## 7:00 — Revenue / Sales / Growth Radars (2 min)

**AR:**
> "ثلاث رادارات: الإيرادات، الـ pipeline، النمو. كل رقم له مصدر — لا أرقام مخترعة."

**EN:** "Three radars: revenue, sales pipeline, growth signals. Every number has a source — no fake metrics."

**What you SHOW:**
- Revenue Radar: confirmed_payments_count + confirmed_revenue_sar (in DEMO this is 0, that's honest)
- Sales Pipeline: sessions_active + sessions_delivered + sessions_complete
- Growth Radar: 16 signal types tracked (hiring_sales, tender, funding, new_branch, WhatsApp_business, …)

**Talking point:** "في DEMO الأرقام صفر لأن ما عندك بيانات حقيقيّة بعد. هذا هو الصدق."

---

## 9:00 — Support Journey (1 min)

**AR:**
> "الدعم في Dealix ليس tickets فقط. ٧ مراحل: قبل البيع → onboarding → التسليم → الفوترة → الإثبات → التجديد → الخصوصيّة. كل مرحلة لها SLA مختلف."

**EN:** "Support is journey-aware: pre_sales → onboarding → delivery → billing → proof → renewal → privacy. Each stage has its own SLA."

**What you SHOW:**
- Hit `POST /api/v1/support-journey/answer` with sample message
- Show the response: classification + journey_stage + draft + escalation policy
- Highlight: billing/privacy/renewal **always** escalate to founder (p0 SLA)

**Talking point:** "تذكرة استرجاع فلوس ما تروح للـ AI ترد لوحده — تروح للمؤسس فوراً."

---

## 10:00 — Guardrails & Trust (1 min)

**AR:**
> "كل tool call داخل Dealix يمر من ٥ طبقات حراسة: input · tool · output · cost · audit. متطابقة مع OpenAI Agents SDK + OWASP LLM categories."

**EN:** "Every tool call passes 5 guardrail layers: input · tool · output · cost · audit. Matches OpenAI Agents SDK pattern + OWASP LLM categories."

**What you SHOW:**
- Hit `POST /api/v1/tool-guardrails/check` with `tool_name=linkedin_automate`
- Response: `permitted=False`, reason: "NO_LINKEDIN_AUTO constitutional gate"
- Try `tool_name=whatsapp_send_live` → blocked with "NO_LIVE_SEND"
- Try `tool_name=scrape_external` → blocked with "NO_SCRAPING"

**Talking point:** "الـ ٨ بوّابات الصلبة مفروضة في الكود، مو settings في الإعدادات. حتى المؤسس ما يقدر يعطّلها."

---

## 11:00 — Customer Portal (2 min)

**AR:**
> "هذا اللي يشوفه عميلك يومياً. ٨ أقسام أساسيّة + ١٤ قسم enriched إضافي. كل شي بالعربي السعودي + Arabic primary."

**EN:** "This is what your customer sees daily. 8 core sections + 14 enriched sections. Saudi Arabic primary."

**What you SHOW:**
- Open `https://dealix.me/customer-portal.html`
- Walk through: Operations اليوم → الرحلة (Journey) → Radar اليومي → القرارات المعلّقة → Digest أسبوعي/شهري → خريطة كل التسلسلات
- Show the empty-state copy: "لم يبدأ هذا القسم بعد. سيظهر هنا أوّل proof event بعد تسليم أوّل مخرج معتمد."
- Show degraded banner: when active mode falls back to demo

**Talking point:** "Empty states واضحة بالعربي. لا 'No data found' غامض."

---

## 13:00 — Proof Path (1 min)

**AR:**
> "كل ادّعاء عندنا له دليل. Proof Ledger يسجّل كل واقعة: من، متى، الدليل، إذن النشر، التوقيع. لا case study بدون توقيع العميل."

**EN:** "Every claim has evidence. Proof Ledger records: who, when, evidence, publication consent, signature. No case study without customer signature."

**What you SHOW:**
- Open `https://dealix.me/proof.html`
- Empty state if no published proof: "نُحدّث هذه الصفحة بعد كل تسليم معتمد. لا ندّعي أرقام."
- Hit `GET /api/v1/proof-ledger/status` — show hard_gates: pii_redacted_before_persistence, no_raw_pii_in_exports

**Talking point:** "لو طلعت من Dealix بكره، تطلع ومعاك Proof Pack كامل بصيغة قابلة للتدقيق."

---

## 14:00 — 499 SAR Pilot Offer (1 min)

**AR:**
> "إذا حسّيتك مهتم، عندنا Sprint قصير: ٧ أيّام، ٤٩٩ ريال، ٥ تسليمات + Proof Pack أوّلي. الدفع عبر تحويل بنكي (لا live charge). ضمان استرجاع ١٠٠٪ خلال ١٤ يوم بدون أسئلة."

**EN:** "If you're interested, we have a short Sprint: 7 days, 499 SAR, 5 deliverables + initial Proof Pack. Payment via bank transfer (no live charge). 100% refund within 14 days, no questions."

**Sprint deliverables (recap):**
1. Lead Quality Audit (2-page PDF)
2. Pipeline Audit (your actual leads scored)
3. 3 Daily Decisions Briefs (sample of `/decisions.html`)
4. 1 sample WhatsApp/email draft (you approve manually)
5. Initial Proof Pack (3 evidence events minimum)
6. 30-day plan PDF
7. Day 7 review call (continue to Partner OR refund)

**KPI commitment (NOT guarantee):** "لو ما تحقّق +٢٠٪ على المؤشّر المتّفق عليه، أشتغل مجّاناً حتى يتحقّق."

---

## 15:00 — Close (1 min)

**AR:**
> "إذا تبي تبدأ، عندي رابط جاهز للـ diagnostic المجّاني (٢ دقيقة) — يولّد لك تقرير مخصّص لشركتك خلال ٢٤ ساعة. هل أرسله لك الآن؟"

**EN:** "If you want to start, here's the link to the free diagnostic (2 min) — generates a custom report for your company in 24h. Want me to send it now?"

**What you SHOW:**
- Send `https://dealix.me/diagnostic.html` (or sector-specific `/diagnostic-real-estate.html`)
- If they say yes → log the demo outcome via `dealix_demo_outcome.py --outcome pilot_requested`
- If they say "let me think" → log `--outcome follow_up`
- If they say no → log `--outcome not_now`

**After the call (founder's homework):**
1. `python3 scripts/dealix_demo_outcome.py --prospect-handle <handle> --sector <s> --outcome <o> --next-action "..."`
2. Send Calendly link for diagnostic call (within 24h)
3. If pilot_requested → run `python3 scripts/dealix_pilot_brief.py --company <c> --sector <s>` and send the PDF

---

## Things you must NOT say during the demo

- ❌ "Dealix يضمن ١٠× revenue" → say "نلتزم بـ KPI lift +٢٠٪، لا ضمانات"
- ❌ "We'll auto-send WhatsApp campaigns" → say "كل رسالة بموافقتك، لا live send"
- ❌ "Scrape your competitors' data" → say "لا scraping أبداً"
- ❌ "Cold WhatsApp blast to your old leads" → say "لا cold WhatsApp، لا blast"
- ❌ "We'll automate LinkedIn for you" → say "LinkedIn يدوي فقط، لا أتمتة"
- ❌ Any reference to "v11/v12/v13/v14/beast/growth_beast" — these are internal names

## Things you SHOULD show without prompting

- ✅ The honest empty states (no fake metrics)
- ✅ The DEMO label visible everywhere
- ✅ The 8 hard gates documented
- ✅ The 4-tier package ladder (Free / 499 / 1500 / 2999-4999/mo / 7500-15000/mo)
- ✅ The ECC 4-state UX (DEMO / SIGNED_UP / ACTIVE / DEGRADED)
- ✅ The Saudi-Arabic-first design (RTL + IBM Plex Sans Arabic)

## After the demo (within 1 hour)

```bash
# Log the outcome
python3 scripts/dealix_demo_outcome.py \
  --prospect-handle <handle> \
  --sector <real_estate|agencies|services|consulting> \
  --outcome <interested|not_now|pilot_requested|paid|follow_up> \
  --next-action "send Calendly link" \
  --notes "30-min discovery call needed Tuesday"

# If pilot_requested, generate brief
python3 scripts/dealix_pilot_brief.py \
  --company "<company>" \
  --sector <sector> \
  --amount-sar 499

# If diagnostic was already collected during call, generate it
python3 scripts/dealix_ai_ops_diagnostic.py \
  --company "<company>" \
  --sector <sector> \
  --region <city> \
  --problem "<one-sentence>" \
  --language ar
```
