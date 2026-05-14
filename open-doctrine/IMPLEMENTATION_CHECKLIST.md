# Implementation Checklist — قائمة التبنّي التشغيلية

_A 30-item checklist any AI operations team can run against its own codebase. Grouped by the 11 commitments. Each item: a yes/no question, the evidence to gather, and a remediation if the answer is "no"._

## EN — How to run this checklist

Walk the checklist top-to-bottom. For each item, the team lead and the technical lead together answer yes/no. "Yes" requires the evidence to be visible — a record, a log line, a test run, a config file. "No" is not a failure; it is a remediation queue. A team is at parity with the doctrine when every item is "yes" and the evidence for each is reproducible within one business day.

## AR — كيف تُنفّذ القائمة

سِر في القائمة من أعلى إلى أسفل. لكل بند، يتفق قائد الفريق والقائد التقني على إجابة نعم/لا. "نعم" تتطلب أن يكون الإثبات مرئياً — سجل، سطر لوج، نتيجة اختبار، ملف إعدادات. "لا" ليست فشلاً بل قائمة معالجة. يكون الفريق متوافقاً مع الدستور حين تكون كل البنود "نعم" والإثبات قابلاً للاسترجاع خلال يوم عمل واحد.

---

## Group 1 — No scraping (3 items)

- [ ] **1.1 Source-binding at ingestion.** Does every contact record carry a Source Passport ID at ingestion time?
  - **Evidence:** schema field present + a query showing 100% coverage on the latest week of records.
  - **Remediation:** add the field, backfill or quarantine the unbound records, re-run the query.
- [ ] **1.2 Scraping pathway audit.** Are there zero code paths in the repository that fetch a third-party UI and parse it as a contact source?
  - **Evidence:** dependency-and-import audit; explicit deny-list of known scraping libraries.
  - **Remediation:** remove the dependency, delete the pathway, replace with a Source-Passport-bound import.
- [ ] **1.3 Quarantine policy.** Is there a documented quarantine path for any record that arrives without a Source Passport?
  - **Evidence:** documented policy + a quarantine table or queue with at least one historical entry.
  - **Remediation:** create the quarantine path; route untraced records into it instead of the main table.

## Group 2 — No cold WhatsApp (2 items)

- [ ] **2.1 Channel-policy gate.** Does every WhatsApp send pass through a channel-policy decision that checks recipient consent?
  - **Evidence:** decision log with one entry per attempted send.
  - **Remediation:** insert the gate; route every send through it.
- [ ] **2.2 Cold-send blocked event.** When the gate blocks a cold send, is a governance event of type "blocked" written and visible in the audit chain?
  - **Evidence:** at least one blocked-send event in the log; the event includes recipient hash, gate decision, and timestamp.
  - **Remediation:** write the event; surface it in the audit chain dashboard.

## Group 3 — No LinkedIn automation (2 items)

- [ ] **3.1 Automation pathway audit.** Are there zero code paths that automate LinkedIn connection requests, messages, scraping, or feed actions?
  - **Evidence:** dependency-and-import audit; explicit deny-list of known LinkedIn-automation libraries and browser-emulation tools used against LinkedIn.
  - **Remediation:** remove the dependency, delete the pathway, replace with customer-owned export ingestion.
- [ ] **3.2 Export-only ingestion.** When LinkedIn data enters the system, does it enter only as a legitimate export the customer owns?
  - **Evidence:** schema field naming the export source + retention rule + a sample audit.
  - **Remediation:** introduce the field, refuse non-export ingestion at the boundary.

## Group 4 — No fake or un-sourced claims (3 items)

- [ ] **4.1 Source-ref on every published claim.** Does every published number, quote, case study, and proof artifact carry a `source_ref`?
  - **Evidence:** schema field present + a publish-time check that rejects records without it.
  - **Remediation:** add the field, add the check, downgrade legacy unsourced records to `draft_only`.
- [ ] **4.2 Sourceless downgrade visible.** When a piece of content lacks a source, is it visibly marked `draft_only` and blocked from public proof?
  - **Evidence:** UI label + a public-surface filter; at least one historical downgrade in the log.
  - **Remediation:** add the label, add the filter, run the downgrade.
- [ ] **4.3 Source retrieval SLO.** Can the team produce the source file for any published claim within one business day?
  - **Evidence:** a stopwatch test: pick a random claim from the last quarter and retrieve its source.
  - **Remediation:** improve the Source Passport storage; until it is reproducible within a day, treat the claim as unsourced.

## Group 5 — No guaranteed sales outcomes (2 items)

- [ ] **5.1 Outcome-language redaction.** Does the customer-safe-language middleware redact "guarantee", "ensure", "we will close X" and equivalent Arabic phrases from drafts before they leave the system?
  - **Evidence:** middleware log with at least one redaction event; a unit test exercising the redaction.
  - **Remediation:** add the middleware; backfill the test.
- [ ] **5.2 Estimate naming.** Are estimates explicitly labeled "estimated / تقديري" wherever they appear in customer-facing output?
  - **Evidence:** label present on at least three customer-facing surfaces (PDF, email, dashboard).
  - **Remediation:** add the label; reject publish on surfaces missing it.

## Group 6 — No PII in logs (3 items)

- [ ] **6.1 Redaction middleware on every log path.** Does every log writer (application logs, friction logs, telemetry, error reporters) pass through a redaction middleware first?
  - **Evidence:** middleware imported by every log path; an integration test forcing a redactable string through each path and asserting it is redacted.
  - **Remediation:** add the middleware; add the test.
- [ ] **6.2 PII categories named.** Does the redaction middleware name the categories it redacts (names, phone numbers, national IDs, emails, addresses) and is the list reviewed quarterly?
  - **Evidence:** category list in code + a review log entry from the most recent quarter.
  - **Remediation:** name the categories; schedule the review.
- [ ] **6.3 Leak response.** Is there a documented P0 response procedure for a PII leak in logs?
  - **Evidence:** the procedure document; a tabletop run within the last twelve months.
  - **Remediation:** write the procedure; run the tabletop.

## Group 7 — No source-less knowledge answers (2 items)

- [ ] **7.1 AI-router source-binding gate.** Does the AI router refuse to answer a business-knowledge question when no Source Passport is bound to the query?
  - **Evidence:** integration test asserting "source required" is returned in the no-source case.
  - **Remediation:** add the gate; add the test.
- [ ] **7.2 Citation in every AI answer.** When the AI does answer, is the Source Passport ID returned alongside the answer and visible to the end user?
  - **Evidence:** UI element showing the source; an API field carrying it.
  - **Remediation:** add the field, add the UI element.

## Group 8 — No external action without approval (3 items)

- [ ] **8.1 Runtime decision on every external action.** Does every external send, charge, publish, or share pass through a runtime decision function?
  - **Evidence:** decision log with one entry per external action.
  - **Remediation:** insert the function; route every external action through it.
- [ ] **8.2 Approver identity logged.** Does every approval log carry approver identity + timestamp + the artifact approved?
  - **Evidence:** an approval-log entry showing the three fields.
  - **Remediation:** add the fields; reject approvals that lack them.
- [ ] **8.3 Bypass attempts rejected.** When a code path attempts to bypass the approval gate, does the runtime return `REQUIRE_APPROVAL` or `BLOCK`?
  - **Evidence:** integration test that exercises a bypass and asserts the return code.
  - **Remediation:** wire the gate; add the test.

## Group 9 — No agent without identity (3 items)

- [ ] **9.1 Agent registry exists.** Is there an agent registry that names every autonomous workflow (name, version, owner, governance scope)?
  - **Evidence:** the registry as code or config; a query listing the registered agents.
  - **Remediation:** create the registry; register existing workflows.
- [ ] **9.2 Workflow start blocks unregistered agents.** At workflow start, does the runtime reject any agent not present in the registry?
  - **Evidence:** integration test that starts an unregistered agent and asserts the rejection.
  - **Remediation:** add the check; add the test.
- [ ] **9.3 Audit chain traces to identity.** Does every action in the audit chain trace back to a registered agent identity?
  - **Evidence:** sample five audit entries; show the identity field is populated and resolvable.
  - **Remediation:** add the field; backfill historical entries or mark them legacy.

## Group 10 — No project without a Proof Pack (4 items)

- [ ] **10.1 Proof Pack template exists.** Is there a 14-section Proof Pack template the team uses for every engagement?
  - **Evidence:** the template file + a sample assembled pack.
  - **Remediation:** create the template.
- [ ] **10.2 Proof score computed.** Is a proof score computed automatically against the 14 sections?
  - **Evidence:** the score function + a sample score on a historical pack.
  - **Remediation:** write the function; backfill scores.
- [ ] **10.3 Closure-gate enforced.** Does engagement closure require an assembled Proof Pack with a non-empty score?
  - **Evidence:** the gate in code or process; an audit of recent closures.
  - **Remediation:** add the gate; refuse closure without a Proof Pack.
- [ ] **10.4 Signed exportable PDF.** Is the Proof Pack delivered to the customer as a signed exportable PDF?
  - **Evidence:** a sample signed PDF from a recent engagement.
  - **Remediation:** add the signing step.

## Group 11 — No project without a Capital Asset (3 items)

- [ ] **11.1 Reusable-artifact ledger exists.** Is there a ledger that records every reusable artifact deposited at engagement closure?
  - **Evidence:** the ledger as code or sheet + at least one historical entry.
  - **Remediation:** create the ledger.
- [ ] **11.2 Closure requires deposit.** Does engagement closure refuse if no reusable artifact is deposited?
  - **Evidence:** the gate in code or process.
  - **Remediation:** add the gate.
- [ ] **11.3 Weekly review.** Is there a weekly review that flags zero-artifact projects as productization failures?
  - **Evidence:** the review meeting record from the last four weeks.
  - **Remediation:** schedule the review; document the first one.

---

## Closing — خاتمة

A team that has answered "yes" to every item, with reproducible evidence, is in alignment with the doctrine. A team that wants the alignment **certified** can request a Dealix review — see [`ADOPTION_GUIDE.md`](./ADOPTION_GUIDE.md) tier 4.

الفريق الذي أجاب "نعم" على كل البنود بإثبات قابل للاسترجاع يكون متوافقاً مع الدستور. الفريق الذي يرغب في **اعتماد** التوافق يطلب مراجعة Dealix — راجع المرحلة الرابعة من [`ADOPTION_GUIDE.md`](./ADOPTION_GUIDE.md).

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
