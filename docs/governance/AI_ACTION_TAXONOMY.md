# AI Action Taxonomy

Classify every AI behavior by **risk** and **blast radius**. Default Dealix posture is conservative on **external** effects.

## Levels

| Level | Name | Description |
|------:|------|-------------|
| **0** | Read | Read allowed data only |
| **1** | Draft | Create draft output (no external effect) |
| **2** | Recommend | Recommend next action (human executes) |
| **3** | Queue | Prepare action for **approval** queue |
| **4** | Execute internal | Update **internal** state **after** approval |
| **5** | Execute external | Send/publish/contact externally — **heavily restricted** |
| **6** | Autonomous external | **Not allowed** in Dealix MVP / default product posture |

## MVP policy

```text
Levels 0–3: allowed by default with governance + QA
Level 4: requires approval + audit
Level 5: enterprise-only, explicit contracts + controls
Level 6: forbidden
```

Pair with [`RUNTIME_GOVERNANCE.md`](RUNTIME_GOVERNANCE.md) and [`FORBIDDEN_ACTIONS.md`](FORBIDDEN_ACTIONS.md).
