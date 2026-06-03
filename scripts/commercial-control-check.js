// commercial-control-check.js
// Enforces the hard commercial guardrails and writes a control report.
// Exits non-zero if any HARD guardrail is violated, so `npm run commercial:check`
// fails loudly in CI and locally.
import { readFileSync } from 'node:fs'
import { join } from 'node:path'
import {
  ROOT, SYSTEM_IDS, loadRegistry, readJsonl, writeReport, nowISODate,
  containsBannedClaim, listSchemas,
} from './lib/commercial.js'

const fails = [] // hard violations → non-zero exit
const warns = [] // soft issues → reported, no failure
const passes = []

function hard(cond, msg) {
  if (cond) passes.push(msg)
  else fails.push(msg)
}
function soft(cond, msg) {
  if (!cond) warns.push(msg)
}

function main() {
  const date = nowISODate()

  // 1. All schemas parse.
  let schemaOk = 0
  for (const f of listSchemas()) {
    try { JSON.parse(readFileSync(join(ROOT, 'schemas', f), 'utf8')); schemaOk++ }
    catch (e) { fails.push(`schema ${f} is invalid JSON: ${e.message}`) }
  }
  hard(schemaOk > 0, `schemas parse cleanly (${schemaOk} files)`)

  // 2. Registry integrity.
  const registry = loadRegistry()
  hard(registry.systems.length === 5, `registry defines exactly 5 systems (found ${registry.systems.length})`)
  const draftTotal = registry.systems.reduce((a, s) => a + (s.ops?.drafts_per_day || 0), 0)
  hard(draftTotal === registry.daily_draft_total, `daily draft distribution sums to ${registry.daily_draft_total} (found ${draftTotal})`)
  hard(registry.systems.every((s) => s.customer?.starting_price_sar > 0), 'every system has a starting price')

  // 3. No external send enabled by default.
  const sendEnv = (process.env.DEALIX_SEND || process.env.SEND_ENABLED || '').toLowerCase()
  hard(sendEnv !== 'true' && sendEnv !== '1', 'external send is NOT enabled by default (no DEALIX_SEND/SEND_ENABLED=true)')

  // Build suppression set (companies that must not be contacted).
  const suppression = new Set()
  for (const r of readJsonl('data/acquisition/suppression_list.jsonl').records) {
    if (r.company) suppression.add(String(r.company).trim().toLowerCase())
  }
  for (const t of readJsonl('data/acquisition/contact_targets.jsonl').records) {
    if (t.do_not_contact && t.company) suppression.add(String(t.company).trim().toLowerCase())
  }

  // 4. Email drafts: valid system, no auto-send state, no banned claims, suppression respected.
  const drafts = readJsonl('data/outreach/email_drafts.jsonl').records
  const allowedSendReadiness = new Set(['not_ready', 'ready_for_review', 'approved_draft'])
  let badSystem = 0, autoSend = 0, claimDrafts = 0, suppressedHit = 0, notDraftStatus = 0
  for (const d of drafts) {
    if (!SYSTEM_IDS.includes(d.recommended_system)) badSystem++
    if (d.send_readiness && !allowedSendReadiness.has(d.send_readiness)) autoSend++
    if (containsBannedClaim(d.email_body) || containsBannedClaim(d.subject)) claimDrafts++
    if (suppression.has(String(d.company || '').trim().toLowerCase())) suppressedHit++
    if (d.approval_status && !['draft', 'pending', 'approved', 'rejected'].includes(d.approval_status)) notDraftStatus++
  }
  hard(badSystem === 0, `every email draft maps to a known system (${badSystem} bad)`)
  hard(autoSend === 0, `no email draft carries an auto-send readiness state (${autoSend} bad)`)
  hard(claimDrafts === 0, `no email draft contains guarantee-style claims (${claimDrafts} bad)`)
  hard(suppressedHit === 0, `no email draft targets a suppressed / do-not-contact company (${suppressedHit} bad)`)
  hard(notDraftStatus === 0, `every email draft uses an allowed approval_status (${notDraftStatus} bad)`)

  // 5. Company intelligence packs: recommended_system + best_contact_role present and role allowed.
  const packs = readJsonl('data/acquisition/company_intelligence_packs.jsonl').records
  const roleBySystem = new Map(registry.systems.map((s) => [s.id, new Set(s.ops.contact_roles)]))
  let packNoSystem = 0, packNoRole = 0, packRoleMismatch = 0
  for (const p of packs) {
    if (!SYSTEM_IDS.includes(p.recommended_system)) packNoSystem++
    if (!p.best_contact_role) packNoRole++
    else if (roleBySystem.get(p.recommended_system) && !roleBySystem.get(p.recommended_system).has(p.best_contact_role)) packRoleMismatch++
  }
  hard(packNoSystem === 0, `every intelligence pack has a valid recommended_system (${packNoSystem} bad)`)
  hard(packNoRole === 0, `every intelligence pack has a best_contact_role (${packNoRole} bad)`)
  soft(packRoleMismatch === 0, `${packRoleMismatch} intelligence pack(s) use a contact role outside the system's allowed roles`)

  // 6. Call briefs: human-only, must have opening line + questions.
  const briefs = readJsonl('data/acquisition/call_briefs.jsonl').records
  let briefBad = 0
  for (const b of briefs) {
    if (!b.opening_line || !(Array.isArray(b.discovery_questions) && b.discovery_questions.length)) briefBad++
  }
  hard(briefBad === 0, `every call brief has an opening line and discovery questions (${briefBad} bad)`)

  // 7. Mini proposals: approval required, deliverables + starter price present, no claims.
  const minis = readJsonl('data/acquisition/mini_proposals.jsonl').records
  let miniNoApproval = 0, miniNoDeliv = 0, miniNoPrice = 0, miniClaim = 0
  for (const m of minis) {
    if (m.approval_required !== true) miniNoApproval++
    if (!(Array.isArray(m.deliverables) && m.deliverables.length)) miniNoDeliv++
    if (!m.starter_price) miniNoPrice++
    if (containsBannedClaim(JSON.stringify(m))) miniClaim++
  }
  hard(miniNoApproval === 0, `every mini proposal requires founder approval (${miniNoApproval} bad)`)
  hard(miniNoDeliv === 0, `every mini proposal lists deliverables (${miniNoDeliv} bad)`)
  hard(miniNoPrice === 0, `every mini proposal has a starter price (${miniNoPrice} bad)`)
  hard(miniClaim === 0, `no mini proposal contains guarantee-style claims (${miniClaim} bad)`)

  // 8. Delivery: cannot start work without required inputs.
  const pipelines = readJsonl('data/delivery/pipelines.jsonl').records
  const workStates = new Set(['delivery_started', 'first_output_ready', 'client_review', 'accepted', 'weekly_value_report', 'renewal_candidate'])
  let startedNoInputs = 0
  for (const p of pipelines) {
    if (workStates.has(p.state) && p.required_inputs_received !== true) startedNoInputs++
  }
  hard(startedNoInputs === 0, `no delivery pipeline started work without required inputs (${startedNoInputs} bad)`)

  // 9. Weekly value reports: no guarantee-style claims.
  const wvr = readJsonl('data/delivery/weekly_value_reports.jsonl').records
  let wvrClaim = 0
  for (const r of wvr) if (containsBannedClaim(JSON.stringify(r))) wvrClaim++
  hard(wvrClaim === 0, `no weekly value report contains guarantee-style claims (${wvrClaim} bad)`)

  // 10. No secret-like keys leaked into data records.
  const secretKey = /(password|secret|api[_-]?key|token|private[_-]?key|access[_-]?key)/i
  const dataFiles = [
    'data/outreach/email_drafts.jsonl',
    'data/acquisition/company_intelligence_packs.jsonl',
    'data/acquisition/contact_targets.jsonl',
    'data/acquisition/mini_proposals.jsonl',
    'data/delivery/pipelines.jsonl',
  ]
  let secretHits = 0
  for (const f of dataFiles) {
    for (const r of readJsonl(f).records) {
      for (const k of Object.keys(r)) if (secretKey.test(k)) secretHits++
    }
  }
  hard(secretHits === 0, `no secret-like fields present in data records (${secretHits} bad)`)

  // --- Report ---
  const lines = []
  lines.push('# Commercial Control Check')
  lines.push(`*Generated: ${date} — by scripts/commercial-control-check.js*`)
  lines.push('')
  lines.push(`Result: ${fails.length ? '🔴 **FAIL**' : '🟢 **PASS**'} — ${passes.length} passed, ${fails.length} failed, ${warns.length} warnings.`)
  lines.push('')
  if (fails.length) {
    lines.push('## ❌ Hard violations')
    for (const f of fails) lines.push(`- ${f}`)
    lines.push('')
  }
  lines.push('## ✅ Guardrails enforced')
  for (const p of passes) lines.push(`- ${p}`)
  lines.push('')
  if (warns.length) {
    lines.push('## ⚠️ Warnings (non-blocking)')
    for (const w of warns) lines.push(`- ${w}`)
    lines.push('')
  }
  lines.push('## Always-on policy')
  lines.push('- 400 drafts/day required; 400 sends/day not enabled.')
  lines.push('- No external send by default. Every email stays a draft until founder approval.')
  lines.push('- No automated calling. Call briefs are for human callers only.')
  lines.push('- No cold WhatsApp or LinkedIn automation. No purchased lists. No fake Re:/Fwd:.')
  lines.push('- No guaranteed-revenue claims. Public or founder-provided data only. Respect do-not-contact.')
  writeReport('reports/founder/COMMERCIAL_CONTROL_CHECK.md', lines.join('\n'))

  console.log(`[control-check] ${fails.length ? 'FAIL' : 'PASS'} — ${passes.length} ok, ${fails.length} fail, ${warns.length} warn`)
  if (fails.length) {
    for (const f of fails) console.error('  ✗', f)
    process.exit(1)
  }
}

main()
