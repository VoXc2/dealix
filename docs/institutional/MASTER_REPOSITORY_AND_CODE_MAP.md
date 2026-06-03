# Master Repository Map + Code Map (فعلي في الريبو)

خريطة المستخدم §19–20 مُطابَقة **للهيكل الحالي** — لا تغيّر أسماء الملفات هنا دون تحديث السكربتات.

## `docs/` — مجالي المؤسسة

| المسار المقصود في التصميم | الموقع الفعلي |
|---------------------------|----------------|
| `institutional/*` | **`docs/institutional/`** (هذا المجلد) |
| `group/HOLDING…` | `docs/group/` — [`DEALIX_COMPOUND_HOLDING_DOCTRINE.md`](../group/DEALIX_COMPOUND_HOLDING_DOCTRINE.md) إلخ |
| `standards/` | `docs/standards/` — [`DEALIX_AI_OPERATIONS_STANDARD.md`](../standards/DEALIX_AI_OPERATIONS_STANDARD.md) |
| `architecture/` | `docs/architecture/` — [`CORE_OS.md`](../architecture/CORE_OS.md) إلخ |
| `governance/` | `docs/governance/` |
| `ledgers/` | `docs/ledgers/` |
| `growth/` | `docs/growth/` — ACADEMY · PARTNER_NETWORK |
| `units/revenue/` | **`docs/institutional/units/revenue/`** |
| playbook قطاعات | `docs/playbooks/` |
| `intelligence/*` | **`docs/intelligence/`** — طبقة العقل التشغيلي |
| `memory/*` | **`docs/memory/`** — الدروس الاستراتيجية |

## كود — `auto_client_acquisition/` (واقعي)

| المقصود في التصميم | الواقع اليوم |
|---------------------|-------------|
| `llm_gateway/*` | **`llm_gateway_v10/`** |
| `core_os/` | *مستهدف* — لم يُنشأ بعد |
| `capital_os/` · `command_center/` | *مستهدف* + وثائق ledgers/product |
| `data_os/` · `governance_os/` · `revenue_os/` · `reporting_os/` | **موجود** |
| `brain_os/` · `operations_os/` · `support_os/` | أجزاء مبعثرة في الريبو — **راجع** [`../product/MASTER_CODE_MAP.md`](../product/MASTER_CODE_MAP.md) |
| `intelligence_os/` | **`intelligence_os/`** — نماذج scoring محضة (`capital_allocator`، `venture_signal`، …) |

**خريطة كود موسعة:** [`../product/MASTER_CODE_MAP.md`](../product/MASTER_CODE_MAP.md) · واجهات: [`../architecture/API_MAP.md`](../architecture/API_MAP.md) · [`../architecture/API_SPEC.md`](../architecture/API_SPEC.md) · ذكاء تنفيذي: [`../intelligence/README.md`](../intelligence/README.md)
