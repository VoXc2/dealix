# Business Unit Maturity Score — نضج وحدة الأعمال

## الأبعاد

| البعد | الوزن |
|-------|------|
| Revenue | 20% |
| Repeatability | 20% |
| Retainers | 15% |
| Product module | 15% |
| Playbook | 10% |
| Proof library | 10% |
| Owner readiness | 10% |

## النطاقات

| النتيجة | التصنيف |
|---------|---------|
| 85+ | venture candidate |
| 70–84 | business unit |
| 55–69 | service line |
| &lt; 55 | experiment |

## الكود

`auto_client_acquisition/command_os/unit_maturity_score.py`

**ملاحظة:** أوزان ومخرجات **Sovereign Command**؛ مساعد منفصل في `intelligence_os/venture_signal.py` قد يُستخدم للمسارات الأخرى — وازن عند الدمج في الـaggregator.

**صعود:** [`SOVEREIGN_COMMAND_SYSTEM.md`](SOVEREIGN_COMMAND_SYSTEM.md) · [`../control_tower/UNIT_MATURITY_SCORE.md`](../control_tower/UNIT_MATURITY_SCORE.md)
