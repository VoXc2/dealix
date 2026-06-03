# AI Agent Control Standard

كل agent له **Agent Card**: هوية، غرض، مدخلات، أدوات، ممنوعات، مستوى استقلال، موافقات، audit.

## مستويات الاستقلال (0–6)

0 Read · 1 Analyze · 2 Draft/Recommend · 3 Queue for approval · 4 Execute internal after approval · 5 External restricted · 6 Autonomous external forbidden.

## MVP Rule

```text
Dealix MVP allows only autonomy levels 0–3.
```

**تهديدات agentic AI:** أدوات، ذاكرة، تنفيذ، operational execution vulnerabilities — [arXiv:2504.19956](https://arxiv.org/abs/2504.19956).

**الكود:** `MVP_AUTONOMY_LEVEL_MAX` · `agent_autonomy_allowed_in_mvp` — `standards_os/agent_control_standard.py`

**صعود:** [`../institutional_control/AGENT_CONTROL_PLANE.md`](../institutional_control/AGENT_CONTROL_PLANE.md)
