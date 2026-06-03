# Frontend Professional Polish Plan (Phase 10 Wave 5)

**Date:** 2026-05-07
**Audience:** anyone touching `/landing/` HTML/CSS/JS

This is the customer-facing UX standard for Dealix. Every new page or
edit must pass these checks (test in `tests/test_frontend_professional_polish.py`).

---

## Rules

### 1. One primary CTA per page (max 1 secondary)
- Homepage `/` — primary "ابدأ Mini Diagnostic" + secondary "شوف Executive Radar"
- Customer Portal — primary "شوف الباقة المغلقة" + secondary "تشخيص مجّاني"
- Executive Command Center — primary "شوف الباقة المغلقة" + secondary "لوحة العميل"
- Launchpad — primary "احجز Sprint" + secondary "تشخيص مجّاني أوّلاً"

### 2. Arabic primary, English secondary
- Page `<html lang="ar" dir="rtl">`
- Headings in Arabic
- English helper text in smaller font (≤14px usually)
- Saudi-Arabic dialect for marketing copy (e.g., "وش الوضع اليوم", "ابدأ بكره")

### 3. Mobile-first card order
- KPI cards stack vertically on mobile
- Hero CTA visible above-the-fold without scrolling
- Tap targets ≥ 44px (Apple HIG / Material baseline)
- No horizontal scroll on any viewport ≥ 320px

### 4. Empty states (Saudi-Arabic friendly copy)
- "لم يبدأ هذا القسم بعد. سيظهر هنا أوّل proof event بعد تسليم أوّل مخرج معتمد."
- Never blank `<div>` — always show empty-state copy
- Hint about what TRIGGERS the data to appear

### 5. Degraded states (honest about partial failure)
- Yellow banner with `<i data-lucide="alert-triangle">`
- Bilingual reason
- Specific hint: "X / Y / Z sections waiting for live data"
- NEVER "internal_error", "stacktrace", or any V11/V12 reference

### 6. DEMO labels
- Visible only in DEMO state (no `?org=`)
- `<span class="src-pill">DEMO</span>` on every section showing demo data
- Hidden when state is LIVE (no fake metrics without DEMO label)

### 7. Trust badges
- "Saudi-PDPL · Approval-first · Proof-backed" footer string on every customer-facing page
- "8 Hard Gates" badge linkable to `/dealix-beast-power.html`

### 8. Hard-gate explanations (in CUSTOMER language)
- Not: `NO_LIVE_SEND=true`
- Yes: "لا نُرسل رسائل خارجية بدون موافقتك"

### 9. Proof sections (real data only)
- `/proof.html` shows ONLY published Proof Pack snippets
- Empty state if no published proof: "نُحدّث هذه الصفحة بعد كل تسليم معتمد. لا ندّعي أرقام."
- NEVER fake testimonials, NEVER fake metrics

### 10. No internal names
- Customers don't see: `v10`, `v11`, `v12`, `v13`, `v14`, `beast`, `growth_beast`, `revops`, `customer_inbox_v10`, `compliance_os_v12`, `auto_client_acquisition`, `stacktrace`, `pytest`, `internal_error`
- Test enforces this on customer-facing pages (see `tests/test_customer_safe_product_language.py`)

### 11. No fake metrics
- Every metric on `/customer-portal.html` and `/executive-command-center.html` either:
  - Marked `DEMO`, OR
  - Sourced from a real API that respects "insufficient_data" pattern
- No "10x revenue", "guaranteed growth", "ranking guaranteed" claims

### 12. Proof-of-life footer
- Each customer-facing page links to `/privacy.html`, `/terms.html`, `/subprocessors.html`
- Each customer-facing page links to `/proof.html`

---

## Testing checklist

`tests/test_frontend_professional_polish.py` asserts:
- mobile meta tag present
- single primary CTA detectable per page
- Arabic + English text both present
- demo label rules
- footer trust strings present
- no internal terms (delegated to `tests/test_customer_safe_product_language.py`)

---

## What we will NOT polish in Wave 5

- Full pricing page rewrite (deferred — doc-only changes per Article 11)
- New animation library
- New design tokens (existing design-system.css remains canonical)
- New components beyond what's already built
- Storybook / Chromatic — defer until first Partner asks
