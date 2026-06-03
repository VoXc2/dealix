// commercial-daily-brief.js
// Generates the founder's Daily Super Command from the live data files.
// Answers, in one page: how many drafts, the Top 100, who needs a call,
// how many mini proposals are ready, who is interested, open deliveries,
// blockers, and the single most important decision today.
// Writes reports/founder/DAILY_SUPER_COMMAND.md.
import {
  loadRegistry, systemMap, readJsonl, writeReport, nowISODate,
  scoreDraft, QUALITY_GATE_MIN,
} from './lib/commercial.js'

function main() {
  const registry = loadRegistry()
  const map = systemMap(registry)
  const date = nowISODate()

  const drafts = readJsonl('data/outreach/email_drafts.jsonl').records
  const passed = drafts
    .map((d) => ({ d, s: scoreDraft(d, map.get(d.recommended_system)).score }))
    .filter((x) => x.s >= QUALITY_GATE_MIN)

  const briefs = readJsonl('data/acquisition/call_briefs.jsonl').records
  const minis = readJsonl('data/acquisition/mini_proposals.jsonl').records
  const miniReady = minis.filter((m) => (m.approval_status || 'pending') !== 'rejected')
  const miniApproved = minis.filter((m) => m.approval_status === 'approved')

  const pipelines = readJsonl('data/delivery/pipelines.jsonl').records
  const interested = pipelines.filter((p) => ['interested', 'qualified'].includes(p.state))
  const openDelivery = pipelines.filter((p) =>
    ['won', 'intake_required', 'delivery_started', 'first_output_ready', 'client_review'].includes(p.state),
  )
  const blockers = []
  for (const p of pipelines) {
    if (Array.isArray(p.blockers)) for (const b of p.blockers) blockers.push(`${p.company}: ${b}`)
    if (p.state === 'intake_required' && !p.required_inputs_received) blockers.push(`${p.company}: بانتظار المدخلات الأساسية قبل بدء التسليم`)
  }
  const renewal = pipelines.filter((p) => p.state === 'renewal_candidate')

  // Decide the single most important decision today (simple priority ladder).
  let topDecision
  if (blockers.length) topDecision = `أزل عائق التسليم: ${blockers[0]}`
  else if (miniApproved.length) topDecision = `أرسل العرض المعتمد: ${miniApproved[0].company}`
  else if (miniReady.length) topDecision = `راجع واعتمد Mini Proposal: ${miniReady[0].company}`
  else if (briefs.length) topDecision = `نفّذ مكالمة المتابعة: ${briefs[0].company}`
  else if (passed.length) topDecision = `اعتمد دفعة من Top 100 (${passed.length} جاهزة للمراجعة)`
  else topDecision = 'جهّز مسودات اليوم وعبّئ خط الأنابيب'

  const l = []
  l.push('# Founder Daily Super Command')
  l.push(`*${date} — by scripts/commercial-daily-brief.js*`)
  l.push('')
  l.push('## أهم قرار اليوم')
  l.push(`> **${topDecision}**`)
  l.push('')
  l.push('## اللوحة اليومية')
  l.push('')
  l.push('| السؤال | الرقم |')
  l.push('|--------|------:|')
  l.push(`| كم draft مخزّن؟ | ${drafts.length} |`)
  l.push(`| كم تجاوز بوابة الجودة (Top 100)؟ | ${passed.length} |`)
  l.push(`| من يحتاج اتصال (Call Briefs)؟ | ${briefs.length} |`)
  l.push(`| كم Mini Proposal بانتظار/معتمد؟ | ${miniReady.length} (معتمد: ${miniApproved.length}) |`)
  l.push(`| كم عميل مهتم/مؤهل؟ | ${interested.length} |`)
  l.push(`| كم تسليم مفتوح؟ | ${openDelivery.length} |`)
  l.push(`| كم عائق؟ | ${blockers.length} |`)
  l.push(`| مرشحون للتجديد؟ | ${renewal.length} |`)
  l.push('')

  if (briefs.length) {
    l.push('## مكالمات اليوم')
    for (const b of briefs.slice(0, 8)) {
      l.push(`- **${b.company}** (${b.contact_role || 'جهة الاتصال'}) — ${map.get(b.recommended_system)?.name_ar || b.recommended_system}: ${b.call_objective || ''}`)
    }
    l.push('')
  }
  if (miniReady.length) {
    l.push('## عروض بانتظار قرار')
    for (const m of miniReady.slice(0, 8)) {
      l.push(`- **${m.company}** — ${m.title || ''} (${m.starter_price || ''}) — الحالة: ${m.approval_status || 'pending'}`)
    }
    l.push('')
  }
  if (openDelivery.length) {
    l.push('## تسليمات مفتوحة')
    for (const p of openDelivery.slice(0, 10)) {
      l.push(`- **${p.company}** — ${map.get(p.recommended_system)?.name_ar || p.recommended_system} — الحالة: \`${p.state}\``)
    }
    l.push('')
  }
  if (blockers.length) {
    l.push('## عوائق')
    for (const b of blockers.slice(0, 10)) l.push(`- ${b}`)
    l.push('')
  }
  l.push('---')
  l.push('سياسة ثابتة: لا إرسال خارجي افتراضيًا، كل draft مسودة حتى الموافقة، لا اتصال آلي، لا أتمتة واتساب/لينكدإن باردة.')

  const out = writeReport('reports/founder/DAILY_SUPER_COMMAND.md', l.join('\n'))
  console.log(`[daily-brief] drafts=${drafts.length} top100=${passed.length} calls=${briefs.length} minis=${miniReady.length} delivery=${openDelivery.length} blockers=${blockers.length} → ${out}`)
}

main()
