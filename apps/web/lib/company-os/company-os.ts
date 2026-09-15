// Company OS — Shared data backbone for the founder operating system
// Used by: /war-room, /client-acquisition, /delivery-os, /kpi-finance,
// /api/company-os/ceo-brief

export type AcquisitionStage =
  | "discover"
  | "qualify"
  | "outreach"
  | "review_draft"
  | "meeting"
  | "proposal"
  | "close"
  | "deliver"
  | "retain";

export interface AcquisitionStep {
  id: AcquisitionStage;
  title: string;
  titleAr: string;
  goal: string;
  goalAr: string;
  owner: string;
  exitCriteria: string;
  exitCriteriaAr: string;
  tools: string[];
}

export interface DeliveryStage {
  id: "intake" | "workflow_map" | "command_setup" | "automation_build" | "weekly_review" | "expansion";
  title: string;
  titleAr: string;
  dayRange: string;
  deliverables: string[];
  deliverablesAr: string[];
  risk: string;
  riskAr: string;
}

export interface KpiMetric {
  id: string;
  label: string;
  labelAr: string;
  unit: string;
  target: number;
  current: number;
  owner: string;
  cadence: "daily" | "weekly" | "monthly";
  status: "on_track" | "watch" | "off_track";
  source: string;
}

export interface FounderPriority {
  id: string;
  rank: number;
  title: string;
  titleAr: string;
  description: string;
  descriptionAr: string;
  dueInDays: number;
  blockedBy: string[];
}

export const ACQUISITION_FUNNEL: AcquisitionStep[] = [
  {
    id: "discover",
    title: "Discover",
    titleAr: "اكتشاف",
    goal: "Identify companies that match ICP and show visible operational leakage.",
    goalAr: "تحديد الشركات المطابقة لـ ICP واللي عندها تسرّب تشغيلي واضح.",
    owner: "Founder + Sales OS",
    exitCriteria: "Account list with public signal, weakness hypothesis, and source note.",
    exitCriteriaAr: "قائمة حسابات بإشارة عامة وفرضية ضعف ومصدر موثّق.",
    tools: ["business/lead-lists", "connectors/website_signal_analyzer"],
  },
  {
    id: "qualify",
    title: "Qualify",
    titleAr: "تأهيل",
    goal: "Score accounts against BANT, segment, and weakness severity.",
    goalAr: "احتساب نقاط الحسابات على BANT والقطاع وحدّة الضعف.",
    owner: "Lead scoring engine",
    exitCriteria: "Score >= 60, segment clear, weakness specific.",
    exitCriteriaAr: "نقاط ≥ 60، قطاع واضح، ضعف محدّد.",
    tools: ["scripts/score_leads.py", "business/scoring/LEAD_SCORING_MODEL.md"],
  },
  {
    id: "outreach",
    title: "Outreach (Drafts Only)",
    titleAr: "تواصل (مسوّدة فقط)",
    goal: "Generate Arabic/English drafts that match the weakness and the right offer.",
    goalAr: "توليد مسوّدة عربي/إنجليزي تتناسب مع الضعف والعرض المناسب.",
    owner: "Outreach Lab + Human Reviewer",
    exitCriteria: "Draft with review_status=pending, channel, language, and follow-ups.",
    exitCriteriaAr: "مسوّدة بحالة pending وقناة ولغة ومتابعتين.",
    tools: ["scripts/generate_outreach_drafts.py", "business/persuasion"],
  },
  {
    id: "review_draft",
    title: "Human Review Gate",
    titleAr: "بوابة المراجعة البشرية",
    goal: "Approve or reject every draft before any sending happens.",
    goalAr: "قبول أو رفض كل مسوّدة قبل أي إرسال.",
    owner: "Founder (single human reviewer)",
    exitCriteria: "review_status=approved with reviewer name and timestamp.",
    exitCriteriaAr: "review_status=approved مع اسم المراجع والتوقيت.",
    tools: ["scripts/approve_outreach_draft.py", "scripts/reject_outreach_draft.py"],
  },
  {
    id: "meeting",
    title: "Workflow Review Call",
    titleAr: "مكالمة مراجعة سير العمل",
    goal: "Run a 20-min diagnostic, capture pain, and align on the right offer.",
    goalAr: "تنفيذ تشخيص 20 دقيقة، توثيق الألم، ومواءمة العرض المناسب.",
    owner: "Founder",
    exitCriteria: "Notes saved, offer chosen, next step scheduled.",
    exitCriteriaAr: "تدوين الملاحظات، اختيار العرض، تحديد الخطوة التالية.",
    tools: ["scripts/generate_sales_call_notes.py", "business/closing/DISCOVERY_CALL_SCRIPT_AR.md"],
  },
  {
    id: "proposal",
    title: "Proposal",
    titleAr: "عرض رسمي",
    goal: "Generate a bilingual proposal scoped to the chosen offer and timeline.",
    goalAr: "توليد عرض ثنائي اللغة مربوط بالعرض والجدول الزمني.",
    owner: "Proposal generator + Founder",
    exitCriteria: "Proposal sent, logged in deal ledger, quote prepared.",
    exitCriteriaAr: "إرسال العرض، تسجيله في سجل الصفقات، تجهيز عرض السعر.",
    tools: ["scripts/generate_proposal.py", "scripts/generate_quote.py"],
  },
  {
    id: "close",
    title: "Close",
    titleAr: "إغلاق",
    goal: "Convert proposal to won deal with setup + monthly retainer.",
    goalAr: "تحويل العرض لصفقة ناجحة بإعداد + اشتراك شهري.",
    owner: "Founder + Deal Desk",
    exitCriteria: "Deal won, contract signed, kickoff scheduled.",
    exitCriteriaAr: "ربح الصفقة، توقيع العقد، تحديد الانطلاق.",
    tools: ["scripts/mark_deal_won.py", "business/closing/DEAL_DESK_RULES.md"],
  },
  {
    id: "deliver",
    title: "Deliver",
    titleAr: "تسليم",
    goal: "Run the Delivery OS end-to-end with weekly command reports.",
    goalAr: "تشغيل Delivery OS بالكامل مع تقارير قيادة أسبوعية.",
    owner: "Delivery lead + Founder review",
    exitCriteria: "Workflow live, proof report generated, client review accepted.",
    exitCriteriaAr: "سير العمل حي، تقرير إثبات جاهز، مراجعة العميل مقبولة.",
    tools: ["scripts/generate_delivery_plan.py", "scripts/generate_weekly_command_report.py"],
  },
  {
    id: "retain",
    title: "Retain & Expand",
    titleAr: "احتفاظ وتوسعة",
    goal: "Run monthly review, capture proof, and pitch next OS module.",
    goalAr: "تنفيذ مراجعة شهرية، توثيق الإثبات، وعرض وحدة OS تالية.",
    owner: "Founder + Account Manager",
    exitCriteria: "Monthly review sent, expansion offer accepted or queued.",
    exitCriteriaAr: "إرسال مراجعة شهرية، قبول عرض توسعة أو جدولته.",
    tools: ["scripts/generate_monthly_client_review.py", "scripts/generate_expansion_offer.py"],
  },
];

export const DELIVERY_PIPELINE: DeliveryStage[] = [
  {
    id: "intake",
    title: "Intake",
    titleAr: "الاستلام",
    dayRange: "Intake phase",
    deliverables: [
      "Signed contract and PO",
      "Stakeholder map (decision maker + blockers + influencers)",
      "Channel of truth (Slack/WhatsApp group)",
      "Confidential data scope document",
    ],
    deliverablesAr: [
      "العقد و أمر الشراء",
      "خريطة أصحاب المصلحة (صانع القرار + المعطّلات + المؤثرين)",
      "قناة الحقيقة الوحيدة (مجموعة سلاك/واتساب)",
      "وثيقة نطاق البيانات السرية",
    ],
    risk: "If the stakeholder map is unclear, the initial scope stalls.",
    riskAr: "لو خريطة أصحاب المصلحة غير واضحة، يتعثر النطاق الأولي.",
  },
  {
    id: "workflow_map",
    title: "Workflow Map",
    titleAr: "خريطة سير العمل",
    dayRange: "Discovery and mapping phase",
    deliverables: [
      "End-to-end workflow map (as-is)",
      "Pain points tagged with revenue/cost/risk impact",
      "Selected OS modules list with clear scope",
      "First automation candidates (top 3)",
    ],
    deliverablesAr: [
      "خريطة سير العمل الكاملة (الحالي)",
      "نقاط الألم موسومة بالأثر (إيراد/تكلفة/مخاطرة)",
      "قائمة وحدات OS المختارة بنطاق واضح",
      "أفضل 3 مرشحين للأتمتة",
    ],
    risk: "Trying to automate everything before the first bounded proof.",
    riskAr: "محاولة أتمتة كل شيء قبل أول إثبات محدود.",
  },
  {
    id: "command_setup",
    title: "Command Center Setup",
    titleAr: "تجهيز غرفة القيادة",
    dayRange: "Command setup phase",
    deliverables: [
      "Command Center URL live with first 3 modules",
      "Owner assignment per metric",
      "Cadence definition (daily standup, weekly review)",
      "Escalation path documented",
    ],
    deliverablesAr: [
      "رابط غرفة القيادة حيّ بأول 3 وحدات",
      "تعيين مسؤول لكل مؤشر",
      "تحديد الإيقاع (standup يومي، مراجعة أسبوعية)",
      "توثيق مسار التصعيد",
    ],
    risk: "Metrics without owners or cadence — pure dashboard theater.",
    riskAr: "مؤشرات بدون مسؤول أو إيقاع = داشبورد فارغ.",
  },
  {
    id: "automation_build",
    title: "Automation Build",
    titleAr: "بناء الأتمتة",
    dayRange: "Automation build phase",
    deliverables: [
      "Top 3 automations live and tested",
      "Fallback rules for human review on edge cases",
      "Audit log on every external action",
      "First end-to-end test report",
    ],
    deliverablesAr: [
      "أفضل 3 أتمتة حية ومختبرة",
      "قواعد احتياطية للمراجعة البشرية على الحالات الحرجة",
      "سجل تدقيق لكل إجراء خارجي",
      "أول تقرير اختبار شامل",
    ],
    risk: "Automating before proof of value on a small slice.",
    riskAr: "أتمتة قبل إثبات القيمة على شريحة صغيرة.",
  },
  {
    id: "weekly_review",
    title: "Operating Review",
    titleAr: "مراجعة تشغيلية",
    dayRange: "Operating review cadence",
    deliverables: [
      "Weekly command report (5 metrics + 3 risks + 3 next moves)",
      "Client sign-off on each report",
      "Proof items added to vault",
      "Decisions log updated",
    ],
    deliverablesAr: [
      "تقرير قيادة أسبوعي (5 مؤشرات + 3 مخاطر + 3 خطوات)",
      "اعتماد العميل على كل تقرير",
      "إضافة عناصر إثبات لخزانة الإثبات",
      "تحديث سجل القرارات",
    ],
    risk: "Skipping the review kills retention and expansion.",
    riskAr: "تخطّي المراجعة يقتل الاحتفاظ والتوسعة.",
  },
  {
    id: "expansion",
    title: "Expansion Review",
    titleAr: "مراجعة التوسعة",
    dayRange: "Evidence-based expansion phase",
    deliverables: [
      "Quarterly business review",
      "Expansion offer based on observed gap",
      "Case study draft (with client approval)",
      "Referral ask (warm intro script ready)",
    ],
    deliverablesAr: [
      "مراجعة أعمال ربع سنوية",
      "عرض توسعة مبني على فجوة مرصودة",
      "مسوّدة دراسة حالة (بموافقة العميل)",
      "طلب إحالة (سكريبت تعريف جاهز)",
    ],
    risk: "Pitching expansion without a proof report.",
    riskAr: "عرض توسعة بدون تقرير إثبات.",
  },
];

export const KPI_METRICS: KpiMetric[] = [
  {
    id: "monthly_revenue_sar",
    label: "Monthly Recurring Revenue",
    labelAr: "الإيرادات الشهرية المتكررة",
    unit: "SAR",
    target: 250000,
    current: 42000,
    owner: "Founder",
    cadence: "monthly",
    status: "watch",
    source: "scripts/generate_daily_ceo_brief.py",
  },
  {
    id: "active_retainers",
    label: "Active Retainer Clients",
    labelAr: "عملاء اشتراك فعّال",
    unit: "clients",
    target: 12,
    current: 3,
    owner: "Founder",
    cadence: "monthly",
    status: "on_track",
    source: "business/_data/deals.ledger.json",
  },
  {
    id: "proposal_conversion",
    label: "Proposal → Close Rate",
    labelAr: "نسبة تحويل العرض إلى إغلاق",
    unit: "%",
    target: 35,
    current: 22,
    owner: "Sales",
    cadence: "monthly",
    status: "watch",
    source: "business/conversion/CONVERSION_SCORECARD.md",
  },
  {
    id: "drafts_pending_review",
    label: "Drafts Pending Human Review",
    labelAr: "مسوّدات تنتظر المراجعة",
    unit: "drafts",
    target: 0,
    current: 14,
    owner: "Founder",
    cadence: "daily",
    status: "off_track",
    source: "business/_data/outreach_review_queue.json",
  },
  {
    id: "followups_due_today",
    label: "Follow-ups Due Today",
    labelAr: "متابعات مستحقة اليوم",
    unit: "followups",
    target: 5,
    current: 8,
    owner: "Founder",
    cadence: "daily",
    status: "on_track",
    source: "scripts/generate_followup_queue.py",
  },
  {
    id: "proof_items_logged",
    label: "Proof Items Logged This Month",
    labelAr: "عناصر إثبات مسجّلة هذا الشهر",
    unit: "items",
    target: 20,
    current: 7,
    owner: "Delivery lead",
    cadence: "monthly",
    status: "watch",
    source: "business/_data/proof_vault.json",
  },
];

export const FOUNDER_PRIORITIES: FounderPriority[] = [
  {
    id: "review_drafts",
    rank: 1,
    title: "Clear the review queue — 14 drafts waiting",
    titleAr: "تصفّر طابور المراجعة — 14 مسوّدة تنتظر",
    description: "Approve or reject every pending draft. Block any sending until status is approved.",
    descriptionAr: "اقبل أو ارفض كل مسوّدة معلّقة. امنع أي إرسال حتى تتغير الحالة إلى approved.",
    dueInDays: 1,
    blockedBy: [],
  },
  {
    id: "ship_launch_brief",
    rank: 2,
    title: "Generate today’s launch brief + CEO brief",
    titleAr: "ولّد ملخص الإطلاق اليومي + ملخص CEO",
    description: "Run the daily operator, then publish the launch brief to the founder channel.",
    descriptionAr: "شغّل المشغّل اليومي، ثم انشر ملخص الإطلاق في قناة المؤسس.",
    dueInDays: 1,
    blockedBy: [],
  },
  {
    id: "first_100_leads",
    rank: 3,
    title: "First 100 leads plan — segment split ready",
    titleAr: "خطة أول 100 ليد — تقسيم القطاعات جاهز",
    description: "Build, review, and approve the first 100 leads plan (25 agencies / 20 training / 15 clinics / 15 brokers / 15 logistics / 10 partners).",
    descriptionAr: "ابنِ وراجع ووافق على خطة أول 100 ليد (25 وكالات / 20 تدريب / 15 عيادات / 15 وسطاء / 15 لوجستيات / 10 شركاء).",
    dueInDays: 3,
    blockedBy: ["review_drafts"],
  },
  {
    id: "deployment_readiness",
    rank: 4,
    title: "Deployment readiness — Vercel + Railway",
    titleAr: "جاهزية النشر — Vercel + Railway",
    description: "Run production_readiness_check and address any P0 blockers before announcing launch.",
    descriptionAr: "شغّل فحص جاهزية الإنتاج وعالج أي عائق P0 قبل إعلان الإطلاق.",
    dueInDays: 5,
    blockedBy: ["ship_launch_brief"],
  },
  {
    id: "first_retainer",
    rank: 5,
    title: "First retainer contract signed",
    titleAr: "توقيع أول عقد اشتراك",
    description: "Convert the highest-priority demo account into a paying retainer.",
    descriptionAr: "حوّل أعلى حساب تجريبي أولوية إلى عقد اشتراك مدفوع.",
    dueInDays: 14,
    blockedBy: ["first_100_leads", "deployment_readiness"],
  },
];

export function ceoBriefMarkdown(date: string, mode: "demo" | "production" = "demo"): string {
  const lines: string[] = [];
  lines.push(`# Dealix Daily CEO Brief — ${date}`);
  lines.push("");
  lines.push(`Mode: ${mode}`);
  lines.push("");
  lines.push("## 1. Acquisition Moves");
  for (const step of ACQUISITION_FUNNEL.slice(0, 5)) {
    lines.push(`- **${step.title}** (${step.titleAr}): ${step.goal}`);
  }
  lines.push("");
  lines.push("## 2. Delivery Moves");
  for (const stage of DELIVERY_PIPELINE.slice(0, 3)) {
    lines.push(`- **${stage.title}** (${stage.titleAr}) — ${stage.dayRange}`);
    for (const d of stage.deliverables.slice(0, 2)) lines.push(`  - ${d}`);
  }
  lines.push("");
  lines.push("## 3. KPI Checks");
  for (const k of KPI_METRICS) {
    const gap = k.target === 0 ? 0 : Math.round(((k.current - k.target) / Math.max(1, k.target)) * 100);
    const arrow = gap >= 0 ? "OK" : "GAP";
    lines.push(`- [${arrow}] ${k.label} (${k.labelAr}): target ${k.target}${k.unit}, current ${k.current}${k.unit} (${gap}%)`);
  }
  lines.push("");
  lines.push("## 4. Risks");
  lines.push("- Review queue not cleared → no outreach should be sent.");
  lines.push("- Conversion rate below 35% — tighten close criteria and proposal quality.");
  lines.push("- Proof vault underused — coach delivery lead to log proof items weekly.");
  lines.push("");
  lines.push("## 5. Operating Focus");
  for (const p of FOUNDER_PRIORITIES) {
    lines.push(`- [P${p.rank}] ${p.title} (${p.titleAr}) — due in ${p.dueInDays}d`);
  }
  lines.push("");
  lines.push("---");
  lines.push("Generated by Dealix Company OS. Draft only. Human review required before any external action.");
  return lines.join("\n");
}

export function ceoBriefJson(date: string, mode: "demo" | "production" = "demo") {
  return {
    date,
    mode,
    acquisition: ACQUISITION_FUNNEL.map((s) => ({
      id: s.id,
      title: s.title,
      titleAr: s.titleAr,
      goal: s.goal,
      goalAr: s.goalAr,
      exitCriteria: s.exitCriteria,
      exitCriteriaAr: s.exitCriteriaAr,
    })),
    delivery: DELIVERY_PIPELINE.map((s) => ({
      id: s.id,
      title: s.title,
      titleAr: s.titleAr,
      dayRange: s.dayRange,
      deliverables: s.deliverables,
      deliverablesAr: s.deliverablesAr,
      risk: s.risk,
    })),
    kpis: KPI_METRICS.map((k) => ({
      id: k.id,
      label: k.label,
      labelAr: k.labelAr,
      target: k.target,
      current: k.current,
      unit: k.unit,
      status: k.status,
      cadence: k.cadence,
      owner: k.owner,
    })),
    priorities: FOUNDER_PRIORITIES.map((p) => ({
      id: p.id,
      rank: p.rank,
      title: p.title,
      titleAr: p.titleAr,
      dueInDays: p.dueInDays,
      blockedBy: p.blockedBy,
    })),
    safety: {
      noAutoSend: true,
      humanReviewRequired: true,
      noScraping: true,
      noSpam: true,
    },
  };
}
