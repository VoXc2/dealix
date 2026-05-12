# Architecture Decision Records — Index

This directory holds the canonical record of every architectural decision
that shapes Dealix. Each ADR is a self-contained markdown file; the goal
is that a new engineer can read the index and understand *why* the system
looks the way it does in under an hour.

## Conventions

- Filename: `NNNN-kebab-title.md` where `NNNN` is the next zero-padded
  number. Numbers never reuse, even if an ADR is rejected or superseded.
- Use `template.md` as the starting point.
- Reviewers: at minimum one engineering + one founder approval.
- An ADR is **Accepted** only when merged on `main`.

## Decisions

| # | Status | Title | Owner |
| --- | --- | --- | --- |
| [0001](0001-plain-vs-intercom.md) | Accepted | Customer support — Plain over Intercom / Crisp | Founder |
| [0002](0002-inngest-vs-temporal.md) | Accepted | Durable workflows — Inngest over Temporal | Platform |

## Pending / proposed

(none today; new proposals open as `XXXX-draft-<title>.md` files in
this directory until accepted)
