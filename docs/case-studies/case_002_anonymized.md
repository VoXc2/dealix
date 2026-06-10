# Case 002 — Saudi Professional Training Academy (Anonymized) / أكاديمية تدريب مهني سعودية

> **This is a hypothetical / case-safe template based on the Dealix delivery methodology. No real customer is implied or named.**
> **هذا نموذج افتراضي مبني على منهجية ديليكس، ولا يُقصد به أي عميل حقيقي.**

Cross-link: [SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md), [case_001_anonymized.md](./case_001_anonymized.md), [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md).

---

## Customer profile — ملف العميل

- **Sector:** Saudi professional training academy / أكاديمية تدريب مهني (corporate upskilling).
- **Size:** small-mid (estimated 12–25 staff, instructor-led + digital).
- **Region:** Jeddah, with corporate clients across multiple Saudi cities.
- **Anonymization:** real name, course catalogue, and revenue figures are not disclosed under the case-safe summary policy.

---

## Problem — المشكلة

Unlike Case 001, this customer's **data was already clean**. The CRM had been migrated within the prior six months and discipline was strong. The actual gap was different: the academy could not classify its corporate-client base by *sector taxonomy* (banking-ops training vs. hospitality training vs. construction safety). Without a sector taxonomy, outreach was generic, and the academy could not stand up a recurring outreach cadence without a clear owner-of-record for the workflow.

البيانات كانت نظيفة، لكن لم يكن للأكاديمية تصنيف قطاعي للعملاء المؤسسين، ولم يكن لها مالك مُعيَّن لتشغيل سير العمل بشكل دوري.

---

## Inputs — المدخلات

- **One CSV** with **640 corporate-account records**, already deduped and field-normalized by the client.
- A signed Source Passport: `owner=client`, `source_type=crm_export`, `allowed_use=sprint_only_and_retainer_renewable`, `pii_flag=true`, `retention_days=180`.
- One named workflow owner: the Head of Corporate Partnerships.
- Primary workflow declared: sector-segmented quarterly corporate outreach.

---

## Work performed — الأعمال المُنفَّذة

1. **Source Passport agreed** with retainer-renewable clause from day one (which later mattered).
2. **DQ baseline:** **DQ = 78/100** — already strong. Time was redirected from cleaning to *taxonomy*.
3. **Sector taxonomy built:** `revenue_os.account_scoring` was extended with a new feature dimension — sector cluster — populated from declared client industry plus inferred features (training course history, contract size band). The taxonomy produced **6 sector clusters** with explainable membership rules.
4. **Top 10 accounts ranked per sector cluster** (60 ranked accounts total internally; 10 surfaced as the headline deliverable, matching scope).
5. **Draft pack:** **5 Arabic drafts + 5 English drafts**, each parameterized by sector cluster (banking-ops drafts emphasized compliance training; hospitality drafts emphasized peak-season readiness).
6. **Governance review:** **0 BLOCKED**, **1 REDACTED** (an instructor name accidentally embedded in a preview). The cleanliness of the data reduced governance friction relative to Case 001.

---

## Outputs — المخرجات

- **Proof Pack** assembled with all 14 sections, **proof_score = 76**.
- **Value tier mapped:** `revenue_ops_lite` (Tier 2.5 — borderline between sales_support and full revenue_ops; documented as a sub-tier observation).
- **Capital assets registered (2):**
  1. **Sector taxonomy schema for Saudi professional training** — six-cluster definition with explainable inclusion rules. Reusable for any future training-sector engagement.
  2. **Retainer-renewable Source Passport clause template** — became the default for all subsequent retainer engagements (productization signal).
- **Bilingual deliverables:** AR proof report, EN proof report, sector taxonomy reference (AR+EN), governance decisions CSV.

---

## Observed value — القيمة المُلاحَظة (Estimated, not verified)

- **Sector clusters established:** 6 (previously: 0 formal clusters).
- **Drafts personalized per cluster:** 10 (previously: 1 generic template reused for everyone).
- **Governance interventions:** 1 redaction, 0 blocks — indicating the methodology runs lighter on clean data.
- **Retainer conversion:** this customer became the **first Managed Revenue Ops retainer (2,999 SAR/month)** the week following Sprint close-out. Estimated value of retainer-readiness work captured in `value_ledger.tier=revenue_ops_lite`.

**These figures describe what the sprint produced and how the engagement progressed. They do not claim a specific revenue outcome for the client.**

---

## Limitations — حدود هذه الحالة

- **Clean-data bias:** the methodology worked smoothly *because* the data was already clean. The case does not generalize to customers with DQ < 60.
- **Taxonomy is sector-bound:** the six-cluster taxonomy is specific to professional training; it does not transfer wholesale to, say, B2B advisory.
- **Estimated retainer value, not lifetime:** the customer entered the retainer at the end of the sprint window; long-term retention is a forward-looking estimate, not a verified figure.
- **Anonymized for client confidentiality:** real corporate clients of the academy, instructor names, and course-catalogue specifics are intentionally withheld.

---

## Next step — الخطوة التالية

The retainer began the week after sprint delivery, with the same Source Passport renewed under the retainer clause. Retainer scope: monthly taxonomy refresh, quarterly draft-pack regeneration, ongoing governance review. This case is the reference for the **Sprint-to-Retainer conversion path** documented in [SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md) Day 6.

أصبحت هذه الحالة هي المرجع لمسار التحويل من السبرنت إلى عقد الاحتفاظ الشهري.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
