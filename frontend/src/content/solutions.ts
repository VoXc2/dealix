export type SectorId =
  | "government_b2g"
  | "construction_epc"
  | "industrial_manufacturing"
  | "logistics_supply_chain"
  | "energy_utilities_oil_gas"
  | "mining_metals"
  | "real_estate_proptech"
  | "healthcare"
  | "finance_fintech_insurance"
  | "retail_commerce_ecommerce"
  | "tourism_hospitality"
  | "professional_services"
  | "technology_saas_si"
  | "telecom_media_marketing"
  | "education_training"
  | "agriculture_food_water"
  | "mobility_automotive"
  | "export_import_rhq"
  | "creative_sports_gaming"
  | "associations_nonprofits";

export interface SectorSolution {
  id: SectorId;
  nameAr: string;
  nameEn: string;
  icon: string;
  buyersAr: string[];
  buyersEn: string[];
  problemsAr: string[];
  problemsEn: string[];
  servicesAr: { title: string; desc: string; agents: string }[];
  servicesEn: { title: string; desc: string; agents: string }[];
}

export const SECTOR_SOLUTIONS: Record<SectorId, SectorSolution> = {
  government_b2g: {
    id: "government_b2g",
    nameAr: "الجهات الحكومية و B2G",
    nameEn: "Government & B2G",
    icon: "🏛️",
    buyersAr: ["مدير المشتريات", "مدير المشروع", "الأمن السيبراني"],
    buyersEn: ["Procurement Director", "Project Director", "CISO"],
    problemsAr: ["تأخر المناقصات", "عبء الامتثال", "تأخر الموافقات"],
    problemsEn: ["Procurement delays", "Compliance burden", "Approval delays"],
    servicesAr: [
      { title: "جاهزية B2G", desc: "تقييم مستندات وتصنيف وتأهيل", agents: "يديره dealix-pm + dealix-sales" },
      { title: "ذكاء المناقصات", desc: "مراقبة Etimad وتوصية bid/no-bid", agents: "يديره dealix-sales + dealix-engineer" },
      { title: "حوكمة AI", desc: "تحويل Tender إلى تسليم محكوم", agents: "يديره dealix-delivery" },
    ],
    servicesEn: [
      { title: "B2G Readiness", desc: "Documents, classification, qualification", agents: "Managed by dealix-pm + dealix-sales" },
      { title: "Tender Intelligence", desc: "Etimad monitoring + bid/no-bid", agents: "Managed by dealix-sales + dealix-engineer" },
      { title: "AI Governance", desc: "Tender to governed delivery", agents: "Managed by dealix-delivery" },
    ],
  },
  construction_epc: {
    id: "construction_epc",
    nameAr: "الإنشاءات و EPC",
    nameEn: "Construction & EPC",
    icon: "🏗️",
    buyersAr: ["مدير المشروع", "المالية", "المشتريات"],
    buyersEn: ["Project Director", "CFO", "Procurement"],
    problemsAr: ["تأخر المشاريع", "فوضى المستندات", "تسرّب تكلفة"],
    problemsEn: ["Project delays", "Document chaos", "Cost leakage"],
    servicesAr: [
      { title: "ضوابط المشروع", desc: "RFI، أوامر تغيير، مطالبات", agents: "dealix-delivery + dealix-engineer" },
      { title: "ذكاء المستندات", desc: "استخراج، موافقات، بحث", agents: "dealix-engineer" },
      { title: "المشروع إلى النقد", desc: "تحصيل وتحصيل متأخر", agents: "dealix-sales + dealix-content" },
    ],
    servicesEn: [
      { title: "Project Controls", desc: "RFI, variations, claims", agents: "dealix-delivery + dealix-engineer" },
      { title: "Document Intelligence", desc: "Extraction, approvals, search", agents: "dealix-engineer" },
      { title: "Project to Cash", desc: "Collections & delayed payments", agents: "dealix-sales + dealix-content" },
    ],
  },
  technology_saas_si: {
    id: "technology_saas_si",
    nameAr: "التقنية و SaaS",
    nameEn: "Technology & SaaS",
    icon: "💻",
    buyersAr: ["CTO", "CEO", "CISO"],
    buyersEn: ["CTO", "CEO", "CISO"],
    problemsAr: ["مخاطر حوكمة AI", "فشل تكامل", "تسرّب إيراد"],
    problemsEn: ["AI governance risk", "Integration failure", "Revenue leakage"],
    servicesAr: [
      { title: "حوكمة AI", desc: "جرد، مخاطر، رقابة بشرية", agents: "dealix-engineer + dealix-pm" },
      { title: "محرك الإيرادات", desc: "كشف تسرّب إيراد", agents: "dealix-sales" },
      { title: "AI خاص", desc: "نشر محلي آمن", agents: "dealix-engineer" },
    ],
    servicesEn: [
      { title: "AI Governance", desc: "Inventory, risk, human oversight", agents: "dealix-engineer + dealix-pm" },
      { title: "Revenue Engine", desc: "Leakage detection", agents: "dealix-sales" },
      { title: "Private AI", desc: "Secure on-prem deployment", agents: "dealix-engineer" },
    ],
  },
  finance_fintech_insurance: {
    id: "finance_fintech_insurance",
    nameAr: "المالية والتأمين",
    nameEn: "Finance & Insurance",
    icon: "🏦",
    buyersAr: ["CFO", "CISO", "الامتثال"],
    buyersEn: ["CFO", "CISO", "Compliance"],
    problemsAr: ["عبء الامتثال", "مخاطر سيبرانية", "تسرّب إيراد"],
    problemsEn: ["Compliance burden", "Cyber risk", "Revenue leakage"],
    servicesAr: [
      { title: "عمليات الفوترة", desc: "جاهزية ZATCA، تكامل ERP", agents: "dealix-engineer" },
      { title: "حوكمة AI", desc: "تقييم مخاطر", agents: "dealix-pm" },
      { title: "تحصيل", desc: "تأخر تحصيل", agents: "dealix-sales" },
    ],
    servicesEn: [
      { title: "Fatoora Ops", desc: "ZATCA readiness, ERP integration", agents: "dealix-engineer" },
      { title: "AI Governance", desc: "Risk assessment", agents: "dealix-pm" },
      { title: "Collections", desc: "Delayed collections", agents: "dealix-sales" },
    ],
  },
  healthcare: {
    id: "healthcare",
    nameAr: "الرعاية الصحية",
    nameEn: "Healthcare",
    icon: "🏥",
    buyersAr: ["CIO", "الامتثال", "العمليات"],
    buyersEn: ["CIO", "Compliance", "Operations"],
    problemsAr: ["عبء امتثال", "تشتت بيانات", "تراكم دعم"],
    problemsEn: ["Compliance", "Data fragmentation", "Support backlog"],
    servicesAr: [
      { title: "تشخيص البيانات", desc: "جودة، حداثة، حوكمة", agents: "dealix-engineer" },
      { title: "أتمتة الدعم", desc: "تصنيف تذاكر", agents: "dealix-delivery" },
      { title: "PDPL", desc: "حوكمة بيانات", agents: "dealix-pm" },
    ],
    servicesEn: [
      { title: "Data Diagnostic", desc: "Quality, freshness, governance", agents: "dealix-engineer" },
      { title: "Support Automation", desc: "Ticket classification", agents: "dealix-delivery" },
      { title: "PDPL", desc: "Data governance", agents: "dealix-pm" },
    ],
  },
  logistics_supply_chain: {
    id: "logistics_supply_chain",
    nameAr: "اللوجستيات",
    nameEn: "Logistics",
    icon: "🚚",
    buyersAr: ["العمليات", "COO"],
    buyersEn: ["Operations", "COO"],
    problemsAr: ["استثناءات مخزون", "تأخر مشاريع", "تأخر قرار"],
    problemsEn: ["Inventory exceptions", "Project delays", "Decision latency"],
    servicesAr: [
      { title: "تشخيص سلسلة الإمداد", desc: "طلب، مخزون، تنفيذ", agents: "dealix-delivery" },
      { title: "أتمتة استثناء", desc: "معالجة استثناءات", agents: "dealix-engineer" },
      { title: "تكامل", desc: "ربط أنظمة", agents: "dealix-engineer" },
    ],
    servicesEn: [
      { title: "Supply Chain Diagnostic", desc: "Demand, inventory, fulfillment", agents: "dealix-delivery" },
      { title: "Exception Automation", desc: "Exception handling", agents: "dealix-engineer" },
      { title: "Integration", desc: "System linkage", agents: "dealix-engineer" },
    ],
  },
  professional_services: {
    id: "professional_services",
    nameAr: "خدمات مهنية",
    nameEn: "Professional Services",
    icon: "💼",
    buyersAr: ["CEO", "المبيعات", "المالية"],
    buyersEn: ["CEO", "Sales", "Finance"],
    problemsAr: ["تسرّب إيراد", "تأخر عرض", "تأخر تحصيل"],
    problemsEn: ["Revenue leakage", "Quote delays", "Collection delays"],
    servicesAr: [
      { title: "تسرّب إيراد", desc: "قياس وعرض→نقد", agents: "dealix-sales" },
      { title: "أتمتة عرض", desc: "توليد عرض", agents: "dealix-engineer" },
      { title: "تحصيل", desc: "متابعة تحصيل", agents: "dealix-sales" },
    ],
    servicesEn: [
      { title: "Revenue Leakage", desc: "Lead→cash mapping", agents: "dealix-sales" },
      { title: "Proposal Automation", desc: "Proposal generation", agents: "dealix-engineer" },
      { title: "Collections", desc: "Collection follow-up", agents: "dealix-sales" },
    ],
  },
  industrial_manufacturing: {
    id: "industrial_manufacturing",
    nameAr: "الصناعة",
    nameEn: "Industrial",
    icon: "🏭",
    buyersAr: ["العمليات", "COO", "المالية"],
    buyersEn: ["Operations", "COO", "CFO"],
    problemsAr: ["فشل جودة", "استثناء مخزون", "تسرّب تكلفة"],
    problemsEn: ["Quality failure", "Inventory exception", "Cost leakage"],
    servicesAr: [
      { title: "تشخيص عمليات", desc: "إنتاجية، جودة", agents: "dealix-delivery" },
      { title: "أتمتة جودة", desc: "فحص جودة", agents: "dealix-engineer" },
      { title: "تكامل", desc: "ربط ERP", agents: "dealix-engineer" },
    ],
    servicesEn: [
      { title: "Operations Diagnostic", desc: "Throughput, quality", agents: "dealix-delivery" },
      { title: "Quality Automation", desc: "Quality checks", agents: "dealix-engineer" },
      { title: "Integration", desc: "ERP linkage", agents: "dealix-engineer" },
    ],
  },
  retail_commerce_ecommerce: {
    id: "retail_commerce_ecommerce",
    nameAr: "التجزئة",
    nameEn: "Retail & eCommerce",
    icon: "🛍️",
    buyersAr: ["التسويق", "العمليات"],
    buyersEn: ["Marketing", "Operations"],
    problemsAr: ["دعم متراكم", "إرجاع", "تسرّب إيراد"],
    problemsEn: ["Support backlog", "Returns", "Revenue leakage"],
    servicesAr: [
      { title: "دعم", desc: "أتمتة تذاكر", agents: "dealix-delivery" },
      { title: "تحويل", desc: "تحسين تحويل", agents: "dealix-content" },
      { title: "تحليلات", desc: "تتبع طلب", agents: "dealix-engineer" },
    ],
    servicesEn: [
      { title: "Support", desc: "Ticket automation", agents: "dealix-delivery" },
      { title: "Conversion", desc: "Conversion optimization", agents: "dealix-content" },
      { title: "Analytics", desc: "Order tracking", agents: "dealix-engineer" },
    ],
  },
  real_estate_proptech: {
    id: "real_estate_proptech",
    nameAr: "العقار",
    nameEn: "Real Estate",
    icon: "🏢",
    buyersAr: ["العمليات", "COO"],
    buyersEn: ["Operations", "COO"],
    problemsAr: ["استثناءات تشغيل", "فوضى مستندات"],
    problemsEn: ["Ops exceptions", "Document chaos"],
    servicesAr: [
      { title: "تشغيل", desc: "صيانة، مستندات", agents: "dealix-delivery" },
      { title: "مستندات", desc: "ذكاء مستندات", agents: "dealix-engineer" },
      { title: "تأجير→نقد", desc: "تحصيل", agents: "dealix-sales" },
    ],
    servicesEn: [
      { title: "Operations", desc: "Maintenance, docs", agents: "dealix-delivery" },
      { title: "Documents", desc: "Document intelligence", agents: "dealix-engineer" },
      { title: "Lease→Cash", desc: "Collections", agents: "dealix-sales" },
    ],
  },

  energy_utilities_oil_gas: {
    id: "energy_utilities_oil_gas",
    nameAr: "الطاقة والمرافق",
    nameEn: "Energy & Utilities",
    icon: "⚡",
    buyersAr: ["CTO", "الأمن السيبراني", "العمليات"],
    buyersEn: ["CTO", "CISO", "Operations"],
    problemsAr: ["مخاطر سيبرانية", "تحميل تشغيلي", "تأخر قرار"],
    problemsEn: ["Cyber risk", "Ops overload", "Decision latency"],
    servicesAr: [
      { title: "AI خاص", desc: "نشر محلي آمن", agents: "dealix-engineer" },
      { title: "مراقبة عمليات", desc: "كشف استثناء", agents: "dealix-delivery" },
      { title: "حوكمة", desc: "تقييم NCA", agents: "dealix-pm" },
    ],
    servicesEn: [
      { title: "Private AI", desc: "Secure on-prem", agents: "dealix-engineer" },
      { title: "Ops Monitoring", desc: "Exception detection", agents: "dealix-delivery" },
      { title: "Governance", desc: "NCA assessment", agents: "dealix-pm" },
    ],
  },
  mining_metals: {
    id: "mining_metals",
    nameAr: "التعدين",
    nameEn: "Mining & Metals",
    icon: "⛏️",
    buyersAr: ["العمليات", "CFO"],
    buyersEn: ["Operations", "CFO"],
    problemsAr: ["تأخر مشروع", "تكلفة", "مخاطر"],
    problemsEn: ["Project delays", "Cost", "Risk"],
    servicesAr: [
      { title: "تشغيل", desc: "إنتاجية", agents: "dealix-delivery" },
      { title: "تكلفة", desc: "تحليل تكلفة", agents: "dealix-sales" },
      { title: "مخاطر", desc: "تقييم مخاطر", agents: "dealix-pm" },
    ],
    servicesEn: [
      { title: "Operations", desc: "Throughput", agents: "dealix-delivery" },
      { title: "Cost", desc: "Cost analysis", agents: "dealix-sales" },
      { title: "Risk", desc: "Risk assessment", agents: "dealix-pm" },
    ],
  },
  tourism_hospitality: {
    id: "tourism_hospitality",
    nameAr: "السياحة والضيافة",
    nameEn: "Tourism & Hospitality",
    icon: "🏨",
    buyersAr: ["العمليات", "التسويق"],
    buyersEn: ["Operations", "Marketing"],
    problemsAr: ["تجربة عميل", "حجز", "دعم"],
    problemsEn: ["Customer experience", "Booking", "Support"],
    servicesAr: [
      { title: "تجربة عميل", desc: "تحسين تجربة", agents: "dealix-delivery" },
      { title: "حجز", desc: "أتمتة حجز", agents: "dealix-engineer" },
      { title: "دعم", desc: "دعم", agents: "dealix-delivery" },
    ],
    servicesEn: [
      { title: "Customer Experience", desc: "Experience improvement", agents: "dealix-delivery" },
      { title: "Booking", desc: "Booking automation", agents: "dealix-engineer" },
      { title: "Support", desc: "Support", agents: "dealix-delivery" },
    ],
  },
  telecom_media_marketing: {
    id: "telecom_media_marketing",
    nameAr: "الاتصالات والإعلام",
    nameEn: "Telecom & Media",
    icon: "📡",
    buyersAr: ["CTO", "التسويق"],
    buyersEn: ["CTO", "Marketing"],
    problemsAr: ["تشتت بيانات", "حملات", "تحويل"],
    problemsEn: ["Data fragmentation", "Campaigns", "Conversion"],
    servicesAr: [
      { title: "بيانات", desc: "توحيد بيانات", agents: "dealix-engineer" },
      { title: "حملات", desc: "أتمتة حملات", agents: "dealix-content" },
      { title: "تحويل", desc: "تحسين تحويل", agents: "dealix-sales" },
    ],
    servicesEn: [
      { title: "Data", desc: "Data unification", agents: "dealix-engineer" },
      { title: "Campaigns", desc: "Campaign automation", agents: "dealix-content" },
      { title: "Conversion", desc: "Conversion optimization", agents: "dealix-sales" },
    ],
  },
  education_training: {
    id: "education_training",
    nameAr: "التعليم",
    nameEn: "Education",
    icon: "🎓",
    buyersAr: ["العمليات", "التقنية"],
    buyersEn: ["Operations", "Tech"],
    problemsAr: ["إدارة معرفة", "تسجيل", "دعم طلاب"],
    problemsEn: ["Knowledge mgmt", "Enrollment", "Student support"],
    servicesAr: [
      { title: "معرفة", desc: "إدارة معرفة", agents: "dealix-delivery" },
      { title: "تسجيل", desc: "أتمتة تسجيل", agents: "dealix-engineer" },
      { title: "دعم", desc: "دعم", agents: "dealix-delivery" },
    ],
    servicesEn: [
      { title: "Knowledge", desc: "Knowledge mgmt", agents: "dealix-delivery" },
      { title: "Enrollment", desc: "Enrollment automation", agents: "dealix-engineer" },
      { title: "Support", desc: "Support", agents: "dealix-delivery" },
    ],
  },
  agriculture_food_water: {
    id: "agriculture_food_water",
    nameAr: "الزراعة والمياه",
    nameEn: "Agriculture & Water",
    icon: "🌾",
    buyersAr: ["العمليات", "المالية"],
    buyersEn: ["Operations", "Finance"],
    problemsAr: ["سلسلة إمداد", "جودة", "تكلفة"],
    problemsEn: ["Supply chain", "Quality", "Cost"],
    servicesAr: [
      { title: "سلسلة إمداد", desc: "تشخيص", agents: "dealix-delivery" },
      { title: "جودة", desc: "مراقبة جودة", agents: "dealix-engineer" },
      { title: "تكلفة", desc: "تحليل", agents: "dealix-sales" },
    ],
    servicesEn: [
      { title: "Supply Chain", desc: "Diagnostic", agents: "dealix-delivery" },
      { title: "Quality", desc: "Quality monitoring", agents: "dealix-engineer" },
      { title: "Cost", desc: "Analysis", agents: "dealix-sales" },
    ],
  },
  mobility_automotive: {
    id: "mobility_automotive",
    nameAr: "التنقل والسيارات",
    nameEn: "Mobility & Automotive",
    icon: "🚗",
    buyersAr: ["العمليات", "المبيعات"],
    buyersEn: ["Operations", "Sales"],
    problemsAr: ["أسطول", "صيانة", "مبيعات"],
    problemsEn: ["Fleet", "Maintenance", "Sales"],
    servicesAr: [
      { title: "أسطول", desc: "إدارة أسطول", agents: "dealix-delivery" },
      { title: "صيانة", desc: "جدولة صيانة", agents: "dealix-engineer" },
      { title: "مبيعات", desc: "تحسين مبيعات", agents: "dealix-sales" },
    ],
    servicesEn: [
      { title: "Fleet", desc: "Fleet mgmt", agents: "dealix-delivery" },
      { title: "Maintenance", desc: "Maintenance scheduling", agents: "dealix-engineer" },
      { title: "Sales", desc: "Sales optimization", agents: "dealix-sales" },
    ],
  },
  export_import_rhq: {
    id: "export_import_rhq",
    nameAr: "الاستيراد والتصدير",
    nameEn: "Export/Import & RHQ",
    icon: "🌐",
    buyersAr: ["التجارة", "المالية"],
    buyersEn: ["Trade", "Finance"],
    problemsAr: ["دخول سوق", "امتثال", "شريك"],
    problemsEn: ["Market entry", "Compliance", "Partner"],
    servicesAr: [
      { title: "دخول سوق", desc: "ذكاء سوق سعودي", agents: "dealix-sales" },
      { title: "امتثال", desc: "تقييم امتثال", agents: "dealix-pm" },
      { title: "شريك", desc: "مطابقة شريك", agents: "dealix-sales" },
    ],
    servicesEn: [
      { title: "Market Entry", desc: "Saudi market intel", agents: "dealix-sales" },
      { title: "Compliance", desc: "Compliance assessment", agents: "dealix-pm" },
      { title: "Partner", desc: "Partner matching", agents: "dealix-sales" },
    ],
  },
  creative_sports_gaming: {
    id: "creative_sports_gaming",
    nameAr: "إبداع ورياضة",
    nameEn: "Creative & Sports",
    icon: "🎮",
    buyersAr: ["التسويق", "العمليات"],
    buyersEn: ["Marketing", "Operations"],
    problemsAr: ["فعاليات", "تذاكر", "رعاة"],
    problemsEn: ["Events", "Ticketing", "Sponsors"],
    servicesAr: [
      { title: "فعاليات", desc: "إدارة فعاليات", agents: "dealix-delivery" },
      { title: "تذاكر", desc: "نظام تذاكر", agents: "dealix-engineer" },
      { title: "رعاة", desc: "إدارة رعاة", agents: "dealix-sales" },
    ],
    servicesEn: [
      { title: "Events", desc: "Event mgmt", agents: "dealix-delivery" },
      { title: "Ticketing", desc: "Ticketing system", agents: "dealix-engineer" },
      { title: "Sponsors", desc: "Sponsor mgmt", agents: "dealix-sales" },
    ],
  },
  associations_nonprofits: {
    id: "associations_nonprofits",
    nameAr: "جمعيات وغير ربحية",
    nameEn: "Associations & Nonprofits",
    icon: "🤝",
    buyersAr: ["العمليات", "المالية"],
    buyersEn: ["Operations", "Finance"],
    problemsAr: ["تبرعات", "متطوعين", "تقارير"],
    problemsEn: ["Donations", "Volunteers", "Reporting"],
    servicesAr: [
      { title: "تبرعات", desc: "إدارة تبرعات", agents: "dealix-engineer" },
      { title: "متطوعين", desc: "تنسيق", agents: "dealix-delivery" },
      { title: "تقارير", desc: "تقارير", agents: "dealix-content" },
    ],
    servicesEn: [
      { title: "Donations", desc: "Donation mgmt", agents: "dealix-engineer" },
      { title: "Volunteers", desc: "Coordination", agents: "dealix-delivery" },
      { title: "Reporting", desc: "Reporting", agents: "dealix-content" },
    ],
  },

};

export const ALL_SECTORS = Object.values(SECTOR_SOLUTIONS);

// Fallback for remaining sectors (generic)
export function getSector(id: string): SectorSolution | undefined {
  return SECTOR_SOLUTIONS[id as SectorId];
}
