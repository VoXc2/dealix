#!/usr/bin/env python3
"""
Dealix Acquisition Pack Generator
=================================
For every target company in company_os/revenue/prospects.csv this builds the
acquisition layer used to win the client:

  - Company Intelligence Pack   -> data/acquisition/company_intelligence_packs.jsonl
  - Client Need Card            -> data/acquisition/client_need_cards.jsonl
  - Call Brief                  -> data/acquisition/call_briefs.jsonl
  - Mini Proposal               -> data/acquisition/mini_proposals.jsonl

The recommended system is chosen deterministically from the prospect pain, then
the first contact role is resolved from data/acquisition/contact_targets.jsonl.

Hard rules baked in:
  - Every email/proposal stays a DRAFT (approval_required = true).
  - No guaranteed-revenue claims in any generated copy.
  - No fake Re:/Fwd: subjects.
  - Call briefs are for human callers only (automated_calling = false).
  - Roles only — never personal names.
"""

import argparse
import csv
import json
from pathlib import Path

RUN_DATE = "2026-06-03"

SYSTEMS = (
    "Revenue Operating System",
    "Executive Command OS",
    "Follow-up Recovery OS",
    "WhatsApp Client OS",
    "Proposal & Proof OS",
)

# Deterministic pain -> system map (exact prospects.csv pain strings).
PAIN_TO_SYSTEM = {
    "Leads not converting": "Revenue Operating System",
    "No follow-up system": "Follow-up Recovery OS",
    "WhatsApp inquiries lost": "WhatsApp Client OS",
    "Low registration rate": "Follow-up Recovery OS",
    "Slow deal closure": "Revenue Operating System",
    "Weak CRM usage": "Revenue Operating System",
    "No proof for clients": "Proposal & Proof OS",
    "Seasonal campaigns fail": "Executive Command OS",
    "Proposals not tracked": "Proposal & Proof OS",
    "Founder blind to pipeline": "Executive Command OS",
    "Client churn due to no ROI proof": "Proposal & Proof OS",
    "Follow-up takes too long": "Follow-up Recovery OS",
    "Deals stuck in proposal stage": "Proposal & Proof OS",
    "Leads from ads not followed up": "Follow-up Recovery OS",
    "Inquiry to enrollment gap": "Follow-up Recovery OS",
}

# Keyword fallback for any pain not in the explicit map above.
KEYWORD_FALLBACK = (
    ("whatsapp", "WhatsApp Client OS"),
    ("proof", "Proposal & Proof OS"),
    ("proposal", "Proposal & Proof OS"),
    ("roi", "Proposal & Proof OS"),
    ("blind", "Executive Command OS"),
    ("pipeline", "Executive Command OS"),
    ("report", "Executive Command OS"),
    ("campaign", "Executive Command OS"),
    ("follow", "Follow-up Recovery OS"),
    ("registration", "Follow-up Recovery OS"),
    ("enrollment", "Follow-up Recovery OS"),
    ("lead", "Revenue Operating System"),
    ("crm", "Revenue Operating System"),
    ("deal", "Revenue Operating System"),
)

# Arabic rendering of each English pain string for personalised copy.
PAIN_AR = {
    "Leads not converting": "وصول فرص جيدة لكنها لا تتحول إلى مبيعات بالشكل المتوقع",
    "No follow-up system": "غياب نظام متابعة موحد بعد أول تواصل",
    "WhatsApp inquiries lost": "ضياع جزء من استفسارات واتساب قبل أن تتحول إلى عملاء",
    "Low registration rate": "انخفاض نسبة تحول الاستفسارات إلى تسجيلات",
    "Slow deal closure": "بطء إغلاق الصفقات مقارنة بحجم الفرص المتاحة",
    "Weak CRM usage": "تشتت بيانات الفرص وضعف الاعتماد على نظام موحد لإدارتها",
    "No proof for clients": "صعوبة تقديم دليل واضح على النتائج للعملاء",
    "Seasonal campaigns fail": "تذبذب الأداء بين المواسم وغياب الصورة التنفيذية اليومية",
    "Proposals not tracked": "عدم تتبع العروض بعد إرسالها",
    "Founder blind to pipeline": "عدم وضوح الصورة اليومية لخط الفرص أمام الإدارة",
    "Client churn due to no ROI proof": "تسرب العملاء بسبب غياب دليل واضح على العائد",
    "Follow-up takes too long": "تأخر المتابعة بعد أول تواصل مع العميل",
    "Deals stuck in proposal stage": "توقف الصفقات عند مرحلة العرض دون حسم",
    "Leads from ads not followed up": "عدم متابعة الفرص القادمة من الحملات الإعلانية",
    "Inquiry to enrollment gap": "وجود فجوة بين الاستفسار والتسجيل الفعلي",
}

# Per-system acquisition content. AR copy, English structure. No guarantee words.
SYSTEM_CONTENT = {
    "Revenue Operating System": {
        "signal": "وجود فرص ومبيعات قائمة بلا نظام تشغيل موحد يربط الفرصة بالخطوة التالية",
        "why": "النظام يبني خريطة تسرب الإيراد ويعطي كل فرصة حالة وخطوة تالية وتقريراً واضحاً للإدارة، وهو أسرع طريق لرؤية أين تضيع المبيعات الحالية.",
        "first_mission": "بناء Revenue Leakage Map ونموذج مراحل الفرص خلال أول سبرنت.",
        "proof_angle": "إظهار نقطة التسرب الأكبر بين الاستفسار والإغلاق برقم تقريبي قابل للنقاش.",
        "email_intro": "نعمل مع شركات لديها فرص ومبيعات قائمة لكن بلا نظام تشغيل موحد يربط كل فرصة بخطوتها التالية.",
        "call_opener": "تواصلنا لأن الشركات في وضعكم غالباً تملك طلباً جيداً لكن جزءاً من الإيراد يتسرب بين الاستفسار والإغلاق بسبب غياب نظام موحد.",
        "call_questions": [
            "هل عندكم مصدر واحد واضح لكل الفرص أم موزعة على أكثر من مكان؟",
            "هل كل فرصة (lead) لها حالة وخطوة تالية محددة؟",
            "هل تصل الإدارة تقرير أسبوعي واضح عن الفرص والإيراد؟",
        ],
        "objections": [
            "عندنا CRM بالفعل",
            "الفريق مشغول ولا يوجد وقت لنظام جديد",
        ],
        "best_response": "لا نستبدل أدواتكم؛ نرتب ما لديكم في نظام تشغيل يعطي كل فرصة خطوة تالية وتقريراً واحداً للإدارة، والسبرنت قصير ومخرجاته جاهزة للاستخدام.",
        "mini_proposal_angle": "سبرنت 7 أيام لبناء نظام تشغيل الإيراد وكشف أكبر نقطة تسرب.",
        "current_state": "فرص ومبيعات قائمة بلا نظام تشغيل موحد، وخطوات المتابعة تعتمد على اجتهاد الفريق.",
        "desired_outcome": "نظام تشغيل يعطي كل فرصة حالة وخطوة تالية، وتقرير إيراد واضح للإدارة.",
        "success_metric": "كل فرصة لها حالة وخطوة تالية، ووجود تقرير إيراد أسبوعي واحد معتمد.",
        "required_inputs": [
            "مصادر الاستفسارات",
            "ملف leads أو CRM export إن وجد",
            "مراحل البيع الحالية",
            "قنوات التواصل",
            "أمثلة رسائل حالية",
            "صاحب القرار",
        ],
        "sprint_title": "7-Day Revenue Operating Sprint",
        "first_sprint": "نبني Revenue Leakage Map ونموذج مراحل الفرص ونرتب المتابعة في نظام واحد.",
        "deliverables": [
            "Revenue Leakage Map",
            "Opportunity Stage Model",
            "Follow-up Workflow",
            "Draft Templates",
            "Weekly Revenue Report",
            "Founder Next-Action List",
        ],
        "starter_price": "تبدأ من 4,500 ريال",
        "starter_price_sar": 4500,
        "expected_first_proof": "خريطة مبدئية تُظهر أين تتسرب أكبر نسبة من الفرص.",
        "next_step": "مكالمة 20 دقيقة لفهم مصادر الفرص وقنوات التواصل.",
    },
    "Executive Command OS": {
        "signal": "غياب صورة تنفيذية يومية تربط الأرقام بالقرار التالي",
        "why": "النظام يحوّل الأرقام المبعثرة إلى تقرير قيادة يومي يوضح أهم قرار، ويرتب المخاطر والفرص، وهو أسرع قيمة للمؤسس أو المدير الذي يفتقد الصورة اليومية.",
        "first_mission": "بناء KPI Map وتقرير القيادة اليومي خلال أول سبرنت.",
        "proof_angle": "تحويل أرقام يوم واحد إلى تقرير يوضح القرار التالي بدل عرض الأرقام فقط.",
        "email_intro": "نعمل مع مؤسسين ومدراء يحتاجون صورة تنفيذية يومية واضحة تربط الأرقام بالقرار التالي بدل مجرد لوحات أرقام.",
        "call_opener": "تواصلنا لأن كثيراً من القيادات ترى أرقاماً يومية لكنها لا تترجم إلى قرار واضح، وهنا غالباً يبدأ التعطل.",
        "call_questions": [
            "ما أهم تقرير تطّلع عليه الإدارة يومياً؟",
            "هل التقرير يقول القرار التالي أم يعرض أرقاماً فقط؟",
            "أين أكثر نقطة تعطل تتكرر في القرارات؟",
        ],
        "objections": [
            "عندنا لوحات بيانات (dashboards) كثيرة",
            "الإدارة تتابع الأمور بشكل غير رسمي",
        ],
        "best_response": "اللوحات تعرض أرقاماً؛ ما نبنيه يعطي قراراً يومياً مرتباً حسب الأثر والمخاطرة، وهذا ما يصعب استخلاصه من لوحات متعددة.",
        "mini_proposal_angle": "سبرنت 7 أيام لبناء تقرير قيادة يومي يوضح القرار التالي.",
        "current_state": "أرقام موزعة على أكثر من مصدر بلا تقرير قيادة يومي موحد يوضح أهم قرار.",
        "desired_outcome": "تقرير قيادة يومي يوضح أهم قرار، مع ترتيب واضح للمخاطر والفرص.",
        "success_metric": "تقرير يومي يوضح القرار التالي، ومصفوفة مخاطر/فرص مرتبة، وسجل قرارات واضح.",
        "required_inputs": [
            "أهم أهداف الشركة",
            "مؤشرات المبيعات الحالية",
            "مصادر العملاء",
            "أهم المخاطر",
            "شكل التقارير الحالية",
            "المسؤولون الداخليون",
        ],
        "sprint_title": "7-Day Executive Command Sprint",
        "first_sprint": "نبني KPI Map وتقرير قيادة يومي ومصفوفة مخاطر/أولويات وسجل قرارات.",
        "deliverables": [
            "KPI Map",
            "Daily Command Report",
            "Risk/Priority Matrix",
            "Decision Log",
            "Executive Action Board",
            "Weekly Executive Review Template",
        ],
        "starter_price": "تبدأ من 4,000 ريال",
        "starter_price_sar": 4000,
        "expected_first_proof": "نموذج تقرير قيادة ليوم واحد يوضح أهم قرار بدل عرض الأرقام فقط.",
        "next_step": "مكالمة 20 دقيقة لفهم أهداف الشركة وشكل التقارير الحالية.",
    },
    "Follow-up Recovery OS": {
        "signal": "ضياع جزء من الفرص بعد أول تواصل بسبب متابعة غير منظمة",
        "why": "النظام يبني طابور متابعة ونموذج حالات ورسائل جاهزة حسب حالة العميل، وهو أسرع قيمة عندما تضيع الفرص بعد أول رد.",
        "first_mission": "بناء Follow-up Queue ونموذج حالات الفرص خلال أول سبرنت.",
        "proof_angle": "إظهار عدد الفرص القابلة للاسترجاع التي توقفت متابعتها.",
        "email_intro": "نعمل مع شركات تصلها استفسارات جيدة لكن جزءاً منها يتوقف بعد أول تواصل بسبب غياب متابعة منظمة.",
        "call_opener": "تواصلنا لأن الشركات في وضعكم غالباً تخسر جزءاً من الفرص ليس بسبب ضعف الطلب، بل بسبب متابعة غير منتظمة بعد أول رد.",
        "call_questions": [
            "هل عندكم متابعة موحدة بعد أول تواصل أم تعتمد على اجتهاد الفريق؟",
            "كم فرصة تقديرياً تضيع بسبب تأخر المتابعة؟",
            "هل الرسائل جاهزة حسب حالة العميل أم تُكتب كل مرة من جديد؟",
        ],
        "objections": [
            "الفريق يتابع بالفعل",
            "ما عندنا قائمة منظمة للفرص",
        ],
        "best_response": "حتى لو الفريق يتابع، غياب الطابور والرسائل الجاهزة يجعل المتابعة متذبذبة؛ نرتب ذلك في نظام بسيط قابل للاستخدام فوراً، ونبدأ مما لديكم مهما كان بسيطاً.",
        "mini_proposal_angle": "سبرنت 7 أيام لاسترجاع الفرص وبناء نظام متابعة.",
        "current_state": "استفسارات تصل لكن المتابعة بعد أول تواصل غير منظمة، وبعض الفرص يتوقف بلا سبب واضح.",
        "desired_outcome": "طابور متابعة واضح، ورسائل جاهزة حسب حالة كل عميل، وإيقاع متابعة ثابت.",
        "success_metric": "وجود طابور متابعة، ولكل فرصة رسالة مناسبة، وإيقاع متابعة واضح، وتقرير أسبوعي.",
        "required_inputs": [
            "قائمة leads أو محادثات",
            "آخر تواصل لكل فرصة",
            "حالة كل lead إن وجدت",
            "قنوات المتابعة",
            "أمثلة ردود العملاء",
        ],
        "sprint_title": "7-Day Follow-up Recovery Sprint",
        "first_sprint": "نبني follow-up queue ونموذج حالات ورسائل متابعة حسب حالة العميل وإيقاع تذكير.",
        "deliverables": [
            "Follow-up Queue",
            "Lead Status Model",
            "Follow-up Message Set",
            "Reminder Rhythm",
            "Recovery Report",
            "Escalation Rules",
        ],
        "starter_price": "تبدأ من 3,500 ريال",
        "starter_price_sar": 3500,
        "expected_first_proof": "قائمة أولية بالفرص القابلة للاسترجاع التي توقفت متابعتها.",
        "next_step": "مكالمة 20 دقيقة لفهم مصادر الاستفسارات وقنوات المتابعة.",
    },
    "WhatsApp Client OS": {
        "signal": "واتساب قناة رئيسية لكن الطلبات داخله غير مصنفة وبلا تصعيد واضح",
        "why": "النظام يرسم flows لمحادثات واتساب ويضع سياسة تصعيد لإنسان وبوابة آمنة للملفات، وهو أسرع قيمة عندما يكون واتساب القناة الأساسية.",
        "first_mission": "بناء WhatsApp Flow Map وReadiness Scan خلال أول سبرنت.",
        "proof_angle": "إظهار أنواع الطلبات الأكثر تكراراً ونقاط التأخر قبل التصعيد لإنسان.",
        "email_intro": "نعمل مع شركات يكون واتساب فيها قناة رئيسية، فنرتب المحادثات في مسارات واضحة مع سياسة تصعيد لإنسان بدل بوت عام مفتوح.",
        "call_opener": "تواصلنا لأن واتساب عندما يكون القناة الرئيسية، غياب التصنيف وسياسة التصعيد يجعل بعض الطلبات تتأخر أو تضيع.",
        "call_questions": [
            "هل واتساب قناة رئيسية في التواصل مع عملائكم؟",
            "هل الطلبات داخله مصنفة حسب نوعها؟",
            "متى يتم تصعيد المحادثة لإنسان؟",
        ],
        "objections": [
            "نبي بوت يرد على كل شيء",
            "الخصوصية والملفات تقلقنا",
        ],
        "best_response": "لا نوصي ببوت عام مفتوح؛ نصمم مسارات مضبوطة مع تصعيد واضح لإنسان وبوابة آمنة للملفات، بحيث لا تُطلب أسرار داخل واتساب.",
        "mini_proposal_angle": "سبرنت 7 أيام لترتيب محادثات واتساب وبناء سياسة تصعيد.",
        "current_state": "واتساب قناة رئيسية لكن الطلبات غير مصنفة، والتصعيد لإنسان غير واضح.",
        "desired_outcome": "مسارات واضحة للمحادثات، وسياسة تصعيد لإنسان، وبوابة آمنة للملفات.",
        "success_metric": "وجود flows للمحادثات، وتصعيد واضح لإنسان، وعدم طلب أسرار داخل واتساب.",
        "required_inputs": [
            "أنواع الطلبات في واتساب",
            "أكثر الأسئلة تكراراً",
            "متى يحتاج العميل تصعيداً لإنسان",
            "الروابط أو النماذج المستخدمة",
            "سياسة الملفات والصلاحيات",
        ],
        "sprint_title": "7-Day WhatsApp Client Sprint",
        "first_sprint": "نرسم WhatsApp Flow Map ونجهز Action Cards وسياسة تصعيد لإنسان وبوابة آمنة للملفات.",
        "deliverables": [
            "WhatsApp Flow Map",
            "Readiness Scan",
            "Action Cards",
            "Human Handoff Policy",
            "Secure Portal Handoff Guide",
            "Weekly WhatsApp Review",
        ],
        "starter_price": "تبدأ من 3,500 ريال",
        "starter_price_sar": 3500,
        "expected_first_proof": "خريطة أولية لأنواع الطلبات ونقاط التأخر قبل التصعيد لإنسان.",
        "next_step": "مكالمة 20 دقيقة لفهم أنواع الطلبات وسياسة الملفات.",
    },
    "Proposal & Proof OS": {
        "signal": "عروض بطيئة أو ضعيفة أو بلا دليل واضح على النتائج",
        "why": "النظام يبني قالب عرض وحزمة دليل ونطاقاً واضحاً وقائمة مراجعة، وهو أسرع قيمة عندما تكون العروض بطيئة أو بلا proof.",
        "first_mission": "بناء Proposal Template وProof Pack Template خلال أول سبرنت.",
        "proof_angle": "إظهار الفرق بين العرض الحالي وعرض واضح النطاق مدعوم بدليل.",
        "email_intro": "نعمل مع شركات تريد عروضاً أوضح وأسرع ومدعومة بدليل، فنبني قالب عرض وحزمة proof ونطاقاً واضحاً.",
        "call_opener": "تواصلنا لأن العرض البطيء أو غير المدعوم بدليل غالباً يكلف صفقات كان يمكن إغلاقها.",
        "call_questions": [
            "كم يستغرق تجهيز العرض لديكم عادة؟",
            "هل يحتوي العرض على نطاق واضح ودليل (proof)؟",
            "ما أكثر اعتراض يتكرر على عروضكم؟",
        ],
        "objections": [
            "عندنا قالب عرض بالفعل",
            "كل عميل مختلف ويصعب توحيد العرض",
        ],
        "best_response": "نبقي المرونة لكل عميل، لكن نضيف نطاقاً واضحاً وحزمة دليل وقائمة مراجعة تجعل العرض أسرع تجهيزاً وأقوى في الإقناع.",
        "mini_proposal_angle": "سبرنت 7 أيام لبناء نظام عروض ودليل أقوى.",
        "current_state": "عروض تُجهَّز ببطء أو بلا نطاق واضح أو دليل، ما يطيل دورة الإغلاق.",
        "desired_outcome": "قالب عرض واضح النطاق مدعوم بدليل، مع قائمة مراجعة قبل الإرسال.",
        "success_metric": "العرض واضح النطاق، ويحتوي زاوية دليل، وله خطوة تالية، وبلا وعود مبالغ فيها.",
        "required_inputs": [
            "الخدمة أو المنتج",
            "نموذج عرض سابق إن وجد",
            "اعتراضات العملاء",
            "أمثلة أعمال سابقة",
            "نطاق الخدمة",
            "الأسعار التقريبية",
        ],
        "sprint_title": "7-Day Proposal & Proof Sprint",
        "first_sprint": "نبني Proposal Template وProof Pack وكتلة نطاق/خارج النطاق وقائمة مراجعة العرض.",
        "deliverables": [
            "Proposal Template",
            "Proof Pack Template",
            "Scope / Out-of-scope",
            "Risk & Assumption Block",
            "Next-step Card",
            "Proposal Review Checklist",
        ],
        "starter_price": "تبدأ من 3,000 ريال",
        "starter_price_sar": 3000,
        "expected_first_proof": "مسودة عرض واحدة واضحة النطاق ومدعومة بزاوية دليل.",
        "next_step": "مكالمة 20 دقيقة لفهم الخدمة والاعتراضات المتكررة.",
    },
}


def load_prospects(path: Path) -> list[dict]:
    rows: list[dict] = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rows.append(row)
    except FileNotFoundError:
        print(f"Warning: {path} not found.")
    return rows


def load_contact_targets(path: Path) -> dict[str, dict]:
    targets: dict[str, dict] = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    obj = json.loads(line)
                    targets[obj["system"]] = obj
    except FileNotFoundError:
        print(f"Warning: {path} not found.")
    return targets


def pick_system(pain: str) -> str:
    if pain in PAIN_TO_SYSTEM:
        return PAIN_TO_SYSTEM[pain]
    low = pain.lower()
    for keyword, system in KEYWORD_FALLBACK:
        if keyword in low:
            return system
    return "Revenue Operating System"


def resolve_contact_role(system: str, sector: str, targets: dict[str, dict]) -> str:
    target = targets.get(system, {})
    overrides = target.get("sector_overrides", {})
    if sector in overrides:
        return overrides[sector]
    primary = target.get("primary_roles", [])
    return primary[0] if primary else "Founder"


def build_email(company: str, role: str, pain_ar: str, content: dict) -> str:
    return (
        "السلام عليكم،\n"
        f"أكتب لكم بخصوص {company}. {content['email_intro']}\n"
        f"لاحظنا من المؤشرات العامة احتمال {pain_ar}.\n"
        f"الفكرة ليست أداة جديدة، بل {content['sprint_title']} يوضح أين تحديداً تحدث الخسارة "
        "ويسلّمكم مخرجات جاهزة للاستخدام، بلا أي التزام مالي قبل وضوح القيمة.\n"
        "هل يناسبكم أن أرسل ملخصاً مختصراً من صفحة واحدة قبل أي خطوة؟"
    )


def build_pack(idx: int, prospect: dict, system: str, role: str, content: dict) -> dict:
    pain = prospect.get("pain", "")
    pain_ar = PAIN_AR.get(pain, pain)
    company = prospect.get("company", "")
    return {
        "pack_id": f"CIP-{idx:03d}",
        "company": company,
        "website": prospect.get("website", ""),
        "country": "Saudi Arabia",
        "city": "",
        "sector": prospect.get("segment", ""),
        "public_contact_channels": ["website", "email", "whatsapp"],
        "likely_decision_maker": prospect.get("decision_maker", ""),
        "best_contact_role": role,
        "signal": content["signal"],
        "likely_pain": pain_ar,
        "recommended_system": system,
        "why_this_system": content["why"],
        "first_mission": content["first_mission"],
        "proof_angle": content["proof_angle"],
        "email_subject": f"{company}: {content['mini_proposal_angle']}",
        "email_draft": build_email(company, role, pain_ar, content),
        "call_opener": content["call_opener"],
        "call_questions": content["call_questions"],
        "expected_objections": content["objections"],
        "mini_proposal_angle": content["mini_proposal_angle"],
        "next_action": "إرسال المسودة لقائمة موافقة المؤسس قبل أي تواصل خارجي.",
        "risk_level": "low",
        "evidence_level": "public_only",
        "approval_required": True,
        "do_not_contact": False,
        "created_at": RUN_DATE,
    }


def build_need_card(idx: int, prospect: dict, system: str, role: str, content: dict) -> dict:
    pain = prospect.get("pain", "")
    pain_ar = PAIN_AR.get(pain, pain)
    try:
        score = int(prospect.get("score", 0))
    except ValueError:
        score = 0
    urgency = "high" if score >= 9 else "medium" if score >= 7 else "low"
    return {
        "card_id": f"CNC-{idx:03d}",
        "company": prospect.get("company", ""),
        "sector": prospect.get("segment", ""),
        "recommended_system": system,
        "current_state": content["current_state"],
        "pain_hypothesis": pain_ar,
        "desired_outcome": content["desired_outcome"],
        "success_metric": content["success_metric"],
        "required_inputs": content["required_inputs"],
        "decision_maker_target": role,
        "urgency": urgency,
        "evidence_level": "public_only",
        "next_action": content["next_step"],
        "created_at": RUN_DATE,
    }


def build_call_brief(idx: int, prospect: dict, system: str, role: str, content: dict) -> dict:
    pain = prospect.get("pain", "")
    pain_ar = PAIN_AR.get(pain, pain)
    company = prospect.get("company", "")
    return {
        "brief_id": f"CB-{idx:03d}",
        "company": company,
        "contact_role": role,
        "recommended_system": system,
        "likely_pain": pain_ar,
        "email_sent_summary": f"مسودة بريد حول {content['mini_proposal_angle']} (بانتظار موافقة المؤسس).",
        "call_objective": f"التحقق من فرضية الألم وحجز مكالمة اكتشاف لـ {content['sprint_title']}.",
        "opening_line": content["call_opener"],
        "discovery_questions": content["call_questions"],
        "expected_objection": content["objections"][0] if content["objections"] else "",
        "best_response": content["best_response"],
        "next_step": content["next_step"],
        "caller_type": "human",
        "automated_calling": False,
        "created_at": RUN_DATE,
    }


def build_mini_proposal(idx: int, prospect: dict, system: str, content: dict) -> dict:
    pain = prospect.get("pain", "")
    pain_ar = PAIN_AR.get(pain, pain)
    company = prospect.get("company", "")
    return {
        "proposal_id": f"MP-{idx:03d}",
        "title": f"{content['sprint_title']} — {company}",
        "company": company,
        "recommended_system": system,
        "why_this_system": content["why"],
        "current_likely_pain": pain_ar,
        "first_sprint": content["first_sprint"],
        "deliverables": content["deliverables"],
        "timeline": "7 أيام",
        "starter_price": content["starter_price"],
        "starter_price_sar": content["starter_price_sar"],
        "required_inputs": content["required_inputs"],
        "expected_first_proof": content["expected_first_proof"],
        "next_step": content["next_step"],
        "approval_required": True,
        "created_at": RUN_DATE,
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Dealix acquisition packs")
    parser.add_argument("--prospects", default=None)
    parser.add_argument("--out", default=None, help="data/acquisition output dir")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent.parent
    prospects_path = Path(args.prospects) if args.prospects else base / "company_os" / "revenue" / "prospects.csv"
    out_dir = Path(args.out) if args.out else base / "data" / "acquisition"
    targets_path = out_dir / "contact_targets.jsonl"

    prospects = load_prospects(prospects_path)
    targets = load_contact_targets(targets_path)

    # Stable, deterministic order: highest score first, then company name.
    def sort_key(p: dict) -> tuple:
        try:
            score = int(p.get("score", 0))
        except ValueError:
            score = 0
        return (-score, p.get("company", ""))

    prospects.sort(key=sort_key)

    packs, cards, briefs, proposals = [], [], [], []
    system_counts: dict[str, int] = {s: 0 for s in SYSTEMS}

    for i, prospect in enumerate(prospects, start=1):
        pain = prospect.get("pain", "")
        system = pick_system(pain)
        content = SYSTEM_CONTENT[system]
        role = resolve_contact_role(system, prospect.get("segment", ""), targets)
        system_counts[system] += 1

        packs.append(build_pack(i, prospect, system, role, content))
        cards.append(build_need_card(i, prospect, system, role, content))
        briefs.append(build_call_brief(i, prospect, system, role, content))
        proposals.append(build_mini_proposal(i, prospect, system, content))

    write_jsonl(out_dir / "company_intelligence_packs.jsonl", packs)
    write_jsonl(out_dir / "client_need_cards.jsonl", cards)
    write_jsonl(out_dir / "call_briefs.jsonl", briefs)
    write_jsonl(out_dir / "mini_proposals.jsonl", proposals)

    print("✅ Acquisition packs generated")
    print(f"   Companies processed: {len(prospects)}")
    for system in SYSTEMS:
        print(f"   - {system}: {system_counts[system]}")
    print(f"   Output: {out_dir}")


if __name__ == "__main__":
    main()
