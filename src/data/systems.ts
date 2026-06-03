// Dealix — Focus 5 Business Operating Systems
// Single source of truth for the market-entry layer (frontend + tests).
//
// This module is intentionally free of React / icon imports so it can be
// consumed by Node-environment unit tests as plain data.
//
// Customer-facing copy rules enforced here (see tests/content-guard.test.ts):
//   - No guaranteed-result claims (نضمن / مضمون / ضمان / guarantee / 100%).
//   - No internal module / agent identifiers leaked to customer copy.

export type SystemSlug =
  | "revenue-operating-system"
  | "executive-command-os"
  | "follow-up-recovery-os"
  | "whatsapp-client-os"
  | "proposal-proof-os";

export type SystemIconName =
  | "TrendingUp"
  | "Gauge"
  | "RefreshCw"
  | "MessageCircle"
  | "FileCheck";

export type SystemAccent = {
  iconBg: string;
  iconText: string;
  badge: string;
  gradient: string;
  ring: string;
  border: string;
};

export type SystemFaq = {
  q: string;
  a: string;
};

export type SystemEmail = {
  subject: string;
  body: string;
};

export type BusinessSystem = {
  /** Stable URL slug. */
  slug: SystemSlug;
  /** Public English name (customer-facing). */
  name: string;
  /** Public Arabic name (customer-facing). */
  nameAr: string;
  /** One-line hook. */
  tagline: string;
  /** lucide-react icon name, resolved in the UI layer. */
  iconName: SystemIconName;
  /** Tailwind accent classes (literal strings so they survive purge). */
  accent: SystemAccent;
  /** Pain statement / who-it-is-for description. */
  pain: string;
  /** Short "best if you have…" line for the comparison table. */
  bestIf: string;
  /** Short "first tangible result" line for the comparison table. */
  firstResult: string;
  /** Audiences this system is sold to. */
  whoFor: string[];
  /** Concrete benefits. */
  benefits: string[];
  /** Human-readable sprint duration, e.g. "7–10 أيام". */
  sprintDuration: string;
  /** What the company gets in the first sprint. */
  sevenDayOutcome: string;
  /** Tangible delivery artifacts. */
  deliveryPack: string[];
  /** Opening "starts at" price, in SAR. */
  startingPrice: number;
  /** Short "what the starter sprint includes" line for the pricing table. */
  priceIncludes: string;
  /** Call to action label. */
  cta: string;
  /** Daily personalized draft allocation for this system. */
  dailyDrafts: number;
  /** Reference cold-email angle (outreach library). */
  email: SystemEmail;
  /** Page FAQ — never contains guaranteed claims. */
  faq: SystemFaq[];
};

/** Opening sprint pricing copy shown under every price. */
export const PRICING_NOTE =
  "هذه أسعار Sprint افتتاحي. النطاق النهائي يعتمد على حجم البيانات، عدد القنوات، التكاملات، وعدد الـ workflows المطلوبة.";

/** Shown wherever pricing finality might be implied. */
export const PRICING_DISCLAIMER =
  "الأسعار النهائية والمشاريع الكاملة والتشغيل الشهري تُسعّر بعد التشخيص وباعتماد المؤسس.";

const REVENUE: BusinessSystem = {
  slug: "revenue-operating-system",
  name: "Revenue Operating System",
  nameAr: "نظام تشغيل الإيرادات",
  tagline: "لا تدع الفرصة تضيع قبل أن تتحول إلى عرض أو اجتماع.",
  iconName: "TrendingUp",
  accent: {
    iconBg: "bg-emerald-100",
    iconText: "text-emerald-600",
    badge: "bg-emerald-100 text-emerald-800",
    gradient: "from-emerald-500 to-teal-600",
    ring: "ring-emerald-200",
    border: "border-emerald-300",
  },
  pain: "لشركات عندها فرص واستفسارات، لكن لا تعرف يوميًا من يحتاج متابعة، ما الخطوة التالية، وأين تضيع الفرصة قبل أن تتحول إلى اجتماع أو عرض.",
  bestIf: "فرص تضيع ولا يوجد نظام next action",
  firstResult: "خريطة تسرب + pipeline متابعة",
  whoFor: ["وكالات تسويق", "شركات تدريب", "شركات خدمات", "عقار", "توظيف"],
  benefits: [
    "كشف أماكن تسرب الفرص",
    "ترتيب leads حسب الأولوية",
    "تحديد next action لكل فرصة",
    "تجهيز drafts للمتابعة",
    "تقرير يومي للإدارة",
  ],
  sprintDuration: "7–10 أيام",
  sevenDayOutcome:
    "خلال 7–10 أيام: نحلل مسار الفرص، نبني أول revenue workflow، ونجهز تقريرًا يوضح أين تضيع الفرص وماذا تفعل بعدها.",
  deliveryPack: [
    "خريطة تسرب الإيرادات (Revenue leakage map)",
    "مراحل الفرص (Opportunity stages)",
    "Workflow متابعة",
    "قوالب مسودات (Draft templates)",
    "تقرير يومي/أسبوعي",
  ],
  startingPrice: 4500,
  priceIncludes: "leakage map + workflow متابعة",
  cta: "ابدأ بتشخيص الإيرادات",
  dailyDrafts: 100,
  email: {
    subject: "أين تضيع فرص الإيراد عندكم؟",
    body: [
      "السلام عليكم [الاسم/الفريق]،",
      "",
      "راجعت حضور [الشركة] في [القطاع/المدينة]، والظاهر أن عندكم أكثر من نقطة تواصل مع العملاء: [signal].",
      "",
      "في هذا النوع من الشركات، المشكلة غالبًا لا تكون في قلة الفرص، بل في أن كل فرصة لا يكون لها next action واضح:",
      "من يتابع؟ متى؟ وماذا يقال؟ ومتى تتحول الفرصة إلى عرض أو مكالمة؟",
      "",
      "Dealix يبني Revenue Operating System يبدأ بخريطة تسرب بسيطة، ثم يحولها إلى workflow متابعة وتقرير يومي للإدارة.",
      "الفكرة ليست أتمتة عشوائية، بل نظام يوضح: أين تضيع الفرصة، ما الأولوية، ماذا نرسل، وما القرار التالي.",
      "",
      "إذا مناسب، أرسل لك تصورًا مختصرًا لأول Revenue Sprint يناسب [الشركة].",
    ].join("\n"),
  },
  faq: [
    {
      q: "كم يستغرق أول Sprint؟",
      a: "من 7 إلى 10 أيام عمل، حسب حجم البيانات وعدد القنوات.",
    },
    {
      q: "ماذا نحتاج أن نجهّز قبل البداية؟",
      a: "مصدر بسيط للفرص (جدول، CRM، أو حتى رسائل)، ونبدأ ببيانات محدودة ومجهّلة قدر الإمكان.",
    },
    {
      q: "هل تتطلبون صلاحيات كاملة على أنظمتنا؟",
      a: "لا. نبدأ بأقل صلاحية ممكنة، والذكاء الاصطناعي يجهّز مسودات بينما الإنسان يعتمد كل خطوة.",
    },
    {
      q: "هل تَعِدون بأرقام محددة للإيراد؟",
      a: "لا نقدّم وعودًا برقم. نقدّم تشخيصًا واضحًا، نظامًا قابلًا للتنفيذ، وتقريرًا يوضح أين القيمة وما الخطوة التالية.",
    },
  ],
};

const EXECUTIVE: BusinessSystem = {
  slug: "executive-command-os",
  name: "Executive Command OS",
  nameAr: "لوحة القرار التنفيذي",
  tagline: "أهم قرار اليوم في شاشة واحدة، بدل عشرات التقارير.",
  iconName: "Gauge",
  accent: {
    iconBg: "bg-blue-100",
    iconText: "text-blue-600",
    badge: "bg-blue-100 text-blue-800",
    gradient: "from-blue-500 to-indigo-600",
    ring: "ring-blue-200",
    border: "border-blue-300",
  },
  pain: "للرؤساء والمؤسسين الذين لا يريدون تقارير كثيرة، بل يريدون معرفة أهم قرار اليوم: أين الفرصة؟ أين الخطر؟ من يحتاج متابعة؟ وما القرار التالي؟",
  bestIf: "قرارات يومية غير واضحة وبلا رؤية",
  firstResult: "لوحة قرار يومية",
  whoFor: ["مؤسس", "CEO", "GM", "مالك وكالة", "مالك عيادة", "شركات خدمات"],
  benefits: [
    "تقرير يومي مختصر للإدارة",
    "ربط المبيعات والمتابعة والعروض والتسليم",
    "كشف القرارات المتأخرة",
    "ترتيب المخاطر والأولويات",
    "تقليل اعتماد الشركة على المتابعة اليدوية",
  ],
  sprintDuration: "7–14 يوم",
  sevenDayOutcome:
    "خلال 7–14 يوم: نجهّز Daily Executive Command يوضح أهم المؤشرات والقرارات اليومية للإدارة.",
  deliveryPack: [
    "خريطة مؤشرات (KPI map)",
    "مواصفات لوحة القرار (Decision dashboard spec)",
    "تقرير القيادة اليومي (Daily command report)",
    "مصفوفة المخاطر/الأولويات",
    "سجل قرارات المؤسس (Founder action log)",
  ],
  startingPrice: 5500,
  priceIncludes: "dashboard / report spec + تقرير قيادة يومي",
  cta: "جهّز لوحة القرار",
  dailyDrafts: 70,
  email: {
    subject: "تقرير يومي يوضح أهم قرار في الشركة",
    body: [
      "السلام عليكم [الاسم/الفريق]،",
      "",
      "في الشركات التي تتحرك بسرعة، غالبًا لا تكون المشكلة نقص التقارير، بل كثرتها بدون قرار واضح.",
      "",
      "الأسئلة اليومية الأهم عادة: ما أهم فرصة اليوم؟ أين التعطيل؟ من يحتاج متابعة؟ أي عرض متأخر؟ وأي قرار يجب أن يتخذه المدير الآن؟",
      "",
      "Dealix يبني Executive Command OS: لوحة قرار مختصرة تربط الإيرادات، المتابعة، العروض، التسليم، والمخاطر في تقرير واحد قابل للتنفيذ.",
      "",
      "إذا مناسب، أرسل لك نموذج Daily Command مخصصًا لطبيعة [الشركة].",
    ].join("\n"),
  },
  faq: [
    {
      q: "هل هذا مجرد Dashboard آخر؟",
      a: "لا. المخرج قرار يومي مرتّب (فرصة/خطر/متابعة/قرار)، وليس مجرد رسوم بيانية.",
    },
    {
      q: "من أين تأتي البيانات؟",
      a: "من مصادرك الحالية (مبيعات، متابعة، عروض، تسليم) بأقل تكامل ممكن في البداية.",
    },
    {
      q: "هل يتخذ النظام قرارات بدل المدير؟",
      a: "لا. النظام يرتّب ويوضح، والقرار يبقى بيد الإنسان دائمًا.",
    },
    {
      q: "كم يستغرق التجهيز؟",
      a: "من 7 إلى 14 يومًا حسب عدد المصادر والمؤشرات المطلوبة.",
    },
  ],
};

const FOLLOWUP: BusinessSystem = {
  slug: "follow-up-recovery-os",
  name: "Follow-up Recovery OS",
  nameAr: "نظام استرجاع المتابعات",
  tagline: "آخر متابعة لم تحدث قد تكون أغلى فرصة.",
  iconName: "RefreshCw",
  accent: {
    iconBg: "bg-amber-100",
    iconText: "text-amber-600",
    badge: "bg-amber-100 text-amber-800",
    gradient: "from-amber-500 to-orange-600",
    ring: "ring-amber-200",
    border: "border-amber-300",
  },
  pain: "لشركات تخسر فرصًا لأن المتابعة لا تحدث في الوقت المناسب، أو لأن الفريق لا يعرف ماذا يرسل بعد أول تواصل.",
  bestIf: "متابعة ضعيفة تضيع بعد أول رسالة",
  firstResult: "follow-up queue + رسائل جاهزة",
  whoFor: ["شركات تدريب", "عقار", "عيادات", "وكالات", "استشارات"],
  benefits: [
    "قائمة واضحة لمن يحتاج متابعة",
    "رسائل جاهزة حسب حالة العميل",
    "إيقاع متابعة (follow-up rhythm) واضح",
    "منع ضياع العملاء المهتمين",
    "تقرير أسبوعي عن المتابعات",
  ],
  sprintDuration: "7 أيام",
  sevenDayOutcome:
    "خلال 7 أيام: نبني follow-up queue، ونجهّز أول حزمة رسائل متابعة قابلة للمراجعة والإرسال بعد الاعتماد.",
  deliveryPack: [
    "Follow-up queue",
    "نموذج حالة العميل (Customer status model)",
    "حزمة رسائل متابعة (Message set)",
    "إيقاع التذكير (Reminder rhythm)",
    "تقرير استرجاع أسبوعي",
  ],
  startingPrice: 3500,
  priceIncludes: "تحليل + queue + رسائل متابعة",
  cta: "استرجع المتابعات الضائعة",
  dailyDrafts: 90,
  email: {
    subject: "آخر متابعة لم تحدث قد تكون أغلى فرصة",
    body: [
      "السلام عليكم [الاسم/الفريق]،",
      "",
      "لاحظت أن [الشركة] تعمل في [القطاع]، وهذا النوع من الشركات غالبًا عنده استفسارات وفرص تأتي من أكثر من قناة.",
      "",
      "الفرص لا تضيع دائمًا بسبب ضعف العرض. أحيانًا تضيع لأن: لا أحد يعرف من يحتاج متابعة، الرسالة التالية غير جاهزة، المتابعة تتأخر، والعميل المهتم لا ينتقل للخطوة التالية.",
      "",
      "Dealix يبني Follow-up Recovery OS خلال Sprint قصير: نرتّب من يحتاج متابعة، نجهّز الرسائل، ونبني queue واضحًا للفريق.",
      "",
      "إذا مناسب، أرسل لك خريطة مختصرة لأول 7 أيام لتقليل ضياع المتابعة.",
    ].join("\n"),
  },
  faq: [
    {
      q: "ما الفرق بينه وبين Revenue OS؟",
      a: "هذا أسرع وأضيق: يركّز على ترتيب المتابعة والرسائل أولًا. Revenue OS أوسع ويغطي مسار الفرصة كاملًا.",
    },
    {
      q: "هل ترسلون الرسائل نيابة عنا؟",
      a: "نجهّز المسودات وقائمة المتابعة، والإرسال يبقى باعتماد بشري وعبر قنواتكم — لا إرسال تلقائي بدون موافقة.",
    },
    {
      q: "هل يصلح للعيادات والعقار؟",
      a: "نعم، صُمّم للقطاعات التي تستقبل استفسارات كثيرة وتحتاج متابعة منظمة.",
    },
  ],
};

const WHATSAPP: BusinessSystem = {
  slug: "whatsapp-client-os",
  name: "WhatsApp Client OS",
  nameAr: "نظام تشغيل العملاء على واتساب",
  tagline: "حوّل واتساب من رسائل متفرقة إلى نظام واضح.",
  iconName: "MessageCircle",
  accent: {
    iconBg: "bg-green-100",
    iconText: "text-green-600",
    badge: "bg-green-100 text-green-800",
    gradient: "from-green-500 to-emerald-600",
    ring: "ring-green-200",
    border: "border-green-300",
  },
  pain: "إذا كان واتساب قناة رئيسية للتواصل مع العملاء، فهذا النظام يحوّله من رسائل متفرقة إلى flows واضحة، action cards، تصعيد، وتقرير.",
  bestIf: "واتساب فوضوي بدون نظام",
  firstResult: "flows + action cards + handoff",
  whoFor: ["عيادات", "عقار", "تدريب", "خدمات محلية"],
  benefits: [
    "تنظيم محادثات العملاء",
    "Readiness Scan للعميل المهتم",
    "Action Cards للخيارات",
    "تصعيد للإنسان عند الحاجة",
    "ربط واتساب بالبوابة والتسليم",
  ],
  sprintDuration: "7–10 أيام",
  sevenDayOutcome:
    "خلال 7–10 أيام: نصمّم أول WhatsApp flow ونجهّز action cards للعميل، بدون طلب مفاتيح أو أسرار داخل واتساب.",
  deliveryPack: [
    "خريطة WhatsApp flow",
    "Readiness scan",
    "Action cards",
    "سياسة التصعيد للإنسان (Human handoff policy)",
    "دليل التحويل لبوابة آمنة (Secure portal handoff)",
  ],
  startingPrice: 4500,
  priceIncludes: "flow + action cards + handoff",
  cta: "حوّل واتساب إلى نظام",
  dailyDrafts: 70,
  email: {
    subject: "تحويل واتساب من محادثات إلى نظام",
    body: [
      "السلام عليكم [الاسم/الفريق]،",
      "",
      "إذا كان واتساب قناة مهمة عند [الشركة]، فالتحدي غالبًا ليس الرد فقط.",
      "",
      "التحدي هو تنظيم المحادثة: ما نوع الطلب؟ ما الخطوة التالية؟ متى نصعّد للإنسان؟ متى نرسل رابطًا آمنًا؟ ومتى يتحول العميل إلى عرض أو موعد؟",
      "",
      "Dealix يبني WhatsApp Client OS: flows واضحة، action cards، readiness scan، وتصعيد عند الحاجة — بدون طلب مفاتيح أو بيانات حساسة داخل واتساب.",
      "",
      "إذا مناسب، أرسل لك نموذج flow بسيط يناسب طريقة تواصل عملائكم.",
    ].join("\n"),
  },
  faq: [
    {
      q: "هل هذا واتساب بارد (cold) للعملاء الجدد؟",
      a: "لا. النظام يعمل بعد اهتمام العميل أو موافقته، عبر WhatsApp Business Platform كقناة خدمة عملاء — وليس رسائل بادئة غير مطلوبة.",
    },
    {
      q: "هل تطلبون مفاتيح حساباتنا أو رموز الدخول؟",
      a: "لا. لا نطلب مفاتيح أو أسرارًا أو بيانات حساسة داخل واتساب؛ التحويلات الحساسة تتم عبر بوابة آمنة.",
    },
    {
      q: "هل يرد النظام تلقائيًا على كل شيء؟",
      a: "لا. يرتّب المحادثة ويقترح، ويصعّد للإنسان عند الحاجة. القرار النهائي بشري.",
    },
  ],
};

const PROPOSAL: BusinessSystem = {
  slug: "proposal-proof-os",
  name: "Proposal & Proof OS",
  nameAr: "نظام العروض والإثبات",
  tagline: "العرض المقنع يحتاج Proof، وليس كلامًا أكثر.",
  iconName: "FileCheck",
  accent: {
    iconBg: "bg-violet-100",
    iconText: "text-violet-600",
    badge: "bg-violet-100 text-violet-800",
    gradient: "from-violet-500 to-purple-600",
    ring: "ring-violet-200",
    border: "border-violet-300",
  },
  pain: "لشركات الخدمات التي تتأخر في تجهيز العروض، أو ترسل عروضًا لا توضح المشكلة، النطاق، الدليل، والخطوة التالية.",
  bestIf: "عروض غير مقنعة أو بطيئة أو بلا دليل",
  firstResult: "proposal + proof pack",
  whoFor: ["استشارات", "وكالات", "B2B services"],
  benefits: [
    "Proposal واضح ومقنع",
    "Proof Pack يشرح المشكلة والدليل",
    "Scope و Out-of-scope",
    "Next step واضح",
    "تقليل تردد العميل",
  ],
  sprintDuration: "5–7 أيام",
  sevenDayOutcome:
    "خلال 5–7 أيام: نجهّز نموذج عرض وProof Pack لأول خدمة أو عميل مستهدف.",
  deliveryPack: [
    "نموذج Proposal",
    "نموذج Proof Pack",
    "Scope / Out-of-scope",
    "افتراضات المخاطر (Risk assumptions)",
    "بطاقة الخطوة التالية (Next-step card)",
  ],
  startingPrice: 3000,
  priceIncludes: "proposal + proof pack",
  cta: "جهّز عرضًا مقنعًا",
  dailyDrafts: 70,
  email: {
    subject: "العرض المقنع يحتاج Proof وليس كلامًا أكثر",
    body: [
      "السلام عليكم [الاسم/الفريق]،",
      "",
      "في شركات الخدمات، كثير من العروض لا تفشل لأن الخدمة ضعيفة، بل لأن العرض لا يوضح بما يكفي:",
      "ما المشكلة؟ ما النطاق؟ ما الدليل؟ ما المخاطر؟ وما الخطوة التالية؟",
      "",
      "Dealix يبني Proposal & Proof OS: نموذج عرض واضح + proof pack يربط المشكلة بالحل والمخرجات ومؤشر النجاح.",
      "",
      "إذا مناسب، أرسل لك نموذج Proposal/Proof مبسطًا يناسب [الشركة] وطبيعة خدماتها.",
    ].join("\n"),
  },
  faq: [
    {
      q: "هل تكتبون العرض بالكامل عنا؟",
      a: "نجهّز النموذج والـ Proof Pack وهيكل المحتوى، وأنتم تعتمدون وتخصّصون قبل الإرسال.",
    },
    {
      q: "ما المقصود بـ Proof Pack؟",
      a: "حزمة تربط مشكلة العميل بالدليل والمخرجات ومؤشر نجاح واضح، لتقليل التردد.",
    },
    {
      q: "هل يصلح لخدمات متعددة؟",
      a: "نبدأ بخدمة أو عميل مستهدف واحد كنموذج، ثم يسهل تعميمه على بقية خدماتكم.",
    },
  ],
};

/** The five market-entry systems, in display order. */
export const SYSTEMS: BusinessSystem[] = [
  REVENUE,
  EXECUTIVE,
  FOLLOWUP,
  WHATSAPP,
  PROPOSAL,
];

/** Lookup map by slug. */
export const SYSTEM_BY_SLUG: Record<SystemSlug, BusinessSystem> = SYSTEMS.reduce(
  (acc, system) => {
    acc[system.slug] = system;
    return acc;
  },
  {} as Record<SystemSlug, BusinessSystem>,
);

/** Resolve a system by an unknown slug string. */
export function getSystem(slug: string | undefined): BusinessSystem | undefined {
  if (!slug) return undefined;
  return SYSTEM_BY_SLUG[slug as SystemSlug];
}

/** Format a SAR amount with thousands separators, e.g. 4500 -> "4,500 ر.س". */
export function formatSar(amount: number): string {
  return `${amount.toLocaleString("en-US")} ر.س`;
}

/** Format a "starts at" price label, e.g. "يبدأ من 4,500 ر.س". */
export function startingPriceLabel(system: BusinessSystem): string {
  return `يبدأ من ${formatSar(system.startingPrice)}`;
}
