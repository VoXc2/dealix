# CEO Command Center

## المبدأ

الواجهة لا تقول «هذه الأرقام» فقط — تقول:

```text
هذه القرارات الخمسة التي يجب اتخاذها هذا الأسبوع.
```

## سطح العرض (taxonomy)

Top 5 decisions، جودة الإيراد، قوة Proof، فرص retainer، مخاطر عملاء، طابور productization، مخاطر حوكمة، إيراد سيء للرفض، نضج وحدات أعمال، إشارات venture.

**الكود:** `CEO_COMMAND_CENTER_SURFACES` · `ceo_command_center_coverage_score` — `board_decision_os/ceo_command_center.py`

## مثال Top Decisions (JSON — خمس أولويات)

```json
[
  {
    "priority": 1,
    "decision": "OFFER_RETAINER",
    "target": "Client A",
    "reason": "Proof Score 87, Adoption Score 78, monthly workflow exists"
  },
  {
    "priority": 2,
    "decision": "BUILD_MVP",
    "target": "Approval Center",
    "reason": "Approval friction repeated across 4 clients"
  },
  {
    "priority": 3,
    "decision": "RAISE_PRICE",
    "target": "Revenue Intelligence Sprint",
    "reason": "High proof score and repeatable delivery"
  },
  {
    "priority": 4,
    "decision": "REJECT_BAD_REVENUE",
    "target": "Cold WhatsApp automation request",
    "reason": "Unsafe channel risk and prohibited automation"
  },
  {
    "priority": 5,
    "decision": "CREATE_PLAYBOOK",
    "target": "B2B Services Revenue Readiness",
    "reason": "Repeated sector pattern"
  }
]
```

**صعود:** [`BOARD_MEMO_AUTOMATION.md`](BOARD_MEMO_AUTOMATION.md)
