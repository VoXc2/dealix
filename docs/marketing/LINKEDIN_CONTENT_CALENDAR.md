# LinkedIn 12-Week Content Calendar (Arabic + English) — W13.10

> **Audience:** Saudi B2B founders, CTOs, CIOs, sales leaders + Saudi VC partners.
> **Cadence:** 2 posts/week (Sun + Wed) for 12 weeks = 24 posts pre-planned.
> **Voice:** founder-first, honest, technical-when-relevant, no marketing fluff.
> **Goal:** build relationships pre-pitch. Pitch happens later, in DMs, after trust.

## The Posting Discipline (the Saudi B2B founder playbook)

1. **Sunday 09:00 AST:** technical / engineering insight (CTO audience)
2. **Wednesday 12:00 AST:** business / commercial insight (founder + sales audience)
3. **Post in Arabic + English in same post** (bilingual = 2× reach)
4. **First line is the hook** (LinkedIn algorithm prioritizes 3-line preview)
5. **No links in first 2 hours** (algorithm penalty) — link in first comment
6. **Engage every reply** within 4 hours (algorithm signal + relationship)
7. **No reposting US content** — write original Saudi-specific takes

---

## Week 1 — Foundation (Vision)

### Post 1 (Sun) — "Why I'm building Saudi-sovereign AI"

> سنواتي قبل Dealix كنت أحاول استخدام أدوات AI أمريكية لشركات
> سعودية. كل مرة نصطدم بنفس الجدار: PDPL. ZATCA. me-south-1.
>
> القرار: نبني نظام AI من الصفر، سعودي القلب، عالمي التقنية.
>
> 121 router، 8 migrations، 290+ test لاحقاً، Dealix الآن
> 7 streams إيرادية جاهزة + PDPL Articles 5/13/14/18/21 wired
> + ZATCA Phase 2 e-invoice.
>
> الـ moat الحقيقي ليس النموذج AI — منافسون US عندهم Claude/GPT-4 نفسه.
> الـ moat هو سنة-سنتين compliance gap.
>
> ---
> Years before Dealix I was forcing US AI tools onto Saudi B2B
> companies. Every time, same wall: PDPL. ZATCA. me-south-1.
>
> Decision: build a Saudi-native AI OS from zero.
>
> 121 routers, 8 migrations, 290+ tests later, Dealix has 7 active
> revenue streams + PDPL articles wired + ZATCA Phase 2.
>
> The real moat isn't the AI model — competitors use the same
> Claude/GPT-4. The moat is the 18-24 month compliance gap.

### Post 2 (Wed) — "The math of bootstrapping"

> 30,000 ريال شخصي.
> 1,725 ريال بنية تحتية شهرياً.
> 17 شهر runway لو لم أرفع راتب.
>
> هذا الإطار يجبرني على decision tree معقّد:
> - عميل #1 يجب يأتي قبل اليوم 90، أو أعدّل المسار.
> - كل ساعة code = ساعتي sales (الـ ratio v3 §6).
> - راتبي = 0 حتى MRR > 5K، ثم 5K حتى MRR > 25K.
>
> الفرق بين هذا والـ VC-funded:
> Disciplined founder ينظر للقيمة بريال.
> VC-funded founder ينظر للقيمة بـ "burn".
>
> الاثنان يعملان. الأول يبقى في القيادة، الثاني يعطي مفاتيحه.
>
> ---
> 30K SAR personal capital.
> 1,725 SAR/mo infrastructure.
> 17 months runway if no salary.
>
> Bootstrapping logic:
> - Customer #1 by day 90 or pivot.
> - 1h coding = 2h sales (v3 §6 ratio).
> - Salary = 0 until MRR > 5K, then 5K until MRR > 25K.
>
> VC vs bootstrap difference:
> Disciplined founder values money in riyals.
> VC founder values money in "burn".
>
> Both work. First keeps founder in control. Second hands over keys.

---

## Week 2 — Compliance Differentiation

### Post 3 (Sun) — "PDPL Article 18 deep dive"

> PDPL Art. 18 — قراءة سعودية:
> كل وصول لبيانات شخصية يجب تسجيله مع retention 5 سنوات.
>
> ما الفرق بيننا و US tools:
>
> Dealix:
>   - middleware يلتقط 15 personal-data path prefix تلقائياً
>   - audit log row per access: timestamp, user_id, tenant_id, path,
>     ip_address, purpose
>   - 5-year retention في Postgres
>   - PDPL Art. 14 export يرجع كل entries هذا data subject
>
> Salesforce / HubSpot:
>   - audit log مخصّص للأمن (login attempts)
>   - يحتاج enterprise tier + custom config
>   - retention defaults أقل
>   - PDPL-specific schema غير موجود
>
> الفرق ليس feature gap — هو architecture gap.

### Post 4 (Wed) — "Why I'm pricing at 499 SAR not free pilot"

> سؤل: "ليش 499 ريال للـ pilot؟ مو الـ free pilot أكثر جذباً؟"
>
> الجواب باختصار: 499 ريال = filter للجدية.
>
> Free pilot الذي اتجاوب معه:
>   - 80% غير جادين (يشترك بسرعة، ينسى)
>   - 15% يطلبون "more demos" بلا التزام
>   - 5% يدفعون monthly subscription
>
> 499 SAR pilot:
>   - 100% الذين دفعوا = جدّيين
>   - 50%+ يرتقون لـ Growth (industry data)
>   - منخفض-المخاطرة لي (founder time worth it)
>   - يثبت قيمة الـ AI بميزانية sandwich
>
> السعر-الفلتر ≠ السعر-المرفوع. اختر الأول.

---

## Week 3 — Technical depth

### Post 5 (Sun) — "Decision Passport: the audit trail I wish I had at my last job"

> فكرة Decision Passport جاءتني من معاناة شخصية:
> ​​​​​​​​​​​​​في وظيفتي السابقة، AI أرسل رسالة لعميل enterprise
> بمعلومة خاطئة. لاحقاً سألوني: "من اعتمد؟ متى؟ بأي evidence؟"
> ​​​​​​​​​​​​​لم يكن لدينا جواب.
>
> Dealix يحتفظ بـ Decision Passport entry لكل external commitment:
>   - agent_id + version (أي model + أي system prompt)
>   - evidence_level (high/medium/low confidence)
>   - approver_user_id (لو required approval)
>   - timestamp + tenant_id
>
> ​​​​​​​​​​​​​"No Passport, No Action" — مبدأ Golden Chain enforced
> ​​​​​​​​​​​​​في الكود.
>
> ​​​​​​​​​​​​​Compliance officers يحبون هذا. CIO يحبه. Customer يحبه.

### Post 6 (Wed) — "The Saudi B2B SaaS pricing reality"

> 2,999 ريال/شهر — هل هذا مرتفع لـ Saudi B2B؟
>
> Reality check:
>   - Salesforce Sales Cloud: 5,500-9,000 ريال/شهر
>   - HubSpot Pro: 3,000-6,000 ريال/شهر
>   - Intercom Engage: 6,000-12,000 ريال/شهر
>   - + compliance consulting: 50K-200K ريال/سنة على top
>
> Dealix Growth: 2,999 ريال/شهر شاملاً compliance.
>
> الـ "premium" ليس premium — هو fair value relative to alternative.
>
> https://dealix.me/why-saudi-ai (مقارنة شفافة)

---

## Week 4-12 — Outline (24 posts pre-titled)

| Wk | Sun Topic | Wed Topic |
|----|-----------|-----------|
| 4 | "How we built tenant theming in 567 lines" | "First customer expectations vs reality" |
| 5 | "ZATCA Phase 2 — implementation notes" | "When NOT to choose Dealix (honest)" |
| 6 | "Building Lead Engine with 5 adapters + ICP scorer" | "Customer #5 — what changed in playbook" |
| 7 | "WhatsApp Webhook security — the threats no one talks about" | "5K SAR referral economics" |
| 8 | "Saudi sector intel — what data actually moves needles" | "Pre-seed conversation patterns" |
| 9 | "Decision Passport vs Generic Audit Log" | "Why no LinkedIn auto (policy + product)" |
| 10 | "How to choose your first Saudi VC" | "Customer #10 milestone + retention data" |
| 11 | "Tenant isolation: 3 layers (middleware, ORM, RLS)" | "Mistakes founders make negotiating Saudi VCs" |
| 12 | "Building the agency channel (R6)" | "Year-1 lessons + Year-2 plan" |

---

## Content Templates (reusable patterns)

### Pattern 1: "Personal Frustration → Technical Solution"

> Frustration → "Last week a customer asked X..."
> Why obvious solutions don't work → "Tried Salesforce, Notion, Airtable. Failed because Y."
> Dealix approach → "We built Z that solves..."
> Code/file reference → file path + line numbers
> CTA → "If you face same: dealix.me/{relevant-page}"

### Pattern 2: "Saudi vs International Math"

> Quantified Saudi-specific problem
> US-tool cost + workaround cost
> Dealix cost + native solution
> Saving math
> Live evidence URL

### Pattern 3: "Honest Disclosure"

> What we're great at + customer evidence
> What we're not (specifically)
> Who should NOT use Dealix
> Who SHOULD
> CTA only for fit

### Pattern 4: "Behind-the-scenes engineering"

> Yesterday I built X
> Why this took longer than expected
> What I learned (specific technical insight)
> What I'd do differently
> Open invitation to discuss

### Pattern 5: "Founder math"

> A specific decision faced
> Two/three options evaluated quantitatively
> What I chose + why
> What this tells you about Dealix's approach
> Implicit invite to dig deeper

---

## Anti-Patterns (don't post these)

❌ "Excited to announce..." — language signal of marketing
❌ "X% of companies..." statistics without specific citation
❌ Vague "AI is the future" takes — adds no signal
❌ Hot takes on Saudi politics / religion / royalty
❌ Disparaging competitors by name
❌ Reposts of US tech news with no local angle
❌ "Drop a 🚀 if you agree" engagement bait
❌ "Hiring soon" before hire trigger (customer #10)

---

## Engagement Protocol

When someone comments:
1. Reply within 4 hours during business
2. If question = deep, offer to DM
3. If criticism = engage honestly, never dismiss
4. If founder peer = recognize them by name + their context

Goal: build 200 meaningful Saudi B2B relationships before pre-seed.
Then 50 of them become "first call" for any major announcement.

---

## Tracking (review monthly)

| Metric | Target Y1 | Y2 |
|--------|-----------|----|
| Followers | 500 → 2,000 | 5,000 |
| Average post views | 1,000 | 5,000 |
| Post engagement rate | ≥ 3% | ≥ 5% |
| DM conversations triggered | 5/month | 20/month |
| Customer leads from LinkedIn | 1/quarter (Y1) | 1/month (Y2) |

---

## Activation Note

These posts are pre-planned for the founder to actually publish.
Schedule one weekly Sunday morning (15 min) to:
1. Customize the placeholder details to current state
2. Add screenshot/image if relevant (Decision Passport entry, etc.)
3. Schedule via LinkedIn native scheduler for Sun + Wed
4. Set 4-hour reminder to engage replies

Founder-led content > corporate content in B2B by 10×.
This calendar removes the "what to post" decision so founder
focuses on the conversation, not the composition.
