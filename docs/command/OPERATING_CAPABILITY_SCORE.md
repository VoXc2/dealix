# Operating Capability Score — درجة القدرة التشغيلية

**السؤال:** هل هذا المشروع **خلق قدرة تشغيلية فعلية**، أم مخرجات «جميلة» بلا صلابة؟

## المكوّنات (0–100 لكل بند قبل الدمج)

| المكوّن | الوزن |
|---------|------|
| Workflow clarity | 15% |
| Data readiness | 15% |
| AI usefulness | 15% |
| Governance coverage | 20% |
| QA score | 10% |
| Proof strength | 15% |
| Repeatability | 10% |

## النطاقات

| النتيجة | التفسير |
|---------|---------|
| 85–100 | strong capability |
| 70–84 | usable capability |
| 50–69 | partial capability |
| &lt; 50 | not a capability yet |

## الكود

`auto_client_acquisition/command_os/capability_score.py` — `OperatingCapabilityInputs`، `compute_operating_capability_score`، `operating_capability_band`.

**صعود:** [`SOVEREIGN_COMMAND_SYSTEM.md`](SOVEREIGN_COMMAND_SYSTEM.md)
