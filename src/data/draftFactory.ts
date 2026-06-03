// Dealix — Daily 400 System Draft Factory (canonical configuration)
//
// This module is the single source of truth for the outreach engine:
//   - How many personalized drafts are produced per system per day.
//   - The hard invariant that drafts are NOT sends.
//   - The safety gates that must be green before any send is enabled.
//   - The fields every draft (Client Need Card) must carry.
//
// Governance alignment: company_os/governance/agent_permissions.md
//   "AI drafts → Human reviews → Approve/Reject → If approved: execute → Log"
//
// Kept React-free so Node tests can import it directly.

import type { SystemSlug } from "./systems";

/** Total personalized drafts produced every day. */
export const DAILY_DRAFT_TOTAL = 400;

/**
 * HARD RULE: producing 400 drafts/day is required.
 * Enabling 400 sends/day is NOT on by default — it requires the safety gates
 * below plus explicit human approval per batch.
 */
export const SEND_DEFAULT_ENABLED = false;

export type DraftAllocation = {
  slug: SystemSlug;
  drafts: number;
};

/** Per-system daily draft allocation. Must sum to DAILY_DRAFT_TOTAL. */
export const DRAFT_DISTRIBUTION: DraftAllocation[] = [
  { slug: "revenue-operating-system", drafts: 100 },
  { slug: "follow-up-recovery-os", drafts: 90 },
  { slug: "executive-command-os", drafts: 70 },
  { slug: "whatsapp-client-os", drafts: 70 },
  { slug: "proposal-proof-os", drafts: 70 },
];

export type SendRampPhase = {
  phase: string;
  draftsPerDay: string;
  sendsPerDay: string;
};

/**
 * Safe daily send ramp. Drafts stay constant; sends only grow as domain
 * health holds. Aligned with Google sender guidelines (gradual warm-up,
 * SPF/DKIM/DMARC, spam rate < 0.3%, working unsubscribe).
 */
export const SEND_RAMP: SendRampPhase[] = [
  { phase: "الأسبوع 1 (أول 7 أيام)", draftsPerDay: "400", sendsPerDay: "20–40" },
  { phase: "الأسبوع 2", draftsPerDay: "400", sendsPerDay: "50–100" },
  { phase: "الأسبوع 3", draftsPerDay: "400", sendsPerDay: "100–200" },
  { phase: "الأسبوع 4", draftsPerDay: "400", sendsPerDay: "200–300" },
  { phase: "بعد ثبات صحة الدومين", draftsPerDay: "400–800", sendsPerDay: "300–400" },
];

/** Gates that must ALL be satisfied before sends are enabled or ramped. */
export const SEND_SAFETY_GATES: string[] = [
  "موافقة بشرية على كل دفعة إرسال (approval)",
  "رابط إلغاء اشتراك واضح ويعمل (unsubscribe)",
  "قائمة استبعاد فعّالة (suppression list)",
  "جاهزية مصادقة الدومين SPF / DKIM / DMARC",
  "صحة دومين جيدة (domain health) و bounce منخفض",
  "spam complaints منخفضة و reply rate مقبول",
];

/** Practices that are never allowed in the outreach engine. */
export const PROHIBITED_PRACTICES: string[] = [
  "لا cold WhatsApp تلقائي",
  "لا LinkedIn automation",
  "لا قوائم بريد مشتراة (purchased lists)",
  "لا Re:/Fwd: مزيفة أو عناوين مضللة",
  "لا وعود بأرقام إيراد محددة",
  "لا أسرار أو بيانات شخصية (PII) في المسودات أو السجلات",
  "لا أسماء وحدات/أنظمة داخلية في نص موجّه للعميل",
];

/** Required fields on every personalized draft (Client Need Card). */
export const CLIENT_NEED_CARD_FIELDS = [
  "company",
  "sector",
  "country",
  "city",
  "website",
  "signal",
  "likely_pain",
  "recommended_system",
  "why_this_system",
  "first_mission",
  "proof_angle",
  "email_angle",
  "cta",
  "risk_level",
  "evidence_level",
  "approval_status",
  "send_readiness",
] as const;

export type ClientNeedCardField = (typeof CLIENT_NEED_CARD_FIELDS)[number];

/** How the daily Top-100 approval queue is ranked before any send. */
export const APPROVAL_RANKING_SIGNALS: string[] = [
  "ألم واضح",
  "قطاع مناسب",
  "إشارة شراء",
  "قابلية الدفع",
  "جودة التخصيص",
  "انخفاض المخاطر",
];

/** Sum of the per-system draft allocation. */
export function totalAllocatedDrafts(): number {
  return DRAFT_DISTRIBUTION.reduce((sum, item) => sum + item.drafts, 0);
}
