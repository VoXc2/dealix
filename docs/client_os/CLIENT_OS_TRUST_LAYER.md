# Client OS — طبقة الثقة

لكل مخرج عرض: source status · governance · PII · approval · QA · ربط proof.

## مثال

```text
Output: Draft email pack
Status: Draft-only
PII: Contains contact names
External sending: Not approved
Approval required: Yes
Audit event: AUD-002
```

**وكلاء وصلاحيات:** **68%** من المؤسسات لا تستطيع التمييز بثقة بين نشاط AI ونشاط البشر، و**74%** تقول إن الوكلاء غالبًا يحصلون على صلاحيات أكثر من اللازم — [IT Pro — CSA / Aembit](https://www.itpro.com/technology/artificial-intelligence/workers-cant-identify-work-produced-by-ai-agents-business-risks).

**الكود:** `TRUST_OUTPUT_STRIP_SIGNALS` · `trust_output_strip_coverage_score` — `client_os/governance_panel.py`

**صعود:** [`AGENT_TRANSPARENCY_CARD.md`](AGENT_TRANSPARENCY_CARD.md)
