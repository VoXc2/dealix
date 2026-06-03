# Dealix Founder Daily Operating Rhythm

This is the daily operating rhythm for running Dealix after the live domain is connected.

## Morning check — 10 minutes

1. Check production smoke status.
2. Check API health and public website availability.
3. Review new demo requests, checkout events, and inbound messages.
4. Review overnight errors and failed webhooks.
5. Review AI/provider cost or failure spikes.
6. Confirm no P0 issues are open without owner/action.

## Midday commercial review — 15 minutes

1. Review pipeline movement and lead quality.
2. Review customer replies and demo booking friction.
3. Check whether public copy matches current offer.
4. Record any objection pattern in the backlog.
5. Prioritize fixes that improve demo conversion or trust.

## Evening trust review — 10 minutes

1. Check no-overclaim register if any public copy changed.
2. Confirm no high-stakes action bypassed approval.
3. Review suppression/opt-out handling for outreach.
4. Confirm incident notes or failed checks are tracked.
5. Decide whether tomorrow is safe for more outreach or paid traffic.

## Stop rules

Pause outbound, paid traffic, or public demos when any of these happen:

- API health fails.
- Public website is unavailable.
- Checkout flow fails.
- Demo request routing fails.
- Webhook verification fails.
- Admin/auth boundary is unclear.
- A public claim lacks evidence.
- Opt-out/suppression behavior is uncertain.
- AI sends or prepares a high-stakes commitment without required approval.

## Weekly review

- Review Issues #467–#471 until closed.
- Review cost, conversion, and provider reliability.
- Review `docs/ops/EXECUTION_BACKLOG.md`.
- Promote recurring fixes into CI, scripts, or runbooks.
- Archive stale docs or update them to match reality.

## Arabic summary

كل يوم افحص الصحة، الطلبات، الدفع، الأخطاء، التكلفة، والثقة. أوقف الإرسال أو الحملات فورًا إذا الصحة، الدفع، الديمو، الموافقات، أو الادعاءات غير مؤكدة.
