# Enterprise Adoption Gates

لا تنتقل بين مراحل Rollout إلا بعد اجتياز البوابة.

| Gate | متطلبات (ملخص) |
|------|------------------|
| 1 Sponsor | sponsor · business owner · مشكلة واضحة |
| 2 Data | مصادر معروفة · Source Passport · PII · allowed use |
| 3 Workflow | workflow owner · approval owner · success metric |
| 4 Governance | external actions · draft-only · blocked actions |
| 5 Proof | Proof Pack كامل · score ≥ 70 · limitations · next action |
| 6 Adoption | مراجعة مخرجات · موافقات · استخدام مكرر للـworkflow |
| 7 Retainer | proof ≥ 80 · adoption ≥ 70 · قيمة شهرية · التزام المالك |

**الكود:** `ENTERPRISE_ADOPTION_GATES` · `enterprise_gate_passes` — `enterprise_rollout_os/adoption_gates.py`

**صعود:** [`ENTERPRISE_ROLLOUT_PLAYBOOK.md`](ENTERPRISE_ROLLOUT_PLAYBOOK.md)
