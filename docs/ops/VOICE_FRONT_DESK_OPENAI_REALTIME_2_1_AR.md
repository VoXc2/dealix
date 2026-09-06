# Dealix Voice Front Desk — OpenAI GPT-Realtime-2.1

## القرار الكنسي

طبقة الصوت في Dealix هي **قناة داخل Company Machine الحالية** وليست CRM أو Agent Fleet أو Proof Ledger جديدًا.

المسار المستهدف:

`Virgin/Business number -> verified forwarding/SIP provider -> OpenAI Realtime SIP -> Dealix verified webhook -> GPT-Realtime-2.1 -> server-side sideband tools -> Communication Hub -> qualification/booking/handoff`

لا نفترض أن Virgin Mobile Saudi توفر SIP أو programmable voice مباشرة. يجب إثبات مسار forwarding/porting/SIP الحي قبل تفعيل الرقم.

## نموذج التشغيل

- **Live model:** `gpt-realtime-2.1` فقط.
- **Default mode:** inbound-first.
- **Outbound voice:** مقفل افتراضيًا.
- **Recording/raw transcript retention:** غير منفذ في هذا adapter ومقفل افتراضيًا.
- **Disclosure:** الوكيل يعرّف نفسه كمساعد Dealix الذكي، ولا ينتحل شخصية المؤسس أو موظف بشري.
- **Language:** عربي سعودي/عربي واضح افتراضيًا، مع التحويل الطبيعي للإنجليزية.
- **Commercial authority:** لا أسعار أو خصومات أو SLA أو عقد أو التزام قانوني غير معتمد.

## ما يستطيع الوكيل فعله

1. فهم سياق الشركة والمشكلة قبل العرض.
2. تشخيص workflow الحالي، الأدوات، التسرب/التأخير/التكلفة/المخاطر، الاستعجال وصاحب القرار.
3. شرح Dealix حسب المشكلة بدل قراءة brochure.
4. شرح أن Dealix هو Governed AI Execution / Business OS وليس chatbot أو CRM بديلًا.
5. التعامل مع الاعتراضات العادية بشكل استشاري ومقنع قائم على الأدلة.
6. إرجاع شرح capabilities من مصدر grounded داخل الكود.
7. إرجاع رابط الحجز الكنسي عند توفره.
8. حفظ **structured qualification note** فقط داخل Communication Hub؛ لا يحفظ raw transcript.
9. نقل المكالمة عبر SIP REFER عندما يكون `VOICE_AI_HANDOFF_TARGET_URI` مهيأ.
10. التصعيد للإنسان عند القانون/العقد/الأمن الحساس/الشك/الصفقات الكبيرة أو طلب المتصل.

## الأدوات الجانبية Sideband

- `lookup_dealix_capabilities`
- `get_booking_link`
- `save_qualification`
- `request_human_handoff`

الـsideband يتصل بالمكالمة المقبولة باستخدام `call_id`. وهو المسؤول عن تنفيذ الأدوات server-side، ثم إعادة `function_call_output` إلى نفس جلسة Realtime.

## Endpoint

Webhook عام لكنه **متحقق بتوقيع OpenAI**:

`POST https://api.dealix.me/api/v1/webhooks/openai/realtime`

Readiness بدون كشف قيم أسرار:

`GET https://api.dealix.me/api/v1/webhooks/openai/voice-readiness`

`/api/v1/webhooks/*` معفى من API-key middleware لأن provider webhooks يجب أن تتحقق بتوقيع مزودها بدل Dealix API key.

## متغيرات البيئة

### أسرار — لا تكتب في Git أو chat

- `OPENAI_API_KEY`
- `OPENAI_WEBHOOK_SECRET`

### إعدادات غير سرية

- `VOICE_AI_ENABLED=false` — يبقى false حتى نجاح acceptance ومسار SIP.
- `VOICE_AI_MAX_OUTPUT_TOKENS=900`
- `VOICE_AI_REASONING_EFFORT=medium`
- `VOICE_AI_TRACING_ENABLED=true`
- `VOICE_RECORDING_ENABLED=false`
- `VOICE_OUTBOUND_ENABLED=false`
- `VOICE_AI_HANDOFF_TARGET_URI=` — مثال لاحقًا `tel:+966...` أو SIP URI بعد اعتماده.
- `CALENDLY_URL=` — يستخدم رابط Dealix الكنسي الموجود.

الموديل **مقفل في الكود على `gpt-realtime-2.1`** حتى لا يتحول إلى mini أو model آخر بسبب env drift.

## ترتيب التفعيل

1. نشر الكود مع `VOICE_AI_ENABLED=false`.
2. إضافة `OPENAI_API_KEY` إلى Railway secrets دون إظهاره في المحادثة أو logs.
3. إنشاء OpenAI webhook على endpoint أعلاه واختيار حدث `realtime.call.incoming`، ثم إضافة `OPENAI_WEBHOOK_SECRET` إلى Railway secrets.
4. تثبيت non-secret flags أعلاه.
5. تنفيذ readiness probe والتأكد من أن القيم السرية تظهر كـconfigured فقط، لا قيمها.
6. تنفيذ unit/source acceptance على exact release.
7. إثبات مسار telephony/SIP الحقيقي من الرقم السعودي إلى OpenAI.
8. Canary inbound محدود.
9. بعد PASS فقط: `VOICE_AI_ENABLED=true`.
10. مراقبة latency/interruption/tool errors/cost/qualified-call ratio/handoff success.

## Fail-closed

إذا وصل provider traffic قبل التفعيل، المكالمة verified تُرفض بـSIP 603 بدل قبولها بنصف runtime.

إذا webhook signature غير صحيحة، الطلب يرفض بدون طباعة body أو headers.

إذا handoff غير مهيأ، الوكيل لا يدّعي أن التحويل حدث؛ يعرض human follow-up.

إذا qualification persistence فشلت، لا يكشف storage details للمتصل أو للموديل.

## Commercial truth

الوكيل لا يجوز أن يختلق:

- عميلًا أو case study أو testimonial.
- ROI أو توفير أو revenue result.
- integration أو certification أو Production state غير مثبت.
- سعرًا أو خصمًا أو عقدًا أو SLA.
- Payment/Invoice/Proof غير موثق.

المسار التجاري المرجعي:

`Execution Diagnostic -> Discovery -> Customer-Specific Quote -> Verified Payment -> Governed Delivery -> Customer-Validated Proof -> Expansion`

## Telephony truth

حالة الرقم السعودي وشبكة Virgin لا تكفي وحدها لإثبات SIP. خيارات الربط المقبولة بعد التحقق:

- call forwarding من MSISDN إلى DID/SIP provider يدعم الربط مع OpenAI؛ أو
- DID/SIP سعودي/محلي منفصل للصوت مع بقاء الرقم الحالي لـWhatsApp/SMS؛ أو
- port/enterprise SIP عندما يثبت provider أنه يدعم المسار المطلوب.

لا يتم إلغاء الشريحة أو نقل الرقم قبل canary ناجح وخطة rollback.

## مؤشرات الأداء

- answer latency / interruption recovery
- call completion rate
- tool-call success rate
- human-handoff success rate
- qualified-problem rate
- booked-discovery rate
- cost per call / qualified call / booked diagnostic
- opt-out / complaint rate
- verified cash attributed to eligible calls
- customer-validated proof attributed to voice-originated opportunities

الهدف ليس زيادة عدد المكالمات؛ الهدف هو **Real Interaction -> Qualified Problem -> Verified Cash -> Customer Proof**.
