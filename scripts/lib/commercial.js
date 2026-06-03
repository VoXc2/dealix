/**
 * Dealix Commercial OS — shared library
 *
 * Pure ESM, zero external dependencies. Loads the company_os data layer and
 * provides the safety primitives shared by every commercial:* script:
 *
 *   - draft quality gate (no guaranteed claims, no fake Re:/Fwd:, offer
 *     mapping, suppression, PII)
 *   - approval / dry-run guards
 *   - data loaders for the revenue + governance files
 *
 * Hard rules enforced here (see README "Safety model"):
 *   - SEND is never enabled by default. Drafts are produced, never sent.
 *   - Every outbound item is approval-gated.
 *   - Suppressed recipients can never be send-ready.
 *   - No guaranteed-revenue or overclaim language is allowed in a draft.
 */

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));

/** Repository root (two levels up from scripts/lib). */
export const ROOT = resolve(__dirname, "..", "..");

/** External sending is disabled unless explicitly and dangerously overridden. */
export const SEND_ENABLED = process.env.DEALIX_SEND_ENABLED === "true";
export const DRY_RUN = !SEND_ENABLED;

// ---------------------------------------------------------------------------
// Data loaders
// ---------------------------------------------------------------------------

export function readText(relPath) {
  return readFileSync(resolve(ROOT, relPath), "utf-8");
}

export function loadJSON(relPath, fallback = null) {
  try {
    return JSON.parse(readText(relPath));
  } catch {
    return fallback;
  }
}

export function loadJSONL(relPath) {
  let raw;
  try {
    raw = readText(relPath);
  } catch {
    return [];
  }
  return raw
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      try {
        return JSON.parse(line);
      } catch {
        return null;
      }
    })
    .filter(Boolean);
}

/** Minimal, dependency-free CSV reader (handles simple quoted fields). */
export function loadCSV(relPath) {
  let raw;
  try {
    raw = readText(relPath);
  } catch {
    return [];
  }
  const lines = raw.split(/\r?\n/).filter((l) => l.length > 0);
  if (lines.length === 0) return [];
  const header = splitCsvLine(lines[0]);
  return lines.slice(1).map((line) => {
    const cells = splitCsvLine(line);
    const row = {};
    header.forEach((key, i) => {
      row[key] = cells[i] ?? "";
    });
    return row;
  });
}

function splitCsvLine(line) {
  const out = [];
  let cur = "";
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') {
        cur += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === "," && !inQuotes) {
      out.push(cur);
      cur = "";
    } else {
      cur += ch;
    }
  }
  out.push(cur);
  return out.map((c) => c.trim());
}

export const loadOutreachQueue = () =>
  loadJSON("company_os/revenue/outreach_queue.json", { queue: [] });
export const loadApprovalQueue = () =>
  loadJSON("company_os/governance/approval_queue.json", []);
export const loadLedger = () =>
  loadJSONL("company_os/governance/ai_action_ledger.jsonl");
export const loadProposals = () =>
  loadJSON("company_os/revenue/proposals.json", { templates: [] });
export const loadPipeline = () =>
  loadJSON("company_os/revenue/pipeline.json", { counts: {}, value_sar: {} });
export const loadFollowups = () =>
  loadJSON("company_os/revenue/followups.json", { followups: [] });
export const loadProspects = () => loadCSV("company_os/revenue/prospects.csv");
export const loadSuppressionList = () =>
  loadJSON("company_os/governance/suppression_list.json", { suppressed: [] });

// ---------------------------------------------------------------------------
// Safety primitives
// ---------------------------------------------------------------------------

/**
 * Overclaim / guaranteed-result language. Outbound must never promise
 * guaranteed revenue or risk-free results. Arabic + English.
 */
export const GUARANTEED_CLAIM_PATTERNS = [
  /نضمن/, // "we guarantee"
  /مضمون(?:ة|ه)?/, // "guaranteed"
  /نتائج\s+مضمونة/, // "guaranteed results"
  /زيادة\s+مضمونة/, // "guaranteed increase"
  /بدون\s+مخاطرة/, // "no risk / risk-free"
  /نضاعف\b/, // "we double"
  /مضاعفة\s+(?:المبيعات|الإيرادات|الأرباح)/, // "double sales/revenue/profit"
  /\bguarantee(?:d|s)?\b/i,
  /\brisk[-\s]?free\b/i,
  /\b\d+\s?x\s+(?:revenue|sales|growth|roi)\b/i, // "10x revenue"
  /\b(?:double|triple|quadruple)\s+your\s+(?:revenue|sales|leads)\b/i,
];

/** Subjects that fake a prior thread (deceptive). */
export const FAKE_REPLY_SUBJECT_PATTERNS = [
  /^\s*re\s*:/i,
  /^\s*fwd?\s*:/i,
  /^\s*رد\s*:/,
  /^\s*إعادة\s+توجيه\s*:/,
];

/** Rough PII detectors — recipient PII should not be baked into a template. */
const EMAIL_RE = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}/i;
const PHONE_RE = /(?:\+?9665\d{8}|\b05\d{8}\b)/; // KSA mobile shapes

export function detectGuaranteedClaims(text = "") {
  return GUARANTEED_CLAIM_PATTERNS.filter((re) => re.test(text)).map((re) =>
    re.toString(),
  );
}

export function isFakeReplySubject(subject = "") {
  return FAKE_REPLY_SUBJECT_PATTERNS.some((re) => re.test(subject));
}

/** Canonical offer keywords derived from the proposal catalog + known names. */
export function knownOfferKeywords(proposals = loadProposals()) {
  const keywords = new Set([
    "Revenue Intelligence Sprint",
    "Sprint",
    "Retainer",
    "Proof Pack",
    "Revenue Ops",
  ]);
  for (const t of proposals.templates ?? []) {
    if (t.name) keywords.add(t.name);
  }
  return [...keywords];
}

export function mentionsKnownOffer(text = "", keywords = knownOfferKeywords()) {
  const lower = text.toLowerCase();
  return keywords.some((k) => lower.includes(k.toLowerCase()));
}

/** Normalize a company name for suppression matching. */
function norm(s = "") {
  return s.trim().toLowerCase();
}

export function isSuppressed(draft, suppression = loadSuppressionList()) {
  const entries = suppression.suppressed ?? [];
  const company = norm(draft.company);
  const body = `${draft.draft_subject ?? ""} ${draft.draft_body ?? ""}`;
  const emailMatch = body.match(EMAIL_RE);
  const email = emailMatch ? norm(emailMatch[0]) : null;
  return entries.find((e) => {
    if (e.company && norm(e.company) === company) return true;
    if (e.email && email && norm(e.email) === email) return true;
    if (e.domain && email && email.endsWith(`@${norm(e.domain)}`)) return true;
    return false;
  });
}

/**
 * Evaluate a single outreach draft against every quality + safety gate.
 * Returns { id, company, pass, failures[], warnings[] }.
 * A draft is send-ready only when there are zero CRITICAL failures AND it is
 * approval-gated AND not suppressed.
 */
export function evaluateDraft(draft, ctx = {}) {
  const suppression = ctx.suppression ?? loadSuppressionList();
  const offerKeywords = ctx.offerKeywords ?? knownOfferKeywords();
  const failures = [];
  const warnings = [];

  const subject = draft.draft_subject ?? "";
  const body = draft.draft_body ?? "";
  const combined = `${subject}\n${body}`;

  // CRITICAL: guaranteed / overclaim language
  const claims = detectGuaranteedClaims(combined);
  if (claims.length > 0) {
    failures.push({
      code: "QG-CLAIM",
      severity: "CRITICAL",
      detail: `Guaranteed/overclaim language: ${claims.join(", ")}`,
    });
  }

  // CRITICAL: fake Re:/Fwd: subject
  if (isFakeReplySubject(subject)) {
    failures.push({
      code: "QG-FAKE-REPLY",
      severity: "CRITICAL",
      detail: `Subject fakes a prior thread: "${subject}"`,
    });
  }

  // CRITICAL: suppressed recipient
  const suppressed = isSuppressed(draft, suppression);
  if (suppressed) {
    failures.push({
      code: "QG-SUPPRESSION",
      severity: "CRITICAL",
      detail: `Recipient is on the suppression list (${suppressed.reason ?? "do_not_contact"})`,
    });
  }

  // CRITICAL: must be approval-gated, never auto-sendable
  const status = draft.status ?? "";
  if (status === "sent" || status === "auto_send" || status === "approved_send") {
    failures.push({
      code: "QG-APPROVAL",
      severity: "CRITICAL",
      detail: `Draft is not approval-gated (status="${status}")`,
    });
  }

  // HIGH: must map to a product/offer in the catalog
  if (!mentionsKnownOffer(combined, offerKeywords)) {
    failures.push({
      code: "QG-OFFER",
      severity: "HIGH",
      detail: "Draft does not map to a known offer in the product catalog",
    });
  }

  // WARNING: personalization signal
  const hasPersonalization =
    /\[الاسم\]|\[name\]/i.test(body) ||
    (draft.company && combined.includes(draft.company)) ||
    (draft.pain && combined.includes(draft.pain));
  if (!hasPersonalization) {
    warnings.push({
      code: "QG-PERSONALIZATION",
      detail: "No personalization token, company, or pain reference found",
    });
  }

  // WARNING: recipient PII baked into the template
  if (EMAIL_RE.test(body) || PHONE_RE.test(body)) {
    warnings.push({
      code: "QG-PII",
      detail: "Draft body contains an email/phone — keep recipient PII out of templates",
    });
  }

  const critical = failures.filter((f) => f.severity === "CRITICAL");
  return {
    id: draft.id ?? null,
    company: draft.company ?? null,
    pass: critical.length === 0 && failures.length === 0,
    sendReady: critical.length === 0 && !suppressed && status !== "sent",
    failures,
    warnings,
  };
}

// ---------------------------------------------------------------------------
// Presentation helpers
// ---------------------------------------------------------------------------

export function today() {
  return new Date().toISOString().slice(0, 10);
}

export function hr(char = "=", n = 72) {
  return char.repeat(n);
}

export function printHeader(title) {
  console.log(hr());
  console.log(`  ${title}`);
  console.log(hr());
  console.log("");
}
