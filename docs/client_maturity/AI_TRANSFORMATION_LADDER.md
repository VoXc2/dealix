# Dealix AI Transformation Ladder — سلم التحول (0–7)

Dealix لا تبيع **نفس الشيء** لكل عميل. تُقيس **نضج العميل** ثم تُحرّكه درجة بدرجة: من فوضى AI إلى تشغيل محكوم، ثم **Sprint → Retainer → طبقة تشغيل (Platform pull)**.

## لماذا النضج؟

كثير من الشركات تستثمر في AI دون ربط واضح بالأدوار والبيانات والحوكمة وROI. الفشل غالبًا في **تصميم العمل والأدوار والتكامل** أكثر من «ضعف النموذج». لذلك AI عند Dealix هو **رحلة نضج** لا feature واحد.

## القواعد السريعة

| إن كان العميل… | فلا تبيعه… | بِعْه… |
|----------------|-------------|--------|
| غير جاهز | منصة | تشخيص |
| بيانات ضعيفة | agent | Data Readiness |
| بلا owner | automation | Workflow Ownership |
| بلا proof | scaling | Proof Pack |
| بلا adoption | expansion | تمكين + cadence |
| بلا audit need | Control Plane | طبقة أخف حتى تنضج الحوكمة |

---

## Level 0 — AI Chaos

**الحالة:** استخدام شخصي عشوائي؛ موظفون على أدوات AI بلا سياسة؛ لا مصادر بيانات واضحة؛ لا موافقات؛ لا proof.  
**الخطر:** بيانات حساسة في أدوات عامة؛ مخرجات غير دقيقة؛ قرارات بلا تدقيق؛ **Shadow AI** يخرج عن رقابة IT.  
**عرض Dealix:** AI Governance & Readiness Diagnostic.  
**ممنوع:** agents، منصة، external automation، outreach.  
**الهدف (0→1):** AI Inventory، Use Case Risk Classification، إعداد Source Passport، حدود حوكمة أولية.

---

## Level 1 — AI Awareness

**الحالة:** الإدارة مقتنعة بأهمية AI؛ حماس؛ لكن لا use cases واضحة ولا أهداف ROI.  
**عرض Dealix:** Capability Diagnostic.  
**مخرجات:** Capability Score، Transformation Gap، use cases موصى بها، مخاطر جاهزية بيانات، مخاطر حوكمة، **توصية أول Sprint**.  
**فرع القرار (بعد التشخيص):**

- الألم قريب من الإيراد → **Revenue Intelligence Sprint**  
- الخطر أعلى من القيمة → **AI Governance Review**  
- المعرفة مبعثرة → **Company Brain Sprint**  

(الدالة البرمجية: `level1_first_track` في `offer_matrix.py`.)

**ممنوع:** منصة كاملة، Enterprise OS مبكرًا.

---

## Level 2 — Structured Use Case

**الحالة:** use case واضح؛ owner؛ مصدر معروف؛ لكن الـ workflow لم يدخل AI بعد.  
**عرض Dealix:** Productized Sprint (Revenue Intelligence / Company Brain / AI Quick Win).  
**شروط الدخول:** Source Passport، Workflow owner، مقياس نجاح، حدود حوكمة.  
**مخرجات:** مخرجات بمساعدة AI، Draft Pack، Workflow Map، Proof Pack، Next Action.  
**ممنوع:** Enterprise OS قبل إثبات أول sprint.

---

## Level 3 — AI-Assisted Workflow

**الحالة:** AI يساعد في draft أو scoring أو summary؛ مراجعة بشرية موجودة؛ **الحوكمة والـ audit غير مكتملة**.  
**عرض Dealix:** Governance Runtime Setup + Proof Pack System + Monthly Operating Cadence.  
**الهدف (3→4):** governance decisions، approval workflow، AI run ledger، QA rubric، proof metrics.  
**ممنوع:** external automation بلا موافقة.

---

## Level 4 — Governed AI Workflow

**الحالة:** كل output له governance status؛ كل إجراء خارجي يحتاج موافقة؛ كل مصدر له passport؛ كل AI run مسجل؛ كل مشروع له proof.  
**عرض Dealix:** Monthly Retainer (Monthly RevOps OS / Monthly Governance / Monthly Company Brain / Monthly AI Ops).  
**لماذا؟** العميل عنده **قدرة قابلة للتشغيل** وليس مجرد مشروع واحد.  
**شروط Retainer:** Proof ≥ 80، Adoption ≥ 70، owner، cadence شهري، مخاطر حوكمة مسيطر عليها.  
**ممنوع:** وكلاء مستقلون بالكامل عن مسار الموافقة.

---

## Level 5 — Operating AI Capability

**الحالة:** workflow ضمن cadence أسبوعي/شهري؛ الإدارة ترى value report؛ استخدام متكرر للمخرجات؛ proof يتحسن شهريًا.  
**عرض Dealix:** Client Workspace + Proof Timeline + Value Dashboard + Approval Center.  
**الهدف:** تحويل Dealix من **خدمة** إلى **طبقة تشغيل** داخل العميل.  
**Platform Pull Signals:** عدة مستخدمين يحتاجون وصولًا؛ تكرار الموافقات؛ تكرار تقارير proof؛ طلب لوحة تنفيذية؛ طلب audit.

---

## Level 6 — Multi-Workflow AI OS

**الحالة:** أكثر من إدارة تستخدم Dealix (Revenue + Operations + Knowledge + Governance)؛ احتياجات cross-workflow.  
**عرض Dealix:** Enterprise AI Operations Program.  
**مخرجات:** multi-workflow dashboard، AI inventory، governance map، executive value dashboard، risk dashboard، proof عبر الأقسام.  
**ممنوع:** white-label مبكرًا.

---

## Level 7 — Enterprise AI Control Plane

**الحالة:** حاجة audit exports، Agent registry، Policy registry، AI run ledger، RBAC/SSO لاحقًا، incident response.  
**عرض Dealix:** AI Control Plane + Enterprise Governance Program.  
**تحذير:** لا تدخل L7 مبكرًا — ضوابط enterprise مكلفة ومعقدة.  
**شروط الدخول:** 3+ workflows، راعٍ تنفيذي، مالك حوكمة، حاجة audit، cadence شهري، ميزانية واضحة.  
**ممنوع:** بيع Control Plane **بدون** مسار audit واضح.

---

## الخلاصة

Dealix تفوز عندما **لا تبيع AI كمنتج واحد للجميع**، بل تقود كل عميل عبر سلم واضح: فوضى → وعي → use case → مساعدة محكومة → تشغيل شهري → قدرة تشغيلية → نظام مؤسسي → طائرة تحكم قابلة للتدقيق.

## مراجع

- [CLIENT_MATURITY_ENGINE.md](CLIENT_MATURITY_ENGINE.md)  
- [MATURITY_TO_OFFER_MATRIX.md](MATURITY_TO_OFFER_MATRIX.md)  
- [MATURITY_DASHBOARD.md](MATURITY_DASHBOARD.md)  
- الكود: `auto_client_acquisition/client_maturity_os/`
