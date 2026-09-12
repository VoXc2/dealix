# OP2 Arm Activation Packs — 2026-09-12

OP2 lane. All content is research/draft-only. No new arm, no new permanent agent,
no pipeline, no revenue, no external effect. `L5_EXECUTED=NONE`.

## Purpose

Turn fresh, independently-verified Saudi official signals into truth-safe
commercial activation packs bound to arms that **already exist** in the canonical
44-arm registry (`config/company/dealix_arm_registry.json`). Research is never a
relationship, and research alone never changes an arm's state.

## Official signals used (verified from source)

| Signal | Authority | Observed | Deadline / freshness |
|---|---|---|---|
| ZATCA Wave 25 integration-phase criteria; VAT-subject revenue > SAR 187,500 in 2022–2025 | ZATCA | 2026-07-24 | integrate by **2027-02-01** |
| CST Awareness Guide for AI Adoption in Technology Companies (internal ops, customer-facing, AI agents; 5 readiness dimensions) | CST | 2026 (Year of AI) | guide, fresh to 2027-06 |
| NCA Cybersecurity Controls for private-sector non-CNI entities | NCA | 2025-12-28 | fresh to 2026-12-28 |
| NCA ECC-2:2024 + implementation guidance | NCA | ongoing | fresh to 2027 |
| SAMA open-banking licensing commenced | SAMA | 2026-03-26 | fresh to 2027-03-26 |
| SDAIA AI governance package + PDPL enforcement | SDAIA | 2026 | fresh to 2027 |

Sources: `data/commercial/op2_market_intelligence_wave_v1.json` (30 receipts,
all `authority=false`, `allowed_use=INTERNAL_RESEARCH_ONLY`).

## Packs (existing arms only)

### A. `OP2-PACK-A-FATOORA` — arms **ARM-001, ARM-016**
Free D0–D2 applicability/readiness diagnostic → qualified discovery →
customer-specific implementation / managed exception operations.
Deadline driver: ZATCA Wave 25 (1 Feb 2027).
Boundary: **no tax/legal certification claim**; a licensed firm partner is used
only if a certification opinion is required.

### B. `OP2-PACK-B-GOVERNED-AI` — arms **ARM-002, ARM-006, ARM-008**
AI adoption / governance / agent-reliability readiness for Saudi tech/SaaS:
AI inventory, control/eval/approval/human-oversight/resilience evidence, and a
remediation pack. Driver: CST AI Adoption Guide + SDAIA guidance + PDPL.
Boundary: **no certification or legal opinion**; evidence engineering only.

### C. `OP2-PACK-C-MARKET-ACCESS-CYBER` — arms **ARM-003, ARM-028**
NCA evidence-readiness (NCNICC/ECC/CCC applicability, evidence matrix, gap map)
with a documented partner/specialist route.
Boundary: **no government-access or accreditation claim**; default
`PARTNER_OR_NO_BID` when specialist authority is required.

### D. `OP2-PACK-D-OPEN-BANKING` — arm **ARM-023** (VALIDATE)
SAMA open-banking is **VALIDATE / partner-first**. Dealix must **never** represent
itself as a SAMA-licensed provider (`licensed_provider_claim=NONE_NEVER`).
Deliverables are scoped strictly as non-licensed technical support behind a
licensed partner.

Each pack includes: ICP/buyer/problem hypotheses · free D0–D2 diagnostic
(card-free, no ROI promise) · qualification gates · Arabic/English discovery
questions · proposal skeleton (`QUOTE_AFTER_QUALIFIED_DISCOVERY`, no public fixed
price) · acceptance criteria · proof requirements · delivery runbook · stop-loss ·
partner/regulatory boundary · bilingual content/SEO drafts
(`publish_authority=false`) · exact next evidence required.

## 44-arm priority view (transparent, research-only)

`ranking` in `data/commercial/op2_arm_activation_packs_v1.json` scores all 44 arms
on: official signal strength · relationship evidence (0 — none verified) ·
time-to-cash · delivery readiness · cost/margin proxy · founder-minutes factor ·
regulatory risk.

- `state_changes_applied = 0`
- `active_deep_locked_top3 = [ARM-001, ARM-002, ARM-003]` — **unchanged**
- every row: `state_change_allowed=false`, `disposition=RESEARCH_ONLY_NO_STATE_CHANGE`
- `deep_wip_max = 3`

Research can move only LIGHT/HOLD/RADAR prioritisation. It can never silently
displace the current ACTIVE_DEEP Top-3; that requires real customer/economic
evidence.

## Verification

```
DEALIX_OP2_ARM_PACKS_VERDICT=PASS
pytest tests/test_op2_arm_activation_packs.py  → 14 passed
```

Truth laws enforced by tests/verifier: exactly 44 arms · 20 sectors routed ·
D0–D2 free/no card · no public fixed prices · no invented customer/intent/
consent/pipeline/revenue (payment ≠ revenue) · no cold WhatsApp / mass LinkedIn ·
no stale iMini $150 or placeholder action hash as send authority · all external
effects false · `L5_EXECUTED=NONE`.

## Next evidence required

1. Confirm ZATCA notification status per prospect (Pack A).
2. Confirm AI/agent systems per prospect and which official guidance they track (Pack B).
3. Confirm NCNICC applicability per prospect; identify accredited partners (Pack C).
4. Identify licensed/partnering open-banking providers from SAMA primary notices (Pack D).
5. Reconcile iMini Gmail truth only from canonical local evidence; exact payload
   not available → **HOLD**, no stale amount, no placeholder hash.
