import type { LucideIcon } from "lucide-react";
import {
  TrendingUp,
  LayoutDashboard,
  RefreshCw,
  MessageCircle,
  FileText,
} from "lucide-react";

export type SystemSlug =
  | "revenue-operating-system"
  | "executive-command-os"
  | "follow-up-recovery-os"
  | "whatsapp-client-os"
  | "proposal-proof-os";

export interface SystemFAQ {
  q: string;
  a: string;
}

export interface BusinessSystem {
  slug: SystemSlug;
  /** English product name shown as the primary brand label. */
  name: string;
  /** Arabic descriptive name. */
  nameAr: string;
  /** One-line positioning used on cards. */
  tagline: string;
  icon: LucideIcon;
  /** Tailwind accent token, e.g. "emerald". Used for gradients/badges. */
  accent: "emerald" | "blue" | "amber" | "violet" | "rose";
  /** Hero sub-headline describing who this is for and the core tension. */
  hero: string;
  /** Short pain statement used on cards and the systems table. */
  painShort: string;
  /** The first tangible result the client receives. */
  firstResult: string;
  /** Who the system is best for (bullet list). */
  whoFor: string[];
  /** Concrete client benefits. */
  benefits: string[];
  /** First sprint window + what happens in it. */
  firstSprint: {
    window: string;
    summary: string;
  };
  /** Tangible deliverables handed over. */
  deliveryPack: string[];
  /** Starting price in SAR (starter sprint only). */
  startingPrice: number;
  /** Human-readable sprint duration. */
  duration: string;
  /** Primary call-to-action label. */
  cta: string;
  /** Frequently asked questions. */
  faq: SystemFAQ[];
}

export const CURRENCY = "ريال";

export const systems: BusinessSystem[] = [
  {
    slug: "revenue-operating-system",
    name: "Revenue Operating System",
    nameAr: "نظام تشغيل الإيرادات",
    tagline: "حوِّل الفرص المتفرقة إلى متابعة وقرار يومي واضح.",
    icon: TrendingUp,
    accent: "emerald",
    hero: "للشركات التي عندها فرص واستفسارات، لكنها لا تعرف يوميًا من يحتاج متابعة، ما الخطوة التالية، وأين تضيع الفرصة قبل أن تتحول إلى اجتماع أو عرض.",
    painShort: "فرص تضيع ولا يوجد إجراء تالٍ واضح لكل فرصة.",
    firstResult: "خريطة تسرب الفرص + أول workflow متابعة.",
    whoFor: [
      "شركات عندها استفسارات من أكثر من قناة بدون ترتيب أولويات",
      "فرق مبيعات تعتمد على الذاكرة بدل نظام متابعة",
      "مؤسس يريد رؤية واضحة لمكان تعطل الإيراد",
    ],
    benefits: [
      "كشف أماكن تسرب الفرص قبل أن تضيع",
      "ترتيب العملاء المحتملين حسب الأولوية",
      "تحديد الخطوة التالية لكل فرصة",
      "تجهيز مسودات جاهزة للمتابعة",
      "تقرير يومي واضح للإدارة",
      "ربط الإيراد بالمتابعة لا بالتخمين",
    ],
    firstSprint: {
      window: "7–10 أيام",
      summary:
        "نحلل مسار الفرص، نبني خريطة تسرب الإيراد، ونجهز أول workflow متابعة مع تقرير إداري واضح.",
    },
    deliveryPack: [
      "خريطة تسرب الإيراد (Revenue Leakage Map)",
      "نموذج مراحل الفرصة (Opportunity Stage Model)",
      "Workflow متابعة قابل للتنفيذ",
      "قوالب مسودات متابعة",
      "تقرير إيرادات يومي/أسبوعي",
      "قائمة الإجراءات التالية للمؤسس",
    ],
    startingPrice: 4500,
    duration: "7–10 أيام",
    cta: "ابدأ بتشخيص الإيرادات",
    faq: [
      {
        q: "هل أحتاج CRM قبل أن نبدأ؟",
        a: "لا. نبدأ بالبيانات المتاحة لديك مهما كانت بسيطة، ونبني النظام فوقها. إذا كان عندك CRM نربط العمل به، وإن لم يوجد نجهز هيكلًا عمليًا أولًا.",
      },
      {
        q: "ما الفرق بين هذا والنظام التنفيذي؟",
        a: "نظام تشغيل الإيرادات يركز على مستوى الفرص والمتابعة اليومية للفريق. لوحة القرار التنفيذي ترفع الصورة للإدارة في تقرير قرار واحد.",
      },
      {
        q: "هل تضمنون زيادة الإيراد؟",
        a: "لا نقدم ضمانات إيراد. نقدم نظامًا يوضح أين تضيع الفرص وكيف تُتابع، والنتيجة تعتمد على تنفيذكم للمتابعة.",
      },
    ],
  },
  {
    slug: "executive-command-os",
    name: "Executive Command OS",
    nameAr: "لوحة القرار التنفيذي",
    tagline: "قرار واحد واضح كل يوم بدل عشرة تقارير بلا خلاصة.",
    icon: LayoutDashboard,
    accent: "blue",
    hero: "للرؤساء والمؤسسين والمدراء الذين لا يريدون تقارير كثيرة، بل يريدون معرفة أهم قرار اليوم: أين الفرصة؟ أين الخطر؟ من يحتاج متابعة؟ وما القرار التالي؟",
    painShort: "الإدارة لا ترى القرار اليومي وسط كثرة التقارير.",
    firstResult: "تقرير القرار اليومي (Daily Command Report).",
    whoFor: [
      "مؤسس أو رئيس تنفيذي يريد صورة قرار واحدة يوميًا",
      "إدارة تتلقى تقارير كثيرة بلا أولوية واضحة",
      "شركات تتحرك بسرعة وتحتاج كشف القرارات المتأخرة",
    ],
    benefits: [
      "تقرير يومي مختصر للإدارة",
      "ربط المبيعات والمتابعة والعروض والتسليم في صورة واحدة",
      "كشف القرارات المتأخرة قبل أن تكلف",
      "ترتيب المخاطر والأولويات",
      "تقليل الاعتماد على المتابعة اليدوية",
    ],
    firstSprint: {
      window: "7–14 يوم",
      summary:
        "نجهز لوحة القرار اليومي التي توضح أهم المؤشرات، المخاطر، والقرارات المطلوبة اليوم.",
    },
    deliveryPack: [
      "خريطة المؤشرات (KPI Map)",
      "تقرير القرار اليومي (Daily Command Report)",
      "مصفوفة المخاطر والأولويات",
      "سجل القرارات (Decision Log)",
      "لوحة إجراءات المؤسس/الرئيس التنفيذي",
      "قالب المراجعة التنفيذية الأسبوعية",
    ],
    startingPrice: 5500,
    duration: "7–14 يوم",
    cta: "جهّز لوحة القرار",
    faq: [
      {
        q: "من أين تأتي بيانات اللوحة؟",
        a: "نربط المصادر المتاحة لديك (مبيعات، متابعة، عروض، تسليم) ونلخصها في تقرير قرار واحد. لا نطلب أنظمة جديدة كشرط للبدء.",
      },
      {
        q: "هل هذه مجرد لوحة مؤشرات؟",
        a: "لا. الهدف ليس عرض أرقام، بل إبراز القرار المطلوب اليوم: أين الفرصة، أين الخطر، ومن يحتاج تدخلًا الآن.",
      },
      {
        q: "كم وقت يأخذ مني يوميًا؟",
        a: "اللوحة مصممة لتُقرأ في دقائق وتنتهي بقائمة قرارات قصيرة، لا بتقرير طويل.",
      },
    ],
  },
  {
    slug: "follow-up-recovery-os",
    name: "Follow-up Recovery OS",
    nameAr: "نظام استرجاع المتابعات",
    tagline: "آخر متابعة لم تحدث قد تكون أغلى فرصة لديك.",
    icon: RefreshCw,
    accent: "amber",
    hero: "لشركات تخسر فرصًا لأن المتابعة لا تحدث في الوقت المناسب، أو لأن الفريق لا يعرف ماذا يرسل بعد أول تواصل.",
    painShort: "المتابعة تضيع بعد أول تواصل مع العميل.",
    firstResult: "Follow-up Queue + أول حزمة رسائل متابعة.",
    whoFor: [
      "شركات تأتيها استفسارات من أكثر من قناة دون متابعة منظمة",
      "فرق تنسى توقيت المتابعة أو لا تعرف ماذا ترسل",
      "نشاط يفقد عملاء مهتمين قبل الوصول للعرض",
    ],
    benefits: [
      "معرفة من يحتاج متابعة الآن",
      "تجهيز رسائل حسب حالة العميل",
      "بناء إيقاع متابعة واضح (Follow-up rhythm)",
      "منع ضياع العملاء المهتمين",
      "تقرير أسبوعي عن المتابعات والفرص",
    ],
    firstSprint: {
      window: "7 أيام",
      summary:
        "نبني Follow-up Queue، ونجهز أول حزمة رسائل متابعة قابلة للمراجعة والإرسال بعد الموافقة.",
    },
    deliveryPack: [
      "قائمة المتابعة (Follow-up Queue)",
      "نموذج حالات العميل (Lead Status Model)",
      "حزمة رسائل المتابعة",
      "إيقاع التذكير (Reminder Rhythm)",
      "تقرير الاسترجاع (Recovery Report)",
      "قواعد التصعيد (Escalation Rules)",
    ],
    startingPrice: 3500,
    duration: "7 أيام",
    cta: "استرجع المتابعات الضائعة",
    faq: [
      {
        q: "هل ترسلون الرسائل نيابة عني؟",
        a: "نجهز الرسائل والقائمة، لكن الإرسال يبقى مسودة حتى تعتمدها أنت. لا إرسال تلقائي دون موافقة.",
      },
      {
        q: "ما أسرع نتيجة أراها؟",
        a: "خلال الأسبوع الأول تحصل على قائمة واضحة بمن يحتاج متابعة الآن، ورسائل جاهزة لكل حالة.",
      },
      {
        q: "هل يشمل واتساب؟",
        a: "هذا النظام يركز على إيقاع المتابعة. تنظيم محادثات واتساب نفسها يغطّيه نظام تشغيل العملاء على واتساب.",
      },
    ],
  },
  {
    slug: "whatsapp-client-os",
    name: "WhatsApp Client OS",
    nameAr: "نظام تشغيل العملاء على واتساب",
    tagline: "حوِّل واتساب من رسائل متفرقة إلى نظام واضح.",
    icon: MessageCircle,
    accent: "emerald",
    hero: "إذا كان واتساب قناة رئيسية للتواصل مع عملائك، فهذا النظام يحوّله من رسائل متفرقة إلى مسارات واضحة، بطاقات إجراء، تصعيد، وتقرير.",
    painShort: "واتساب ممتلئ برسائل بلا نظام أو خطوة تالية.",
    firstResult: "Flow Map + Action Cards للعميل.",
    whoFor: [
      "نشاط يعتمد على واتساب كقناة تواصل رئيسية",
      "فريق يفقد الطلبات داخل المحادثات",
      "شركة تريد تنظيم الرد والتصعيد دون بوت عام مفتوح",
    ],
    benefits: [
      "تنظيم محادثات العملاء",
      "فحص جاهزية العميل المهتم (Readiness Scan)",
      "بطاقات إجراء للخيارات (Action Cards)",
      "تصعيد للإنسان عند الحاجة",
      "ربط واتساب بالبوابة والتسليم بشكل آمن",
      "تقليل ضياع الطلبات داخل المحادثات",
    ],
    firstSprint: {
      window: "7–10 أيام",
      summary:
        "نصمم أول WhatsApp Flow ونجهز Action Cards للعميل، دون طلب مفاتيح أو بيانات حساسة داخل واتساب.",
    },
    deliveryPack: [
      "خريطة مسار واتساب (WhatsApp Flow Map)",
      "فحص الجاهزية (Readiness Scan)",
      "بطاقات الإجراء (Action Cards)",
      "سياسة التسليم للإنسان (Human Handoff Policy)",
      "دليل التحويل الآمن للبوابة (Secure Portal Handoff)",
      "المراجعة الأسبوعية لواتساب",
    ],
    startingPrice: 4500,
    duration: "7–10 أيام",
    cta: "حوّل واتساب إلى نظام",
    faq: [
      {
        q: "هل هذا بوت واتساب؟",
        a: "لا نبني بوتًا عامًا مفتوحًا. نبني مساعد سير عمل يعمل بعد اهتمام العميل، مع تصعيد واضح للإنسان عند الحاجة.",
      },
      {
        q: "هل تطلبون بيانات حساسة داخل واتساب؟",
        a: "لا. أي بيانات أو مدفوعات حساسة تُحوَّل عبر بوابة آمنة، وليس داخل المحادثة.",
      },
      {
        q: "هل يحتاج واتساب Business API؟",
        a: "نصمم المسار ليعمل مع وضعكم الحالي، ونوضح متى يفيد الانتقال إلى منصة واتساب للأعمال حسب الحجم.",
      },
    ],
  },
  {
    slug: "proposal-proof-os",
    name: "Proposal & Proof OS",
    nameAr: "نظام العروض والإثبات",
    tagline: "العرض المقنع يحتاج دليلًا، لا كلامًا أكثر.",
    icon: FileText,
    accent: "violet",
    hero: "لشركات الخدمات التي تتأخر في تجهيز العروض، أو ترسل عروضًا لا توضح المشكلة، النطاق، الدليل، والخطوة التالية.",
    painShort: "العروض ضعيفة أو بطيئة ولا توضح الدليل.",
    firstResult: "نموذج عرض + Proof Pack لأول خدمة.",
    whoFor: [
      "شركات خدمات تتأخر في تجهيز العروض",
      "فرق ترسل عروضًا لا توضح المشكلة والنطاق والدليل",
      "نشاط يفقد صفقات بسبب تردد العميل قبل القرار",
    ],
    benefits: [
      "عرض واضح ومقنع",
      "Proof Pack يشرح المشكلة والدليل",
      "تحديد النطاق وما هو خارج النطاق",
      "كتلة المخاطر والافتراضات",
      "بطاقة الخطوة التالية",
      "تقليل تردد العميل قبل القرار",
    ],
    firstSprint: {
      window: "5–7 أيام",
      summary:
        "نجهز نموذج عرض وProof Pack لأول خدمة أو عميل مستهدف، جاهزَين للاستخدام والتكرار.",
    },
    deliveryPack: [
      "قالب العرض (Proposal Template)",
      "قالب الإثبات (Proof Pack Template)",
      "النطاق وما هو خارج النطاق",
      "كتلة المخاطر والافتراضات",
      "بطاقة الخطوة التالية (Next-step Card)",
      "قائمة مراجعة العرض (Proposal Review Checklist)",
    ],
    startingPrice: 3000,
    duration: "5–7 أيام",
    cta: "جهّز عرضًا مقنعًا",
    faq: [
      {
        q: "هل تكتبون العروض بدلًا عني لكل عميل؟",
        a: "نبني نظامًا وقوالب تنتج عروضًا قوية بسرعة، ونجهز أول عرض كمثال عملي. بعدها تكررونه بسهولة.",
      },
      {
        q: "ما الفرق بين العرض والـ Proof Pack؟",
        a: "العرض يوضح المشكلة والنطاق والسعر والخطوة التالية. الـ Proof Pack يربط ذلك بدليل ومؤشر نجاح يقلل تردد العميل.",
      },
      {
        q: "هل يناسب الخدمات غير التقنية؟",
        a: "نعم. النظام مصمم لشركات الخدمات عمومًا، ونكيّف القوالب حسب طبيعة خدمتكم.",
      },
    ],
  },
];

export function getSystem(slug: string): BusinessSystem | undefined {
  return systems.find((s) => s.slug === slug);
}

/** Tailwind class fragments per accent, kept explicit so they survive purge. */
export const accentClasses: Record<
  BusinessSystem["accent"],
  {
    text: string;
    bgSoft: string;
    border: string;
    gradient: string;
    button: string;
    ring: string;
  }
> = {
  emerald: {
    text: "text-emerald-600",
    bgSoft: "bg-emerald-100",
    border: "border-emerald-500",
    gradient: "from-emerald-500 to-teal-600",
    button: "bg-emerald-600 hover:bg-emerald-700",
    ring: "ring-emerald-200",
  },
  blue: {
    text: "text-blue-600",
    bgSoft: "bg-blue-100",
    border: "border-blue-500",
    gradient: "from-blue-500 to-indigo-600",
    button: "bg-blue-600 hover:bg-blue-700",
    ring: "ring-blue-200",
  },
  amber: {
    text: "text-amber-600",
    bgSoft: "bg-amber-100",
    border: "border-amber-500",
    gradient: "from-amber-500 to-orange-600",
    button: "bg-amber-600 hover:bg-amber-700",
    ring: "ring-amber-200",
  },
  violet: {
    text: "text-violet-600",
    bgSoft: "bg-violet-100",
    border: "border-violet-500",
    gradient: "from-violet-500 to-purple-600",
    button: "bg-violet-600 hover:bg-violet-700",
    ring: "ring-violet-200",
  },
  rose: {
    text: "text-rose-600",
    bgSoft: "bg-rose-100",
    border: "border-rose-500",
    gradient: "from-rose-500 to-pink-600",
    button: "bg-rose-600 hover:bg-rose-700",
    ring: "ring-rose-200",
  },
};

export function formatPrice(value: number): string {
  return value.toLocaleString("en-US");
}
