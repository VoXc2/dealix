// Synthetic seed universe for the Daily 400 Draft Factory.
//
// SAFETY / HONESTY NOTE:
// Every company produced here is SYNTHETIC and clearly labelled
// (source: "synthetic-seed", synthetic: true, placeholder website domain).
// It exists only to demonstrate and test the draft pipeline end-to-end.
// Before ANY real outreach, replace this universe with a real, verified list
// of companies that have agreed to be contacted. No purchased lists.

const CITIES = [
  "الرياض",
  "جدة",
  "الدمام",
  "الخبر",
  "مكة المكرمة",
  "المدينة المنورة",
  "أبها",
  "تبوك",
  "بريدة",
  "حائل",
  "الجبيل",
  "ينبع",
  "الطائف",
  "نجران",
];

// Arabic brand-name building blocks (generic, non-real).
const NAME_PREFIX = [
  "النخبة",
  "الرواد",
  "المسار",
  "الأفق",
  "الإتقان",
  "الريادة",
  "التميز",
  "الواحة",
  "المنارة",
  "الإبداع",
  "الذروة",
  "الركيزة",
  "الصدارة",
  "المرتكز",
  "البيان",
  "الموثوق",
];

const NAME_SUFFIX = [
  "",
  "القابضة",
  "السعودية",
  "للأعمال",
  "المتقدمة",
  "الحديثة",
  "الذكية",
];

/**
 * Each sector defines its Arabic/English label, typical signals & pains,
 * baseline ability-to-pay, compliance sensitivity, and an affinity weight
 * toward each of the five systems (used for fit-aware assignment).
 */
const SECTORS = [
  {
    ar: "وكالة تسويق",
    en: "Marketing Agency",
    word: "للتسويق",
    abilityToPay: 0.7,
    riskSensitive: false,
    signals: [
      "حملات إعلانية نشطة وصفحات تواصل متعددة",
      "نموذج تواصل على الموقع + واتساب ظاهر",
      "محفظة أعمال كبيرة بدون دليل نتائج واضح",
    ],
    pains: [
      "leads من الإعلانات لا تُتابع بنفس الجودة",
      "لا يوجد دليل ROI واضح للعملاء",
      "بطء في تجهيز العروض للعملاء المحتملين",
    ],
    affinity: {
      "revenue-operating-system": 0.34,
      "follow-up-recovery-os": 0.26,
      "proposal-proof-os": 0.24,
      "executive-command-os": 0.08,
      "whatsapp-client-os": 0.08,
    },
  },
  {
    ar: "شركة تدريب",
    en: "Training Company",
    word: "للتدريب",
    abilityToPay: 0.55,
    riskSensitive: false,
    signals: [
      "برامج متعددة + واتساب ظاهر للتواصل",
      "تقويم دورات نشط واستفسارات تسجيل",
      "صفحات هبوط لكل برنامج",
    ],
    pains: [
      "استفسارات التسجيل قد تضيع أو لا تُتابع",
      "فجوة بين الاستفسار والتسجيل الفعلي",
      "ضغط موسمي على المتابعة",
    ],
    affinity: {
      "follow-up-recovery-os": 0.36,
      "whatsapp-client-os": 0.3,
      "revenue-operating-system": 0.2,
      "proposal-proof-os": 0.08,
      "executive-command-os": 0.06,
    },
  },
  {
    ar: "خدمات B2B",
    en: "B2B Services",
    word: "للخدمات",
    abilityToPay: 0.65,
    riskSensitive: false,
    signals: [
      "عملاء مؤسسات وعقود متوسطة المدى",
      "فريق مبيعات صغير يعتمد على المتابعة اليدوية",
      "خط أنابيب فرص بدون مراحل واضحة",
    ],
    pains: [
      "بطء في إغلاق الصفقات",
      "فرص عالقة في مرحلة العرض",
      "لا يوجد next action واضح لكل فرصة",
    ],
    affinity: {
      "revenue-operating-system": 0.34,
      "proposal-proof-os": 0.26,
      "executive-command-os": 0.2,
      "follow-up-recovery-os": 0.16,
      "whatsapp-client-os": 0.04,
    },
  },
  {
    ar: "حلول تقنية",
    en: "IT Solutions",
    word: "للحلول التقنية",
    abilityToPay: 0.75,
    riskSensitive: false,
    signals: [
      "مشاريع تقنية متعددة بالتوازي",
      "فريق يوزّع وقته بين البيع والتسليم",
      "تقارير متفرقة بين أكثر من أداة",
    ],
    pains: [
      "الإدارة لا ترى صورة القرار اليومي",
      "ضعف استخدام CRM",
      "تأخر القرارات بين المبيعات والتسليم",
    ],
    affinity: {
      "executive-command-os": 0.34,
      "revenue-operating-system": 0.28,
      "proposal-proof-os": 0.2,
      "follow-up-recovery-os": 0.12,
      "whatsapp-client-os": 0.06,
    },
  },
  {
    ar: "خدمات قانونية",
    en: "Legal Services",
    word: "للمحاماة",
    abilityToPay: 0.7,
    riskSensitive: true,
    signals: [
      "استشارات وعقود متعددة العملاء",
      "عروض خدمات تُرسل يدويًا",
      "موقع رسمي بنماذج تواصل",
    ],
    pains: [
      "العروض غير مُتتبَّعة",
      "بطء في تجهيز عروض الخدمات",
      "لا يوجد دليل واضح يقلل تردد العميل",
    ],
    affinity: {
      "proposal-proof-os": 0.4,
      "executive-command-os": 0.22,
      "follow-up-recovery-os": 0.2,
      "revenue-operating-system": 0.12,
      "whatsapp-client-os": 0.06,
    },
  },
  {
    ar: "عقارات",
    en: "Real Estate",
    word: "العقارية",
    abilityToPay: 0.6,
    riskSensitive: false,
    signals: [
      "استفسارات كثيرة على واتساب",
      "حملات مشاريع وإعلانات وحدات",
      "فريق مبيعات ميداني",
    ],
    pains: [
      "استفسارات واتساب تضيع بلا متابعة",
      "بطء الرد يفقد المهتمين",
      "لا يوجد ترتيب لأولوية العملاء",
    ],
    affinity: {
      "whatsapp-client-os": 0.34,
      "follow-up-recovery-os": 0.3,
      "revenue-operating-system": 0.22,
      "proposal-proof-os": 0.08,
      "executive-command-os": 0.06,
    },
  },
  {
    ar: "لوجستيات",
    en: "Logistics",
    word: "للخدمات اللوجستية",
    abilityToPay: 0.68,
    riskSensitive: false,
    signals: [
      "عملاء شركات وعقود تشغيل",
      "عمليات يومية كثيفة",
      "تقارير تشغيل متفرقة",
    ],
    pains: [
      "الإدارة لا ترى القرار اليومي",
      "تعطّل بين المبيعات والتشغيل",
      "تأخر اتخاذ القرار",
    ],
    affinity: {
      "executive-command-os": 0.36,
      "revenue-operating-system": 0.26,
      "proposal-proof-os": 0.16,
      "follow-up-recovery-os": 0.16,
      "whatsapp-client-os": 0.06,
    },
  },
  {
    ar: "عيادات",
    en: "Clinics",
    word: "الطبية",
    abilityToPay: 0.6,
    riskSensitive: true,
    signals: [
      "حجوزات واستفسارات على واتساب",
      "حملات عروض موسمية",
      "استقبال يتعامل مع رسائل كثيرة",
    ],
    pains: [
      "حجوزات تضيع داخل محادثات واتساب",
      "متابعة المراجعين غير منتظمة",
      "ضغط على الاستقبال",
    ],
    affinity: {
      "whatsapp-client-os": 0.36,
      "follow-up-recovery-os": 0.3,
      "revenue-operating-system": 0.16,
      "executive-command-os": 0.1,
      "proposal-proof-os": 0.08,
    },
  },
  {
    ar: "استشارات إدارية",
    en: "Management Consulting",
    word: "للاستشارات",
    abilityToPay: 0.78,
    riskSensitive: false,
    signals: [
      "مشاريع استشارية متعددة",
      "عروض مفصلة لكل عميل",
      "فريق صغير عالي القيمة",
    ],
    pains: [
      "العروض بطيئة التجهيز",
      "ضعف توضيح الدليل والنطاق",
      "صعوبة رؤية أولويات القرار",
    ],
    affinity: {
      "proposal-proof-os": 0.36,
      "executive-command-os": 0.28,
      "revenue-operating-system": 0.18,
      "follow-up-recovery-os": 0.12,
      "whatsapp-client-os": 0.06,
    },
  },
  {
    ar: "تجارة إلكترونية",
    en: "E-commerce",
    word: "للتجارة الإلكترونية",
    abilityToPay: 0.6,
    riskSensitive: false,
    signals: [
      "متجر نشط واستفسارات واتساب",
      "حملات تخفيضات متكررة",
      "خدمة عملاء عبر القنوات",
    ],
    pains: [
      "استفسارات الطلبات تضيع في المحادثات",
      "لا يوجد نظام متابعة للسلات المتروكة",
      "ضعف ربط القنوات بالطلب",
    ],
    affinity: {
      "whatsapp-client-os": 0.32,
      "revenue-operating-system": 0.28,
      "follow-up-recovery-os": 0.26,
      "executive-command-os": 0.08,
      "proposal-proof-os": 0.06,
    },
  },
  {
    ar: "مقاولات",
    en: "Contracting",
    word: "للمقاولات",
    abilityToPay: 0.72,
    riskSensitive: false,
    signals: [
      "مشاريع وعطاءات متعددة",
      "عروض أسعار مفصلة",
      "إدارة تتابع أكثر من موقع",
    ],
    pains: [
      "عروض الأسعار بطيئة وغير موحدة",
      "الإدارة لا ترى أولويات القرار",
      "ضعف توثيق النطاق والمخاطر",
    ],
    affinity: {
      "proposal-proof-os": 0.32,
      "executive-command-os": 0.3,
      "revenue-operating-system": 0.2,
      "follow-up-recovery-os": 0.12,
      "whatsapp-client-os": 0.06,
    },
  },
  {
    ar: "خدمات مالية",
    en: "Financial Services",
    word: "المالية",
    abilityToPay: 0.8,
    riskSensitive: true,
    signals: [
      "عملاء مؤسسات وأفراد",
      "عروض خدمات منظمة",
      "حاجة لرؤية تنفيذية واضحة",
    ],
    pains: [
      "كثرة التقارير دون قرار واضح",
      "بطء في العروض",
      "صعوبة ترتيب المخاطر والأولويات",
    ],
    affinity: {
      "executive-command-os": 0.34,
      "proposal-proof-os": 0.28,
      "revenue-operating-system": 0.2,
      "follow-up-recovery-os": 0.12,
      "whatsapp-client-os": 0.06,
    },
  },
  {
    ar: "توظيف وموارد بشرية",
    en: "HR & Recruitment",
    word: "للتوظيف",
    abilityToPay: 0.58,
    riskSensitive: false,
    signals: [
      "طلبات توظيف واستفسارات شركات",
      "تواصل مستمر مع المرشحين والعملاء",
      "قاعدة بيانات متجددة",
    ],
    pains: [
      "متابعة العملاء والمرشحين تتأخر",
      "فرص توظيف تضيع بلا متابعة",
      "لا يوجد إيقاع متابعة واضح",
    ],
    affinity: {
      "follow-up-recovery-os": 0.34,
      "revenue-operating-system": 0.28,
      "whatsapp-client-os": 0.18,
      "proposal-proof-os": 0.12,
      "executive-command-os": 0.08,
    },
  },
  {
    ar: "تنظيم فعاليات",
    en: "Events",
    word: "للفعاليات",
    abilityToPay: 0.6,
    riskSensitive: false,
    signals: [
      "استفسارات فعاليات موسمية",
      "تواصل عبر واتساب والبريد",
      "عروض مخصصة لكل مناسبة",
    ],
    pains: [
      "استفسارات الفعاليات تضيع قبل العرض",
      "متابعة غير منتظمة",
      "بطء تجهيز العروض",
    ],
    affinity: {
      "follow-up-recovery-os": 0.32,
      "whatsapp-client-os": 0.28,
      "proposal-proof-os": 0.22,
      "revenue-operating-system": 0.12,
      "executive-command-os": 0.06,
    },
  },
  {
    ar: "تصميم داخلي",
    en: "Interior Design",
    word: "للتصميم الداخلي",
    abilityToPay: 0.62,
    riskSensitive: false,
    signals: [
      "محفظة أعمال بصرية قوية",
      "استفسارات عبر واتساب وإنستغرام",
      "عروض مشاريع مخصصة",
    ],
    pains: [
      "العروض بطيئة وغير موحدة",
      "استفسارات تضيع في المحادثات",
      "ضعف توضيح النطاق والمراحل",
    ],
    affinity: {
      "proposal-proof-os": 0.32,
      "whatsapp-client-os": 0.3,
      "follow-up-recovery-os": 0.2,
      "revenue-operating-system": 0.12,
      "executive-command-os": 0.06,
    },
  },
  {
    ar: "صناعة وتصنيع",
    en: "Manufacturing",
    word: "للصناعة",
    abilityToPay: 0.74,
    riskSensitive: false,
    signals: [
      "عملاء جملة وعقود توريد",
      "دورة بيع أطول",
      "تقارير إنتاج ومبيعات متفرقة",
    ],
    pains: [
      "الإدارة لا ترى القرار اليومي",
      "فرص توريد تضيع بلا متابعة",
      "تعطّل بين المبيعات والتشغيل",
    ],
    affinity: {
      "executive-command-os": 0.32,
      "revenue-operating-system": 0.3,
      "proposal-proof-os": 0.18,
      "follow-up-recovery-os": 0.14,
      "whatsapp-client-os": 0.06,
    },
  },
];

function pick(rng, arr) {
  return arr[Math.floor(rng() * arr.length)];
}

function clamp01(x) {
  return Math.max(0, Math.min(1, x));
}

/**
 * Build a synthetic universe of `size` companies.
 * @param {() => number} rng seeded RNG returning [0,1)
 * @param {number} size
 */
export function buildUniverse(rng, size) {
  const companies = [];
  for (let i = 0; i < size; i++) {
    const sector = pick(rng, SECTORS);
    const city = pick(rng, CITIES);
    const prefix = pick(rng, NAME_PREFIX);
    const suffix = pick(rng, NAME_SUFFIX);
    const company = `شركة ${prefix} ${sector.word} ${suffix}`.replace(/\s+/g, " ").trim();
    const signal = pick(rng, sector.signals);
    const likelyPain = pick(rng, sector.pains);
    const abilityToPay = clamp01(sector.abilityToPay + (rng() - 0.5) * 0.2);

    companies.push({
      id: `SYN-${String(i + 1).padStart(4, "0")}`,
      company,
      website: `https://sample.example/${String(i + 1).padStart(4, "0")}`,
      country: "السعودية",
      city,
      sector: sector.ar,
      sectorEn: sector.en,
      signal,
      likely_pain: likelyPain,
      abilityToPay,
      riskSensitive: sector.riskSensitive,
      affinity: sector.affinity,
      synthetic: true,
      source: "synthetic-seed",
    });
  }
  return companies;
}

export { CITIES, SECTORS };
