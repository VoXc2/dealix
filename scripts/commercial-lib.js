// Dealix Commercial Operating Factory — shared library
// Dependency-free (Node built-ins only). Deterministic scoring + IO helpers.
// Governance principle: AI drafts. Human approves. System logs.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const COMMERCIAL_DIR = path.join(ROOT, "company_os", "commercial");
export const REVENUE_DIR = path.join(ROOT, "company_os", "revenue");
export const REPORTS_DIR = path.join(ROOT, "reports");

export function today() {
  return new Date().toISOString().slice(0, 10);
}

export function loadJson(filePath, fallback = null) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return fallback;
  }
}

// Minimal CSV reader (no embedded commas/quotes in this dataset).
export function loadCsv(filePath) {
  let raw;
  try {
    raw = fs.readFileSync(filePath, "utf8");
  } catch {
    return [];
  }
  const lines = raw.split(/\r?\n/).filter((l) => l.trim().length > 0);
  if (lines.length === 0) return [];
  const headers = lines[0].split(",").map((h) => h.trim());
  return lines.slice(1).map((line) => {
    const cells = line.split(",");
    const row = {};
    headers.forEach((h, i) => (row[h] = (cells[i] ?? "").trim()));
    return row;
  });
}

export function writeFileEnsured(filePath, content) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, content, "utf8");
}

export function loadConfig() {
  const systems = loadJson(path.join(COMMERCIAL_DIR, "systems.json"));
  const rubric = loadJson(path.join(COMMERCIAL_DIR, "draft_scoring_rubric.json"));
  const suppression = loadJson(path.join(COMMERCIAL_DIR, "suppression_list.json"), {
    do_not_contact_companies: [],
    do_not_contact_domains: [],
  });
  if (!systems || !rubric) {
    throw new Error("Missing systems.json or draft_scoring_rubric.json in company_os/commercial/");
  }
  return { systems, rubric, suppression };
}

const lower = (s) => (s || "").toString().toLowerCase();
const includesAny = (haystack, needles) => needles.some((n) => haystack.includes(lower(n)));

// Match free text to a Focus-5 system by counting distinct pain-signal hits.
export function matchSystem(text, systems) {
  const t = lower(text);
  let best = null;
  let bestHits = 0;
  for (const sys of systems.systems) {
    const hits = sys.pain_signals.filter((sig) => t.includes(lower(sig))).length;
    if (hits > bestHits) {
      bestHits = hits;
      best = sys;
    }
  }
  return { system: best, confidence: bestHits };
}

const HEDGE_AR = ["غالبًا", "غالبا", "قد يكون", "في هذا النوع", "عادةً", "عادة", "كثير من", "يكتشف", "يواجه", "تحتاج"];
const CONCRETE_PAIN = ["تضيع", "تسرب", "بطء", "متابعة", "تحويل", "استفسار", "صفقات", "تتعطل", "تأخر", "churn", "pipeline", "conversion"];
const SOFT_CTA = ["نرسل لك", "نقدر نرسل", "نقدر نتواصل", "تهمك", "تهمني", "نقدر نسوي", "أرسل لك", "نقدر نسوي call", "ملخص"];

// Deterministic 100-point score for one outreach draft.
export function scoreDraft(draft, cfg) {
  const { systems, suppression } = cfg;
  const body = draft.draft_body || "";
  const subject = draft.draft_subject || "";
  const blob = `${subject}\n${body}`;
  const lblob = lower(blob);

  // recommended system
  const { system, confidence } = matchSystem(`${draft.pain || ""} ${blob}`, systems);
  const recommended_system = system ? system.id : null;

  // hard-signal detections (shared by gate + risk scoring)
  const hasGuaranteedClaim = includesAny(lblob, systems.guaranteed_claim_phrases);
  const hasPainAsFact = systems.unverified_pain_as_fact_phrases.some((p) => blob.includes(p));
  const hasFakeThread = systems.fake_thread_prefixes.some((p) => subject.trim().startsWith(p));
  const leakedModule = systems.internal_module_names.find((m) => blob.includes(m)) || null;
  const suppressed =
    (suppression.do_not_contact_companies || []).some((c) => lower(draft.company) === lower(c)) ||
    (suppression.do_not_contact_domains || []).some((d) => lblob.includes(lower(d)));

  const hasNameSlot = body.includes("[الاسم]") || body.includes("[Name]");
  const hasQuestion = body.includes("؟") || body.includes("?");
  const hasSoftCta = SOFT_CTA.some((c) => body.includes(c));
  const hasCta = hasQuestion || hasSoftCta;
  const concretePain = CONCRETE_PAIN.filter((k) => lblob.includes(lower(k))).length;
  const hedged = HEDGE_AR.some((h) => blob.includes(h));
  const polite = blob.includes("السلام عليكم") || lblob.includes("hello");
  const valueWords = ["proof", "خطة", "نظام", "تحليل", "report"].filter((w) => lblob.includes(lower(w))).length;

  // evidence level: we know website (L1); specific stated pain bumps to L2
  const evidence_level = draft.pain && draft.pain.trim().length > 0 ? "L2" : "L1";

  // client need card present when we have a pain + a recommended system
  const client_need_card = recommended_system && draft.pain ? {
    company: draft.company,
    likely_pain: draft.pain,
    recommended_system,
    evidence_level,
    hedged,
  } : null;

  // ---- dimension scores ----
  const personalization = Math.min(25, (hasNameSlot ? 8 : 0) + (concretePain > 0 ? 9 : 0) + (draft.decision_maker ? 8 : 0));
  const pain_clarity = Math.min(20, (draft.pain ? 8 : 0) + (concretePain > 0 ? 7 : 0) + (hedged && !hasPainAsFact ? 5 : 0));
  const system_fit = Math.min(20, (recommended_system ? 10 : 0) + (confidence >= 2 ? 5 : confidence === 1 ? 2 : 0) + (confidence >= 1 ? 5 : 0));
  const cta_clarity = Math.min(15, (hasQuestion ? 8 : 0) + (hasSoftCta ? 7 : 0));
  let risk_safety = 10;
  if (hasGuaranteedClaim) risk_safety -= 10;
  if (hasFakeThread) risk_safety -= 5;
  if (hasPainAsFact) risk_safety -= 5;
  if (leakedModule) risk_safety -= 10;
  if (suppressed) risk_safety -= 10;
  risk_safety = Math.max(0, risk_safety);
  let tone_quality = 6 + (polite ? 2 : 0) + (valueWords > 0 ? 2 : 0);
  if (/[A-Z]{6,}/.test(body) || body.includes("!!!")) tone_quality -= 3;
  tone_quality = Math.max(0, Math.min(10, tone_quality));

  const total = personalization + pain_clarity + system_fit + cta_clarity + risk_safety + tone_quality;

  // ---- email gate (hard pass/fail) ----
  const gate_fails = [];
  if (!client_need_card) gate_fails.push("no Client Need Card");
  if (!recommended_system) gate_fails.push("no recommended_system");
  if (!hasCta) gate_fails.push("no CTA");
  if (hasGuaranteedClaim) gate_fails.push("guaranteed claim");
  if (hasFakeThread) gate_fails.push("fake Re/Fwd");
  if (hasPainAsFact) gate_fails.push("unverified pain written as fact");
  if (leakedModule) gate_fails.push(`internal module name leaked (${leakedModule})`);
  if (suppressed) gate_fails.push("suppression hit");
  const gate_pass = gate_fails.length === 0;

  // status from thresholds
  let status = "rejected";
  if (total >= 85) status = "top_priority";
  else if (total >= 75) status = "approval_queue";
  else if (total >= 65) status = "needs_rewrite";

  const risk_level = risk_safety >= 8 ? "low" : risk_safety >= 5 ? "medium" : "high";

  // Top-100 eligibility
  const top_eligible = gate_pass && total >= 75 && risk_level !== "high";

  return {
    id: draft.id,
    company: draft.company,
    recommended_system,
    recommended_system_name: system ? system.customer_facing_name_en : null,
    evidence_level,
    client_need_card: !!client_need_card,
    scores: { personalization, pain_clarity, system_fit, cta_clarity, risk_safety, tone_quality },
    total,
    status,
    risk_level,
    gate_pass,
    gate_fails,
    top_eligible,
  };
}

export function statusEmoji(status) {
  return { top_priority: "🟢", approval_queue: "🟡", needs_rewrite: "🟠", rejected: "🔴" }[status] || "⚪";
}

export function systemById(systems, id) {
  return systems.systems.find((s) => s.id === id) || null;
}
