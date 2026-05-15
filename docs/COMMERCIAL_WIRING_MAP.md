# Dealix Commercial Wiring Map — خريطة الربط التجاري

_Version 1.0 · Wave 14J_
_Generated: 2026-05-15T06:16:23.252396+00:00_
_Source of truth: `auto_client_acquisition/service_catalog/registry.py` (6 offerings)_

Single source of truth showing how every commercial offer maps to a landing page + a backend endpoint + a delivery surface.

---

## Free AI Diagnostic — التشخيص المجاني للذكاء الاصطناعي

- **Service ID:** `free_diagnostic`
- **Price:** Free
- **Duration:** 2 days
- **Customer journey stage:** discovery

_Rung 1. Free 48h bilingual diagnostic — opens the funnel. Confirmation email auto-sent. Founder reviews every intake within 48h._

**Wiring:**
  - `landing_url`: /diagnostic.html
  - `intake_endpoint`: POST /api/v1/company-growth-beast/diagnostic
  - `lead_capture_endpoint`: POST /api/v1/public/demo-request
  - `delivery_module`: founder reviews via /api/v1/founder/leads
  - `delivery_endpoint`: GET /api/v1/founder/leads
  - `proof_endpoint`: auto_client_acquisition/email/transactional.send_transactional(kind=diagnostic_intake_confirmation)
  - `founder_surface`: /founder-leads.html
  - `next_offer`: sprint

**Non-negotiables enforced (`hard_gates`):**
  - `no_live_send`
  - `no_live_charge`
  - `no_cold_whatsapp`
  - `no_linkedin_auto`
  - `no_scraping`
  - `no_fake_proof`
  - `no_fake_revenue`
  - `no_blast`

**KPI commitment (EN):** Diagnostic delivered within 48 hours of form submission.

**التزام KPI (AR):** نسلّم التشخيص خلال ٤٨ ساعة من تعبئة النموذج.

**Deliverables:**
  - 1-page bilingual sector-fit diagnostic
  - 3 ranked revenue opportunities
  - 1 Arabic message draft
  - 1 best-channel recommendation
  - 1 risk to avoid
  - 1 next-step decision passport

**Refund (EN):** Free — no payment.
**Refund (AR):** مجاني — لا يوجد دفع.

---

## Value Proof Sprint — سبرنت إثبات القيمة

- **Service ID:** `sprint`
- **Price:** 2,500 SAR one-time
- **Duration:** 10 days
- **Customer journey stage:** first_paid

_Rung 2. First paid offer — 2,500 SAR. 10 working days. Proof Pack mandatory. Absorbs the data-cleaning scope. 14-day full refund._

**Wiring:**
  - `landing_url`: /start.html
  - `preview_url`: /sprint-sample.html
  - `intake_endpoint`: POST /api/v1/service-setup/qualify
  - `proposal_endpoint`: POST /api/v1/service-setup/proposal/{customer_id}
  - `checkout_url`: /checkout.html?tier=sprint
  - `checkout_endpoint`: POST /api/v1/payment-ops/invoice-intent
  - `delivery_module`: auto_client_acquisition.delivery_factory.delivery_sprint.run_sprint
  - `delivery_endpoint`: POST /api/v1/sprint/run
  - `sample_endpoint`: GET /api/v1/sprint/sample
  - `proof_endpoint`: auto_client_acquisition.proof_os.proof_pack.assemble
  - `case_safe_endpoint`: GET /api/v1/proof-to-market/case-safe/{engagement_id}
  - `founder_surface`: /founder-dashboard.html
  - `next_offer`: pilot

**Non-negotiables enforced (`hard_gates`):**
  - `no_live_send`
  - `no_live_charge`
  - `no_cold_whatsapp`
  - `no_linkedin_auto`
  - `no_scraping`
  - `no_fake_proof`
  - `no_fake_revenue`
  - `no_blast`

**KPI commitment (EN):** Deliverables shipped within 10 working days. If we do not surface 20 approved opportunities, we keep working at no extra cost until we do.

**التزام KPI (AR):** نسلّم المخرجات خلال ١٠ أيام عمل. إذا لم نُبرز ٢٠ فرصة معتمدة، نواصل العمل بدون مقابل إضافي حتى نصل.

**Deliverables:**
  - Company Brain v1
  - Cleaned + deduplicated lead board
  - Source + data-quality report
  - Top 20 ranked opportunities
  - Decision Passports for the top 5
  - Arabic Draft Pack (10 messages)
  - 7-day follow-up plan
  - Risk + objection map
  - Executive Pack
  - Proof Pack
  - Next-best-offer recommendation

**Refund (EN):** Full 100% refund within 14 days, no questions asked.
**Refund (AR):** استرداد كامل ١٠٠٪ خلال ١٤ يومًا، بدون أسئلة.

---

## Operating Pilot — بايلوت التشغيل

- **Service ID:** `pilot`
- **Price:** 9,500 SAR one-time
- **Duration:** 30 days
- **Customer journey stage:** pilot

_Rung 3. 9,500 SAR. 30-day operating pilot — 4 weekly pipeline cycles with executive reports and a closing Proof Pack._

**Wiring:**
  - `landing_url`: /pricing.html#pilot
  - `intake_endpoint`: POST /api/v1/service-setup/qualify
  - `proposal_endpoint`: POST /api/v1/service-setup/proposal/{customer_id}
  - `checkout_url`: /checkout.html?tier=pilot
  - `checkout_endpoint`: POST /api/v1/payment-ops/invoice-intent
  - `delivery_module`: auto_client_acquisition.delivery_factory.delivery_sprint + scripts/weekly_brief_runner.py
  - `delivery_endpoint`: POST /api/v1/sprint/run
  - `proof_endpoint`: auto_client_acquisition.proof_os.proof_pack.assemble
  - `founder_surface`: /founder-dashboard.html
  - `next_offer`: retainer_managed_ops

**Non-negotiables enforced (`hard_gates`):**
  - `no_live_send`
  - `no_live_charge`
  - `no_cold_whatsapp`
  - `no_linkedin_auto`
  - `no_scraping`
  - `no_fake_proof`
  - `no_fake_revenue`
  - `no_blast`

**KPI commitment (EN):** A weekly pipeline operating cycle across 30 days. If a weekly cycle slips, we extend the work at no extra cost until it completes.

**التزام KPI (AR):** تشغيل أسبوعي للـ pipeline على مدى ٣٠ يومًا. إذا تأخّرت دورة أسبوعية، نمدّد العمل بدون مقابل إضافي حتى تكتمل.

**Deliverables:**
  - 4 weekly pipeline operating cycles
  - Weekly lead board + scoring refresh
  - Weekly Arabic Draft Pack
  - Opportunity + meeting tracker
  - Weekly executive report
  - Support + operations insights
  - Closing Proof Pack
  - Next-best-offer recommendation

**Refund (EN):** 75% refund if the KPI commitment is unmet within 45 days.
**Refund (AR):** استرداد ٧٥٪ إذا لم يتحقق التزام KPI خلال ٤٥ يومًا.

---

## Managed Operations Retainer — التشغيل المُدار الشهري

- **Service ID:** `retainer_managed_ops`
- **Price:** 6,000–18,000 SAR / month
- **Duration:** 120 days
- **Customer journey stage:** retainer

_Rung 4. 6,000–18,000 SAR / month retainer engine. Monthly operating cadence with weekly audits, support insights, and a board pack at the upper band. Renewal after confirmed cycles._

**Wiring:**
  - `landing_url`: /pricing.html#retainer
  - `intake_endpoint`: POST /api/v1/service-setup/qualify
  - `proposal_endpoint`: POST /api/v1/service-setup/proposal/{customer_id}
  - `checkout_url`: /checkout.html?tier=retainer
  - `checkout_endpoint`: POST /api/v1/payment-ops/invoice-intent
  - `delivery_module`: scripts/weekly_brief_runner.py + scripts/monthly_cadence_runner.py
  - `delivery_endpoint`: GET /api/v1/customer-portal/{handle}/workspace
  - `proof_endpoint`: GET /api/v1/value/{handle}/report/monthly
  - `adoption_endpoint`: GET /api/v1/customer-success/{handle}/adoption-score
  - `renewal_module`: auto_client_acquisition.payment_ops.renewal_scheduler
  - `founder_surface`: /customer-portal.html?handle={customer}
  - `next_offer`: enterprise_custom_ai

**Non-negotiables enforced (`hard_gates`):**
  - `no_live_send`
  - `no_live_charge`
  - `no_cold_whatsapp`
  - `no_linkedin_auto`
  - `no_scraping`
  - `no_fake_proof`
  - `no_fake_revenue`
  - `no_blast`

**KPI commitment (EN):** We commit to a +20% reply-rate lift within 4 months. If it is not reached, we keep working at no extra cost until it is.

**التزام KPI (AR):** نلتزم برفع معدل الردود +٢٠٪ خلال ٤ أشهر. إن لم يتحقق، نواصل العمل بدون مقابل إضافي حتى يتحقق.

**Deliverables:**
  - Monthly operating cadence (revenue + support + ops + delivery + proof)
  - Weekly pipeline audits
  - Daily approval queue
  - Arabic Draft Pack (≥20 messages / month)
  - Support insights (included)
  - Monthly Proof Pack
  - Monthly executive summary + board pack (upper band)
  - Expansion recommendation

**Refund (EN):** Pro-rata refund of unused months if the KPI commitment is unmet.
**Refund (AR):** استرداد تناسبي للأشهر غير المستخدمة عند عدم تحقيق التزام KPI.

---

## Enterprise & Custom AI — المؤسسات والذكاء الاصطناعي المخصّص

- **Service ID:** `enterprise_custom_ai`
- **Price:** 45,000–120,000 SAR one-time
- **Duration:** 120 days
- **Customer journey stage:** enterprise

_Rung 5. 45,000–120,000 SAR. Custom AI build + governance program. Scope, milestones, and refunds fixed in a signed SOW._

**Wiring:**
  - `landing_url`: /pricing.html#enterprise
  - `intake_endpoint`: POST /api/v1/service-setup/requests
  - `checkout_url`: founder-issued
  - `checkout_endpoint`: POST /api/v1/payment-ops/invoice-intent
  - `delivery_module`: auto_client_acquisition.executive_command_center + custom SOW build
  - `delivery_endpoint`: GET /api/v1/executive-command-center/*
  - `proof_endpoint`: GET /api/v1/audit/{handle}/control-graph/markdown
  - `trust_pack_endpoint`: GET /api/v1/value/trust-pack/{handle}/pdf
  - `founder_surface`: /founder-dashboard.html

**Non-negotiables enforced (`hard_gates`):**
  - `no_live_send`
  - `no_live_charge`
  - `no_cold_whatsapp`
  - `no_linkedin_auto`
  - `no_scraping`
  - `no_fake_proof`
  - `no_fake_revenue`
  - `no_blast`

**KPI commitment (EN):** Scope, milestones, and acceptance criteria are fixed in a written SOW before work begins, and we commit to the SOW milestones.

**التزام KPI (AR):** نثبّت النطاق والمراحل ومعايير القبول في SOW مكتوب قبل بدء العمل، ونلتزم بمراحل الـ SOW.

**Deliverables:**
  - Discovery + AI readiness review
  - Custom workflow + agent design
  - Integrations scope + data governance
  - PDPL-aware data review
  - Build + iteration cycles
  - Team training + handover
  - AI governance program + audit pack
  - SLA definition

**Refund (EN):** Per a signed SOW with cancellation terms — lawyer-reviewed.
**Refund (AR):** وفق عقد SOW موقّع بشروط إلغاء — يُراجَع قانونيًا.

---

## Agency Partner OS — نظام شريك الوكالة

- **Service ID:** `agency_partner_os`
- **Price:** Custom
- **Duration:** 0 days
- **Customer journey stage:** channel

_Channel offer. 5K SAR / closed deal + 30% commission first year. Partner Covenant enforced: no unsafe automation, no guaranteed claims._

**Wiring:**
  - `landing_url`: /agency-partner.html
  - `intake_endpoint`: POST /api/v1/public/partner-application
  - `checkout_url`: founder-issued
  - `delivery_module`: auto_client_acquisition.partnership_os.referral_store
  - `delivery_endpoint`: POST /api/v1/referrals/create + /redeem + /{code}/convert
  - `proof_endpoint`: GET /api/v1/founder/dashboard
  - `founder_surface`: /founder-leads.html
  - `covenant_doc`: docs/40_partners/PARTNER_COVENANT.md

**Non-negotiables enforced (`hard_gates`):**
  - `no_live_send`
  - `no_live_charge`
  - `no_cold_whatsapp`
  - `no_linkedin_auto`
  - `no_scraping`
  - `no_fake_proof`
  - `no_fake_revenue`
  - `no_blast`

**KPI commitment (EN):** 30% commission for the first paid year per referred customer. Never publish proof without signed consent.

**التزام KPI (AR):** نلتزم بـ٣٠٪ عمولة لأول سنة من كل عميل محوّل، ولا نشر proof بدون موافقة موقّعة.

**Deliverables:**
  - Partner intake doc
  - Co-branded diagnostic for the partner's clients
  - Client Proof Sprint (per client)
  - Proof Pack (per client)
  - Renewal / upsell pack
  - Partner revenue tracking
  - 30% commission tracking

**Refund (EN):** Formal contract with cancellation terms — lawyer-reviewed.
**Refund (AR):** عقد رسمي بشروط الإلغاء — يُراجَع قانونيًا.

---

## Cross-cutting infrastructure

- Lead inbox: `auto_client_acquisition/lead_inbox.py`
- Transactional email (9 whitelisted kinds): `auto_client_acquisition/email/transactional.py`
- Sales qualification: `auto_client_acquisition/sales_os/qualification.py`
- Proposal renderer: `auto_client_acquisition/sales_os/proposal_renderer.py`
- Sprint orchestrator: `auto_client_acquisition/delivery_factory/delivery_sprint.py`
- Renewal scheduler: `auto_client_acquisition/payment_ops/renewal_scheduler.py`
- Proof Pack assembler: `auto_client_acquisition/proof_os/proof_pack.py`
- Trust Pack: `auto_client_acquisition/trust_os/trust_pack.py`
- Audit + Evidence Control Plane: `auto_client_acquisition/auditability_os/`, `evidence_control_plane_os/`
- Agent OS + Secure Runtime: `auto_client_acquisition/agent_os/`, `secure_agent_runtime_os/`
- Benchmark engine: `auto_client_acquisition/benchmark_os/`
- PDF renderer: `auto_client_acquisition/proof_to_market/pdf_renderer.py`
- Referral persistence: `auto_client_acquisition/partnership_os/referral_store.py`

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
