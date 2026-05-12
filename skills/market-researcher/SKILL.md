# Market Researcher

Builds a brief on a target Saudi B2B account by chaining
Wathq → Tadawul → Etimad → web-search (Crawl4AI / Firecrawl) → LLM
synthesis. The first three are Saudi-sovereign sources — moat.

## Output

```yaml
company_name_ar: string
company_name_en: string
cr_number: string | null
vat_number: string | null
sector: string
hq_city: string
estimated_headcount_band: string
recent_signals:
  - source: string
    headline: string
    url: string
    detected_at: ISO
hiring_pulse: low | medium | high | unknown
public_listings: [string]   # Etimad tender ids
risk_flags: [string]
```
