# ملخص سجل المخاطر — Dealix Risk Register Summary (AR)

> **هذا ملخص investor/partner-ready لسجل المخاطر.** التفصيل في
> `docs/legal/FOUNDER_RISK_AND_COMPLIANCE_REGISTER_AR.md`.

**الحالة:** مسودة — Phase 1 من Agent #16
**التاريخ:** 2026-06-03

---

## 1. Top 10 Risks (مباشر)

| # | المخاطرة | Impact | Probability | Mitigation | Owner |
| - | --- | --- | --- | --- | --- |
| 1 | Overclaim / ادعاء غير مثبت | High | Medium | claims evidence matrix + founder review | founder |
| 2 | WhatsApp account ban (Meta policy) | High | Medium | mock mode default + 4 governance rules | ops |
| 3 | PDPL breach (data leak) | Critical | Low | DPA + DSAR + breach response plan | DPO (TBD) |
| 4 | LLM cost spike | Medium | Medium | daily cap + model routing | founder |
| 5 | Vendor outage (Railway / AWS) | High | Low | runbook + backup vendor | ops |
| 6 | Single-vendor dependency (WhatsApp Meta) | Medium | Medium | multi-provider chain | ops |
| 7 | Lead gen slowdown | High | Medium | multiple lead sources + warm list | sales |
| 8 | Founder concentration risk | Critical | Medium | document everything + first hire Q1 2027 | founder |
| 9 | Pricing pivot (premature) | Medium | Low | locked pricing until 3+ paying pilots | founder |
| 10 | AI hallucination in client output | High | Medium | evidence + approval + proof ledger | product |

## 2. Risk Domains

### 2.1 Commercial
- Overclaim (1)
- Pricing pivot (9)
- Pilot churn (low — not in top 10)

### 2.2 Operational
- WhatsApp ban (2)
- Vendor outage (5)
- Single-vendor (6)
- Lead gen (7)
- LLM cost (4)

### 2.3 Compliance
- PDPL breach (3)
- ZATCA non-compliance (low)
- SOC 2 missing (medium — only when enterprise)

### 2.4 Talent
- Founder concentration (8)
- First hire delay (medium)

### 2.5 Technical
- AI hallucination (10)
- Data quality (medium)
- API limits (medium)

## 3. Risk Treatment Plan

| Risk # | Treatment | Timeline |
| --- | --- | --- |
| 1 | Ship `CLAIMS_EVIDENCE_MATRIX_AR.md` (Agent #13) | 2026-Q3 |
| 2 | Multi-provider WhatsApp chain | ✅ Done |
| 3 | DPO appointment (TBD) | 2026-Q3 |
| 4 | Daily LLM cost alert | ✅ Done (SLO) |
| 5 | Vendor runbooks | 2026-Q4 |
| 6 | Multi-provider | ✅ Done |
| 7 | Saudi Lead Machine | ✅ Done |
| 8 | First CSM hire | 2026-Q4 / 2027-Q1 |
| 9 | Pricing lock | ✅ Done (PRICING_AND_PACKAGING_V6.md) |
| 10 | Proof ledger | ✅ Done |

## 4. New Risks (TBD)

- EU AI Act compliance (if expanding to EU clients)
- US sanctions on Saudi data
- Currency volatility (SAR/USD)
- Telecom policy changes (CITC)

## 5. Risk Review Cadence

- **Weekly:** operational risks (in founder weekly)
- **Monthly:** commercial risks
- **Quarterly:** full review + risk register update
- **Annually:** strategic + compliance

## 6. المراجع

- `docs/legal/FOUNDER_RISK_AND_COMPLIANCE_REGISTER_AR.md` — main register
- `docs/SECURITY_RUNBOOK.md` — incident response
- `docs/PDPL_BREACH_RESPONSE_PLAN.md` — breach
- `docs/insurance/` (TBD) — D&O, cyber
- `docs/data_room/DATA_ROOM_INDEX_AR.md` — data room
