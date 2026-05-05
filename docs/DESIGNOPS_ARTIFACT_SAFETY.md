# DesignOps Artifact Safety

Every DesignOps artifact passes through a `safety_gate` before it is allowed
to be exported, and `safe_to_send` defaults to **False** on every manifest.
This doc is the founder-facing reference for the gate's rules.

## What the safety gate checks
1. **Forbidden-token scan.** The 8 tokens below (case-insensitive,
   AR + EN forms) are matched against rendered markdown + HTML.
2. **Marketing-claim scan.** Phrases like "the best", "guaranteed results",
   "#1 in Saudi Arabia" are flagged even when they don't contain a token
   verbatim.
3. **Real-customer-name scan.** Cross-checks the artifact body against the
   internal customer registry; any match blocks `safe_to_send`.
4. **PDPL alignment.** Customer data appearing in the artifact must have a
   matching `consent_event` in `proof_ledger`. Missing consent → block.
5. **Bilingual completeness.** For `mode=bilingual` skills, both AR and EN
   blocks must be present and non-empty.
6. **Forbidden-claim ledger.** Any phrase already on the
   `MASTER_NO_GUARANTEED_CLAIMS` list (see `test_no_guaranteed_claims.py`)
   blocks the artifact.

If any check fails, the manifest stays `safe_to_send=False` and the
exporter still writes the file locally — but the founder review banner
remains visible at the top of the artifact.

## Why `safe_to_send=False` is the default
- A generator is a probabilistic system. The gate is a deterministic one.
  Defaulting to `False` means a single bug in either layer cannot leak a
  bad artifact to a real customer.
- It forces a human read-through every time. This is the cost of trust at
  the early-customer stage, and it is intentional.
- Reverting from "sent" is expensive (apology, redaction, possible PDPL
  incident). Reverting from "not yet sent" is free.

## How to flip `safe_to_send=True`
1. **Manual founder review.** Open the rendered HTML in a local browser.
   Read it end-to-end, AR and EN.
2. **Redaction confirmed.** No real customer name, no PII that lacks
   consent, no internal financial figure that should not leave.
3. **Forbidden-token re-scan passes.** Re-run the gate after any edit.
4. **Founder explicit flip.** Edit the manifest JSON: set
   `safe_to_send: true` and add `reviewed_by: <founder_handle>` plus
   `reviewed_at: <iso8601>`. The exporter does not flip this flag — only
   the founder does, by hand.
5. **Send by hand.** No automation sends the artifact. The founder copies
   the markdown into the chosen channel (email, WhatsApp, Notion).

## PDPL alignment
- **Consent.** Customer data appears in an artifact only if a matching
  `consent_event` is recorded in `proof_ledger`.
- **Opt-out.** If a customer has opted out, the gate refuses to render
  any new artifact about them and emits an audit event.
- **Audit trail.** Every export (and every `safe_to_send` flip) is logged
  to `docs/proof-events/*.jsonl` with `actor`, `artifact_id`,
  `safe_to_send_before`, `safe_to_send_after`.
- **Data minimization.** Generators receive only the fields they declare
  in their input schema. The brief builder strips everything else.

## The 8 forbidden tokens — bilingual rephrasing
| Token (EN) | AR equivalents | Why blocked | Acceptable rephrasing (EN / AR) |
|---|---|---|---|
| `guaranteed` | مضمون، ضمان | Implies an outcome promise we cannot enforce. | "we aim to" / "نسعى إلى" |
| `best` | الأفضل، الأحسن | Superlative claim without independent proof. | "a strong fit for" / "خيار مناسب لـ" |
| `#1` | الأول، رقم 1 | Ranking claim without independent proof. | "an early entrant in" / "من المبكرين في" |
| `free forever` | مجاني للأبد | Misleads on commercial terms. | "no fee for the pilot" / "لا رسوم على الباكورة" |
| `risk-free` | بدون مخاطر | Implies zero downside. | "low-commitment pilot" / "باكورة بالتزام محدود" |
| `100%` | 100٪، مئة بالمئة | Implies certainty. | "in our sample" / "في عينتنا" |
| `instant` | فوري، فورًا | Implies a delivery time we cannot honor. | "within <N> business days" / "خلال <N> أيام عمل" |
| `certified` | معتمد، شهادة | Implies a third-party stamp we don't hold. | "documented internally" / "موثق داخليًا" |

## Incident response — forbidden token leaks into a draft
If a draft artifact contains a forbidden token and the gate did not catch
it:
1. **Stop.** Do not flip `safe_to_send`. Do not send.
2. **Quarantine the artifact.** Move the file out of
   `docs/designops/exports/` into a local-only `quarantine/` folder.
3. **Open an incident.** File a row in `MASTER_CLOSURE_EVIDENCE_TABLE`
   with `Layer=designops/safety_gate`, `Status=red`,
   `Evidence=<artifact_id>`.
4. **Add a regression test.** Drop the offending phrase into
   `tests/test_no_guaranteed_claims.py` so the next gate run catches it.
5. **Patch the gate.** Update the forbidden-token list or claim regex.
6. **Re-run the full bundle.** `pytest --no-cov -q` must be green
   before any new artifact is generated.
7. **Audit the day's exports.** Any artifact written after the leak
   started must be re-scanned.

If the artifact was already sent to a customer:
8. **Notify the customer in writing**, retract the claim, and log the
   event in `proof_ledger` with `event_type=correction_sent`.
9. **Review PDPL exposure** with counsel if the leak involved PII.
