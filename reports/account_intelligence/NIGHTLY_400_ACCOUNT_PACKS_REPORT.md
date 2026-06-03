# Nightly Account Packs Report

*Run date: 2026-06-03 | Sample run: 10 packs | Target: 400/night*
*Generated/validated by `scripts/validate_account_intelligence.py` (17/17 ✅)*

---

## 1. Run summary

| Metric | Value |
|--------|------:|
| Packs produced | 10 (sample) |
| Nightly target | 400 |
| Validated against schema | 10/10 ✅ |
| draft_ready | 9 |
| researched / held (no contact) | 1 |
| With ≥1 public contact channel | 9 |
| Missing contact (held) | 1 |

---

## 2. Distribution by system (sample)

| System | Packs (sample) | Nightly target |
|--------|---------------:|---------------:|
| revenue_os | 2 | 100 |
| followup_recovery_os | 2 | 90 |
| executive_command_os | 2 | 70 |
| whatsapp_client_os | 2 | 70 |
| proposal_proof_os | 2 | 70 |
| **Total** | **10** | **400** |

---

## 3. Evidence level mix

| Evidence | Packs |
|----------|------:|
| L2 | 5 |
| L1 | 4 |
| L0 | 1 |
| L3 / L4 | 0 |

> كل باقات L0/L1 (5) اجتازت فحص اللغة الاحتمالية وخلوّها من الادعاءات الجازمة.

---

## 4. All packs (this run)

| ID | Company | System | Ev. | CC | Score | Tier | Status |
|----|---------|--------|----|----|------:|------|--------|
| ACC-005 | TrainMe KSA | whatsapp_client_os | L2 | CC2 | 88 | top_20_send | draft_ready |
| ACC-006 | BrightSmile Dental Clinic | whatsapp_client_os | L2 | CC2 | 88 | top_20_send | draft_ready |
| ACC-007 | TechVenture Partners | executive_command_os | L2 | CC2 | 88 | top_20_send | draft_ready |
| ACC-009 | LegalEdge SA | proposal_proof_os | L2 | CC2 | 88 | top_20_send | draft_ready |
| ACC-001 | Digital Rise Agency | revenue_os | L2 | CC1 | 83 | top_20_send | draft_ready |
| ACC-003 | Growth Labs SA | followup_recovery_os | L1 | CC2 | 68 | top_30_call | draft_ready |
| ACC-010 | CloudShift Consulting | proposal_proof_os | L1 | CC2 | 68 | top_30_call | draft_ready |
| ACC-002 | Nexus IT Solutions | revenue_os | L1 | CC1 | 63 | top_100 | draft_ready |
| ACC-004 | LearnFast Academy | followup_recovery_os | L1 | CC1 | 63 | top_100 | draft_ready |
| ACC-008 | Alpha Consulting Group | executive_command_os | L0 | CC0 | 29 | hold | researched |

---

## 5. Gates passed

```txt
✅ schema validation (10/10)
✅ every pack has recommended_system
✅ role matches system (targeting matrix)
✅ no invented contact fields
✅ missing contact handled gracefully (ACC-008 held)
✅ L0/L1 hedged, no absolute claims
✅ no guarantee language
✅ no Re:/Fwd:, no internal-name leaks
```

---

## 6. Next

- مرشحو الإرسال (5) و الاتصال (4): `TOP_100_ACCOUNT_QUEUE.md`
- غياب التواصل (1): `../contacts/MISSING_CONTACTS_REVIEW.md`
- قرار المؤسس اليومي: `../founder/DAILY_SUPER_COMMAND.md`
