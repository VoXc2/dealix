// commercial-daily-plan.js
// Builds the daily 400-draft production plan from the systems registry and
// compares it against the drafts currently staged in data/outreach/email_drafts.jsonl.
// Writes reports/outreach/DAILY_400_SYSTEM_DRAFT_PRODUCTION.md.
//
// Hard rule: 400 DRAFTS/day is the target. 400 SENDS/day is NOT enabled.
import { loadRegistry, readJsonl, writeReport, nowISODate, pct } from './lib/commercial.js'

function main() {
  const registry = loadRegistry()
  const { records: drafts, missing } = readJsonl('data/outreach/email_drafts.jsonl')
  const date = nowISODate()

  const bySystem = new Map()
  for (const d of drafts) {
    bySystem.set(d.recommended_system, (bySystem.get(d.recommended_system) || 0) + 1)
  }

  const rows = registry.systems
    .slice()
    .sort((a, b) => a.order - b.order)
    .map((s) => {
      const target = s.ops.drafts_per_day
      const actual = bySystem.get(s.id) || 0
      return { name: s.name_en, target, actual, gap: target - actual }
    })

  const totalTarget = rows.reduce((a, r) => a + r.target, 0)
  const totalActual = rows.reduce((a, r) => a + r.actual, 0)

  const lines = []
  lines.push('# Daily 400-Draft Production Plan')
  lines.push(`*Generated: ${date} — by scripts/commercial-daily-plan.js*`)
  lines.push('')
  lines.push('> الهدف: **400 draft يوميًا**. الإرسال (sends) **غير مُفعّل افتراضيًا**؛ كل draft يبقى مسودة حتى موافقة المؤسس.')
  lines.push('')
  lines.push('## Per-system distribution')
  lines.push('')
  lines.push('| System | Target/day | Staged | Gap | Coverage |')
  lines.push('|--------|-----------:|-------:|----:|---------:|')
  for (const r of rows) {
    lines.push(`| ${r.name} | ${r.target} | ${r.actual} | ${r.gap > 0 ? r.gap : 0} | ${pct(r.actual, r.target)} |`)
  }
  lines.push(`| **Total** | **${totalTarget}** | **${totalActual}** | **${Math.max(totalTarget - totalActual, 0)}** | **${pct(totalActual, totalTarget)}** |`)
  lines.push('')
  lines.push('## Pipeline per draft')
  lines.push('')
  lines.push('```')
  lines.push('Company Search → Company Intelligence Pack → Client Need Card →')
  lines.push('Recommended System → Email Draft → Quality Score → Top 100 Queue')
  lines.push('```')
  lines.push('')
  lines.push('## Notes')
  lines.push('- المخرج الكامل (400) يُنتج خارج هذا التقرير عبر مولّد المسودات؛ هنا نعرض الخطة والمخزون الحالي.')
  lines.push('- العمود "Staged" يحسب المسودات الموجودة فعليًا في `data/outreach/email_drafts.jsonl`.')
  if (missing) lines.push('- ⚠️ `data/outreach/email_drafts.jsonl` غير موجود بعد — الأرقام الفعلية صفر.')
  lines.push('- لا إرسال خارجي افتراضيًا، ولا قوائم مشتراة، ولا Re:/Fwd: مزيفة.')

  const out = writeReport('reports/outreach/DAILY_400_SYSTEM_DRAFT_PRODUCTION.md', lines.join('\n'))
  console.log(`[daily-plan] target=${totalTarget} staged=${totalActual} → ${out}`)
}

main()
