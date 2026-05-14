# Decision Types — أمثلة JSON

## Scale

متى: بيع متكرر، proof عالٍ، تسليم قابل للتكرار، مسار retainer، حوكمة مضبوطة، هامش صحي.

```json
{
  "decision": "SCALE",
  "target": "Revenue Intelligence Sprint",
  "evidence": [
    "sold 3+ times",
    "average proof score >85",
    "retainer path exists",
    "delivery checklist stable"
  ],
  "actions": [
    "raise price",
    "publish one-pager",
    "build account_scoring module",
    "create B2B services playbook"
  ]
}
```

## Build

متى: خطوة يدوية ≥3، ≥ساعتين/مشروع، مرتبط بعرض مدفوع، يقلل مخاطر أو يحسن هامش، سحب عميل.

```json
{
  "decision": "BUILD",
  "target": "Approval Center MVP",
  "evidence": [
    "approval friction repeated across 4 clients",
    "draft packs delayed",
    "retainer adoption affected"
  ],
  "actions": [
    "build approval matrix",
    "create approval status UI",
    "log approval events"
  ]
}
```

## Hold

متى: إشارة ضعيفة، طلب غير واضح، proof غير كافٍ، حوكمة غير جاهزة، صيانة عالية.

```json
{
  "decision": "HOLD",
  "target": "Academy Portal",
  "evidence": [
    "method not stable enough",
    "proof assets below threshold",
    "certification QA not defined"
  ],
  "next_condition": "10 projects + 3 strong proof-backed assets"
}
```

## Kill

متى: هامش منخفض، creep، proof ضعيف، لا retainer، مخاطر حوكمة، لا تكرار.

```json
{
  "decision": "KILL",
  "target": "Custom chatbot without source registry",
  "reason": "Weak proof, high hallucination risk, no governance boundary",
  "replacement": "Company Brain Sprint"
}
```

**الكود:** `offer_scorecard_strategic_decision` · `board_scorecards` · `BOARD_DECISION_INPUT_SIGNALS` — `board_decision_os/`

**صعود:** [`BOARD_SCORECARDS.md`](BOARD_SCORECARDS.md)
