# First Customer Launch Room
<!-- Wave 8 — Active Document — Update before each customer call -->

> **Usage:** Fill in this document before going live with first paying customer.
> **Language:** Arabic primary, English secondary.
> **Command:** `py scripts/wave8_customer_ready_verify.sh` before proceeding.

---

## §1 — System Status / حالة النظام

| Component | Status | Notes |
|---|---|---|
| API backend | ☐ GREEN / ☐ DEGRADED | Railway health check |
| Database | ☐ GREEN / ☐ DEGRADED | |
| GitHub Actions CI | ☐ PASS / ☐ FAIL | Last run: |
| Wave 8 verifier | ☐ PASS / ☐ FAIL | Run: `bash scripts/wave8_customer_ready_verify.sh` |

---

## §2 — PR / Deploy Status

| Item | Status |
|---|---|
| Last PR merged | #___ — description |
| Railway deploy | ☐ Deployed / ☐ Pending |
| Deploy URL | https://dealix.sa |

---

## §3 — Git SHA

```
git_sha: ___________________________
branch: main
```

---

## §4 — Service Truth Verification

- [ ] Run: `bash scripts/wave7_5_service_truth_verify.sh`
- [ ] All services return: `SERVICE_TRUTH: PASS`
- [ ] Endpoint `/api/v1/health` returns 200

---

## §5 — DPA Status

| Customer | DPA Signed | Signed By | Signed At | Stored |
|---|---|---|---|---|
| _____________ | ☐ YES / ☐ NO | | | Google Drive / Physical |

> ❌ DO NOT proceed without signed DPA.

---

## §6 — Warm Intro Status

- [ ] Customer introduced via warm connection (not cold outreach)
- [ ] Connection: ___________________________
- [ ] Initial contact date: ___________________________
- [ ] Customer vetted: ☐ YES (legitimate business, verified CR/identity)

---

## §7 — Onboarding Wizard

```bash
# Run wizard (live screen-share with customer):
py scripts/dealix_customer_onboarding_wizard.py \
    --customer-handle <handle> \
    --company "<Company Name>" \
    --sector <sector>

# Or dry-run first:
py scripts/dealix_customer_onboarding_wizard.py \
    --customer-handle <handle> \
    --company "<Company Name>" \
    --sector <sector> \
    --dry-run
```

- [ ] Wizard completed successfully
- [ ] Output dir: `data/customers/<handle>/` (gitignored)
- [ ] integration_plan.md generated
- [ ] env_vars_railway.txt generated (founder adds to Railway)

---

## §8 — Integration Plan Location

```
data/customers/<handle>/integration_plan.md
```

- [ ] Integration plan reviewed with customer
- [ ] All 8 channels confirmed

---

## §9 — Credentials Status

Run: `py scripts/dealix_customer_credentials_check.py`

- [ ] All REQUIRED: PRESENT
- [ ] MOYASAR: BLOCKED_BY_POLICY (expected — use bank transfer)
- [ ] LLM key configured (at least one)

---

## §10 — Payment / Billing

| Method | Status | Notes |
|---|---|---|
| Bank transfer | ☐ ACTIVE | Safe default |
| Moyasar | 🚫 BLOCKED | NO_LIVE_CHARGE gate |

- [ ] Payment method confirmed with customer
- [ ] Invoice template ready: `py scripts/dealix_invoice.py`
- [ ] Refund policy communicated (100% in 14 days for Sprint)

---

## §11 — Delivery

- [ ] Sprint scope agreed (documented)
- [ ] Day 0 kickoff scheduled: ___________________________
- [ ] Delivery timeline communicated (10-14 days)
- [ ] Delivery kickoff: `py scripts/dealix_delivery_kickoff.py --customer-handle <handle>`

---

## §12 — Proof Pack

- [ ] Proof pack template ready: `py scripts/dealix_proof_pack.py`
- [ ] Proof publication consent signed (see `docs/wave8/PROOF_PUBLICATION_CONSENT_TEMPLATE.md`)
- [ ] ❌ NO fake metrics / NO inflated numbers

---

## §13 — Case Study Consent

- [ ] `docs/wave8/PROOF_PUBLICATION_CONSENT_TEMPLATE.md` filled and signed
- [ ] Content shown to customer before publishing
- [ ] Stored in: `data/customers/<handle>/proof_publication_consent.md` (gitignored)

---

## §14 — Customer Signal Log

- [ ] Feature requests logged in `data/customers/<handle>/feature_requests.jsonl`
- [ ] Run signal synthesis: `py scripts/dealix_customer_signal_synthesis.py`

---

## §15 — GO / NO-GO Decision

| Gate | Status |
|---|---|
| System health GREEN | ☐ |
| DPA signed | ☐ |
| Warm intro (not cold) | ☐ |
| Onboarding wizard completed | ☐ |
| Credentials check PASS | ☐ |
| Payment method confirmed | ☐ |
| No hard gate violations | ☐ |
| Wave 8 verifier PASS | ☐ |

> **Decision:** ☐ GO — proceed with onboarding  
> **Decision:** ☐ NO-GO — fix blocking items above first

**Founder signature (digital / timestamp):** ___________________________
