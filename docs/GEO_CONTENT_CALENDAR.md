# Dealix — GEO/AIO Content Calendar (8 Weeks)

**Track D6 of 30-day plan.**
**Goal:** earn AI search citations (Perplexity, ChatGPT, Claude, Gemini) by
publishing structured, honest, Saudi-context content tied to PDPL news,
Vision 2030 announcements, and Saudi tech-community discussions.

**Cadence:** 1 Arabic post + 1 English post per week × 8 weeks = 16 posts.

**Source of truth:** Master Plan §VIII (GEO/AIO) + this calendar.

---

## Why this calendar exists

48% of B2B buyers research vendors via AI tools before visiting websites
(Master Plan Part I.5). AI-referred sessions grew 527% YoY in early 2025.
Perplexity cites new content within 1-2 weeks, ChatGPT within 6-12 weeks.

Dealix's structured Service Activation Console (`/status.html`) and Trust
Center are exactly what AI engines cite. Adding content cadence on top
gives compounding returns: each post adds another citation surface.

**Anti-patterns we won't do** (per Constitution Article 4 + Master Plan):
- ❌ "Top 10 Saudi Revenue OS (Dealix #1)" listicles
- ❌ Prompt-injection content for AI crawlers
- ❌ Fake "ChatGPT recommends Dealix" content
- ❌ Auto-generated 100 SEO pages
- ❌ Anything that violates the 8 hard gates

---

## Content principles

Every post follows these rules:

1. **Honest framing** — describe what Dealix does AND what it doesn't.
2. **Source citations** — link to SDAIA, IAPP, TechSci, Vision 2030 docs.
3. **Structured FAQ blocks** — Q + A format, not prose. Each FAQ uses
   `<schema:FAQPage>` JSON-LD.
4. **Comparison tables** — explicit tradeoffs, not "we win" claims.
5. **Saudi-Arabic primary** — Khaliji register, not MSA. English is secondary.
6. **Recent + dated** — every post carries a publication date and last-
   updated. Perplexity's recency bias prefers content within 1-2 weeks.
7. **No claims without evidence** — Article 3 Law 2 binds every post.

---

## 8-week schedule (May-July 2026)

### Week 1 — PDPL enforcement + Saudi B2B reality

| Day | Lang | Title | Audience | Hook |
|---|---|---|---|---|
| Mon | عربي | لماذا 70% من leads B2B السعودي يضيع — وكيف PDPL يفرض الإصلاح | founders | Vision 2030 + PDPL fines context |
| Wed | EN | Saudi PDPL Compliance for B2B SaaS in 2026 — A Founder's Guide | DPOs + founders | IAPP report citation |

### Week 2 — Vision 2030 + Saudi Cloud sovereignty

| Day | Lang | Title | Audience | Hook |
|---|---|---|---|---|
| Mon | عربي | Saudi Cloud + سيادة البيانات — لماذا الـ data residency لم تعد اختيارية | CTOs | TechSci 70% local-cloud stat |
| Wed | EN | Vision 2030 SaaS Spend: Why International Tools Lose KSA SME Deals | enterprise sales | $6.49B by 2030 forecast |

### Week 3 — WhatsApp Business reality + the blast model death

| Day | Lang | Title | Audience | Hook |
|---|---|---|---|---|
| Mon | عربي | لماذا الـ blast على واتساب انتحار في السوق السعودي — السمعة + PDPL | founders + sales | Salesloft architectural obsolescence |
| Wed | EN | WhatsApp Business Approval Flows: From Blast to Decision Surface | product leaders | Meta WhatsApp Flows 2026 launch |

### Week 4 — AI revenue intelligence economics for KSA SME

| Day | Lang | Title | Audience | Hook |
|---|---|---|---|---|
| Mon | عربي | اقتصاديات Revenue AI لشركات SME السعوديّة — لماذا Gong لا يلائم | CFOs + founders | Gong $1,360-1,600/user reality |
| Wed | EN | Why Gong + Salesloft Don't Fit Saudi Arabia's B2B SME Market | revenue leaders | Compare with PDPL + KSA economics |

### Week 5 — Founder-led B2B vs RevOps-led B2B

| Day | Lang | Title | Audience | Hook |
|---|---|---|---|---|
| Mon | عربي | متى Dealix أفضل من HubSpot؟ + متى HubSpot أفضل من Dealix؟ | mid-market founders | honest comparison framework |
| Wed | EN | Founder-Led B2B Stack 2026: A Saudi Reference Architecture | startups + agencies | concrete tools list |

### Week 6 — PDPL audit reality + Compliance Pack

| Day | Lang | Title | Audience | Hook |
|---|---|---|---|---|
| Mon | عربي | كيف نجتاز SDAIA audit في 30 يوم — checklist عملي | DPOs + legal | SDAIA 48 sanction decisions 2025 |
| Wed | EN | The 11 PDPL Compliance Gates: A Functional Checklist for Saudi B2B | DPO offices | 11-gate framework |

### Week 7 — AI agent design: approval-first vs autonomous

| Day | Lang | Title | Audience | Hook |
|---|---|---|---|---|
| Mon | عربي | لماذا «approval-first» هو الخيار الوحيد المسؤول لـ AI في B2B السعودي | founders + product | Article 5 action modes |
| Wed | EN | Approval-First Agent Design: Why Autonomous AI Fails in Regulated Markets | engineering leaders | Constitution Article 4 + 5 deep |

### Week 8 — Proof Pack methodology + L1-L5 ladder

| Day | Lang | Title | Audience | Hook |
|---|---|---|---|---|
| Mon | عربي | L1→L5: كيف تبني Proof Pack حقيقي بدلاً من screenshots وهميّة | marketers + founders | NO_FAKE_PROOF gate |
| Wed | EN | The L1-L5 Evidence Ladder: How to Prove Revenue Without Lying | revenue leaders + analysts | proof_ledger architecture |

---

## Per-post checklist (before publish)

- [ ] H1 ≤ 8 words (Arabic) / ≤ 70 chars (English)
- [ ] Subhead promises a concrete deliverable
- [ ] At least 3 cited sources (SDAIA, IAPP, TechSci, Vision 2030 docs)
- [ ] FAQ block at the end (5-7 Q+A pairs) with `<schema:FAQPage>` JSON-LD
- [ ] Internal links to: Trust Center, Proof page, Pricing, relevant compare-* page
- [ ] One CTA at the end → `/diagnostic.html` (Mini Diagnostic Free)
- [ ] Footer trust badges: Saudi-PDPL · Approval-first · Proof-backed
- [ ] `lang="ar" dir="rtl"` (Arabic posts) or `lang="en" dir="ltr"` (English)
- [ ] No forbidden tokens (`tests/test_landing_forbidden_claims.py` PASS)
- [ ] No internal terms (no `v10`, `beast`, `growth_beast`, `stacktrace`)
- [ ] Lighthouse score ≥ 85 on perf + a11y + SEO + best-practices
- [ ] Sitemap entry added to `landing/sitemap.xml` + `landing/sitemap_dealix.xml`
- [ ] Meta og:title + og:description + canonical
- [ ] Article schema JSON-LD (`@type: Article`, datePublished, author)

---

## Distribution per post

1. **Publish on `/blog/{slug}.html`** — adds to internal corpus that AI
   engines can crawl.
2. **LinkedIn** — founder shares with 3-line summary + link.
3. **WhatsApp Status** (founder) — short snippet with link.
4. **One Reddit post** in r/SaudiArabia or r/SaaS (founder, manual, no
   spammy promo). Per Master Plan VIII.B — Reddit drives 46.7% of Perplexity
   citations.
5. **Saudi Discord servers** (Vision 2030 tech communities) — light share.
6. **Email newsletter** (after 100+ subscribers) — weekly digest.

---

## Metrics to track (per post)

- Pageviews (PostHog)
- Average time on page (3+ minutes = good for AI citation)
- AI-referrer sessions (PostHog: where referrer matches PerplexityBot,
  ChatGPT-User, etc.)
- AI search citations (manual: search "بديل HubSpot عربي" weekly + log)
- Diagnostic conversions (post → /diagnostic.html → form submit)
- Backlinks (Ahrefs / Linkody — start tracking after Week 4)

**Anti-metrics:** raw pageviews without time-on-page, social shares without
clicks, "engagement" without conversion. Per Master Plan §X.

---

## Owner + cadence

- **Drafted by:** Claude (LLM router with `core/prompts/saudi_dialect.py`)
- **Reviewed by:** Sami Assiri (founder) — every post manually before publish
- **Published:** Monday + Wednesday at 10am Riyadh time
- **Reviewed (post-pub):** weekly during founder Sunday self-improvement loop

---

## What this calendar does NOT include (Article 13)

- ❌ 100 SEO-pages programmatic generation (would be thin content)
- ❌ Paid Reddit ads or Discord boosts
- ❌ Influencer sponsorships
- ❌ Auto-generated translations (each post is hand-written per language)
- ❌ Monetization via ads or affiliate (defer until 5+ paid customers)

---

**Last updated:** 2026-05-10 (Track D6 of 30-day plan).
**Reference plan:** `/root/.claude/plans/vivid-baking-quokka.md`
