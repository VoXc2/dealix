# Dealix Design Language — لغة التصميم

> Plain-English (and Arabic) narrative. Why Dealix looks and feels
> the way it does. Not a token reference — that lives in
> `design-systems/dealix/DESIGN.md`. This document is the *why*.

---

## 1. Audience and stance

Dealix is built for Saudi executives who buy outcomes, not features.
Every screen, document, and email is written for a CEO, a COO, or a
GM who has six minutes to decide whether to pay an invoice or
forward an introduction. The design language exists to make that
six-minute decision easy and safe.

دِيليكس مصمم لقادة الأعمال في السوق السعودي. كل شاشة وكل تقرير وكل
رسالة موجَّهة لمسؤول تنفيذي يقرأ بسرعة، يطلب الدليل، ويحتاج إلى
وضوح وأمان قبل التوقيع. لغة التصميم هذه موجودة لتجعل القرار سهلاً
وآمناً.

## 2. Saudi-first UX

The default direction is right-to-left. The default language is
Arabic. English exists as a parallel sub-block, never as the
primary surface. This is not a localisation toggle — it is the
default rendering pathway. We invert it only for *internal-only*
operator tooling, where English-first is acceptable because no
customer ever sees the screen.

Practical consequences:

- All container layouts use logical CSS properties
  (`margin-inline-start`, `padding-inline-end`) so RTL/LTR
  mirroring is automatic.
- All status chips, evidence badges, and approval pills have
  Arabic and English label pairs in the design system; the renderer
  picks based on the active locale, never hard-codes English.
- Numerals in prose use Arabic-Indic in Arabic blocks; ASCII in
  tables and KPIs to keep machine-readability.

## 3. Enterprise trust

Saudi enterprise buyers are sceptical of fast-talking martech. They
have seen too many guaranteed-ROI decks. Dealix earns trust by
*subtraction*: we remove the words and patterns that cheap
competitors use, and leave only the ones we can defend.

What we never show:

- Hero numbers without an evidence link.
- Trend arrows without a proof ledger reference.
- "Trusted by" logos without a written, signed permission record.
- Money-back-guarantee wording outside an explicit, founder-approved
  refund clause.

What we always show:

- The outcome on top.
- The evidence badge directly under it.
- The status chip that names the *current* state — `Live`, `Pilot`,
  `Partial`, `Target`, `Blocked`, `Approval Required`, `Draft Only`,
  `Internal Only`.
- The next step, with the approval state attached.

## 4. AI-workforce clarity

Dealix is an AI-augmented service company, not a SaaS. A real human
approves every external send, every invoice, every customer
artefact. The interface must make that fact obvious — not hidden in
a footer, not buried in a settings panel, but on the same row as
the action.

Rendering rules:

- Every send/publish/external-action button starts in the
  `Approval Required` state.
- The approval pill is the same visual weight as the action button.
  A user cannot accidentally bypass it.
- Internal AI-generated drafts carry the `Draft Only` chip until a
  named human approves.
- Logs of approvals are first-class artefacts: they have evidence
  badges, they are linkable, they are auditable.

In other words: the AI is a co-worker, not an autonomous agent.
The design language makes that distinction visible at every
interaction point.

## 5. Safety-first design

Saudi Arabia has PDPL. Saudi enterprises have internal compliance
teams. Dealix's design language treats safety as a first-class
visual element, not a footnote.

Patterns:

- The `Approval Required` chip uses the `block` colour token. It
  reads as "stop and check", not as "warning, maybe later".
- PII is never on-screen by default. Customer names appear only when
  `consent_for_publication=True` is recorded in the proof ledger.
- Forbidden copy (see DESIGN.md §7) is enforced by a perimeter test
  that fails the build. The visual language and the test suite
  agree, so nobody can ship a phrase that the system cannot back.
- Negation copy ("Dealix never initiates cold outreach") is allowed
  and even encouraged — it tells the buyer what we *don't* do, which
  is often more reassuring than what we do.

## 6. Evidence-first rule

Every customer-facing claim must link to a proof ledger record.
This is the single rule that subordinates the rest of the design
language.

Concretely:

- A KPI tile without an evidence badge is a *bug*, not a stylistic
  choice. The renderer should refuse to emit it.
- A proposal page without a proof pack reference is *Draft Only*
  by default, regardless of how polished it looks.
- A status chip of `Live` requires at least one
  `proof_pack_assembled` event in the ledger; otherwise the chip
  defaults to `Pilot` or `Target`.
- The evidence badge format is fixed (`EVT-…`, `INV-…`, `PROOF-…`)
  so customers learn to read it as a verifiable handle, not a
  decorative element.

## 7. Bilingual without compromise

Arabic and English carry equal weight in customer-facing artefacts.
We do not translate one into the other after the fact; we draft
both, side by side, and treat them as a single source.

Operational rules:

- The Arabic block is always first in source order and on screen.
- The English block is a sub-section under it, marked `lang="en"
  dir="ltr"`.
- Headings carry both languages where space allows. KPI labels
  carry both. Status chips have both label strings in the registry,
  and the renderer picks one — never machine-translates.
- Internal-only operator screens may be English-only; they wear the
  `Internal Only` chip so we never confuse them with a customer
  surface.

## 8. Why mobile-first

Saudi executives read on phones. Board members forward decks via
WhatsApp. Procurement staff open proposals between meetings. If
the artefact is unreadable on a 360-px screen, it is unreadable
to the buyer.

The design system therefore caps the comfortable reading width at
720 px and collapses to a single column under 560 px. Tables become
key/value lists. KPI tiles stack. Evidence badges and status chips
never disappear at small breakpoints — they are the load-bearing
elements.

## 9. Tone summary

Calm. Specific. Bilingual. Evidence-linked. Approval-gated.
Never hyped. Never guaranteed. Never automated past the point a
human signed off.

That is the Dealix design language.
