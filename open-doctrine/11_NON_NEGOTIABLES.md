# The 11 Non-Negotiables

These are the operating commitments that distinguish governed AI operations from generic AI tool usage. Each is stated as a refusal — what will not happen — because doctrine is enforced by what is refused, not by what is announced.

## 1. No Scraping
No automated extraction of data from sources whose terms of service or owner consent forbid it. Data acquisition relies on client-owned sources, paid licensed sources, and explicit consent.

## 2. No Cold WhatsApp Automation
No automated WhatsApp outreach to recipients who have not opted in. Messaging respects local regulation and recipient consent.

## 3. No LinkedIn Automation
No bots, scrapers, or automated connection/message flows on LinkedIn. Outreach is human-authored, human-sent, and consent-aware.

## 4. No Guaranteed Sales Outcomes
No claim of guaranteed revenue, lead count, or conversion rate. Public claims require verified proof.

## 5. No Source-less AI Output
No AI output is presented to a client or buyer without a source passport that names where input data came from and under what permission.

## 6. No External Action Without Approval
No AI agent takes any external-facing action — sending, posting, submitting, paying, contacting — without a logged human approval.

## 7. No Agent Without Identity
No AI agent operates without an explicit identity, owner, scope, and audit trail.

## 8. No Public Case Study Without Verified Proof
No case study, customer logo, or success claim is published without verified proof and client written approval.

## 9. No Autonomous Upsell
No AI agent or automation triggers an upsell, contract change, or pricing change autonomously.

## 10. No Capital Asset Without Provenance
No artifact is registered as a capital asset without provenance, ownership, and a reproducibility note.

## 11. No Unsafe Growth
No growth motion that requires violating non-negotiables 1-10, regardless of revenue impact.

## How These Are Enforced
- Doctrine tests in CI for the implementer (Dealix uses test_doctrine_*).
- Source Passport requirement at the data layer.
- Approval gate at the action layer.
- Proof Pack requirement at the claim layer.
- Public verification endpoints where machine-readable.
