# Dealix Service Tower — Reality Matrix

> Source: live `https://api.dealix.me/api/v1/services/catalog` (verified 2026-05-03).
> Six bundles registered. Each row below is verified end-to-end via the
> public API. Statuses use the canonical set:
> `PROVEN_LIVE | PROVEN_LOCAL | CODE_EXISTS_NOT_PROVEN | MISSING_OR_EMPTY | BLOCKER | BACKLOG`.

## Matrix

| Service | Contract | Intake | Workflow | Deliverables | Proof Metrics | Safety | API | Frontend | Test | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Free Diagnostic** | id, name_ar, name_en, price=0, cadence=one_time, duration=1d, sla_ar="24 ساعة", safe_policy_ar | 4 questions (`company_name`, `sector`, `goal`, `current_channels`) | not exposed as a state machine — runs as part of operator chat then `service/start` | sectors_scanned, 3 improvement areas, recommended bundle | sectors_scanned, improvement_areas, recommended_bundle | approval-first, no external contact | `GET /api/v1/services/free_diagnostic` + `…/intake-questions` + `POST /api/v1/operator/service/start` | `private-beta.html` cta exists | covered by smoke | **PROVEN_LIVE** |
| **Growth Starter** | id, price=499 SAR, cadence=one_time, duration=7d, sla_ar="Proof Pack خلال 7 أيام", safe_policy_ar="كل draft يمر بموافقتك. لا cold WhatsApp." | 5 questions (`company_name`, `sector`, `ideal_customer`, `avg_deal_sar`, `current_channels`) | service start session created; deliverables generated downstream by `prospect/route` + `personal-operator/messages/draft` | 10 opportunities, AR messages, recommended channel, risk notes, proof pack | `opportunities_created`, `drafts_created`, `risks_blocked`, `proof_pack_url` | approval-first; cold WA blocked at `compliance/check-outreach`; live send gate on `os/test-send` | `GET /api/v1/services/growth_starter` + `POST /api/v1/operator/service/start` | `private-beta.html` | local E2E pass | **PROVEN_LIVE** (contract) + **PROVEN_LOCAL** (E2E) |
| **Data to Revenue** | id, price=1,500 SAR, cadence=one_time, duration=10d, cta=`operator.html` | 4 questions (`source_url_or_file`, `consent_status`, `last_contact_date`, `desired_outcome`) | `data/import/{id}` → `dedupe` → `enrich` → `normalize` → `report` | cleaned/ranked list, contactability, drafts | `rows_cleaned`, `contactability_score`, `drafts_created`, `risks_blocked` | consent_status required; opt-out enforced via SuppressionRecord; cold purchased lists blocked | `services/data_to_revenue` + `data/import` chain | cta route `operator.html` not present in repo (page missing in landing) | smoke covers /catalog, full chain not run | **PROVEN_LIVE (contract)** / **CODE_EXISTS_NOT_PROVEN (full chain)** |
| **Executive Growth OS** | id, price=2,999 SAR/mo, cadence=monthly, duration=30d | 4 questions (`team_size`, `monthly_pipeline_target_sar`, `roles`, `current_kpis`) | daily `personal-operator/daily-brief` + weekly `command-center/proof-pack` | role briefs, weekly proof pack, growth scorecard | `weekly_proof_packs`, `role_briefs_delivered`, `decisions_logged` | role-based decisions; no live customer sends | `services/executive_growth_os` + `role-briefs/daily?role=*` | `growth-os.html` cta | smoke covers brief endpoints | **PROVEN_LIVE (contract + briefs for growth_manager/ceo/customer_success/compliance)** / **BLOCKER for sales_manager (DB)** |
| **Partnership Growth** | id, price=3,000–7,500 SAR, cadence=one_time, duration=30d | 3 questions (`target_partner_type`, `target_geo`, `existing_partners`) | `partners/intake` → `partners/outreach` → `partners/{id}/dashboard` | partner shortlist + scorecard, co-branded Proof Pack, revenue share tracker | `partner_shortlist_size`, `intros_sent`, `co_pilot_started` | no exclusivity early; revenue share only with referral attribution | `services/partnership_growth` + `partners/*` | `agency-partner.html` cta | partner intake works locally | **PROVEN_LIVE (contract)** / **PROVEN_LOCAL (intake)** |
| **Full Growth Control Tower** | id, custom price, cadence=monthly, no fixed duration | n/a (enterprise) | sales-led | full revenue OS | enterprise-defined | gated to enterprise — `support.html#contact` | `services/full_growth_control_tower` (returns 200) | none (sales contact) | not for self-serve | **PROVEN_LIVE (contract)** / **BACKLOG (sales motion)** |

## Definition of Done — per bundle

- **Free Diagnostic:** intake form completed, AR diagnostic delivered ≤24h, recommendation logged.
- **Growth Starter:** 10 opportunities + 6 drafts + 3 follow-ups + Proof Pack signed (HMAC) — proof_pack_url set.
- **Data to Revenue:** import_id with `report` populated AND `compliance/check-outreach` run on every row before any send.
- **Executive Growth OS:** ≥4 weekly proof packs delivered AND role briefs accessible.
- **Partnership Growth:** ≥1 referred customer signed before continuing engagement.
- **Full Growth Control Tower:** enterprise contract — out of scope here.

## Gaps (honest)

1. `data_to_revenue` cta points to `operator.html` which is not in the repo — landing-side breakage. **BACKLOG (or remove the link)**.
2. The `command-center/proof-pack` response does NOT currently include an `hmac` / `signature` field by default — proof packs are not yet self-verifiable. **BACKLOG**.
3. `proof_pack_url` listed as a proof metric for `growth_starter` is not generated as a hosted PDF — `customer/{id}/proof-pack` returns a Markdown template only. **CODE_EXISTS_NOT_PROVEN** for hosted PDF rendering.
4. Pricing claim "499 ريال / 7 أيام" — verified ✅. No "guaranteed" language found in the catalog response; safety language is approval-first throughout. ✅
