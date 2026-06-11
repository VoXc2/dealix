# AI Task Routing (Dealix)

## نموذج التوجيه
| Task | Route | Reason |
|------|-------|--------|
| Lead scoring | Deterministic script | Audit + reproducibility |
| Outreach draft | LLM (draft only) | Tone + language |
| Proposal generation | LLM + template | Quality + speed |
| Proof report | LLM + template | Quality + speed |
| Pricing quote | Deterministic script | Audit + math |
| Risk flag | Deterministic script | Logic + audit |
| Final send | Human only | Safety |

## قواعد التوجيه
- لا route لمهمة فيها قرار مالي/قانوني
- لا route لمهمة تحتاج بيانات خاصة
- كل route له `route_id` + `safety_flags`
- أي فشل route → fallback manual
