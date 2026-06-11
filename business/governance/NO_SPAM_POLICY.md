# No Spam Policy (Dealix)

## لا، بكل بساطة
- لا spam. هذا ليس استثناء.
- لا توجد "حالات خاصة" يرسل فيها المزعج.
- لا "mass blast" بحجة الوقت.
- لا "unverified lead" يدخل قائمة.
- لا "auto follow-up" بدون review_status.

## الاختبار
- `tests/test_no_auto_send.py` يفشل CI إذا لقي نمط إرسال آلي
- `scripts/check_no_secrets.py` يفشل إذا لقي API keys مكشوفة
- `tests/test_review_status_required.py` يفشل إذا draft بدون review_status

## الثقافة
- كل عضو في الفريق يعرف: إرسال بدون موافقة = مخالفة
- المراجعة البشرية ليست bottleneck، هي جودة
- "نقدر نرسل بسرعة" ليس ميزة، هو خطر
