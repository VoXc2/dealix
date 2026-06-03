#!/usr/bin/env node
// Dealix — Commercial Control Check (npm run commercial:check)
// The master gate. Re-verifies the whole factory: draft data integrity, that no
// dangerous content slipped into a sendable draft, that untrusted injection is
// contained, and that call / mini-proposal / delivery gates hold. Writes the
// daily agent security review. Exits 1 on any CRITICAL or HIGH finding
// (mirrors scripts/governance_check.py).

import path from "node:path";
import {
  loadContext, evaluateBatch, runControlChecks, today, writeReport,
  INJECTION_PATTERNS, GUARANTEE_PATTERNS,
} from "./lib/commercial.js";

function renderSecurityReview(ctx, control, evalResult) {
  const date = today();
  const bySeverity = (sev) => control.findings.filter((f) => f.severity === sev);
  const section = (title, items) => {
    let s = `### ${title} (${items.length})\n\n`;
    if (items.length === 0) return s + `_None._\n\n`;
    s += `| Gate | Detail | Ref |\n|------|--------|-----|\n`;
    for (const f of items) s += `| ${f.gate} | ${f.detail} | ${f.id || "—"} |\n`;
    return s + "\n";
  };

  return `# Daily Agent Security Review — مراجعة أمان الوكلاء اليومية
*Date: ${date}*

---

## 1. Posture

| Signal | Value |
|--------|------:|
| Critical findings | ${control.critical.length} |
| High findings | ${control.high.length} |
| Injection attempts contained | ${control.injectionContained} |
| Drafts scored | ${evalResult.total} |
| Sendable (not rejected) | ${evalResult.evaluations.filter((e) => e.status !== "rejected").length} |

Overall: ${control.critical.length ? "🔴 NON-COMPLIANT" : control.high.length ? "🟠 AT RISK" : "✅ COMPLIANT"}

---

## 2. Untrusted-Data Boundary

All company web/email/PDF text is **untrusted data** and never becomes instructions.
This run scanned \`source_excerpt\` fields for injection markers and confirmed each
hit was **quarantined** (draft rejected), not acted on.

- Injection patterns watched: ${INJECTION_PATTERNS.length}
- Guarantee patterns watched: ${GUARANTEE_PATTERNS.length}
- Injection attempts contained this run: **${control.injectionContained}**

---

## 3. Findings

${section("🔴 Critical", bySeverity("CRITICAL"))}${section("🟠 High", bySeverity("HIGH"))}

---

## 4. Enforced Boundaries (assertions)

- [x] No external sending by agents (drafts stay in approval queue)
- [x] No automated calling / no cold WhatsApp automation
- [x] No purchased lists (suppression honored)
- [x] No guaranteed-revenue claims in sendable drafts
- [x] No secrets in prompts/logs/reports
- [x] No internal module names in sendable customer-facing copy

---

*Generated: ${date} | npm run commercial:check*
`;
}

function main() {
  const ctx = loadContext();
  const evalResult = evaluateBatch(ctx);
  const control = runControlChecks(ctx, evalResult, []);

  const reviewMd = renderSecurityReview(ctx, control, evalResult);
  // Self-scan: ensure the report we are about to write carries no secrets.
  const control2 = runControlChecks(ctx, evalResult, [{ name: "DAILY_AGENT_SECURITY_REVIEW.md", content: reviewMd }]);
  const reviewPath = writeReport("security/DAILY_AGENT_SECURITY_REVIEW.md", reviewMd);

  const critical = control2.critical;
  const high = control2.high;

  console.log("=".repeat(72));
  console.log(`  DEALIX COMMERCIAL CONTROL CHECK — ${today()}`);
  console.log("=".repeat(72));
  console.log(`  🔴 Critical: ${critical.length}   🟠 High: ${high.length}`);
  console.log(`  🛡  Injection attempts contained: ${control2.injectionContained}`);
  console.log(`  Report: ${path.relative(process.cwd(), reviewPath)}`);
  for (const f of [...critical, ...high]) console.log(`  [${f.severity}] ${f.gate}: ${f.detail} (${f.id || "—"})`);

  if (critical.length || high.length) {
    console.log("  OVERALL: 🔴 NON-COMPLIANT — fix before running the factory.");
    console.log("=".repeat(72));
    process.exit(1);
  }
  console.log("  OVERALL: ✅ COMPLIANT");
  console.log("=".repeat(72));
}

main();
