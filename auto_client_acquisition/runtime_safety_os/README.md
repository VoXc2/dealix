# runtime_safety_os — System 31: Enterprise Safety Engine

## English

Runtime operational safety: circuit breakers, kill switches, execution limits
and policy boundaries. Any agent or workflow can be halted instantly.

Every transition asserts its preconditions and raises `SafetyError` loudly on
an invalid operation — a kill switch never silently fails to engage
(`no_silent_failures`). Engaging a kill switch propagates: it isolates the
target agent in the mesh (System 27) and pauses the target run in the control
plane (System 26).

## العربية

أمان تشغيلي وقت التشغيل: قواطع الدوائر ومفاتيح الإيقاف وحدود التنفيذ وحدود
السياسات. يمكن إيقاف أي وكيل أو سير عمل فورًا. كل انتقال يتحقق من شروطه ويرفع
خطأً صريحًا عند أي عملية غير صالحة — مفتاح الإيقاف لا يفشل بصمت. تفعيل المفتاح
يعزل الوكيل في الشبكة ويوقف التشغيل في طبقة التحكم.

## API

`/api/v1/runtime-safety` — `POST /check`, `POST /kill-switch`,
`DELETE /kill-switch/{id}`, `GET /circuit-breakers`, `PUT /execution-limits`,
`GET /status/{target}`.
