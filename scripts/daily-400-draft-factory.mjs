#!/usr/bin/env node
// Dealix — Daily 400 Draft Factory
// ---------------------------------
// Generates 400 company-specific cold-email DRAFTS per day across the five
// business operating systems, ranks a Top 100 approval queue, builds Client
// Need Cards, and writes Markdown reports + a machine-readable JSON.
//
// HARD RULES (enforced in code):
//   - 400 drafts/day are produced; 400 sends/day are NOT enabled.
//   - Every draft is approval_status = "pending_approval".
//   - send_readiness is "blocked" unless ALL gates pass:
//       founder approval + domain auth (SPF/DKIM/DMARC) + verified opt-in list.
//   - The seed universe is synthetic and clearly labelled; replace with a real,
//     consented list before any real outreach. No purchased lists.
//
// Usage:
//   node scripts/daily-400-draft-factory.mjs [--date=YYYY-MM-DD]
// Env gates (all default false):
//   FOUNDER_APPROVAL=true DOMAIN_AUTH_READY=true VERIFIED_OPT_IN=true

import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { SYSTEMS, DAILY_TOTAL, getSystemBySlug } from "./lib/systems-data.mjs";
import { buildUniverse } from "./lib/seed-companies.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");

// ---------- args & gates ----------
const args = process.argv.slice(2);
const dateArg = args.find((a) => a.startsWith("--date="));
const DATE = dateArg ? dateArg.split("=")[1] : new Date().toISOString().slice(0, 10);

const GATES = {
  founderApproval: process.env.FOUNDER_APPROVAL === "true",
  domainAuthReady: process.env.DOMAIN_AUTH_READY === "true",
  verifiedOptIn: process.env.VERIFIED_OPT_IN === "true",
};

// ---------- deterministic RNG (mulberry32 seeded by date) ----------
function hashSeed(str) {
  let h = 1779033703 ^ str.length;
  for (let i = 0; i < str.length; i++) {
    h = Math.imul(h ^ str.charCodeAt(i), 3432918353);
    h = (h << 13) | (h >>> 19);
  }
  return h >>> 0;
}
function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rng = mulberry32(hashSeed(`dealix-${DATE}`));

function pseudo01(str) {
  return (hashSeed(str) % 1000) / 1000;
}
const clamp01 = (x) => Math.max(0, Math.min(1, x));

// ---------- email angle per system ----------
const EMAIL_ANGLE = {
  "revenue-operating-system":
    "المشكلة ليست في قلة الفرص، بل في غياب الخطوة التالية لكل فرصة.",
  "follow-up-recovery-os":
    "المشكلة ليست في عدد الاستفسارات، بل في آخر متابعة لم تحدث.",
  "executive-command-os":
    "المشكلة ليست نقص التقارير، بل غياب القرار اليومي الواضح.",
  "whatsapp-client-os":
    "المشكلة ليست في الرد، بل في غياب نظام يحوّل المحادثة إلى خطوة.",
  "proposal-proof-os":
    "المشكلة ليست ضعف الخدمة، بل عرض لا يوضح المشكلة والدليل.",
};

// ---------- build universe & assign systems (fit-aware, exact distribution) ----------
const universe = buildUniverse(rng, DAILY_TOTAL);
let unassigned = [...universe];
const assignments = new Map(); // companyId -> systemSlug

for (const system of SYSTEMS) {
  const ranked = [...unassigned].sort((a, b) => {
    const fa = a.affinity[system.slug] ?? 0;
    const fb = b.affinity[system.slug] ?? 0;
    if (fb !== fa) return fb - fa;
    return b.abilityToPay - a.abilityToPay;
  });
  const chosen = ranked.slice(0, system.dailyCount);
  for (const c of chosen) assignments.set(c.id, system.slug);
  const chosenIds = new Set(chosen.map((c) => c.id));
  unassigned = unassigned.filter((c) => !chosenIds.has(c.id));
}

// ---------- gates -> send readiness ----------
function sendReadiness(draftRisk) {
  const reasons = [];
  if (!GATES.founderApproval) reasons.push("بانتظار موافقة المؤسس");
  if (!GATES.domainAuthReady) reasons.push("توثيق الدومين غير مكتمل (SPF/DKIM/DMARC)");
  if (!GATES.verifiedOptIn) reasons.push("القائمة غير موثّقة/غير موافِقة على التواصل");
  if (draftRisk === "Medium") reasons.push("قطاع حساس يتطلب مراجعة امتثال إضافية");
  return {
    status: reasons.length === 0 ? "ready" : "blocked",
    reasons,
  };
}

// ---------- build drafts ----------
function buildDraft(company) {
  const slug = assignments.get(company.id);
  const system = getSystemBySlug(slug);
  const ctx = {
    company: company.company,
    city: company.city,
    sector: company.sector,
    signal: company.signal,
  };
  const { subject, body } = system.email(ctx);

  const riskLevel = company.riskSensitive ? "Medium" : "Low";
  const evidenceLevel = "inferred"; // synthetic seed -> inferred, never "verified"

  // scoring components (0..1)
  const systemFit = clamp01((company.affinity[slug] ?? 0) / 0.4);
  const painClarity = clamp01(0.6 + 0.4 * systemFit);
  const personalization = clamp01(0.82 + 0.18 * pseudo01(company.signal + company.company));
  const signalStrength = clamp01(0.55 + 0.45 * pseudo01(company.id + company.signal));
  const abilityToPay = company.abilityToPay;
  const lowRisk = company.riskSensitive ? 0.6 : 1.0;

  const score = Math.round(
    (0.22 * systemFit +
      0.18 * painClarity +
      0.16 * personalization +
      0.14 * signalStrength +
      0.16 * abilityToPay +
      0.14 * lowRisk) *
      100,
  );

  const readiness = sendReadiness(riskLevel);

  return {
    company: company.company,
    website: company.website,
    sector: company.sector,
    country: company.country,
    city: company.city,
    signal: company.signal,
    likely_pain: company.likely_pain,
    recommended_system: system.nameAr,
    recommended_system_slug: slug,
    why_this_system: system.whyThisSystem,
    first_mission: system.firstMission,
    proof_angle: system.proofAngle,
    email_angle: EMAIL_ANGLE[slug],
    subject,
    email_body: body,
    cta: system.cta,
    risk_level: riskLevel,
    evidence_level: evidenceLevel,
    approval_status: "pending_approval",
    send_readiness: readiness.status,
    send_blockers: readiness.reasons,
    unsubscribe_required: true,
    unsubscribe_note:
      "يُضاف خيار إلغاء الاشتراك (one-click) عند الإرسال الفعلي للقنوات التسويقية.",
    // meta
    _score: score,
    _scoreBreakdown: {
      system_fit: +systemFit.toFixed(2),
      pain_clarity: +painClarity.toFixed(2),
      personalization: +personalization.toFixed(2),
      signal_strength: +signalStrength.toFixed(2),
      ability_to_pay: +abilityToPay.toFixed(2),
      low_risk: +lowRisk.toFixed(2),
    },
    _synthetic: company.synthetic,
    _source: company.source,
  };
}

const drafts = universe.map(buildDraft);
const ranked = [...drafts].sort((a, b) => b._score - a._score);
const top100 = ranked.slice(0, 100);

// ---------- distribution summary ----------
const distribution = SYSTEMS.map((s) => ({
  nameAr: s.nameAr,
  nameEn: s.nameEn,
  slug: s.slug,
  target: s.dailyCount,
  actual: drafts.filter((d) => d.recommended_system_slug === s.slug).length,
  startingPrice: s.startingPrice,
}));

const readyCount = drafts.filter((d) => d.send_readiness === "ready").length;
const blockedCount = drafts.length - readyCount;

// ---------- writers ----------
function write(relPath, content) {
  const abs = resolve(ROOT, relPath);
  mkdirSync(dirname(abs), { recursive: true });
  writeFileSync(abs, content, "utf8");
  return relPath;
}

const SAFETY_BANNER = [
  "> ⚠️ **بيانات عينة اصطناعية:** الشركات في هذا التقرير مُولّدة للتوضيح والاختبار فقط",
  "> (المصدر: `synthetic-seed`, الدومينات وهمية مثل `sample.example`). استبدلها بقائمة حقيقية",
  "> موافِقة على التواصل قبل أي إرسال. لا قوائم مشتراة.",
  ">",
  "> 🔒 **بوابة الإرسال:** كل المسودات `pending_approval`. الإرسال يتطلب: موافقة المؤسس +",
  "> توثيق الدومين (SPF/DKIM/DMARC) + قائمة موثّقة وموافِقة. **400 مسودة/يوم مفعّلة،",
  "> و400 إرسال/يوم غير مفعّل افتراضيًا.**",
].join("\n");

// --- 1) production report ---
function productionReport() {
  const lines = [];
  lines.push("# تقرير إنتاج المسودات اليومي — Daily 400 Draft Production");
  lines.push("");
  lines.push(`**التاريخ:** ${DATE}`);
  lines.push("");
  lines.push(SAFETY_BANNER);
  lines.push("");
  lines.push("## الملخص");
  lines.push("");
  lines.push(`- إجمالي المسودات المنتجة: **${drafts.length}**`);
  lines.push(`- جاهزة للإرسال (بعد البوابات): **${readyCount}**`);
  lines.push(`- محجوبة عن الإرسال (بانتظار البوابات): **${blockedCount}**`);
  lines.push(`- حالة كل المسودات: \`pending_approval\``);
  lines.push("");
  lines.push("### بوابات الإرسال الحالية");
  lines.push("");
  lines.push("| البوابة | الحالة |");
  lines.push("| --- | --- |");
  lines.push(`| موافقة المؤسس | ${GATES.founderApproval ? "✅ مُفعّلة" : "⛔ غير مُفعّلة"} |`);
  lines.push(`| توثيق الدومين (SPF/DKIM/DMARC) | ${GATES.domainAuthReady ? "✅ جاهز" : "⛔ غير جاهز"} |`);
  lines.push(`| قائمة موثّقة وموافِقة (opt-in) | ${GATES.verifiedOptIn ? "✅ جاهزة" : "⛔ غير جاهزة"} |`);
  lines.push("");
  lines.push("## التوزيع اليومي حسب النظام");
  lines.push("");
  lines.push("| النظام | المستهدف | المنتَج | السعر الافتتاحي |");
  lines.push("| --- | ---: | ---: | ---: |");
  for (const d of distribution) {
    lines.push(`| ${d.nameAr} (${d.nameEn}) | ${d.target} | ${d.actual} | ${d.startingPrice.toLocaleString("en-US")} ريال |`);
  }
  lines.push(`| **الإجمالي** | **${DAILY_TOTAL}** | **${drafts.length}** | — |`);
  lines.push("");
  lines.push("## نماذج مسودات (واحدة لكل نظام)");
  lines.push("");
  for (const system of SYSTEMS) {
    const sample = drafts.find((d) => d.recommended_system_slug === system.slug);
    if (!sample) continue;
    lines.push(`### ${system.nameAr} — ${sample.company}`);
    lines.push("");
    lines.push(`- **القطاع / المدينة:** ${sample.sector} — ${sample.city}`);
    lines.push(`- **الموقع:** ${sample.website}`);
    lines.push(`- **الإشارة (signal):** ${sample.signal}`);
    lines.push(`- **الألم المرجّح:** ${sample.likely_pain}`);
    lines.push(`- **لماذا هذا النظام:** ${sample.why_this_system}`);
    lines.push(`- **أول مهمة:** ${sample.first_mission}`);
    lines.push(`- **زاوية الإثبات:** ${sample.proof_angle}`);
    lines.push(`- **زاوية الإيميل:** ${sample.email_angle}`);
    lines.push(`- **المخاطرة:** ${sample.risk_level} · **مستوى الدليل:** ${sample.evidence_level} · **الدرجة:** ${sample._score}/100`);
    lines.push(`- **حالة الاعتماد:** ${sample.approval_status} · **جاهزية الإرسال:** ${sample.send_readiness} (${sample.send_blockers.join("، ") || "—"})`);
    lines.push("");
    lines.push(`**Subject:** ${sample.subject}`);
    lines.push("");
    lines.push("```text");
    lines.push(sample.email_body);
    lines.push("");
    lines.push(`CTA: ${sample.cta}`);
    lines.push("```");
    lines.push("");
  }
  lines.push("## المخرجات");
  lines.push("");
  lines.push("- `reports/outreach/TOP_100_SYSTEM_APPROVAL_QUEUE.md` — أفضل 100 للمراجعة.");
  lines.push("- `reports/outreach/SYSTEM_BASED_CLIENT_NEED_CARDS.md` — بطاقات احتياج العميل.");
  lines.push("- `company_os/outreach/daily_400_drafts.json` — كل المسودات (400) بصيغة آلية.");
  lines.push("");
  lines.push(`<sub>تم التوليد آليًا بواسطة \`scripts/daily-400-draft-factory.mjs\` — seed: dealix-${DATE}</sub>`);
  return lines.join("\n") + "\n";
}

// --- 2) top 100 queue ---
function top100Report() {
  const lines = [];
  lines.push("# أفضل 100 للمراجعة — Top 100 System Approval Queue");
  lines.push("");
  lines.push(`**التاريخ:** ${DATE}`);
  lines.push("");
  lines.push(SAFETY_BANNER);
  lines.push("");
  lines.push(
    "التصنيف بحسب درجة مركّبة: ملاءمة النظام، وضوح الألم، التخصيص، قوة الإشارة، القدرة على الدفع، وانخفاض المخاطرة.",
  );
  lines.push("");
  lines.push("| # | الدرجة | الشركة | القطاع | المدينة | النظام المقترح | المخاطرة | الاعتماد | الإرسال |");
  lines.push("| ---: | ---: | --- | --- | --- | --- | --- | --- | --- |");
  top100.forEach((d, i) => {
    lines.push(
      `| ${i + 1} | ${d._score} | ${d.company} | ${d.sector} | ${d.city} | ${d.recommended_system} | ${d.risk_level} | ${d.approval_status} | ${d.send_readiness} |`,
    );
  });
  lines.push("");
  lines.push(`<sub>تم التوليد آليًا — seed: dealix-${DATE}</sub>`);
  return lines.join("\n") + "\n";
}

// --- 3) client need cards (top 20 expanded) ---
function clientNeedCardsReport() {
  const lines = [];
  lines.push("# بطاقات احتياج العميل — System-Based Client Need Cards");
  lines.push("");
  lines.push(`**التاريخ:** ${DATE}`);
  lines.push("");
  lines.push(SAFETY_BANNER);
  lines.push("");
  lines.push(
    "أدناه بطاقات احتياج العميل لأفضل 20 شركة. البطاقات الكاملة للـ 400 متاحة في `company_os/outreach/daily_400_drafts.json`.",
  );
  lines.push("");
  top100.slice(0, 20).forEach((d, i) => {
    lines.push(`## ${i + 1}. ${d.company}`);
    lines.push("");
    lines.push(`- **Company:** ${d.company}`);
    lines.push(`- **Website:** ${d.website}`);
    lines.push(`- **Country:** ${d.country}`);
    lines.push(`- **City:** ${d.city}`);
    lines.push(`- **Sector:** ${d.sector}`);
    lines.push(`- **Signal:** ${d.signal}`);
    lines.push(`- **Likely Pain:** ${d.likely_pain}`);
    lines.push(`- **Recommended System:** ${d.recommended_system}`);
    lines.push(`- **Why this system:** ${d.why_this_system}`);
    lines.push(`- **First Mission:** ${d.first_mission}`);
    lines.push(`- **Proof Angle:** ${d.proof_angle}`);
    lines.push(`- **Email Angle:** ${d.email_angle}`);
    lines.push(`- **CTA:** ${d.cta}`);
    lines.push(`- **Risk Level:** ${d.risk_level}`);
    lines.push("");
  });
  lines.push(`<sub>تم التوليد آليًا — seed: dealix-${DATE}</sub>`);
  return lines.join("\n") + "\n";
}

// --- 4) machine JSON ---
function machineJson() {
  return JSON.stringify(
    {
      generated_for: DATE,
      seed: `dealix-${DATE}`,
      total: drafts.length,
      daily_total_target: DAILY_TOTAL,
      gates: GATES,
      send_ready: readyCount,
      send_blocked: blockedCount,
      distribution,
      notice:
        "Synthetic seed data for pipeline demonstration. Replace with a real, consented list before any sending. All drafts are pending_approval.",
      drafts,
    },
    null,
    2,
  );
}

// ---------- emit ----------
const written = [];
written.push(write("reports/outreach/DAILY_400_SYSTEM_DRAFT_PRODUCTION.md", productionReport()));
written.push(write("reports/outreach/TOP_100_SYSTEM_APPROVAL_QUEUE.md", top100Report()));
written.push(write("reports/outreach/SYSTEM_BASED_CLIENT_NEED_CARDS.md", clientNeedCardsReport()));
written.push(write("company_os/outreach/daily_400_drafts.json", machineJson()));

// ---------- console summary ----------
console.log(`Dealix Daily 400 Draft Factory — ${DATE}`);
console.log(`  drafts produced : ${drafts.length} (target ${DAILY_TOTAL})`);
console.log(`  send-ready      : ${readyCount}`);
console.log(`  send-blocked    : ${blockedCount}`);
console.log("  distribution    :");
for (const d of distribution) {
  const ok = d.actual === d.target ? "ok" : "MISMATCH";
  console.log(`    - ${d.nameEn.padEnd(26)} ${d.actual}/${d.target} ${ok}`);
}
console.log("  written:");
for (const w of written) console.log(`    - ${w}`);

// ---------- self-check (fails loudly) ----------
const totalOk = drafts.length === DAILY_TOTAL;
const distOk = distribution.every((d) => d.actual === d.target);
const allPending = drafts.every((d) => d.approval_status === "pending_approval");
const gatedOk = GATES.founderApproval && GATES.domainAuthReady && GATES.verifiedOptIn
  ? true
  : drafts.every((d) => d.send_readiness === "blocked");

if (!totalOk || !distOk || !allPending || !gatedOk) {
  console.error("SELF-CHECK FAILED:", { totalOk, distOk, allPending, gatedOk });
  process.exit(1);
}
console.log("  self-check      : passed");
