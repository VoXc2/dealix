# Mini Diagnostic — Template

The Mini Diagnostic is the **free entry point** for every Phase E
warm intro. The customer trades 5 minutes of basic context for a
30-minute-of-Claude analysis output.

## Required sections

1. **Header** — bilingual, customer placeholder name, date
2. **Snapshot of inputs** — what the customer told you
3. **3 opportunities** — ranked by feasibility × revenue potential
4. **1 draft message (Arabic)** — for the highest-feasibility
   opportunity, written for warm contact (NOT cold)
5. **Recommended safe channel** — picked from the customer's
   `approved_channels` list (warm intro / referral / inbound DM /
   reply to existing thread)
6. **1 risk to avoid** — bilingual, specific
7. **Service recommendation** — pointer to the Dealix service tier
   that matches (Diagnostic / Growth Starter Pilot / Custom)
8. **No-guarantee clause** — bilingual

## Forbidden in this output

- ❌ "نضمن X%" / "guaranteed X%"
- ❌ "blast to all leads" / "scrape competitors"
- ❌ Any specific revenue claim ("you'll make Y SAR")
- ❌ Cold outreach plan
- ❌ Specific named competitor's data without source

## Required closing

Every Mini Diagnostic ends with:

```
action_mode: approval_required
no_live_send: true
no_live_charge: true
audience: internal_only
```

## How to generate

```
python scripts/dealix_diagnostic.py \
  --company "[Customer-Slot-A]" \
  --sector "b2b_services" \
  --region "riyadh" \
  --pipeline-state "has leads but inconsistent follow-up"
```

Output: bilingual Markdown ≤ 2 pages. NO LLM call required (the
script composes from local YAML + heuristics).

## Manual override if script doesn't fit

If the customer's situation is too unique for the script, draft the
Diagnostic by hand following the 8 sections above. Keep it ≤ 2
pages. NEVER ship a Diagnostic that:
- exceeds 2 pages
- contains a guaranteed claim
- mentions a specific named competitor without a public source
- contains the customer's PII in clear (use placeholders)

## Bilingual

**Arabic**: التشخيص المصغّر هو نقطة الدخول المجانية لكل عميل.
**English**: The Mini Diagnostic is the free entry point for every customer.
