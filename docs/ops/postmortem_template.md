# Postmortem — YYYY-MM-DD — <short title>

> Blameless. The goal is to make the system safer; nobody's career
> depends on this document. Use precise language; avoid "should have".

## Summary

One paragraph for an executive reader. What happened, who was impacted,
how long, what we did to fix it, what we're changing.

## Impact

- **Severity**: SEV-1 / 2 / 3
- **Duration**: HH:MM — HH:MM Asia/Riyadh (UTC offset +03)
- **Customers affected**: count + tier breakdown
- **Revenue impact**: SAR (best estimate)
- **Data integrity impact**: rows lost / exposed / corrupted (always be specific)

## Timeline (UTC)

| Time | Event |
| --- | --- |
| HH:MM | Alert fired (BetterStack / Sentry / customer) |
| HH:MM | IC declared, comms channel opened |
| HH:MM | First mitigation attempted: ... |
| HH:MM | Root cause confirmed: ... |
| HH:MM | Fix deployed via ... |
| HH:MM | Healthy — confirmed via /healthz + customer follow-up |
| HH:MM | Comms closed; customer summary sent |

## Root cause

The actual root cause, *not* a list of contributing factors. Cite code
paths (`api/foo.py:123`), config diffs, vendor outage URLs.

## Contributing factors

Things that made the incident worse or harder to detect. Use a
bulleted list, one per factor.

## What went well

Recovery actions, automation that worked as intended, communication
that landed cleanly. Capture these — they're as important as the
gaps.

## What went poorly

Where we lost time. Where signals were missed. Where customers had to
remind us of something we should have caught.

## Lessons learned

Not "we should be more careful" — concrete, testable claims about the
system or the process.

## Action items

| # | Description | Owner | Severity | Due |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |
| 2 |  |  |  |  |

File each action item as a GitHub issue with the `postmortem` label.

## Customer communications

- Initial: link to status page entry / email.
- Resolution: link to summary email.
- Affected tenants list (private; do not commit names).

---

*Reviewed by:* IC + one other engineer. *Closed:* date.
