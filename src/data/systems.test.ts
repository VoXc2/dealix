import { readFileSync } from 'node:fs'
import { describe, it, expect } from 'vitest'
import { SYSTEMS } from './systems'

// Guards the display registry (src/data/systems.ts) against drift from the
// canonical operational registry (data/systems.json) consumed by the scripts.
const registry = JSON.parse(readFileSync(new URL('../../data/systems.json', import.meta.url), 'utf8')) as {
  daily_draft_total: number
  systems: Array<{ id: string; name_en: string; customer: { starting_price_sar: number } }>
}

describe('systems registry consistency', () => {
  it('exposes exactly five systems', () => {
    expect(SYSTEMS).toHaveLength(5)
    expect(registry.systems).toHaveLength(5)
  })

  it('matches ids, names, and starting prices with data/systems.json', () => {
    for (const json of registry.systems) {
      const ts = SYSTEMS.find((s) => s.id === json.id)
      expect(ts, `missing system ${json.id} in src/data/systems.ts`).toBeDefined()
      expect(ts!.nameEn).toBe(json.name_en)
      expect(ts!.startingPriceSar).toBe(json.customer.starting_price_sar)
    }
  })

  it('has non-empty required content blocks for every system', () => {
    for (const s of SYSTEMS) {
      expect(s.benefitsAr.length).toBeGreaterThan(0)
      expect(s.deliveryPackAr.length).toBeGreaterThan(0)
      expect(s.requiredInputsAr.length).toBeGreaterThan(0)
      expect(s.acceptanceCriteriaAr.length).toBeGreaterThan(0)
      expect(s.faqAr.length).toBeGreaterThan(0)
      expect(s.startingPriceSar).toBeGreaterThan(0)
    }
  })

  it('contains no guarantee-style claims in customer copy', () => {
    const banned = /نضمن|مضمون|نضاعف/
    for (const s of SYSTEMS) {
      const copy = [s.taglineAr, s.painAr, s.whoAr, ...s.benefitsAr, s.firstResultAr].join(' ')
      expect(banned.test(copy), `guarantee-style claim in ${s.id}`).toBe(false)
    }
  })
})
