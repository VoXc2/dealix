# Control Mapping — جدول الضوابط

_The bridge between the abstract doctrine and the Dealix reference implementation. Adopters writing their own tests map the abstract test category to their own test paths._

## EN — How to read this table

Four columns per row: the Non-Negotiable, the Operating Control that enforces it in production, the Evidence Artifact that proves a single execution passed the control, and a Test Example pointing to a Dealix-specific reference test path. Adopters re-map column four to their own paths; columns one through three are the doctrine itself.

## AR — كيف تقرأ الجدول

أربعة أعمدة لكل صف: الالتزام، الضابط التشغيلي الذي ينفّذه في الإنتاج، أثر الإثبات الذي يُثبت اجتياز تنفيذ واحد، ومثال اختبار يُشير إلى مسار اختبار مرجعي في Dealix. المتبنّون يُعيدون ربط العمود الرابع بمساراتهم؛ أما الأعمدة الأولى إلى الثالثة فهي نص الدستور نفسه.

---

## The Control Mapping — الجدول

| # | Non-Negotiable | Operating Control | Evidence Artifact | Test Example (Dealix reference) |
|---|---|---|---|---|
| 1 | **No scraping** / لا تجريف بيانات | Source-binding gate at data-ingestion boundary; non-sourced records quarantined. | Source Passport record per contact. | `tests/test_no_scraping_engine.py` |
| 2 | **No cold WhatsApp** / لا واتساب بارد | Channel-policy gate at the send layer; cold sends produce a blocked governance event. | Channel Policy decision log entry. | `tests/test_no_cold_whatsapp.py` |
| 3 | **No LinkedIn automation** / لا أتمتة LinkedIn | Channel-policy refusal at PR review and at runtime. | Channel Policy decision log entry. | `tests/test_no_linkedin_automation.py` |
| 4 | **No fake or un-sourced claims** / لا ادعاءات بلا مصدر | Claim-review gate on every outbound artifact; sourceless content downgraded to `draft_only`. | Claim review log + Source Passport. | `tests/test_no_guaranteed_claims.py` |
| 5 | **No guaranteed sales outcomes** / لا ضمانات مبيعات | Customer-safe-language redaction middleware rewrites or rejects outcome-promise phrasing. | Claim review log entry. | `tests/test_no_guaranteed_claims.py`, `tests/test_customer_safe_product_language.py` |
| 6 | **No PII in logs** / لا PII في السجلات | Redaction middleware on every log path; raw PII rejected before log writer. | Redaction middleware log. | `api/middleware/bopla_redaction.py` (module-level test fixtures), `auto_client_acquisition/friction_log/sanitizer.py` |
| 7 | **No source-less knowledge answers** / لا إجابة بلا مصدر | Source-binding gate at AI router; missing source returns "source required". | Source Passport record per AI call. | `tests/test_no_source_passport_no_ai.py` |
| 8 | **No external action without approval** / لا فعل خارجي بلا موافقة | Runtime decision function on every external action; bypass returns `REQUIRE_APPROVAL` or `BLOCK`. | Approval record + Audit Chain entry. | `tests/test_pii_external_requires_approval.py`, `auto_client_acquisition/governance_os/runtime_decision.py` |
| 9 | **No agent without identity** / لا عميل ذكي بلا هوية | Agent-identity check at the registry at workflow start. | Agent Card + Agent Registry record. | `auto_client_acquisition/agent_os/agent_registry.py`, `auto_client_acquisition/secure_agent_runtime_os/four_boundaries.py` |
| 10 | **No project without a Proof Pack** / لا مشروع بلا Proof Pack | Proof-pack required-gate at engagement closure; invoice blocked without it. | Proof Pack PDF (14 sections). | `tests/test_proof_pack_required.py`, `auto_client_acquisition/proof_os/proof_pack.py` |
| 11 | **No project without a Capital Asset** / لا مشروع بلا أصل رأسمالي | Reusable-artifact ledger gate at closure; zero-artifact projects flagged in weekly review. | Reusable-artifact ledger record. | `auto_client_acquisition/capital_os/capital_ledger.py` |

---

## Mapping notes — ملاحظات الربط

### Why test paths are Dealix-specific in column four

The abstract doctrine names a **category** of test (e.g., "source-binding test", "channel-policy test", "approval-gate test"). Column four of this table names the **Dealix reference test file** that implements the category. This file is the **adoption bridge**: it lets an adopter read "approval-gate test" and see what one concrete implementation looks like, then write their own test in their own framework against their own code paths.

### EN — Adopter rewrite procedure

1. Copy this table into the adopter's own repository.
2. Keep columns 1, 2, 3 unchanged (this is the doctrine).
3. Replace column 4 entries with the adopter's own test paths.
4. For any row where the adopter has no implementation, write the test before claiming the row as adopted.

### AR — إجراء إعادة الكتابة للمتبنّي

1. انسخ الجدول إلى مستودعك.
2. أبقِ الأعمدة ١ و٢ و٣ كما هي (فهي نص الدستور).
3. استبدل العمود الرابع بمسارات اختبارك.
4. لكل صف لا يوجد له تطبيق عندك، اكتب الاختبار قبل ادعاء التبنّي.

### Why categories, not file paths, define the doctrine

A doctrine that hard-codes file paths is brittle and ties adoption to a single implementation. A doctrine that names test categories survives refactors, language changes, and platform changes. The categories below are stable; the file paths are illustrative.

The eight test categories named by the doctrine: **source-binding**, **channel-policy**, **claim-review**, **customer-safe-language**, **redaction-middleware**, **approval-gate**, **agent-identity**, **proof-pack**, **reusable-artifact-ledger**. Each row of the mapping above belongs to one or more of these categories.

### EN — Coverage rule

Every doctrine commitment must be covered by at least one test in at least one category. A commitment with zero passing tests is not adopted; it is documented.

### AR — قاعدة التغطية

كل التزام مغطّى باختبار واحد على الأقل في فئة واحدة على الأقل. الالتزام بلا اختبار ليس مُتبنّى، بل مُوثَّق فقط.

---

## Cross-link — روابط

- Canonical text → [`GOVERNED_AI_OPS_DOCTRINE.md`](./GOVERNED_AI_OPS_DOCTRINE.md)
- Condensed reference → [`11_NON_NEGOTIABLES.md`](./11_NON_NEGOTIABLES.md)
- Adoption checklist → [`IMPLEMENTATION_CHECKLIST.md`](./IMPLEMENTATION_CHECKLIST.md)
- Public surface → `/api/v1/doctrine/controls`

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
