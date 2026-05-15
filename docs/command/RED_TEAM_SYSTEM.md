# Red Team System — الفريق الأحمر الداخلي

**الفكرة:** اختبار العرض أو المشروع **قبل** الالتزام — مهاجمة الذات بأسئلة حادة.

## أسئلة (نعم/لا في المراجعة)

- هل هذا مجرد **custom work** بلا أصول؟  
- هل يوجد **proof** حقيقي؟  
- هل هناك خطر **PII**؟  
- هل هناك **وعد مبالغ**؟  
- هل نستطيع **تسليمه مرة ثانية** بنفس الجودة؟  
- هل العميل **جاهز لـ retainer** (إن كان ذلك الهدف)؟  
- هل نبني **feature** قبل السوق؟  
- هل الشريك قد **يضر الثقة**؟  
- هل هذا **يراكم capital**؟  

## مخرجات

- Proceed  
- Proceed with controls  
- Rescope  
- Reject  
- Escalate  

## الكود

`auto_client_acquisition/command_os/red_team.py` — `red_team_verdict(...)` بقواعد أولوية بسيطة ومحافظة (قابلة لتوسيعها لاحقًا).

**صعود:** [`SOVEREIGN_COMMAND_SYSTEM.md`](SOVEREIGN_COMMAND_SYSTEM.md)
