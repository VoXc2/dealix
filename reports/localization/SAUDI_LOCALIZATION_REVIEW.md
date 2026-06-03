# Saudi Localization Review — Findings (2026-06-03)

| Check | Status |
|-------|--------|
| Arabic-first content & docs | 🟢 AR docs throughout |
| Saudi B2B tone (respectful, no hype) | 🟢 tone guide + claim detector |
| SAR pricing language | 🟢 ر.س / SAR |
| Riyadh timezone (UTC+3) assumption | 🟢 documented |
| Bilingual consistency | 🟢 style guide + glossary |
| WhatsApp Saudi UX | 🟢 post-consent, mobile-friendly |
| No exaggerated claims (AR+EN) | 🟢 enforced by `core/safety/claims.py` |
| Frontend RTL support | 🟡 review recommended in `src/` |

**Verdict:** Localization is Arabic-first and Saudi-appropriate at the content/
governance layer. Recommend a UI RTL pass in `src/` (Frontend UX Agent, L3, in
branch) as a follow-up.
