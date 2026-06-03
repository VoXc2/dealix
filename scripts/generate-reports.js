// generate-reports.js
// Generates the acquisition, delivery, and founder weekly reports from the live
// data files, so the reporting layer always reflects current data. Read-only
// over data/**, writes Markdown under reports/**. No sending, no side effects.
import { loadRegistry, systemMap, readJsonl, writeReport, nowISODate } from './lib/commercial.js'

const registry = loadRegistry()
const MAP = systemMap(registry)
const date = nowISODate()
const sysName = (id) => MAP.get(id)?.name_ar || id

function table(headers, rows) {
  const head = `| ${headers.join(' | ')} |`
  const sep = `|${headers.map(() => '---').join('|')}|`
  const body = rows.length ? rows.map((r) => `| ${r.join(' | ')} |`).join('\n') : `| ${headers.map(() => '—').join(' | ')} |`
  return [head, sep, body].join('\n')
}

function header(title) {
  return [`# ${title}`, `*Generated: ${date} — by scripts/generate-reports.js*`, ''].join('\n')
}

// ---------- Acquisition ----------
const packs = readJsonl('data/acquisition/company_intelligence_packs.jsonl').records
const needCards = readJsonl('data/acquisition/client_need_cards.jsonl').records
const briefs = readJsonl('data/acquisition/call_briefs.jsonl').records
const minis = readJsonl('data/acquisition/mini_proposals.jsonl').records
const sequences = readJsonl('data/acquisition/follow_up_sequences.jsonl').records
const objections = readJsonl('data/acquisition/objection_responses.jsonl').records

writeReport('reports/acquisition/DAILY_COMPANY_INTELLIGENCE_PACKS.md',
  header('Daily Company Intelligence Packs') +
  `\n**${packs.length}** packs. Public or founder-provided data only; L0/L1 are assumptions, not facts.\n\n` +
  table(['Company', 'Sector', 'System', 'Best contact role', 'Likely pain', 'Risk', 'Evidence'],
    packs.map((p) => [p.company, p.sector || '—', sysName(p.recommended_system), p.best_contact_role || '—', (p.likely_pain || '—'), p.risk_level || '—', p.evidence_level || '—'])))

writeReport('reports/outreach/SYSTEM_BASED_CLIENT_NEED_CARDS.md',
  header('System-Based Client Need Cards') +
  `\n**${needCards.length}** need cards mapped to a single recommended system.\n\n` +
  table(['Company', 'System', 'Likely pain', 'First mission', 'Evidence'],
    needCards.map((c) => [c.company, sysName(c.recommended_system), c.likely_pain || '—', c.first_mission || '—', c.evidence_level || '—'])))

writeReport('reports/acquisition/CALL_FOLLOWUP_QUEUE.md',
  header('Call Follow-up Queue') +
  `\n> مكالمات بشرية فقط — لا اتصال آلي. **${briefs.length}** بطاقة مكالمة.\n\n` +
  table(['Company', 'Contact role', 'System', 'Objective', 'Opening line', 'Next step'],
    briefs.map((b) => [b.company, b.contact_role || '—', sysName(b.recommended_system), b.call_objective || '—', (b.opening_line || '—').slice(0, 60) + '…', b.next_step || '—'])))

writeReport('reports/acquisition/MINI_PROPOSAL_QUEUE.md',
  header('Mini Proposal Queue') +
  `\n> كل عرض يحتاج موافقة المؤسس قبل الإرسال. **${minis.length}** عرض.\n\n` +
  table(['Company', 'Title', 'System', 'Starter price', 'Deliverables', 'Approval'],
    minis.map((m) => [m.company, m.title || '—', sysName(m.recommended_system), m.starter_price || '—', String((m.deliverables || []).length), m.approval_status || 'pending'])))

writeReport('reports/acquisition/EMAIL_TO_CALL_HANDOFF_QUEUE.md',
  header('Email → Call Handoff Queue') +
  `\nالعملاء الذين أُرسل لهم بريد معتمد ويحتاجون مكالمة متابعة بشرية.\n\n` +
  table(['Company', 'System', 'Email sent summary', 'Call objective'],
    briefs.map((b) => [b.company, sysName(b.recommended_system), b.email_sent_summary || '—', b.call_objective || '—'])))

writeReport('reports/acquisition/FOLLOW_UP_SEQUENCE_QUEUE.md',
  header('Follow-up Sequence Queue') +
  `\n> مسودات بريد فقط — لا أتمتة واتساب باردة. **${sequences.length}** تسلسل.\n\n` +
  table(['Sequence', 'System', 'Lead status', 'Channel', 'Steps'],
    sequences.map((s) => [s.sequence_id, sysName(s.recommended_system), s.lead_status || '—', s.channel || '—', String((s.steps || []).length)])))

writeReport('reports/acquisition/OBJECTION_REVIEW.md',
  header('Objection Review') +
  `\n**${objections.length}** اعتراض موثّق مع رد آمن (بلا وعود قاطعة).\n\n` +
  table(['Objection', 'Response', 'Avoid'],
    objections.map((o) => [o.objection, (o.response || '—'), o.avoid || '—'])))

// ---------- Delivery ----------
const pipelines = readJsonl('data/delivery/pipelines.jsonl').records
const wvr = readJsonl('data/delivery/weekly_value_reports.jsonl').records
const gates = readJsonl('data/delivery/acceptance_gates.jsonl').records

const stateOrder = [
  'interested', 'qualified', 'mini_proposal_ready', 'proposal_sent', 'payment_handoff', 'won',
  'intake_required', 'delivery_started', 'first_output_ready', 'client_review', 'accepted',
  'weekly_value_report', 'renewal_candidate',
]
const counts = Object.fromEntries(stateOrder.map((s) => [s, 0]))
for (const p of pipelines) if (counts[p.state] !== undefined) counts[p.state]++

writeReport('reports/delivery/DELIVERY_PIPELINE_STATUS.md',
  header('Delivery Pipeline Status') +
  `\n**${pipelines.length}** engagements across the pipeline.\n\n` +
  '## By state\n\n' +
  table(['State', 'Count'], stateOrder.filter((s) => counts[s] > 0).map((s) => [`\`${s}\``, String(counts[s])])) +
  '\n\n## Engagements\n\n' +
  table(['Company', 'System', 'State', 'Inputs received', 'Price (SAR)'],
    pipelines.map((p) => [p.company, sysName(p.recommended_system), `\`${p.state}\``, p.required_inputs_received ? '✅' : '⏳', String(p.starter_price_sar ?? '—')])))

const blockerRows = []
for (const p of pipelines) {
  for (const b of (p.blockers || [])) blockerRows.push([p.company, `\`${p.state}\``, b])
  if (p.state === 'intake_required' && !p.required_inputs_received) blockerRows.push([p.company, '`intake_required`', 'بانتظار المدخلات الأساسية قبل بدء التسليم'])
}
writeReport('reports/delivery/DELIVERY_BLOCKERS.md',
  header('Delivery Blockers') +
  `\n**${blockerRows.length}** blocker(s). التسليم لا يبدأ قبل اكتمال المدخلات.\n\n` +
  table(['Company', 'State', 'Blocker'], blockerRows))

writeReport('reports/delivery/WEEKLY_VALUE_REPORT_QUEUE.md',
  header('Weekly Value Report Queue') +
  `\n**${wvr.length}** weekly value report(s). Evidence-based, no guaranteed-outcome claims.\n\n` +
  table(['Company', 'System', 'Week of', 'Delivered', 'Renewal signal'],
    wvr.map((r) => [r.company, sysName(r.recommended_system), r.week_of || '—', String((r.delivered_this_week || []).length), r.renewal_signal ? '✅' : '—'])))

writeReport('reports/delivery/DELIVERY_ACCEPTANCE_REVIEW.md',
  header('Delivery Acceptance Review') +
  `\n**${gates.length}** acceptance gate(s). الانتقال إلى accepted يتطلب توقيع العميل.\n\n` +
  table(['Pipeline', 'System', 'Criteria met', 'All met', 'Client sign-off'],
    gates.map((g) => {
      const met = (g.criteria || []).filter((c) => c.met).length
      const total = (g.criteria || []).length
      return [g.pipeline_id, sysName(g.recommended_system), `${met}/${total}`, g.all_met ? '✅' : '⏳', g.client_signed_off ? '✅' : '⏳']
    })))

// ---------- Founder weekly ----------
const interested = pipelines.filter((p) => ['interested', 'qualified'].includes(p.state)).length
const won = pipelines.filter((p) => p.state === 'won').length
const openDelivery = pipelines.filter((p) => ['delivery_started', 'first_output_ready', 'client_review'].includes(p.state)).length
const renewal = pipelines.filter((p) => p.state === 'renewal_candidate').length
const approvedMinis = minis.filter((m) => m.approval_status === 'approved').length

writeReport('reports/founder/WEEKLY_BOARD_REVIEW.md',
  header('Weekly Board Review') +
  '\n## Funnel snapshot\n\n' +
  table(['Metric', 'Value'], [
    ['Intelligence packs', String(packs.length)],
    ['Call briefs ready', String(briefs.length)],
    ['Mini proposals (approved)', `${minis.length} (${approvedMinis})`],
    ['Interested / qualified', String(interested)],
    ['Won', String(won)],
    ['Open delivery', String(openDelivery)],
    ['Renewal candidates', String(renewal)],
  ]) +
  '\n\n## Per-system pipeline weight\n\n' +
  table(['System', 'Engagements'], registry.systems.map((s) => [s.name_ar, String(pipelines.filter((p) => p.recommended_system === s.id).length)])) +
  '\n\n## Standing policy\n' +
  '- لا إرسال خارجي افتراضيًا؛ كل بريد مسودة حتى الموافقة.\n' +
  '- لا اتصال آلي؛ بطاقات المكالمة للبشر فقط.\n' +
  '- لا أتمتة واتساب/لينكدإن باردة؛ لا قوائم مشتراة؛ لا وعود قاطعة.\n')

console.log('[generate-reports] acquisition + delivery + founder weekly reports written.')
