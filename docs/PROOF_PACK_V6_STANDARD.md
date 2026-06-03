# Proof Pack v6 Standard / معيار حزمة الأدلة v6

> Bilingual standard for assembling and sharing Proof Packs at Dealix.
> Defines the difference between an internal pack and a customer-shareable
> pack, the consent + approval gate, the ``~``-prefix convention for
> estimates, and the HMAC-SHA256 metadata signing interface.

**Date opened:** 2026-05-04
**Owner:** Founder
**Hard rule (re-asserted):** No customer name, logo, screenshot, or
metric leaves the platform without (1) ``consent_for_publication=True``
on every included event AND (2) explicit founder approval recorded in
the Approval Center.

---

## 1. Two pack flavors / النسختان من الحزمة

### 1.1 Internal Proof Pack — حزمة داخلية فقط

**Audience:** founder + delivery team only.
**Trigger:** ANY included event has ``consent_for_publication=False``
or no consent record exists for it.
**Field that carries this:** ``audience = "internal_only"``.
**Allowed uses:**
- Founder weekly review
- Internal forecasting and pipeline learnings
- Investor/partner conversations under NDA — only at founder discretion

**Forbidden uses:**
- Public website / landing pages
- Social posts / press releases
- Outbound sales decks shared without NDA

### 1.2 Customer-Shareable Proof Pack — حزمة قابلة للنشر

**Audience:** customer + (with founder approval) prospects.
**Trigger:** EVERY included event has ``consent_for_publication=True``
AND the assembled pack passes the safe-publishing gate.
**Field that carries this:** ``audience = "public_with_consent"``.
**Still required even when public-eligible:**
- ``approval_status = "approval_required"`` until the founder approves
  via the Approval Center.

```text
┌──────────────────────────────────────────────────────────────┐
│  consent_for_publication = True for every event              │
│            AND                                                │
│  founder approval recorded in approval_center                │
│            ⇩                                                  │
│  ONLY THEN may a Proof Pack appear on a public surface       │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. Estimates vs measurements / التقديرات مقابل القياسات

Numbers in any Proof Pack fall into one of two classes:

| Class | Prefix | Example | Source |
|---|---|---|---|
| Measured | (none) | ``14 qualified opportunities`` | Customer Data Plane / signed event |
| Estimate | ``~`` | ``~30% pipeline lift`` | Forecast / extrapolation |

**Rule:** any number that did NOT come from a recorded ProofEvent
MUST carry the ``~`` prefix in both Arabic and English snippets.
Authors of new snippet templates must run the safe-publishing gate
AND verify visually that estimates are clearly labeled.

The ``proof_snippet_engine.render`` function already refuses to
invent numbers — every metric must come from the input event.

---

## 3. HMAC interface / واجهة HMAC

To detect tampering after a pack leaves the platform, callers may
sign the pack metadata with an HMAC-SHA256 keyed off a deployment
secret.

**Module:** ``auto_client_acquisition.proof_ledger.hmac_signing``

```python
from auto_client_acquisition.proof_ledger.hmac_signing import sign_pack_metadata

signature = sign_pack_metadata(
    payload={"customer_handle": "Slot-A", "events_count": 3},
    secret=deployment_secret,  # or None for UNSIGNED
)
```

**Contract:**
- ``sign_pack_metadata(payload: dict, secret: str | None = None) -> str``
- When ``secret`` is ``None`` (or empty), returns the literal string
  ``"UNSIGNED"`` — never a digest of an empty key.
- When ``secret`` is provided, returns a 64-character lowercase hex
  digest derived from HMAC-SHA256 over the canonical JSON of
  ``payload`` (sorted keys, no whitespace, UTF-8).
- Same ``(payload, secret)`` pair yields the same digest across
  processes — useful for receiver-side verification.
- Pure stdlib: ``hashlib`` + ``hmac`` + ``json``. No new dependency.

**Out of scope (explicitly):** key rotation, KMS integration,
multi-tenant key segregation. The signer accepts the secret as
input; storage and rotation live outside this module.

---

## 4. PDF rendering — deferred / تصدير PDF — مؤجَّل

PDF export is deliberately deferred until the first paying customer
explicitly requests a PDF. Reasons:

1. The bilingual markdown rendering already handles every current need.
2. Adding ``weasyprint`` introduces a heavyweight C-library dependency
   (cairo, pango) that we do not want to carry without a paying user.
3. The default share format is the Customer Data Plane URL +
   bilingual markdown — both are searchable, signable, and tamper-evident.

**When the trigger fires:** add ``weasyprint`` to ``requirements.txt``
and call ``HTML(string=markdown_to_html(pack["markdown_en"])).write_pdf(...)``.
Until then this section is documentation only — no implementation,
no tests for PDF rendering exist on this branch.

---

## 5. Mapping to existing modules / ربط بالوحدات الحالية

| Concern | Module | Function |
|---|---|---|
| Render single event | ``self_growth_os.proof_snippet_engine`` | ``render(event)`` |
| Assemble pack | ``self_growth_os.proof_snippet_engine`` | ``render_pack(events)`` |
| Forbidden vocabulary gate | ``self_growth_os.safe_publishing_gate`` | ``check_text(text)`` |
| Approval queue | ``approval_center`` | ``create_approval`` / ``list_pending`` |
| HMAC metadata signing | ``proof_ledger.hmac_signing`` | ``sign_pack_metadata`` |
| Audit-trail storage | ``proof_ledger.file_backend`` / ``postgres_backend`` | (existing) |

---

## 6. Hard guarantees / ضمانات صارمة

- A Proof Pack with ``audience = "internal_only"`` MUST NOT be sent
  to a public surface. The router refuses; the founder console hides
  the "Publish" button; the safe-publishing gate is run again at
  publish time.
- A Proof Pack with even one forbidden token (``نضمن`` / ``guaranteed``
  / ``blast`` / ``scrape`` / ``cold whatsapp``) is BLOCKED at pack
  level — not just at event level.
- A Proof Pack always carries ``approval_status = "approval_required"``
  on first render. Approval is a separate, recorded, founder-initiated
  event — never an automatic side effect.
- All numbers without a measurement source carry the ``~`` prefix.

— Proof Pack v6 Standard v1.0 · 2026-05-04 · Dealix
