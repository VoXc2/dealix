# Capital Allocation Score (World-Class)

**استثمار الوقت/المال** يجب أن يحقق على الأقل أحد: إيراد · هامش · مخاطر أقل · تسليم أسرع · proof · capital · distribution · market authority. إن تحقق **3+** فغالبًا **أولوية**.

## الصيغة (0–100 لكل مدخل قبل الدمج)

`Score =`  
`Revenue impact × 0.20`  
`+ Margin impact × 0.15`  
`+ Risk reduction × 0.15`  
`+ Proof creation × 0.15`  
`+ Productization potential × 0.15`  
`+ Market authority × 0.10`  
`+ Strategic fit × 0.10`

## النطاقات

| النتيجة | قرار |
|---------|------|
| 85+ | invest hard |
| 70–84 | build |
| 55–69 | pilot |
| 40–54 | hold |
| &lt; 40 | kill |

**الاستخدام:** feature · service · vertical · partner · content · academy track · venture idea.

**الكود:** `command_os/capital_allocation.py` — `WorldClassAllocationInputs`، `compute_world_class_allocation_score`، `world_class_allocation_band`.

**مرجع قديم مختلف الأوزان:** [`../intelligence/CAPITAL_ALLOCATION_SCORE.md`](../intelligence/CAPITAL_ALLOCATION_SCORE.md) و`intelligence_os/capital_allocator.py` (أولوية رأس مال داخلية أخرى).

**صعود:** [`COMMAND_SYSTEM.md`](COMMAND_SYSTEM.md)
