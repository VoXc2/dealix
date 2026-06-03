// Shared helpers for the Dealix commercial machine (daily plan, quality gate,
// control check, daily brief). Pure Node ESM, no dependencies. Reads the
// canonical systems registry from data/systems.json and the operational data
// from data/**/*.jsonl, and writes Markdown reports under reports/.
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from 'node:fs'
import { dirname, resolve, join } from 'node:path'
import { fileURLToPath } from 'node:url'

export const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..')

export const SYSTEM_IDS = [
  'revenue-operating-system',
  'executive-command-os',
  'follow-up-recovery-os',
  'whatsapp-client-os',
  'proposal-proof-os',
]

// Phrases that imply guaranteed outcomes — banned in every draft, proposal, and
// report. Kept deliberately broad; better to flag a borderline phrase for human
// review than to let a guarantee slip through.
export const BANNED_CLAIM_PATTERNS = [
  /نضمن/, /مضمون/, /ضمان\s+(?:الإيراد|الأرباح|النتيجة|النتائج)/, /نضاعف/, /مضاعفة\s+الأرباح/,
  /أرباح\s+مضمونة/, /عائد\s+مضمون/, /\b100%\b/, /\bguarantee/i, /\bguaranteed/i, /\bdouble your\b/i,
]

// Draft quality rubric (total 100). Drafts must reach QUALITY_GATE_MIN to enter
// the Top 100 approval queue.
export const QUALITY_GATE_MIN = 75
export const RUBRIC = {
  personalization: 25,
  pain_clarity: 20,
  system_fit: 20,
  cta_clarity: 15,
  risk_safety: 10,
  tone_quality: 10,
}

const CTA_KEYWORDS = ['مكالمة', 'احجز', 'تشخيص', 'نرسل', 'رد', 'موعد', 'اتصال', 'جرب', 'ابدأ']

export function loadRegistry() {
  return JSON.parse(readFileSync(join(ROOT, 'data', 'systems.json'), 'utf8'))
}

export function systemMap(registry = loadRegistry()) {
  const map = new Map()
  for (const s of registry.systems) map.set(s.id, s)
  return map
}

// Read a JSONL file tolerantly. Returns { records, errors, missing }.
export function readJsonl(relPath) {
  const abs = join(ROOT, relPath)
  if (!existsSync(abs)) return { records: [], errors: [], missing: true }
  const records = []
  const errors = []
  const lines = readFileSync(abs, 'utf8').split('\n')
  lines.forEach((line, i) => {
    const trimmed = line.trim()
    if (!trimmed || trimmed.startsWith('//')) return
    try {
      records.push(JSON.parse(trimmed))
    } catch (e) {
      errors.push({ line: i + 1, message: e.message })
    }
  })
  return { records, errors, missing: false }
}

export function writeReport(relPath, content) {
  const abs = join(ROOT, relPath)
  mkdirSync(dirname(abs), { recursive: true })
  writeFileSync(abs, content.endsWith('\n') ? content : content + '\n', 'utf8')
  return abs
}

export function nowISODate() {
  return new Date().toISOString().slice(0, 10)
}

export function containsBannedClaim(text) {
  if (!text) return null
  for (const re of BANNED_CLAIM_PATTERNS) {
    if (re.test(text)) return re.source
  }
  return null
}

// Deterministic, explainable draft scoring. We never trust a stored score; the
// gate recomputes from the draft's own fields so the rubric is auditable.
export function scoreDraft(draft, sys) {
  const b = {}
  const body = String(draft.email_body || '')
  const subject = String(draft.subject || '')
  const company = String(draft.company || '')

  // Personalization (25): company named in body, plus concrete context fields.
  let p = 0
  if (company && body.includes(company)) p += 12
  if (draft.signal && String(draft.signal).length > 8) p += 7
  if (draft.sector || draft.city) p += 6
  b.personalization = Math.min(p, RUBRIC.personalization)

  // Pain clarity (20): a real likely_pain that the body actually echoes.
  let pc = 0
  const pain = String(draft.likely_pain || '')
  if (pain.length > 10) pc += 12
  if (pain && (body.includes(pain.slice(0, 6)) || /متابعة|إيراد|عرض|قرار|واتساب|فرص/.test(body))) pc += 8
  b.pain_clarity = Math.min(pc, RUBRIC.pain_clarity)

  // System fit (20): valid system + a reason tied to it.
  let sf = 0
  if (SYSTEM_IDS.includes(draft.recommended_system)) sf += 12
  if (draft.why_this_system && String(draft.why_this_system).length > 12) sf += 8
  b.system_fit = Math.min(sf, RUBRIC.system_fit)

  // CTA clarity (15): a CTA that asks for one clear, low-friction next step.
  let cta = 0
  const ctaText = String(draft.cta || '')
  if (ctaText.length > 4) cta += 8
  if (CTA_KEYWORDS.some((k) => ctaText.includes(k) || body.includes(k))) cta += 7
  b.cta_clarity = Math.min(cta, RUBRIC.cta_clarity)

  // Risk safety (10): no guarantee language, risk level present, evidence honest.
  let rs = RUBRIC.risk_safety
  if (containsBannedClaim(body) || containsBannedClaim(subject)) rs -= 10
  if (!draft.risk_level) rs -= 3
  // L0/L1 evidence must not be phrased with certainty markers.
  if (['L0', 'L1'].includes(draft.evidence_level) && /\b(سوف نزيد|سنزيد|بالتأكيد|قطعًا)\b/.test(body)) rs -= 4
  b.risk_safety = Math.max(rs, 0)

  // Tone quality (10): sane length, not shouty, not spammy.
  let tone = RUBRIC.tone_quality
  const len = body.length
  if (len < 120 || len > 1400) tone -= 4
  if ((body.match(/!/g) || []).length > 3) tone -= 3
  if (/[A-Z]{6,}/.test(body)) tone -= 3
  b.tone_quality = Math.max(tone, 0)

  const score = Object.values(b).reduce((a, c) => a + c, 0)
  return { score, breakdown: b, system: sys ? sys.name_en : draft.recommended_system }
}

export function pct(n, d) {
  if (!d) return '0%'
  return Math.round((n / d) * 100) + '%'
}

// List schema files so the control check can prove they all parse.
export function listSchemas() {
  const dir = join(ROOT, 'schemas')
  if (!existsSync(dir)) return []
  return readdirSync(dir).filter((f) => f.endsWith('.json'))
}
