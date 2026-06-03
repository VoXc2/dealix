// Dealix Daily Operating Factory — shared engine.
// Pure, dependency-free ESM. Loaders + scoring + gates + security scans +
// derived board views + markdown renderers. The commercial:* entry scripts are
// thin wrappers over this module, so each recomputes the full derived state from
// company_os/commercial/* on every run (order-independent).

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(__dirname, "..", "..");
const DATA = path.join(ROOT, "company_os", "commercial");
const REPORTS = path.join(ROOT, "reports");

// ── Constants ─────────────────────────────────────────────────────────────
export const SCORE_MAX = {
  personalization: 25,
  pain_clarity: 20,
  system_fit: 20,
  cta_clarity: 15,
  risk_safety: 10,
  tone_quality: 10,
};
export const SCORE_CRITERIA = Object.keys(SCORE_MAX);

export const BOARD_STATUSES = [
  "researched", "need_card_ready", "draft_ready", "approved", "sent",
  "call_due", "called", "interested", "mini_proposal_ready", "proposal_sent",
  "won", "delivery_started", "active", "renewal_candidate", "lost", "do_not_contact",
];

export const REQUIRED_SUPER_COMMAND_SECTIONS = [
  "Today's critical decision",
  "400 Draft status",
  "Top 100 Approval Queue",
  "Top 20 companies to send",
  "Top 30 calls to make",
  "Mini proposals waiting approval",
  "Delivery pipelines status",
  "Website leads",
  "Best performing system",
  "Best sector",
  "Biggest risk",
  "Cash / pricing opportunities",
  "Tomorrow recommendation",
];

// Detection patterns. Treated as data, never executed.
export const GUARANTEE_PATTERNS = [
  /نضمن/, /مضمون/, /ضمان/, /نضاعف/, /زيادة\s+مضمونة/,
  /\b100\s*%/, /\bguarantee/i, /\bguaranteed/i, /\bROI\s+مضمون/i,
];

export const INJECTION_PATTERNS = [
  /ignore (all |your |the )?previous instructions/i,
  /disregard (all |the )?(previous|above) instructions/i,
  /send (this|your system prompt|the prompt)/i,
  /reveal (the )?(secret|system prompt|api key)/i,
  /execute (the )?command/i,
  /change (the )?system prompt/i,
  /api[_\s-]?key/i,
  /forget (everything|all previous)/i,
];

export const SECRET_PATTERNS = [
  /sk-[A-Za-z0-9]{16,}/,
  /AKIA[0-9A-Z]{12,}/,
  /Bearer\s+[A-Za-z0-9._-]{16,}/,
  /(APP_SECRET|API_KEY|DATABASE_URL|PASSWORD)\s*=\s*\S+/,
];

const PAIN_AS_FACT_PATTERNS = [
  /أنتم تعانون/, /عندكم مشكلة/, /واضح أنكم تخسرون/, /أنتم تخسرون/, /تعانون من/,
];

const RE_FWD_PATTERNS = [/^\s*re\s*:/i, /^\s*fwd?\s*:/i, /^\s*رد\s*:/, /^\s*إعادة توجيه/];

// ── Loaders ───────────────────────────────────────────────────────────────
export function loadJson(file, fallback) {
  try {
    return JSON.parse(fs.readFileSync(file, "utf-8"));
  } catch {
    return fallback;
  }
}

export function loadContext(dataDir = DATA) {
  const systems = loadJson(path.join(dataDir, "systems.json"), { systems: [] });
  const suppression = loadJson(path.join(dataDir, "suppression.json"), { companies: [], domains: [] });
  const draftFactory = loadJson(path.join(dataDir, "draft_factory.json"), { drafts: [], target_per_day: 400 });
  const board = loadJson(path.join(dataDir, "board.json"), { opportunities: [] });
  const content = loadJson(path.join(dataDir, "content_calendar.json"), { weekly_themes: [], queue: [] });
  const partners = loadJson(path.join(dataDir, "partners.json"), { partner_fit: [], pipeline: [] });
  const websiteLeads = loadJson(path.join(dataDir, "website_leads.json"), { leads: [] });
  const systemIds = (systems.systems || []).map((s) => s.id);
  const systemById = Object.fromEntries((systems.systems || []).map((s) => [s.id, s]));
  return { systems, suppression, draftFactory, board, content, partners, websiteLeads, systemIds, systemById };
}

export function today() {
  return process.env.DEALIX_TODAY || new Date().toISOString().slice(0, 10);
}

export function systemName(ctx, id) {
  if (!id) return "—";
  const s = ctx.systemById[id];
  return s ? s.customer_name_ar : id;
}

// ── Detection helpers ───────────────────────────────────────────────────────
export const matchesAny = (text, patterns) => patterns.some((re) => re.test(text || ""));
export const containsGuaranteedClaim = (text) => matchesAny(text, GUARANTEE_PATTERNS);
export const containsPromptInjection = (text) => matchesAny(text, INJECTION_PATTERNS);
export const containsSecret = (text) => matchesAny(text, SECRET_PATTERNS);
export const statesPainAsFact = (text) => matchesAny(text, PAIN_AS_FACT_PATTERNS);
export const isLowEvidence = (level) => level === "L0" || level === "L1";

export function isFakeReFwd(subject, threadExists) {
  return !threadExists && matchesAny(subject, RE_FWD_PATTERNS);
}

export function leaksInternalName(text, systemIds) {
  const t = (text || "").toLowerCase();
  return systemIds.some((id) => t.includes(id.toLowerCase()));
}

// Diagnostic router: maps free-text intake (e.g. a website form) to a system.
const RECOMMEND_RULES = [
  { system: "whatsapp_client_os", patterns: [/واتساب/, /يتوهون/, /whatsapp/i] },
  { system: "followup_recovery_os", patterns: [/متابعة/, /تسجيلات/, /لا نتابع/, /نسينا/, /follow.?up/i] },
  { system: "executive_command_os", patterns: [/تقارير/, /قرار/, /لوحة/, /kpi/i, /dashboard/i] },
  { system: "proposal_proof_os", patterns: [/عرض/, /عروض/, /إثبات/, /proposal/i, /proof/i] },
  { system: "revenue_operating_system", patterns: [/تسرب/, /إيراد/, /فرص/, /pipeline/i, /revenue/i] },
];

export function recommendSystem(text) {
  for (const rule of RECOMMEND_RULES) {
    if (matchesAny(text, rule.patterns)) return rule.system;
  }
  return "revenue_operating_system"; // default umbrella system
}

export function isSuppressed(company, domain, suppression) {
  const companies = (suppression.companies || []).map((c) => c.toLowerCase());
  const domains = suppression.domains || [];
  if (company && companies.includes(company.toLowerCase())) return true;
  if (domain && domains.some((d) => domain.toLowerCase().endsWith(d.toLowerCase()))) return true;
  return false;
}

// ── Scoring ────────────────────────────────────────────────────────────────
// Returns { total, valid, issues } — clamps out-of-range values and flags them.
export function scoreTotal(scores = {}) {
  let total = 0;
  const issues = [];
  for (const k of SCORE_CRITERIA) {
    const max = SCORE_MAX[k];
    let v = scores[k];
    if (typeof v !== "number" || Number.isNaN(v)) {
      issues.push(`missing_or_nan:${k}`);
      v = 0;
    } else if (v < 0 || v > max) {
      issues.push(`out_of_range:${k}`);
      v = Math.max(0, Math.min(max, v));
    }
    total += v;
  }
  return { total, valid: issues.length === 0, issues };
}

export function band(total) {
  if (total >= 85) return "top_priority";
  if (total >= 75) return "approval_queue";
  if (total >= 65) return "needs_rewrite";
  return "rejected";
}

// ── Email quality gate (hard fail conditions) ───────────────────────────────
export function emailGate(draft, ctx) {
  const reasons = [];
  if (!draft.has_need_card) reasons.push("no_need_card");
  if (!draft.recommended_system) reasons.push("no_recommended_system");
  if (!draft.cta || !String(draft.cta).trim()) reasons.push("no_cta");
  if (containsGuaranteedClaim(draft.body) || containsGuaranteedClaim(draft.subject)) reasons.push("guaranteed_claim");
  if (isFakeReFwd(draft.subject, draft.thread_exists)) reasons.push("fake_re_fwd");
  if (statesPainAsFact(draft.body) && isLowEvidence(draft.evidence_level)) reasons.push("unverified_pain_as_fact");
  if (leaksInternalName(`${draft.subject} ${draft.body}`, ctx.systemIds)) reasons.push("internal_module_name_leaked");
  if (isSuppressed(draft.company, draft.domain, ctx.suppression)) reasons.push("suppression_hit");
  if (containsPromptInjection(draft.source_excerpt) || containsPromptInjection(draft.body)) reasons.push("prompt_injection_in_source");
  if (!draft.evidence_level) reasons.push("no_evidence_level");
  return { passed: reasons.length === 0, reasons };
}

// ── Draft evaluation + batch / Top 100 ──────────────────────────────────────
export function evaluateDraft(draft, ctx) {
  const { total, valid, issues } = scoreTotal(draft.scores);
  const gate = emailGate(draft, ctx);
  const status = gate.passed ? band(total) : "rejected";
  const inTop100 =
    gate.passed &&
    total >= 75 &&
    !!draft.recommended_system &&
    draft.has_need_card === true &&
    draft.risk_level !== "high" &&
    !!draft.evidence_level &&
    !!(draft.cta && String(draft.cta).trim());
  return {
    id: draft.id,
    company: draft.company,
    system: draft.recommended_system,
    evidence_level: draft.evidence_level,
    risk_level: draft.risk_level,
    total,
    band: band(total),
    status,
    gate,
    inTop100,
    scoreValid: valid,
    scoreIssues: issues,
  };
}

export function evaluateBatch(ctx) {
  const drafts = ctx.draftFactory.drafts || [];
  const evaluations = drafts.map((d) => evaluateDraft(d, ctx));
  const counts = { top_priority: 0, approval_queue: 0, needs_rewrite: 0, rejected: 0 };
  for (const e of evaluations) counts[e.status]++;
  const rejectionReasons = {};
  for (const e of evaluations) {
    if (e.status === "rejected") {
      for (const r of e.gate.reasons) rejectionReasons[r] = (rejectionReasons[r] || 0) + 1;
    }
  }
  const top100 = evaluations
    .filter((e) => e.inTop100)
    .sort((a, b) => b.total - a.total)
    .slice(0, 100);
  return {
    total: evaluations.length,
    target: ctx.draftFactory.target_per_day || 400,
    counts,
    rejectionReasons,
    evaluations,
    top100,
  };
}

// ── Other gates ─────────────────────────────────────────────────────────────
export function callGate(brief = {}) {
  const reasons = [];
  if (!brief.opening_line || !String(brief.opening_line).trim()) reasons.push("no_opening_line");
  if (!Array.isArray(brief.questions) || brief.questions.length === 0) reasons.push("no_discovery_questions");
  if (!brief.expected_objection || !String(brief.expected_objection).trim()) reasons.push("no_expected_objection");
  if (!brief.next_step || !String(brief.next_step).trim()) reasons.push("no_next_step");
  return { passed: reasons.length === 0, reasons };
}

export function miniProposalGate(mp = {}) {
  const reasons = [];
  if (!mp.system) reasons.push("no_system");
  if (!Array.isArray(mp.deliverables) || mp.deliverables.length === 0) reasons.push("no_deliverables");
  if (!mp.timeline) reasons.push("no_timeline");
  if (typeof mp.starter_price_sar !== "number") reasons.push("no_starter_price");
  if (!Array.isArray(mp.required_inputs) || mp.required_inputs.length === 0) reasons.push("no_required_inputs");
  if (mp.approval_required !== true) reasons.push("no_approval_required");
  return { passed: reasons.length === 0, reasons };
}

export function deliveryGate(d = {}) {
  const reasons = [];
  if (!d.scope) reasons.push("no_scope");
  if (!Array.isArray(d.required_inputs) || d.required_inputs.length === 0) reasons.push("no_required_inputs");
  if (!d.success_metric) reasons.push("no_success_metric");
  if (!d.acceptance_criteria) reasons.push("no_acceptance_criteria");
  return { passed: reasons.length === 0, reasons };
}

// ── Board derived views ─────────────────────────────────────────────────────
const PRIORITY_RANK = { P1: 1, P2: 2, P3: 3, P4: 4 };

export function boardSummary(ctx) {
  const counts = Object.fromEntries(BOARD_STATUSES.map((s) => [s, 0]));
  for (const o of ctx.board.opportunities || []) {
    if (counts[o.stage] === undefined) counts[o.stage] = 0;
    counts[o.stage]++;
  }
  return counts;
}

export function callsToMake(ctx, limit = 30) {
  return (ctx.board.opportunities || [])
    .filter((o) => ["call_due", "called", "interested"].includes(o.stage) && o.call_brief)
    .sort((a, b) => (PRIORITY_RANK[a.call_priority] || 9) - (PRIORITY_RANK[b.call_priority] || 9))
    .slice(0, limit);
}

export function companiesToSend(ctx, evalResult, limit = 20) {
  return evalResult.top100.slice(0, limit);
}

export function miniProposalsWaiting(ctx) {
  return (ctx.board.opportunities || []).filter(
    (o) => o.mini_proposal && o.mini_proposal.status === "pending_founder_approval"
  );
}

export function deliveryPipelines(ctx) {
  return (ctx.board.opportunities || []).filter((o) =>
    ["won", "delivery_started", "active", "renewal_candidate"].includes(o.stage)
  );
}

export function bestSystem(evalResult) {
  const score = {};
  for (const e of evalResult.top100) score[e.system] = (score[e.system] || 0) + 1;
  let best = null;
  let max = -1;
  for (const [sys, n] of Object.entries(score)) {
    if (n > max) {
      max = n;
      best = sys;
    }
  }
  return { system: best, count: max < 0 ? 0 : max };
}

// ── Control / security checks ───────────────────────────────────────────────
// Findings model mirrors scripts/governance_check.py (CRITICAL / HIGH / INFO).
export function runControlChecks(ctx, evalResult, generatedReports = []) {
  const findings = [];
  const add = (gate, severity, detail, id) => findings.push({ gate, severity, detail, id });

  // 1. Draft data integrity + "did anything dangerous slip through?"
  for (const e of evalResult.evaluations) {
    if (!e.scoreValid) add("data_integrity", "HIGH", `Invalid score schema: ${e.scoreIssues.join(",")}`, e.id);
    if (e.status !== "rejected") {
      const draft = (ctx.draftFactory.drafts || []).find((d) => d.id === e.id) || {};
      if (containsGuaranteedClaim(draft.body) || containsGuaranteedClaim(draft.subject))
        add("email_gate", "CRITICAL", `Guaranteed claim in sendable draft`, e.id);
      if (containsPromptInjection(draft.body)) add("prompt_injection", "CRITICAL", `Injection text in sendable draft body`, e.id);
      if (containsSecret(draft.body)) add("secrets", "CRITICAL", `Secret-like token in sendable draft body`, e.id);
      if (leaksInternalName(`${draft.subject} ${draft.body}`, ctx.systemIds))
        add("email_gate", "CRITICAL", `Internal module name in sendable draft`, e.id);
    }
  }

  // 2. Prompt injection in untrusted source excerpts — must be contained (rejected).
  let injectionContained = 0;
  for (const d of ctx.draftFactory.drafts || []) {
    if (containsPromptInjection(d.source_excerpt)) {
      const ev = evalResult.evaluations.find((e) => e.id === d.id);
      if (ev && ev.status === "rejected") injectionContained++;
      else add("prompt_injection", "CRITICAL", `Untrusted injection NOT quarantined`, d.id);
    }
  }

  // 3. Call / mini-proposal / delivery gates on board opportunities.
  for (const o of ctx.board.opportunities || []) {
    if (["call_due", "called", "interested"].includes(o.stage) && o.call_brief) {
      const g = callGate(o.call_brief);
      if (!g.passed) add("call_gate", "HIGH", `Call brief incomplete: ${g.reasons.join(",")}`, o.id);
    }
    if (o.mini_proposal && o.mini_proposal.status === "pending_founder_approval") {
      const g = miniProposalGate(o.mini_proposal);
      if (!g.passed) add("mini_proposal_gate", "HIGH", `Mini proposal incomplete: ${g.reasons.join(",")}`, o.id);
    }
    if (["won", "delivery_started", "active", "renewal_candidate"].includes(o.stage)) {
      const g = deliveryGate(o.delivery || {});
      if (!g.passed) add("delivery_gate", "CRITICAL", `Delivering/active without: ${g.reasons.join(",")}`, o.id);
    }
  }

  // 4. No secrets in generated reports.
  for (const r of generatedReports) {
    if (containsSecret(r.content)) add("secrets", "CRITICAL", `Secret-like token in report ${r.name}`, r.name);
  }

  const critical = findings.filter((f) => f.severity === "CRITICAL");
  const high = findings.filter((f) => f.severity === "HIGH");
  return { findings, critical, high, injectionContained };
}

// ── Markdown helpers ─────────────────────────────────────────────────────────
export function writeReport(relPath, content) {
  const full = path.join(REPORTS, relPath);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, content, "utf-8");
  return full;
}

export { DATA, REPORTS };
