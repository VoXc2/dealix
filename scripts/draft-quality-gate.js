// draft-quality-gate.js
// Scores every staged email draft against the 100-point rubric and gates drafts
// that reach 75+ into the Top 100 approval queue. Writes:
//   reports/outreach/SYSTEM_EMAIL_DRAFTS_REVIEW.md  (all drafts + breakdown)
//   reports/outreach/TOP_100_SYSTEM_APPROVAL_QUEUE.md  (>=75, capped at 100)
// Nothing here sends anything — the queue is for human approval only.
import {
  loadRegistry, systemMap, readJsonl, writeReport, nowISODate,
  scoreDraft, QUALITY_GATE_MIN, containsBannedClaim,
} from './lib/commercial.js'

function main() {
  const registry = loadRegistry()
  const map = systemMap(registry)
  const { records: drafts, errors } = readJsonl('data/outreach/email_drafts.jsonl')
  const date = nowISODate()

  const scored = drafts.map((d) => {
    const res = scoreDraft(d, map.get(d.recommended_system))
    const banned = containsBannedClaim(d.email_body) || containsBannedClaim(d.subject)
    return { draft: d, ...res, banned }
  })
  scored.sort((a, b) => b.score - a.score)

  const passed = scored.filter((s) => s.score >= QUALITY_GATE_MIN && !s.banned).slice(0, 100)
  const failed = scored.filter((s) => s.score < QUALITY_GATE_MIN || s.banned)

  // --- Full review report ---
  const rev = []
  rev.push('# System Email Drafts — Quality Review')
  rev.push(`*Generated: ${date} — by scripts/draft-quality-gate.js*`)
  rev.push('')
  rev.push(`Scored **${scored.length}** drafts. Gate = **${QUALITY_GATE_MIN}/100**. Passed: **${passed.length}**, below gate: **${failed.length}**.`)
  if (errors.length) rev.push(`\n> ⚠️ ${errors.length} malformed line(s) in data/outreach/email_drafts.jsonl were skipped.`)
  rev.push('')
  rev.push('| Company | System | Score | Pers | Pain | Fit | CTA | Risk | Tone | Gate |')
  rev.push('|---------|--------|------:|----:|----:|----:|----:|----:|----:|:----:|')
  for (const s of scored) {
    const b = s.breakdown
    const gate = s.banned ? '🚫 claim' : s.score >= QUALITY_GATE_MIN ? '✅' : '❌'
    rev.push(
      `| ${s.draft.company || '—'} | ${s.system} | ${s.score} | ${b.personalization} | ${b.pain_clarity} | ${b.system_fit} | ${b.cta_clarity} | ${b.risk_safety} | ${b.tone_quality} | ${gate} |`,
    )
  }
  rev.push('')
  rev.push('Rubric: Personalization 25 · Pain clarity 20 · System fit 20 · CTA clarity 15 · Risk safety 10 · Tone 10.')
  writeReport('reports/outreach/SYSTEM_EMAIL_DRAFTS_REVIEW.md', rev.join('\n'))

  // --- Top 100 approval queue ---
  const q = []
  q.push('# Top 100 System Approval Queue')
  q.push(`*Generated: ${date} — by scripts/draft-quality-gate.js*`)
  q.push('')
  q.push(`**${passed.length}** drafts passed the ${QUALITY_GATE_MIN}/100 gate and await founder approval.`)
  q.push('')
  q.push('> كل عنصر هنا **مسودة** بانتظار موافقة المؤسس. لا إرسال خارجي افتراضيًا.')
  q.push('')
  q.push('| # | Company | System | Score | Subject | Evidence | Approval |')
  q.push('|--:|---------|--------|------:|---------|:--------:|:--------:|')
  passed.forEach((s, i) => {
    const subj = (s.draft.subject || '').replace(/\|/g, '/')
    q.push(`| ${i + 1} | ${s.draft.company || '—'} | ${s.system} | ${s.score} | ${subj} | ${s.draft.evidence_level || '—'} | ${s.draft.approval_status || 'draft'} |`)
  })
  if (!passed.length) q.push('| — | _no drafts above gate yet_ | | | | | |')
  q.push('')
  q.push('Approval is manual. Approving a draft does **not** send it; sending is a separate, deliberate step.')
  writeReport('reports/outreach/TOP_100_SYSTEM_APPROVAL_QUEUE.md', q.join('\n'))

  console.log(`[quality-gate] scored=${scored.length} passed=${passed.length} below=${failed.length}`)
  if (scored.some((s) => s.banned)) {
    console.warn('[quality-gate] WARNING: drafts containing guarantee-style claims were excluded from the queue.')
  }
}

main()
