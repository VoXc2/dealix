# Dealix Master Status — حالة الشركة الرئيسية

> Wave 19 Recovery — CEO Completion Sprint.
> Source of truth: `scripts/verify_all_dealix.py` (run anytime to refresh).
> Updated: 2026-05-14.

This document is the founder's single honest CEO-completion view. The
master verifier scores 9 systems on a 1-5 scale. **Build-complete** is
necessary; **company-complete** requires real market motion (outreach
sent + invoice issued), not just the right code on disk.

هذه الوثيقة هي النظرة الصادقة لاكتمال Dealix كشركة. يصنّف المُحقق الرئيسي
٩ أنظمة على مقياس ١-٥. **اكتمال البناء** ضروري لكن غير كافٍ؛ **اكتمال
الشركة** يتطلّب حركة سوقية حقيقية (تواصل مُرسَل + فاتورة مُصدَرة)، لا
مجرّد ملفات صحيحة على القرص.

---

## 1. The 9 verified systems · الأنظمة التسعة المُحقَّقة

| # | System | Build state | CEO-complete trigger |
|---|---|---|---|
| 1 | Doctrine (Dealix Promise + 11 Non-Negotiables) | code + public API + tests | always 5/5 once shipped |
| 2 | Offer Ladder (3 offers + INVESTOR_ONE_PAGER + reframe doc) | code + docs + tests | always 5/5 once shipped |
| 3 | GCC Standardization Pack | 8-doc pack + gcc_markets API | always 5/5 once shipped |
| 4 | Capital Asset Library | 15 assets + index + library docs | always 5/5 once shipped |
| 5 | Open Governed AI Ops Doctrine | open-doctrine/ pack + public API | always 5/5 once shipped |
| 6 | Funding + Hiring Pack | memo + use-of-funds + scorecards + first-3-hires | always 5/5 once shipped |
| 7 | Founder Command Center | page + admin API + deployment marker JSON | always 5/5 once shipped |
| 8 | **Partner Motion** | pipeline + log + doc artifacts | **3/5 ready → 5/5 only after 1st outreach sent** |
| 9 | **First Invoice Motion** | runbook + log + Moyasar + ZATCA artifacts | **3/5 ready → 5/5 only after 1st invoice issued** |

Systems 1-7 score 5/5 because they are pure build artifacts. Systems 8
and 9 are deliberately capped at 3/5 until the founder takes an
irreversible market action. **The marker files refuse to lie.**

الأنظمة 1-7 تحقق 5/5 لأنها مخرجات بناء. الأنظمة 8 و 9 تبقى مقصوصة عند
3/5 حتى يتخذ المؤسس فعلًا سوقيًا غير قابل للتراجع. **ملفات العلامات لا
تكذب.**

---

## 2. The two CEO actions that flip the verifier · الفعلان

### Action A — Send 1 anchor partner outreach
1. Open `docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md`.
2. Pick the specific company name + the specific person at the company.
3. Open `data/anchor_partner_pipeline.json` — confirm the archetype.
4. Send the bilingual draft from your own account (no automation).
5. Append the entry to `data/partner_outreach_log.json`:
   ```json
   {
     "partner_name": "...",
     "archetype": "Big 4 advisory Saudi practice",
     "sent_at": "2026-05-15T08:30:00Z",
     "channel": "email",
     "message_file": "docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md#archetype-1",
     "status": "sent",
     "next_follow_up_at": "2026-05-17T08:30:00Z"
   }
   ```
6. Increment `outreach_sent_count` to 1.
7. Re-run `python scripts/verify_all_dealix.py` → Partner Motion now 5/5.

### Action B — Issue Invoice #1
1. Qualified buyer accepts the proposal.
2. Follow `docs/ops/FIRST_INVOICE_UNLOCK.md` exactly — Capital Asset registration FIRST.
3. Run `scripts/moyasar_live_cutover.py` if not already flipped.
4. Run `scripts/zatca_preflight.py` to confirm e-invoicing readiness.
5. Issue the invoice via Moyasar (founder approval logged).
6. Append the entry to `data/first_invoice_log.json` with all required fields.
7. Increment `invoice_sent_count`. Increment `invoice_paid_count` only when Moyasar confirms.
8. Re-run `python scripts/verify_all_dealix.py` → First Invoice Motion 5/5.

When both flip, `ceo_complete: true`.

---

## 3. Anti-pattern · ممنوع

**Never edit the marker files to claim outreach or invoices that did
not happen.** The CEO-completion score is not a vanity metric — it is
the founder's own honest signal. Faking it defeats its purpose and
breaches non-negotiable #4 (no fake or un-sourced claims).

**لا تعدّل ملفات العلامات لتدّعي تواصلًا أو فواتير لم تحدث.** درجة اكتمال
الشركة ليست مؤشر زهو — هي إشارة المؤسس الصادقة لنفسه. تزييفها يُلغي
غرضها ويخرق Non-Negotiable #4 (لا ادّعاءات بلا مصدر).

---

## 4. Cross-links · روابط

- Verifier script: `scripts/verify_all_dealix.py`
- Pre-merge verifier (build only): `scripts/pr235_merge_readiness.sh`
- 11 Non-Negotiables canonical text: `docs/00_constitution/NON_NEGOTIABLES.md`
- The Dealix Promise: `docs/THE_DEALIX_PROMISE.md`
- First Invoice runbook: `docs/ops/FIRST_INVOICE_UNLOCK.md`
- Anchor Partner Outreach kit: `docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md`
- Investor One-Pager: `docs/sales-kit/INVESTOR_ONE_PAGER.md`

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
