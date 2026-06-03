#!/usr/bin/env node
/**
 * Dealix — Maximum Business Operating Factory: validation harness.
 *
 * Pure Node (no dependencies). Validates the account-intelligence factory:
 *   - all JSON schemas parse
 *   - every account pack has the required fields, valid enums, and ONE of the five systems
 *   - recommended_system maps to a valid contact role (Role Targeting Matrix)
 *   - L0/L1 packs use hedged ("likely / غالبًا / قد") language
 *   - no guaranteed claims in generated email/proposal copy
 *   - missing contacts are handled gracefully (no invented names/phones/emails required)
 *   - mini proposals carry a starter price and approval_required = true
 *   - cash-priority component weights sum to the total
 *   - founder daily command contains every required section
 *   - security docs treat external content as untrusted; privacy docs cover minimization + do-not-contact
 *
 * Exit code 0 = all checks passed, 1 = at least one failure. Safe to run in CI.
 *
 * Usage: node scripts/account-factory-check.mjs   (or: npm run factory:check)
 */
import { readFileSync, existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const p = (...x) => resolve(ROOT, ...x);

// ── canonical contracts ────────────────────────────────────────────────
const SYSTEMS = [
  "Revenue Operating System",
  "Executive Command OS",
  "Follow-up Recovery OS",
  "WhatsApp Client OS",
  "Proposal & Proof OS",
];
const EVIDENCE = ["L0", "L1", "L2", "L3", "L4"];
const CONFIDENCE = ["C0", "C1", "C2", "C3", "C4"];
const RISK = ["low", "medium", "high"];

// recommended_system -> allowed role keywords (case-insensitive substring match)
const ROLE_MATRIX = {
  "Revenue Operating System": ["head of sales", "sales", "founder", "gm", "general manager", "marketing"],
  "Executive Command OS": ["founder", "ceo", "general manager", "gm", "operations", "owner"],
  "Follow-up Recovery OS": ["sales", "marketing", "founder"],
  "WhatsApp Client OS": ["operations", "customer service", "customer care", "support", "founder"],
  "Proposal & Proof OS": ["founder", "partner", "bd", "business development", "sales lead", "sales"],
};

const HEDGES = ["غالب", "قد ", "يبدو", "محتمل", "ربما", "يُحتمل", "likely", "probably", "may "];

const PACK_REQUIRED = [
  "id", "company_name", "country", "sector", "likely_decision_maker_role",
  "best_contact_route", "contact_confidence", "likely_pain", "recommended_system",
  "why_this_system", "first_sprint_offer", "email_subject", "email_body",
  "risk_level", "evidence_level", "cash_priority_score", "next_action", "owner", "status",
];

// ── reporting helpers ──────────────────────────────────────────────────
let pass = 0;
const failures = [];
function ok(msg) { pass++; }
function fail(msg) { failures.push(msg); }
function check(cond, msg) { cond ? ok(msg) : fail(msg); }

function readText(rel) {
  const full = p(rel);
  if (!existsSync(full)) return null;
  return readFileSync(full, "utf8");
}
function readJsonl(rel) {
  const txt = readText(rel);
  if (txt == null) { fail(`missing data file: ${rel}`); return []; }
  const out = [];
  txt.split("\n").forEach((line, i) => {
    const t = line.trim();
    if (!t) return;
    try { out.push(JSON.parse(t)); }
    catch (e) { fail(`${rel}:${i + 1} invalid JSON — ${e.message}`); }
  });
  return out;
}

// no-guarantee detector: ignores negated disclaimers ("لا نضمن", "لا نعد", "بدون ضمان")
function hasGuaranteeClaim(text) {
  if (!text) return false;
  const cleaned = String(text)
    .replace(/لا\s+نضمن/g, "")
    .replace(/لا\s+نعد/g, "")
    .replace(/بدون\s+ضمان/g, "")
    .replace(/دون\s+ضمان/g, "");
  return /نضمن|مضمون|نضاعف\s+مبيعات|\bguarantee/i.test(cleaned) || /10x/i.test(cleaned);
}

// ── 1. schemas parse ───────────────────────────────────────────────────
const SCHEMAS = [
  "schemas/account_intelligence_pack.schema.json",
  "schemas/contact_discovery.schema.json",
  "schemas/contact_channel.schema.json",
  "schemas/account_scoring.schema.json",
  "schemas/mini_proposal.schema.json",
  "schemas/cash_priority_score.schema.json",
];
for (const s of SCHEMAS) {
  const txt = readText(s);
  if (txt == null) { fail(`missing schema: ${s}`); continue; }
  try {
    const j = JSON.parse(txt);
    check(j.title && j.properties, `schema has title+properties: ${s}`);
  } catch (e) { fail(`schema invalid JSON: ${s} — ${e.message}`); }
}

// ── 2. account packs ───────────────────────────────────────────────────
const packs = readJsonl("data/account_intelligence/account_packs.jsonl");
check(packs.length > 0, "account_packs.jsonl has at least one pack");
const packIds = new Set();
for (const a of packs) {
  const id = a.id || "(no-id)";
  for (const f of PACK_REQUIRED) {
    check(a[f] !== undefined && a[f] !== null && a[f] !== "", `${id}: has required field '${f}'`);
  }
  packIds.add(a.id);
  check(SYSTEMS.includes(a.recommended_system), `${id}: recommended_system is one of the five (${a.recommended_system})`);
  check(EVIDENCE.includes(a.evidence_level), `${id}: evidence_level valid (${a.evidence_level})`);
  check(CONFIDENCE.includes(a.contact_confidence), `${id}: contact_confidence valid (${a.contact_confidence})`);
  check(RISK.includes(a.risk_level), `${id}: risk_level valid (${a.risk_level})`);
  check(typeof a.cash_priority_score === "number" && a.cash_priority_score >= 0 && a.cash_priority_score <= 100, `${id}: cash_priority_score in 0..100`);

  // role matrix
  const allowed = ROLE_MATRIX[a.recommended_system] || [];
  const role = String(a.likely_decision_maker_role || "").toLowerCase();
  check(allowed.some((k) => role.includes(k)), `${id}: role '${a.likely_decision_maker_role}' valid for ${a.recommended_system}`);

  // never require invented contacts
  check(a.phone_if_public === null || typeof a.phone_if_public === "string", `${id}: phone_if_public is null or string (not fabricated structure)`);

  // hedge rule for low evidence
  if (a.evidence_level === "L0" || a.evidence_level === "L1") {
    const blob = `${a.likely_pain} ${a.email_body}`;
    check(HEDGES.some((h) => blob.includes(h)), `${id}: L0/L1 copy uses hedged language (likely/غالبًا/قد)`);
  }

  // no guaranteed claims in generated copy
  check(!hasGuaranteeClaim(a.email_body), `${id}: email_body has no guaranteed claim`);
  check(!hasGuaranteeClaim(a.why_this_system), `${id}: why_this_system has no guaranteed claim`);

  // draft-by-default safety
  check(a.status === "draft" || a.status === "approval_queue", `${id}: status is draft/approval_queue (not auto-sent)`);
}

// ── 3. contact discovery / channels (missing contacts handled) ─────────
const discovery = readJsonl("data/contacts/contact_discovery.jsonl");
for (const d of discovery) {
  check(packIds.has(d.account_id), `${d.id}: discovery account_id ${d.account_id} exists`);
  check(CONFIDENCE.includes(d.contact_confidence), `${d.id}: discovery contact_confidence valid`);
  check(Array.isArray(d.sources) && d.sources.length > 0, `${d.id}: discovery has at least one public source`);
  // graceful missing: if confidence is C0/C1 we must NOT carry an invented direct contact
  if (d.contact_confidence === "C0" || d.contact_confidence === "C1") {
    check(!d.email_if_public && !d.phone_if_public, `${d.id}: low-confidence record carries no fabricated direct contact`);
  }
}
const channels = readJsonl("data/contacts/contact_channels.jsonl");
for (const c of channels) {
  check(packIds.has(c.account_id), `${c.id}: channel account_id ${c.account_id} exists`);
  check(c.is_public === true, `${c.id}: channel is_public=true`);
}

// ── 4. mini proposals ──────────────────────────────────────────────────
const proposals = readJsonl("data/proposals/mini_proposals.jsonl");
check(proposals.length > 0, "mini_proposals.jsonl has at least one proposal");
for (const m of proposals) {
  check(packIds.has(m.account_id), `${m.id}: proposal account_id ${m.account_id} exists`);
  check(typeof m.starter_price_sar === "number" && m.starter_price_sar > 0, `${m.id}: starter_price_sar present and > 0`);
  check(m.approval_required === true, `${m.id}: approval_required === true`);
  check(Array.isArray(m.deliverables) && m.deliverables.length >= 3, `${m.id}: has >= 3 deliverables`);
  check(!!m.expected_first_proof, `${m.id}: has expected_first_proof`);
  check(SYSTEMS.includes(m.recommended_system), `${m.id}: recommended_system valid`);
  check(!hasGuaranteeClaim(m.why_this_system), `${m.id}: proposal copy has no guaranteed claim`);
}

// ── 5. cash priority scores sum correctly ──────────────────────────────
const cps = readJsonl("data/finance/cash_priority_scores.jsonl");
for (const s of cps) {
  check(packIds.has(s.account_id), `cash:${s.account_id}: account exists`);
  const sum = s.ability_to_pay + s.urgency + s.ease_of_delivery + s.upsell_potential + s.contact_availability;
  check(sum === s.total_score, `cash:${s.account_id}: components sum (${sum}) === total_score (${s.total_score})`);
}

// ── 6. founder daily command sections ──────────────────────────────────
const founder = readText("reports/founder/DAILY_SUPER_COMMAND.md");
const FOUNDER_SECTIONS = [
  "Critical Decision", "400 Account Pack", "Contacts Found", "Missing Contacts",
  "Top 100", "Top 20 Send", "Top 30 Call", "Mini Proposals Ready",
  "Proposal Approvals", "Delivery Pipelines", "Delivery Blockers", "Website Leads",
  "Best System", "Best Sector", "Best City", "Cash Opportunity", "Biggest Risk", "Tomorrow Plan",
];
if (founder == null) fail("missing reports/founder/DAILY_SUPER_COMMAND.md");
else for (const sec of FOUNDER_SECTIONS) check(founder.includes(sec), `founder command contains section: ${sec}`);

// ── 7. security + privacy docs ─────────────────────────────────────────
const sec = readText("docs/security/AGENT_SECURITY_GATES_AR.md");
if (sec == null) fail("missing docs/security/AGENT_SECURITY_GATES_AR.md");
else {
  check(/untrusted/i.test(sec) || sec.includes("غير موثوق"), "security doc treats external content as untrusted");
  check(/prompt injection/i.test(sec) || sec.includes("حقن"), "security doc covers prompt injection");
  check(sec.includes("allowlist") || sec.includes("قائمة سماح"), "security doc requires tool allowlist");
}
const priv = readText("docs/privacy/DATA_MINIMIZATION_AND_DO_NOT_CONTACT_AR.md");
if (priv == null) fail("missing docs/privacy/DATA_MINIMIZATION_AND_DO_NOT_CONTACT_AR.md");
else {
  check(/minimization/i.test(priv) || priv.includes("تقليل"), "privacy doc covers data minimization");
  check(/do[\s-]?not[\s-]?contact/i.test(priv) || priv.includes("عدم التواصل"), "privacy doc covers do-not-contact / suppression");
}

// ── summary ────────────────────────────────────────────────────────────
const total = pass + failures.length;
console.log(`\nDealix factory check: ${pass}/${total} checks passed.`);
if (failures.length) {
  console.log(`\n❌ ${failures.length} failure(s):`);
  for (const f of failures) console.log("  - " + f);
  process.exit(1);
}
console.log("✅ All factory checks passed.\n");
