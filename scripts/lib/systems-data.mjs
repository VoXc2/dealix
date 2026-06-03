// Shared configuration for the Daily 400 Draft Factory.
// Mirrors src/data/systems.ts (kept in sync manually) plus outreach-specific
// fields: daily distribution, email templates, mission, proof angle.
//
// IMPORTANT: drafts produced from this config are ALWAYS pending_approval and
// are NOT send-ready by default. Sending requires founder approval + domain
// authentication (SPF/DKIM/DMARC) + a verified, opted-in contact list.

/**
 * @typedef {Object} EmailContext
 * @property {string} company
 * @property {string} city
 * @property {string} sector
 * @property {string} signal
 */

export const SYSTEMS = [
  {
    slug: "revenue-operating-system",
    nameAr: "نظام تشغيل الإيرادات",
    nameEn: "Revenue Operating System",
    dailyCount: 100,
    startingPrice: 4500,
    firstMission: "Revenue Sprint افتتاحي (7–10 أيام)",
    proofAngle: "قبل/بعد خريطة تسرب الإيراد + أول workflow متابعة",
    whyThisSystem:
      "أسرع قيمة تظهر في كشف أين تضيع الفرص وبناء إجراء تالٍ واضح لكل فرصة.",
    cta: "أرسل لك تصور مختصر لأول Revenue Sprint يناسب شركتك؟",
    /** @param {EmailContext} c */
    email: (c) => ({
      subject: "أين تضيع فرص الإيراد عندكم؟",
      body: [
        "السلام عليكم [الاسم/الفريق]،",
        "",
        `راجعت حضور ${c.company} في قطاع ${c.sector} بمدينة ${c.city}، والظاهر أن عندكم أكثر من نقطة تواصل مع العملاء مثل ${c.signal}.`,
        "",
        "في هذا النوع من الشركات، المشكلة غالبًا لا تكون في قلة الفرص، بل في أن كل فرصة لا يكون لها خطوة تالية واضحة: من يتابع؟ متى؟ وماذا يقال؟ ومتى تتحول الفرصة إلى عرض أو اجتماع؟",
        "",
        "نبني نظام تشغيل الإيرادات يبدأ بخريطة تسرب بسيطة، ثم يحولها إلى workflow متابعة وتقرير يومي للإدارة.",
        "",
        "إذا مناسب، أرسل لك تصورًا مختصرًا لأول Revenue Sprint يناسب شركتكم.",
      ].join("\n"),
    }),
  },
  {
    slug: "follow-up-recovery-os",
    nameAr: "نظام استرجاع المتابعات",
    nameEn: "Follow-up Recovery OS",
    dailyCount: 90,
    startingPrice: 3500,
    firstMission: "Follow-up Recovery Sprint (7 أيام)",
    proofAngle: "قبل/بعد follow-up queue + تقرير استرجاع أسبوعي",
    whyThisSystem:
      "أسرع قيمة تظهر في ترتيب من يحتاج متابعة الآن وتجهيز الرسائل المناسبة لكل حالة.",
    cta: "أرسل لك خريطة مختصرة لأول 7 أيام لتقليل ضياع المتابعة؟",
    /** @param {EmailContext} c */
    email: (c) => ({
      subject: "آخر متابعة لم تحدث قد تكون أغلى فرصة",
      body: [
        "السلام عليكم [الاسم/الفريق]،",
        "",
        `لاحظت أن ${c.company} تعمل في قطاع ${c.sector}، وهذا النوع من الشركات غالبًا عنده استفسارات وفرص تأتي من أكثر من قناة مثل ${c.signal}.`,
        "",
        "الفرص لا تضيع دائمًا بسبب ضعف العرض. أحيانًا تضيع لأن: لا أحد يعرف من يحتاج متابعة، الرسالة التالية غير جاهزة، المتابعة تتأخر، أو العميل المهتم لا ينتقل للخطوة التالية.",
        "",
        "نبني نظام استرجاع المتابعات خلال Sprint قصير: نرتب من يحتاج متابعة، نجهز الرسائل، ونبني queue واضحًا للفريق.",
        "",
        "إذا مناسب، أرسل لك خريطة مختصرة لأول 7 أيام لتقليل ضياع المتابعة.",
      ].join("\n"),
    }),
  },
  {
    slug: "executive-command-os",
    nameAr: "لوحة القرار التنفيذي",
    nameEn: "Executive Command OS",
    dailyCount: 70,
    startingPrice: 5500,
    firstMission: "Executive Command Sprint (7–14 يوم)",
    proofAngle: "نموذج Daily Command Report مخصص + خريطة مؤشرات",
    whyThisSystem:
      "أسرع قيمة تظهر في تحويل كثرة التقارير إلى قرار واحد واضح كل يوم.",
    cta: "أرسل لك نموذج Daily Command مخصصًا لطبيعة شركتكم؟",
    /** @param {EmailContext} c */
    email: (c) => ({
      subject: "تقرير يومي يوضح أهم قرار في الشركة",
      body: [
        "السلام عليكم [الاسم/الفريق]،",
        "",
        `في الشركات التي تتحرك بسرعة مثل ${c.company}، غالبًا لا تكون المشكلة نقص التقارير، بل كثرتها بدون قرار واضح.`,
        "",
        "الأسئلة اليومية الأهم عادة: ما أهم فرصة اليوم؟ أين التعطيل؟ من يحتاج متابعة؟ أي عرض متأخر؟ وأي قرار يجب أن يتخذه المدير الآن؟",
        "",
        "نبني لوحة القرار التنفيذي: لوحة مختصرة تربط الإيرادات، المتابعة، العروض، التسليم، والمخاطر في تقرير واحد قابل للتنفيذ.",
        "",
        `إذا مناسب، أرسل لك نموذج Daily Command مخصصًا لطبيعة عمل ${c.company} في ${c.city}.`,
      ].join("\n"),
    }),
  },
  {
    slug: "whatsapp-client-os",
    nameAr: "نظام تشغيل العملاء على واتساب",
    nameEn: "WhatsApp Client OS",
    dailyCount: 70,
    startingPrice: 4500,
    firstMission: "WhatsApp Flow Sprint (7–10 أيام)",
    proofAngle: "نموذج WhatsApp Flow + Action Cards للعميل",
    whyThisSystem:
      "أسرع قيمة تظهر في تحويل محادثات واتساب المتفرقة إلى مسارات وبطاقات إجراء.",
    cta: "أرسل لك نموذج flow بسيط يناسب طريقة تواصل عملائكم؟",
    /** @param {EmailContext} c */
    email: (c) => ({
      subject: "تحويل واتساب من محادثات إلى نظام",
      body: [
        "السلام عليكم [الاسم/الفريق]،",
        "",
        `إذا كان واتساب قناة مهمة عند ${c.company} في ${c.city}، فالتحدي غالبًا ليس الرد فقط.`,
        "",
        "التحدي هو تنظيم المحادثة: ما نوع الطلب؟ ما الخطوة التالية؟ متى نصعّد للإنسان؟ متى نرسل رابطًا آمنًا؟ ومتى يتحول العميل إلى عرض أو موعد؟",
        "",
        "نبني نظام تشغيل العملاء على واتساب: مسارات واضحة، بطاقات إجراء، فحص جاهزية، وتصعيد عند الحاجة — دون طلب مفاتيح أو بيانات حساسة داخل واتساب.",
        "",
        "إذا مناسب، أرسل لك نموذج flow بسيطًا يناسب طريقة تواصل عملائكم.",
      ].join("\n"),
    }),
  },
  {
    slug: "proposal-proof-os",
    nameAr: "نظام العروض والإثبات",
    nameEn: "Proposal & Proof OS",
    dailyCount: 70,
    startingPrice: 3000,
    firstMission: "Proposal & Proof Sprint (5–7 أيام)",
    proofAngle: "نموذج Proposal + Proof Pack لأول خدمة مستهدفة",
    whyThisSystem:
      "أسرع قيمة تظهر في تحويل العروض الضعيفة إلى عرض واضح مدعوم بدليل.",
    cta: "أرسل لك نموذج Proposal/Proof مبسطًا يناسب خدماتكم؟",
    /** @param {EmailContext} c */
    email: (c) => ({
      subject: "العرض المقنع يحتاج دليلًا وليس كلامًا أكثر",
      body: [
        "السلام عليكم [الاسم/الفريق]،",
        "",
        `في شركات الخدمات مثل ${c.company}، كثير من العروض لا تفشل لأن الخدمة ضعيفة، بل لأن العرض لا يوضح بما يكفي:`,
        "ما المشكلة؟ ما النطاق؟ ما الدليل؟ ما المخاطر؟ وما الخطوة التالية؟",
        "",
        "نبني نظام العروض والإثبات: نموذج عرض واضح + proof pack يربط المشكلة بالحل والمخرجات ومؤشر النجاح.",
        "",
        `إذا مناسب، أرسل لك نموذج Proposal/Proof مبسطًا يناسب ${c.company} وطبيعة خدماتها في ${c.sector}.`,
      ].join("\n"),
    }),
  },
];

export const DAILY_TOTAL = SYSTEMS.reduce((sum, s) => sum + s.dailyCount, 0);

export function getSystemBySlug(slug) {
  return SYSTEMS.find((s) => s.slug === slug);
}
